"""Units III and IV: textbook concepts, runnable reworked examples and visual summaries."""
from content import units,examples,lesson,ex,q
from slots import pick_slots
units.update({3:[],4:[]})
def topic(u,id,title,pages,lead,paragraphs,steps,headers,rows,ids=(),tasks=(),**slots):
 lesson(u,id,title,pages,lead,paragraphs,ids,tasks,**pick_slots(slots))
 units[u][-1]['visual']=(title+' · 한눈에 보기',steps,headers,rows)
def example(id,title,src,packages='',mode='web',files=None,checks='',note='',**slots):
 data={'main.py':src,**(files or {})}
 if packages:data['requirements.txt']=packages.replace(' ',',') .replace(',','\n')+'\n'
 ex(id,title,data,mode=mode,checks=checks,note=note,**pick_slots(slots))

# III. Concepts: explicitly separate data, learned parameters and chosen settings.
topic(3,'ml-overview','머신러닝이란? — AI·머신러닝·딥러닝의 관계','63–67','규칙을 직접 쓰는 것과 데이터에서 규칙을 배우는 것은 어떻게 다를까요?',[
'인공지능은 지능적인 문제 해결 기술의 넓은 범위입니다. 머신러닝은 데이터에서 패턴을 학습하는 접근이며, 딥러닝은 여러 층의 신경망을 사용하는 머신러닝의 한 종류입니다. 모든 AI가 머신러닝인 것은 아닙니다.',
'초기의 규칙 중심 연구는 지식 입력과 계산 자원의 한계를 겪었습니다. 이후 데이터·계산 장치·학습 알고리즘의 발전이 함께 영향을 주었습니다. 1956년 다트머스 워크숍, 1997년 딥 블루의 체스 승리, 2012년 ImageNet의 딥러닝 성과는 서로 다른 접근의 발전 사례입니다. 딥 블루를 현대 딥러닝 모델과 같은 것으로 보지 마세요.'],['인공지능｜가장 넓은 범위','머신러닝｜데이터로 학습','딥러닝｜여러 층의 신경망'],['접근','규칙의 출처','예'],[['규칙 기반','사람이 조건 작성','비밀번호 길이 검사'],['머신러닝','데이터와 학습 알고리즘','스팸 분류'],['딥러닝','다층 신경망의 학습','이미지 특징 학습']],tasks=['주변의 AI 서비스 하나에서 입력과 출력을 찾아 설명하세요.'])
topic(3,'ml-use','머신러닝의 필요성과 활용','68–70','정확한 규칙을 쓰기 어려운 문제를 찾아보세요.',[
'추천, 이미지 분류, 음성 처리처럼 복잡한 패턴이 있는 문제에서 머신러닝을 활용합니다. 규칙이 명확한 사칙연산이나 간단한 유효성 검사에는 일반 프로그램이 더 간단할 수 있습니다.',
'학습 데이터가 현실을 충분히 대표하지 않으면 특정 조건에서 오류가 늘어납니다. 예측을 사실로 단정하지 말고, 데이터의 범위·오류 비용·사람의 확인 절차를 함께 설명하세요.'],['문제 찾기','입력 데이터 정하기','예측할 출력 정하기','오류가 미칠 영향 점검'],['서비스','입력','예측'],[['추천','이용 기록·항목 특성','선호 가능성'],['제조 검사','제품 이미지','정상/결함'],['대출량 예상','과거 대출·요일','예상 권수']],tasks=['학교 도서 대출량을 예측한다면 어떤 데이터를 모을지 표로 적으세요.'])
topic(3,'ml-process','머신러닝 문제 해결 과정','71–75','모델을 만들기 전에 성공 기준을 정하세요.',[
'문제 정의 → 수집·탐색 → 전처리 → 모델 선택 → 학습·평가 → 해석·응용으로 진행합니다. 실제 프로젝트에서는 결과를 보고 앞 단계로 돌아가 수정하기도 합니다.',
'평가용 데이터는 먼저 분리해 둡니다. 평균·스케일·범주 목록처럼 데이터에서 배우는 전처리 값도 훈련 부분에서만 구합니다. 모델 후보는 검증 데이터나 교차 검증으로 비교하고, 최종 테스트는 선택을 마친 뒤 사용합니다.'],['문제·성공 기준','수집·탐색','훈련/테스트 분할','전처리·학습·검증','최종 평가·해석'],['분할','역할','금지할 일'],[['훈련','전처리 값·모델 학습','정답을 입력 특성에 포함'],['검증','모델·설정 선택','최종 테스트로 반복 선택'],['테스트','선택 완료 후 최종 확인','fit / fit_transform 호출']],tasks=['도서 대출 예측의 성공 기준을 평균 오차로 표현해 보세요.'])
topic(3,'ml-terms','머신러닝의 주요 용어','76–78','표의 어느 열을 X로, 어느 열을 y로 사용할까요?',[
'데이터 세트의 한 행은 보통 한 관측입니다. X는 예측 시점에 알 수 있는 특성의 표이며 y는 예측할 정답입니다. 샘플 수와 특성 수를 확인하고 같은 행의 X와 y가 대응하는지 검사합니다.',
'모델은 학습한 예측 규칙입니다. 가중치 같은 파라미터는 학습 과정에서 정해지고, k-NN의 k 같은 하이퍼파라미터는 학습 전에 설정합니다. 훈련 성능만 좋고 검증 성능이 낮으면 과대 적합, 둘 다 낮으면 과소 적합을 의심합니다.'],['행｜샘플 1개','입력 열 X｜특성 여러 개','정답 열 y｜레이블','fit → predict｜학습 후 예측'],['기호','도서 예','형태'],[['X','요일·최근 대출 수','(샘플 수, 특성 수)'],['y','다음 날 대출 수','(샘플 수,)'],['하이퍼파라미터','트리의 최대 깊이','학습 전에 선택']],tasks=['미래 대출 수를 특성에 넣으면 왜 잘못된 평가가 되는지 설명하세요.'])
topic(3,'ml-methods','머신러닝 학습 방법의 종류','79–82','정답을 배우나요, 구조를 찾나요, 행동의 보상을 배우나요?',[
'지도 학습은 입력과 정답의 관계를 학습합니다. 범주를 예측하면 분류, 연속적인 수치를 예측하면 회귀입니다. 비지도 학습은 정답 없이 군집이나 낮은 차원의 구조를 찾습니다.',
'강화 학습에서는 에이전트가 상태를 보고 행동하며 환경에서 보상을 받습니다. 정책은 행동 선택 전략이고 장기 누적 보상을 높이는 방향으로 배웁니다. Q-learning은 여러 강화 학습 알고리즘 중 하나입니다.'],['정답 있음｜지도 학습','정답 없음｜비지도 학습','상태·행동·보상｜강화 학습'],['유형','목표','예'],[['분류','범주 예측','스팸 여부'],['회귀','수치 예측','내일 기온'],['군집','유사한 데이터 묶기','고객 그룹'],['강화','행동 전략 학습','미로에서 탈출']],tasks=['미로 탈출에 보상을 설계하고 반복 제자리 움직임을 막는 방법을 설명하세요.'])
example('ml-sklearn-exam','교과서 86쪽 sklearn_exam.py — 공부 시간으로 합격 예측','''from sklearn.tree import DecisionTreeClassifier
import numpy as np

# 학습 데이터
X_study = np.array([[1], [3]])   # 공부 시간
y_pass = np.array([0, 1])        # 합격 여부

# 모델 만들고 학습
model = DecisionTreeClassifier()
model.fit(X_study, y_pass)

# 새로운 공부 시간으로 예측
prediction = model.predict(np.array([[2]]))
print(f"공부 시간 2시간일 때 예측: {prediction[0]}")
''','scikit-learn numpy',checks='assert prediction[0] == 0')
example('ml-numpy-exam','교과서 87쪽 numpy_exam.py — 배열 계산과 이어 붙이기','''import numpy as np
my_array = np.array([10, 20, 30])
print("NumPy 배열:", my_array)

result = my_array + 5
print("5를 더한 결과:", result)

# 여러 개의 배열 합치기
array_part1 = np.array([1, 2])
array_part2 = np.array([3, 4])
combined_array = np.concatenate((array_part1, array_part2))
print("\\n합쳐진 배열:", combined_array)
''','numpy',checks='assert list(combined_array) == [1,2,3,4]')
example('ml-pandas-exam','교과서 87~88쪽 pandas_exam.py — DataFrame 만들고 칼럼 선택','''import pandas as pd
data = {'이름': ['철수', '영희'], '점수': [85, 92]}
my_df = pd.DataFrame(data)
print("학생 점수표:")
print(my_df)
print("\\n'점수' 칼럼:\\n", my_df['점수'])
''','pandas',checks='assert list(my_df["점수"]) == [85,92]')
example('ml-matplot-exam','교과서 88~89쪽 matplot_exam.py — Seaborn 막대그래프','''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data_for_plot = pd.DataFrame({'fruits': ['apple', 'banana', 'apple']})

# Seaborn으로 막대 그래프 그리기(각 과일 개수)
plt.figure(figsize=(8, 6))
sns.countplot(x='fruits', data=data_for_plot)
plt.savefig("matplot_exam.png")
''','matplotlib seaborn pandas',checks='assert data_for_plot.shape == (3,1)',note='교과서는 plt.show()로 화면에 띄우지만, 브라우저 실습에서는 plt.savefig()로 저장한 그림을 결과 아래에 보여줍니다(매트플롯립 백엔드도 Agg로 지정) — 이 두 줄만 교과서 코드에 추가했습니다.')
topic(3,'ml-libraries','파이썬 머신러닝 라이브러리 소개','86–89','배열·표·모델·그래프 도구를 연결해 보세요.',[
'NumPy는 다차원 배열과 벡터 연산, pandas는 Series·DataFrame과 표 탐색, scikit-learn은 전처리·학습·평가 도구를 제공합니다. Matplotlib은 그래프 구성, Seaborn은 표 데이터의 통계 시각화를 돕습니다.',
'웹에서는 NumPy·pandas·그래프와 작은 원리 실습을 실행합니다. scikit-learn 전체 파이프라인은 PC에서 실행합니다. 필요한 웹 패키지는 처음에 내려받습니다. 실행한 Python이 만든 PNG 그래프는 결과 아래에 표시됩니다. PC에서는 예제 폴더에서 requirements.txt를 설치합니다.'],['NumPy｜배열','pandas｜표 정리','scikit-learn｜학습·평가','Matplotlib / Seaborn｜시각화'],['확인','코드','의미'],[['앞부분','df.head()','표의 실제 값'],['구조','df.info()','자료형·결측 개수'],['통계','df.describe()','수치 분포'],['배열 크기','array.shape','축별 길이']],['ml-sklearn-exam','ml-numpy-exam','ml-pandas-exam','ml-matplot-exam'],['과일 종류와 개수를 바꾸고 그래프가 바뀌는지 확인하세요.'])
example('ml-read-data','교과서 90~91쪽 read_data.py — CSV·Excel 불러오기','''import pandas as pd

# 교과서는 텍스트 편집기·엑셀로 만든 data.csv/data.xlsx를 코랩에 업로드해서 읽습니다.
# 웹 실습에서는 같은 내용을 코드로 먼저 만든 뒤 그대로 읽어 들입니다.
with open('data.csv', 'w', encoding='utf-8') as f:
    f.write('Name, Score\\nAlice, 90\\nBob, 85\\n')
pd.DataFrame({'Name': ['Alice', 'Bob'], 'Score': [90, 85]}).to_excel('data.xlsx', index=False)

df_csv = pd.read_csv('data.csv')
print("CSV에서 불러온 데이터:")
print(df_csv)

df_excel = pd.read_excel('data.xlsx')
print("\\nExcel에서 불러온 데이터:")
print(df_excel)
''','pandas openpyxl',mode='pc',checks='assert list(df_csv.columns)[0]=="Name"',note='교과서는 텍스트 편집기·엑셀로 미리 만든 data.csv·data.xlsx를 코랩에 업로드해 읽습니다. 이 예제는 같은 내용을 코드 앞 두 줄에서 직접 만든 뒤 그대로 읽어 들입니다 — 그 두 줄만 교과서 코드에 추가했습니다. Excel 저장에 openpyxl이 필요해 PC/코랩에서 실행하세요.')
example('ml-head-describe-info','교과서 91~93쪽 head_describe_info.py — head·describe·info','''import pandas as pd
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
        'Score': [90, 85, 78, 92, 65, 70],
        'City': ['Seoul', 'Busan', 'Seoul', 'Jeju', 'Busan', 'Seoul']}

df = pd.DataFrame(data)
print("--- 데이터프레임 상위 3행 (df.head(3)) ---")
print(df.head(3))

print("\\n--- 숫자 데이터 통계 요약 (df.describe()) ---")
print(df.describe())

print("\\n--- 데이터프레임 요약 정보 (df.info()) ---")
df.info()
''','pandas',checks='assert df.shape == (6,3)',note='교과서 표기(mean 79.00, std 9.92)는 같은 코드의 실제 실행값(mean 80.00, std 10.94)과 다릅니다 — 이 페이지는 실제 실행값을 싣습니다. dtype 표시도 pandas 버전에 따라 object/str로 다를 수 있습니다.')
example('ml-missing-values','교과서 93~96쪽 missing_values.py — 결측치 확인·제거·채우기','''import pandas as pd
import numpy as np

data_missing = {'Name': ['Alice', 'Bob', np.nan],
                'Score': [90, np.nan, 70],
                'City': ['Seoul', 'Busan', 'Seoul']}

df_missing = pd.DataFrame(data_missing)
print("결측치 확인 (각 열의 결측치 개수):")
print(df_missing.isnull().sum())

df_dropna_row = df_missing.dropna(axis=0)
print("\\n결측치가 있는 행 제거 후 데이터:")
print(df_dropna_row)

# 결측치를 0으로 채우기
df_fill_zero = df_missing.fillna(0)
print("\\n결측치를 0으로 채운 후 데이터:")
print(df_fill_zero)

# Name 칼럼의 결측치를 'Unknown'으로 채우기
df_fill_unknown_name = df_missing.fillna({'Name': 'Unknown'})
print("\\nName 결측치를 'Unknown'으로 채운 후 데이터:")
print(df_fill_unknown_name)

# 'Score' 열의 평균값으로 결측치 채우기
score_mean = df_missing['Score'].mean()
df_fill_mean = df_missing.fillna({'Score': score_mean})
print(f"\\n'Score' 결측치를 평균({score_mean:.2f})으로 채운 후 데이터:")
print(df_fill_mean)

# 'Score' 열의 중앙값으로 결측치 채우기
score_median = df_missing['Score'].median()
df_fill_median = df_missing.fillna({'Score': score_median})
print(f"\\n'Score' 결측치를 중앙값({score_median:.2f})으로 채운 후 데이터:")
print(df_fill_median)
''','pandas numpy',checks='assert df_fill_zero.isna().sum().sum() == 0')
example('ml-normalization','교과서 96~98쪽 normalization.py — 정규화(Min-Max)','''import pandas as pd
from sklearn.preprocessing import MinMaxScaler

data_norm = {'Feature1': [10, 20, 30, 40],
             'Feature2': [100, 200, 300, 400]}
df_norm = pd.DataFrame(data_norm)
print("--- 원본 데이터 (정규화 전) ---")
print(df_norm)

scaler_minmax = MinMaxScaler()
df_normalized = pd.DataFrame(scaler_minmax.fit_transform(df_norm), columns=df_norm.columns)
print("\\n--- 정규화된 데이터 ---")
print(df_normalized)
''','pandas scikit-learn',checks='assert round(df_normalized["Feature1"].max(),3) == 1.0')
example('ml-standardization','교과서 98~99쪽 standardization.py — 표준화(Standardization)','''import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np                                 # 통계량 확인을 위해 사용

data = {
    'Feature1': [10, 20, 30, 40, 50],
    'Feature2': [100, 200, 50, 150, 250],
    'Feature3': [1, 2, 3, 100, 4]                 # 이상치인 큰 값을 포함
}
df = pd.DataFrame(data)

scaler_standard = StandardScaler()
df_standardized = scaler_standard.fit_transform(df) # 데이터에 표준화 적용
df_standardized = pd.DataFrame(df_standardized, columns=df.columns)
print(df_standardized)

print("각 특성의 평균 :", scaler_standard.mean_)
print("각 특성의 표준편차 :", np.sqrt(scaler_standard.var_))
''','pandas scikit-learn numpy',checks='assert round(df_standardized["Feature1"].mean(),6) == 0.0')
example('ml-one-hot-encoding','교과서 100~101쪽 one_hot_encoding.py — 원-핫 인코딩','''import pandas as pd

data_onehot = {'도시': ['서울', '부산', '서울', '제주', '부산'],
               '직업': ['학생', '직장인', '직장인', '학생', '학생']}
df_onehot = pd.DataFrame(data_onehot)
print(" - 원본 데이터")
print(df_onehot)

df_encoded = pd.get_dummies(df_onehot, columns=['도시', '직업'], drop_first=True, dtype=int)
print("\\n--- 2. 원-핫 인코딩된 데이터 ---")
print(df_encoded)
''','pandas',checks='assert "도시_부산" not in df_encoded.columns')
example('ml-train-test-split','교과서 101~102쪽 train_test_split.py — 훈련/테스트 분할','''import pandas as pd
from sklearn.model_selection import train_test_split
data_split = {'공부 시간': [2, 3, 5, 4, 6],
              '수면 시간': [7, 6, 8, 7, 7],
              '시험 점수': [60, 70, 85, 75, 90]}
df = pd.DataFrame(data_split)
X = df[['공부 시간', '수면 시간']]
y = df['시험 점수']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("\\n--- 3. 분할된 데이터의 형태 확인 ---")
print(f" - 훈련 특징 데이터 (X_train) 형태: {X_train.shape}")
print(f" - 테스트 특징 데이터 (X_test) 형태: {X_test.shape}")
print(f" - 훈련 목표 변수 (y_train) 형태: {y_train.shape}")
print(f" - 테스트 목표 변수 (y_test) 형태: {y_test.shape}")
''','pandas scikit-learn',checks='assert X_train.shape == (3,2) and X_test.shape == (2,2)')
topic(3,'ml-preprocess','데이터 준비와 전처리','90–102','값을 바꾼 이유와 기준을 남겨 보세요.',[
'CSV는 read_csv, Excel은 read_excel로 읽습니다. 결측치는 isna로 확인한 뒤 dropna로 제거하거나 fillna·SimpleImputer로 채울 수 있습니다. 이상치는 입력 오류인지 드문 정상 관측인지 먼저 확인합니다. 임의 삭제는 데이터의 의미를 바꿀 수 있습니다.',
'MinMaxScaler는 훈련 범위를 기준으로 값을 조정하며 새로운 값은 0~1 범위를 벗어날 수 있습니다. StandardScaler는 훈련 평균과 표준편차로 변환하지만 정규분포를 만들어 주지는 않습니다. 범주형 값에는 get_dummies 또는 OneHotEncoder를 사용하며 새 범주 처리 기준도 정합니다.'],['불러오기·자료형 확인','분할 후 훈련 부분 탐색','결측·이상치 처리 기준','수치 스케일·범주 인코딩','테스트에는 transform'],['처리','배우는 기준','확인'],[['결측 채우기','훈련 중앙값 등','누락 의미 보존'],['정규화','훈련 최소·최대','새 값은 범위 밖 가능'],['표준화','훈련 평균·표준편차','분포 모양 보장 안 함'],['원-핫','훈련 범주 목록','알 수 없는 범주 대응']],['ml-read-data','ml-head-describe-info','ml-missing-values','ml-normalization','ml-standardization','ml-one-hot-encoding','ml-train-test-split'],['1000점이 실제 값인지 입력 실수인지 확인할 질문을 적으세요.'])
example('ml-knn-exam','교과서 104~105쪽 knn.py — K-최근접 이웃으로 붓꽃 분류','''import pandas as pd
from sklearn.datasets import load_iris                # 붓꽃 데이터 세트
from sklearn.model_selection import train_test_split  # 데이터 분할
from sklearn.neighbors import KNeighborsClassifier    # K-최근접 이웃 알고리즘 모델

iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target)
print("원본 데이터 미리보기 (특징 X)\\n", X.head())
print("원본 데이터 미리보기(목표 변수 y)\\n", y.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                    random_state=42, stratify=y)
print(f" - 훈련 데이터 형태: {X_train.shape}, {y_train.shape}")
print(f" - 테스트 데이터 형태: {X_test.shape}, {y_test.shape}")

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)

y_pred = knn_model.predict(X_test)
print(y_pred[:5])                 # 예측 결과 중 앞의 5개만 출력
''','scikit-learn pandas',checks='assert list(y_pred[:5]) == [2,1,2,1,2]')
topic(3,'ml-classification','주요 알고리즘 활용 · 분류','103–105','이름에 회귀가 들어 있어도 범주를 예측하는 모델이 있어요.',[
'k-NN은 가까운 이웃들의 정답을 참고합니다. 로지스틱 회귀는 분류에 사용하는 모델이고, 결정 트리는 조건으로 데이터를 나누며, SVM은 범주 사이의 경계를 학습합니다.',
'붓꽃 예제에서 X는 꽃받침·꽃잎의 측정값이고 y는 품종입니다. stratify=y는 분할 시 클래스 비율을 고려합니다. k-NN·SVM 등은 거리나 스케일의 영향을 받으므로 전처리를 파이프라인 안에서 학습합니다.'],['붓꽃 X,y','분할','스케일 + 분류기 fit','새 X로 predict','정답과 비교'],['알고리즘','핵심','조절값 예'],[['k-NN','가까운 이웃','n_neighbors'],['로지스틱','클래스 확률','C'],['결정 트리','조건 분기','max_depth'],['SVM','분리 경계','C / kernel']],['ml-knn-exam'],['k를 3과 7로 바꾸고 같은 분할에서 결과를 비교하세요.'])
example('ml-linear-regression','교과서 106~108쪽 linear_regression.py — 당뇨병 데이터로 선형 회귀','''import pandas as pd
from sklearn.datasets import load_diabetes            # 예제 데이터 세트(당뇨병 데이터)
from sklearn.model_selection import train_test_split  # 데이터 분할
from sklearn.linear_model import LinearRegression      # 선형 회귀 모델

diabetes = load_diabetes()
X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)    # 특징
y = pd.Series(diabetes.target)              # 질병 진행도: 연속적인 숫자 값
print(" - 특징(X) 데이터 미리보기 (상위 5개) \\n", X.head())
print("\\n - 목표 변수(y) 미리보기 (상위 3개):\\n", y.head(3))
print(f" - 원본 데이터 형태: {X.shape}, {y.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f" - 훈련 데이터 형태: {X_train.shape}, {y_train.shape}")
print(f" - 테스트 데이터 형태: {X_test.shape}, {y_test.shape}")

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)                # 모델 학습
print(f" - 모델의 계수: {linear_model.coef_}")
print(f" - 모델의 절편: {linear_model.intercept_:.4f}")

y_pred = linear_model.predict(X_test)
print(" - 테스트 데이터에 대한 예측 결과 (일부):")
print(y_pred[:5])
''','scikit-learn pandas',checks='assert round(linear_model.intercept_,4) == 151.0082',note='X.head() 출력은 pandas가 화면 폭에 맞춰 가운데 열을 생략(...)해 보여줄 수 있습니다 — 교과서는 지면 폭이 넓어 10개 열을 모두 보여줍니다. 계수·절편·예측값은 동일합니다.')
example('ml-regression-metrics','교과서 122~123쪽 regression_metrics.py — 캘리포니아 주택 가격 MSE·MAE·R²','''import pandas as pd
import numpy as np              # 수치 계산을 위한 numpy 라이브러리
from sklearn.datasets import fetch_california_housing    # 회귀 예제 데이터 세트
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression        # 선형 회귀 모델
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
                                         # 회귀 평가 지표 함수들

housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = pd.Series(housing.target)   # 주택 가격 (연속형)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"\\n - 평균 제곱 오차 (MSE): {mse:.4f}")
print(f" - 평균 절대 오차 (MAE): {mae:.4f}")
print(f" - 결정계수 (R-squared): {r2:.4f}")
''','scikit-learn pandas numpy',mode='pc',checks='assert round(r2,4) == 0.5958',note='첫 실행에 캘리포니아 주택 데이터 다운로드가 필요해 PC/코랩에서 실행하세요.')
topic(3,'ml-regression','주요 알고리즘 활용 · 회귀 / 회귀와 수치 오차','106–107, 121–123','예측 숫자는 정답에서 얼마나 떨어져 있나요?',[
'회귀는 연속적인 목표값을 예측합니다. 선형 회귀는 특성들의 가중합과 절편으로 값을 예측합니다. 예측한 값과 실제 값의 차이를 잔차라고 부릅니다.',
'MAE는 절대 오차 평균, MSE는 제곱 오차 평균입니다. MSE는 큰 오차에 더 큰 벌점을 줍니다. R²는 평균 예측 기준과 비교한 값으로 음수가 될 수 있습니다. 한 지표의 숫자만 보지 말고 목표값의 단위와 오류 사례도 확인하세요.'],['입력 특성','가중합 + 절편','예측 숫자','정답과 오차 계산'],['지표','작을수록?','의미'],[['MAE','좋음','원래 목표값 단위'],['MSE','좋음','큰 오차를 강하게 반영'],['R²','클수록 좋음','0은 평균 기준, 음수 가능']],['ml-linear-regression','ml-regression-metrics'],['기울기 실험에서 MSE가 가장 작은 위치를 찾으세요.'])
example('ml-clustering','교과서 108~110쪽 clustering.py — K-평균으로 4개 군집 찾기','''import pandas as pd
from sklearn.datasets import make_blobs         # 가상 데이터 생성
from sklearn.cluster import KMeans              # K-평균 군집화 모델
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                 # 시각화를 위한 라이브러리
import numpy as np                              # 수치 연산을 위한 라이브러리

X, y_true = make_blobs(n_samples=300, n_features=2, centers=4, cluster_std=0.60,
                        random_state=42)
print(" - 생성된 데이터 형태 (X):", X.shape)
print(" - 생성된 데이터 미리보기 (상위 3개):\\n", pd.DataFrame(X, columns=['Feature_1', 'Feature_2']).head(3))

kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, random_state=42,
                n_init=10)
kmeans.fit(X)
cluster_labels = kmeans.labels_
print(f" - 각 데이터 포인트의 할당된 군집 레이블 (일부): {cluster_labels[:10]}")

centroids = kmeans.cluster_centers_
print(f" - 각 군집의 중심점:\\n {centroids}")
print(f" - 군집 내 응집도: {kmeans.inertia_:.2f}")

plt.figure(figsize=(10, 7))
scatter = plt.scatter(X[:, 0], X[:, 1], c=cluster_labels, cmap='viridis', s=50, alpha=0.8)
plt.scatter(centroids[:, 0], centroids[:, 1], s=200, marker='X', c='red',
            edgecolor='black', label='Centroids')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.savefig("clustering.png")
''','scikit-learn matplotlib pandas numpy',checks='assert list(cluster_labels[:10]) == [3,3,0,1,3,1,2,1,0,2]')
topic(3,'ml-cluster','주요 알고리즘 활용 · 군집화','108–111','정답 이름 없이 비슷한 점들을 묶을 수 있을까요?',[
'K-평균은 정한 개수 K의 중심을 이용해 가까운 샘플들을 묶고 중심을 갱신합니다. labels_의 번호는 정답 클래스나 순위가 아니며 실행 조건에 따라 번호가 달라질 수 있습니다.',
'데이터의 스케일, K, 초기 중심이 결과에 영향을 줍니다. n_init은 여러 초기화 시도를 제어합니다. 점들의 분포를 보고 군집이 의미 있는지 해석하며, 항상 원형 군집이 존재한다고 가정하지 마세요.'],['K개 중심 초기화','가장 가까운 중심에 배정','그룹 평균으로 중심 갱신','수렴까지 반복'],['속성','의미'],[['labels_','샘플별 군집 번호'],['cluster_centers_','군집 중심 좌표'],['n_clusters','미리 정하는 그룹 수'],['random_state / n_init','재현 조건 / 초기화 반복']],['ml-clustering'],['K를 2·3·4로 바꾸고 중심 위치와 군집의 의미를 비교하세요.'])
example('ml-performance-metrics','교과서 119쪽 performance_evaluation_metrics.py — 유방암 데이터 혼동행렬·지표','''import pandas as pd
from sklearn.datasets import load_breast_cancer   # 유방암 데이터 세트
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
                                        # 모델 성능 평가 지표 함수들 임포트

cancer = load_breast_cancer()
X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
y = pd.Series(cancer.target)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                    random_state=42) # stratify=y는 생략(간소화 목적)

model = LogisticRegression(max_iter=5000, random_state=42, solver='liblinear')
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

conf_matrix = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("\\n - 혼동 행렬:\\n", conf_matrix)
print(f" - 정확도: {accuracy:.4f} - 정밀도: {precision:.4f}")
print(f" - 재현율: {recall:.4f} - F1 점수: {f1:.4f}")
''','scikit-learn pandas',checks='assert conf_matrix.tolist() == [[59,4],[2,106]]')
topic(3,'ml-metrics','모델 평가와 선택 · 분류 지표','117–120','어떤 종류의 실수가 더 중요한가요?',[
'양성으로 삼는 클래스를 먼저 정합니다. TP는 실제 양성을 양성으로, TN은 실제 음성을 음성으로 맞힌 수입니다. FP는 음성을 양성으로, FN은 양성을 음성으로 틀린 수입니다.',
'정확도는 전체 정답 비율입니다. 정밀도는 양성 예측 중 실제 양성의 비율, 재현율은 실제 양성 중 찾아낸 비율입니다. F1은 정밀도와 재현율의 조화평균입니다. 클래스 불균형이 있으면 정확도만으로 비교하기 어렵습니다.'],['양성 의미 정하기','예측 임계값 선택','TP·FP·FN·TN 세기','목표에 맞는 지표 해석'],['지표','계산','질문'],[['정확도','(TP+TN)/전체','전체에서 얼마나 맞혔나?'],['정밀도','TP/(TP+FP)','양성이라고 한 것 중 맞은 비율?'],['재현율','TP/(TP+FN)','실제 양성 중 찾은 비율?'],['F1','2PR/(P+R)','두 지표의 균형은?']],['ml-performance-metrics'],['임계값을 올릴 때 FP와 FN이 어떻게 달라지는지 관찰하세요.'])
example('ml-train-test-split2','교과서 112~113쪽 train_test_split2.py — 훈련·테스트 R² 비교','''import pandas as pd
from sklearn.model_selection import train_test_split # 데이터 분할 함수
from sklearn.linear_model import LinearRegression      # 예시 모델 (선형 회귀)
from sklearn.datasets import load_diabetes             # 예제 데이터 세트

diabetes = load_diabetes()
X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names) # 특징 데이터
y = pd.Series(diabetes.target)   # 목표 변수 데이터

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(" - 훈련 데이터 형태:", X_train.shape, y_train.shape)
print(" - 테스트 데이터 형태:", X_test.shape, y_test.shape)

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)             # 훈련 데이터로 학습
r2_train = linear_model.score(X_train, y_train) # 훈련 데이터 R²
r2_test = linear_model.score(X_test, y_test)   # 테스트 데이터 R²
print(" - 훈련 데이터 R²:", r2_train)          # 일반적으로 테스트 데이터보다 높음
print(" - 테스트 데이터 R²:", r2_test)          # 훈련 데이터보다 낮음 (일반화 성능)
''','scikit-learn pandas',checks='assert round(r2_train,4) == 0.5244')
example('ml-cross-val-score','교과서 114~115쪽 cross_val_score.py — 5-겹 교차 검증','''import pandas as pd
from sklearn.datasets import load_diabetes            # 예제 데이터 세트 (회귀)
from sklearn.linear_model import LinearRegression     # 예시 모델
from sklearn.model_selection import cross_val_score # 교차 검증 함수
import numpy as np                                    # 평균 계산을 위해

diabetes = load_diabetes()
X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names) # 특징 데이터
y = pd.Series(diabetes.target)                        # 목표 변수 데이터

linear_model = LinearRegression()                     # 선형 회귀 모델 객체 생성
scores = cross_val_score(linear_model, X, y, scoring='r2', cv=5)
print(f"\\n - 각 폴드별 R² 점수: {scores}")
print(f" - 교차 검증 평균 R² 점수: {np.mean(scores):.4f}")
print(f" - 교차 검증 R² 점수의 표준편차: {np.std(scores):.4f}")
''','scikit-learn pandas numpy',checks='assert len(scores) == 5')
example('ml-grid-search-cv','교과서 115~117쪽 grid_search_cv.py — GridSearchCV로 K 값 찾기','''from sklearn.datasets import load_iris               # 간단한 분류 데이터 세트
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV     # 그리드 서치
import numpy as np                                   # 결과 출력을 위해

iris = load_iris()
X, y = iris.data, iris.target

knn = KNeighborsClassifier()
param_grid = {'n_neighbors': [3, 5, 7]} # K 값만 3, 5, 7로 단순화

grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X, y)

print(f"\\n - 최적 하이퍼파라미터: {grid_search.best_params_}")
print(f" - 최고 교차 검증 정확도: {grid_search.best_score_:.4f}")
''','scikit-learn numpy',checks='assert grid_search.best_params_["n_neighbors"] == 7',note='최고 교차 검증 정확도는 scikit-learn 버전에 따라 다를 수 있습니다 — 교과서는 0.9733, 이 실습 환경(scikit-learn 1.9.1)은 0.9800입니다. 최적 K(7)는 동일합니다.')
example('ml-learning-curve','교과서 124~126쪽 learning_curve.py — 학습 곡선으로 과대·과소 적합 진단','''import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt # 그래프 시각화를 위한 라이브러리
from sklearn.datasets import load_breast_cancer       # 유방암 데이터 세트 사용
from sklearn.model_selection import learning_curve # 학습 곡선 생성
from sklearn.linear_model import LogisticRegression

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target
model = LogisticRegression(max_iter=5000, random_state=42, solver='liblinear')

train_sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=5, n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 5)
)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.figure(figsize=(10, 6))                             # 그래프 크기 설정
plt.title("Learning Curve for Logistic Regression") # 그래프 제목
plt.xlabel("Training Examples")                         # x축 라벨
plt.ylabel("Score (Accuracy)")                          # y축 라벨
plt.grid()                                              # 격자선 표시
plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training Score")
plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                  train_scores_mean + train_scores_std, alpha=0.1, color="r")

plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation Score")
plt.fill_between(
    train_sizes, test_scores_mean - test_scores_std,
    test_scores_mean + test_scores_std, alpha=0.1, color="g")

plt.legend(loc="best")                                  # 범례 표시
plt.savefig("learning_curve.png")
''','numpy scikit-learn matplotlib',checks='assert len(train_sizes) == 5',note='교과서는 plt.show()로 화면에 띄우지만, 브라우저 실습에서는 matplotlib 백엔드를 Agg로 지정하고 plt.savefig()로 저장한 그림을 보여줍니다 — 이 부분만 교과서 코드에 추가했습니다.')
topic(3,'ml-selection','모델 평가와 선택 · 교차 검증·튜닝·학습 곡선','112–116, 124–128','한 번 나눈 점수만으로 모델을 선택해도 될까요?',[
'교차 검증은 훈련 자료를 여러 묶음으로 나누어 검증 역할을 번갈아 맡깁니다. GridSearchCV는 설정 후보를 교차 검증으로 비교합니다. 전처리도 각 훈련 묶음에서 다시 학습하도록 Pipeline을 사용합니다.',
'학습 곡선은 훈련 샘플 수에 따른 훈련·검증 성능을 함께 보여 줍니다. 두 곡선의 간격과 수준을 보고 데이터 추가, 모델 복잡도 조절, 규제, 특성 개선 등을 검토합니다. 데이터 스케일 정규화와 모델 규제(regularization)는 다른 개념입니다.'],['최종 테스트 별도 보관','훈련 부분에서 교차 검증','GridSearchCV로 설정 선택','학습 곡선·오류 분석','테스트 한 번 평가'],['관찰','가능한 해석','다음 실험'],[['훈련↑ 검증↓','과대 적합','복잡도 감소·자료 추가'],['훈련↓ 검증↓','과소 적합','특성·모델 개선'],['분할마다 점수 차이','불안정한 추정','평균·편차 함께 보고']],['ml-train-test-split2','ml-cross-val-score','ml-grid-search-cv','ml-learning-curve'],['best_score_와 최종 테스트 점수가 다른 이유를 설명하세요.'])
topic(3,'ml-project','모델 구현·평가 프로젝트와 단원 정리','129–131 + 확장','입력부터 결과 설명까지 재현 가능한 보고서를 만드세요.',[
'문제와 목표값, 데이터 출처, 특성, 분할 조건, 전처리, 모델, 평가 결과를 한 흐름으로 연결하세요. 비교 대상과 난수 조건을 기록하고, 점수가 낮아진 사례를 찾아 개선안을 제안합니다.',
'스팸 분류의 FP와 정밀도, 가격 같은 수치 예측과 회귀, 정답 없는 고객 군집, AI 포함 관계, 과대 적합 방지, DataFrame.describe를 모두 설명할 수 있는지 확인하세요.'],['문제·데이터 카드','분할·전처리 코드','모델 비교·선택','최종 지표·한계','저널·코드 제출'],['산출물','포함할 것'],[['실행 코드','재현 조건과 패키지'],['결과 표','훈련·검증·테스트 역할'],['해석','오류 사례와 개선 근거']],['ml-grid-search-cv'],['같은 파이프라인에서 k 후보 하나를 추가하고 선택 근거를 기록하세요.'])

