from collections import defaultdict
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

def visaulize(file_path, keyword):
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # 사이트별 점수와 우선도 저장
    site_data = defaultdict(lambda: {"scores": [], "priorities": []})

    for item in articles:
        try:
            score = float(item["score"])
            site = item["site"]
            page = int(item.get("page", 1))
            index = int(item.get("index", 1))

            priority = 1 / (page + index / 10.0)

            site_data[site]["scores"].append(score)
            site_data[site]["priorities"].append(priority)
        except:
            continue

    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    # 사이트 리스트
    site_list = sorted(site_data.keys())
    site_to_y = {site: i for i, site in enumerate(site_list)}

    # 컬러맵 생성 (사이트 수에 맞게 컬러 분배)
    cmap = cm.get_cmap('Set2', len(site_list))

    plt.figure(figsize=(10, 6))

    for idx, (site, data) in enumerate(site_data.items()):
        scores = np.array(data["scores"])
        priorities = np.array(data["priorities"])

        # 점 크기 정규화 (5~80 범위로 크게 조정)
        sizes = np.log1p(priorities * 200)
        sizes = 70 * (sizes - sizes.min()) / (sizes.max() - sizes.min() + 1e-6) + 10  # → 10~80

        y = np.full_like(scores, site_to_y[site], dtype=float)
        jitter = np.random.normal(loc=0, scale=0.1, size=len(y))
        y_jittered = y + jitter

        plt.scatter(scores, y_jittered, s=sizes, color=cmap(idx), alpha=0.6,
                    edgecolors='gray', linewidths=0.5, label=site)

    plt.yticks(ticks=range(len(site_list)), labels=site_list)
    plt.xlabel("기사 점수 (score)")
    plt.title(f'"{keyword}" 키워드에 대한 사이트별 기사 감정 분포')
    plt.grid(True)
    plt.legend(title="사이트", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visaulize(file_path=r"C:\Users\cn120\바탕 화면\rag\fairness\data\dumy\[07 21-17 13]이재명_result.json", keyword="이재명")