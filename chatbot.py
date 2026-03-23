import requests
import json

# -----------------------------
# CONFIGURAÇÕES
# -----------------------------
apikey = "IMg7aKGjBbU-Szjh7RQK4Tc3gxGWfunoXY-Ir9CxKw3F"
assistant_id = "6c813ce8-316d-4e42-b3e0-b9740c9dd489"
base_url = "https://api.us-south.assistant.watson.cloud.ibm.com"
version = "2024-08-25"  # Parâmetro obrigatório da API REST

auth = ("apikey", apikey)

# -----------------------------
# 1️⃣ Criar sessão
# -----------------------------
session_url = f"{base_url}/v2/assistants/{assistant_id}/sessions?version={version}"
response = requests.post(session_url, auth=auth)
session_data = response.json()

print("Dados da sessão:", json.dumps(session_data, indent=2))

session_id = session_data.get("session_id")
if not session_id:
    raise Exception("Erro: não foi possível criar a sessão. Confira a API Key e o Assistant ID.")

print("Sessão criada com sucesso! Session ID:", session_id)

# -----------------------------
# 2️⃣ Enviar mensagem
# -----------------------------
message_url = f"{base_url}/v2/assistants/{assistant_id}/sessions/{session_id}/message?version={version}"
user_input = "Olá, assistente!"

payload = {"input": {"text": user_input}}

message_response = requests.post(message_url, auth=auth, json=payload)
message_json = message_response.json()

print("\nResposta do assistente:")
print(json.dumps(message_json, indent=2))

# -----------------------------
# 3️⃣ Fechar sessão
# -----------------------------
requests.delete(f"{base_url}/v2/assistants/{assistant_id}/sessions/{session_id}?version={version}", auth=auth)
print("\nSessão encerrada com sucesso!")