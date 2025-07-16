
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    with open(r"data\dumy\result.json", 'r', encoding='utf-8') as f:
        articles = json.load(f)
    # 미디어별 점수 정리
    # 점수와 미디어 정보 분리
    scores = []
    medias = []
    for item in articles:
        try:
            scores.append(float(item["score"]))
            medias.append(item["media"])
        except:
            continue

    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False
    # 시각화
    plt.figure(figsize=(10, 6))
    sns.stripplot(x=scores, y=medias, jitter=True, size=5, orient='h', palette='Set2')
    plt.title("\"민생정책\" 키워드에 대한 기사 감정 분포 (-1 ~ 1)")
    plt.xlabel("키워드에 대한 기사 점수(score)")
    # plt.ylabel("밀도(Density)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
