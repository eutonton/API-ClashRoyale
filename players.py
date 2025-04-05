import requests
from pymongo import MongoClient

# Token da API Clash Royale
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQwYzY3OGYxLWYyNTYtNDBjNy04ODE0LTBkNzI2Y2VmMWNkZSIsImlhdCI6MTc0Mzc5MjEzMywic3ViIjoiZGV2ZWxvcGVyLzNmM2VlMjBiLTg0YTItOTBkMi04MzI2LWFhOTAwZDY2YjUyZiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNjguMTk2LjQxLjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.BAtVDj4pxGsB-Leg4b-6_Ks8OoDTukhY5jUrmXki1j4V8a8LRXSXgTbLpGzLm9c9X3bqN-Vpk8Ctihy_2oRLjw'

# Conexão com o MongoDB
client = MongoClient('Conexão com Cluster')
db = client.db_clash_royale
colecao_jogadores = db.jogadores

def buscar_info_jogador(player_tag):
    url = f"https://api.clashroyale.com/v1/players/{player_tag}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro ao buscar jogador:", response.status_code, response.text)
        return

    dados = response.json()
    

    documento = {
        "nickname": dados.get("name"),
        "nivel": dados.get("expLevel"),
        "trofeus": dados.get("trophies"),
        "tempo_jogo": None
    }

    # Inserção no MongoDB
    colecao_jogadores.insert_one(documento)
    print("✅ Jogador inserido com sucesso no MongoDB!")
    print("📄 Documento inserido:", documento)


# === EXECUÇÃO ===
if __name__ == "__main__":
    print("=== Consulta e Inserção de Jogador ===")
    tag = input("Digite o playerTag (ex: #8UQY9V09): ").strip().upper()
    tag_formatado = tag.replace("#", "%23")

    buscar_info_jogador(tag_formatado)
