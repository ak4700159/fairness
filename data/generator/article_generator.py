from openai import OpenAI
import json
import re
from datetime import datetime


class ArticleGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def escape_inner_quotes(self, match):
        key = match.group(1)
        value = match.group(2)

        # 유니코드 따옴표 → ASCII
        value = value.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")

        # 본문 내부의 " 이스케이프
        # 단, 이미 escape된 경우는 중복 방지
        value = re.sub(r'(?<!\\)"', r'\\"', value)

        return f'"{key}": "{value}"'

    def extract_and_clean_json(self, text):
        """
        OpenAI 응답에서 JSON 객체 블록만 추출하고 유니코드 따옴표와 문제되는 문자를 정제한다.
        """
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            print("❌ JSON 객체를 찾을 수 없음")
            return None

        json_str = match.group()
        #본문 필드만 먼저 escape 처리
        json_str = re.sub(r'"(본문)"\s*:\s*"(.*?)"', self.escape_inner_quotes, json_str, flags=re.DOTALL)
        #나머지 유니코드 따옴표도 정리 (본문 외)
        json_str = json_str.replace("“", "\"").replace("”", "\"").replace("‘", "'").replace("’", "'")

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("❌ JSON 디코딩 실패:", e)
            print("📦 원본 문자열:\n", json_str)
            return None

    def generate_article(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": f"""
                 당신은 훌륭한 기사 작성자입니다. 주어진 프롬프트 기사와 반대되는 견해를 가지는 기사를 작성하는 것이 목표입니다. 작성한 내용은 JSON 형식으로 반환되어야 합니다. 양식은 다음과 같습니다. 
                 {{\"기사제목\": \"기사 제목\", \"본문\": \"기사 내용\", \"작성일자\": \"생성시점 시간\", \"신문사\": \"Comnet\", \"URL\": \"AI생성\"}}. 해당 양식에서 신문사는 계명대학교로 작성하고 URL은 기존 기사와 동일하게 작성합시오.
                    작성일자는 {datetime.now().strftime("%Y.%m.%d. %p %I:%M")} 시간으로 작성하십시오. 그리고 본문의 길이는 주어진 기사와 비슷한 길이로 작성하십시오.
                기존 기사 내용을 보면 대부분 대화식 인터뷰 문장도 있는데 이런 인터뷰 문장도 반대측 입장에서 유리하게 변형해 작성하십시오.
                 """},
                {"role": "user", "content": prompt}
            ]
        )
        return self.extract_and_clean_json(response.choices[0].message.content)


    def generate_article_from_file(self, file_path, output_file):
        """ 
            다음과 같은 JSON 형식을 담는 파일을 읽는다. 배열의 형태로 데이터가 담겨져 있다.
            [{
                    "신문사": press_name,
                    "기사제목": title,
                    "본문": body,
                    "작성일자": pub_date,
                    "URL": url
            },]
        """ 
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        articles = []
        for item in data:
            prompt = f"{item['신문사']}의 {item['기사제목']}, {item['URL']}에 대한 기사를 작성하십시오."
            # json 형식 기사 생성
            article = self.generate_article(prompt)
            if article is None:
                print(f"⚠️ '{item['기사제목']}' 기사 생성 실패. 건너뜀.")
                continue
            print(f"✅ 기사 생성 완료: {article.get('기사제목', '[기사제목 없음]')}")
            print(f"   - 기사 본문: {article.get('본문', '[본문 없음]')}")
            print(f"   - 작성일자: {article.get('작성일자', '[작성일자 없음]')}")
            print(f"   - 신문사: {article.get('신문사', '[신문사 없음]')}")
            print(f"   - URL: {article.get('URL', '[URL 없음]')}")
            print("-" * 50)
            articles.append(article)
            with open(output_file, 'w', encoding='utf-8') as outfile:
                json.dump(articles, outfile, ensure_ascii=False, indent=4)
        return articles

    def regenerate_missing_articles(self, original_file, generated_file, output_file=None):
        """
        원본 기사 파일과 이미 생성된 기사 파일을 비교하여 누락된 기사만 다시 생성.
        output_file이 지정되지 않으면 generated_file에 덮어쓴다.
        """
        if output_file is None:
            output_file = generated_file

        # 1. 원본 기사 목록
        with open(original_file, 'r', encoding='utf-8') as f:
            original_data = json.load(f)

        # 2. 이미 생성된 기사 목록
        try:
            with open(generated_file, 'r', encoding='utf-8') as f:
                generated_data = json.load(f)
        except FileNotFoundError:
            print("📁 생성된 기사 파일이 없어 새로 시작합니다.")
            generated_data = []

        # 3. 생성된 기사들의 URL 추출
        existing_urls = set(item.get("URL") for item in generated_data if "URL" in item)

        # 4. 누락된 기사 추출
        missing_articles = [item for item in original_data if item.get("URL") not in existing_urls]

        print(f"📌 총 원본 기사 수: {len(original_data)}")
        print(f"✅ 생성 완료된 기사 수: {len(generated_data)}")
        print(f"❗ 생성되지 않은 기사 수: {len(missing_articles)}")

        for item in missing_articles:
            prompt = f"{item['신문사']}의 {item['기사제목']}, {item['URL']}에 대한 기사를 작성하십시오."
            article = self.generate_article(prompt)
            if article is None:
                print(f"⚠️ '{item['기사제목']}' 기사 생성 실패. 건너뜀.")
                continue

            required_keys = ['기사제목', '본문', '작성일자', '신문사', 'URL']
            missing = [k for k in required_keys if k not in article]
            if missing:
                print(f"⚠️ 필수 키 누락으로 건너뜀: {missing} | 제목: {article.get('기사제목', '[제목 없음]')}")
                continue

            print(f"✅ 기사 생성 완료: {article['기사제목']}")
            generated_data.append(article)

            # 매번 누적 저장
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(generated_data, f, ensure_ascii=False, indent=4)

        print(f"\n✅ 누락 기사 재생성 완료! 최종 저장: {output_file}")