from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PATH_FILE = PROJECT_ROOT / ".mimic_path"

def _validar_mimic(path: Path) -> Path:
    path = path.expanduser().resolve()
    hosp = path / "hosp"
    icu = path / "icu"
    if not hosp.is_dir() or not icu.is_dir():
        raise FileNotFoundError(
            "La ruta indicada no parece ser la raíz de MIMIC-IV: "
            "debe contener las carpetas 'hosp' e 'icu'.\n"
            f"Ruta recibida: {path}"
        )
    return path

def _obtener_mimic_dir() -> Path:
    # 1) Si existe variable de entorno, úsala.
    env_path = os.getenv("MIMIC_IV_PATH")
    if env_path:
        return _validar_mimic(Path(env_path))

    # 2) Si ya se guardó una ruta local, úsala.
    if PATH_FILE.exists():
        saved = PATH_FILE.read_text(encoding="utf-8").strip()
        if saved:
            try:
                return _validar_mimic(Path(saved))
            except FileNotFoundError:
                pass

    # 3) Primera ejecución: pedir la ruta una sola vez.
    raw = input(
        "Escribe la ruta a la carpeta raíz de MIMIC-IV "
        "(la que contiene 'hosp' e 'icu'): "
    ).strip().strip('"').strip("'")

    if not raw:
        raise RuntimeError("No se proporcionó una ruta a MIMIC-IV.")

    path = _validar_mimic(Path(raw))
    PATH_FILE.write_text(str(path), encoding="utf-8")
    return path

MIMIC_DIR = _obtener_mimic_dir()
HOSP_DIR = MIMIC_DIR / "hosp"
ICU_DIR = MIMIC_DIR / "icu"

DATA_DIR = PROJECT_ROOT / "data"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

INTERIM_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
