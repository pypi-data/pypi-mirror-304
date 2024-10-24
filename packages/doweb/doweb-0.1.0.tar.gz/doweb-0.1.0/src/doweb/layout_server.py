from __future__ import annotations

import asyncio
import base64
import json
from collections.abc import Callable
from collections import defaultdict
from pathlib import Path
from typing import Any, TypeAlias, Literal, TypedDict
from urllib.parse import parse_qs

# NOTE: import db to enable stream format readers
import klayout.db as db
import klayout.lay as lay
import klayout.rdb as rdb
from fastapi import WebSocket
from starlette.endpoints import WebSocketEndpoint
from typing import Iterator
from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color
from functools import cache

port = 8765
host = "localhost"

CellDict: TypeAlias = "dict[str, int | str | list[CellDict]]"

markers: list[lay.Marker] = []


class MarkerCategory(BaseModel):
    color: int
    dither_pattern: int
    frame_color: int
    halo: int
    line_style: int
    line_width: int

    def __init__(
        self,
        color: int | str | tuple[int, int, int] = "red",
        dither_pattern: int = 5,
        frame_color: int | str | tuple[int, int, int] = "blue",
        halo: Literal[-1, 0, 1] = -1,
        line_style: int = 0,
        line_width: int = 1,
    ):
        if isinstance(color, int):
            color = (color % 256**3, color % 256**2, color % 256)
        super().__init__(
            color=int(Color(color).as_hex(format="long")[1:], 16),
            dither_pattern=dither_pattern,
            frame_color=int(Color(color).as_hex(format="long")[1:], 16),
            halo=halo,
            line_style=line_style,
            line_width=line_width,
        )


class ItemMarkerGroup:
    markers: list[lay.Marker] = Field(default_factory=list)

    def clear(self) -> None:
        self.markers = []

    def add_item(
        self,
        item: rdb.RdbItem,
        category: MarkerCategory,
        bbox: db.DBox,
        lv: lay.LayoutView,
    ) -> db.DBox:
        def get_marker() -> lay.Marker:
            m = lay.Marker(lv)
            m.dither_pattern = category.dither_pattern
            m.color = category.color
            m.frame_color = category.frame_color
            m.halo = category.halo
            m.line_style = category.line_style
            m.line_width = category.line_width
            self.markers.append(m)
            return m

        for value in item.each_value():
            if value.is_box():
                box = value.box()
                m = get_marker()
                m.set_box(box)
                bbox += box
            if value.is_edge():
                edge = value.edge()
                m = get_marker()
                m.set_edge(edge)
                bbox += edge.bbox()
            if value.is_edge_pair():
                ep = value.edge_pair()
                m1 = get_marker()
                m1.set_edge(ep.first)
                m2 = get_marker()
                m2.set_edge(ep.second)
                mp = get_marker()
                mp.line_width = 0
                mp.set_polygon(ep.polygon(0))
                bbox += ep.bbox()
            if value.is_path():
                path = value.path()
                m = get_marker()
                m.set_path(path)
                bbox += path.bbox()
            if value.is_polygon():
                polygon = value.polygon()
                m = get_marker()
                m.set_polygon(polygon)
                bbox += polygon.bbox()
        return bbox


