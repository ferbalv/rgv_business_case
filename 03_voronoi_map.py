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
    data_dir / "02_denue0526_461212_comercio_cerveza.csv",
    encoding="utf-8-sig",
    dtype={"cve_mun": str},
    usecols=["nom_estab", "latitud", "longitud", "cve_mun"],
)

municipalities = {
    "014": (
        "queretaro",
        "Querétaro",
        "03_queretaro_voronoi.png",
    ),
    "016": (
        "san_juan_del_rio",
        "San Juan del Río",
        "04_san_juan_del_rio_voronoi.png",
    ),
}
voronoi_cities = []

for code, (city, display_name, map_filename) in municipalities.items():
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
    map_boundary = boundary.to_crs(epsg=32614)
    map_voronoi = voronoi.to_crs(epsg=32614)
    map_sites = sites.to_crs(epsg=32614)
    min_x, min_y, max_x, max_y = map_boundary.total_bounds
    x_margin = (max_x - min_x) * 0.12
    y_margin = (max_y - min_y) * 0.12

    fig = plt.figure(figsize=(10, 12), facecolor="#F5F7FA")
    layout = fig.add_gridspec(
        4,
        1,
        height_ratios=(0.9, 7.3, 0.55, 1.15),
        left=0.08,
        right=0.92,
        top=0.96,
        bottom=0.04,
        hspace=0.02,
    )
    header_ax, map_ax, legend_ax, footer_ax = (
        fig.add_subplot(layout[row]) for row in range(4)
    )

    header_ax.set_axis_off()
    header_ax.text(
        0.5,
        0.88,
        "RGV Soluciones  |  Cervecería Maxi",
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
        "Áreas de influencia de comercios de cerveza en "
        f"la ciudad de {display_name}",
        transform=header_ax.transAxes,
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#1D2D3E",
    )
    header_ax.text(
        0.5,
        0.08,
        "Polígonos de Voronoi y ubicación de establecimientos comerciales",
        transform=header_ax.transAxes,
        ha="center",
        va="center",
        fontsize=9,
        color="#647588",
    )

    map_ax.set_facecolor("#F5F7FA")
    map_voronoi.plot(
        ax=map_ax,
        color="#DCE8EF",
        edgecolor="black",
        linewidth=0.45,
    )
    map_boundary.boundary.plot(
        ax=map_ax,
        color="#405B70",
        linewidth=1.4,
    )
    map_ax.scatter(
        map_sites.geometry.x,
        map_sites.geometry.y,
        s=22,
        color="#147D92",
        edgecolors="white",
        linewidths=0.7,
        zorder=3,
    )
    map_ax.set_xlim(min_x - x_margin, max_x + x_margin)
    map_ax.set_ylim(min_y - y_margin, max_y + y_margin)
    map_ax.set_aspect("equal", adjustable="box")
    map_ax.set_axis_off()

    legend_ax.set_axis_off()
    legend_ax.scatter(
        0.28,
        0.5,
        s=24,
        color="#147D92",
        edgecolors="white",
        linewidths=0.7,
        transform=legend_ax.transAxes,
        clip_on=False,
    )
    legend_ax.text(
        0.31,
        0.5,
        "Establecimientos comerciales (símbolos de tamaño uniforme)",
        transform=legend_ax.transAxes,
        ha="left",
        va="center",
        fontsize=8,
        color="#526273",
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
        '"461212 Comercio al por menor de cerveza".',
        transform=footer_ax.transAxes,
        ha="left",
        va="center",
        fontsize=7,
        color="#526273",
    )
    footer_ax.text(
        0.02,
        0.31,
        "Nota 2: Para más detalles sobre los mapas y el nivel socioeconómico, "
        "consultar 06_voronoi_qro.html.",
        transform=footer_ax.transAxes,
        ha="left",
        va="center",
        fontsize=7,
        color="#526273",
    )
    fig.savefig(
        maps_dir / map_filename,
        dpi=250,
        facecolor=fig.get_facecolor(),
    )
    plt.close(fig)

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