# IV. Synthetic data removes missing textbook image-file dependencies.
SCENE='''import cv2
import numpy as np
from pathlib import Path
Path("result").mkdir(exist_ok=True)
img = np.full((180, 260, 3), 235, dtype=np.uint8)
cv2.rectangle(img, (30, 30), (120, 130), (40, 80, 220), -1)
cv2.circle(img, (190, 90), 35, (40, 160, 40), -1)
cv2.imwrite("scene.png", img)
'''
def cvexample(id,title,src,notes=''):
 example(id,title,SCENE+src,'numpy opencv-python',mode='pc',note='제공 코드가 실습용 도형 이미지를 직접 생성합니다. result 폴더의 PNG를 열어 결과를 비교하세요. '+notes)
topic(4,'cv-overview','컴퓨터 비전과 영상 처리','134–139','사진을 다듬는 것과 사진의 의미를 판단하는 것을 구별하세요.',[
'영상 처리는 밝기·잡음·크기처럼 이미지 표현을 바꾸는 작업입니다. 컴퓨터 비전은 영상에서 물체·위치·행동 등 의미 있는 정보를 추론합니다. 전처리는 비전 시스템의 일부로 쓰일 수 있습니다.',
'스마트폰, 교통, 제조, 보안, 의료 보조 등에서 활용하지만 조명·가림·각도·데이터 분포 변화로 오류가 생길 수 있습니다. 인간은 맥락을 활용하고 컴퓨터는 수치 연산으로 반복 분석합니다. 촬영 자료의 이용 범위와 오판 영향을 생각하며 실습은 제공 도형과 사용 허락을 받은 자료로 진행하세요.'],['영상 입력','화질·크기 처리','특징·객체 분석','결과 표시·사람의 확인'],['작업','출력','구분'],[['블러','새 이미지','영상 처리'],['객체 검출','위치와 클래스','컴퓨터 비전'],['사람의 검토','맥락에 따른 판단','시스템 활용']],tasks=['학교에서 사용할 비전 기술의 이점과 오판 시 문제를 함께 설명하세요.'])
example('cv-pixels','작은 이미지의 픽셀·반전·이진화','''pixels = [[0, 64, 128], [192, 224, 255]]
threshold = 128
inverted = [[255-v for v in row] for row in pixels]
binary = [[255 if v > threshold else 0 for v in row] for row in pixels]
print("height, width:", len(pixels), len(pixels[0]))
print("Inverted:", inverted)
print("Binary:", binary)
''',checks='assert binary[0] == [0,0,0]\nassert inverted[1][-1] == 0')
topic(4,'cv-pixels','픽셀·해상도·RGB·그레이스케일','140–141','숫자 행렬이 그림이 되는 과정을 살펴보세요.',[
'이미지는 픽셀의 격자입니다. 너비×높이가 해상도이고, 8비트 채널 하나는 보통 0~255 값을 사용합니다. RGB는 빨강·초록·파랑 채널이고 그레이스케일은 밝기 한 채널입니다.',
'NumPy 이미지의 shape는 보통 (높이, 너비, 채널)입니다. 배열의 size는 채널을 포함한 원소 수이므로 컬러 이미지의 픽셀 수와 다릅니다. 예를 들어 (2,3,3)은 픽셀 6개, 채널 값 18개입니다.'],['숫자 하나｜한 채널 값','RGB 3개｜컬러 픽셀','행과 열｜이미지','연속된 이미지｜영상'],['표현','예','의미'],[['shape','(2,3,3)','높이2·너비3·채널3'],['픽셀 수','2×3=6','위치의 개수'],['원소 수 size','2×3×3=18','채널 값의 개수'],['OpenCV 기본 순서','B,G,R','RGB 표시 전 변환']],['cv-pixels'],['픽셀 실험실에서 기준이 128일 때 값 128이 어느 색이 되는지 확인하세요.'])
topic(4,'cv-pipeline','알고리즘·처리 과정·평가 기준','142–146','정확도뿐 아니라 처리 시간도 비교하세요.',[
'패턴 매칭은 정해진 모양과의 유사성, 특징점 검출은 모서리 같은 위치 단서, 머신러닝은 학습한 특징 관계, 딥러닝은 다층 신경망의 표현을 활용합니다. 목적과 입력 조건에 따라 도구를 고릅니다.',
'입력 → 전처리 → 특징 추출·검출 → 해석 → 출력으로 구성할 수 있습니다. 같은 대상도 조명과 각도가 바뀌면 결과가 달라집니다. 정확도·속도·실시간 지연·조건 변화에 대한 안정성을 함께 비교하세요.'],['입력','전처리','특징과 위치','의미 해석','출력·평가'],['기준','질문'],[['정확성','무엇을 놓치거나 잘못 찾나?'],['처리 시간','한 장에 몇 ms인가?'],['실시간성','입력부터 출력까지 얼마나 늦나?'],['안정성','조명·가림·각도 변화에도 유지되나?']],tasks=['번호판 검출과 문자 인식을 서로 다른 단계로 그려 보세요.'])
example('cv-pillow','Pillow로 만들기·크기 변경·회전·저장','''from PIL import Image, ImageDraw
img = Image.new("RGB", (240, 160), "white")
draw = ImageDraw.Draw(img)
draw.rectangle((30, 30, 130, 110), fill="navy")
draw.ellipse((145, 40, 215, 110), fill="orange")
img.save("original.png")
small = img.resize((120, 80))
small.save("small.png")
img.rotate(30, expand=True).save("rotated.png")
print("size (width, height):", img.size)
''','pillow',checks='assert small.size == (120,80)')
example('cv-skimage','scikit-image Sobel과 이미지 비교','''import numpy as np
from skimage import filters
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
img = np.zeros((48, 64))
img[10:35, 15:45] = 1
edges = filters.sobel(img)
fig, axes = plt.subplots(1, 2)
axes[0].imshow(img, cmap="gray")
axes[0].set_title("Original")
axes[1].imshow(edges, cmap="gray")
axes[1].set_title("Sobel")
plt.savefig("sobel.png")
print("Edge maximum:", edges.max())
''','numpy scikit-image matplotlib',mode='pc')
topic(4,'cv-libraries','OpenCV·Pillow·Matplotlib·scikit-image','147–154','입출력·편집·표시·분석 도구를 구별해 보세요.',[
'OpenCV는 영상 입출력과 처리·검출, Pillow는 이미지 편집·형식 변환, Matplotlib은 결과 비교와 그래프, scikit-image는 필터와 과학적 이미지 분석을 제공합니다.',
'OpenCV의 기본 컬러 읽기는 BGR이며 Pillow는 보통 RGB를 사용합니다. Pillow size의 (너비, 높이)와 NumPy shape의 (높이, 너비)를 구별하세요. 화면 표시 방식도 라이브러리별로 다릅니다.'],['입력 읽기','배열/이미지 객체','처리 도구 적용','표시·저장'],['도구','설치 이름','핵심 호출'],[['OpenCV','opencv-python','cv2.imread / cv2.imwrite'],['Pillow','pillow','Image.open / resize / save'],['Matplotlib','matplotlib','imshow / subplots'],['scikit-image','scikit-image','filters.sobel']],['cv-pillow','cv-skimage'],['같은 240×160 이미지에서 Pillow.size와 OpenCV.shape가 어떻게 다른지 적으세요.'])
cvexample('cv-io','OpenCV 읽기·색상·크기·회전·저장','''loaded = cv2.imread("scene.png")
if loaded is None:
    raise FileNotFoundError("scene.png")
print("shape:", loaded.shape, "size:", loaded.size)
gray = cv2.cvtColor(loaded, cv2.COLOR_BGR2GRAY)
small = cv2.resize(loaded, (130, 90))
center = (loaded.shape[1] / 2, loaded.shape[0] / 2)
matrix = cv2.getRotationMatrix2D(center, 30, 1.0)
rotated = cv2.warpAffine(loaded, matrix, (260, 180))
for name, data in [("gray", gray), ("small", small), ("rotated", rotated)]:
    assert cv2.imwrite(f"result/{name}.png", data)
print("Saved:", sorted(str(p) for p in Path("result").glob("*.png")))
''')
cvexample('cv-display','PC 창에서 이미지 보기','''cv2.imshow("Scene", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
''','창을 닫기 전에 키를 누릅니다. 화면 표시가 가능한 PC 환경이 필요합니다.')
topic(4,'cv-io','이미지 읽기·표시·변환·저장','155–162','파일을 못 읽었을 때 무엇부터 확인할까요?',[
'imread가 실패하면 None을 반환하므로 shape를 읽기 전에 확인합니다. cvtColor는 색 공간을, resize는 크기를 바꿉니다. getRotationMatrix2D와 warpAffine은 지정한 중심과 각도로 회전시킵니다.',
'OpenCV 창은 imshow로 표시하고 waitKey로 키 입력과 창 처리를 기다린 뒤 destroyAllWindows로 정리합니다. 저장 폴더를 먼저 만들고 imwrite의 성공 여부도 확인하세요. 고정 크기로 바꾸면 비율이 달라질 수 있고 회전 출력 영역 밖은 잘릴 수 있습니다.'],['imread → None 확인','색상·크기·회전','imshow + waitKey','imwrite 성공 확인','창 정리'],['변환','입력','주의'],[['resize','(너비,높이)','shape 순서와 반대'],['cvtColor','변환 코드','BGR↔RGB / GRAY'],['warpAffine','행렬·출력 크기','잘림과 빈 영역'],['imwrite','경로·이미지','폴더 먼저 생성']],['cv-io','cv-display'],['축소 후 픽셀 수와 원소 수를 계산하고 shape로 검증하세요.'])
cvexample('cv-filters','블러·Canny·세 가지 이진화 비교','''gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
outputs = {"mean": cv2.blur(img, (7,7)), "gaussian": cv2.GaussianBlur(img,(7,7),0), "median": cv2.medianBlur(img,7), "canny": cv2.Canny(gray,50,150)}
outputs["equalized"] = cv2.equalizeHist(gray)
outputs["clahe"] = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8)).apply(gray)
_, outputs["fixed"] = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
otsu, outputs["otsu"] = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
outputs["adaptive"] = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,7)
for name, data in outputs.items():
    cv2.imwrite(f"result/{name}.png", data)
print("Otsu threshold:", otsu)
''')
topic(4,'cv-filters','블러·에지·이진화','163–168','밝기를 부드럽게 할까요, 경계를 찾을까요?',[
'평균 블러는 주변 평균, 가우시안 블러는 가중 평균, 중앙값 블러는 주변 중앙값으로 잡음을 줄입니다. 커널이 커지면 세부 정보가 더 사라질 수 있습니다. Canny는 밝기 변화의 경계를 찾으며 두 임계값이 연결되는 에지의 선택에 영향을 줍니다.',
'고정 이진화는 한 기준, Otsu는 밝기 분포를 이용해 자동 선택한 기준, 적응형은 주변 영역별 기준을 사용합니다. THRESH_BINARY에서는 값이 기준보다 클 때 255이고 같거나 작으면 0입니다. 조명이 고르지 않으면 방법별 차이가 커집니다.'],['원본','블러로 잡음 완화','그레이스케일','에지 또는 이진화','조건별 결과 비교'],['기법','목적','바꿀 값'],[['블러','잡음 완화','커널 크기'],['Canny','경계 찾기','하한·상한'],['고정/Otsu','전역 이진화','고정/자동 임계값'],['적응형','영역별 이진화','홀수 blockSize·C']],['cv-filters'],['커널 3과 15, 고정 임계값 80과 180의 결과를 비교하세요.'])
cvexample('cv-perspective','네 점으로 원근 변환','''src = np.float32([[30,30],[220,15],[240,150],[15,160]])
dst = np.float32([[0,0],[199,0],[199,119],[0,119]])
M = cv2.getPerspectiveTransform(src, dst)
result = cv2.warpPerspective(img, M, (200,120))
cv2.imwrite("result/rectified.png", result)
print("Output:", result.shape)
''')
cvexample('cv-click-card','마우스로 카드 네 꼭짓점 선택','''points = []
preview = img.copy()
def clicked(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append([x,y])
        cv2.circle(preview,(x,y),4,(0,0,255),-1)
cv2.namedWindow("Click TL TR BR BL")
cv2.setMouseCallback("Click TL TR BR BL", clicked)
try:
    while len(points) < 4:
        cv2.imshow("Click TL TR BR BL", preview)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    if len(points) == 4:
        src = np.float32(points)
        dst = np.float32([[0,0],[199,0],[199,119],[0,119]])
        if abs(cv2.contourArea(src)) < 10:
            raise ValueError("사각형을 이루는 네 꼭짓점을 순서대로 선택하세요.")
        M = cv2.getPerspectiveTransform(src,dst)
        cv2.imwrite("result/clicked-card.png",cv2.warpPerspective(img,M,(200,120)))
finally:
    cv2.destroyAllWindows()
''','왼쪽 위→오른쪽 위→오른쪽 아래→왼쪽 아래 순서로 클릭하세요. ESC는 취소입니다.')
topic(4,'cv-transform','원근 변환과 마우스 이벤트','168–172','원본 네 점과 목적지 네 점의 순서를 맞춰 보세요.',[
'원근 변환은 기울어진 평면의 네 꼭짓점을 새 사각형의 네 꼭짓점에 대응시킵니다. getPerspectiveTransform으로 행렬을 구하고 warpPerspective로 새 이미지에 매핑합니다.',
'마우스 콜백은 클릭 좌표를 모으고, 네 점을 모으면 변환합니다. 두 목록의 순서를 일치시키고 교차되거나 한 직선 위에 놓인 점을 피하세요. ESC 취소와 읽기 실패도 처리합니다.'],['왼쪽 위','오른쪽 위','오른쪽 아래','왼쪽 아래','대응 행렬 → 새 이미지'],['단계','OpenCV','주의'],[['클릭 연결','setMouseCallback','이벤트 종류 확인'],['행렬','getPerspectiveTransform','float32·점 순서'],['변환','warpPerspective','출력 (너비,높이)']],['cv-perspective','cv-click-card'],['원본과 목적지에서 두 점 순서만 뒤바꾸면 어떤 문제가 생길지 예상하세요.'])
cvexample('cv-features','에지·코너·윤곽선 비교','''gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150)
corners = cv2.goodFeaturesToTrack(gray,50,0.01,10)
marked = img.copy()
if corners is not None:
    for corner in corners:
        x,y = corner.ravel().astype(int)
        cv2.circle(marked,(int(x),int(y)),4,(0,0,255),-1)
_, binary = cv2.threshold(gray,180,255,cv2.THRESH_BINARY_INV)
contours,_ = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
outlined = img.copy()
cv2.drawContours(outlined,contours,-1,(0,180,0),2)
for contour in contours:
    print("area:",cv2.contourArea(contour),"box:",cv2.boundingRect(contour))
for name,data in [("edges",edges),("corners",marked),("contours",outlined)]:
    cv2.imwrite(f"result/{name}.png",data)
''')
topic(4,'cv-features','에지·코너·윤곽선으로 중요한 부분 찾기','173–176','선·점·닫힌 경계 중 무엇이 필요한가요?',[
'에지는 밝기가 급변하는 경계, 코너는 여러 방향으로 밝기가 바뀌는 위치, 윤곽선은 이진 영역의 경계를 잇는 점 집합입니다. 파노라마의 대응 위치, 도형 개수, 크기 측정 등 목적에 따라 선택합니다.',
'코너가 없으면 반환값이 None일 수 있습니다. 윤곽선은 이진화 결과와 잡음에 영향을 받으므로 면적 등으로 걸러야 합니다. 단순히 에지를 찾았다고 물체의 종류나 신원을 안 것은 아닙니다.'],['그레이스케일','에지 / 코너 / 이진화','윤곽·위치·면적','그림에 표시'],['도구','결과','활용'],[['Canny','경계 픽셀','형태 단서'],['goodFeaturesToTrack','코너 좌표','영상 간 대응'],['findContours','경계 점 목록','영역·면적·개수']],['cv-features'],['네모와 원에서 코너 수가 왜 다른지 관찰하세요.'])
example('cv-haar','Haar 얼굴·눈·웃음 검출 · 정적 이미지','''import cv2
from pathlib import Path
image_path = "photo.jpg"  # 사용 허락을 받은 사진을 이 폴더에 넣으세요.
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError("photo.jpg 파일을 예제 폴더에 넣으세요.")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
smile = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
if any(c.empty() for c in [face,eye,smile]):
    raise RuntimeError("분류기 XML 파일을 확인하세요.")
faces = face.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
for x,y,w,h in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi = gray[y:y+h,x:x+w]
    for classifier,color,neighbors in [(eye,(0,255,0),5),(smile,(0,0,255),20)]:
        for a,b,c,d in classifier.detectMultiScale(roi,1.1,neighbors):
            cv2.rectangle(img,(x+a,y+b),(x+a+c,y+b+d),color,2)
Path("result").mkdir(exist_ok=True)
cv2.imwrite("result/faces.png",img)
print("Faces:",len(faces))
''','opencv-python',mode='pc',note='photo.jpg는 직접 준비합니다. 얼굴 위치를 찾는 예제이며 개인의 신원이나 감정을 판정하지 않습니다.')
example('cv-camera','실시간 얼굴 검출과 자원 정리','''import cv2
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
if face.empty():
    raise RuntimeError("분류기 로드 실패")
cap = cv2.VideoCapture(0)
try:
    if not cap.isOpened():
        raise RuntimeError("카메라 연결과 사용 권한을 확인하세요.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        for x,y,w,h in face.detectMultiScale(gray,1.1,5):
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow("Faces - press q to quit",frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
''','opencv-python',mode='pc',note='실제 카메라는 PC에서 직접 실행할 때만 사용합니다. 영상은 저장하지 않습니다.')
topic(4,'cv-haar','얼굴·눈·웃음 검출과 웹캠','177–184','얼굴의 위치를 찾는 것과 누구인지 아는 것은 달라요.',[
'Haar Cascade는 밝기 패턴과 단계적 판별로 특정 대상의 후보 영역을 찾습니다. 얼굴을 찾은 뒤 그 영역(ROI) 안에서 눈·웃음 패턴을 탐색하면 계산 범위를 줄일 수 있습니다. 웃음 패턴 검출만으로 감정을 단정할 수 없습니다.',
'scaleFactor는 크기 탐색 간격, minNeighbors는 후보 유지 조건에 영향을 줍니다. 값에 따른 속도·누락·오탐을 실제로 비교하세요. VideoCapture → read → 처리·표시 → 종료 흐름에서 실패를 확인하고 finally로 release와 창 정리를 보장합니다.'],['분류기·카메라 확인','프레임 읽기','얼굴 → ROI 속 눈/웃음','사각형 표시','종료·자원 해제'],['문제','시도','기록'],[['놓친 얼굴','크기 간격·조명 조절','누락 수'],['잘못 찾은 얼굴','minNeighbors 조절','오탐 수'],['느린 처리','프레임 축소','처리 시간'],['눈 좌표','ROI 원점 더하기','전체 화면 위치']],['cv-haar','cv-camera'],['같은 사진에서 minNeighbors를 바꾸고 오탐·누락 표를 작성하세요.'])
example('cv-yolo','YOLOv8 객체 검출 · 이미지 한 장','''from ultralytics import YOLO
from pathlib import Path
source = Path("photo.jpg")
if not source.is_file():
    raise FileNotFoundError("사용 허락을 받은 photo.jpg를 준비하세요.")
model = YOLO("yolov8n.pt")
result = model(str(source), device="cpu", conf=0.5)[0]
result.save(filename="detected.jpg")
for box in result.boxes:
    cls = int(box.cls.item())
    print(result.names[cls], round(float(box.conf.item()),3), box.xyxy.tolist())
''','ultralytics',mode='pc',note='교과서의 YOLOv8 모델을 사용합니다. 첫 실행에 가중치를 내려받으므로 네트워크·디스크 공간이 필요합니다.')
example('cv-yolo-count','YOLO 웹캠 프레임별 객체 개수','''import cv2
from ultralytics import YOLO
from collections import Counter
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
try:
    if not cap.isOpened():
        raise RuntimeError("카메라를 확인하세요.")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        result = model(frame,device="cpu",conf=0.5,verbose=False)[0]
        counts = Counter(result.names[int(box.cls.item())] for box in result.boxes)
        view = result.plot()
        for row,(name,count) in enumerate(sorted(counts.items())):
            cv2.putText(view,f"{name}: {count}",(10,30+25*row),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
        cv2.imshow("Frame counts - q to quit",view)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
''','ultralytics opencv-python',mode='pc',note='한 프레임 안의 개수입니다. 프레임 합계를 누적 통행 인원으로 해석하지 마세요.')
example('cv-count','검출 결과 목록으로 개수 세기','''from collections import Counter
frames = [["person", "car", "person"], ["person", "car"]]
for i, names in enumerate(frames):
    print("Frame", i, dict(Counter(names)))
# 같은 객체가 다음 프레임에 다시 등장할 수 있으므로 합계는 고유 객체 수가 아닙니다.
''',checks='assert Counter(frames[0])["person"] == 2')
topic(4,'cv-yolo','YOLOv8 객체 탐지와 개수 표시','185–191','박스·클래스·신뢰도를 읽고 프레임별 개수를 세어 보세요.',[
'YOLO 예제는 사전 학습된 yolov8n.pt로 이미지 속 여러 클래스의 위치와 점수를 반환합니다. 이 단원은 교과서의 YOLOv8 경로를 다루며 특정 버전을 최신이라고 단정하지 않습니다. conf 기준을 바꾸면 출력되는 후보 수가 달라집니다.',
'검출 결과의 boxes.cls는 클래스 번호, conf는 모델 점수, xyxy는 박스 좌표입니다. 프레임마다 Counter를 새로 만들어 현재 개수를 셉니다. 여러 프레임의 합계는 고유 객체 수가 아니며, 누적 통행량에는 추적과 중복 처리 설계가 더 필요합니다. 보안·교통·매장·농업·운전 보조 등 응용에서는 해당 대상의 학습 범위와 실패 조건도 확인해야 합니다.'],['모델·입력 준비','추론','클래스·좌표·점수','현재 프레임 개수','표시·조건 비교'],['Haar','YOLO','선택 기준'],[['특정 패턴 분류기','다중 클래스 모델','찾을 대상'],['명암 패턴 기반','학습 가중치 기반','입력 조건'],['CPU에서 비교적 가벼운 구성','모델·해상도별 비용 차이','실측 속도와 오류']],['cv-yolo','cv-yolo-count','cv-count'],['conf를 바꿨을 때 물체를 놓치는 경우와 오탐이 어떻게 달라지는지 기록하세요.'])
topic(4,'cv-project','컴퓨터 비전 프로젝트와 단원 정리','192–195 + 확장','입력·처리·출력을 나누어 완성하세요.',[
'문서 스캔은 원근 보정 → 잡음 완화 → 대비 조정 → 이진화 흐름을 실험할 수 있습니다. 항상 한 순서가 모든 이미지에 최선인 것은 아니므로 같은 입력에서 결과를 비교하세요. 정적 이미지로 검증한 뒤 카메라 입력으로 확장합니다.',
'라이브러리 선택, 블러·이진화·에지의 목적, 얼굴 검출과 개인 식별의 차이, Haar 코드의 분류기·detectMultiScale·imshow를 점검하세요. 이미지와 오류 조건, 결과 비교표, 처리 시간과 한계를 함께 제출합니다.'],['입력 자료·목표','처리 함수 모듈','오류·조건별 결과','GUI 또는 카메라 연결','비교표·저널'],['프로젝트','핵심 처리','확인'],[['문서 스캔','원근·대비·이진화','글자와 경계 보존'],['도형 계수','이진화·윤곽','잡음 제외'],['객체 탐지','Haar / YOLO','오탐·누락·속도']],['cv-perspective','cv-features'],['2단원 GUI의 버튼에서 이미지 처리 함수를 호출하는 앱을 설계하세요.'])

