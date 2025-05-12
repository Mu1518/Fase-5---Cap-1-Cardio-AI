import geopandas as gpd
from shapely.geometry import Point

# Carregar o shapefile com a malha territorial dos municípios
gdf = gpd.read_file(r"C:\Users\techg\Desktop\TESTESP3\BR_Municipios_2024.shx")
print("Colunas disponíveis no shapefile:", gdf.columns)
print("Tipos de geometria no shapefile:", gdf['geometry'].geom_type.unique())


print(gdf.head())
# Verificar as colunas disponíveis no shapefile
print("Colunas disponíveis no shapefile:", gdf.columns)

# Verificar o CRS atual
print("CRS atual:", gdf.crs)

# Transformar para WGS84 (EPSG:4326), se necessário
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs(epsg=4326)


def identificar_municipio(lat, lon):
    """
    Identifica o município com base em coordenadas geográficas.
    :param lat: Latitude
    :param lon: Longitude
    :return: Nome do município ou mensagem de erro
    """
    # Criar um ponto a partir das coordenadas
    ponto = Point(lon, lat)

    # Verificar em qual polígono o ponto está
    for _, row in gdf.iterrows():  # Iterando sobre os polígonos
        if row['geometry'].contains(ponto):

            return row['NM_MUN']
    return "Coordenadas fora de qualquer município."


def extrair_dados_municipios(caminho_municipios):
    """
    Extrai dados de municípios de um shapefile.
    :param caminho_municipios: Caminho para o arquivo shapefile de municípios.
    :return: Lista de dicionários com latitude, longitude e nome do município.
    """
    gdf = gpd.read_file(caminho_municipios)

    # Verificar as colunas disponíveis
    print("Colunas disponíveis no shapefile:", gdf.columns)

    # Definir o CRS original, se necessário
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4674)  # Exemplo: EPSG:4674 (SIRGAS 2000)

    # Converter para WGS84
    gdf = gdf.to_crs(epsg=4326)

    # Verificar os tipos de geometria
    print("Tipos de geometria no shapefile:",
          gdf['geometry'].geom_type.unique())

    dados = []
    for _, row in gdf.iterrows():
        if row['geometry'].geom_type in ['Polygon', 'MultiPolygon']:
            # Calcular o centróide do polígono para obter latitude e longitude
            centroid = row['geometry'].centroid
            dados.append({
                'lat': centroid.y,
                'lon': centroid.x,
                # Substitua 'NM_MUN' pelo nome correto da coluna
                'municipio': row['NM_MUN']
            })
    return dados

# Exemplo de uso
latitude = -23.55052
longitude = -46.633308
municipio = identificar_municipio(latitude, longitude)
print(f"O município na coordenada ({latitude}, {longitude}) é: {municipio}")
