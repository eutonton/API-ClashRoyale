import requests

API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQwYzY3OGYxLWYyNTYtNDBjNy04ODE0LTBkNzI2Y2VmMWNkZSIsImlhdCI6MTc0Mzc5MjEzMywic3ViIjoiZGV2ZWxvcGVyLzNmM2VlMjBiLTg0YTItOTBkMi04MzI2LWFhOTAwZDY2YjUyZiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNjguMTk2LjQxLjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.BAtVDj4pxGsB-Leg4b-6_Ks8OoDTukhY5jUrmXki1j4V8a8LRXSXgTbLpGzLm9c9X3bqN-Vpk8Ctihy_2oRLjw'

url = 'https://api.clashroyale.com/v1/cards'

# Cabeçalhos da requisição
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Requisição GET para a API
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    cards = data.get('items', [])

    # Mostra informações básicas de cada carta
    for card in cards:
        print(f"Nome: {card['name']}")
        print(f"Raridade: {card['rarity']}")
        print(f"Nível Máximo: {card['maxLevel']}")
        print(f"Elixir: {card.get('elixirCost', 'N/A')}")
        print('-' * 30)
else:
    print(f"Erro ao acessar a API: {response.status_code}")
    print(response.text)
