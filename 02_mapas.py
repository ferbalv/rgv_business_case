# Para la construcción de los mapas, utilicé los poligonos municipales, obtenidos del
# Marco Geoestadístico del INEGI, descargados de su página.
# Utilicé Copilot para la generar los mapas y mejorar la lectura del código. 
# Nota: El formato de los mapas fue la tarea que más tiempo me tomó en el caso. 
import json
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import pandas as pd


root = Path(__file__).resolve().parent
data_dir = root / "data"
maps_dir = root / "maps"
geojson_dir = data_dir / "geojson"
maps_dir.mkdir(exist_ok=True)
geojson_dir.mkdir(exist_ok=True)

breweries = pd.read_csv(
    data_dir / "01_denue0526_ 312120_elab_cerveza.csv",
    encoding="utf-8-sig",
    dtype={"cve_mun": str},
)

with (data_dir / "03_brewing_comp_metrics.json").open(encoding="utf-8") as metrics_file:
    metrics = pd.DataFrame.from_dict(json.load(metrics_file), orient="index")
metrics.index.name = "nom_estab"
metrics = metrics.reset_index()
if set(metrics["nom_estab"]) != set(breweries["nom_estab"]):
    raise ValueError("JSON company names must match nom_estab values in the brewing CSV")
for column in ["ig_followers", "views_viral_video"]:
    metrics[column] = pd.to_numeric(metrics[column], errors="raise")

brewing_comp = breweries.merge(metrics, on="nom_estab", how="left", validate="one_to_one")
if brewing_comp[["ig_followers", "views_viral_video"]].isna().all(axis=None):
    print("Add company metrics in data/03_brewing_comp_metrics.json to customize map labels and sizes.")

brewing_comp["norm_name"] = brewing_comp["nom_estab"].str.strip().str.title()
brewing_comp = brewing_comp[
    [
        "nom_estab",
        "per_ocu",
        "latitud",
        "longitud",
        "ig_followers",
        "views_viral_video",
        "norm_name",
    ]
]

municipality_polygons = gpd.read_file(data_dir / "maps_polygons" / "22mun.shp")
municipality_polygons["CVE_MUN"] = (
    municipality_polygons["CVE_MUN"].astype(str).str.zfill(3)
)
municipality_polygons = municipality_polygons.to_crs(epsg=4326)

brewing_points = gpd.GeoDataFrame(
    brewing_comp,
    geometry=gpd.points_from_xy(brewing_comp["longitud"], brewing_comp["latitud"]),
    crs="EPSG:4326",
)
brewing_points = brewing_points.merge(
    breweries[["nom_estab", "cve_mun"]],
    on="nom_estab",
    how="left",
    validate="one_to_one",
)

municipality_maps = {
    "014": (
        "queretaro",
        "Queretaro",
        "01_queretaro_cervecerias.png",
    ),
    "016": (
        "san_juan_del_rio",
        "San Juan del Río",
        "02_san_juan_del_rio_cervecerias.png",
    ),
}

