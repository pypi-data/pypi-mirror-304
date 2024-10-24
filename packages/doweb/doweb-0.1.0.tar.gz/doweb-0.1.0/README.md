# doweb 0.1.0

KLayout Web Viewer ![demo](docs/_static/doweb.png)

Based on https://github.com/klayoutmatthias/canvas2canvas

## Install & Run

### Through pypi

From a python virtual environment run:

```bash
python -m pip install doweb
export DOWEB_FILESLOCATION="/path/to/gds/folder" # or the windows equivalent with set
uvicorn --reload doweb.default:app
````

#### Advanced Usage

KWeb offers two basic apps:

- Browser:

  A version that provides a version with a file browser for a folder and the doweb viewer for viewing the gds file in that folder.
  This can be used by importing the function `doweb.browser.get_app` and settings the `DOWEB_FILESLOCATION` env variable of passing
  `fileslocation=<Path object for target folder>` to the function. Alternatively there is a default one in `doweb.default.app` that
  will only look for the env variable.

- Viewer:

  Only enables the `/gds/<filename>` endpoints, no root path, i.e. no file browser. Available at `doweb.viewer.get_app`. This version
  doesn't provide a listener for the env variable. Use the `fileslocation` parameter in the function instead.

### Development

#### Clone & Install


```bash
# Clone the repository to your local
git clone https://github.com/gdsfactory/doweb.git
# Install the necessary dependencies
cd /doweb
python -m pip install -e .[dev]
```

#### Set a folder for doweb to use when looking for gds files

```bash
export DOWEB_FILESLOCATION=/path/to/folder/with/gdsfiles
```

#### Run

```bash
cd src/doweb
uvicorn --reload default:app
```

Copy the link http://127.0.1.0:8000/gds/file.gds (or http://localhost:8000/gds/file.gds also works) to your browser to open the waveguide example


#### Contributing

Please make sure you have also installed pre-commit before committing:

```bash
python -m pip install pre-commit
pre-commit install
```