class LayoutViewServerEndpoint(WebSocketEndpoint):
    editable: bool = False
    add_missing_layers: bool = True
    meta_splitter: str
    root: Path
    max_rdb_limit: int = 100

    def __init_subclass__(
        cls,
        root: Path,
        editable: bool = False,
        add_missing_layers: bool = True,
        meta_splitter: str = ":",
        max_rdb_limit: int = 100,
        **kwargs: Any,
    ):
        super().__init_subclass__(**kwargs)
        cls.editable = editable
        cls.add_missing_layers = add_missing_layers
        cls.meta_splitter = meta_splitter
        cls.root = root
        cls.max_rdb_limit = max_rdb_limit

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        params = parse_qs(self.scope["query_string"].decode("utf-8"))
        self.url = str(self.root / params["file"][0])
        self.layer_props = params.get("layer_props", [None])[0]
        if self.layer_props:
            self.layer_props = str(self.root / self.layer_props)
        self.rdb_file = params.get("rdb", [None])[0]
        if self.rdb_file:
            self.rdb_file = str(self.root / self.rdb_file)
        self.initial_cell = params.get("cell", [None])[0]
        self.db = rdb.ReportDatabase("dowebrdb")
        self.rdb_items: dict[int, rdb.RdbItem] = {}
        self.cell_map: dict[int, db.Cell | None] = {}
        self.rdb_layer: int = -1  # place holder until initialization

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        await self.connection(websocket)

    async def on_receive(self, websocket: WebSocket, data: str) -> None:
        await self.reader(websocket, data)

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        pass

    async def send_image(self, websocket: WebSocket, data: bytes) -> None:
        await websocket.send_bytes(data)

    def image_updated(self, websocket: WebSocket) -> None:
        pixel_buffer = self.layout_view.get_screenshot_pixels()
        asyncio.create_task(self.send_image(websocket, pixel_buffer.to_png_data()))

    def mode_dump(self) -> list[str]:
        return self.layout_view.mode_names()

    def annotation_dump(self) -> list[str]:
        return [d[1] for d in self.layout_view.annotation_templates()]

    def current_cell(self) -> db.Cell:
        cv = self.layout_view.active_cellview()
        ci = cv.cell_index
        return cv.layout().cell(ci)

    async def set_current_cell(self, ci: int | str, websocket: WebSocket) -> None:
        cell = self.layout_view.active_cellview().layout().cell(ci)
        self.layout_view.active_cellview().cell = cell
        self.layout_view.max_hier()
        self.layout_view.clear_markers()
        await self.send_metainfo(
            cell=cell, websocket=websocket, splitter=self.meta_splitter
        )

    async def send_metainfo(
        self,
        cell: db.Cell,
        websocket: WebSocket,
        splitter: str | None,
    ) -> None:
        metainfo: Any = {}

        flat = False
        if splitter is not None:
            for m in cell.each_meta_info():
                keys = m.name.split(splitter)
                d: Any = metainfo
                for key in keys[:-1]:
                    if key not in d:
                        d[key] = {}
                    if not isinstance(d[key], dict):
                        flat = True
                        break
                    else:
                        d = d[key]
                d[keys[-1]] = m.value

                if flat:
                    break
        if flat:
            for m in cell.each_meta_info():
                metainfo[m.name] = m.value

        await websocket.send_text(
            json.dumps(
                {
                    "msg": "metainfo",
                    "metainfo": metainfo,
                },
                default=meta_json_serializer,
            )
        )

    def layer_dump(
        self,
        iter: lay.LayerPropertiesIterator | None = None,
        end_iter: lay.LayerPropertiesIterator | None = None,
    ) -> list[dict[str, object]]:
        if iter is None:
            iter = self.layout_view.begin_layers()
        js = []
        # for layer in self.layout_view.each_layer():
        if end_iter:
            while not iter.at_end() and iter != end_iter:
                layer = iter.current()
                if layer.has_children():
                    children = self.layer_dump(
                        iter=iter.dup().down_first_child(),
                        end_iter=iter.dup().down_last_child(),
                    )
                    js.append(
                        {
                            "dp": layer.eff_dither_pattern(),
                            "ls": layer.eff_line_style(),
                            "c": layer.eff_fill_color(),
                            "fc": layer.eff_frame_color(),
                            "m": layer.marked,
                            "s": layer.source,
                            "t": layer.transparent,
                            "va": layer.valid,
                            "v": layer.visible,
                            "w": layer.width,
                            "x": layer.xfill,
                            "name": layer.name,
                            "id": layer.id(),
                            "img": base64.b64encode(
                                self.layout_view.icon_for_layer(
                                    iter, 30, 12, 1
                                ).to_png_data()
                            ).decode("ASCII"),
                            "children": children,
                            "empty": all(c["empty"] for c in children),
                        }
                    )
                    iter.next_sibling(1)
                else:
                    js.append(
                        {
                            "dp": layer.eff_dither_pattern(),
                            "ls": layer.eff_line_style(),
                            "c": layer.eff_fill_color(),
                            "fc": layer.eff_frame_color(),
                            "m": layer.marked,
                            "s": layer.source,
                            "t": layer.transparent,
                            "va": layer.valid,
                            "v": layer.visible,
                            "w": layer.width,
                            "x": layer.xfill,
                            "name": layer.name,
                            "id": layer.id(),
                            "img": base64.b64encode(
                                self.layout_view.icon_for_layer(
                                    iter, 30, 12, 1
                                ).to_png_data()
                            ).decode("ASCII"),
                            "empty": self.current_cell()
                            .bbox_per_layer(layer.layer_index())
                            .empty(),
                        }
                    )
                    iter.next_sibling(1)
        else:
            while not iter.at_end():
                layer = iter.current()
                if layer.has_children():
                    children = self.layer_dump(
                        iter=iter.dup().down_first_child(),
                        end_iter=iter.dup().down_last_child(),
                    )
                    js.append(
                        {
                            "dp": layer.eff_dither_pattern(),
                            "ls": layer.eff_line_style(),
                            "c": layer.eff_fill_color(),
                            "fc": layer.eff_frame_color(),
                            "m": layer.marked,
                            "s": layer.source,
                            "t": layer.transparent,
                            "va": layer.valid,
                            "v": layer.visible,
                            "w": layer.width,
                            "x": layer.xfill,
                            "name": layer.name,
                            "id": layer.id(),
                            "img": base64.b64encode(
                                self.layout_view.icon_for_layer(
                                    iter, 30, 12, 1
                                ).to_png_data()
                            ).decode("ASCII"),
                            "children": children,
                            "empty": all(c["empty"] for c in children),
                        }
                    )
                    iter.next_sibling(1)
                else:
                    js.append(
                        {
                            "dp": layer.eff_dither_pattern(),
                            "ls": layer.eff_line_style(),
                            "c": layer.eff_fill_color(),
                            "fc": layer.eff_frame_color(),
                            "m": layer.marked,
                            "s": layer.source,
                            "t": layer.transparent,
                            "va": layer.valid,
                            "v": layer.visible,
                            "w": layer.width,
                            "x": layer.xfill,
                            "name": layer.name,
                            "id": layer.id(),
                            "img": base64.b64encode(
                                self.layout_view.icon_for_layer(
                                    iter, 30, 12, 1
                                ).to_png_data()
                            ).decode("ASCII"),
                            "empty": self.current_cell()
                            .bbox_per_layer(layer.layer_index())
                            .empty(),
                        }
                    )
                    iter.next_sibling(1)

        return js

    def hierarchy_dump(self) -> list[CellDict]:
        layout = self.layout_view.active_cellview().layout()
        top_cells = layout.top_cells()

        def get_children(cell: db.Cell) -> list[CellDict]:
            if not cell.child_cells():
                return []
            children: list[CellDict] = []
            iter = cell.each_child_cell()
            for child_idx in iter:
                child = layout.cell(child_idx)
                children.append(
                    {
                        "name": child.name,
                        "id": child.cell_index(),
                        "children": get_children(child),
                    }
                )
            return children

        return [
            {
                "name": top_cell.name,
                "id": top_cell.cell_index(),
                "children": get_children(top_cell),
            }
            for top_cell in top_cells
        ]

    async def send_hierarchy(self, websocket: WebSocket) -> None:
        await websocket.send_text(
            json.dumps(
                {
                    "msg": "hierarchy",
                    "hierarchy": self.hierarchy_dump(),
                    "ci": self.current_cell().cell_index(),
                }
            )
        )

    async def draw_items(self, items: dict[int, bool]) -> None:
        dbbox = db.DBox()
        self.marker_group.clear()
        for index, selected in items.items():
            if selected:
                item = self.rdb_items[int(index)]
                dbbox = self.marker_group.add_item(
                    item=item,
                    category=self.marker_categories[item.category_id()],
                    bbox=dbbox,
                    lv=self.layout_view,
                )
        dbbox.enlarge(dbbox.width() * 0.1, dbbox.height() * 0.1)
        self.layout_view.zoom_box(dbbox)

    async def connection(self, websocket: WebSocket, path: str | None = None) -> None:
        self.layout_view = lay.LayoutView(self.editable)
        self.marker_group = ItemMarkerGroup()
        self.marker_categories: dict[int, MarkerCategory] = defaultdict(MarkerCategory)
        self.layout_view.load_layout(self.url)
        self.rdb_layer = self.layout_view.active_cellview().layout().layer("RDB View")
        self.layout_view.add_missing_layers()
        if self.layer_props and Path(self.layer_props).is_file():
            try:
                self.layout_view.load_layer_props(self.layer_props)
            except RuntimeError as e:
                await websocket.send_text(
                    json.dumps(
                        {
                            "msg": "error",
                            "details": "Error loading layper properties file (.lyp)\nError:\n"
                            + str(e),
                        }
                    )
                )
                self.layer_props = None
        if self.initial_cell:
            await self.set_current_cell(self.initial_cell, websocket)
            self.layout_view.zoom_fit()
        loaded_rdb = False
        if self.rdb_file:
            ly = self.layout_view.active_cellview().layout()
            try:
                self.db.load(self.rdb_file)
                loaded_rdb = True
                self.cell_map = {
                    cell.rdb_id(): ly.cell(cell.qname()) for cell in self.db.each_cell()
                }
            except RuntimeError as e:
                await websocket.send_text(
                    json.dumps(
                        {
                            "msg": "error",
                            "details": "Error loading rdb file\nError:\n" + str(e),
                        }
                    )
                )
                self.rdb_file = None
        if self.add_missing_layers:
            self.layout_view.add_missing_layers()
        self.layout_view.max_hier()

        if self.layout_view.active_cellview().layout().cells():
            await self._send_loaded(
                websocket=websocket,
                cell_index=self.current_cell().cell_index(),
            )
            await self.send_metainfo(
                cell=self.current_cell(),
                websocket=websocket,
                splitter=self.meta_splitter,
            )
        else:
            await self._send_loaded(
                websocket=websocket,
                cell_index=0,
            )

        if loaded_rdb:
            d: dict[str, int] = {}
            for cat in self.db.each_category():
                await update_cats(d, cat)
            await websocket.send_text(
                json.dumps(
                    {
                        "msg": "rdbinfo",
                        "rdbinfo": {
                            "categories": d,
                            "cells": {
                                cell.qname(): cell.rdb_id()
                                for cell in self.db.each_cell()
                                if cell.num_items()
                            },
                        },
                    }
                )
            )

        asyncio.create_task(self.timer(websocket))

    async def get_records(
        self, category_id: int | None, cell_id: int | None
    ) -> Iterator[rdb.RdbItem]:
        if category_id is not None and cell_id is not None:
            return self.db.each_item_per_cell_and_category(cell_id, category_id)
        if category_id is not None:
            return self.db.each_item_per_category(category_id)
        if cell_id is not None:
            return self.db.each_item_per_cell(cell_id)
        return self.db.each_item()

    async def timer(self, websocket: WebSocket) -> None:
        def update() -> None:
            self.image_updated(websocket)

        self.layout_view.on_image_updated_event = update  # type: ignore[assignment]
        while True:
            self.layout_view.timer()
            await asyncio.sleep(0.01)

    def buttons_from_js(self, js: dict[str, int]) -> int:
        buttons = 0
        k = js["k"]
        b = js["b"]
        if (k & 1) != 0:
            buttons |= lay.ButtonState.ShiftKey
        if (k & 2) != 0:
            buttons |= lay.ButtonState.ControlKey
        if (k & 4) != 0:
            buttons |= lay.ButtonState.AltKey
        if (b & 1) != 0:
            buttons |= lay.ButtonState.LeftButton
        if (b & 2) != 0:
            buttons |= lay.ButtonState.RightButton
        if (b & 4) != 0:
            buttons |= lay.ButtonState.MidButton
        return buttons

    def wheel_event(
        self, function: Callable[[int, bool, db.DPoint, int], None], js: dict[str, int]
    ) -> None:
        delta = 0
        dx = js["dx"]
        dy = js["dy"]
        if dx != 0:
            delta = -dx
            horizontal = True
        elif dy != 0:
            delta = -dy
            horizontal = False
        if delta != 0:
            function(
                delta, horizontal, db.DPoint(js["x"], js["y"]), self.buttons_from_js(js)
            )

    def mouse_event(
        self, function: Callable[[db.DPoint, int], None], js: dict[str, int]
    ) -> None:
        function(db.DPoint(js["x"], js["y"]), self.buttons_from_js(js))

    def key_event(self, js: dict[str, int]) -> None:
        match js["k"]:
            case 27:
                mode = self.layout_view.mode_name()
                self.layout_view.switch_mode("select")
                self.layout_view.switch_mode(mode)

    async def reader(self, websocket: WebSocket, data: str) -> None:
        js = json.loads(data)
        msg = js["msg"]
        match msg:
            case "quit":
                return
            case "resize":
                self.layout_view.resize(js["width"], js["height"])
            case "clear-annotations":
                self.layout_view.clear_annotations()
            case "select-ruler":
                ruler = js["value"]
                self.layout_view.set_config("current-ruler-template", str(ruler))
            case "select-mode":
                mode = js["value"]
                self.layout_view.switch_mode(mode)
            case "layer-v-all":
                vis = js["value"]
                for layer in self.layout_view.each_layer():
                    layer.visible = vis
            case "layer-v":
                id = js["id"]
                vis = js["value"]
                iter = self.layout_view.begin_layers()
                end = False
                while not (iter.at_end() or end):
                    layer = iter.current()
                    if layer.id() == id:
                        layer.visible = vis
                        nit = iter.dup()
                        nit.next_sibling(1)
                        await websocket.send_text(
                            json.dumps(
                                {
                                    "msg": "layer-u",
                                    "layers": self.layer_dump(iter.dup(), end_iter=nit),
                                }
                            )
                        )
                        end = True
                    iter.next()

            case "initialize":
                self.layout_view.resize(js["width"], js["height"])
                await websocket.send_text(json.dumps({"msg": "initialized"}))
            case "mode_select":
                self.layout_view.switch_mode(js["mode"])
            case "mouse_move":
                self.mouse_event(self.layout_view.send_mouse_move_event, js)
            case "mouse_pressed":
                self.mouse_event(
                    self.layout_view.send_mouse_press_event,
                    js,
                )
            case "mouse_released":
                self.mouse_event(
                    self.layout_view.send_mouse_release_event,
                    js,
                )
            case "mouse_enter":
                self.layout_view.send_enter_event()
            case "mouse_leave":
                self.layout_view.send_leave_event()
            case "mouse_dblclick":
                self.mouse_event(
                    self.layout_view.send_mouse_double_clicked_event,
                    js,
                )
            case "wheel":
                self.wheel_event(self.layout_view.send_wheel_event, js)
            case "keydown":
                self.key_event(js)
            case "ci-s":
                await self.set_current_cell(js["ci"], websocket)
                self.layout_view.zoom_fit()
            case "cell-s":
                await self.set_current_cell(js["cell"], websocket)
                self.layout_view.zoom_fit()
            case "show-ports":
                hierarchy = js["hierarchy"]
                match hierarchy:
                    case 0, 0:
                        self.layout_view.clear_markers()
                        await self.show_ports(self.current_cell())
                    case -1, -1:
                        self.layout_view.clear_markers()
                    case x, -1:
                        print(f"showing ports with hierarchy {x=} and below")
                        await self.show_ports(self.current_cell(), recursive=True)
            case "zoom-f":
                self.layout_view.zoom_fit()
            case "rdb-records":
                item_iter = await self.get_records(
                    category_id=js["category_id"], cell_id=js["cell_id"]
                )
                self.rdb_items = {
                    i: item for i, item in zip(range(self.max_rdb_limit), item_iter)
                }
                await websocket.send_json(
                    {
                        "msg": "rdb-items",
                        "items": {
                            i: item.tags_str or "<no tags>"
                            for i, item in self.rdb_items.items()
                        },
                    }
                )
            case "rdb-selected":
                await self.draw_items(js["items"])
            case "reload":
                cname = self.current_cell().name
                self.layout_view.reload_layout(
                    self.layout_view.active_cellview().index()
                )
                c = self.layout_view.active_cellview().layout().cell(cname)
                if c is None:
                    tcs = self.layout_view.active_cellview().layout().top_cells()
                    if len(tcs) > 0:
                        c = tcs[0]

                ci = 0
                if c is not None:
                    ci = c.cell_index()
                await self.set_current_cell(ci, websocket=websocket)
                if self.rdb_file is not None:
                    self.db.load(self.rdb_file)

                await self._send_reloaded(
                    websocket=websocket,
                    cell_index=self.current_cell().cell_index(),
                )

    async def _send_loaded(self, websocket: WebSocket, cell_index: int = 0) -> None:
        await websocket.send_json(
            {
                "msg": "loaded",
                "modes": self.mode_dump(),
                "annotations": self.annotation_dump(),
                "layers": self.layer_dump(),
                "hierarchy": self.hierarchy_dump(),
                "ci": cell_index,
            }
        )

    async def _send_reloaded(self, websocket: WebSocket, cell_index: int = 0) -> None:
        await websocket.send_json(
            {
                "msg": "reloaded",
                "layers": self.layer_dump(),
                "hierarchy": self.hierarchy_dump(),
                "ci": cell_index,
            }
        )

    async def show_ports(self, cell: db.Cell, recursive: bool = False) -> None:
        self.layout_view.clear_markers()
        await self.show_ports_subcell(cell)
        if recursive:
            for it in cell.begin_instances_rec().each():
                await self.show_ports_subcell(
                    it.inst_cell(), it.dtrans() * it.inst_dtrans()
                )

    async def show_ports_subcell(
        self, cell: db.Cell, trans: db.DCplxTrans = db.DCplxTrans()
    ) -> None:
        print("showing ports of " + cell.name)
        ports_meta: dict[str, dict[str, Any]] = defaultdict(dict)
        ly = cell.layout()
        for m in cell.each_meta_info():
            if m.name.startswith("kfactory:ports:"):
                p_index = m.name.removeprefix("kfactory:ports:")
                ports_meta[p_index] = m.value

                ports_meta[p_index]["width"] = ly.meta_info_value(
                    "kfactory:cross_section:" + m.value["cross_section"]
                )["width"]

        for _, vdict in sorted(ports_meta.items()):
            if "dcplx_trans" in vdict:
                dcplx_trans: db.DCplxTrans = vdict["dcplx_trans"]
                poly = port_poly(vdict["width"] * cell.layout().dbu).transformed(
                    trans * dcplx_trans
                )
                marker = lay.Marker()
                marker.set_polygon(poly)
            else:
                dcplx_trans = db.DCplxTrans(vdict["trans"].to_dtype(cell.layout().dbu))
                poly = port_poly(vdict["width"] * cell.layout().dbu).transformed(
                    trans * dcplx_trans
                )
                marker = lay.Marker()
                marker.set_polygon(poly)

            marker.color = 0x00FF00
            marker.dither_pattern = 3
            marker.frame_color = 0x00FF00
            self.layout_view.add_marker(marker)
            if "name" in vdict:
                marker2 = lay.Marker()
                marker2.color = 0x00FF00
                marker2.dither_pattern = 3
                marker2.frame_color = 0x00FF00
                dtrans = dcplx_trans.s_trans()
                match dtrans.angle:
                    case 0:
                        ha = db.Text.HAlignRight
                        va = db.Text.VAlignCenter
                    case 1:
                        ha = db.Text.HAlignCenter
                        va = db.Text.VAlignTop
                    case 2:
                        ha = db.Text.HAlignLeft
                        va = db.Text.VAlignCenter
                    case _:
                        ha = db.Text.HAlignCenter
                        va = db.Text.VAlignBottom

                t = db.DText(vdict["name"], trans.s_trans() * dtrans)
                t.valign = va
                t.halign = ha
                marker2.set_text(t)
                self.layout_view.add_marker(marker2)


