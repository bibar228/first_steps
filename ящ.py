import csv
from bs4 import BeautifulSoup
import json
import requests
import time


url = "https://health-diet.ru"
#создание хтмл копии страницы и ее использование в дальнейшем
#x = requests.get(url).text
with open("data/index.html", "r", encoding="UTF-8") as file:
    src = file.read()


soup = BeautifulSoup(src, "lxml").find_all(class_="mzr-tc-group-item-href")
#создание словаря с продуктами и ссылками
products_dict = {}
for i in soup:
    products_dict[i.text] = url + i.get("href")


count = 0
for name_product, link_product in products_dict.items():
    src = requests.get(link_product).text
    if BeautifulSoup(src, "lxml").find(class_="uk-alert-danger") != None:
        continue
    #запись хтмл конкретных продуктов в файл
    with open(f"data/{name_product}.html", "w", encoding="UTF-8") as file:
        file.write(src)

    with open(f"data/{name_product}.html", "r", encoding="UTF-8") as file:
        src = file.read()
    soup_zag = BeautifulSoup(src, "lxml").find("thead").find_all("th")
    soup = BeautifulSoup(src, "lxml").find("tbody").find_all("tr")
    product = soup_zag[0].text
    ccal = soup_zag[1].text
    proteins = soup_zag[2].text
    fats = soup_zag[3].text
    carbohydrates = soup_zag[4].text
    #запись названия столбцов в файл
    with open(f"data/{name_product}.csv", "w", encoding="UTF-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow((product, ccal, proteins, fats, carbohydrates))
    json_file = {}
    for i in soup:
        d = i.find_all("td")
        product = d[0].text.strip()
        ccal = d[1].text
        proteins = d[2].text
        fats = d[3].text
        carbohydrates = d[4].text
        #запись характеристик блюд в ексель
        with open(f"data/{name_product}.csv", "a+", encoding="UTF-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow((product, ccal, proteins, fats, carbohydrates))
        json_file[product] = f"Ккал: {ccal}", f"Протеины: {proteins}", f"Жиры :{fats}", f"Углеводы :{carbohydrates}"

    #создание json
    with open(f"data/{name_product}.json", "a+", encoding="UTF-8") as file:
        json.dump(json_file, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"Осталось итераций: {len(products_dict)-count}...")
    time.sleep(2)
print("Обработка завершена!")
