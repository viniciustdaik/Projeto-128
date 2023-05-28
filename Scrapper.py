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
end_reached = False
name_undefined = False
unconfirmed_brown_dwarfs_reached = False

# Loop for para extrair todas as tags <td>
for tr_tag in tr_tags:
    # print("tr_tags:", tr_tags, "\n")
    # print("tr_tag:", tr_tag)
    temp_list = []

    index = -1

    for td_tag in tr_tag.find_all("td"):
        index += 1
        data = td_tag.text.strip()

        if data == "L 34-26" and index == 0:
            end_reached = True
        elif data == "OGLE_TR_109" and index == 0:
            unconfirmed_brown_dwarfs_reached = True
        elif data == "SDSS J000013.54+255418.6 [de]" and index == 0:
            SDSS_reached = 1
            unconfirmed_brown_dwarfs_reached = False
        
        if data == "" and index == 0:
            name_undefined = True
        elif data != "" and index == 0 and name_undefined == True:
            name_undefined = False

        if (index == 0 or index == 5 or index == 8-SDSS_reached or index == 9-SDSS_reached) and end_reached == False and unconfirmed_brown_dwarfs_reached == False and name_undefined == False:
            # if SDSS_reached != 0:
            print("td_tag:", td_tag)
            indexToPrint = index
            if index == 8 or index == 9:
                indexToPrint = index-SDSS_reached

            if data == "":
                data = "No Info"

            print("data:", data+", index:", indexToPrint)

            #if end_reached != -4:
            #    end_reached += 1
            #    print("end_reached:", end_reached)

            # Guarde todas as linhas <td> na lista vazia que criamos anteriormente
            temp_list.append(data)

    if end_reached == False and unconfirmed_brown_dwarfs_reached == False and name_undefined == False:
        scarped_data.append(temp_list)

# print("scarped_data:", scarped_data)

headers = ["name", "distance", "mass", "radius"]
# "name", "radius", "mass", "distance"

# Defina o dataframe do Pandas
star_df_1 = pd.DataFrame(scarped_data, columns=headers)

# Converta para CSV
star_df_1.to_csv('scraped_data.csv', index=True, index_label="id")
