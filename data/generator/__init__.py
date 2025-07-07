from article_generator import ArticleGenerator
import json
import datetime
import nest_asyncio
import asyncio

async def generateArticleByGenertor(generator, label, articles) :
    new_articles = []
    for idx, article in enumerate(articles):
        print(f"\n▶️ {idx+1}번째 [{label}] 기사 생성 시작: \"{article['기사제목']}\"")
        # print(f"\n▶️ {idx+1}번째 기사 제목: {article['기사제목']}")  # 현재 처리 중인 기사 제목 출력
        for trial in range(5):
            print(f"  └ {trial+1}번째 시도 중...", end=' ')
            response = await generator.generate(article["기사제목"], article["본문"])
            if response is None:
                print(f"❌ {idx+1}번째 기사에서 오류 발생")
                continue
            # print(f"🔹 생성된 제목: {response['title']}")  # 생성된 제목 출력
            # print(f"🔹 생성된 본문 일부: {response['content'][:100]}...")  # 생성된 본문 일부 출력

            new_article = {
                "기사제목": response["title"],
                "본문": response["content"],
                "URL": article["URL"],
                "신문사": "계명대학교 김승민",
                "작성일자": datetime.datetime.now().strftime("%Y.%m.%d. %p %I:%M"),
                "편향" : label
            }
            new_articles.append(new_article)
    return new_articles

async def main() :
    # 정치적으로 반대되는 성향 글 생성기
    generator1 = ArticleGenerator(
        "주어진 원본 기사 본문 : {content} \n" \
        "원본 기사제목 : {title}를 보고 새로운 기사 본문과 제목를 생성해주세요. \n " \
        "주어진 기사의 내용을 바탕으로 작성해야되며 주어진 기사와 비슷한 어조를 사용하고 " \
        "원본 기사와 정치적인 성향과 반대되는 입장에서 비판적인 기사 본문을 생성해내시오" \
        "생성된 본문을 자극적으로 나타내는 기사제목을 작성해야 되고 분량은 원본 분량과 비슷해야합니다." \
        "인터뷰 내용이 있다면 정치적성향과 반대되는 입장에서 유리하도록 인터뷰를 작성하시오." \
        "\n {format_instructions}"
    )

    # 세대적인 관점에서의 글 생성기
    generator2 = ArticleGenerator(
        "주어진 원본 기사 본문 : {content} \n" \
        "원본 기사제목 : {title}를 보고 새로운 기사 본문과 제목를 생성해주세요. \n " \
        "주어진 기사의 내용을 바탕으로 작성해야되며 주어진 기사와 비슷한 어조를 사용하고 " \
        "또한 원본 기사를 세대적인 관점 입장에서 원본 기사 내용을 분석하고 나올 수 있는 본문을 생성해내시오" \
        "생성된 본문을 자극적으로 나타내는 기사제목을 작성해야 되고 분량은 원본 분량과 비슷해야합니다." \
        "인터뷰 내용이 있다면 세대적인 관점에 나올 수 있는 인터뷰를 생성하시오." \
        "\n {format_instructions}"
    )

    # 종교적인 측면에서 글 생성기
    generator3 = ArticleGenerator(
        "주어진 원본 기사 본문 : {content} \n" \
        "원본 기사제목 : {title}를 보고 새로운 기사 본문과 제목를 생성해주세요. \n " \
        "주어진 기사의 내용을 바탕으로 작성해야되며 주어진 기사와 비슷한 어조를 사용하고 " \
        "또한 원본 기사를 종교적인 측면에서 원본 기사 내용을 분석하고 나올 수 있는 본문을 생성해내시오" \
        "생성된 본문을 자극적으로 나타내는 기사제목을 작성해야 되고 분량은 원본 분량과 비슷해야합니다." \
        "인터뷰 내용이 있다면 종교적인 측면에 나올 수 있는 인터뷰를 생성하시오." \
        "\n {format_instructions}"
    )

    # 민족적인 측면에서 글 생성기
    generator4 = ArticleGenerator(
        "주어진 원본 기사 본문 : {content} \n" \
        "원본 기사제목 : {title}를 보고 새로운 기사 본문과 제목를 생성해주세요. \n " \
        "주어진 기사의 내용을 바탕으로 작성해야되며 주어진 기사와 비슷한 어조를 사용하고 " \
        "또한 원본 기사를 민족적인 측면에서 원본 기사 내용을 분석하고 나올 수 있는 본문을 생성해내시오" \
        "생성된 본문을 자극적으로 나타내는 기사제목을 작성해야 되고 분량은 원본 분량과 비슷해야합니다." \
        "인터뷰 내용이 있다면 민족적인 측면에 나올 수 있는 인터뷰를 생성하시오." \
        "\n {format_instructions}"
    )

    # 성별 측면에서 글 생성기
    generator5 = ArticleGenerator(
        "주어진 원본 기사 본문 : {content} \n" \
        "원본 기사제목 : {title}를 보고 새로운 기사 본문과 제목를 생성해주세요. \n " \
        "주어진 기사의 내용을 바탕으로 작성해야되며 주어진 기사와 비슷한 어조를 사용하고 " \
        "또한 원본 기사를 성별 측면에서 원본 기사 내용을 분석하고 나올 수 있는 본문을 생성해내시오" \
        "생성된 본문을 자극적으로 나타내는 기사제목을 작성해야 되고 분량은 원본 분량과 비슷해야합니다." \
        "인터뷰 내용이 있다면 성별 측면에 나올 수 있는 인터뷰를 생성하시오." \
        "\n {format_instructions}"
    )

    generators = [
        (generator1, "정치"),
        (generator2, "세대"),
        (generator3, "종교"),
        (generator4, "민족"),
        (generator5, "성별")
    ]
    with open("../target_articles.json", 'r', encoding='utf-8') as f:
        articles = json.load(f)
    print(f"✅ 원본 기사 개수: {len(articles)}")  # 원본 기사 개수 출력
    new_articles = []

    # 멀티스레딩 방식(비동기 요청)으로 동작
    # generator마다 모든 기사에 대해 비동기로 기사 생성 (각 generator의 결과를 합침)
    tasks = []
    # 비동기 작업 추가
    for generator, label in generators:
        tasks.append(generateArticleByGenertor(generator, label, articles))
    # 비동기 작업 대기 + 결과 모으기
    results = await asyncio.gather(*tasks)
    for articles_by_gen in results:
        new_articles.extend(articles_by_gen)
    with open("../generated_articles2.json", 'w', encoding='utf-8') as f:
        json.dump(new_articles, f, ensure_ascii=False, indent=4)
    print("✅ 모든 기사 처리 완료")

if __name__ == "__main__":
    asyncio.run(main())
