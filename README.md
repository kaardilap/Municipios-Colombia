# Municipios de Colombia - Nivel 2
Este repositorio contiene datos geoespaciales de los municipios de Colombia a nivel 2, junto con un script para procesarlos y generar un archivo TSV con información relevante.

## Contenido

- `municipios_col.py` - Script principal que procesa el shapefile y genera el TSV.
- `datos_entrada/gadm41_COL_2.shp` - Shapefile original de municipios 
- `municipios_colombia_level2.tsv` - Archivo resultante con la información de municipios.
- `README.md` - Este archivo de documentación.

## Requisitos

- Python 3.8+
- Paquetes de Python:
  - geopandas
  - pandas
  - fiona

Instalación de paquetes:

```bash
pip install geopandas pandas fiona
```

Uso:
1. Clonar repositorio:
```
git clone https://github.com/tu_usuario/municipios_col.git
cd municipios_col
```
2. Ejecutar el script para generar el TSV:
```
python municipios_col.py
```
3. El archivo municipios_colombia_level2.tsv se generará en la mimsma carpeta.

## Contenido de los archivos generados

municipios_colombia_level2.tsv contiene:

pais - Código del país

departamento_id - ID del departamento

municipio_id - ID del municipio

municipio_codigo - Código abreviado tipo ISO

departamento_nombre - Nombre del departamento

municipio_nombre - Nombre del municipio

geometry - Geometría del municipio

num_poligonos - Número de polígonos del municipio

centroide_lon - Longitud del centroide

centroide_lat - Latitud del centroide

## Visualización

Se recomienda ejecutar Excel y desde allí abrir el archivo para una visaulización más clara y amigable de la información.

