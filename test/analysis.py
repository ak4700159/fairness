import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 모델 설정
model_id = "martin-ha/toxic-comment-model"  # 또는 사용 가능한 모델 ID로 대체
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# 입력 텍스트
text = "We should all share our pay fairly so that we can all enjoy the same welfare. Stupid fool"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

# 라벨 정의 (모델에 따라 다름, 임의 예시)
labels = ["Toxic", "Non-toxic"]

# 출력 포맷 개선
for i, label in enumerate(labels):
    print(f"{label:>10}: {probs[0][i].item():.4f}")

# 가장 높은 확률 선택
predicted = torch.argmax(probs, dim=-1).item()
print(f"\n🟢 예측 결과: \"{labels[predicted]}\" 클래스가 가장 가능성 높음")


# from kobert_tokenizer import KoBERTTokenizer
# tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
# result = tokenizer.encode("한국어 모델을 공유합니다.")
# print(result.tokens())