# Questions: concept transfer, output prediction, ordering, coding and explanation.
def choice(u,topic,prompt,answer,options,explain,ref='보강'):
 import random
 options=list(options);random.Random(prompt).shuffle(options)
 q(u,topic,'선택',prompt,answer,'개념 표의 입력·출력과 비교하세요.',explain,options=options,ref=ref)
def choice5(u,topic,prompt,answer,options,explain,ref='보강',level='기본',qid=None):
 import random
 options=list(options);random.Random(prompt).shuffle(options)
 assert len(set(options))==5 and answer in options,f'{qid}: 5지선다 옵션 확인'
 q(u,topic,'선택',prompt,answer,'개념 표의 입력·출력과 비교하세요.',explain,options=options,ref=ref,level=level,qid=qid)
# 2026-09-28 (#131) 3단원 문항 재편 — 보기 2개짜리 선택형을 모두 5지선다로
# 교체하고, 교과서 원문 문항(확인 학습 84·128쪽, 대단원 종합 평가 129~131쪽)은
# 그대로 인용한다. 옛 u3-q001~018은 폐기(재사용 금지), 신규는 u3-q101부터.
choice5(3,'ml-overview','다음 중 인공지능·머신러닝·딥러닝의 포함 관계를 올바르게 나타낸 것은?','인공지능 ⊃ 머신러닝 ⊃ 딥러닝',
 ['인공지능 ⊃ 머신러닝 ⊃ 딥러닝','딥러닝 ⊃ 머신러닝 ⊃ 인공지능','머신러닝 = 딥러닝 = 인공지능','머신러닝 ⊃ 인공지능 ⊃ 딥러닝','인공지능 ⊃ 딥러닝 ⊃ 머신러닝'],
 '인공지능이 가장 넓은 범위이고 머신러닝, 딥러닝 순서로 좁아집니다.',ref='교과서 129쪽 3',qid='u3-q101')
