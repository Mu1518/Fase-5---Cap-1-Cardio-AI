import pandas as pd
from clima import extrair_dados_clima
from solos import extrair_dados_solo
from municipios_br import extrair_dados_municipios
from altitude import extrair_dados_altitude
import os

# Diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminhos dos arquivos
arquivo_clima = os.path.join(diretorio_atual, "clima_5000.shp")
arquivo_solo = os.path.join(diretorio_atual, "solos.csv")
arquivo_municipios = os.path.join(diretorio_atual, "BR_Municipios_2024.shp")
arquivo_altitude = os.path.join(diretorio_atual, "BR_Localidades_2010_v1.kml")

# Gerar dataset de clima
dados_clima = extrair_dados_clima(arquivo_clima)
df_clima = pd.DataFrame(dados_clima)
df_clima.to_csv(os.path.join(diretorio_atual, "dados_clima.csv"), index=False)

# Gerar dataset de solo
dados_solo = extrair_dados_solo(arquivo_solo)
df_solo = pd.DataFrame(dados_solo)
df_solo.to_csv(os.path.join(diretorio_atual, "dados_solo.csv"), index=False)

# Gerar dataset de municípios
dados_municipios = extrair_dados_municipios(arquivo_municipios)
df_municipios = pd.DataFrame(dados_municipios)
df_municipios.to_csv(os.path.join(
    diretorio_atual, "dados_municipios.csv"), index=False)

# Gerar dataset de altitude
dados_altitude = extrair_dados_altitude(arquivo_altitude)
df_altitude = pd.DataFrame(dados_altitude)
df_altitude.to_csv(os.path.join(
    diretorio_atual, "dados_altitude.csv"), index=False)

print("Datasets gerados com sucesso no mesmo diretório do script!")
