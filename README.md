# Predicción de estancia hospitalaria restante en UCI con MIMIC-IV

Pipeline reproducible para construir, explorar, depurar y preparar un conjunto de datos clínicos orientado a un problema de **regresión de estancia hospitalaria restante en UCI**, utilizando información disponible durante las **primeras 12 horas de estancia**.

El proyecto está construido a partir de **MIMIC-IV 3.1** y organiza el flujo completo de preparación de datos en cuatro notebooks ejecutables en secuencia.

---

## 1. Objetivo del proyecto

El objetivo es construir un conjunto analítico a nivel de **estancia en UCI (`stay_id`)** que permita desarrollar posteriormente modelos de regresión para estimar:

```text
los_restante_dias
```

donde:

```text
los_restante_dias = los - 0.5
```

El punto de predicción se establece a las **12 horas después del ingreso a UCI**.

Por diseño, solo se incluyen estancias que continúan activas al llegar a ese punto temporal:

```text
los >= 0.5 días
```

La información clínica empleada como predictora se restringe a la ventana:

```text
0 <= horas_desde_ingreso < 12
```

De esta forma se evita utilizar información posterior al momento en el que se pretende realizar la predicción.

---

## 2. Fuente de datos

El proyecto utiliza **MIMIC-IV 3.1**.

Se emplean principalmente tablas de los módulos:

```text
hosp/
icu/
```

Los archivos originales de MIMIC-IV **no se incluyen en este repositorio**.

Para reproducir el pipeline es necesario contar previamente con acceso a MIMIC-IV y disponer localmente de una carpeta cuya estructura incluya, al menos:

```text
mimic-iv-3.1/
├── hosp/
└── icu/
```

---

## 3. Unidad de análisis

La unidad de análisis es:

```text
stay_id
```

Cada fila del dataset analítico representa una estancia en UCI.

Los identificadores:

```text
subject_id
stay_id
```

se conservan para trazabilidad y para realizar posteriormente una separación correcta entre entrenamiento y prueba.

No se utilizan como variables predictoras.

---

## 4. Variable objetivo

La variable objetivo del problema de regresión es:

```text
los_restante_dias
```

y representa los días de estancia restantes después de las primeras 12 horas.

La duración total:

```text
los
```

no se utiliza como predictor, ya que la variable objetivo se deriva directamente de ella y su inclusión produciría fuga de información (*data leakage*).

---

## 5. Variables predictoras seleccionadas

Después del análisis exploratorio y de la etapa de selección de variables, el conjunto reducido conserva variables demográficas, signos vitales y laboratorios de carácter general.

### Variables demográficas

```text
edad_ingreso
gender
```

### Signos vitales

Se conserva una representación media durante las primeras 12 horas para reducir redundancia entre mínimos, medias y máximos:

```text
fc_mean
fr_mean
spo2_mean
temperatura_mean
pas_mean
```

### Laboratorios

```text
lab_50882_bicarbonate
lab_50902_chloride
lab_50912_creatinine
lab_50931_glucose
lab_50971_potassium
lab_50983_sodium
lab_51006_urea_nitrogen
lab_51222_hemoglobin
lab_51265_platelet_count
lab_51301_white_blood_cells
```

En total, el conjunto mínimo contempla hasta **17 variables predictoras**, además de los identificadores y la variable objetivo.

La selección prioriza:

- disponibilidad durante las primeras 12 horas;
- generalización clínica;
- reducción de redundancia;
- ausencia de fuga de información;
- parsimonia;
- menor dependencia de codificaciones administrativas propias de un hospital.

---

## 6. Estructura del repositorio

```text
estancia-hospitalaria-uci/
│
├── notebooks/
│   ├── 01_construccion_dataset_analitico.ipynb
│   ├── 02_eda_dataset_analitico.ipynb
│   ├── 03_seleccion_variables.ipynb
│   └── 04_limpieza_eda_dataset_final.ipynb
│
├── src/
│   ├── __init__.py
│   └── config.py
│
├── data/
│   ├── README.md
│   ├── interim/
│   └── processed/
│
├── results/
│
├── requirements.txt
├── .gitignore
└── README.md
```

Las carpetas `data/interim/`, `data/processed/` y `results/` se utilizan para almacenar localmente los archivos generados durante la ejecución.

Los datasets derivados no se versionan en Git.

---

## 7. Flujo de trabajo

El pipeline debe ejecutarse en el siguiente orden:

