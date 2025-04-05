import requests
from pymongo import MongoClient

# Token da API Clash Royale
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQwYzY3OGYxLWYyNTYtNDBjNy04ODE0LTBkNzI2Y2VmMWNkZSIsImlhdCI6MTc0Mzc5MjEzMywic3ViIjoiZGV2ZWxvcGVyLzNmM2VlMjBiLTg0YTItOTBkMi04MzI2LWFhOTAwZDY2YjUyZiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNjguMTk2LjQxLjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.BAtVDj4pxGsB-Leg4b-6_Ks8OoDTukhY5jUrmXki1j4V8a8LRXSXgTbLpGzLm9c9X3bqN-Vpk8Ctihy_2oRLjw'

# URL da API
url = 'https://api.clashroyale.com/v1/cards'

# Cabeçalhos da requisição
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

#Conexão com o MongoDB
client = MongoClient('Conexão com o Cluster')
db = client.db_clash_royale 
colecao_cartas = db.cartas 

# Requisição GET
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    cards = data.get('items', [])

    # Limpa a coleção para evitar duplicações
    colecao_cartas.delete_many({})

    # Prepara e insere os dados
    for card in cards:
        documento = {
            'id': card['id'],
            'nome': card['name'],
            'raridade': card['rarity'],
            'nivel_maximo': card['maxLevel'],
            'elixir': card.get('elixirCost', None),
            'tipo': card.get('type', None),
            'arena': card.get('arena', 'Desconhecida')
        }

        # Primeiro imprime
        print(f"Nome: {documento['nome']}")
        print(f"Raridade: {documento['raridade']}")
        print(f"Nível Máximo: {documento['nivel_maximo']}")
        print(f"Elixir: {documento['elixir'] if documento['elixir'] is not None else 'N/A'}")
        print('-' * 30)

        # Depois insere
        colecao_cartas.insert_one(documento)
        print(f"Inserido: {documento['nome']}\n")

    print(f"✅ Total de cartas inseridas: {len(cards)}")

else:
    print(f" Erro ao acessar a API: {response.status_code}")
    print(response.text)