for code, (name, display_name, filename) in municipality_maps.items():
    polygon = municipality_polygons[municipality_polygons["CVE_MUN"] == code]
    if polygon.empty:
        raise ValueError(f"Municipality code {code} was not found in the shapefile")

    companies = brewing_points[brewing_points["cve_mun"] == code]
    polygon.to_file(geojson_dir / f"{name}_poligono.geojson", driver="GeoJSON")
    companies.to_file(geojson_dir / f"{name}_cervecerias.geojson", driver="GeoJSON")

    ordered_companies = companies.sort_values("longitud").reset_index(drop=True)
    map_polygon = polygon.to_crs(epsg=32614)
    map_companies = ordered_companies.to_crs(epsg=32614)
    min_x, min_y, max_x, max_y = map_polygon.total_bounds
    x_margin = (max_x - min_x) * 0.12
    y_margin = (max_y - min_y) * 0.12

    fig = plt.figure(figsize=(10, 12), facecolor="#F5F7FA")
    layout = fig.add_gridspec(
        4,
        1,
        height_ratios=(0.9, 7.3, 1.4, 1.0),
        left=0.08,
        right=0.92,
        top=0.96,
        bottom=0.04,
        hspace=0.02,
    )
    header_ax, map_ax, companies_ax, footer_ax = (
        fig.add_subplot(layout[row]) for row in range(4)
    )

    header_ax.set_axis_off()
    header_ax.text(
        0.5,
        0.88,
        "RGV Soluciones |  Cervecería Maxi",
        transform=header_ax.transAxes,
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#52708A",
    )
    header_ax.text(
        0.5,
        0.42,
        f"Empresas productoras de cerveza en la ciudad de {display_name}",
        transform=header_ax.transAxes,
        ha="center",
        va="center",
        fontsize=15,
        fontweight="bold",
        color="#1D2D3E",
    )
    header_ax.text(
        0.5,
        0.08,
        "Ubicación de establecimientos registrados en el municipio",
        transform=header_ax.transAxes,
        ha="center",
        va="center",
        fontsize=9,
        color="#647588",
    )

    map_ax.set_facecolor("#F5F7FA")
    map_polygon.plot(
        ax=map_ax,
        facecolor="#E5EDF3",
        edgecolor="#405B70",
        linewidth=1.4,
    )
    follower_counts = pd.to_numeric(
        map_companies["ig_followers"], errors="coerce"
    ).fillna(0).clip(lower=0)
    marker_sizes = follower_counts * 0.01
    map_ax.scatter(
        map_companies.geometry.x,
        map_companies.geometry.y,
        s=marker_sizes,
        color="#147D92",
        edgecolors="white",
        linewidths=1.5,
        zorder=3,
    )
    label_offsets = {
        "queretaro": [(-18, 58), (22, -58)],
        "san_juan_del_rio": [(24, 22)],
    }
    for index, (_, point) in enumerate(map_companies.iterrows()):
        views = pd.to_numeric(point["views_viral_video"], errors="coerce")
        views_label = f"{views:,.0f}" if pd.notna(views) else "N/D"
        map_ax.annotate(
            f"{point['norm_name']}\nVistas: {views_label}",
            (point.geometry.x, point.geometry.y),
            xytext=label_offsets[name][index],
            textcoords="offset points",
            ha="right" if label_offsets[name][index][0] < 0 else "left",
            va="center",
            fontsize=8,
            fontweight="medium",
            color="#1D2D3E",
            arrowprops={
                "arrowstyle": "-",
                "color": "#647588",
                "linewidth": 0.9,
                "shrinkA": 3,
                "shrinkB": 4,
            },
            path_effects=[
                path_effects.withStroke(linewidth=3, foreground="#F5F7FA")
            ],
            zorder=4,
        )

    map_ax.set_xlim(min_x - x_margin, max_x + x_margin)
    map_ax.set_ylim(min_y - y_margin, max_y + y_margin)
    map_ax.set_aspect("equal", adjustable="box")
    map_ax.set_axis_off()

    companies_ax.set_axis_off()
    companies_ax.text(
        0.49,
        0.52,
        "Tamaño del círculo proporcional al número de seguidores en Instagram",
        transform=companies_ax.transAxes,
        ha="left",
        va="center",
        fontsize=8,
        color="#526273",
    )
    for x_position, followers in zip((0.08, 0.20, 0.34), (10_000, 50_000, 100_000)):
        companies_ax.scatter(
            x_position,
            0.52,
            s=followers * 0.01,
            color="#147D92",
            edgecolors="white",
            linewidths=1,
            transform=companies_ax.transAxes,
            clip_on=False,
            zorder=2,
        )
        companies_ax.text(
            x_position,
            0.1,
            f"{followers // 1000} mil",
            transform=companies_ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=6.5,
            color="#647588",
        )

    footer_ax.set_axis_off()
    footer_ax.plot(
        [0, 1],
        [0.96, 0.96],
        transform=footer_ax.transAxes,
        color="#D9E1E8",
        linewidth=0.8,
        clip_on=False,
    )
    footer_ax.text(
        0.02,
        0.66,
        'Nota: Datos con base en DENUE (INEGI) para empresas en la rama '
        '"312120 Elaboración de cerveza" y cuentas de Instagram de cada una de las empresas.',
        transform=footer_ax.transAxes,
        ha="left",
        va="center",
        fontsize=7,
        color="#526273",
    )
    footer_ax.text(
        0.02,
        0.31,
        "Nota 2: Para ver más detalle del mapa de cada municipio, consultar el archivo "
        "05_brewings_qro.html.",
        transform=footer_ax.transAxes,
        ha="left",
        va="center",
        fontsize=7,
        color="#526273",
    )
    fig.savefig(
        maps_dir / filename,
        dpi=250,
        facecolor=fig.get_facecolor(),
    )
    plt.close(fig)
