# entregable2
entregable 2 proyecto SSDD

# 🚦 Proyecto Sistemas Distribuidos - Entrega 2: Procesamiento Distribuido con Pig

**Autores**: Lucas Vicuña, Vicente Silva  
**Curso**: Sistemas Distribuidos - Universidad Diego Portales  
**Profesor**: Nicolás Hidalgo  
**Fecha**: 1 de junio de 2025  
**Project ID**: `69384236`  

---

## 📌 Descripción General

Esta segunda entrega expande el sistema distribuido de análisis de eventos de tráfico mediante el uso de **Apache Pig** como herramienta de procesamiento paralelo. Se incorporan nuevos análisis agrupando eventos por **tipo y calle** y por **hora de ocurrencia**, con visualizaciones generadas automáticamente.

---

## ⚙️ Tecnologías utilizadas

- **Python 3.10+**
- **MySQL 8.0 (contenedor Docker)**
- **Apache Pig 0.17 (contenedor Docker)**
- **Redis 7 (contenedor Docker)**
- **Selenium (modo headless) + ChromeDriver**
- **Pandas, NumPy, Matplotlib**
- **Docker + Docker Compose**

---

## 🐳 Instalación y ejecución

### 1. Clona el repositorio

```bash
git clone https://gitlab.com/proyectos_u/sistemas_distribuidos.git
cd sistemas_distribuidos
```

### 2. Requisitos

- Docker + Docker Compose
- Python 3.10+
- `chromedriver.exe` (ya incluido)
- Google Chrome instalado

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Levanta los servicios

```bash
docker-compose up -d
```

Se levantarán:

- `mysql_eventos`: contenedor de base de datos MySQL
- `redis_cache`: contenedor Redis
- `pig_container`: contenedor con Apache Pig

### 5. Ejecuta el programa principal

```bash
python main.py
```

Desde el menú podrás:

- Ejecutar scraping desde Waze
- Consultar la base de datos
- Simular tráfico y evaluar caché
- Ejecutar procesamiento distribuido con Pig
- Ver resultados y gráficos

---

## 🐷 Procesamiento con Apache Pig

Se ejecutan automáticamente dos scripts Pig:

- `test.pig`: agrupa eventos por **tipo y calle**.
- `test_hora.pig`: agrupa eventos por **hora** de ocurrencia.

Los resultados se guardan en:

- `data/output_tipo_calle.xlsx`
- `data/output_por_hora.xlsx`

Los gráficos resultantes son:

- `distribucion_tipos_evento.png`
- `evolucion_eventos_por_hora.png`

---

## 📂 Estructura del Repositorio

```
├── main.py                     # Menú principal del sistema
├── scraper.py                  # Web scraping de Waze
├── db.py                       # Conexión y consultas a MySQL
├── trafico.py                  # Simulación de tráfico y caché
├── funciones.py                # Gráficos y visualización
├── pig_processor.py            # Ejecución de scripts Pig
├── data/
│   ├── eventos.csv / eventos.xlsx
│   ├── output_tipo_calle.xlsx
│   ├── output_por_hora.xlsx
├── informe/
│   └── main.tex                # Informe en LaTeX
├── docker-compose.yml
├── Dockerfile.pig
├── README.md
```

---

## 📈 Resultados de la Entrega 2

Se generaron:

| Agrupación     | Archivo Excel                  | Imagen generada                   |
|----------------|--------------------------------|-----------------------------------|
| Tipo y Calle   | `output_tipo_calle.xlsx`       | `distribucion_tipos_evento.png`   |
| Hora del día   | `output_por_hora.xlsx`         | `evolucion_eventos_por_hora.png`  |

> Ambos análisis permiten visualizar tendencias de tráfico en distintos contextos.

---

## 🔗 Enlaces

- [Repositorio GitLab](https://gitlab.com/proyectos_u/sistemas_distribuidos)
- [Entrega 1 README](./README.md)
- [Informe LaTeX](./informe/main.tex)

---

## 📌 Notas

- El contenedor `pig_container` debe estar corriendo antes de ejecutar el procesamiento.
- Si los archivos de salida no se generan, verifica los logs en `data/*.log`.
- Para ejecutar los scripts Pig manualmente:
  
```bash
docker exec -it pig_container bash
pig -x local /data/test.pig
pig -x local /data/test_hora.pig
```

---
