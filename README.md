# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# PROJETO - Cardio AI

![capa](https://github.com/Mu1518/Fase-5---Cap-1-Cardio-AI/blob/main/assets/capa.png)

## Grupo 20

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/jonatasgomes">Jônatas Gomes Alves</a>
- <a href="https://www.linkedin.com/in/iolanda-helena-fabbrini-manzali-de-oliveira-14ab8ab0">Iolanda Helena Fabbrini Manzali de Oliveira</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Murilo Carone Nasser</a> 
- <a href="https://www.linkedin.com/in/pedro-eduardo-soares-de-sousa-439552309">Pedro Eduardo Soares de Sousa</a>
- <a href= "https://www.linkedin.com/in/amanda-fragnan-b61537255">Amanda Fragnan<a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/leonardoorabona">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Andre Godoi Chaviato</a>

## 🔍 SOBRE O PROJETO
Bem-vindos ao Cardio AI

## 🫀 CardioAI — Assistente Cardiológico Inteligente

O **CardioAI** é um assistente cardiológico conversacional desenvolvido para simular um atendimento inicial em saúde utilizando técnicas de Inteligência Artificial, Processamento de Linguagem Natural (NLP) e automação.

O sistema interage com o paciente, interpreta informações clínicas básicas e retorna respostas organizadas e contextualizadas, auxiliando na compreensão inicial de sintomas cardiovasculares.


## 🎯 Objetivo do Projeto

Desenvolver um Assistente Cardiológico Inteligente capaz de:

 - Interagir com o usuário em linguagem natural
 - Simular triagem inicial cardiológica
 - Interpretar sintomas informados pelo paciente
 - Organizar respostas clínicas de forma estruturada
 - Integrar serviços de NLP
 - Disponibilizar interface simples de chat
 - Demonstrar automação inteligente aplicada à saúde

## 🧠 Tecnologias Utilizadas

 - Python
 - Flask
 - IBM Watson Assistant
 - NLP
 - HTML
 - CSS
 - JavaScript
 - IA Generativa
 - RPA
 - Banco de dados relacional
 - Banco de dados não relacional

## 🧩 ARQUITETURA DA SOLUÇÃO

A arquitetura do CardioAI foi projetada de forma modular, permitindo integração eficiente entre interface, backend e serviços de inteligência artificial.

O sistema é dividido em três camadas principais:

🔹 Camada de Interface (Frontend)

Responsável pela interação com o usuário.

Desenvolvida com HTML, CSS e JavaScript
Interface de chat simples e intuitiva
Permite envio e visualização de mensagens em tempo real
🔹 Camada de Aplicação (Backend)

Responsável pela comunicação entre usuário e inteligência artificial.

Desenvolvida em Python com Flask
Gerencia requisições HTTP
Controla sessões de conversa
Realiza integração com a API do Watson Assistant
🔹 Camada de Inteligência (IBM Watson Assistant)

Responsável pelo processamento de linguagem natural.

Interpretação das mensagens do usuário (NLP)
Identificação de intenções (intents)
Extração de entidades (entities)
Execução do fluxo conversacional (dialog nodes)

## 💬 Fluxo Conversacional

O fluxo conversacional do CardioAI foi desenvolvido para simular um atendimento inicial em saúde cardiovascular, priorizando clareza e acessibilidade.

Usuário envia mensagem pela interface
Frontend envia requisição para o backend
Backend aciona a API do Watson Assistant
O Watson processa a mensagem utilizando NLP
A resposta é retornada ao backend
Backend envia a resposta ao frontend
Usuário visualiza a resposta no chat

🧠 Estrutura do Assistente

O assistente foi modelado com base em três componentes principais:

🔹 Entities (Entidades)

Identificam informações específicas dentro da mensagem.

Exemplo:

Valores de pressão arterial:
“12 por 8”
“14 por 9”

Permitem respostas mais personalizadas e contextualizadas.

🔹 Dialog Nodes (Nós de Diálogo)

Controlam o fluxo da conversa e definem as respostas.

Incluem:

Início da conversa
Respostas informativas
Orientações preventivas
Identificação de possíveis riscos
Fallback (quando o sistema não entende a mensagem)

🔄 Etapas do Fluxo
🟢 1. Início da Conversa

O usuário inicia a interação com uma mensagem ou saudação.

🟡 2. Interpretação (NLP)

O sistema analisa a mensagem e identifica a intenção.

🔵 3. Processamento

O assistente verifica entidades e direciona para o fluxo adequado.

🟣 4. Resposta

O sistema retorna uma resposta clara, objetiva e educativa.

🔴 5. Tratamento de Exceções

Caso não compreenda a mensagem, o sistema solicita reformulação (fallback).

## 🤖 IA Generativa

O CardioAI também utiliza IA Generativa para:

Interpretar texto clínico não estruturado
Extrair informações relevantes
Organizar dados do paciente
Gerar resposta estruturada em JSON

## 📁 Estrutura das Pastas

- <b>assets</b>: imagens utilizadas no projeto e documentação
  
- <b>docs</b>: documentos prinicpais

- <b>README.md</b>: guia e explicação geral sobre o projeto

## ▶️ Como Executar o Projeto

# 🎥 Vídeo de Demonstração

Confira abaixo a demonstração do funcionamento do CardioAI:

[![Assistir vídeo]


## 🗃 Histórico de lançamentos

* 1.0.0 - 23/03/2026
    

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
