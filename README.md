# RGV Business Case
Link del repositorio: [RGV Business Case](https://github.com/ferbalv/rgv_business_case)
Link de mapas: [Voronoi](https://ferbalv.github.io/rgv_business_case/maps/06_voronoi_qro.html) y [Cervecerías](https://ferbalv.github.io/rgv_business_case/maps/05_brewings_qro.html)
Link Google Sheets: [Google Sheets](https://docs.google.com/spreadsheets/d/1ASmtTRtTbqUnTtVMc79xMOlt7d4u_U_QOHlMll9uF_E/edit?usp=sharing)

Este repositorio contiene los archivos del ejercicio 2 descritos en `20261008 RGV Assessment.pdf`. A continuación, se resume el contenido:

## Contenido del repositorio

- `data/`: contiene los datos del DENUE para el estado de Querétaro (`00_denue_inegi_22.csv`) y los datasets `01_denue0526_ 312120_elab_cerveza.csv` y `02_denue0526_461212_comercio_cerveza.csv`. También incluye los archivos auxiliares `03_brewing_comp_metrics.json` y `04_nse_qro.geojson`.
- `data/geojson/`: contiene los archivos GeoJSON utilizados para construir los mapas.
- `data/maps_polygons/`: contiene los archivos utilizados para construir los polígonos de los municipios de Querétaro y San Juan del Río.
- `maps/`: contiene los mapas solicitados en formato PNG y los mapas interactivos en HTML, construidos con Kepler.gl. También incluye un archivo GeoJSON con los polígonos de Voronoi.
- `README.md`: describe los archivos e incluye instrucciones para crear el entorno virtual (`venv`).
- `01_dataspitter.py`: procesa los datos del DENUE y los divide en dos datasets para facilitar la construcción de los mapas.
- `02_mapas.py`: genera los mapas.
- `03_voronoi_map_py`: calcula los polígonos de Voronoi.
- `04_map_kepler.ipynb`: notebook de Jupyter que construye los mapas en Kepler.gl.

A continuación, se muestran las instrucciones para correr el entorno virtual (en ingles, construido por un agente).

## Setup

Follow these steps in a terminal after cloning the repository. The commands below assume the repository folder is named `rgv_business_case`; if yours has a different name, use that folder name instead.

### 1. Clone the repository and enter its folder

```bash
git clone https://github.com/ferbalv/rgv_business_case.git
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
