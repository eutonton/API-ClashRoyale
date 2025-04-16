
# 🏰 Clash Royale Data Collector

Este projeto realiza a integração com a **API oficial do Clash Royale** para coletar **informações de jogadores**, **cartas** e **últimas batalhas**, armazenando tudo em um banco de dados **MongoDB**.

---

## 📁 Estrutura do Projeto

- `players.py`: Gerencia operações relacionadas aos jogadores.
- `battles.py`: Busca o histórico de batalhas de um jogador pela tag e salva no MongoDB.
- `cards.py`: Lista todas as cartas disponíveis no jogo e salva no MongoDB.

---

## ⚙️ Requisitos

- Python 3.7+
- Conta no [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) ou MongoDB local
- Token da [API do Clash Royale](https://developer.clashroyale.com/)

### 📦 Instalação de dependências

```bash
pip install pymongo requests
```

---

## 🔐 Configuração

1. Substitua o valor de `API_TOKEN` nos arquivos pelo seu token de acesso da API do Clash Royale.
2. Configure a URI do MongoDB nas linhas onde aparece:

```python
client = MongoClient('mongodb+srv://<usuário>:<senha>@<cluster>.mongodb.net/')
```

---

## 🚀 Como Usar

### 🔹 Obter Cartas

```bash
python cards.py
```
> Lista e salva no MongoDB todas as cartas disponíveis no jogo.

### 🔹 Buscar Batalhas por Jogador

```bash
python battles.py
```
> Será solicitado um `playerTag` no formato `#XXXXXXX`.

---

## 🧠 O Que Está Sendo Salvo

- **Cartas** (`cartas`):
  - Nome, raridade, custo de elixir, tipo, arena, nível máximo.

- **Batalhas** (`batalhas`):
  - Data, modo de jogo, arena, dados dos dois jogadores (deck, troféus, coroa), resultado da batalha.

---

## 📦 Banco de Dados MongoDB

As coleções utilizadas são:

- `db_clash_royale.cartas`
- `db_clash_royale.batalhas`

---

## 📌 Exemplo de Uso

```text
=== 🔍 Consulta de Batalhas - Clash Royale ===
Digite o playerTag (ex: #8UQY9V09): #8UQY9V09

🔹 BATALHA 1
🕒 Data: 15/04/2025 17:32
🎮 Modo: ladder
🏟 Arena: Legendary Arena

👤 Jogador 1: João
 - Troféus antes: 5300
 - Coroas: 2
 - Deck: Arqueiras, Gigante, Zap...

🏆 Resultado: João venceu!
```

---

