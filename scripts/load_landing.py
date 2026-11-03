
from pathlib import Path
import duckdb

# Identificar la carpeta raíz del repositorio
ROOT = Path(__file__).resolve().parents[1]

# Ubicación de los archivos originales
DATA_DIR = ROOT / "data" / "replica" / "carga_1"

# Base de datos local compartida con dbt
DB_PATH = ROOT / "deacero.duckdb"

# Relación entre archivos, esquemas y tablas
TABLES = {
    "fle_viaje.csv": ("landing_fle", "fle_viaje"),
    "fle_viaje_det.csv": ("landing_fle", "fle_viaje_det"),
    "fle_entrega.csv": ("landing_fle", "fle_entrega"),
    "vta_cliente.csv": ("landing_vta", "vta_cliente"),
    "opc_planta.csv": ("landing_opc", "opc_planta"),
}


def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta: {DATA_DIR}")

    con = duckdb.connect(str(DB_PATH))

    try:
        for filename, (schema, table) in TABLES.items():
            file_path = DATA_DIR / filename

            if not file_path.exists():
                raise FileNotFoundError(f"No se encontró: {file_path}")

            con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

            # Se conservan todas las columnas como texto.
            path_sql = str(file_path).replace("\\", "/").replace("'", "''")

            con.execute(f"""
                CREATE OR REPLACE TABLE {schema}.{table} AS
                SELECT *
                FROM read_csv_auto(
                    '{path_sql}',
                    header = true,
                    all_varchar = true,
                    sample_size = -1
                )
            """)

            count = con.execute(
                f"SELECT COUNT(*) FROM {schema}.{table}"
            ).fetchone()[0]

            print(f"OK | {schema}.{table} | {count:,} filas")

        print(f"\nCarga terminada. Base de datos: {DB_PATH}")

    finally:
        con.close()


if __name__ == "__main__":
    main()
