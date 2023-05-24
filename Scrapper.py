from bs4 import BeautifulSoup
import pandas as pd
import requests

# URL do exoPlanetas da Nasa
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Faça uma requisição da página usando o módulo request
site = requests.get(START_URL)
print("site:", site)

soup = BeautifulSoup(site.content, "html.parser")

# Obtenha todas as tabelas da página usando o método find_all()
tbody = soup.find_all('tbody')  # _all('tbody')
# print("tbody:", tbody)

# Crie uma lista vazia
scarped_data = []

# Obtenha todas as tags <tr> da tabela
tr_tags = soup.find_all("tr")  # tbody.find_all("tr")

SDSS_reached = 0
L3426_reached = -4

# Loop for para extrair todas as tags <td>
for tr_tag in tr_tags:
    # print("tr_tags:", tr_tags, "\n")
    # print("tr_tag:", tr_tag)
    temp_list = []

    index = -1

    for td_tag in tr_tag.find_all("td"):
        index += 1
        if (index == 0 or index == 5 or index == 8-SDSS_reached or index == 9-SDSS_reached) and L3426_reached < 0:
            data = td_tag.text.strip()
            # if SDSS_reached != 0:
            # print("td_tag:", td_tag)
            print("data:", data)

            if L3426_reached != -4:
                L3426_reached += 1
                print("L3426_reached:", L3426_reached)

            if data == "SDSS J000013.54+255418.6 [de]" and index == 0:
                SDSS_reached = 1
            elif data == "L 34-26" and index == 0:
                SDSS_reached = 0
                L3426_reached += 1

            if data == "":
                data = "?"

            # Guarde todas as linhas <td> na lista vazia que criamos anteriormente
            temp_list.append(data)
        else:
            pass
            # print("SDSS_reached:", SDSS_reached,
            #      "L3426_reached:", L3426_reached)

    scarped_data.append(temp_list)

# print("scarped_data:", scarped_data)

print("sadsars_reached:", L3426_reached)

headers = ["name", "distance", "mass", "radius"]
# "name", "radius", "mass", "distance"

# Defina o dataframe do Pandas
star_df_1 = pd.DataFrame(scarped_data, columns=headers)

# Converta para CSV
star_df_1.to_csv('scraped_data.csv', index=True, index_label="id")
