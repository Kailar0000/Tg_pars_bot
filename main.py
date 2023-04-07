import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0"
    }
    url = "https://moscow.flamp.ru/firm/elementaree_sluzhba_dostavki_produktov_s_receptami-70000001024084391"
    r = requests.get(url=url, headers=headers)


    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("cat-entities-ugc-item")

    new_dict = {}
    for article in articles_cards:
        article_title = article.find("a", class_="link name t-text t-text--bold").text.strip()
        article_desc = article.find("p", class_="t-rich-text__p").text.strip()
        article_id = article.find("article", class_="ugc-item").get("data-entity-id")

        article_data_taime = article.find("cat-brand-ugc-date").get("date")
        data_from_iso = datetime.fromisoformat(article_data_taime)
        data_taime = datetime.strftime(data_from_iso, "%Y-%m-%d %H:%M:%S")
        article_data_taimestamp = time.mktime(datetime.strptime(data_taime, "%Y-%m-%d %H:%M:%S").timetuple())

        new_dict[article_id] = {
            "article_data_taimestamp": article_data_taimestamp,
            "article_title":article_title,
            "article_desc": article_desc,
        }

        with open("news_dict.json", "w", encoding="UTF-8") as file:
            json.dump(new_dict, file, indent=4, ensure_ascii=False)

def check_news_update():
    with open("news_dict.json",  encoding="UTF-8") as file:
        new_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0"
    }
    url = "https://moscow.flamp.ru/firm/elementaree_sluzhba_dostavki_produktov_s_receptami-70000001024084391"
    r = requests.get(url=url, headers=headers)


    soup = BeautifulSoup(r.text, "lxml")
    articles_cards=soup.find_all("a", class_="article-card")

    fresh_news = {}
    for article in articles_cards:
        article_id = article.find("article", class_="ugc-item").get("data-entity-id")

        if article_id in new_dict:
            continue
        else:
            for article in articles_cards:
                article_title = article.find("a", class_="link name t-text t-text--bold").text.strip()
                article_desc = article.find("p", class_="t-rich-text__p").text.strip()
                article_id = article.find("article", class_="ugc-item").get("data-entity-id")

                article_data_taime = article.find("cat-brand-ugc-date").get("date")
                data_from_iso = datetime.fromisoformat(article_data_taime)
                data_taime = datetime.strftime(data_from_iso, "%Y-%m-%d %H:%M:%S")
                article_data_taimestamp = time.mktime(datetime.strptime(data_taime, "%Y-%m-%d %H:%M:%S").timetuple())

                new_dict[article_id] = {
                    "article_data_taimestamp": article_data_taimestamp,
                    "article_title": article_title,
                    "article_desc": article_desc,
                }

            fresh_news[article_id] = {
                "article_data_taimestamp": article_data_taimestamp,
                "article_title":article_title,
                "article_desc": article_desc,
            }
    with open("news_dict.json", "w", encoding="UTF-8") as file:
        json.dump(new_dict, file, indent=4, ensure_ascii=False)

    return fresh_news

def main():
    #get_first_news()
    check_news_update()

if __name__ == '__main__':
    main()


