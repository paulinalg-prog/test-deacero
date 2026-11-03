from pathlib import Path
import argparse
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
LOAD_SCRIPT = ROOT / "scripts" / "load_landing.py"


def main():
    parser = argparse.ArgumentParser(
        description="Orquestador del pipeline de ingeniería de datos."
    )
    parser.add_argument(
        "--trigger",
        choices=["manual", "scheduled", "event"],
        default="manual",
        help="Mecanismo que inició la ejecución.",
    )
    args = parser.parse_args()

    execution_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    print("=" * 60)
    print("DEACERO | PIPELINE DE LOGÍSTICA")
    print("=" * 60)
    print(f"ID de ejecución: {execution_id}")
    print(f"Disparador: {args.trigger}")
    print("\n[1/4] Iniciando carga de datos landing...")

    if not LOAD_SCRIPT.exists():
        raise FileNotFoundError(
            f"No se encontró el script de carga: {LOAD_SCRIPT}"
        )

    subprocess.run(
        [sys.executable, str(LOAD_SCRIPT)],
        cwd=ROOT,
        check=True,
    )

    print("\n[2/4] Perfilado de datos: pendiente de implementar.")
    print("[3/4] Ejecución de dbt: pendiente de implementar.")
    print("[4/4] Validaciones y agente: pendientes de implementar.")

    print("\nPipeline finalizado correctamente hasta la etapa implementada.")


if __name__ == "__main__":
    main()