import geopandas as gpd
import pandas as pd


# Cargar shapefile de nivel 2 (municipios)

shapefile_path = "gadm41_COL_2.shp"
gdf = gpd.read_file(shapefile_path, engine="fiona")

# -----------------------------
# Asegurar que las columnas de texto sean strings
# -----------------------------
texto_cols = ['NAME_1', 'NAME_2', 'TYPE_2', 'ENGTYPE_2']
for col in texto_cols:
    if col in gdf.columns:
        gdf[col] = gdf[col].astype(str)

# Calcular centroides


gdf['centroid'] = gdf['geometry'].centroid
gdf['centroide_lon'] = gdf['centroid'].x
gdf['centroide_lat'] = gdf['centroid'].y


# Calcular número de polígonos
def contar_poligonos(geom):
    if geom.geom_type == 'Polygon':
        return 1
    elif geom.geom_type == 'MultiPolygon':
        return len(geom.geoms)
    else:
        return 0

gdf['num_poligonos'] = gdf['geometry'].apply(contar_poligonos)


# Crear código abreviado tipo ISO para el municipio
# -----------------------------
iso_departamentos = {
    'COL.1_2': 'CO-AMA',
    'COL.2_2': 'CO-ANT',
    'COL.3_2': 'CO-ARA',
    'COL.4_2': 'CO-ATL',
    'COL.5_2': 'CO-BOG',
    'COL.6_2': 'CO-BOL',
    'COL.7_2': 'CO-BOY',
    'COL.8_2': 'CO-CAL',
    'COL.9_2': 'CO-CAQ',
    'COL.10_2': 'CO-CAS',
    'COL.11_2': 'CO-CAU',
    'COL.12_2': 'CO-CES',
    'COL.13_2': 'CO-CHO',
    'COL.14_2': 'CO-COR',
    'COL.15_2': 'CO-CUN',
    'COL.16_2': 'CO-GUA',
    'COL.17_2': 'CO-GUV',
    'COL.18_2': 'CO-HUI',
    'COL.19_2': 'CO-LAG',
    'COL.20_2': 'CO-MAG',
    'COL.21_2': 'CO-MET',
    'COL.22_2': 'CO-NAR',
    'COL.23_2': 'CO-NSA',
    'COL.24_2': 'CO-PUT',
    'COL.25_2': 'CO-QUI',
    'COL.26_2': 'CO-RIS',
    'COL.27_1': 'CO-SAN',
    'COL.28_2': 'CO-SAN',
    'COL.29_2': 'CO-SUC',
    'COL.30_2': 'CO-TOL',
    'COL.31_2': 'CO-VAC',
    'COL.32_2': 'CO-VAP',
    'COL.33_2': 'CO-VID'
}

gdf['ISO_1'] = gdf['GID_1'].map(iso_departamentos)
gdf['municipio_codigo'] = gdf['ISO_1'] + '-' + gdf['GID_2'].str.split('_').str[1]

# -----------------------------
# Seleccionar y renombrar columnas
# -----------------------------
df_export = gdf[['GID_0','GID_1','GID_2','municipio_codigo','NAME_1','NAME_2','geometry','num_poligonos','centroide_lon','centroide_lat']].copy()
df_export.columns = [
    'pais',
    'departamento_id',
    'municipio_id',
    'municipio_codigo',
    'departamento_nombre',
    'municipio_nombre',
    'geometry',
    'num_poligonos',
    'centroide_lon',
    'centroide_lat'
]

# -----------------------------
# Guardar TSV
# -----------------------------
df_export.to_csv("municipios_colombia_level2.tsv", sep='\t', index=False, encoding='utf-8')
print("TSV nivel 2 generado con éxito. Filas:", len(df_export))
