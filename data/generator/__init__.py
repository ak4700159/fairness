from article_generator import ArticleGenerator
import json

if __name__ == "__main__":
    # 텍스트 파일에 적혀 있는 openai API 키를 사용
    # with open("../../config.json", 'r', encoding='utf-8') as file:
        # api_key = json.load(file)["openai_api_key"]
    # article_generator = ArticleGenerator(api_key=api_key)
    # articles = article_generator.generate_article_from_file("../articles.json", "../gen_articles.json")
    # article_generator.regenerate_missing_articles("../articles.json", "../new_generated_articles.json", "../new_generated_articles.json")
    with open("../articles.json", 'r', encoding='utf-8') as f:
        articles = json.load(f)

        for article in articles:
            pub_date = article.get("작성일자", "")
            pub_date = pub_date.replace("오전", "AM").replace("오후", "PM")
            article["작성일자"] = pub_date

        with open("../articles.json", 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)

        print(f"✅ 작성일자 변환 완료: ../articles.json")