import json
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


root = Path(__file__).resolve().parent
data_dir = root / "data"
maps_dir = root / "maps"
geojson_dir = data_dir / "geojson"
maps_dir.mkdir(exist_ok=True)
geojson_dir.mkdir(exist_ok=True)

breweries = pd.read_csv(
    data_dir / "denue052026_ 312120_elab_cerveza.csv",
    encoding="utf-8-sig",
    dtype={"cve_mun": str},
)

with (data_dir / "brewing_comp_metrics.json").open(encoding="utf-8") as metrics_file:
    metrics = pd.DataFrame.from_dict(json.load(metrics_file), orient="index")
metrics.index.name = "nom_estab"
metrics = metrics.reset_index()
if set(metrics["nom_estab"]) != set(breweries["nom_estab"]):
    raise ValueError("JSON company names must match nom_estab values in the brewing CSV")
for column in ["ig_followers", "views_viral_video"]:
    metrics[column] = pd.to_numeric(metrics[column], errors="raise")

brewing_comp = breweries.merge(metrics, on="nom_estab", how="left", validate="one_to_one")
if brewing_comp[["ig_followers", "views_viral_video"]].isna().all(axis=None):
    print("Add company metrics in data/brewing_comp_metrics.json to customize map labels and sizes.")

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

municipalities = gpd.read_file(data_dir / "maps_polygons" / "22mun.shp")
municipalities["CVE_MUN"] = municipalities["CVE_MUN"].astype(str).str.zfill(3)
municipalities = municipalities.to_crs(epsg=4326)

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

for code, name in {"014": "queretaro", "016": "san_juan_del_rio"}.items():
    polygon = municipalities[municipalities["CVE_MUN"] == code]
    if polygon.empty:
        raise ValueError(f"Municipality code {code} was not found in the shapefile")

    companies = brewing_points[brewing_points["cve_mun"] == code]
    polygon.to_file(geojson_dir / f"{name}_poligono.geojson", driver="GeoJSON")
    companies.to_file(geojson_dir / f"{name}_cervecerias.geojson", driver="GeoJSON")

    ax = polygon.plot(facecolor="#eeeeee", edgecolor="black", figsize=(9, 9))
    follower_counts = pd.to_numeric(companies["ig_followers"], errors="coerce")
    marker_sizes = 30 + follower_counts.fillna(0).clip(lower=0).pow(0.5) * 4
    companies.plot(ax=ax, color="#1f77b4", markersize=marker_sizes)

    for _, company in companies.iterrows():
        views = pd.to_numeric(company["views_viral_video"], errors="coerce")
        views_label = f"{views:,.0f}" if pd.notna(views) else "N/D"
        ax.annotate(
            f"{company['norm_name']}\nViews: {views_label}",
            (company.geometry.x, company.geometry.y),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
        )

    ax.set_title(f"Cervecerías en {name.replace('_', ' ').title()}")
    ax.set_axis_off()
    ax.figure.savefig(maps_dir / f"{name}_cervecerias.png", dpi=200, bbox_inches="tight")
    plt.close(ax.figure)