choice5(3,'ml-overview','다음 설명 중 옳은 것은?','모든 딥러닝은 머신러닝에 속하지만, 모든 머신러닝이 딥러닝인 것은 아니다',
 ['모든 딥러닝은 머신러닝에 속하지만, 모든 머신러닝이 딥러닝인 것은 아니다','모든 인공지능은 머신러닝이다','머신러닝은 딥러닝의 한 종류이다','딥러닝은 규칙 기반 프로그래밍의 한 종류이다','머신러닝과 딥러닝은 서로 관련 없는 별개의 기술이다'],
 '딥러닝은 다층 신경망을 사용하는 머신러닝의 한 갈래이며, 모든 AI가 머신러닝인 것은 아닙니다.',ref='보강',level='심화',qid='u3-q102')
choice5(3,'ml-use','다음 중 머신러닝을 활용하는 것이 적절한 이유로 옳지 않은 것은?','정답이 항상 하나로 고정된 사칙연산처럼 규칙이 단순하고 명확하다',
 ['정확한 규칙을 사람이 일일이 정의하기 어려운 복잡한 패턴이 있다','충분한 양의 학습 데이터를 구할 수 있다','문제의 입력과 출력 사이에 통계적인 규칙성이 있다','정답이 항상 하나로 고정된 사칙연산처럼 규칙이 단순하고 명확하다','유사한 사례들을 일반화해 새로운 입력에도 대응해야 한다'],
 '사칙연산처럼 규칙이 단순하고 명확한 문제는 일반 프로그램이 더 간단합니다.',ref='보강',level='심화',qid='u3-q103')
