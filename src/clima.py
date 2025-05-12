import geopandas as gpd
from shapely.geometry import Point

# Carregar o shapefile
gdf = gpd.read_file(r"C:/Users/techg/Desktop/TESTESP3/clima_5000.shp")

# Verificar as colunas disponíveis no shapefile
print("Colunas disponíveis no shapefile:", gdf.columns)

# Definir o CRS para o sistema de coordenadas WGS84
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=4674)  # Exemplo: EPSG:4674 (SIRGAS 2000)
gdf = gdf.to_crs(epsg=4326)

# Verificar os tipos de geometria no shapefile
print("Tipos de geometria no shapefile:", gdf['geometry'].geom_type.unique())


def identificar_tipo_clima(lat, lon):
    """
    Identifica o tipo de clima com base em coordenadas geográficas.
    :param lat: Latitude
    :param lon: Longitude
    :return: Informações de clima ou mensagem de erro
    """
    # Criar um ponto a partir das coordenadas
    ponto = Point(lon, lat)

    # Verificar em qual polígono o ponto está
    for _, row in gdf.iterrows():  # Iterando sobre os polígonos
        if row['geometry'].contains(ponto):
            # Retornar múltiplas informações
            return {
                'ZONA': row['ZONA'],
                'TEMPERATUR': row['TEMPERATUR'],
                'TP_UMIDADE': row['TP_UMIDADE']
            }

    return "Coordenadas fora de qualquer polígono de clima."


def extrair_dados_clima(caminho_clima):
    """
    Extrai dados de clima de um shapefile.
    :param caminho_clima: Caminho para o arquivo shapefile de clima.
    :return: Lista de dicionários com informações de clima e geometria.
    """
    gdf = gpd.read_file(caminho_clima)

    # Definir o CRS original, se necessário
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4674)  # Exemplo: EPSG:4674 (SIRGAS 2000)

    # Converter para WGS84
    gdf = gdf.to_crs(epsg=4326)

    dados = []
    for _, row in gdf.iterrows():
        if row['geometry'].geom_type in ['Polygon', 'MultiPolygon']:  # Verificar se é polígono
            dados.append({
                'geometry': row['geometry'],
                'ZONA': row['ZONA'],
                'TEMPERATUR': row['TEMPERATUR'],
                'TP_UMIDADE': row['TP_UMIDADE']
            })
    return dados


# Exemplo de uso
latitude = -23.55052
longitude = -46.633308
tipo_clima = identificar_tipo_clima(latitude, longitude)
print(
    f"O tipo de clima na coordenada ({latitude}, {longitude}) é: {tipo_clima}")
