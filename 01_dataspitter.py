# Este código construye dos archivos a partir de "00_denue_inegi_22.csv".

import csv
from pathlib import Path


data_dir = Path(__file__).resolve().parent / "data"
# Los datos se descargaron del DENUE para todo el estado de Querétaro.
source_path = data_dir / "00_denue_inegi_22.csv"

# Del archivo fuente se construyen dos archivos filtrados por código de actividad.
output_paths = {
	"312120": data_dir / "01_denue0526_ 312120_elab_cerveza.csv",
	"461212": data_dir / "02_denue0526_461212_comercio_cerveza.csv",
}

municipality_codes = {"014", "016"} # Códigos de los municipios de Queretaro y San Juan del Río, respectivamente. 
filtered_rows = {activity_code: [] for activity_code in output_paths}

# Para la optimizacion de este seccion del codigo, utilicé un agente de AI (Copilot)
with source_path.open(encoding="cp1252", newline="") as source_file:
	reader = csv.DictReader(source_file)
	if reader.fieldnames is None:
		raise ValueError(f"The source CSV has no header: {source_path}")

	required_columns = {"codigo_act", "cve_mun"} #Estas son las columas con las cuales filtro por actividad economica y municipio.
	missing_columns = required_columns.difference(reader.fieldnames)
	if missing_columns:
		raise ValueError(f"Missing required CSV columns: {', '.join(sorted(missing_columns))}")

	fieldnames = reader.fieldnames
	for row in reader:
		cleaned_row = {
			fieldname: (row.get(fieldname) or "").strip()
			for fieldname in fieldnames
		}
		activity_code = cleaned_row["codigo_act"]
		if cleaned_row["cve_mun"] in municipality_codes and activity_code in filtered_rows:
			filtered_rows[activity_code].append(cleaned_row)

# En este loop obtengo los CSVs que utilizaré para construir los mapas. 
for activity_code, output_path in output_paths.items():
	with output_path.open("w", encoding="utf-8-sig", newline="") as output_file:
		writer = csv.DictWriter(output_file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(filtered_rows[activity_code])