```text
MIMIC-IV 3.1
      │
      ▼
01_construccion_dataset_analitico.ipynb
      │
      ▼
mimic_uci_12h_dataset_analitico.csv.gz
      │
      ▼
02_eda_dataset_analitico.ipynb
      │
      ▼
03_seleccion_variables.ipynb
      │
      ▼
mimic_uci_12h_regresion_final.csv.gz
      │
      ▼
04_limpieza_eda_dataset_final.ipynb
      │
      ├── limpieza
      ├── split train/test por paciente
      ├── evaluación de imputadores
      ├── imputación
      └── EDA post-limpieza
```

---

## 8. Descripción de los notebooks

### 01 — Construcción del dataset analítico

```text
notebooks/01_construccion_dataset_analitico.ipynb
```

Construye el dataset maestro a partir de MIMIC-IV.

Principales tareas:

- carga y validación de fuentes;
- definición de cohorte;
- selección de estancias con al menos 12 horas de duración;
- construcción del target;
- extracción de signos vitales;
- agregación de mediciones repetidas;
- extracción de laboratorios;
- procesamiento de tablas grandes por bloques cuando es necesario;
- integración final a nivel de `stay_id`;
- controles de calidad y análisis exploratorio inicial.

En esta etapa no se realiza la selección definitiva de variables ni la imputación final.

Salida principal:

```text
data/interim/mimic_uci_12h_dataset_analitico.csv.gz
```

---

### 02 — EDA del dataset analítico

```text
notebooks/02_eda_dataset_analitico.ipynb
```

Realiza un análisis exploratorio amplio sobre el dataset maestro.

Incluye:

- dimensiones y tipos de datos;
- identificadores y duplicados;
- valores faltantes;
- variables demográficas;
- variables categóricas;
- duración de estancia;
- signos vitales;
- laboratorios;
- valores extremos;
- correlaciones;
- asociaciones entre predictores y variables de interés;
- revisión de posibles riesgos de *data leakage*.

Esta etapa es principalmente descriptiva.

No se eliminan automáticamente observaciones extremas ni se imputan valores faltantes.

---

### 03 — Selección y justificación de variables

```text
notebooks/03_seleccion_variables.ipynb
```

Construye un conjunto reducido y más parsimonioso para el problema de regresión.

Los criterios principales son:

1. evitar fuga de información;
2. separar identificadores de predictores;
3. favorecer variables clínicamente generalizables;
4. revisar disponibilidad y faltantes;
5. estudiar redundancia mediante correlación de Spearman;
6. reducir representaciones redundantes de signos vitales;
7. conservar un panel básico de laboratorios.

Los identificadores:

```text
subject_id
stay_id
```

se mantienen únicamente para trazabilidad y para realizar la partición por paciente.

Salida principal:

```text
data/interim/mimic_uci_12h_regresion_final.csv.gz
```

También se genera una tabla con la justificación de las variables seleccionadas dentro de:

```text
results/seleccion_variables/
```

---

### 04 — EDA final, limpieza, imputación y validación post-limpieza

```text
notebooks/04_limpieza_eda_dataset_final.ipynb
```

Trabaja con el dataset reducido generado por el notebook 03.

Incluye:

#### EDA final

- auditoría estructural;
- análisis del target;
- valores faltantes;
- distribuciones;
- asimetría y curtosis;
- detección de outliers mediante IQR;
- detección robusta mediante MAD;
- revisión de rangos fisiológicamente plausibles;
- asociaciones predictor-target;
- correlaciones entre predictores;
- análisis de calidad de variables.

#### Limpieza

Se documentan las transformaciones realizadas y se genera un registro de limpieza.

#### Separación train/test

La separación se realiza con:

```text
GroupShuffleSplit
```

utilizando:

```text
subject_id
```

como variable de agrupamiento.

La proporción empleada es:

```text
80 % entrenamiento
20 % prueba
```

con:

```text
random_state = 42
```

Esto evita que estancias pertenecientes al mismo paciente aparezcan simultáneamente en entrenamiento y prueba.

#### Evaluación de imputadores

Se comparan:

```text
Mediana
KNN k=3
KNN k=5
KNN k=7
KNN k=10
```

Para la evaluación se oculta artificialmente una fracción de valores originalmente observados del conjunto de entrenamiento y se comparan:

```text
MAE estandarizado
RMSE estandarizado
```