choice5(3,'ml-use','학습 데이터가 실제 사용 환경의 분포를 충분히 대표하지 못할 때에 대한 설명으로 가장 적절한 것은?','데이터에 없는 조건에서는 예측 오류가 늘어날 수 있어 사용 범위와 한계를 함께 안내해야 한다',
 ['데이터에 없는 조건에서는 예측 오류가 늘어날 수 있어 사용 범위와 한계를 함께 안내해야 한다','데이터 양만 많으면 대표성 문제는 항상 저절로 해결된다','훈련 정확도가 높으면 대표성 문제가 없다는 뜻이다','전처리(정규화·인코딩)만 잘하면 대표성 부족 문제가 사라진다','대표성 문제는 회귀에서만 발생하고 분류에서는 발생하지 않는다'],
 '훈련에 없던 조건에서는 근거가 부족해 오류가 늘 수 있으므로 한계를 함께 안내해야 합니다.',ref='보강',level='심화',qid='u3-q104')
q(3,'ml-process','순서','다음은 일반적인 머신러닝 문제 해결을 위한 데이터 전처리 과정들이다. 가장 적절한 순서대로 나열하시오.',
 ['데이터 불러오기','데이터 탐색 (head(), describe() 등)','결측치 및 이상치 처리','데이터 변환 (정규화/표준화) 또는 범주형 데이터 인코딩','훈련/테스트 데이터 분할'],
 '자료를 불러와 살펴본 뒤 값을 정리하고 바꿉니다.','불러오기→탐색→결측치·이상치 처리→변환→분할 순서입니다. 분할 시점은 교과서 71~75쪽의 일반 순서와 다를 수 있습니다.',ref='교과서 128쪽 2',qid='u3-q105')
choice5(3,'ml-terms','''다음 두 코드 중 데이터 누수(data leakage)가 있는 것은?
A)
X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler = StandardScaler().fit(X_train)
X_train2, X_test2 = scaler.transform(X_train), scaler.transform(X_test)
B)
scaler = StandardScaler().fit(X)
X_train, X_test, y_train, y_test = train_test_split(scaler.transform(X), y)''','B. 분할 전 전체 데이터로 스케일러를 학습해 테스트 정보가 훈련 기준에 섞인다',
 ['A. 훈련 데이터로만 스케일러를 학습해 테스트 정보가 섞이지 않는다','B. 분할 전 전체 데이터로 스케일러를 학습해 테스트 정보가 훈련 기준에 섞인다','A, B 모두 데이터 누수가 있다','A, B 모두 데이터 누수가 없다','스케일러는 훈련·테스트 어느 쪽으로 fit해도 결과가 같다'],
 'B는 분할 전 전체 데이터로 평균·표준편차를 구해 테스트의 정보가 훈련 기준에 섞입니다.',ref='보강',level='심화',qid='u3-q106')
choice5(3,'ml-terms','다음 중 하이퍼파라미터에 대한 설명으로 옳은 것은?','k-NN의 n_neighbors처럼 학습을 시작하기 전에 사람이 정하는 값이다',
 ['k-NN의 n_neighbors처럼 학습을 시작하기 전에 사람이 정하는 값이다','모델이 fit() 과정에서 데이터로부터 자동으로 계산해 정하는 값이다','예측하려는 정답 열 y를 가리키는 다른 이름이다','입력으로 사용하는 특성(X) 값 자체를 의미한다','예측값과 실제값의 차이인 잔차를 의미한다'],
 'n_neighbors는 학습 전에 사용자가 설정하며, fit()으로 데이터에서 자동으로 정해지는 값(파라미터)과 다릅니다.',ref='교과서 78쪽',qid='u3-q107')
choice5(3,'ml-methods','다음 중 분류(Classification) 문제의 예시에 해당하는 것은?','이메일이 스팸인지 아닌지 판별',
 ['주식 종가 예측','주택 가격 예측','내일의 기온 예측','고객의 구매 금액 예측','이메일이 스팸인지 아닌지 판별'],
 '분류는 범주를 예측하며, 나머지는 모두 연속적인 수치를 예측하는 회귀입니다.',ref='교과서 130쪽 5',level='심화',qid='u3-q108')
choice5(3,'ml-methods','고객의 방문 횟수·총 구매 금액·마지막 방문일 정보로 유사한 그룹을 나누어 맞춤형 마케팅을 하려 한다. 가장 적합한 머신러닝 알고리즘 유형은?','군집화',
 ['군집화','분류','회귀','차원 축소','강화 학습'],
 '정답 없이 유사성을 기준으로 그룹을 찾는 것은 군집화이며, 차원 축소는 정답 없이도 변수 개수를 줄이는 다른 비지도 학습입니다.',ref='교과서 128쪽 3',level='심화',qid='u3-q109')
choice5(3,'ml-methods','미로를 탈출하는 로봇이 벽에 부딪히면 감점되고 출구에 도달하면 큰 점수를 받아 행동 전략을 계속 개선해 나간다. 이 방식이 속하는 학습 유형은?','강화 학습',
 ['강화 학습','지도 학습(분류)','지도 학습(회귀)','비지도 학습(군집)','비지도 학습(차원 축소)'],
 '상태를 보고 행동한 뒤 보상을 받아 정책을 개선하는 방식은 강화 학습입니다.',ref='교과서 84쪽 3 연계',qid='u3-q110')
choice5(3,'ml-libraries','pandas의 DataFrame에 대한 설명으로 옳은 것은?','정수·실수·문자열 등 여러 자료형의 열을 함께 담을 수 있다',
 ['정수·실수·문자열 등 여러 자료형의 열을 함께 담을 수 있다','반드시 모든 값이 수치형이어야 한다','한 번 만든 DataFrame은 열을 추가할 수 없다','DataFrame은 1차원 데이터만 표현한다','describe()는 문자열 열의 평균을 계산해 준다'],
 'DataFrame은 열마다 다른 자료형을 가질 수 있는 표 구조입니다.',ref='교과서 128쪽 1①',qid='u3-q111')
choice5(3,'ml-preprocess','''다음 코드에서 전처리 원칙에 어긋나는 줄은?
scaler = StandardScaler()
scaler.fit(X_train)
X_train_s = scaler.transform(X_train)
scaler.fit(X_test)
X_test_s = scaler.transform(X_test)''','scaler.fit(X_test) — 테스트 데이터로 다시 fit하면 훈련 때와 다른 기준이 적용된다',
 ['scaler.fit(X_test) — 테스트 데이터로 다시 fit하면 훈련 때와 다른 기준이 적용된다','scaler.fit(X_train) — 훈련 데이터로 fit하면 안 된다','X_train_s = scaler.transform(X_train) — transform을 쓰면 안 된다','StandardScaler() — 이 클래스를 쓰면 안 된다','네 줄 모두 문제가 없다'],
 '테스트는 훈련에서 배운 기준(scaler.fit(X_train))으로만 transform해야 하며, 테스트로 다시 fit하면 기준이 달라져 평가가 왜곡됩니다.',ref='교과서 128쪽 2 연계',level='심화',qid='u3-q112')
choice5(3,'ml-preprocess','''다음 코드의 출력은?
from sklearn.preprocessing import MinMaxScaler
import numpy as np
scaler = MinMaxScaler().fit(np.array([[10.],[20.],[30.]]))
print(scaler.transform(np.array([[50.]])))''','[[2.]]',
 ['[[2.]]','[[1.]]','[[0.5]]','[[5.]]','오류가 발생해 변환할 수 없다'],
 '(50-10)/(30-10)=2.0이며, 훈련 범위를 넘는 값은 0~1을 벗어날 수 있습니다.',ref='보강',level='심화',qid='u3-q113')
choice5(3,'ml-classification','다음 중 지도 학습(Supervised Learning)의 대표적인 알고리즘이 아닌 것은?','K-평균 군집화',
 ['의사 결정나무','선형 회귀','로지스틱 회귀','K-평균 군집화','K-최근접 이웃'],
 'K-평균 군집화는 정답 없이 그룹을 찾는 비지도 학습 알고리즘입니다.',ref='교과서 130쪽 6',level='심화',qid='u3-q114')
choice5(3,'ml-regression','''다음 코드의 출력과 그 의미로 옳은 것은?
from sklearn.metrics import r2_score
y_true = [3, 5, 7, 9]
y_pred = [9, 1, 9, 1]
print(round(r2_score(y_true, y_pred), 1))''','-5.0, 평균값으로 예측하는 것보다 오차가 훨씬 크다는 뜻이다',
 ['-5.0, 평균값으로 예측하는 것보다 오차가 훨씬 크다는 뜻이다','-5.0, 코드에 오류가 있다는 뜻이다','5.0, 정확도가 5배 높다는 뜻이다','0.5, 절반은 맞혔다는 뜻이다','1.0, 완벽하게 예측했다는 뜻이다'],
 'R²는 평균 예측 기준과 비교한 값이며, 그보다 못하면 음수가 되고 코드 오류를 뜻하지 않습니다.',ref='교과서 121–123쪽',level='심화',qid='u3-q115')
choice5(3,'ml-cluster','''다음 코드에서 X는 서로 떨어진 세 무리로 이루어진 90개의 점이다. print(len(set(labels)))의 출력은?
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, n_init=10, random_state=42)
labels = km.fit_predict(X)
print(len(set(labels)))''','3',
 ['3','1','90','30','정답 레이블이 없어 알 수 없다'],
 'n_clusters=3으로 지정했으므로 labels에는 서로 다른 군집 번호가 3가지 나타납니다.',ref='보강',level='심화',qid='u3-q116')
choice5(3,'ml-cluster','K-평균 군집화 결과 labels_에서 군집 번호 2를 부여받은 그룹은 군집 번호 0을 부여받은 그룹보다 항상 더 우수한 그룹인가요?','아니다. 번호는 그룹을 구별하는 이름일 뿐 순위나 품질을 뜻하지 않는다',
 ['아니다. 번호는 그룹을 구별하는 이름일 뿐 순위나 품질을 뜻하지 않는다','그렇다. 번호가 클수록 항상 더 우수하다','그렇다. 번호가 클수록 항상 중심에서 가깝다','아니다. 번호가 작을수록 항상 더 우수하다','군집 번호는 실행할 때마다 항상 똑같이 부여된다'],
 '군집 번호는 식별용이며 실행 조건에 따라 번호가 달라질 수 있습니다.',ref='교과서 108–111쪽',level='심화',qid='u3-q117')
choice5(3,'ml-metrics','스팸 메일 분류 모델에서 실제 스팸이 아닌 중요한 메일이 스팸함으로 잘못 분류되는 경우(False Positive)를 최대한 줄이려 한다. 가장 중요하게 고려해야 할 지표는?','정밀도(Precision)',
 ['결정계수(R²)','재현율(Recall)','정밀도(Precision)','정확도(Accuracy)','F1 점수(F1 Score)'],
 '스팸을 양성으로 두면 정상 메일을 스팸으로 잘못 분류한 것이 FP이며, 이를 줄이려면 정밀도를 봅니다.',ref='교과서 129쪽 1',level='심화',qid='u3-q118')