def meta_json_serializer(obj: object) -> str:
    return str(obj)


@cache
def port_poly(dwidth: float) -> db.DPolygon:
    poly = db.DPolygon(
        [
            db.DPoint(0, dwidth / 2),
            db.DPoint(0, -dwidth / 2),
            db.DPoint(dwidth / 2, 0),
        ]
    )
    hole = db.DPolygon(
        [
            db.DPoint(0.05 * dwidth / 2 * 0.71, 0),
            db.DPoint(0.95 * dwidth / 2, 0),
            db.DPoint(0.05 * dwidth / 2 * 0.71, (0.95 - 0.05 * 0.71) * dwidth / 2),
        ]
    )
    poly.insert_hole(list(hole.each_point_hull()))
    return poly


class PortDict(TypedDict):
    dwidth: float
    dcplx_trans: db.DCplxTrans


@cache
def cell_ports(cell: db.Cell) -> dict[str, PortDict]:
    ports_dict: dict[str, Any] = defaultdict(dict)
    ports: dict[str, PortDict] = {}
    for meta in cell.each_meta_info():
        if meta.name.startswith("kfactory:ports:"):
            ind, mn = meta.name.removeprefix("kfactory:ports:").split(
                ":",
            )
            ports_dict[ind][mn] = meta.value
    for p in sorted(ports_dict):
        port_dict = ports_dict[p]
        ports[port_dict["name"]] = PortDict(
            dwidth=cell.layout().dbu * port_dict["width"],
            dcplx_trans=db.DCplxTrans(port_dict["trans"].to_dtype(cell.layout().dbu))
            if "trans" in port_dict
            else port_dict["dcplx_trans"],
        )
    return ports