El método seleccionado se ajusta únicamente con datos de entrenamiento.

El conjunto de prueba nunca se utiliza para estimar los parámetros del imputador.

#### EDA post-limpieza

Después del procesamiento se vuelven a revisar:

- faltantes;
- estadísticos descriptivos;
- valores extremos;
- correlaciones;
- asociaciones con el target;
- comportamiento de las variables después de la limpieza.

---

## 9. Archivos generados

### Datos intermedios

```text
data/interim/
├── mimic_uci_12h_dataset_analitico.csv.gz
└── mimic_uci_12h_regresion_final.csv.gz
```

### Datos procesados

El notebook 04 genera localmente archivos como:

```text
data/processed/
├── mimic_uci_12h_limpio_pre_split.csv.gz
├── mimic_uci_12h_train_imputado.csv.gz
├── mimic_uci_12h_test_imputado.csv.gz
├── registro_limpieza.csv
├── comparacion_imputadores.csv
└── revision_post_imputacion.csv
```

### Resultados del EDA

Las tablas de análisis se almacenan en:

```text
results/
```

incluyendo resultados de:

- valores faltantes;
- descriptivos;
- outliers;
- plausibilidad;
- asociaciones con el target;
- correlaciones;
- calidad de variables;
- EDA post-limpieza.

---

## 10. Requisitos

Se recomienda utilizar:

```text
Python >= 3.10
```

Las principales dependencias del proyecto son:

```text
pandas
numpy
matplotlib
seaborn
scipy
scikit-learn
jupyter
ipykernel
```

Para instalarlas:

```bash
pip install -r requirements.txt
```

---

## 11. Configuración de MIMIC-IV

Los notebooks no contienen rutas personales fijas.

Durante la primera ejecución se solicitará la ruta local a la carpeta raíz de MIMIC-IV, es decir, aquella que contiene:

```text
hosp/
icu/
```

Ejemplo en Windows:

```text
C:\Users\usuario\Downloads\mimic-iv-3.1\mimic-iv-3.1
```

La ruta se almacena localmente en:

```text
.mimic_path
```

Este archivo está incluido en `.gitignore`, por lo que **no se comparte en GitHub**.

Para cambiar la ubicación de MIMIC-IV posteriormente, se puede eliminar `.mimic_path` y volver a ejecutar el notebook.

---

## 12. Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/sel-gp/estancia-hospitalaria-uci.git
cd estancia-hospitalaria-uci
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Abrir Jupyter o VS Code

Abrir los notebooks dentro de:

```text
notebooks/
```

### 4. Ejecutar en orden

```text
01_construccion_dataset_analitico.ipynb
02_eda_dataset_analitico.ipynb
03_seleccion_variables.ipynb
04_limpieza_eda_dataset_final.ipynb
```

Cada notebook utiliza los archivos generados por la etapa anterior.

---

## 13. Reproducibilidad

El proyecto está estructurado para evitar dependencias de rutas personales.

La reproducibilidad se basa en:

- configuración centralizada en `src/config.py`;
- identificación local de la ubicación de MIMIC-IV;
- rutas relativas dentro del repositorio;
- salidas encadenadas entre notebooks;
- separación train/test con semilla fija;
- ajuste de imputadores únicamente sobre entrenamiento;
- registro explícito de transformaciones y resultados.

Una persona con acceso a MIMIC-IV puede clonar este repositorio, instalar las dependencias, indicar la ubicación local de MIMIC-IV y ejecutar los cuatro notebooks en orden.

---

## 14. Gestión de datos y Git

Los archivos de MIMIC-IV y los datasets derivados a nivel de registro **no se versionan en este repositorio**.

El archivo `.gitignore` excluye:

```text
.mimic_path
data/interim/*
data/processed/*
results/*
```

Se conservan únicamente archivos vacíos `.gitkeep` para mantener la estructura de directorios.

Esto permite compartir el pipeline sin publicar los datos utilizados durante el análisis.

---

## 15. Estado del proyecto

Esta versión del repositorio cubre:

- construcción de la cohorte;
- integración de fuentes MIMIC-IV;
- construcción del target;
- análisis exploratorio;
- selección de variables;
- construcción del dataset final de regresión;
- limpieza;
- separación train/test;
- comparación de estrategias de imputación;
- imputación;
- análisis post-limpieza.

La etapa posterior corresponde al entrenamiento y evaluación de modelos de regresión sobre los conjuntos preparados por este pipeline.
