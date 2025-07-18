from crawler import Crawler 

class GoogleCrawler(Crawler):
    def __init__(self, keyword, max_pages=5):
        self.keyword = keyword
        self.max_pages = max_pages
        self.driver = None
        self.wait = None
        self.article_links = []
        self.results = [] # [{"기사제목" : "기사제목", "기사본문" : "기사본문"}, {"기사제목" : "기사제목", "기사본문" : "기사본문"},]

    def collect_article_links(self):
        print("temp")

    def extract_article_data(self):
        print("temp")

    def collect_articles(self):
        print("temp")

if __name__ == "__main__":
    crawler = GoogleCrawler(keyword="hello")
    crawler.run()