import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Carregando o dataset
df = pd.read_csv(r"C:/Users/techg/Desktop/TESTESP3/solos.csv")

# conversão da coluna 'geometry' de WKT para geometria real
df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])

# Criar um gdf a partir do df
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# verificando se o sistema de coordenadas está em WGS84
gdf = gdf.set_crs(epsg=4326)

# função para identificar o tipo de solo pela coordenada geografica (latitude e longitude) 
def identificar_tipo_solo(lat, lon):
    """
    Identifica o tipo de solo com base em coordenadas geográficas.
    :param lat: Latitude
    :param lon: Longitude
    :return: Tipo de solo ou mensagem de erro
    """
    # Criar um ponto a partir das coordenadas
    ponto = Point(lon, lat)

    # Verificar em qual polígono o ponto está
    for _, row in gdf.iterrows(): # iterando sobre os polígonos
        if row['geometry'].contains(ponto):
            # Substitua 'classe_dom' pelo nome da coluna que contém o tipo de solo
            return row['classe_dom']

    return "Coordenadas fora de qualquer polígono de solo."


def extrair_dados_solo(caminho_solo):
    """
    Extrai dados de solo de um arquivo CSV com geometria em formato WKT.
    :param caminho_solo: Caminho para o arquivo CSV de solo.
    :return: Lista de dicionários com informações de solo.
    """
    # Carregar o arquivo CSV
    df = pd.read_csv(caminho_solo)

    # Verificar se a coluna 'geometry' está presente
    if 'geometry' not in df.columns:
        raise ValueError("O arquivo CSV deve conter a coluna 'geometry'.")

    # Converter a coluna 'geometry' de WKT para geometria real
    df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])

    # Criar um GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

    # Converter os dados para uma lista de dicionários
    dados = gdf[['geometry', 'classe_dom']].to_dict(orient='records')
    return dados

# Exemplo de uso
latitude = -23.55052
longitude = -46.633308
tipo_solo = identificar_tipo_solo(latitude, longitude)
print(f"O tipo de solo na coordenada ({latitude}, {longitude}) é: {tipo_solo}")
