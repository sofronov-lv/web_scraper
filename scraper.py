import requests
import string

from bs4 import BeautifulSoup
from os import mkdir


class Articles:
    URL = "https://www.nature.com"
    PATH_PAGES = "/nature/articles?sort=PubDate&year=2020"

    def __init__(self, page_count: int, type_article: str):
        self.page_count = page_count
        self.type_article = type_article
        self.page = 0
        self.navigating_through_pages()

    def navigating_through_pages(self):
        """Navigating through pages (counting starts from the first one)
           Creating a folder whose name is Page_N, where N is the page number"""
        for page in range(1, self.page_count + 1):
            self.page = page
            mkdir(f"Page_{self.page}")  # creating a folder for a page
            page_number = f"&page={self.page}"
            self.search_all_articles(page_number)

    def search_all_articles(self, page_number):
        """Search all the articles on the page """
        response = requests.get(self.URL + self.PATH_PAGES + page_number)
        soup = BeautifulSoup(response.content, "html.parser")
        all_articles = (soup.find_all("article", {"class": "u-full-height c-card c-card--flush"}))
        self.search_necessary_articles(all_articles)

    def search_necessary_articles(self, all_articles):
        """Search for all necessary articles from the entire list
           (The required article is an article of the transmitted type)"""
        for article in all_articles:
            necessary_articles = article.find("span", {"class": "c-meta__item c-meta__item--block-at-lg"})
            necessary_articles = necessary_articles.text.replace("\n", "")

            if self.type_article == necessary_articles:
                file_name = self.get_name_for_file(article)
                link = article.find("a").get("href")  # link to the content of the article
                self.writing_page_text_to_file(file_name, link)

    @staticmethod
    def get_name_for_file(article):
        """Formation of the file name and subsequent receipt of the name of this file
           (The file name is formed from the title of the article)"""
        file_name = article.find("h3").text
        for i in string.punctuation:
            if i in file_name:
                file_name = file_name.replace(i, "")
        return file_name.replace("\n", "").replace(" ", "_") + ".txt"

    def writing_page_text_to_file(self, file_name, link):
        """Writing the text content of the desired page to a file
           that should be located in accordance with the page number"""
        new_response = requests.get(self.URL + link)
        new_soup = BeautifulSoup(new_response.content, "html.parser")
        new_page_text = new_soup.find("div", {"class": "c-article-body main-content"}).text

        with open(f"Page_{self.page}/{file_name}", "wb") as file:
            file.write(bytes(new_page_text, "utf-8"))


if __name__ == "__main__":
    pages = int(input())
    required_article = input()
    Articles(pages, required_article)
    print("Saved all articles")
