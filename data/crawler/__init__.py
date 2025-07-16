import json

# 크롤링된 기사 병합 아무것도 없는 빈문자열인 경우 제외해야됨 

if __name__ == "__main__":
    with open(r"C:\Users\cn120\바탕 화면\rag\fairness\data\dumy\real\chosun_articls.json", 'r', encoding='utf-8') as f:
        articles1 = json.load(f)
    
    with open(r"C:\Users\cn120\바탕 화면\rag\fairness\data\dumy\real\khan_articls.json", 'r', encoding='utf-8') as f:
        articles2 = json.load(f)

    with open(r"C:\Users\cn120\바탕 화면\rag\fairness\data\dumy\real\korea_articls.json", 'r', encoding='utf-8') as f:
        articles3 = json.load(f)

    with open(r"C:\Users\cn120\바탕 화면\rag\fairness\data\dumy\total_articles.json", 'w', encoding='utf-8') as f:
        json.dump(articles1+articles2+articles3, f, ensure_ascii=False, indent=4)