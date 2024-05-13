import time
from time import sleep

import requests
from bs4 import BeautifulSoup, PageElement
import pandas as pd

def safe_extract_text(element: PageElement):
    if element is not None:
        return element.text
    else:
        return ''

if __name__ == '__main__':

    for number in range(1, 200):
        time_1 = time.process_time()
        # Request
        html = requests.get(
            url=f"https://www.paginasamarillas.es/search/jardineros/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/{number}?what=jardineros",
            headers={'User-agent': 'Mozilla/5.0'}
        ).content

        # Extract data
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", {"class": "listado-item"})
        parsed_items = []
        for item in items:
            web_element = item.find("a", {"class": "web"})
            web_link = web_element['href'] if web_element else ''
            parsed_items.append({
                "name": safe_extract_text(item.find_next("span", {"itemprop": "name"})),
                "postal_code": safe_extract_text(item.find_next("span", {"itemprop": "postalCode"})),
                "province": safe_extract_text(item.find_next("span", {"itemprop": "addressRegion"})),
                "city": safe_extract_text(item.find_next("span", {"itemprop": "addressLocality"})),
                "phone": safe_extract_text(item.find_next("span", {"itemprop": "telephone"})),
                "address": safe_extract_text(item.find_next("span", {"itemprop": "streetAddress"})),
                "web": web_link
            })

        # Write file
        pd.DataFrame.from_dict(parsed_items).to_csv("jardineros.csv", mode='a', header=False)
        time_2 = time.process_time()
        print(f"Page {number} scrapped (time: {time_2 - time_1})")