choice5(3,'ml-metrics','다음 중 평가 지표와 사용 문제 유형의 연결로 옳지 않은 것은?','정밀도(Precision) – 회귀 문제',
 ['정밀도(Precision) – 회귀 문제','재현율(Recall) – 분류 문제','평균절대오차(MAE) – 회귀 문제','결정계수(R²) – 회귀 문제','F1 점수 – 분류 문제'],
 '정밀도는 TP·FP를 세는 분류 지표이며 회귀에는 쓰지 않습니다.',ref='교과서 84쪽 1② 연계',level='심화',qid='u3-q119')
choice5(3,'ml-selection','다음 중 과대 적합(Overfitting)을 방지하는 방법으로 적절하지 않은 것은?','학습 데이터의 정확도를 높이기 위해 과도하게 반복 학습한다',
 ['모델의 복잡도를 줄인다','더 많은 데이터를 수집하여 학습시킨다','교차 검증을 활용하여 모델을 평가한다','정규화(Regularization) 기법을 사용한다','학습 데이터의 정확도를 높이기 위해 과도하게 반복 학습한다'],
 '훈련 정확도만 높이려는 과도한 반복 학습은 오히려 과대 적합을 키웁니다.',ref='교과서 130쪽 4',level='심화',qid='u3-q120')
choice5(3,'ml-selection','검증 점수를 보고 하이퍼파라미터를 계속 조정한 뒤, 남겨 둔 테스트 데이터로 최고 점수가 나올 때까지 설정을 또 바꾼다면 어떤 문제가 생기나요?','테스트 데이터가 모델 선택에 사용되어 독립적인 최종 평가가 아니게 된다',
 ['테스트 데이터가 모델 선택에 사용되어 독립적인 최종 평가가 아니게 된다','테스트 점수가 항상 더 정확해진다','과대 적합이 자동으로 해결된다','교차 검증이 필요 없어진다','테스트 데이터의 크기가 줄어든다'],
 '테스트는 선택이 끝난 뒤 마지막에 한 번만 사용해야 독립적인 평가로 남습니다.',ref='보강',level='심화',qid='u3-q121')
q(3,'ml-project','서술','다음 두 가지 시나리오를 읽고, 각 시나리오에 가장 적합한 머신러닝 학습 방식과 그 이유를 설명하시오.\n시나리오 A: 과거 10년간의 주식 시장 데이터(주가, 거래량, 뉴스 기사 감성 점수 등)를 분석하여 내일의 특정 주식 종목의 종가를 예측하는 모델을 개발하려고 한다.\n시나리오 B: 수십만 명의 온라인 쇼핑몰 고객 데이터를 분석하여, 고객들을 구매 패턴이나 관심사에 따라 유사한 몇 개의 그룹으로 나누고 각 그룹별 맞춤형 마케팅 전략을 세우고자 한다.',
 '시나리오 A는 지도 학습입니다. 과거 데이터에 내일의 종가라는 명확한 정답(레이블)이 있고, 이 정답을 학습해 미래 값을 예측하는 문제이기 때문입니다.\n시나리오 B는 비지도 학습입니다. 고객을 그룹으로 나누는 데 명확한 정답이 없으며, 데이터 자체의 유사성과 패턴을 바탕으로 그룹을 탐색하고 형성하는 것이 목표이기 때문입니다.',
 '정답 열이 데이터에 있는지 먼저 확인하세요.','레이블의 존재 여부로 지도/비지도를 구별하세요.',ref='교과서 129쪽 2',qid='u3-q122')
choice5(3,'ml-project','재현 가능한 머신러닝 프로젝트 보고서에 반드시 포함해야 할 것으로 가장 적절한 것은?','데이터 출처, 분할 방법, 전처리 기준, 난수 조건, 평가 지표와 결과',
 ['데이터 출처, 분할 방법, 전처리 기준, 난수 조건, 평가 지표와 결과','가장 성능이 좋았던 결과 화면만 캡처한 이미지','모델을 만든 사람의 이름과 날짜만','테스트 점수만 적은 한 줄 요약','과대 적합 여부를 확인하지 않은 최종 점수'],
 '재현하려면 데이터·분할·전처리·난수·평가까지 흐름 전체를 기록해야 합니다.',ref='보강',level='심화',qid='u3-q123')
# 2026-09-28 (#131 검토 반영) 단순 암기 빈칸(옛 u3-q019~025)을 코드 출력·계산
# 적용형 5지선다로 교체한다. 모두 /tmp/mlenv/bin/python으로 실행해 정답을 확인했다.
choice5(3,'pandas','''다음 코드를 실행한 결과로 옳은 것은?
import pandas as pd
df = pd.DataFrame({"name": ["A", "B", "C"], "score": [75, 90, 85]})
print(df.shape)''','(3, 2)',
 ['(3, 2)','(2, 3)','(3,)','(2,)','(75, 90, 85)'],
 '행이 3개(A,B,C), 열이 2개(name, score)이므로 shape는 (3, 2)입니다.',ref='보강',qid='u3-q124')
choice5(3,'pandas','''다음 코드를 실행한 결과로 옳은 것은?
import pandas as pd
df = pd.DataFrame({"score": [70, 80, 90, 100]})
print(df["score"].mean())''','85.0',
 ['85.0','90.0','80.0','340.0','87.5'],
 '(70+80+90+100)/4 = 85.0입니다.',ref='보강',qid='u3-q125')
choice5(3,'모델','''다음 코드에서 모델 학습·평가 원칙에 어긋나는 부분은?
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_test, y_test)
pred = model.predict(X_train)''','테스트 데이터로 모델을 학습(fit)했다',
 ['테스트 데이터로 모델을 학습(fit)했다','n_neighbors 값이 너무 크다','predict의 인자로 X_train을 사용했다','fit과 predict의 순서가 바뀌었다','KNeighborsClassifier 대신 다른 모델을 써야 한다'],
 '모델은 훈련 데이터(X_train, y_train)로 학습해야 하며, 테스트 데이터로 학습하면 평가가 무의미해집니다.',ref='보강',level='심화',qid='u3-q126')
choice5(3,'모델','''붓꽃 데이터(150개)를 다음과 같이 나눌 때 출력으로 옳은 것은?
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(X_train.shape, X_test.shape)''','(105, 4) (45, 4)',
 ['(105, 4) (45, 4)','(45, 4) (105, 4)','(150, 4) (150, 4)','(105,) (45,)','(120, 4) (30, 4)'],
 '전체 150개 중 30%인 45개가 테스트, 나머지 105개가 훈련이며 특성은 4개입니다.',ref='보강',level='심화',qid='u3-q127')
choice5(3,'평가','''다음 코드의 출력은?
from sklearn.metrics import precision_score, recall_score
y_true = [1]*10 + [0]*8
y_pred = [1]*8 + [0]*2 + [1]*4 + [0]*4
print(round(precision_score(y_true, y_pred), 2), round(recall_score(y_true, y_pred), 2))''','0.67 0.8',
 ['0.67 0.8','0.8 0.67','0.75 0.75','1.0 0.8','0.67 0.6'],
 '정밀도 8/(8+4)=0.67, 재현율 8/(8+2)=0.8이며, 이 경우 정밀도가 재현율보다 낮습니다.',ref='보강',level='심화',qid='u3-q128')
choice5(3,'평가','''다음 코드의 출력은?
from sklearn.metrics import mean_absolute_error, mean_squared_error
y_true = [2, 4, 6]
y_pred = [3, 4, 4]
print(round(mean_absolute_error(y_true, y_pred), 2), round(mean_squared_error(y_true, y_pred), 2))''','1.0 1.67',
 ['1.0 1.67','1.67 1.0','1.0 1.0','3.0 9.0','0.33 1.67'],
 'MAE=(1+0+2)/3=1.0, MSE=(1+0+4)/3≈1.67이며 큰 오차가 있어 MSE가 더 큽니다.',ref='보강',level='심화',qid='u3-q129')
choice5(3,'pandas','sales_df.describe()가 기본으로 반환하는 값에 포함되지 않는 것은?','최빈값(mode)',
 ['최빈값(mode)','평균(mean)','표준편차(std)','최솟값(min)','최댓값(max)'],
 'describe()의 기본 출력은 count·mean·std·min·25%·50%·75%·max이며 최빈값은 없습니다.',ref='교과서 131쪽 7③ 연계',level='심화',qid='u3-q130')
choice5(3,'평가','''다음 코드의 출력은? (훈련 데이터는 105개)
from sklearn.model_selection import cross_val_score
scores = cross_val_score(pipe, X_train, y_train, cv=5)
print(len(scores))''','5',
 ['5','105','1','21','훈련 데이터 개수와 같다'],
 'cv=5는 훈련 데이터를 5묶음으로 나눠 5번 검증한다는 뜻이므로 점수도 5개입니다.',ref='보강',level='심화',qid='u3-q131')
