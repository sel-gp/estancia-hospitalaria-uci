# Predicción de estancia hospitalaria restante en UCI — MIMIC-IV

Repositorio reproducible para construir y analizar un dataset de estancias en UCI a partir de MIMIC-IV.

## Requisitos

- Python 3.10 o superior
- Acceso autorizado a MIMIC-IV
- Estructura estándar de MIMIC-IV con las carpetas `hosp/` e `icu/`

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración de MIMIC-IV

No es necesario editar rutas dentro de los notebooks.

En la primera ejecución del proyecto se pedirá:

> Escribe la ruta a la carpeta raíz de MIMIC-IV (la que contiene `hosp` e `icu`)

Ejemplo en Windows:

```text
C:\Users\usuario\Downloads\mimic-iv-3.1\mimic-iv-3.1
```

La ruta se guarda localmente en `.mimic_path`. Ese archivo está ignorado por Git y no se comparte en el repositorio.

Si se necesita cambiar la ubicación de MIMIC-IV, basta con borrar `.mimic_path` y volver a ejecutar el notebook.

## Orden de ejecución

1. `notebooks/01_construccion_dataset_analitico.ipynb`
   - Construye la cohorte de estancias UCI.
   - Usa información de las primeras 12 horas.
   - Genera `data/interim/mimic_uci_12h_dataset_analitico.csv.gz`.

2. `notebooks/02_eda_dataset_analitico.ipynb`
   - Realiza el análisis exploratorio del dataset analítico.

3. `notebooks/03_seleccion_variables.ipynb`
   - Justifica la selección de variables.
   - Genera `data/interim/mimic_uci_12h_regresion_final.csv.gz`.
   - Guarda la justificación en `results/seleccion_variables/`.

4. `notebooks/04_limpieza_eda_dataset_final.ipynb`
   - Realiza EDA final, limpieza, separación train/test, comparación de imputadores,
     imputación y EDA post-limpieza.
   - Guarda datasets procesados en `data/processed/`.
   - Guarda resultados del EDA en `results/`.

## Estructura

```text
estancia-hospitalaria-uci/
├── notebooks/
│   ├── 01_construccion_dataset_analitico.ipynb
│   ├── 02_eda_dataset_analitico.ipynb
│   ├── 03_seleccion_variables.ipynb
│   └── 04_limpieza_eda_dataset_final.ipynb
├── src/
│   ├── __init__.py
│   └── config.py
├── data/
│   ├── interim/
│   └── processed/
├── results/
├── requirements.txt
├── .gitignore
└── README.md
```

## Datos

Los archivos originales de MIMIC-IV y los datasets derivados a nivel de registro no se incluyen en este repositorio. Cada usuario debe contar con acceso autorizado a MIMIC-IV y ejecutar el pipeline localmente.
