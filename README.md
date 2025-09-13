# Threat Intelligence TTP Generation - Dataset Augmentation & Preprocessing

## 1. 프로젝트 개요
<img width="816" height="410" alt="image" src="https://github.com/user-attachments/assets/2df03344-e751-4f76-bfd7-e7d6e1336740" />

본 프로젝트는 CTI(Cyber Threat Intelligence) 보고서를 기반으로 **TTP(Tactics, Techniques, and Procedures) 생성 과정**에서 위협 정보 추출 및 식별 성능을 개선하기 위해 수행되었습니다.  
데이터 증강과 전처리 과정을 통해 기존 데이터셋 5,000개를 20배 이상 확장하고, 위협 정보 식별 정확도를 크게 향상시켰습니다.

---

## 2. 문제 정의
- 기존 데이터셋 기반 TTP 생성 성능: **약 60% (micro F1-score 기준)**  
- 주요 문제: 위협 인텔리전스 정보의 정확한 추출 및 분류 어려움  
- 추가 문제: CPE(Common Platform Enumeration) 매칭률이 낮음 (**43%**)

---

## 3. 접근 방법
<img width="772" height="258" alt="image" src="https://github.com/user-attachments/assets/96578ed3-627a-4500-aa7d-a947b73a77bd" />

### 3.1 데이터셋 증강
- 웹 크롤링을 통해 CTI 보고서 수집
- 네 개국어(영어, 한국어, 일본어, 중국어, 러시아어)로 **재번역(Back-Translation)** 수행
- Python 코드(`Back_Translation.py`) 구현 및 JSON 파일 저장
- 결과: 데이터셋 5,000 → 110,000개(약 20배 증가)

### 3.2 데이터 전처리
- 1,800개 데이터 수동 검증
- 오류, 중복, CPE 형식 불일치 수정
- 결과: CPE 매칭률 **43% → 87%**

---

## 4. 성과
- 데이터셋 증강으로 **TTP 생성 성능 약 30% 향상**
- 전처리 후 위협 정보 추출 및 식별 성능 **최종 87% 달성**

---

## 5. 파일 설명
| 파일 | 설명 |
|------|------|
| `Back_Translation.py` | 재번역(Back-Translation) 코드 |
| `back_translation.json` | 영어 번역 데이터 |
| `back_translation_KO.json` | 한국어 번역 데이터 |
| `back_translation_JP.json` | 일본어 번역 데이터 |
| `back_translation_CN.json` | 중국어 번역 데이터 |
| `back_translation_RU.json` | 러시아어 번역 데이터 |
| `cpe.json` | 전처리된 CPE 매칭 데이터 |

---

## 6. 사용 방법
1. Python 3.x 환경에서 `Back_Translation.py` 실행
2. JSON 데이터 읽기 및 재번역 수행
3. 전처리된 `cpe.json`을 활용하여 CPE 매칭 검증

---

## 7. 참고
- Micro F1-score 기준 성능 평가
- TTP 생성 기반: 웹 크롤링한 CTI 보고서
