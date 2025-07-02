from article_generator import ArticleGenerator
import json

if __name__ == "__main__":
    # 텍스트 파일에 적혀 있는 openai API 키를 사용
    with open("../../config.json", 'r', encoding='utf-8') as file:
        api_key = json.load(file)["openai_api_key"]
    article_generator = ArticleGenerator(api_key=api_key)
    # articles = article_generator.generate_article_from_file("../articles.json", "../gen_articles.json")
    # article_generator.regenerate_missing_articles("../articles.json", "../new_generated_articles.json", "../new_generated_articles.json")