# RGV Business Case

RGV business case repository - Nov, 2026.

## Setup

Follow these steps in a terminal after cloning the repository. The commands below assume the repository folder is named `rgv_business_case`; if yours has a different name, use that folder name instead.

### 1. Clone the repository and enter its folder

Replace `<repository-url>` with the URL for this repository:

```bash
git clone <repository-url>
cd rgv_business_case
```

If you have already cloned the repository, just open a terminal in its folder (the folder containing `requirements.txt`) and continue.

### 2. Create a virtual environment

Use Python 3.9 or newer. Check that Python is installed:

```bash
python3 --version
```

Create a project-local virtual environment:

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

Choose the command for your terminal:

**macOS or Linux (bash/zsh):**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```bat
.venv\Scripts\activate.bat
```

When activated, your terminal prompt normally shows `(.venv)`.

### 4. Install the project libraries

Upgrade pip, then install the exact package versions listed in `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Start JupyterLab

The repository includes a Jupyter notebook. To start JupyterLab from the repository folder:

```bash
jupyter lab
```

Open `map_kepler.ipynb` in the JupyterLab browser tab.

### 6. Deactivate the virtual environment when finished

```bash
deactivate
```

To work on the project again, open a terminal in the repository folder and activate `.venv` using the command for your operating system above.

## Libraries

The following pinned dependencies are installed by the `pip install -r requirements.txt` command above. `requirements.txt` is the authoritative source for package versions.

**Data and geospatial:** `geoarrow-c`, `geoarrow-pandas`, `geoarrow-pyarrow`, `geoarrow-types`, `geopandas`, `keplergl`, `numpy`, `pandas`, `pyarrow`, `pyogrio`, `pyproj`, `shapely`

**Jupyter and interactive computing:** `anywidget`, `ipykernel`, `ipython`, `ipywidgets`, `jupyter`, `jupyter-console`, `jupyter-events`, `jupyter-lsp`, `jupyter_client`, `jupyter_core`, `jupyter_server`, `jupyter_server_terminals`, `jupyterlab`, `jupyterlab_pygments`, `jupyterlab_server`, `jupyterlab_widgets`, `nbclient`, `nbconvert`, `nbformat`, `notebook`, `notebook_shim`, `widgetsnbextension`

**Plotting and images:** `contourpy`, `cycler`, `fonttools`, `kiwisolver`, `matplotlib`, `matplotlib-inline`, `pillow`, `pyparsing`

**Web, networking, and serialization:** `anyio`, `async-lru`, `beautifulsoup4`, `bleach`, `h11`, `httpcore`, `httpx`, `idna`, `isoduration`, `json5`, `jsonpointer`, `jsonschema`, `jsonschema-specifications`, `requests`, `rfc3339-validator`, `rfc3986-validator`, `rfc3987-syntax`, `soupsieve`, `tinycss2`, `uri-template`, `urllib3`, `webcolors`, `webencodings`, `websocket-client`

**Python utilities and support packages:** `appnope`, `argon2-cffi`, `argon2-cffi-bindings`, `arrow`, `asttokens`, `attrs`, `babel`, `certifi`, `cffi`, `charset-normalizer`, `comm`, `debugpy`, `decorator`, `defusedxml`, `exceptiongroup`, `executing`, `fastjsonschema`, `fqdn`, `importlib_metadata`, `importlib_resources`, `jedi`, `Jinja2`, `lark`, `MarkupSafe`, `mistune`, `nest-asyncio`, `overrides`, `packaging`, `pandocfilters`, `parso`, `pexpect`, `platformdirs`, `prometheus_client`, `prompt_toolkit`, `psutil`, `psygnal`, `ptyprocess`, `pure_eval`, `pycparser`, `Pygments`, `python-dateutil`, `python-json-logger`, `pytz`, `PyYAML`, `pyzmq`, `referencing`, `rpds-py`, `Send2Trash`, `six`, `stack-data`, `terminado`, `tomli`, `tornado`, `traitlets`, `typing_extensions`, `tzdata`, `wcwidth`, `zipp`
