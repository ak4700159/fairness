import json
from chosun_crawler import ChosunCrawler
from khan_crawler import KhanCrawler
from korea_crawler import KoreaCrawler

# 크롤링된 기사 병합 아무것도 없는 빈문자열인 경우 제외해야됨 

def main():
    # keyword = "민생지원"
    # chosunCrawler = ChosunCrawler(keyword=keyword, max_pages=5) 
    # khanCrawler = KhanCrawler(keyword=keyword,max_pages=5)
    # koreaCrawler = KoreaCrawler(keyword=keyword,max_pages=2)
    # chosunCrawler.run()
    # khanCrawler.run()
    # koreaCrawler.run()

    with open(r"data\dumy\real\chosun_articls.json", 'r', encoding='utf-8') as f:
        articles1 = json.load(f)
    
    with open(r"data\dumy\real\korea_articls.json", 'r', encoding='utf-8') as f:
        articles2 = json.load(f)

    with open(r"data\dumy\real\khan_articls.json", 'r', encoding='utf-8') as f:
        articles3 = json.load(f)

    with open(r"data\dumy\total_articls.json", 'w', encoding='utf-8') as f:
        json.dump(articles1+articles2+articles3, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()