from datetime import datetime, timedelta, timezone

class Article:
    def __init__(self, **kwargs):
        # 기사 링크
        self.url = kwargs.get("url", "AI생성")
        # 기사 제목 
        self.title = kwargs.get("title", "제목없음")
        # 기사 내용
        self.content = kwargs.get("content", "본문없음")
        # 기사 매체
        self.media = kwargs.get("media", "알 수 없음")
        # 기사 발행 시점
        self.datetime = kwargs.get("datetime", "")
        if self.datetime == "":
            KST = timezone(timedelta(hours=9))
            kst_now = datetime.now(KST)
            self.datetime = kst_now.strftime("%Y-%m-%d %H:%M:%S")

        # 검색 시점 페이지 내 리스트 인덱스(1번부터 시작)
        self.index = kwargs.get("index", -1)
        # 검색 시점 페이지 인덱스(1번부터 시작)
        self.page = kwargs.get("page", -1)
        # 검색 키워드
        self.keyword = kwargs.get("keyword", "검색 키워드 없음")
        # 검색 시점
        self.search_datetime = kwargs.get("search_datetime", kst_now.strftime("%Y-%m-%d %H:%M:%S"))
        # 검색 사이트
        self.site = kwargs.get("site", "알 수 없음")

    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "media": self.media,
            "site" : self.site,
            "datetime": self.datetime,
            "search_datetime" : self.search_datetime,
            "index": self.index,
            "page": self.page,
            "keyword": self.keyword,
        }