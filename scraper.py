from bs4 import BeautifulSoup
import os
import requests
import string

try:
    page_num = str(input())
    for i in range(1, int(page_num)+1):
        if not os.access(f"Page_{i}", os.F_OK):
            os.mkdir(f"Page_{i}")
        else:
            continue
    article_type_input = str(input())
    basic_url = "https://www.nature.com"
    for page in range(1, int(page_num)+1):
        os.chdir(f"/home/ded/PycharmProjects/Web Scraper/Web Scraper/task/Page_{page}")
        url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page}"
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(response.content, "html.parser")
        soup_list = soup.find_all("a", {"class": "c-card__link u-link-inherit"})
        soup_href_list = []

        for link in soup_list:
            soup_href_list.append(link.get("href"))
        for link in soup_href_list:
            article_url = basic_url + link
            article_response = requests.get(article_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            try:
                article_type = article_soup.find('span', {"class": "c-article-identifiers__type"})
                if article_type.text == article_type_input.upper():
                    article_body = article_soup.find('p', {"class": "article__teaser"}).text
                    title = article_soup.find('title').text
                    for i in title:
                        if i in string.punctuation or i == "—":
                            title = title.replace(i, "")
                    title = "_".join(title.split())
                    file = open(f"{title}.txt", "w")
                    file.write(article_body.strip())
                    file.close()
            except AttributeError:
                continue
            else:
                continue

        if response.status_code == 200:
            print("Saved all articles")
        else:
            print(f'The URL returned {response.status_code}')
except (KeyError, TypeError):
    print("Invalid page!")
