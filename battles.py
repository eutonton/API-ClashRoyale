import requests
import json
from datetime import datetime


API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQwYzY3OGYxLWYyNTYtNDBjNy04ODE0LTBkNzI2Y2VmMWNkZSIsImlhdCI6MTc0Mzc5MjEzMywic3ViIjoiZGV2ZWxvcGVyLzNmM2VlMjBiLTg0YTItOTBkMi04MzI2LWFhOTAwZDY2YjUyZiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNjguMTk2LjQxLjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.BAtVDj4pxGsB-Leg4b-6_Ks8OoDTukhY5jUrmXki1j4V8a8LRXSXgTbLpGzLm9c9X3bqN-Vpk8Ctihy_2oRLjw'


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

    for idx, batalha in enumerate(batalhas[:3], 1): 
        print(f"\n🔹 BATALHA {idx}")
        tempo = datetime.strptime(batalha["battleTime"], "%Y%m%dT%H%M%S.000Z")
        print(f"🕒 Data: {tempo.strftime('%d/%m/%Y %H:%M')}")
        print(f"🎮 Modo: {batalha['gameMode']['name']}")
        print(f"🏟 Arena: {batalha['arena']['name']}\n")

        time_1 = batalha["team"][0]
        time_2 = batalha["opponent"][0]

        def mostrar_info(jogador, lado):
            print(f"{lado}: {jogador['name']}")
            print(f" - Troféus antes: {jogador.get('startingTrophies', 'N/A')}")
            print(f" - Troféus ganhos/perdidos: {jogador.get('trophyChange', 'N/A')}")
            print(f" - Coroas: {jogador['crowns']}")
            print(" - Deck:")
            for card in jogador["cards"]:
                print(f"   • {card['name']} (Nível {card['level']}, {card['rarity']})")
            print()

        mostrar_info(time_1, "👤 Jogador 1")
        mostrar_info(time_2, "👤 Jogador 2")

        print("🏆 Resultado:", end=" ")
        if time_1["crowns"] > time_2["crowns"]:
            print(f"{time_1['name']} venceu!")
        elif time_2["crowns"] > time_1["crowns"]:
            print(f"{time_2['name']} venceu!")
        else:
            print("Empate!")

        print("-" * 40)

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    print("=== 🔍 Consulta de Batalhas - Clash Royale ===")
    tag_usuario = input("Digite o playerTag (ex: #8UQY9V09): ").strip().upper()

    # Remove o '#' se o usuário incluir
    tag_formatado = tag_usuario.replace("#", "%23")

    buscar_batalhas(tag_formatado)
