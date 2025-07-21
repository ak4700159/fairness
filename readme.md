# Fair Search Algorithm develop 
사용자가 여러 방면의 의견이 나올 수 있는 키워드 기반 검색할 때, 한 쪽으로 치우치지 않고 여러 가지 관점을 동시에 볼 수 있도록 공평하게 글을 검색하는 알고리즘 


## LLM 라우팅
> **다방면으로 해석 가능한 검색 유형인지 확인**하고 다방면으로 검색 가능하다면 이유와 함께 view points를 추출한다.
> 
> **다면적으로 해석 가능한 입력**이란 사용자가 입력한 검색 키워드가 명확한 객관적 사실로만 설명되지 않고, 사용자의 성향이나 가치관, 입장에 따라 다양한 관점(view points)에서 다르게 해석될 수 있는 경우를 의미, 기본적으로 “정치” “종교” “지역(민족)” “성별” “세대” + a(LLM 판단)의 측면에서 공평하게 검색을 진행한다.
> 결론적으로 RAG에 직접 검색되기 전 view points를 추출하고 추출한 view points 기반으로 검색을 해 정확도를 높인다. 

<br>
<br>
<br>

### 데이터 수집                  

<img width="827" height="459" alt="Image" src="https://github.com/user-attachments/assets/a83ce7b4-07a1-4bb0-a030-44f87e03bc70" />

### RAG Architecture

<img width="1472" height="410" alt="Image" src="https://github.com/user-attachments/assets/031361e9-a4a6-4fd3-8417-fd89f0426fdb" />

---- 
# 목표



Python 3.10.11