for topic_name,prompt,answer,other,explain,ref in [
('기본','이미지 밝기를 부드럽게 만드는 작업은?','영상 처리','개인 식별','픽셀 값을 바꾸는 처리입니다.','교과서 146쪽 1'),
('픽셀','shape가 (2,3,3)인 이미지의 픽셀 수는?','6','18','높이×너비이며 채널 수는 곱하지 않습니다.','교과서 140–141쪽'),
('픽셀','같은 배열의 size 값은?','18','6','size는 채널을 포함한 전체 원소 수입니다.','교과서 150쪽 보완'),
('색상','OpenCV imread의 기본 컬러 순서는?','BGR','RGB','Pillow 및 일반 RGB 표시와 순서가 다릅니다.','교과서 155–156쪽'),
('입출력','imread가 파일을 못 읽으면 보통 무엇을 반환하나요?','None','빈 문자열','shape 전에 None을 확인합니다.','교과서 155쪽'),
('크기','cv2.resize(img,(80,60))의 결과 높이와 너비는?','높이 60, 너비 80','높이 80, 너비 60','크기 인자는 (너비, 높이)입니다.','교과서 157쪽'),
('이진화','THRESH_BINARY 기준 127에서 값 127의 결과는?','0','255','기준보다 커야 흰색입니다.','교과서 167–168쪽'),
('이진화','그림자가 있는 문서에서 영역별 기준을 적용하는 것은?','적응형 이진화','고정 이진화','주변 영역의 정보를 사용합니다.','교과서 172쪽 탐구'),
('특징','파노라마에서 공통 위치 단서로 쓰기 좋은 것은?','코너','전체 이미지 평균','여러 방향의 변화가 있는 코너를 대응할 수 있습니다.','교과서 176쪽'),
('특징','물체의 면적과 외곽 경계를 구할 때 활용할 것은?','윤곽선','키보드 이벤트','이진 영역의 경계 점으로 면적 등을 계산합니다.','교과서 173–176쪽'),
('얼굴','Haar 얼굴 검출 결과만으로 사람의 이름을 알 수 있나요?','알 수 없다','자동으로 알 수 있다','얼굴 위치 검출과 개인 식별은 다릅니다.','교과서 177–184쪽 보완'),
('얼굴','얼굴 ROI의 눈 좌표를 원본 위치로 바꾸려면?','얼굴 원점 좌표를 더한다','이미지 너비를 곱한다','지역 좌표를 전역 좌표로 옮깁니다.','교과서 181–182쪽'),
('YOLO','각 프레임의 person 수를 합하면 고유 방문자 수인가요?','아니다','항상 맞다','같은 사람이 여러 프레임에 반복될 수 있습니다.','교과서 188–190쪽 보강'),
('평가','비전 시스템에서 처리 속도 외에 확인할 것은?','오탐·누락과 조건별 안정성','창의 배경색만','빠르게 틀리는 시스템은 적합하지 않습니다.','교과서 144쪽'),
('도구','실시간 영상 입출력과 검출을 함께 다루는 대표 도구는?','OpenCV','pandas','비디오 프레임과 검출 기능을 제공합니다.','교과서 195쪽 4'),
('도구','픽셀 단위 영역 분석 도구를 고를 때 고려할 것은?','scikit-image의 분석 기능','random의 주사위 기능','측정과 분석 기능을 목적에 맞게 선택합니다.','교과서 195쪽 4')]:choice(4,topic_name,prompt,answer,[other,answer],explain,ref)
# qid를 명시해 u3-q101~123 삽입으로 이 뒤 자동 번호가 밀리지 않게 고정한다(#131).
for u,topic_name,p,a,e,ref,qid in [
(4,'검출','CascadeClassifier에 사용하는 정면 얼굴 파일 이름은?','haarcascade_frontalface_default.xml','OpenCV의 haarcascades 폴더에 있습니다.','교과서 195쪽 3①','u4-q017'),
(4,'검출','face_cascade.____(gray,1.1,5)에서 빈칸은?','detectMultiScale','여러 크기로 얼굴 영역을 찾습니다.','교과서 195쪽 3②','u4-q018'),
(4,'입출력','cv2.____("Result",img)로 화면을 표시합니다.','imshow','키 입력 처리는 waitKey로 합니다.','교과서 195쪽 3③','u4-q019'),
(4,'입출력','cv2.____("photo.jpg")로 이미지를 읽습니다.','imread','읽기 실패 시 None을 확인합니다.','교과서 162쪽','u4-q020'),
(4,'변환','cv2.____(img,cv2.COLOR_BGR2GRAY)로 회색조 변환합니다.','cvtColor','색 공간 변환입니다.','교과서 162쪽','u4-q021'),
(4,'반전','8비트 밝기 40의 반전 값은?','215','255-40입니다.','보강','u4-q022')]:q(u,topic_name,'빈칸',p,a,'예제의 함수 이름 또는 식을 확인하세요.',e,ref=ref,qid=qid)
for u,topic_name,p,a,e,qid in [
(3,'과정','데이터 누수 없이 예측 모델을 구성하는 순서를 정하세요.',['입력과 정답 정의','훈련·테스트 분할','훈련 데이터로 전처리 학습','모델 학습·검증','최종 테스트 평가'],'테스트에서 평균·스케일을 배우지 않습니다.','u3-q026'),
(3,'평가','설정 후보를 고르고 최종 평가하는 순서를 정하세요.',['최종 테스트 보관','훈련 부분 교차 검증','설정 선택','전체 훈련 부분 재학습','테스트 점수 보고'],'교차 검증과 테스트의 역할을 나눕니다.','u3-q027'),
(4,'문서 스캔','기울고 어두운 문서의 처리 경로 예를 배열하세요.',['원근 변환','가우시안 블러','대비 조정','이진화'],'교과서 194쪽 2의 경로입니다. 실제 최적 순서는 입력을 비교해 정합니다.','u4-q023'),
(4,'카메라','카메라 프로그램의 기본 순서를 정하세요.',['카메라 열기','연결 성공 확인','프레임 읽고 처리','종료 입력 확인','카메라·창 자원 해제'],'실패해도 자원을 정리합니다.','u4-q024')]:q(u,topic_name,'순서',p,a,'입력이 준비되어야 다음 작업을 할 수 있습니다.',e,qid=qid)
for u,topic_name,p,starter,answer,checks,hint,qid in [
(3,'평가','mae(actual,pred)가 평균 절대 오차를 반환하게 만드세요.','def mae(actual,pred):\n    pass','def mae(actual,pred):\n    return sum(abs(a-p) for a,p in zip(actual,pred))/len(actual)','assert mae([1,3],[2,2])==1\nassert mae([0,0],[2,-4])==3','길이가 같은 비어 있지 않은 목록을 입력받는다고 가정합니다.','u3-q028'),
(3,'평가','precision(tp,fp)가 정밀도를 반환하게 하세요. 분모 0은 0으로 처리합니다.','def precision(tp,fp):\n    pass','def precision(tp,fp):\n    return tp/(tp+fp) if tp+fp else 0','assert precision(6,2)==0.75\nassert precision(0,0)==0\nassert precision(0,3)==0','양성이라고 예측한 전체 개수를 분모로 씁니다.','u3-q029'),
(3,'전처리','fill(values)가 None을 관측값 평균으로 채운 새 목록을 반환하게 만드세요. 관측값은 한 개 이상입니다.','def fill(values):\n    pass','def fill(values):\n    valid=[v for v in values if v is not None]\n    mean=sum(valid)/len(valid)\n    return [mean if v is None else v for v in values]','v=[0,None,4]\nassert fill(v)==[0,2,4]\nassert v==[0,None,4]\nassert fill([None,6])==[6,6]','0은 결측값이 아닙니다.','u3-q030'),
(3,'회귀','predict(x,w,b)가 선형 예측값을 반환하도록 고치세요.','def predict(x,w,b):\n    return x+w+b','def predict(x,w,b):\n    return w*x+b','assert predict(3,2,1)==7\nassert predict(-2,3,4)==-2','가중치×입력 + 절편입니다.','u3-q031'),
(4,'이진화','binary(values,t)가 OpenCV THRESH_BINARY와 같은 기준으로 0/255 목록을 반환하게 하세요.','def binary(values,t):\n    pass','def binary(values,t):\n    return [255 if v>t else 0 for v in values]','assert binary([0,127,128,255],127)==[0,0,255,255]\nassert binary([255],255)==[0]','기준과 같으면 0입니다.','u4-q025'),
(4,'색상','bgr_to_rgb(pixel)이 채널 순서를 바꾼 튜플을 반환하게 만드세요.','def bgr_to_rgb(pixel):\n    pass','def bgr_to_rgb(pixel):\n    b,g,r=pixel\n    return (r,g,b)','assert bgr_to_rgb((20,80,240))==(240,80,20)\nassert bgr_to_rgb((0,0,0))==(0,0,0)','가운데 G는 유지합니다.','u4-q026'),
(4,'좌표','global_point(origin,local)이 ROI 좌표를 원본 좌표로 바꾸게 만드세요.','def global_point(origin,local):\n    pass','def global_point(origin,local):\n    return (origin[0]+local[0],origin[1]+local[1])','assert global_point((100,50),(20,10))==(120,60)\nassert global_point((0,0),(4,5))==(4,5)','두 좌표는 모두 (x,y)입니다.','u4-q027'),
(4,'계수','counts(names)가 현재 프레임의 클래스별 개수 딕셔너리를 반환하게 만드세요.','def counts(names):\n    pass','def counts(names):\n    result={}\n    for name in names:\n        result[name]=result.get(name,0)+1\n    return result','assert counts(["person","car","person"])=={"person":2,"car":1}\nassert counts([])=={}','매 호출마다 새 딕셔너리를 만듭니다.','u4-q028')]:q(u,topic_name,'구현',p,answer,hint,'조건을 바꾸어 검사하고 반환값의 의미를 설명하세요.',starter=starter,checks=checks,qid=qid)
# One transfer task per topic; model answer remains behind the answer control.
# 2026-09-28 (#131 검토 반영): 옛 u3-q032~044는 '도서 대출 예측'·'과일 그래프'·
# '미로 보상' 등 교과서에 없는 자체 제작 시나리오(later_units.py의 tasks)에 묶여
# 있었다. TRANSFER_ANSWERS를 units[3] 순서와 zip으로 맞추던 방식은 q122(수동 서술
# 문항)이 같은 배치에서 먼저 만들어지며 순서가 한 칸씩 밀리는 버그도 있었다(정답이
# 옆 문항 것으로 붙음). 두 문제를 함께 해결하기 위해 자동 생성·순서 의존 방식을
# 버리고, 소단원마다 교과서 내용에 근거한 서술형을 직접 작성해 id와 답을 1:1로
# 고정한다(순서·개수와 무관하게 항상 올바른 짝을 이룸).
U3_ESSAYS=[
('ml-overview','머신러닝이 비교적 최근에야 널리 쓰이게 된 이유를 데이터·계산 자원·학습 알고리즘의 발전이라는 관점에서 설명하세요.',
 '초기의 규칙 중심 연구는 지식을 사람이 일일이 입력해야 했고 계산 자원의 한계도 있었습니다. 이후 대량의 데이터, 발전한 계산 장치, 개선된 학습 알고리즘이 함께 뒷받침되면서 데이터에서 규칙을 스스로 찾는 머신러닝이 널리 쓰이게 되었습니다.',
 '규칙을 사람이 직접 쓰던 시절의 한계를 먼저 떠올리세요.','데이터·계산 자원·알고리즘 세 가지를 모두 언급했는지 확인하세요.','u3-q132'),
('ml-use','머신러닝을 적용하기에 적합한 문제와, 오히려 일반 프로그램(규칙 기반)이 더 적합한 문제를 예를 들어 구분해 설명하세요.',
 '추천·이미지 분류·음성 처리처럼 복잡한 패턴이 있어 사람이 규칙을 다 적기 어려운 문제에는 머신러닝이 적합합니다. 반대로 사칙연산이나 간단한 유효성 검사처럼 규칙이 이미 명확한 문제는 일반 프로그램이 더 간단하고 정확합니다.',
 '규칙을 사람이 쉽게 다 적을 수 있는지를 기준으로 나누어 보세요.','복잡한 패턴 예시와 명확한 규칙 예시를 각각 하나씩 들었는지 확인하세요.','u3-q133'),
('ml-process','훈련·검증·테스트로 데이터를 나누어야 하는 이유와, 평균·최댓값 같은 전처리 기준을 어느 데이터에서 구해야 하는지 설명하세요.',
 '평가용 데이터를 먼저 따로 떼어 두어야 모델이 한 번도 보지 않은 자료로 공정하게 평가할 수 있습니다. 평균·스케일처럼 데이터에서 배우는 전처리 기준도 훈련 데이터에서만 구해야 하며, 검증으로 모델·설정을 고르고 테스트는 선택을 마친 뒤 마지막에 한 번만 사용합니다.',
 '테스트 데이터의 정보가 학습 과정에 섞이면 안 되는 이유를 생각하세요.','훈련·검증·테스트 세 역할을 모두 구별했는지 확인하세요.','u3-q134'),
('ml-terms','특성(X)과 레이블(y)의 차이를 설명하고, 예측 시점에는 알 수 없는 정보를 X에 포함하면 어떤 문제가 생기는지 설명하세요.',
 'X는 예측 시점에 이미 알 수 있는 입력값들의 표이고, y는 모델이 맞혀야 할 정답입니다. 실제로는 예측 시점에 알 수 없는 값(미래 정답 등)을 X에 넣으면 평가 점수는 높아 보여도 현실에서는 사용할 수 없는 데이터 누수가 되어 잘못된 평가를 하게 됩니다.',
 'X는 언제 알 수 있는 값인지, y는 무엇을 가리키는지 구분하세요.','데이터 누수라는 용어와 그 결과(평가가 부풀려짐)를 모두 적었는지 확인하세요.','u3-q135'),
('ml-methods','지도 학습, 비지도 학습, 강화 학습을 정답(레이블)의 유무와 학습 신호를 기준으로 구분해 설명하세요.',
 '지도 학습은 입력과 정답의 관계를 학습하며 분류·회귀로 나뉩니다. 비지도 학습은 정답 없이 군집처럼 데이터의 구조를 찾습니다. 강화 학습은 정답 대신 에이전트가 상태를 보고 행동한 뒤 받는 보상을 통해 정책을 개선합니다.',
 '정답이 주어지는지, 없는지, 보상으로 대신하는지를 기준으로 나누세요.','세 학습 방식의 이름과 핵심 차이를 모두 적었는지 확인하세요.','u3-q136'),
('ml-libraries','NumPy, pandas, scikit-learn, Matplotlib(또는 Seaborn)이 머신러닝 프로젝트에서 각각 어떤 역할을 하는지 설명하세요.',
 'NumPy는 다차원 배열과 벡터 연산을 담당하고, pandas는 표 형태 데이터를 정리·탐색합니다. scikit-learn은 전처리·학습·평가 도구를 제공하며, Matplotlib과 Seaborn은 그래프로 데이터와 결과를 시각화합니다.',
 '데이터를 다루는 도구와 모델을 다루는 도구, 보여 주는 도구를 구분하세요.','네 도구의 역할을 각각 한 문장으로 적었는지 확인하세요.','u3-q137'),
('ml-preprocess','결측치를 dropna로 제거하는 방법과 fillna(또는 SimpleImputer)로 채우는 방법을 각각 언제 쓰는 것이 적절한지 설명하고, 정규화(MinMaxScaler)와 표준화(StandardScaler)의 차이도 설명하세요.',
 '결측치가 적고 제거해도 데이터의 의미가 크게 바뀌지 않으면 dropna가 간단하지만, 데이터가 적거나 행을 유지해야 하면 평균·중앙값 등으로 채우는 fillna/SimpleImputer가 적합합니다. 정규화는 훈련 데이터의 최솟값·최댓값을 기준으로 값을 0~1 범위로 조정하고, 표준화는 훈련 평균과 표준편차로 변환하며 분포 모양을 정규분포로 만들어 주지는 않습니다.',
 '삭제와 채우기 중 어느 쪽이 정보를 더 보존하는지 생각하세요.','정규화·표준화가 각각 어떤 통계량(최솟값·최댓값 vs 평균·표준편차)을 쓰는지 적었는지 확인하세요.','u3-q138'),
('ml-classification','k-NN 같은 분류 모델에서 하이퍼파라미터(k 값 등)가 작을 때와 클 때 과대 적합·과소 적합이 각각 어떻게 나타날 수 있는지 설명하세요.',
 'k가 너무 작으면 가까운 몇 개의 값에만 민감하게 반응해 훈련 데이터에 지나치게 맞춰지는 과대 적합이 나타날 수 있습니다. 반대로 k가 너무 크면 멀리 있는 값까지 평균에 섞여 패턴을 충분히 학습하지 못하는 과소 적합이 나타날 수 있습니다.',
 'k가 작을수록 개별 데이터에 더 민감해진다는 점을 떠올리세요.','과대 적합과 과소 적합을 각각 k가 작을 때/클 때로 짝지어 설명했는지 확인하세요.','u3-q139'),
('ml-regression','MAE, MSE, R²가 각각 무엇을 나타내며 서로 어떤 차이가 있는지 설명하세요.',
 'MAE는 예측과 실제 값의 차이(오차)의 절댓값 평균으로 원래 단위를 그대로 보여줍니다. MSE는 오차를 제곱해 평균 내므로 큰 오차에 더 큰 벌점을 줍니다. R²는 평균으로 예측하는 단순한 기준과 비교한 값으로 1에 가까울수록 좋고 음수가 될 수도 있습니다.',
 '세 지표가 오차를 계산하는 방식의 차이를 생각하세요.','세 지표의 계산 방식과 좋은 값의 방향(작을수록/클수록)을 모두 적었는지 확인하세요.','u3-q140'),
('ml-cluster','K-평균 군집화에서 군집 개수 K는 누가 정하는지, 그리고 군집 번호가 정답 레이블이 아닌 이유를 설명하세요.',
 'K는 정답이 정해져 있지 않으므로 사용자가 미리 지정해야 하는 하이퍼파라미터입니다. labels_의 군집 번호는 그룹을 구별하기 위한 이름일 뿐이며, 실행 조건(초기화 등)에 따라 같은 그룹이라도 다른 번호가 붙을 수 있어 순위나 정답을 의미하지 않습니다.',
 'K-평균이 비지도 학습이라는 점에서 정답이 있는지 없는지 생각하세요.','K를 정하는 주체와 군집 번호의 의미 두 가지를 모두 설명했는지 확인하세요.','u3-q141'),
('ml-metrics','혼동행렬의 TP·FP·FN·TN을 이용해 정밀도와 재현율이 각각 무엇을 뜻하는지 설명하고, 정밀도가 재현율보다 더 중요한 상황의 예를 드세요.',
 '정밀도는 양성으로 예측한 것 중 실제 양성의 비율(TP/(TP+FP))이고, 재현율은 실제 양성 중 모델이 찾아낸 비율(TP/(TP+FN))입니다. 스팸 분류처럼 정상 메일을 스팸으로 잘못 분류하는 것(FP)의 피해가 클 때는 정밀도가 더 중요합니다.',
 'FP와 FN 중 어느 쪽을 줄이는 것이 더 급한 상황인지 예를 떠올리세요.','정밀도·재현율의 계산식과 정밀도가 중요한 예시를 모두 적었는지 확인하세요.','u3-q142'),
('ml-selection','교차 검증이 한 번의 훈련/검증 분할보다 더 안정적인 평가를 제공하는 이유를 설명하세요.',
 '한 번의 분할은 우연히 쉬운(또는 어려운) 자료가 검증에 몰릴 수 있어 점수가 분할에 따라 크게 달라질 수 있습니다. 교차 검증은 훈련 자료를 여러 묶음으로 나누어 돌아가며 검증에 사용하므로 여러 번의 점수를 평균 내어 더 안정적으로 모델·설정을 비교할 수 있습니다.',
 '한 번만 나누면 그 한 번의 분할 운에 좌우된다는 점을 떠올리세요.','여러 번 나누어 평균을 낸다는 점과 안정성이 좋아지는 이유를 모두 적었는지 확인하세요.','u3-q143'),
('ml-project','학습 곡선에서 훈련 정확도는 높은데 검증 정확도가 낮게 나타났다(과대 적합 의심). 이때 취할 수 있는 조치를 두 가지 이상 설명하세요.',
 '모델의 복잡도를 줄이거나(예: k 늘리기, max_depth 줄이기), 더 많은 훈련 데이터를 모으거나, 정규화(규제) 기법을 적용하거나, 교차 검증으로 설정을 다시 점검하는 방법을 시도할 수 있습니다. 학습 데이터의 정확도를 높이려고 무작정 반복 학습을 늘리는 것은 오히려 과대 적합을 키웁니다.',
 '훈련과 검증 점수의 차이가 클 때 모델을 더 단순하게 만들지, 자료를 더 모을지 생각하세요.','서로 다른 조치 두 가지 이상을 구체적으로 적었는지 확인하세요.','u3-q144'),
]
for topic,prompt,answer,hint,hint2,qid in U3_ESSAYS:
 q(3,topic,'서술',prompt,answer,hint,'개념의 정확성, 구체적인 예, 결과 또는 한계의 근거를 스스로 점검하세요.',ref='교과서 '+next(l for l in units[3] if l['id']==topic)['pages']+' 연계',qid=qid)
# (#138) 확인 학습 84·128쪽·종합 평가 07번 중 원문 그대로 반영되지 않았던 문항을
# 추가한다(교과서 대조 감사). qid는 u3-q145부터 새로 쓴다(기존 최대 u3-q144).
choice5(3,'ml-methods','다음 설명을 읽고 옳은지 판단해 보세요. "머신러닝은 인공지능의 가장 큰 범주에 속하는 기술이다."',
 '틀리다 — 머신러닝은 인공지능의 한 분야이며, 인공지능이 더 넓은 범주이다.',
 ['옳다 — 머신러닝이 가장 넓은 범주이다.','틀리다 — 머신러닝은 인공지능의 한 분야이며, 인공지능이 더 넓은 범주이다.','옳다 — 머신러닝과 인공지능은 같은 크기의 개념이다.','틀리다 — 인공지능과 머신러닝은 서로 무관한 개념이다.','옳다 — 딥러닝이 머신러닝보다 더 넓은 범주이다.'],
 '인공지능이 가장 넓은 개념이고 그 안에 머신러닝, 다시 그 안에 딥러닝이 포함됩니다.',ref='교과서 84쪽 1①·정답 206쪽',qid='u3-q145')
