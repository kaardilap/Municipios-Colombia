import geopandas as gpd
import pandas as pd

# Cargar shapefile de nivel 2 (municipios)
# Para esto, se define una variable con la ruta relativa del archivo 
#y se crea un Geo Data Frame usando la función read_file() de geopandas


shapefile_path = "datos_entrada/gadm41_COL_2.shp"
gdf = gpd.read_file(shapefile_path, engine="fiona")

# -----------------------------
# Asegurar que las columnas de texto sean strings
#Definimos un array con las columnas que tienen un texto descriptivo
#y posteriormente con un ciclo se buscan en el geo data frame y se
#modifica el tipo de dato de esa columna a str (esto para evitar
#futuros problemas al manipular estos datos)

# -----------------------------
# list con los nombre de las columnas

texto_cols = ['NAME_1', 'NAME_2', 'TYPE_2', 'ENGTYPE_2']
# Este ciclo for recorre la list texto_cols
for col in texto_cols:
# Se evalúa con el condicional if si el elemento de la lista está entre las columnas de geo data frame
    if col in gdf.columns:
# En caso de estar, se hace una conversion a str a esa columna se accede a la columna en el geo data frame por su nombre
        gdf[col] = gdf[col].astype(str)

# Calcular centroides
# Se define en el geo data frame tres columnas nuevas (centroid, centroide_lon, centroide_lat)

# Se calcula el centroide con la función centroid sobre la columna geometry


gdf['centroid'] = gdf['geometry'].centroid
# Se define la columna centroide_lon como la coordenada en x del centroide
gdf['centroide_lon'] = gdf['centroid'].x
# Se define la columna centroide_lat como la coordenada en y del centroide
gdf['centroide_lat'] = gdf['centroid'].y


# Calcular número de polígonos: Esta función se usa para definir el tipo de geometría con base en el número de polígonos.

def contar_poligonos(geom):
# se emplea una estructura condicional (if, elif, else)

# si el tipo de la geometría es poligono el valor de retorno de la función es 1
    if geom.geom_type == 'Polygon':
        return 1
# si el tipo de la geometría es Multipoligono el valor de retorno de la función es la cantidad de polígonos
    elif geom.geom_type == 'MultiPolygon':
        return len(geom.geoms) # se usa len para contar la cantidad de polígonos
    else:
        return 0 # en cualquier otro caso distinto a los anteriores el valor de retorno es 0    
# creamos una columna con el numero de polígonos aplicando la función anterior a la columna geometría
gdf['num_poligonos'] = gdf['geometry'].apply(contar_poligonos)
# se redefine la columna geometría unicamente con el dato del tipo de geometría
gdf['geometry'] = gdf['geometry'].geom_type

# Crear código abreviado tipo ISO para el municipio
#Para esta abreviación creamos un diccionario usando como clave el codigo GID_1 de cada departamento según el shapefile de GADM
#y valor el código ISO estandarizado de Colombia para cada departamento
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
# Creamos una columna llamada ISO_1, le aplicamos la función map a la columna GID_1

# la función map toma cada valor de GID_1 y lo busca en el diccionario, si encuentra

# la clave, retorna el valor correspondiente
gdf['ISO_1'] = gdf['GID_1'].map(iso_departamentos)
# Creamos una nueva columna municipio_codigo concatenando ISO_1 con el segundo 

# elemento del split('_') aplicado a GID_2

# (la función split divide el string de GID_2 en substrings con base en el caracter '_')

gdf['municipio_codigo'] = gdf['ISO_1'] + '-' + gdf['GID_2'].str.split('_').str[1]

# -----------------------------
# Seleccionar y renombrar columnas: Seleccionamos las columnas que nos interesan y creamos un data frame unicamente con esas que nos interesan
# -----------------------------
df_export = gdf[['GID_0','GID_1','GID_2','municipio_codigo','NAME_1','NAME_2','geometry','num_poligonos','centroide_lon','centroide_lat']].copy()
# Accedemos a las columnas del data frame que acabamos de crear y renombramos las columnas
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
# exportamos el data frame con la función to_csv y definimos como separador tabuladores ('\t') acorde al formato tsv
# -----------------------------
df_export.to_csv("municipios_colombia_level2.tsv", sep='\t', index=False, encoding='utf-8')
# usamos la impresión por pantalla para confirmar la creación del archivo .tsv
print("TSV nivel 2 generado con éxito. Filas:", len(df_export))

