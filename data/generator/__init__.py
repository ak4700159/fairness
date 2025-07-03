from article_generator import ArticleGenerator
import json
import datetime

if __name__ == "__main__":
    generator = ArticleGenerator()
    with open("../articles.json", 'r', encoding='utf-8') as f:
        articles = json.load(f)
    print(f"✅ 원본 기사 개수: {len(articles)}")  # 원본 기사 개수 출력
    new_articles = []
    for idx, article in enumerate(articles):
        print(f"\n▶️ {idx+1}번째 기사 제목: {article['기사제목']}")  # 현재 처리 중인 기사 제목 출력
        response = generator.generate(article["기사제목"], article["본문"])
        if response is None:
            print(f"❌ {idx+1}번째 기사에서 오류 발생")
            continue
        print(f"🔹 생성된 제목: {response['title']}")  # 생성된 제목 출력
        print(f"🔹 생성된 본문 일부: {response['content'][:100]}...")  # 생성된 본문 일부 출력

        new_article = {
            "기사제목": response["title"],
            "본문": response["content"],
            "URL": article["URL"],
            "신문사": "계명대학교 김승민",
            "작성일자": datetime.datetime.now().strftime("%Y.%m.%d. %p %I:%M")
        }
        new_articles.append(new_article)
        print(f"✅ 새 기사 추가 완료 (총 {len(new_articles)}개)")
        with open("../new_generated_articles2.json", 'w', encoding='utf-8') as f:
            json.dump(new_articles, f, ensure_ascii=False, indent=4)
    print("✅ 모든 기사 처리 완료")