q(3,'ml-methods','서술','\'오늘 날씨를 예측하는 머신러닝 모델\'을 만든다고 가정할 때, 이 모델의 레이블(Label)은 무엇이 될 수 있는지 제시하시오.',
 '기온(섭씨 온도), 강수량(mm), 습도(%), 풍속(km/h) 등',
 '모델이 최종적으로 맞혀야 할 정답이 무엇인지 생각하세요.','예측하려는 날씨 관련 수치를 한 가지 이상 적었는지 확인하세요.',ref='교과서 84쪽 2·정답 206쪽',qid='u3-q146')
choice5(3,'ml-project','다음 설명을 읽고 옳은지 판단해 보세요. "데이터 정규화(Normalization)와 표준화(Standardization)는 데이터의 스케일을 동일하게 조정하여 모델 학습에 도움을 주는 전처리 기법이다."',
 '옳다 — 정규화·표준화는 특성의 스케일을 통일해 모델 학습에 도움을 주는 전처리 기법이다.',
 ['옳다 — 정규화·표준화는 특성의 스케일을 통일해 모델 학습에 도움을 주는 전처리 기법이다.','틀리다 — 정규화·표준화는 결측치를 채우는 기법이다.','틀리다 — 정규화·표준화는 레이블(정답)을 바꾸는 기법이다.','틀리다 — 정규화·표준화는 모델의 하이퍼파라미터를 자동으로 정하는 기법이다.','틀리다 — 정규화·표준화는 훈련·테스트 데이터를 나누는 기법이다.'],
 '정규화는 최솟값·최댓값 기준으로, 표준화는 평균·표준편차 기준으로 스케일을 맞춥니다.',ref='교과서 128쪽 1②·정답 206쪽',qid='u3-q147')
choice5(3,'ml-project','다음 설명을 읽고 옳은지 판단해 보세요. "회귀(Regression) 모델은 주식 가격 예측과 같이 연속적인 값을 예측하는 문제에 주로 사용된다."',
 '옳다 — 회귀는 주가처럼 연속적인 값을 예측하는 문제에 주로 사용된다.',
 ['옳다 — 회귀는 주가처럼 연속적인 값을 예측하는 문제에 주로 사용된다.','틀리다 — 회귀는 스팸/정상처럼 범주를 예측하는 데 사용된다.','틀리다 — 회귀는 군집을 나누는 데 사용된다.','틀리다 — 회귀는 정답이 없는 데이터에서 구조를 찾는 데 사용된다.','틀리다 — 회귀는 이미지 분류에만 사용된다.'],
 '연속적인 숫자 값을 예측하면 회귀, 범주를 예측하면 분류입니다.',ref='교과서 128쪽 1③·정답 206쪽',qid='u3-q148')
q(3,'ml-project','서술','고객을 유사한 그룹으로 나누는 문제(군집화)에서, 이 유형의 대표적인 알고리즘 한 가지와 그 학습 목표를 간략히 설명하시오.',
 'K-평균 군집화(K-means Clustering). 데이터를 여러 개의 중심점(centroid)을 기준으로 나누어, 비슷한 고객끼리 같은 그룹에 속하도록 하는 것이 학습 목표이다. 예를 들어 구매 금액이 많고 방문이 잦은 고객은 \'우수 고객 그룹\', 방문이 드물고 구매가 적은 고객은 \'관심 필요 고객 그룹\'으로 나눌 수 있다.',
 '군집화의 대표 알고리즘 이름을 떠올려 보세요.','알고리즘 이름과 중심점 기준으로 그룹을 나눈다는 학습 목표를 모두 적었는지 확인하세요.',ref='교과서 128쪽 3②·정답 207쪽',qid='u3-q149')
q(3,'ml-project','빈칸','sales_info 딕셔너리로 판다스를 다루는 quiz.py의 일부입니다. 빈칸 ①에 들어갈 코드를 쓰세요.\nimport pandas as ①',
 'pd','pandas를 부를 때 관례적으로 쓰는 짧은 별칭입니다.','import pandas as pd처럼 씁니다.',ref='교과서 131쪽 7①·정답 207쪽',qid='u3-q150')
q(3,'ml-project','빈칸','sales_info 딕셔너리로 판다스를 다루는 quiz.py의 일부입니다. 빈칸 ②에 들어갈 코드를 쓰세요.\nsales_df = pd.②(sales_info)',
 'DataFrame','딕셔너리를 표 형태 자료구조로 바꾸는 pandas 클래스입니다.','pd.DataFrame(sales_info)처럼 씁니다.',ref='교과서 131쪽 7②·정답 207쪽',qid='u3-q151')
for l in units[4]:
 q(4,l['id'],'서술',l['tasks'][0] if l['tasks'] else l['lead'],l['paragraphs'][-1],l['visual'][1][0]+'에서 시작해 입력과 출력을 연결하세요.','개념의 정확성, 구체적인 예, 결과 또는 한계의 근거를 스스로 점검하세요.',ref='교과서 '+l['pages']+' 연계·확장')

# Match each explanation answer to the actual transfer task, not to a generic paragraph.
# 2026-09-28(#131 검토 반영): u3(ml-*) 항목은 위 U3_ESSAYS에서 문항별로 직접 답을
# 지정하므로 더 이상 여기서 쓰지 않는다(u4 cv-* 항목만 아래 zip 로직으로 배정).
TRANSFER_ANSWERS={
'cv-overview':'예: 도서관 빈자리 안내는 좌석 정보를 쉽게 보여 주지만 가방을 사람으로 잘못 찾으면 자리가 틀리게 표시될 수 있습니다. 사람의 신원을 저장하지 않고 오탐과 가림 조건을 시험합니다.',
'cv-pixels':'THRESH_BINARY는 값이 기준보다 클 때만 255입니다. 값 128과 기준 128은 같으므로 검정 0이 됩니다.',
'cv-pipeline':'카메라 입력 → 번호판 영역 검출 → 해당 영역의 문자 인식 → 문자열 결과입니다. 검출은 위치를 찾고 OCR은 글자 내용을 읽으므로 두 단계의 오류를 따로 점검합니다.',
'cv-libraries':'Pillow.size는 (240,160), OpenCV의 3채널 shape는 (160,240,3)입니다. 픽셀은 38400개, 채널 원소는 115200개입니다.',
'cv-io':'260×180 컬러 이미지를 130×90으로 축소하면 픽셀 수는 11700개, 원소 수는 35100개이며 shape는 (90,130,3)입니다.',
'cv-filters':'커널을 3에서 15로 늘리면 잡음뿐 아니라 세부 경계도 더 흐려질 수 있습니다. 고정 이진화 기준을 80에서 180으로 올리면 흰색으로 남는 픽셀은 줄거나 같습니다.',
'cv-transform':'두 대응 목록에서 한쪽만 순서를 바꾸면 잘못된 꼭짓점으로 매핑되어 결과가 뒤틀리거나 뒤집힐 수 있습니다. 양쪽을 왼쪽 위부터 같은 방향으로 맞춥니다.',
'cv-features':'네모의 꼭짓점은 여러 방향의 변화가 강해 코너로 잡히기 쉽습니다. 원의 곡선은 설정과 해상도에 따라 코너가 적거나 다르게 잡힙니다. 결과 개수는 고정 정답이 아니므로 그림과 조건을 함께 기록합니다.',
'cv-haar':'같은 사진에서 minNeighbors=3,5,7로 실행하고 실제 얼굴 수·검출 수·오탐 수·누락 수를 표로 비교합니다. 더 엄격한 기준은 오탐을 줄일 수 있지만 실제 얼굴을 놓칠 수도 있습니다.',
'cv-yolo':'같은 이미지에서 conf=0.3과 0.7을 비교합니다. 기준을 높이면 낮은 점수의 후보가 제외되어 검출 수가 줄 수 있고, 오탐 감소와 실제 객체 누락을 함께 확인해야 합니다.',
'cv-project':'이미지 열기 버튼 → 입력 경로 확인 → 별도 처리 모듈의 함수 호출 → 결과 미리보기 → 저장 버튼으로 구성합니다. GUI 이벤트 코드와 배열 처리 코드를 분리하고 취소·잘못된 경로도 처리합니다.'}
for u in [4]:
 written=[item for item in __import__('content').questions if item['unit']==u and item['kind']=='서술']
 for item,l in zip(written,units[u]):item['answer']=TRANSFER_ANSWERS[l['id']]

# Keep classroom browser activities small; full scientific pipelines remain PC examples.
for id,e in examples.items():
 if id.startswith('ml-') and 'scikit-learn' in e['files'].get('requirements.txt',''):
  e['mode']='pc'
  e['note']='전체 scikit-learn 모델은 PC에서 실행합니다. 브라우저에서는 연결된 원리 실습으로 입력·계산·결과를 먼저 확인하세요. '+e['note']
def browser_example(topic_id,id,title,source,checks):
 example(id,title,source,checks=checks,note='작은 데이터로 핵심 원리를 직접 계산합니다. scikit-learn API 실행과 구별되는 학습용 구현입니다.')
 next(l for l in units[3] if l['id']==topic_id)['examples'].insert(0,id)
browser_example('ml-process','ml-split-small','웹 원리 · 훈련·검증·테스트 분할','''import random
samples = list(range(10))
random.Random(42).shuffle(samples)
train, validation, test = samples[:6], samples[6:8], samples[8:]
print("Training:", train)
print("Validation:", validation)
print("Test:", test)
''','assert len(train)==6 and len(test)==2\nassert not (set(train)&set(test))\nassert len(set(train+validation+test))==10')
browser_example('ml-preprocess','ml-scale-small','웹 원리 · 훈련 평균과 스케일','''import math
train = [10, 20, 30]
test = [50]
mean = sum(train)/len(train)
std = math.sqrt(sum((v-mean)**2 for v in train)/len(train))
low, high = min(train), max(train)
def standardize(v):
    return (v-mean)/std if std else 0
def normalize(v):
    return (v-low)/(high-low) if high!=low else 0
print("Training mean:",mean)
print("Training standardized:",[round(standardize(v),3) for v in train])
print("Test standardized:",[round(standardize(v),3) for v in test])
print("Test normalized:",[normalize(v) for v in test])
''','assert mean==20\nassert normalize(50)==2\nassert standardize(20)==0')
browser_example('ml-classification','ml-knn-small','웹 원리 · 가까운 이웃으로 분류','''from collections import Counter
# 입력값과 클래스가 있는 작은 학습 자료입니다.
training = [(1,"A"),(2,"A"),(4,"B"),(5,"B"),(8,"B")]
x = 3.5
k = 3
neighbors = sorted(training,key=lambda row:abs(row[0]-x))[:k]
prediction = Counter(label for _,label in neighbors).most_common(1)[0][0]
print("Input:",x,"k:",k)
print("Neighbors:",neighbors)
print("Prediction:",prediction)
''','assert len(neighbors)==3\nassert prediction=="B"')
browser_example('ml-regression','ml-line-small','웹 원리 · 최소제곱 직선 학습','''x = [1,2,3,4]
y = [3,5,7,9]
mx,my = sum(x)/len(x),sum(y)/len(y)
w = sum((a-mx)*(b-my) for a,b in zip(x,y))/sum((a-mx)**2 for a in x)
b = my-w*mx
pred = [w*a+b for a in x]
mae = sum(abs(a-p) for a,p in zip(y,pred))/len(y)
print("Learned w, b:",w,b)
print("Prediction at 5:",w*5+b)
print("Training MAE:",mae)
# 훈련 오차 0이 새 데이터에서의 정확성을 보장하지는 않습니다.
''','assert w==2 and b==1\nassert w*5+b==11\nassert mae==0')
browser_example('ml-cluster','ml-kmeans-small','웹 원리 · 군집 중심의 반복 갱신','''values = [1,2,3,8,9,10]
centers = [1.,8.]
for step in range(4):
    groups = [[],[]]
    for value in values:
        index = min(range(2),key=lambda i:abs(value-centers[i]))
        groups[index].append(value)
    new_centers = [sum(group)/len(group) if group else centers[i] for i,group in enumerate(groups)]
    print("Step",step,"groups:",groups,"centers:",new_centers)
    if new_centers == centers:
        break
    centers = new_centers
''','assert centers==[2.,9.]\nassert groups==[[1,2,3],[8,9,10]]')
browser_example('ml-metrics','ml-confusion-small','웹 원리 · 혼동행렬 직접 계산','''truth = [1,0,1,1,0,0]
probability = [.9,.8,.6,.4,.3,.1]
threshold = .5
pred = [int(p>=threshold) for p in probability]
tp = sum(a==1 and b==1 for a,b in zip(truth,pred))
fp = sum(a==0 and b==1 for a,b in zip(truth,pred))
fn = sum(a==1 and b==0 for a,b in zip(truth,pred))
tn = sum(a==0 and b==0 for a,b in zip(truth,pred))
precision = tp/(tp+fp) if tp+fp else None
recall = tp/(tp+fn) if tp+fn else None
print("TP FP FN TN:",tp,fp,fn,tn)
print("Precision:",precision,"Recall:",recall)
''','assert (tp,fp,fn,tn)==(2,1,1,2)\nassert len(pred)==len(truth)')
browser_example('ml-selection','ml-cv-small','웹 원리 · 교차 검증의 역할 바꾸기','''samples = list(range(9))
folds = [samples[i:i+3] for i in range(0,9,3)]
for i, validation in enumerate(folds):
    training = [v for j,fold in enumerate(folds) if j!=i for v in fold]
    print("Fold",i,"train:",training,"validation:",validation)
    assert not set(training)&set(validation)
print("최종 테스트 자료는 이 묶음들과 별도로 보관합니다.")
''','assert len(folds)==3\nassert sorted(v for fold in folds for v in fold)==samples')
import unit3_density
import unit3_pre_api
import unit3_tips
# (#131 C) 3단원은 PPT 슬라이드 기반 deck_lesson_section으로 렌더링해 pre_api·tips·
# lesson['examples'] 슬롯을 쓰지 않는다(verify.py의 같은 취지 주석 참고). 이 세 모듈의
# apply()는 이제 존재하지 않는 예제 id(ml-tools 등, 교과서 코드로 교체되며 이름이
# 바뀌거나 나뉨)를 참조해 빌드가 깨지므로 호출하지 않는다. 모듈 자체는 하위 호환을
# 위해 import만 하고(최상위 ex() 정의는 그대로 등록됨), apply()는 건너뛴다.
import unit4_density
import unit4_pre_api
import unit4_tips
unit4_density.apply()
unit4_pre_api.apply()
unit4_tips.apply()

# 모든 문항 생성이 끝난 뒤(content.py·questions.py·later_units.py) topic을
# 실제 소단원 id로 정리한다(#116). id·순서·지문은 그대로 두고 topic만 바꾼다.
import content
import question_topics
question_topics.apply(content.questions)
