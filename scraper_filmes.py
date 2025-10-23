import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.imdb.com/chart/top/"    #URL alvo

headers = {  #Cabeçalho para evitar bloqueios
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

response = requests.get(url, headers=headers)

if response.status_code == 403:
    print("🚫 Acesso negado (Erro 403). O IMDb bloqueou a requisição.")
    print("💡 Tente novamente mais tarde ou use outro cabeçalho de navegador.")
    exit()

if response.status_code != 200:  #Verifica se deu certo
    print(f"Erro ao carregar página: {response.status_code}")
    exit()
    
soup = BeautifulSoup(response.text, "html.parser")  #Faz o parsing do HTML

filmes = soup.select('li.ipc-metadata-list-summary-item', limit=25)  #Seleciona os filmes

dados= []
for f in filmes:
    titulo = f.find('h3').get_text(strip=True)
    nota_tag = f.find('span', class_='ipc-rating-star')
    nota = nota_tag.get_text(strip=True) if nota_tag else "N/A"
    dados.append({"Título": titulo, "Nota": nota})
    
print("🎬 Top 25 filmes do IMDb: ")  #Exibe no console
for d in dados:
    print(f"- {d['Título']} (Nota: {d['Nota']})")
    
df = pd.DataFrame(dados)  #Salva em CSV
df.to_csv('filmes_imdb.csv', index=False, encoding='utf-8-sig')
print("\n✅ Dados salvos em 'filmes_imdb.csv'")




    


