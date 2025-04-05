import requests
from pymongo import MongoClient
from datetime import datetime

# Token da API Clash Royale
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQwYzY3OGYxLWYyNTYtNDBjNy04ODE0LTBkNzI2Y2VmMWNkZSIsImlhdCI6MTc0Mzc5MjEzMywic3ViIjoiZGV2ZWxvcGVyLzNmM2VlMjBiLTg0YTItOTBkMi04MzI2LWFhOTAwZDY2YjUyZiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNjguMTk2LjQxLjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.BAtVDj4pxGsB-Leg4b-6_Ks8OoDTukhY5jUrmXki1j4V8a8LRXSXgTbLpGzLm9c9X3bqN-Vpk8Ctihy_2oRLjw'

# Conexão MongoDB
client = MongoClient('Conexão com o Cluster')
db = client.db_clash_royale
colecao_batalhas = db.batalhas

def buscar_batalhas(player_tag):
    url = f"https://api.clashroyale.com/v1/players/{player_tag}/battlelog"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro ao buscar dados da API:", response.status_code, response.text)
        return

    batalhas = response.json()

    colecao_batalhas.delete_many({"playerTag": player_tag})  # Limpa anteriores

    for idx, batalha in enumerate(batalhas[:3], 1):  # Puxar últimas 3
        tempo = datetime.strptime(batalha["battleTime"], "%Y%m%dT%H%M%S.000Z")
        time_1 = batalha["team"][0]
        time_2 = batalha["opponent"][0]

        documento = {
            "playerTag": player_tag,
            "data": tempo,
            "modo": batalha['gameMode']['name'],
            "arena": batalha['arena']['name'],
            "jogador_1": {
                "nome": time_1['name'],
                "trofeus_inicio": time_1.get('startingTrophies'),
                "trofeus_change": time_1.get('trophyChange'),
                "coroas": time_1['crowns'],
                "deck": [{
                    "nome": c['name'],
                    "nivel": c['level'],
                    "raridade": c['rarity']
                } for c in time_1['cards']]
            },
            "jogador_2": {
                "nome": time_2['name'],
                "trofeus_inicio": time_2.get('startingTrophies'),
                "trofeus_change": time_2.get('trophyChange'),
                "coroas": time_2['crowns'],
                "deck": [{
                    "nome": c['name'],
                    "nivel": c['level'],
                    "raridade": c['rarity']
                } for c in time_2['cards']]
            },
            "resultado": (
                time_1['name'] if time_1['crowns'] > time_2['crowns']
                else time_2['name'] if time_2['crowns'] > time_1['crowns']
                else "Empate"
            )
        }

        colecao_batalhas.insert_one(documento)

    print("\n=== ✅ Batalhas salvas no MongoDB! ===\n")
    exibir_batalhas_salvas(player_tag)

def exibir_batalhas_salvas(player_tag):
    batalhas = colecao_batalhas.find({"playerTag": player_tag}).sort("data", -1)

    for idx, batalha in enumerate(batalhas, 1):
        print(f"\n🔹 BATALHA {idx}")
        print(f"🕒 Data: {batalha['data'].strftime('%d/%m/%Y %H:%M')}")
        print(f"🎮 Modo: {batalha['modo']}")
        print(f"🏟 Arena: {batalha['arena']}\n")

        def mostrar_info(jogador, lado):
            print(f"{lado}: {jogador['nome']}")
            print(f" - Troféus antes: {jogador.get('trofeus_inicio', 'N/A')}")
            print(f" - Troféus ganhos/perdidos: {jogador.get('trofeus_change', 'N/A')}")
            print(f" - Coroas: {jogador['coroas']}")
            print(" - Deck:")
            for card in jogador["deck"]:
                print(f"   • {card['nome']} (Nível {card['nivel']}, {card['raridade']})")
            print()

        mostrar_info(batalha["jogador_1"], "👤 Jogador 1")
        mostrar_info(batalha["jogador_2"], "👤 Jogador 2")

        print("🏆 Resultado:", end=" ")
        if batalha["resultado"] == "Empate":
            print("Empate!")
        else:
            print(f"{batalha['resultado']} venceu!")

        print("-" * 40)

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    print("=== 🔍 Consulta de Batalhas - Clash Royale ===")
    tag_usuario = input("Digite o playerTag (ex: #8UQY9V09): ").strip().upper()
    tag_formatado = tag_usuario.replace("#", "%23")
    buscar_batalhas(tag_formatado)