def nl2shapes(netlist: db.Netlist, cell: db.Cell) -> list[lay.Marker]:
    circ = netlist.circuit_by_cell_index(cell.cell_index())

    if circ is not None:
        ports = cell_ports(cell)
        sub_cells = {
            c: cell_ports(cell.layout().cell(c)) for c in cell.each_child_cell()
        }
        for net in circ.each_net():
            _cell_ports = [ports[pin.pin().name()] for pin in net.each_pin()]
            subcell_ports = [
                sub_cells[sp.subcircuit().circuit().cell_index][sp.pin().name()]
                for sp in net.each_subcircuit_pin()
            ]
            center = db.DVector()
            for port in _cell_ports:
                center += port["dcplx_trans"].disp
            for port in subcell_ports:
                center += port["dcplx_trans"].disp
            center /= len(_cell_ports) + len(subcell_ports)
            if center == (_cell_ports + subcell_ports)[0]["dcplx_trans"].disp:
                markers = []
                for port in _cell_ports:
                    m = lay.Marker()
                    m.color = 0x00FF00
                    m.set_edge(
                        db.DEdge(
                            0, -port["dwidth"] / 2, 0, port["dwidth"] / 2
                        ).transformed(port["dcplx_trans"])
                    )
                    m.dither_pattern = 2
                    m.line_style = 2
                    markers.append(m)
                for port in subcell_ports:
                    m = lay.Marker()
                    m.color = 0xFF0000
                    m.set_edge(
                        db.DEdge(
                            0, -port["dwidth"] / 2, 0, port["dwidth"] / 2
                        ).transformed(port["dcplx_trans"])
                    )
                    m.dither_pattern = 1
                    m.line_style = 1
                    markers.append(m)
                return markers
            else:
                markers = []
                for port in _cell_ports:
                    m = lay.Marker()
                    m.color = 0x00FF00
                    m.set_edge(
                        db.DEdge(
                            0, -port["dwidth"] / 2, 0, port["dwidth"] / 2
                        ).transformed(port["dcplx_trans"])
                    )
                    m.dither_pattern = 2
                    m.line_style = 2
                    markers.append(m)
                for port in subcell_ports:
                    m = lay.Marker()
                    m.color = 0xFF0000
                    m.set_edge(
                        db.DEdge(
                            0, -port["dwidth"] / 2, 0, port["dwidth"] / 2
                        ).transformed(port["dcplx_trans"])
                    )
                    m.dither_pattern = 1
                    m.line_style = 1
                    markers.append(m)
                return markers

    return []


async def update_cats(d: dict[str, int], category: rdb.RdbCategory) -> None:
    has_items = False
    for it in category.each_item():
        has_items = True
        break
    if has_items:
        d[category.path()] = category.rdb_id()
    for subcat in category.each_sub_category():
        await update_cats(d, subcat)
