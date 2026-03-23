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

O fluxo conversacional do CardioAI foi projetado para simular um atendimento inicial em saúde cardiovascular, priorizando clareza, acessibilidade e naturalidade na interação com o usuário.

A comunicação entre os componentes do sistema ocorre de forma sequencial e integrada:

O usuário envia uma mensagem pela interface de chat
O frontend encaminha a requisição ao backend
O backend aciona a API do IBM Watson Assistant
O Watson processa a mensagem utilizando técnicas de NLP (Processamento de Linguagem Natural)
A resposta é retornada ao backend
O backend envia a resposta ao frontend
O usuário visualiza a resposta no chat em tempo real
🧠 Estrutura do Assistente

O assistente foi modelado com base nos principais componentes do IBM Watson Assistant, responsáveis por garantir a inteligência e organização do diálogo:

🔹 Entities (Entidades)

As entities permitem identificar informações específicas dentro das mensagens do usuário, tornando as respostas mais precisas e contextualizadas.

Exemplo:

Valores de pressão arterial:
“12 por 8”
“14 por 9”

Essas informações são utilizadas para adaptar a resposta de acordo com o contexto clínico informado.

🔹 Dialog Nodes (Nós de Diálogo)

Os dialog nodes são responsáveis por estruturar o fluxo da conversa e definir o comportamento do assistente em diferentes cenários.

Incluem:

Início da conversa (boas-vindas)
Respostas informativas sobre saúde cardiovascular
Orientações preventivas
Identificação de possíveis situações de risco
Nó de fallback (quando o sistema não compreende a mensagem)
🔄 Etapas do Fluxo Conversacional

O funcionamento do assistente segue um fluxo estruturado em etapas:

🟢 1. Início da Conversa

O usuário inicia a interação com uma mensagem ou saudação.

🟡 2. Interpretação (NLP)

O sistema analisa a mensagem e identifica a intenção do usuário.

🔵 3. Processamento

As entidades são extraídas e o fluxo é direcionado para o nó de diálogo correspondente.

🟣 4. Geração de Resposta

O assistente retorna uma resposta clara, objetiva e educativa.

🔴 5. Tratamento de Exceções

Caso a mensagem não seja compreendida, o sistema ativa o fallback, solicitando que o usuário reformule a pergunta.

## 🤖 IA Generativa

O CardioAI também utiliza recursos de IA Generativa para enriquecer o processamento das informações e melhorar a qualidade das respostas.

🔍 Aplicações da IA Generativa
Interpretar texto clínico não estruturado
Extrair informações relevantes da mensagem do usuário
Organizar dados do paciente de forma estruturada
Gerar respostas em formato JSON estruturado

## 📁 Estrutura das Pastas

- assets/ → imagens do projeto
- docs/ → documentação principal
- chatbot.py → integração com o Watson Assistant
- CardioIA_Chatbot-dialog.json → configuração do assistente (intents, entities, diálogos)
- index.html → interface do chatbot
- Relatório do Assistente Cardiológico Conversacional.pdf → documentação detalhada
- .gitignore → controle de versionamento
- README.md → guia do projeto


## ▶️ Como Executar o Projeto

- Clonar repositório
git clone <URL_DO_REPOSITORIO>
cd CardioAI

- (Opcional) Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

- Instalar dependências
pip install flask ibm-watson

- Executar
python chatbot.py

# 🎥 Vídeo de Demonstração

Confira abaixo a demonstração do funcionamento do CardioAI:

[![Assistir vídeo]


## 🗃 Histórico de lançamentos

* 1.0.0 - 23/03/2026
    

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
