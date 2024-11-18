"""
    Programa para acessar o site de empregos "maringá.com" e listar todos os empregos anunciados pelas empresas
    Os anúncios são armazenados em um dataframe e é salvo um arquivo em .xlsx com todos os resultados obtidos
"""

from requests_html import HTMLSession
import pandas as pd
import time

session = HTMLSession()
jobs_list = list()

# Definindo até qual página será percorrido
LAST_PAGE = 10

def main():
    return parse_jobs(parse_page_links())

# Criando uma lista com todos os links que deverá ser percorrido
def parse_page_links():
    all_links = list()
    for page in range(1, LAST_PAGE + 1):
        url = f"https://empregos.maringa.com/?vagas-de-emprego={page}"
        all_links.append(url)
    return all_links

def parse_jobs(urls):
    for url in urls:
        response = session.get(url)
        #size = len(response.html.find("div.card-anuncio.mb-3"))
        for r in response:
            job =  {
                "job_title": r.html.find("b.flex-wrap").text,
                "company_name": r.html.find("div.d-none.d-md-block").text,
                "job_area": r.html.find("p.descricao small").text,
                "publication_date": r.html.find("small.text-nowrap.ml-4").text,
                "job_link": r.html.find("a.flex-wrap[href]").attrs["href"]
            }
            jobs_list.append(job)

        time.sleep(1)

if __name__ == "__main__":
    main()

df = pd.DataFrame(jobs_list)
#df["publication_date"] = pd.to_datetime(df["publication_date"], format = "%d/%m/%Y %H:%M").dt.strftime("%d/%m/%Y %H:%M")
#df["job_title"] = df["job_title"].str.lower()
#df = df[df["job_title"].str.contains("analista|dados|dado|b.i.|b.i|power|inteligência|inteligencia|business|intelligence")]

#df.to_excel("C:\\Users\\diogo\\Downloads\\empregos.xlsx", sheet_name = "empregos")
print(df)