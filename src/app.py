# ===== IMPORTANDO BIBLIOTECAS E MÓDULOS PYTHON NECESSÁRIOS =====

import locale
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import requests
from datetime import datetime
from PIL import Image
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO


# ===== CONFIGURANDO O TÍTULO DA PÁGINA ======

st.markdown(
    """ <style> .centered-text {text-align: center}</style> """, unsafe_allow_html=True)
st.markdown('<h1 class="centered-text"><b> 🛰️ CHALLENGE INGREDION</b></h1>',
            unsafe_allow_html=True)
st.markdown('<h3 class="centered-text"><b>SPRINT 3</b></h3>',
            unsafe_allow_html=True)

# ===== CONSTANTES =====

# URL base da API Oracle
url_base = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap"

# Cabeçalho para requisições JSON
CONTENT_TYPE_JSON = {"Content-Type": "application/json"}

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Configuração de localidade


# ====== DECORADOR PARA EVITAR QUE A API SEJA CHAMADA A CADA REQUISIÇÃO ======

@st.cache_data
def carregar_dados():
    return carregar_dados_oracle("produtividade")

# ===== FUNÇÕES AUXILIARES PARA CARREGAR DADOS DA API ORACLE =====
def carregar_dados_oracle(tipo):  # Carregar dados da API Oracle
    endpoint, cols = None, None  # Inicialização de endpoint e colunas
    if tipo == "ndvi":
        endpoint = f"{url_base}/carga_ndvi/"
        cols = ["localidade", "cultura", "data", "ndvi"]
    elif tipo == "produtividade":
        endpoint = f"{url_base}/carga_produtividade/"
        cols = [
            "localidade",
            "cultura",
            "ano",
            "area_plantada",
            "area_colhida",
            "rendimento_medio",
        ]
    elif tipo == "meteorologicos":
        endpoint = f"{url_base}/carga_dados_meteorologicos/"
        cols = [
            "localidade",
            "data",
            "precipitacao",
            "pressao_atmosferica",
            "radiacao_solar_global",
            "temperatura_bulbo_seco",
            "temperatura_orvalho",
            "umidade_relativa",
            "velocidade_vento",
        ]
    elif tipo == "custos":
        endpoint = f"{url_base}/carga_custos/"
        cols = ["localidade", "cultura", "ano", "indicador", "custo"]
    else:
        st.error(f"Tipo de dados inválido: {tipo}")
        return pd.DataFrame()

    all_items = []  # Lista para armazenar todos os itens
    has_more = True  # Variável para controle de paginação
    while has_more:  # Loop para carregar dados paginados
        try:
            response = requests.get(
                endpoint, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            response_json = response.json()

            if "items" in response_json:
                all_items.extend(response_json["items"])
            else:
                st.warning(
                    f"A resposta da API para {tipo} não continha 'items'. Verifique a API.")
                return pd.DataFrame()
            has_more = response_json.get("hasMore", False)
            if has_more:
                next_link = next(
                    (link["href"] for link in response_json.get(
                        "links", []) if link["rel"] == "next"),
                    None,
                )
                if next_link:
                    endpoint = next_link
                else:
                    st.warning(
                        f"A API para {tipo} indicou 'hasMore', mas não forneceu um link 'next'.")
                    has_more = False
            else:
                has_more = False
        except requests.exceptions.RequestException as e:  # Tratamento de exceções para requisições
            st.error(f"Erro ao carregar dados de {tipo}: {e}")
            return pd.DataFrame(columns=cols)
        except ValueError as e:  # Tratamento de exceções para decodificação JSON
            st.error(
                f"Erro ao decodificar JSON para {tipo}: {e}. Verifique a resposta da API.")
            return pd.DataFrame(columns=cols)
        except KeyError as e:  # Tratamento de exceções para chaves ausentes no JSON
            st.error(
                f"Erro de chave no JSON para {tipo}: {e}. Verifique a estrutura da resposta da API.")
            return pd.DataFrame(columns=cols)

    if not all_items and cols:  # Verifica se não há itens e se as colunas estão definidas
        st.warning(f"Nenhum dado encontrado para o tipo: {tipo}.")
        return pd.DataFrame(columns=cols)
    elif not all_items:
        st.warning(
            f"Nenhum dado encontrado para o tipo: {tipo} e colunas não definidas.")
        return pd.DataFrame()
    else:
        return pd.DataFrame(all_items, columns=cols)


@st.cache_data  # Cache para evitar chamadas repetidas à API
def carregar_dados_produtividade():  # Carregar dados de produtividade via API
    return carregar_dados_oracle("produtividade")


@st.cache_data
def carregar_dados_meteorologicos():  # Carregar dados meteorológicos via API
    return carregar_dados_oracle("meteorologicos")


@st.cache_data
def carregar_dados_custos():  # Carregar dados de custos via API
    return carregar_dados_oracle("custos")


@st.cache_data
def carregar_dados_ndvi():  # Carregar dados de NDVI via API
    df_ndvi_completo = carregar_dados_oracle("ndvi")
    if df_ndvi_completo.empty:
        return pd.DataFrame()
    if 'data' in df_ndvi_completo.columns:
        df_ndvi_completo['data'] = pd.to_datetime(
            df_ndvi_completo['data'], errors='coerce')
    return df_ndvi_completo


# ===== FUNÇÃO DE ANÁLISE EXPLORATÓRIA =====


def executar_analise():

    # Carregar todos os datasets
    df_ndvi_completo = carregar_dados_ndvi()
    df_produtividade_completo = carregar_dados_produtividade()
    df_meteorologicos_completo = carregar_dados_oracle("meteorologicos")
    df_custos_completo = carregar_dados_oracle("custos")

    # Verificar se os dados estão disponíveis
    if df_ndvi_completo.empty or df_produtividade_completo.empty or df_meteorologicos_completo.empty or df_custos_completo.empty:
        return None  # Indica que não há dados suficientes

    # Análise de limpeza dos dados
    def analise_limpeza(df, nome):
        return {
            "Nome": nome,
            "Número de linhas": len(df),
            "Número de colunas": len(df.columns),
            "Número de valores ausentes": df.isnull().sum().sum(),
            "Número de duplicados": df.duplicated().sum()
        }

    # Resultdos da anãlise da limpeza dos datasets
    resultados_limpeza = [
        analise_limpeza(df_ndvi_completo, "NDVI"),
        analise_limpeza(df_produtividade_completo, "Produtividade"),
        analise_limpeza(df_meteorologicos_completo, "Meteorológicos"),
        analise_limpeza(df_custos_completo, "Custos")
    ]

    # Converter os resultados em um DataFrame para exibição
    df_resultados_limpeza = pd.DataFrame(resultados_limpeza)

    # Tratamento e limpeza dos dados (apenas para exibição na análise)
    df_ndvi = df_ndvi_completo.dropna(subset=['ndvi']).copy()
    df_produtividade = df_produtividade_completo.dropna(
        subset=['rendimento_medio']).copy()
    df_meteorologicos = df_meteorologicos_completo.dropna().copy()
    df_custos = df_custos_completo.dropna().copy()

    # Converter a coluna 'data' para 'datetime' em todos os DataFrames, se existir
    dataframes = {
        "NDVI": df_ndvi,
        "Produtividade": df_produtividade,
        "Meteorologicos": df_meteorologicos,
        "Custos": df_custos
    }
    for nome, df in dataframes.items():
        if 'data' in df.columns:
            try:
                df['data'] = pd.to_datetime(df['data'], errors='coerce')
            except (ValueError, TypeError) as e:
                st.error(
                    f"Erro ao converter a coluna 'data' em {nome}: {e}. Verifique o formato da data.")
                return None  # Retorna None em caso de erro

        resultados = {
            "df_resultados_limpeza": df_resultados_limpeza,
            "df_ndvi_completo": df_ndvi_completo,
            "df_produtividade_completo": df_produtividade_completo,
            "df_meteorologicos_completo": df_meteorologicos_completo,
            "df_custos_completo": df_custos_completo,
            "df_ndvi": df_ndvi,
            "df_produtividade": df_produtividade,
            "df_meteorologicos": df_meteorologicos,
            "df_custos": df_custos,
        }

    # Análise do Label
    if not df_ndvi.empty:
        resultados["describe_ndvi"] = df_ndvi['ndvi'].describe().to_frame()
        resultados["fig_hist_ndvi"] = px.histogram(
            df_ndvi, x='ndvi', marginal='box', title='Distribuição do NDVI')

    # Análise das Features
    resultados["colunas_features"] = []
    if not df_produtividade.empty:
        resultados["colunas_features"].append(
            ('rendimento_medio', df_produtividade, 'Produtividade'))
        resultados["describe_produtividade"] = df_produtividade['rendimento_medio'].describe(
        ).to_frame()
        resultados["fig_hist_produtividade"] = px.histogram(
            df_produtividade, x='rendimento_medio', marginal='box', title='Distribuição de Produtividade')

    if not df_meteorologicos.empty:
        print(
            f"Número de linhas em df_meteorologicos após limpeza: {len(df_meteorologicos)}")
        print("Colunas em df_meteorologicos:", df_meteorologicos.columns)
        print("Head do df_meteorologicos antes da análise:",
              df_meteorologicos.head())

        colunas_meteorologicas = [
            'precipitacao', 'pressao_atmosferica', 'temperatura_bulbo_seco']
        for col in colunas_meteorologicas:
            if col in df_meteorologicos.columns:
                resultados["colunas_features"].append(
                    (col, df_meteorologicos, col.capitalize().replace('_', ' ')))
                print(f"Coluna '{col}' adicionada a colunas_features.")
            else:
                print(
                    f"A coluna '{col}' não foi encontrada no DataFrame de meteorológicos.")

        # Dicionário para armazenar as descrições
        resultados["describe_meteorologicos"] = {}
        for col in colunas_meteorologicas:
            if col in df_meteorologicos.columns:
                describe = df_meteorologicos[col].describe().to_frame()
                resultados["describe_" +
                           col.replace('_', ' ').lower()] = describe
                print(
                    f"Descrição de '{col}' calculada e armazenada como 'resultados[describe_{col.replace('_', ' ').lower()}]'.")
            else:
                resultados["describe_meteorologicos"][col] = pd.DataFrame()

        resultados["fig_hist_meteorologicos"] = {}
        for col in colunas_meteorologicas:
            if col in df_meteorologicos.columns:
                fig = px.histogram(
                    df_meteorologicos, x=col, marginal='box', title=f'Distribuição de {col.capitalize().replace('_', ' ')}')
                resultados["fig_hist_" + col.replace('_', ' ').lower()] = fig
                print(
                    f"Histograma de '{col}' calculado e armazenado como 'resultados[fig_hist_{col.replace('_', ' ').lower()}]'.")
            else:
                resultados["fig_hist_meteorologicos"][col] = None
    if not df_custos.empty:
        resultados["colunas_features"].append(('custo', df_custos, 'Custos'))
        resultados["describe_custos"] = df_custos['custo'].describe().to_frame()
        resultados["fig_hist_custos"] = px.histogram(
            df_custos, x='custo', marginal='box', title='Distribuição de Custos')
        resultados["describe_custos"] = df_custos['custo'].describe().to_frame()

    # Análise de Correlação com o NDVI
    if 'ndvi' in df_ndvi and not df_ndvi.empty:
        df_merged = df_ndvi.copy()  # Copia o DataFrame de NDVI
        for col, df, _ in resultados["colunas_features"]:
            if col in df and 'data' in df and 'data' in df_merged:
                df_merged = pd.merge(
                    df_merged, df[['data', col]], on='data', how='inner', suffixes=('', f'_{col}'))

        # Filtrar apenas colunas numéricas para calcular a correlação
        numeric_cols_ndvi = df_merged.select_dtypes(include=np.number).columns
        if 'ndvi' in numeric_cols_ndvi:
            resultados["corr_matrix"] = df_merged[numeric_cols_ndvi].corr()['ndvi'].sort_values(
                ascending=False).to_frame()
            resultados["fig_corr_ndvi_heatmap"] = px.imshow(
                df_merged[numeric_cols_ndvi].corr(), title='Matriz de Correlação com NDVI')
        else:
            resultados["corr_matrix"] = None
            resultados["fig_corr_ndvi_heatmap"] = None
    else:
        resultados["corr_matrix"] = None
        resultados["fig_corr_ndvi_heatmap"] = None

    # Análise de Dispersão entre Features e NDVI
    if 'ndvi' in df_ndvi and not df_ndvi.empty:
        resultados["scatter_plots"] = []
        for col, df, title in resultados["colunas_features"]:
            if col in df and 'data' in df and 'data' in df_ndvi:
                df_scatter = pd.merge(
                    df_ndvi, df[['data', col]], on='data', how='inner')
                if not df_scatter.empty:
                    resultados["scatter_plots"].append({
                        "col": col,
                        "title": title,
                        "fig": px.scatter(df_scatter, x=col, y='ndvi',
                                          title=f'Dispersão entre {title} e NDVI')
                    })
    else:
        resultados["scatter_plots"] = []

    # Análise de Tendências Temporais
    if 'data' in df_ndvi and not df_ndvi.empty:
        resultados["fig_tendencia_ndvi"] = px.line(
            df_ndvi, x='data', y='ndvi', title='Tendência Temporal do NDVI')
        resultados["tendencias_temporais"] = []
        for col, df, title in resultados["colunas_features"]:
            if col in df and 'data' in df:
                resultados["tendencias_temporais"].append({
                    "col": col,
                    "title": title,
                    "fig": px.line(df, x='data', y=col,
                                   title=f'Tendência Temporal de {title}')
                })
    else:
        resultados["fig_tendencia_ndvi"] = None
        resultados["tendencias_temporais"] = []

    # Matriz de Correlação entre Features (incluindo NDVI)
    df_features = pd.DataFrame()
    for col, df, _ in resultados["colunas_features"]:
        if col in df and 'data' in df:
            if df_features.empty:
                df_features = df[['data', col]].copy()
            else:
                df_features = pd.merge(
                    df_features, df[['data', col]], on='data', how='inner', suffixes=('', f'_{col}'))

    # Adicionar a coluna 'ndvi' ao df_features, se existir
    if 'ndvi' in df_ndvi.columns and 'data' in df_ndvi.columns:
        if df_features.empty:
            df_features = df_ndvi[['data', 'ndvi']].copy()
        else:
            df_features = pd.merge(
                df_features, df_ndvi[['data', 'ndvi']], on='data', how='inner')

    if not df_features.empty and df_features.shape[1] > 1:
        # Filtrar apenas colunas numéricas para calcular a correlação
        numeric_cols_features = df_features.select_dtypes(
            include=np.number).columns
        # Recalcular a matriz de correlação incluindo 'ndvi'
        resultados["corr_matrix_features"] = df_features[numeric_cols_features].corr()
        resultados["fig_corr_features_heatmap"] = px.imshow(
            resultados["corr_matrix_features"], title='Matriz de Correlação entre Features (incluindo NDVI)')
    else:
        resultados["corr_matrix_features"] = None
        resultados["fig_corr_features_heatmap"] = None

    return resultados


def analise_exploratoria():

    st.header("🔍 Análise Exploratória")
    st.write("---")

    # lista para obter os resultados pré-calculados, se existirem
    resultados = executar_analise()

    if resultados is None:  # Verifica se os dados estão disponíveis e, se não, exibe uma mensagem de erro
        st.warning("Dados insuficientes para análise.")
        return

    opcoes_exibicao = [
        "Resultados da Limpeza",
        "Dados Completos (Amostra)",
        "Análise da Variável NDVI",
        "Análise das Variáveis Features",
        "Análise de Correlação com o NDVI",
        "Análise de Dispersão entre Features e NDVI",
        "Análise de Tendências Temporais",
        "Matriz de Correlação entre Features (incluindo NDVI)",
        "Download dos Dados"
    ]

    st.write("Selecione o que deseja visualizar:")
    num_colunas = 3  # Número de colunas para exibir os botões
    colunas = st.columns(num_colunas)
    indice_coluna = 0
    selecoes = []

    for opcao in opcoes_exibicao:
        if colunas[indice_coluna].button(opcao, use_container_width=True):
            selecoes.append(opcao)
        indice_coluna = (indice_coluna + 1) % num_colunas

    # Exibir as seções selecionadas
    if "Resultados da Limpeza" in selecoes:
        st.subheader("Resultados da Limpeza de Dados")
        if "df_resultados_limpeza" in resultados:
            st.dataframe(resultados["df_resultados_limpeza"])
        else:
            st.warning("Resultados da limpeza não disponíveis.")

    if "Dados Completos (Amostra)" in selecoes:
        st.subheader("Dados Completos (Amostra)")
        if "df_ndvi_completo" in resultados:
            st.write("Dados de NDVI:")
            st.dataframe(resultados["df_ndvi_completo"].head())
        else:
            st.warning("Dados de NDVI não disponíveis.")
        if "df_produtividade_completo" in resultados:
            st.write("Dados de Produtividade:")
            st.dataframe(resultados["df_produtividade_completo"].head())
        else:
            st.warning("Dados de Produtividade não disponíveis.")
        if "df_meteorologicos_completo" in resultados:
            st.write("Dados Meteorológicos:")
            st.dataframe(resultados["df_meteorologicos_completo"].head())
        else:
            st.warning("Dados Meteorológicos não disponíveis.")
        if "df_custos_completo" in resultados:
            st.write("Dados de Custos:")
            st.dataframe(resultados["df_custos_completo"].head())
        else:
            st.warning("Dados de Custos não disponíveis.")

    if "Análise da Variável NDVI" in selecoes:
        if "describe_ndvi" in resultados and "fig_hist_ndvi" in resultados and resultados["fig_hist_ndvi"] is not None:
            st.subheader("Análise da Variável NDVI")
            st.write(resultados["describe_ndvi"])
            st.plotly_chart(resultados["fig_hist_ndvi"])
        else:
            st.warning("Análise da variável NDVI não disponível.")

    if "Análise das Variáveis Features" in selecoes:
        if "colunas_features" in resultados:
            st.subheader("Análise das Variáveis Features")
            for col, df, title in resultados["colunas_features"]:
                st.write(f"### {title}")
                if f"describe_{title.lower()}" in resultados and resultados[f"describe_{title.lower()}"] is not None and not resultados[f"describe_{title.lower()}"] .empty:
                    st.write(resultados[f"describe_{title.lower()}"])
                else:
                    st.warning(f"Descrição de {title} não disponível.")
                if f"fig_hist_{title.lower()}" in resultados and resultados[f"fig_hist_{title.lower()}"] is not None:
                    if isinstance(resultados[f"fig_hist_{title.lower()}"], dict):
                        for fig in resultados[f"fig_hist_{title.lower()}"]:
                            if resultados[f"fig_hist_{title.lower()}"][fig] is not None:
                                st.plotly_chart(
                                    resultados[f"fig_hist_{title.lower()}"][fig])
                            else:
                                st.warning(
                                    f"Histograma de {title} não disponível.")
                    else:
                        st.plotly_chart(
                            resultados[f"fig_hist_{title.lower()}"])
                else:
                    st.warning(f"Histograma de {title} não disponível.")
        else:
            st.warning("Análise das variáveis features não disponível.")

    if "Análise de Correlação com o NDVI" in selecoes:
        if "corr_matrix" in resultados and "fig_corr_ndvi_heatmap" in resultados and resultados["corr_matrix"] is not None and resultados["fig_corr_ndvi_heatmap"] is not None:
            st.subheader("Análise de Correlação com o NDVI")
            st.write("Correlação com NDVI:")
            st.write(resultados["corr_matrix"])
            st.plotly_chart(resultados["fig_corr_ndvi_heatmap"])
        else:
            st.warning("Análise de correlação com NDVI não disponível.")

    if "Análise de Dispersão entre Features e NDVI" in selecoes:
        if "scatter_plots" in resultados:
            st.subheader("Análise de Dispersão entre Features e NDVI")
            for scatter_plot in resultados["scatter_plots"]:
                if scatter_plot["fig"] is not None:
                    st.plotly_chart(scatter_plot["fig"])
                else:
                    st.warning(
                        f"Gráfico de dispersão para {scatter_plot['title']} não disponível.")
        else:
            st.warning("Análise de dispersão não disponível.")

    if "Análise de Tendências Temporais" in selecoes:
        if "fig_tendencia_ndvi" in resultados and resultados["fig_tendencia_ndvi"] is not None:
            st.subheader("Análise de Tendências Temporais")
            st.plotly_chart(resultados["fig_tendencia_ndvi"])
        else:
            st.warning("Tendência temporal do NDVI não disponível.")
        if "tendencias_temporais" in resultados:
            for tendencia in resultados["tendencias_temporais"]:
                if tendencia["fig"] is not None:
                    st.plotly_chart(tendencia["fig"])
                else:
                    st.warning(
                        f"Tendência temporal de {tendencia['title']} não disponível.")
        else:
            st.warning("Análise de tendências temporais não disponível.")

    if "Matriz de Correlação entre Features (incluindo NDVI)" in selecoes:
        if "corr_matrix_features" in resultados and "fig_corr_features_heatmap" in resultados and resultados["corr_matrix_features"] is not None and resultados["fig_corr_features_heatmap"] is not None:
            st.subheader(
                "Matriz de Correlação entre Features (incluindo NDVI)")
            st.plotly_chart(resultados["fig_corr_features_heatmap"])
        else:
            st.warning("Matriz de correlação entre features não disponível.")

    if "Download dos Dados" in selecoes:
        # Salvar os datasets como CSV e permitir download
        st.subheader(
            "Clique abaixo para fazer o download do Dataset escolhido: ")
        # Criadas 4 colunas, uma para cada opção de download
        col1, col2, col3, col4 = st.columns(4)

        def download_csv(df, filename, button_text, col):
            if df is not None and not df.empty:
                csv = df.to_csv(index=False).encode('utf-8')
                col.download_button(label=button_text, data=csv,
                                    file_name=filename, mime='text/csv')
            else:
                col.warning(
                    f"Dados de {button_text.split(' ')[1]} não disponíveis para download.")

        if "df_ndvi_completo" in resultados:
            download_csv(resultados["df_ndvi_completo"], 'dados_ndvi.csv',
                         'Dataset NDVI', col1)
        else:
            col1.warning("Dados de NDVI não disponíveis.")
        if "df_produtividade_completo" in resultados:
            download_csv(resultados["df_produtividade_completo"], 'dados_produtividade.csv',
                         'Dataset Produtividade', col2)
        else:
            col2.warning("Dados de Produtividade não disponíveis.")
        if "df_meteorologicos_completo" in resultados:
            download_csv(resultados["df_meteorologicos_completo"], 'dados_meteorologicos.csv',
                         'Dataset Dados Metereológicos', col3)
        else:
            col3.warning("Dados Meteorológicos não disponíveis.")
        if "df_custos_completo" in resultados:
            download_csv(resultados["df_custos_completo"], 'dados_custos.csv',
                         'Dataset Custos', col4)
        else:
            col4.warning("Dados de Custos não disponíveis.")


# ===== FUNÇÃO SECUNDÁRIA PARA FORMATAÇÃO DOS VALORES NA PÁGINA PRODUTIVIDADE ======


# acrescenta o prefixo R$ e formata o valor com duas casas decimais
def formata_valores(valor, prefixo=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'


# formata o valor com duas casas decimais e acrescenta o sufixo desejado
def formata_valores_posfixo(valor, posfixo=''):

    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{valor:.2f} {unidade} {posfixo}'.strip()
        valor /= 1000
    return f'{valor:.2f} milhões {posfixo}'.strip()

# ===== FUNÇÃO DA PÁGINA 'SOBRE O PROJETO' ======


def exibir_pagina_sobre():
    st.header(" 🗺️ Sobre o Projeto")
    st.write("---")
    st.write("""
            Este projeto, referente a segunda fase do Challenge Ingredion do Curso de Inteligência Artificial da FiAP (1TIAO),
            tem como foco o desenvolvimento de um modelo de Inteligência Artificial para cálculo de previsão da produtividade agrícola, utilizando NDVI
            (Índice de Vegetação Normalizada), dados climáticos, de produtividade e custo.
            
            Os datasets utilizados no programa foram previamente tratados e limpos antes de serem carregados via APEX para a nuvem Oracle. Isso ocorreu pela
            natureza diversa das formatações e pela necessidade de padronização dos dados para garantir a integridade e a precisão das análises.
            
            Os valores faltantes foram tratados com a média dos dados disponíveis, e os dados foram convertidos para o formato adequado para análise.
            
            O projeto foi desenvolvido em Python, utilizando as bibliotecas Streamlit, Pandas, NumPy, Scikit-learn, Plotly, Pickle, Os, Requests, Locale e Datetime.       
        
    """)

    st.subheader(" 🌟 Nosso Time")

    nomes_com_espacos = "Jonatas Gomes&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Iolanda Manzali&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Murilo Nasser&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pedro Sousa&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Amanda Fragnan"
    st.write(nomes_com_espacos)

    st.subheader(" ⏳ Próximos Passos")
    st.write("""
            Este é um projeto em evolução. Inicialmente foi selecionada a cultura de milho da cidade de  Sorriso, localizada no estado do Mato Grosso.
            O programa foi construido para ser escalável, e para novas versões esperamos acrescentar novos dados para extrapolar o calculo da produtividade.
        """)

    st.write('👍🏻 Gostou do Projeto?')
    sentiment_mapping = ["1", "2", "3", "4", "5"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"Você selecionou {sentiment_mapping[selected]} estrelas!")
        st.balloons()

# ===== FUNÇÃO DA PÁGINA LINKS  ======


def exibir_links_importantes():

    st.write("""
            [IBGE](https://sidra.ibge.gov.br/tabela/839)            
            
            [INMET](https://portal.inmet.gov.br/dadoshistoricos)
                        
            [CONAB](https://www.conab.gov.br/info-agro/custos-de-producao/planilhas-de-custo-de-producao/item/16269-serie-historica-custos-milho-2-safra-2005-a-2021)
            
            [SATVEG](https://www.satveg.cnptia.embrapa.br)
    """)

# ====== FUNÇÃO DA PÁGINA DE PRODUTIVIDADE ======


def exibir_pagina_produtividade():
    st.header("Calcular Produtividade Futura")

    try:
        # Carregar dados para as opções de seleção (localidades e culturas)
        df_prod = carregar_dados_oracle("produtividade")
        if df_prod.empty:
            st.warning(
                "Não há dados de produtividade disponíveis para seleção.")
            return

        localidades = df_prod['localidade'].unique()
        culturas_base = df_prod['cultura'].unique()

        col1, col2 = st.columns(2)
        localidade_selecionada = col1.selectbox("Localidade", localidades)
        culturas_filtradas = df_prod[df_prod['localidade']
                                     == localidade_selecionada]['cultura'].unique()
        cultura_selecionada = col2.selectbox("Cultura", culturas_filtradas)

        col1, col2, col3 = st.columns(3)
        ano_atual = datetime.now().year
        anos_futuros = list(range(ano_atual, ano_atual + 6))
        ano_plantio = col1.selectbox("Ano de Plantio", anos_futuros)
        meses = list(range(1, 13))
        mes_plantio = col2.selectbox(
            "Mês de Plantio",
            meses,
            format_func=lambda x: datetime(ano_atual, x, 1).strftime("%B"),
        )
        area_plantada = col3.number_input(
            "Área Plantada (ha)", min_value=0.0, step=0.1)

        # Verificar se a área plantada é maior que zero
        if area_plantada == 0:
            st.error(
                "A área plantada deve ser maior que zero para realizar o cálculo.")
        else:
            # Botão para prever produtividade
            if st.button("Prever Produtividade", type="primary"):
                PASTA_MODELOS = "modelos_treinados"
                modelo_path = os.path.join(PASTA_MODELOS, "melhor_modelo.pkl")

                if not os.path.exists(modelo_path):
                    st.error(
                        "O melhor modelo não foi encontrado. Por favor, treine os modelos primeiro.")
                    return

                with open(modelo_path, "rb") as f:
                    melhor_modelo_data = pickle.load(f)
                    modelo = melhor_modelo_data.get('modelo', None)
                    modelo_nome = melhor_modelo_data.get(
                        'nome', 'Modelo desconhecido')
                    modelo_features = getattr(
                        modelo, 'feature_names_in_', None)

                # Preparar os dados de entrada para a predição
                input_data = pd.DataFrame({
                    'localidade': [localidade_selecionada],
                    'cultura': [cultura_selecionada],
                    'ano': [ano_plantio],
                    'mes': [mes_plantio],
                    'area_plantada': [area_plantada]
                })

                input_data = pd.get_dummies(input_data)

                if modelo_features is not None:
                    for feature in modelo_features:
                        if feature not in input_data.columns:
                            input_data[feature] = 0
                    input_data = input_data[modelo_features]
                elif hasattr(modelo, 'n_features_in_') and input_data.shape[1] != modelo.n_features_in_:
                    st.error(
                        f"Número de features de entrada ({input_data.shape[1]}) não corresponde ao esperado pelo modelo ({modelo.n_features_in_}).")
                    return

                # Realizar a predição
                predicao = modelo.predict(input_data)[0]

                st.info("Resultado da Predição")
                st.write(f"**Localidade:** {localidade_selecionada}")
                st.write(f"**Cultura:** {cultura_selecionada}")
                st.write(f"**Ano de Plantio:** {ano_plantio}")
                st.write(
                    f"**Mês de Plantio:** {datetime(ano_atual, mes_plantio, 1).strftime('%B')}")
                st.write(
                    f"**Área Plantada:** {formata_valores_posfixo(area_plantada, 'ha')}")
                st.write(
                    f"**Produtividade Prevista:** {formata_valores_posfixo(predicao, 'kg/ha')}")
                st.subheader(
                    f"Produção Total Estimada: {formata_valores(predicao * area_plantada, 'R$ ')}")
                st.caption(
                    f"Modelo utilizado para cálculo da produtividade: {modelo_nome}")

    except Exception as e:
        st.error(f"Ocorreu um erro ao realizar a previsão: {e}")

# ===== FUNÇÃO PÁGINA LINKS  ======


def exibir_links_importantes():

    st.header("🔗 Links Importantes")
    st.write("---")
    st.write("""
        Aqui estão alguns links úteis relacionados ao projeto:
    """)
    st.write("""
        [IBGE](https://sidra.ibge.gov.br/tabela/839)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[INMET](https://portal.inmet.gov.br/dadoshistoricos)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        [CONAB](https://www.conab.gov.br/info-agro/custos-de-producao/planilhas-de-custo-de-producao/item/16269-serie-historica-custos-milho-2-safra-2005-a-2021)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        [SATVEG](https://www.satveg.cnptia.embrapa.br)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        """)


# ===== FUNÇÃO PARA CARREGAR DADOS CSV ======

def exibir_pagina_carregar_dados():

    def upload_dados(tipo):

        st.subheader(tipo["titulo"])
        st.markdown(
            "Os dados devem estar em formato CSV e devem conter as seguintes colunas:<br>"
            f"<b>{tipo['colunas']}</b><br>",
            unsafe_allow_html=True
        )

        df = st.file_uploader(
            "Carregar arquivo CSV",
            type=["csv"],
            label_visibility="collapsed",
            help="Selecione o arquivo CSV",
            key=f"upload_{tipo['url']}"
        )
        if df is not None:
            try:
                df = pd.read_csv(df)
                if tipo == NDVI or tipo == METEOROLOGICOS:    
                    if 'DATA' in df.columns:
                        df['DATA'] = pd.to_datetime(df['DATA'], format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
                st.write("Preview dos dados:")
                st.dataframe(df.head(), hide_index=True)
                if st.button("Processar Dados", key="upload_dados", help="Carregar arquivo CSV", icon="📤"):
                    try:
                        dados = df.to_csv(index=False, quotechar='"', quoting=1)
                        response = requests.post(
                            f"{API_URL}/{tipo["url"]}/batchload?batchRows=500",
                            data=dados,
                            headers={"Content-Type": "text/csv"}
                        )
                        if "SUCCESS" in response.text:
                            st.success(f"Dados enviados com sucesso! {len(df)} registros processados.")
                            return True
                        elif "ERROR" in response.text:
                            st.error(f"Erro ao enviar dados: {response.status_code} - {response.text}")
                            return False
                    except Exception as e:
                        st.error(f"Erro durante o upload: {str(e)}")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {str(e)}")

        st.markdown("---")


    API_URL = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap"
    NDVI = {
        "titulo": "Dados NDVI",
        "url": "carga_ndvi",
        "colunas": '"ID", "LOCALIDADE", "CULTURA", "DATA", "NDVI"'
    }
    PRODUTIVIDADE = {
        "titulo": "Dados de Produtividade",
        "url": "carga_produtividade",
        "colunas": '"ID","LOCALIDADE","CULTURA","ANO","AREA_PLANTADA","AREA_COLHIDA","RENDIMENTO_MEDIO"'
    }
    METEOROLOGICOS = {
        "titulo": "Dados Meteorológicos",
        "url": "carga_dados_meteorologicos",
        "colunas": '"ID","LOCALIDADE","DATA","PRECIPITACAO","PRESSAO_ATMOSFERICA","RADIACAO_SOLAR_GLOBAL","TEMPERATURA_BULBO_SECO","TEMPERATURA_ORVALHO","UMIDADE_RELATIVA","VELOCIDADE_VENTO"'
    }

    # Cabeçalho
    st.header("☁️ Carga de Dados")
    st.markdown("---")

    # Conteúdo
    upload_dados(NDVI)
    upload_dados(PRODUTIVIDADE)
    upload_dados(METEOROLOGICOS)


# ===== FUNÇÃO DA PAGINA DE EXIBICAO DE TREINAMENTO DOS MODELOS ======


def treinar_modelos_supervisionados(X, y, modelos_selecionados):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    modelos = {
        'LinearRegression': (LinearRegression(), {}),
        'SVR': (SVR(), {'C': [0.1, 1, 10], 'kernel': ['rbf', 'linear', 'poly']}),
        'RandomForest': (RandomForestRegressor(), {
            'n_estimators': [100, 200],
            'max_depth': [None, 10],
            'min_samples_split': [2, 5]
        }),
        'GradientBoosting': (GradientBoostingRegressor(), {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'max_depth': [3, 5]
        }),
        'Ridge': (Ridge(), {'alpha': [0.1, 1.0, 10.0]}),
        'Lasso': (Lasso(), {'alpha': [0.1, 1.0, 10.0]}),
        'ElasticNet': (ElasticNet(), {'alpha': [0.1, 1.0, 10.0], 'l1_ratio': [0.2, 0.5, 0.8]}),
        'DecisionTree': (DecisionTreeRegressor(), {'max_depth': [None, 5, 10]}),
        'KNeighbors': (KNeighborsRegressor(), {'n_neighbors': [3, 5, 7]}),
        'AdaBoost': (AdaBoostRegressor(), {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1]})
    }

    resultados = {}
    for nome in modelos_selecionados:
        modelo, params = modelos[nome]
        try:
            with st.spinner(f"Treinando {nome}..."):
                grid = GridSearchCV(modelo, params, cv=5,
                                    scoring='neg_mean_squared_error',
                                    n_jobs=-1, verbose=0)
                grid.fit(X_train, y_train)
                y_pred = grid.predict(X_test)
                score = np.sqrt(mean_squared_error(y_test, y_pred))
                resultados[nome] = {
                    'score': score,
                    'melhor_modelo': grid.best_estimator_,
                    'melhores_params': grid.best_params_
                }
        except Exception as e:
            st.warning(f"Erro no modelo {nome}: {str(e)}")
    return resultados


def exibir_pagina_treinamento():
    st.header("📚 Treinamento de Modelos")
    st.markdown("---")

    modelos_opcoes = {
        'LinearRegression': 'Regressão Linear',
        'SVR': 'Máquina de Vetores de Suporte',
        'RandomForest': 'Random Forest',
        'GradientBoosting': 'Gradient Boosting',
        'Ridge': 'Ridge',
        'Lasso': 'Lasso',
        'ElasticNet': 'Elastic Net',
        'DecisionTree': 'Árvore de Decisão',
        'KNeighbors': 'KNN',
        'AdaBoost': 'AdaBoost'
    }

    st.write(
        "Selecione os modelos que deseja treinar. Você pode escolher mais de um modelo para comparação."
    )
    modelos_selecionados = st.multiselect(
        "Modelos",
        options=list(modelos_opcoes.keys()),
        format_func=lambda x: modelos_opcoes[x],
        default=[],
        label_visibility="collapsed",
    )

    if st.button("Iniciar Treinamento", type="primary"):
        if not modelos_selecionados:
            st.error("Selecione pelo menos um modelo!")
            return

        df = carregar_dados()
        if df.empty:
            st.error("Dados insuficientes para treinamento.")
            return

        X = pd.get_dummies(
            df.drop(columns=["rendimento_medio", "data"], errors='ignore'))
        y = df["rendimento_medio"]

        with st.spinner("Treinando modelos..."):
            resultados = treinar_modelos_supervisionados(
                X, y, modelos_selecionados)

            if resultados:
                melhor_modelo = min(
                    resultados, key=lambda k: resultados[k]['score'])
                PASTA_MODELOS = "modelos_treinados"
                os.makedirs(PASTA_MODELOS, exist_ok=True)

                # Salvar todos modelos
                for nome, info in resultados.items():
                    with open(os.path.join(PASTA_MODELOS, f"{nome}.pkl"), "wb") as f:
                        pickle.dump(info, f)

                # Salvar melhor modelo
                with open(os.path.join(PASTA_MODELOS, "melhor_modelo.pkl"), "wb") as f:
                    pickle.dump({
                        'nome': melhor_modelo,
                        'modelo': resultados[melhor_modelo]['melhor_modelo'],
                        'params': resultados[melhor_modelo]['melhores_params'],
                        'score': resultados[melhor_modelo]['score']
                    }, f)

                # Exibir resultados
                st.subheader("Resultados do Treinamento")
                st.success(
                    f"Melhor modelo: {melhor_modelo} (RMSE: {resultados[melhor_modelo]['score']:.2f})")

                with st.expander("Detalhes dos Modelos"):
                    for nome, info in resultados.items():
                        st.write(f"**{modelos_opcoes[nome]}**")
                        st.write(f"RMSE: {info['score']:.2f}")
                        st.write(
                            f"Melhores parâmetros: {info['melhores_params']}")
                        st.write("---")

                st.balloons()
            else:
                st.error("Nenhum modelo foi treinado com sucesso.")


def exibir_pagina_produtividade():
    st.header("💡 Estimativa de Produtividade")
    st.markdown("---")

    try:
        # Carregar dados para as opções de seleção (localidades e culturas)
        df_prod = carregar_dados_oracle("produtividade")
        if df_prod.empty:
            st.warning("Não há dados de produtividade disponíveis para seleção.")
            return
        localidades = df_prod['localidade'].unique()
        culturas_base = df_prod['cultura'].unique()

        col1, col2 = st.columns(2)
        localidade_selecionada = col1.selectbox("Localidade", localidades)
        culturas_filtradas = df_prod[df_prod['localidade']
                                     == localidade_selecionada]['cultura'].unique()
        cultura_selecionada = col2.selectbox("Cultura", culturas_filtradas)

        col1, col2, col3 = st.columns(3)
        ano_atual = datetime.now().year
        anos_futuros = list(range(ano_atual, ano_atual + 6))
        ano_plantio = col1.selectbox("Ano de Plantio", anos_futuros)
        meses = list(range(1, 13))
        mes_plantio = col2.selectbox(
            "Mês de Plantio",
            meses,
            format_func=lambda x: datetime(ano_atual, x, 1).strftime("%B"),
        )
        area_plantada = col3.number_input(
            "Área Plantada (ha)", min_value=0.0, step=0.1)

        if st.button("Calcular", type="primary"):
            PASTA_MODELOS = "modelos_treinados"
            modelo_path = os.path.join(PASTA_MODELOS, "melhor_modelo.pkl")

            if area_plantada == 0:
                st.error("A área plantada deve ser maior do que zero")
                return

            if not os.path.exists(modelo_path):
                st.error("O melhor modelo não foi encontrado. Por favor, treine os modelos primeiro.")
                return

            with open(modelo_path, "rb") as f:
                melhor_modelo_data = pickle.load(f)
                modelo = melhor_modelo_data.get('modelo', None)
                modelo_nome = melhor_modelo_data.get(
                    'nome', 'Modelo desconhecido')
                # Obter nomes das features esperadas
                modelo_features = getattr(modelo, 'feature_names_in_', None)

            # Preparar os dados de entrada para a predição
            input_data = pd.DataFrame({
                'localidade': [localidade_selecionada],
                'cultura': [cultura_selecionada],
                'ano': [ano_plantio],
                'mes': [mes_plantio],
                'area_plantada': [area_plantada]

            })

            input_data = pd.get_dummies(input_data)

            if modelo_features is not None:
                # Adicionar colunas ausentes com valor 0
                for feature in modelo_features:
                    if feature not in input_data.columns:
                        input_data[feature] = 0
                # Garantir a ordem correta das colunas
                input_data = input_data[modelo_features]
            elif hasattr(modelo, 'n_features_in_') and input_data.shape[1] != modelo.n_features_in_:
                st.error(
                    f"Número de features de entrada ({input_data.shape[1]}) não corresponde ao esperado pelo modelo ({modelo.n_features_in_}).")
                return

            # Realizar a predição
            predicao = modelo.predict(input_data)[0]
            st.info("RESULTADO", icon="ℹ️")
            st.write(f"**Localidade:** {localidade_selecionada}")
            st.write(f"**Cultura:** {cultura_selecionada}")
            st.write(f"**Ano de Plantio:** {ano_plantio}")
            st.write(
                f"**Mês de Plantio:** {datetime(ano_atual, mes_plantio, 1).strftime('%B')}")
            st.write(
                f"**Área Plantada:** {formata_valores_posfixo(area_plantada, 'ha')}")
            st.write(
                f"**Produtividade Prevista:** {formata_valores_posfixo(predicao, 'kg/ha')}")
            st.subheader(
                f"Produção Total Estimada: {formata_valores(predicao * area_plantada, 'R$ ')}"
            )
            st.caption(
                f"Modelo utilizado para cálculo da produtividade: {modelo_nome}")

    except Exception as e:
        st.error(f"Ocorreu um erro ao realizar a previsão: {e}")

# ===== FUNÇÃO PRINCIPAL ======


def main():
    st.subheader("Escolha uma opção abaixo:")
    colun1, colun2 = st.columns(2)

    if colun1.button("Sobre o Projeto", key="menu_sobre", type="secondary", use_container_width=True, icon="🗺️"):
        st.session_state.pagina_ativa = "sobre"
    if colun2.button("Links Importantes", key="menu_links", type="secondary", use_container_width=True, icon="🔗"):
        st.session_state.pagina_ativa = "links"
    if colun1.button("Carga de Dados", key="menu_carga", type="secondary", use_container_width=True, icon="☁️"):
        st.session_state.pagina_ativa = "carga"
    if colun2.button("Análise Exploratória", key="menu_analise", type="secondary", use_container_width=True, icon="🔍"):
        st.session_state.pagina_ativa = "analise"
    if colun1.button("**Treinamento de Modelos**", key="menu_treinamento", type="secondary", use_container_width=True, icon="📚"):
        st.session_state.pagina_ativa = "treinamento"
    if colun2.button("Estimativa de Produtividade", key="menu_previsao", type="primary", use_container_width=True, icon="💡"):
        st.session_state.pagina_ativa = "previsao"

    if "pagina_ativa" in st.session_state:
        if st.session_state.pagina_ativa == "sobre":
            exibir_pagina_sobre()
        elif st.session_state.pagina_ativa == "links":
            exibir_links_importantes()
        elif st.session_state.pagina_ativa == "carga":
            exibir_pagina_carregar_dados()
        elif st.session_state.pagina_ativa == "analise":
            analise_exploratoria()
        elif st.session_state.pagina_ativa == "treinamento":
            exibir_pagina_treinamento()
        elif st.session_state.pagina_ativa == "previsao":
            exibir_pagina_produtividade()


# CHAMADA DA FUNÇÃO PRINCIPAL
if __name__ == "__main__":
    if "pagina_ativa" not in st.session_state:
        st.session_state.pagina_ativa = None
    main()
