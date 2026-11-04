from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import MultiPoint
from shapely.ops import unary_union, voronoi_diagram


root = Path(__file__).resolve().parent
data_dir = root / "data"
geojson_dir = data_dir / "geojson"
maps_dir = root / "maps"
maps_dir.mkdir(exist_ok=True)

commerce = pd.read_csv(
    data_dir / "denue052026_461212_comercio_cerveza.csv",
    encoding="utf-8-sig",
    dtype={"cve_mun": str},
    usecols=["nom_estab", "latitud", "longitud", "cve_mun"],
)

municipalities = {
    "014": "queretaro",
    "016": "san_juan_del_rio",
}
voronoi_cities = []

for code, city in municipalities.items():
    boundary_path = geojson_dir / f"{city}_poligono.geojson"
    boundary = gpd.read_file(boundary_path)
    if boundary.empty:
        raise ValueError(f"No municipality polygon found in {boundary_path}")

    city_data = commerce.loc[
        commerce["cve_mun"] == code,
        ["nom_estab", "latitud", "longitud"],
    ].dropna(subset=["latitud", "longitud"])
    if city_data.empty:
        raise ValueError(f"No commerce locations found for municipality {code}")

    sites = (
        city_data.groupby(["longitud", "latitud"], as_index=False)
        .agg(
            nom_estab=("nom_estab", lambda names: " | ".join(names)),
            establishment_count=("nom_estab", "size"),
        )
    )
    sites = gpd.GeoDataFrame(
        sites,
        geometry=gpd.points_from_xy(sites["longitud"], sites["latitud"]),
        crs="EPSG:4326",
    ).to_crs(epsg=32614)
    boundary = boundary.to_crs(epsg=32614)
    city_polygon = unary_union(boundary.geometry)

    width = city_polygon.bounds[2] - city_polygon.bounds[0]
    height = city_polygon.bounds[3] - city_polygon.bounds[1]
    envelope = city_polygon.envelope.buffer(max(width, height) * 2)
    diagram = voronoi_diagram(
        MultiPoint(list(sites.geometry)),
        envelope=envelope,
        edges=False,
    )

    features = []
    for cell in diagram.geoms:
        site_index = sites.geometry.distance(cell.representative_point()).idxmin()
        site = sites.loc[site_index]
        clipped = cell.intersection(city_polygon)
        if clipped.is_empty or clipped.area == 0:
            continue
        if clipped.geom_type == "GeometryCollection":
            clipped = unary_union(
                [
                    part
                    for part in clipped.geoms
                    if part.geom_type in {"Polygon", "MultiPolygon"}
                ]
            )
        if not clipped.is_empty:
            features.append(
                {
                    "nom_estab": site["nom_estab"],
                    "establishment_count": int(site["establishment_count"]),
                    "geometry": clipped,
                }
            )

    voronoi = gpd.GeoDataFrame(features, geometry="geometry", crs="EPSG:32614")
    if voronoi.empty:
        raise ValueError(f"No Voronoi polygons created for {city}")
    voronoi = voronoi.to_crs(epsg=4326)
    voronoi["municipality"] = city
    voronoi_cities.append(voronoi)

    boundary = boundary.to_crs(epsg=4326)
    sites = sites.to_crs(epsg=4326)
    ax = voronoi.plot(
        column="establishment_count",
        cmap="tab20",
        edgecolor="white",
        linewidth=0.25,
        figsize=(10, 10),
        legend=False,
    )
    boundary.boundary.plot(ax=ax, color="black", linewidth=1)
    sites.plot(ax=ax, color="black", markersize=5)
    ax.set_title(f"Voronoi de comercios de cerveza: {city.replace('_', ' ').title()}")
    ax.set_axis_off()
    ax.figure.savefig(
        maps_dir / f"{city}_voronoi.png",
        dpi=200,
        bbox_inches="tight",
    )
    plt.close(ax.figure)

    print(
        f"{city}: created {len(voronoi)} clipped Voronoi polygons "
        f"from {len(city_data)} establishments"
    )

combined_voronoi = gpd.GeoDataFrame(
    pd.concat(voronoi_cities, ignore_index=True),
    geometry="geometry",
    crs="EPSG:4326",
)
voronoi_path = maps_dir / "queretaro_san_juan_del_rio_voronoi.geojson"
combined_voronoi.to_file(voronoi_path, driver="GeoJSON")
print(f"Saved {len(combined_voronoi)} Voronoi polygons for both cities to {voronoi_path}")
