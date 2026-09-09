"""Units III and IV: textbook concepts, runnable reworked examples and visual summaries."""
from content import units,examples,lesson,ex,q
units.update({3:[],4:[]})
def topic(u,id,title,pages,lead,paragraphs,steps,headers,rows,ids=(),tasks=()):
 lesson(u,id,title,pages,lead,paragraphs,ids,tasks)
 units[u][-1]['visual']=(title+' · 한눈에 보기',steps,headers,rows)
def example(id,title,src,packages='',mode='web',files=None,checks='',note=''):
 data={'main.py':src,**(files or {})}
 if packages:data['requirements.txt']=packages.replace(' ',',') .replace(',','\n')+'\n'
 ex(id,title,data,mode=mode,checks=checks,note=note)

# III. Concepts: explicitly separate data, learned parameters and chosen settings.
topic(3,'ml-overview','AI·머신러닝·딥러닝의 관계','62–67','규칙을 직접 쓰는 것과 데이터에서 규칙을 배우는 것은 어떻게 다를까요?',[
'인공지능은 지능적인 문제 해결 기술의 넓은 범위입니다. 머신러닝은 데이터에서 패턴을 학습하는 접근이며, 딥러닝은 여러 층의 신경망을 사용하는 머신러닝의 한 종류입니다. 모든 AI가 머신러닝인 것은 아닙니다.',
'초기의 규칙 중심 연구는 지식 입력과 계산 자원의 한계를 겪었습니다. 이후 데이터·계산 장치·학습 알고리즘의 발전이 함께 영향을 주었습니다. 1956년 다트머스 워크숍, 1997년 딥 블루의 체스 승리, 2012년 ImageNet의 딥러닝 성과는 서로 다른 접근의 발전 사례입니다. 딥 블루를 현대 딥러닝 모델과 같은 것으로 보지 마세요.'],['인공지능｜가장 넓은 범위','머신러닝｜데이터로 학습','딥러닝｜여러 층의 신경망'],['접근','규칙의 출처','예'],[['규칙 기반','사람이 조건 작성','비밀번호 길이 검사'],['머신러닝','데이터와 학습 알고리즘','스팸 분류'],['딥러닝','다층 신경망의 학습','이미지 특징 학습']],tasks=['주변의 AI 서비스 하나에서 입력과 출력을 찾아 설명하세요.'])
topic(3,'ml-use','머신러닝이 필요한 문제와 활용','68–70','정확한 규칙을 쓰기 어려운 문제를 찾아보세요.',[
'추천, 이미지 분류, 음성 처리처럼 복잡한 패턴이 있는 문제에서 머신러닝을 활용합니다. 규칙이 명확한 사칙연산이나 간단한 유효성 검사에는 일반 프로그램이 더 간단할 수 있습니다.',
'학습 데이터가 현실을 충분히 대표하지 않으면 특정 조건에서 오류가 늘어납니다. 예측을 사실로 단정하지 말고, 데이터의 범위·오류 비용·사람의 확인 절차를 함께 설명하세요.'],['문제 찾기','입력 데이터 정하기','예측할 출력 정하기','오류가 미칠 영향 점검'],['서비스','입력','예측'],[['추천','이용 기록·항목 특성','선호 가능성'],['제조 검사','제품 이미지','정상/결함'],['대출량 예상','과거 대출·요일','예상 권수']],tasks=['학교 도서 대출량을 예측한다면 어떤 데이터를 모을지 표로 적으세요.'])
topic(3,'ml-process','문제 해결 과정과 데이터 분할','71–75, 101–102','모델을 만들기 전에 성공 기준을 정하세요.',[
'문제 정의 → 수집·탐색 → 전처리 → 모델 선택 → 학습·평가 → 해석·응용으로 진행합니다. 실제 프로젝트에서는 결과를 보고 앞 단계로 돌아가 수정하기도 합니다.',
'평가용 데이터는 먼저 분리해 둡니다. 평균·스케일·범주 목록처럼 데이터에서 배우는 전처리 값도 훈련 부분에서만 구합니다. 모델 후보는 검증 데이터나 교차 검증으로 비교하고, 최종 테스트는 선택을 마친 뒤 사용합니다.'],['문제·성공 기준','수집·탐색','훈련/테스트 분할','전처리·학습·검증','최종 평가·해석'],['분할','역할','금지할 일'],[['훈련','전처리 값·모델 학습','정답을 입력 특성에 포함'],['검증','모델·설정 선택','최종 테스트로 반복 선택'],['테스트','선택 완료 후 최종 확인','fit / fit_transform 호출']],tasks=['도서 대출 예측의 성공 기준을 평균 오차로 표현해 보세요.'])
topic(3,'ml-terms','특성·레이블·모델·하이퍼파라미터','76–78','표의 어느 열을 X로, 어느 열을 y로 사용할까요?',[
'데이터 세트의 한 행은 보통 한 관측입니다. X는 예측 시점에 알 수 있는 특성의 표이며 y는 예측할 정답입니다. 샘플 수와 특성 수를 확인하고 같은 행의 X와 y가 대응하는지 검사합니다.',
'모델은 학습한 예측 규칙입니다. 가중치 같은 파라미터는 학습 과정에서 정해지고, k-NN의 k 같은 하이퍼파라미터는 학습 전에 설정합니다. 훈련 성능만 좋고 검증 성능이 낮으면 과대 적합, 둘 다 낮으면 과소 적합을 의심합니다.'],['행｜샘플 1개','입력 열 X｜특성 여러 개','정답 열 y｜레이블','fit → predict｜학습 후 예측'],['기호','도서 예','형태'],[['X','요일·최근 대출 수','(샘플 수, 특성 수)'],['y','다음 날 대출 수','(샘플 수,)'],['하이퍼파라미터','트리의 최대 깊이','학습 전에 선택']],tasks=['미래 대출 수를 특성에 넣으면 왜 잘못된 평가가 되는지 설명하세요.'])
topic(3,'ml-methods','지도·비지도·강화 학습','79–84','정답을 배우나요, 구조를 찾나요, 행동의 보상을 배우나요?',[
'지도 학습은 입력과 정답의 관계를 학습합니다. 범주를 예측하면 분류, 연속적인 수치를 예측하면 회귀입니다. 비지도 학습은 정답 없이 군집이나 낮은 차원의 구조를 찾습니다.',
'강화 학습에서는 에이전트가 상태를 보고 행동하며 환경에서 보상을 받습니다. 정책은 행동 선택 전략이고 장기 누적 보상을 높이는 방향으로 배웁니다. Q-learning은 여러 강화 학습 알고리즘 중 하나입니다.'],['정답 있음｜지도 학습','정답 없음｜비지도 학습','상태·행동·보상｜강화 학습'],['유형','목표','예'],[['분류','범주 예측','스팸 여부'],['회귀','수치 예측','내일 기온'],['군집','유사한 데이터 묶기','고객 그룹'],['강화','행동 전략 학습','미로에서 탈출']],tasks=['미로 탈출에 보상을 설계하고 반복 제자리 움직임을 막는 방법을 설명하세요.'])
example('ml-tools','NumPy·pandas로 표 탐색하기','''import numpy as np
import pandas as pd
values = np.array([10, 20, 30])
print(values + 5)
print(np.concatenate(([1, 2], [3, 4])))
df = pd.DataFrame({"name": ["A", "B", "C"], "score": [75, 90, 85]})
print(df.head())
print(df.describe())
df.info()
''','numpy pandas',checks='assert df.shape == (3, 2)')
example('ml-chart','빈도표를 막대그래프로','''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter
counts = Counter(["apple", "banana", "apple", "pear", "banana", "apple"])
plt.bar(list(counts), list(counts.values()))
plt.ylabel("Count")
plt.title("Fruit frequency")
plt.savefig("frequency.png")
print(dict(counts))
''','matplotlib',note='실제 Python이 저장한 PNG를 실행 결과 아래에서 확인할 수 있습니다.')
example('ml-seaborn','Seaborn countplot과 Excel 입출력','''import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
frame = pd.DataFrame({"fruit": ["apple", "banana", "apple"]})
frame.to_excel("fruit.xlsx", index=False)
print(pd.read_excel("fruit.xlsx").head())
sns.countplot(data=frame, x="fruit")
plt.savefig("fruit.png")
''','pandas seaborn matplotlib openpyxl',mode='pc',note='Excel 입출력과 seaborn 비교 예제입니다. python -m pip install -r requirements.txt 후 PC에서 실행하세요.')
topic(3,'ml-libraries','머신러닝 라이브러리와 그래프','85–89','배열·표·모델·그래프 도구를 연결해 보세요.',[
'NumPy는 다차원 배열과 벡터 연산, pandas는 Series·DataFrame과 표 탐색, scikit-learn은 전처리·학습·평가 도구를 제공합니다. Matplotlib은 그래프 구성, Seaborn은 표 데이터의 통계 시각화를 돕습니다.',
'웹에서는 NumPy·pandas·그래프와 작은 원리 실습을 실행합니다. scikit-learn 전체 파이프라인은 PC에서 실행합니다. 필요한 웹 패키지는 처음에 내려받습니다. 실행한 Python이 만든 PNG 그래프는 결과 아래에 표시됩니다. PC에서는 예제 폴더에서 requirements.txt를 설치합니다.'],['NumPy｜배열','pandas｜표 정리','scikit-learn｜학습·평가','Matplotlib / Seaborn｜시각화'],['확인','코드','의미'],[['앞부분','df.head()','표의 실제 값'],['구조','df.info()','자료형·결측 개수'],['통계','df.describe()','수치 분포'],['배열 크기','array.shape','축별 길이']],['ml-tools','ml-chart','ml-seaborn'],['과일 종류와 개수를 바꾸고 그래프가 바뀌는지 확인하세요.'])
example('ml-clean','CSV·결측치·이상치 탐색','''import pandas as pd
frame = pd.read_csv("scores.csv")
print(frame.head())
print("Missing:", frame.isna().sum())
print("Drop missing:", frame.dropna())
# 이 예제는 탐색용 표입니다. 예측 모델에서는 분할 후 훈련 데이터로 통계량을 구합니다.
median = frame["score"].median()
filled = frame.fillna({"name": "Unknown", "score": median})
print("Filled:", filled)
print("Outside score range:", filled[(filled.score < 0) | (filled.score > 100)])
''','pandas',files={'scores.csv':'name,score\nA,80\nB,\n,90\nD,1000\n'},checks='assert filled.isna().sum().sum() == 0')
example('ml-scale','훈련 데이터로만 전처리 배우기','''import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
train = np.array([[10., 1.], [20., np.nan], [30., 3.]])
test = np.array([[50., 2.]])
imputer = SimpleImputer(strategy="median")
train_filled = imputer.fit_transform(train)
test_filled = imputer.transform(test)
for scaler in [MinMaxScaler(), StandardScaler()]:
    print(type(scaler).__name__)
    print(scaler.fit_transform(train_filled))
    print("Test:", scaler.transform(test_filled))
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
print(encoder.fit_transform([["Seoul"], ["Busan"], ["Seoul"]]))
print("Unseen city:", encoder.transform([["Jeju"]]))
''','numpy scikit-learn',checks='assert test_filled.shape == (1, 2)')
topic(3,'ml-preprocess','결측치·이상치·스케일·범주 처리','90–100','값을 바꾼 이유와 기준을 남겨 보세요.',[
'CSV는 read_csv, Excel은 read_excel로 읽습니다. 결측치는 isna로 확인한 뒤 dropna로 제거하거나 fillna·SimpleImputer로 채울 수 있습니다. 이상치는 입력 오류인지 드문 정상 관측인지 먼저 확인합니다. 임의 삭제는 데이터의 의미를 바꿀 수 있습니다.',
'MinMaxScaler는 훈련 범위를 기준으로 값을 조정하며 새로운 값은 0~1 범위를 벗어날 수 있습니다. StandardScaler는 훈련 평균과 표준편차로 변환하지만 정규분포를 만들어 주지는 않습니다. 범주형 값에는 get_dummies 또는 OneHotEncoder를 사용하며 새 범주 처리 기준도 정합니다.'],['불러오기·자료형 확인','분할 후 훈련 부분 탐색','결측·이상치 처리 기준','수치 스케일·범주 인코딩','테스트에는 transform'],['처리','배우는 기준','확인'],[['결측 채우기','훈련 중앙값 등','누락 의미 보존'],['정규화','훈련 최소·최대','새 값은 범위 밖 가능'],['표준화','훈련 평균·표준편차','분포 모양 보장 안 함'],['원-핫','훈련 범주 목록','알 수 없는 범주 대응']],['ml-clean','ml-scale'],['1000점이 실제 값인지 입력 실수인지 확인할 질문을 적으세요.'])
example('ml-classify','붓꽃 분류 모델 네 가지 비교','''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
models = [KNeighborsClassifier(5), LogisticRegression(max_iter=1000), DecisionTreeClassifier(max_depth=3, random_state=42), SVC()]
for model in models:
    pipe = make_pipeline(StandardScaler(), model)
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    print(type(model).__name__, round(accuracy_score(y_test, pred), 3))
# 이 비교는 관찰용입니다. 실제 모델 선택은 훈련 부분의 교차 검증으로 합니다.
''','scikit-learn',checks='assert len(pred) == len(y_test)')
topic(3,'ml-classification','분류: k-NN·로지스틱·트리·SVM','103–105','이름에 회귀가 들어 있어도 범주를 예측하는 모델이 있어요.',[
'k-NN은 가까운 이웃들의 정답을 참고합니다. 로지스틱 회귀는 분류에 사용하는 모델이고, 결정 트리는 조건으로 데이터를 나누며, SVM은 범주 사이의 경계를 학습합니다.',
'붓꽃 예제에서 X는 꽃받침·꽃잎의 측정값이고 y는 품종입니다. stratify=y는 분할 시 클래스 비율을 고려합니다. k-NN·SVM 등은 거리나 스케일의 영향을 받으므로 전처리를 파이프라인 안에서 학습합니다.'],['붓꽃 X,y','분할','스케일 + 분류기 fit','새 X로 predict','정답과 비교'],['알고리즘','핵심','조절값 예'],[['k-NN','가까운 이웃','n_neighbors'],['로지스틱','클래스 확률','C'],['결정 트리','조건 분기','max_depth'],['SVM','분리 경계','C / kernel']],['ml-classify'],['k를 3과 7로 바꾸고 같은 분할에서 결과를 비교하세요.'])
example('ml-regression','회귀 예측과 MAE·MSE·R²','''from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)
print("Train R2:", model.score(X_train, y_train))
print("Test MAE:", mean_absolute_error(y_test, pred))
print("Test MSE:", mean_squared_error(y_test, pred))
print("Test R2:", r2_score(y_test, pred))
''','scikit-learn',checks='assert mean_absolute_error(y_test, pred) >= 0',note='내장 자료로 회귀 원리를 연습하는 예제이며 실제 개인에 대한 예측 용도로 사용하지 않습니다.')
example('ml-housing','교과서 연결 · 주택 자료 회귀','''from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
pred = LinearRegression().fit(X_train, y_train).predict(X_test)
print("MAE", mean_absolute_error(y_test, pred))
print("MSE", mean_squared_error(y_test, pred))
print("R2", r2_score(y_test, pred))
''','scikit-learn',mode='pc',note='첫 실행에 외부 데이터 다운로드가 필요합니다. 네트워크가 없으면 내장 자료 회귀 예제를 사용하세요.')
topic(3,'ml-regression','회귀와 수치 오차','106–107, 121–123','예측 숫자는 정답에서 얼마나 떨어져 있나요?',[
'회귀는 연속적인 목표값을 예측합니다. 선형 회귀는 특성들의 가중합과 절편으로 값을 예측합니다. 예측한 값과 실제 값의 차이를 잔차라고 부릅니다.',
'MAE는 절대 오차 평균, MSE는 제곱 오차 평균입니다. MSE는 큰 오차에 더 큰 벌점을 줍니다. R²는 평균 예측 기준과 비교한 값으로 음수가 될 수 있습니다. 한 지표의 숫자만 보지 말고 목표값의 단위와 오류 사례도 확인하세요.'],['입력 특성','가중합 + 절편','예측 숫자','정답과 오차 계산'],['지표','작을수록?','의미'],[['MAE','좋음','원래 목표값 단위'],['MSE','좋음','큰 오차를 강하게 반영'],['R²','클수록 좋음','0은 평균 기준, 음수 가능']],['ml-regression','ml-housing'],['기울기 실험에서 MSE가 가장 작은 위치를 찾으세요.'])
example('ml-cluster','군집 중심과 산점도','''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
X, _ = make_blobs(n_samples=120, centers=3, random_state=42, cluster_std=0.7)
model = KMeans(n_clusters=3, n_init=10, random_state=42)
labels = model.fit_predict(X)
centers = model.cluster_centers_
print("Centers:", centers)
plt.scatter(X[:, 0], X[:, 1], c=labels)
plt.scatter(centers[:, 0], centers[:, 1], marker="X", s=180, c="red")
plt.title("K-means: groups and centers")
plt.savefig("clusters.png")
''','scikit-learn matplotlib',checks='assert len(set(labels)) == 3')
topic(3,'ml-cluster','K-평균 군집화','108–111','정답 이름 없이 비슷한 점들을 묶을 수 있을까요?',[
'K-평균은 정한 개수 K의 중심을 이용해 가까운 샘플들을 묶고 중심을 갱신합니다. labels_의 번호는 정답 클래스나 순위가 아니며 실행 조건에 따라 번호가 달라질 수 있습니다.',
'데이터의 스케일, K, 초기 중심이 결과에 영향을 줍니다. n_init은 여러 초기화 시도를 제어합니다. 점들의 분포를 보고 군집이 의미 있는지 해석하며, 항상 원형 군집이 존재한다고 가정하지 마세요.'],['K개 중심 초기화','가장 가까운 중심에 배정','그룹 평균으로 중심 갱신','수렴까지 반복'],['속성','의미'],[['labels_','샘플별 군집 번호'],['cluster_centers_','군집 중심 좌표'],['n_clusters','미리 정하는 그룹 수'],['random_state / n_init','재현 조건 / 초기화 반복']],['ml-cluster'],['K를 2·3·4로 바꾸고 중심 위치와 군집의 의미를 비교하세요.'])
example('ml-metrics','혼동행렬과 분류 지표','''from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
y_true = [1, 0, 1, 1, 0, 0]
y_pred = [1, 1, 1, 0, 0, 0]
print("rows=true, columns=predicted; labels=[0,1]")
print(confusion_matrix(y_true, y_pred, labels=[0, 1]))
for metric in [accuracy_score, precision_score, recall_score, f1_score]:
    print(metric.__name__, metric(y_true, y_pred))
''','scikit-learn',checks='assert confusion_matrix(y_true, y_pred).tolist() == [[2,1],[1,2]]')
topic(3,'ml-metrics','혼동행렬·정확도·정밀도·재현율','117–120','어떤 종류의 실수가 더 중요한가요?',[
'양성으로 삼는 클래스를 먼저 정합니다. TP는 실제 양성을 양성으로, TN은 실제 음성을 음성으로 맞힌 수입니다. FP는 음성을 양성으로, FN은 양성을 음성으로 틀린 수입니다.',
'정확도는 전체 정답 비율입니다. 정밀도는 양성 예측 중 실제 양성의 비율, 재현율은 실제 양성 중 찾아낸 비율입니다. F1은 정밀도와 재현율의 조화평균입니다. 클래스 불균형이 있으면 정확도만으로 비교하기 어렵습니다.'],['양성 의미 정하기','예측 임계값 선택','TP·FP·FN·TN 세기','목표에 맞는 지표 해석'],['지표','계산','질문'],[['정확도','(TP+TN)/전체','전체에서 얼마나 맞혔나?'],['정밀도','TP/(TP+FP)','양성이라고 한 것 중 맞은 비율?'],['재현율','TP/(TP+FN)','실제 양성 중 찾은 비율?'],['F1','2PR/(P+R)','두 지표의 균형은?']],['ml-metrics'],['임계값을 올릴 때 FP와 FN이 어떻게 달라지는지 관찰하세요.'])
example('ml-selection','교차 검증과 GridSearchCV','''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
pipe = make_pipeline(StandardScaler(), KNeighborsClassifier())
print("CV:", cross_val_score(pipe, X_train, y_train, cv=3))
search = GridSearchCV(pipe, {"kneighborsclassifier__n_neighbors": [3, 5, 7]}, cv=3, scoring="accuracy", n_jobs=1)
search.fit(X_train, y_train)
print("Best:", search.best_params_, search.best_score_)
print("Final test:", search.score(X_test, y_test))
''','scikit-learn',checks='assert search.best_params_["kneighborsclassifier__n_neighbors"] in [3,5,7]')
example('ml-learning-curve','학습 곡선으로 과대·과소 적합 살펴보기','''import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import learning_curve, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
X, y = load_iris(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
cv = StratifiedKFold(3, shuffle=True, random_state=42)
sizes, train, valid = learning_curve(model, X, y, train_sizes=[0.4, 0.7, 1.0], cv=cv, shuffle=True, random_state=42, n_jobs=1)
plt.plot(sizes, train.mean(axis=1), "o-", label="Training")
plt.plot(sizes, valid.mean(axis=1), "s--", label="Validation")
plt.xlabel("Training samples")
plt.ylabel("Accuracy")
plt.legend()
plt.savefig("learning-curve.png")
print("Sizes:", sizes)
print("Validation:", np.round(valid.mean(axis=1), 3))
''','numpy scikit-learn matplotlib',checks='assert len(sizes)==3')
topic(3,'ml-selection','교차 검증·튜닝·학습 곡선','112–116, 124–128','한 번 나눈 점수만으로 모델을 선택해도 될까요?',[
'교차 검증은 훈련 자료를 여러 묶음으로 나누어 검증 역할을 번갈아 맡깁니다. GridSearchCV는 설정 후보를 교차 검증으로 비교합니다. 전처리도 각 훈련 묶음에서 다시 학습하도록 Pipeline을 사용합니다.',
'학습 곡선은 훈련 샘플 수에 따른 훈련·검증 성능을 함께 보여 줍니다. 두 곡선의 간격과 수준을 보고 데이터 추가, 모델 복잡도 조절, 규제, 특성 개선 등을 검토합니다. 데이터 스케일 정규화와 모델 규제(regularization)는 다른 개념입니다.'],['최종 테스트 별도 보관','훈련 부분에서 교차 검증','GridSearchCV로 설정 선택','학습 곡선·오류 분석','테스트 한 번 평가'],['관찰','가능한 해석','다음 실험'],[['훈련↑ 검증↓','과대 적합','복잡도 감소·자료 추가'],['훈련↓ 검증↓','과소 적합','특성·모델 개선'],['분할마다 점수 차이','불안정한 추정','평균·편차 함께 보고']],['ml-selection','ml-learning-curve'],['best_score_와 최종 테스트 점수가 다른 이유를 설명하세요.'])
topic(3,'ml-project','모델 구현·평가 프로젝트와 단원 정리','129–131 + 확장','입력부터 결과 설명까지 재현 가능한 보고서를 만드세요.',[
'문제와 목표값, 데이터 출처, 특성, 분할 조건, 전처리, 모델, 평가 결과를 한 흐름으로 연결하세요. 비교 대상과 난수 조건을 기록하고, 점수가 낮아진 사례를 찾아 개선안을 제안합니다.',
'스팸 분류의 FP와 정밀도, 가격 같은 수치 예측과 회귀, 정답 없는 고객 군집, AI 포함 관계, 과대 적합 방지, DataFrame.describe를 모두 설명할 수 있는지 확인하세요.'],['문제·데이터 카드','분할·전처리 코드','모델 비교·선택','최종 지표·한계','저널·코드 제출'],['산출물','포함할 것'],[['실행 코드','재현 조건과 패키지'],['결과 표','훈련·검증·테스트 역할'],['해석','오류 사례와 개선 근거']],['ml-selection'],['같은 파이프라인에서 k 후보 하나를 추가하고 선택 근거를 기록하세요.'])

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
for topic_name,prompt,answer,other,explain,ref in [
('AI 관계','올바른 포함 관계는?','AI ⊃ 머신러닝 ⊃ 딥러닝','딥러닝 ⊃ AI ⊃ 머신러닝','AI가 가장 넓고 딥러닝은 ML의 일부입니다.','교과서 129쪽 3'),
('학습 방식','레이블 없이 데이터의 비슷한 구조를 찾는 학습은?','비지도 학습','지도 학습','정답 없이 패턴을 찾는 것은 비지도 학습입니다.','교과서 84쪽 1③'),
('학습 방식','예측할 값이 내일의 기온이라면 주된 문제 유형은?','회귀','분류','연속적인 수치를 예측합니다.','교과서 84쪽 2'),
('학습 방식','보상에 따라 미로의 행동 전략을 배우는 방식은?','강화 학습','군집화','상태·행동·보상·정책을 구별합니다.','교과서 84쪽 3'),
('군집','정답 없이 고객을 구매 특성별로 묶는 도구는?','KMeans','LinearRegression','유사한 고객 그룹의 중심을 찾습니다.','교과서 128쪽 3'),
('특성','예측 시점에는 알 수 없는 미래 정답 열을 X에 넣으면?','데이터 누수','항상 더 좋은 모델','현실 예측 때 없는 정보를 쓰면 평가가 부풀려집니다.','보강'),
('전처리','StandardScaler.fit을 적용할 데이터는?','훈련 데이터','테스트 포함 전체 데이터','평균과 표준편차도 훈련 부분에서만 구합니다.','교과서 128쪽 2 보완'),
('pandas','문자열 열을 DataFrame에 담을 수 있나요?','가능하다','불가능하다','DataFrame은 수치형과 문자열 등 여러 자료형을 담습니다.','교과서 128쪽 1①'),
('분류','중요한 정상 메일을 스팸으로 잘못 보내는 경우를 줄일 때 주목할 지표는?','정밀도','R²','스팸을 양성으로 두면 잘못 스팸 처리한 것은 FP입니다.','교과서 129쪽 1'),
('과대 적합','훈련 점수만 높이려고 지나치게 반복 학습하면?','과대 적합 위험이 커질 수 있다','일반화가 항상 좋아진다','새 데이터의 성능을 함께 확인해야 합니다.','교과서 130쪽 4'),
('분류','분류 문제에 해당하는 것은?','이메일 스팸 여부','내일 기온 수치','분류는 범주를 예측합니다.','교과서 130쪽 5'),
('알고리즘','지도 학습 알고리즘이 아닌 것은?','KMeans','KNeighborsClassifier','KMeans는 비지도 군집화입니다.','교과서 130쪽 6'),
('전처리','정규화 후 새 데이터의 값이 1.4가 나올 수 있나요?','가능하다','절대로 불가능하다','훈련 최댓값을 넘으면 1보다 커질 수 있습니다.','보강'),
('용어','k-NN의 n_neighbors는 무엇인가요?','하이퍼파라미터','레이블','학습 전에 정하는 설정입니다.','교과서 78쪽'),
('평가','최종 테스트 점수를 보고 k를 계속 고르면?','테스트가 모델 선택에 사용된다','독립적인 최종 평가가 유지된다','검증을 통해 선택하고 테스트는 마지막에 씁니다.','보강'),
('회귀','R²는 음수가 될 수 있나요?','가능하다','항상 0 이상이다','평균 예측보다 오차가 크면 음수가 될 수 있습니다.','교과서 121–123쪽'),
('군집','군집 번호 2는 번호 1보다 더 좋은 그룹인가요?','번호에 우열 의미가 없다','항상 더 좋은 그룹이다','번호는 그룹 식별용입니다.','교과서 108–111쪽'),
('평가','정확도·정밀도·재현율은 주로 어떤 모델에 쓰나요?','분류','회귀','범주 예측과 실제 정답을 비교합니다.','교과서 84쪽 1②')]:choice(3,topic_name,prompt,answer,[answer,other],explain,ref)
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
for u,topic_name,p,a,e,ref in [
(3,'pandas','import pandas as ____','pd','관례적인 별칭입니다.','교과서 131쪽 7①'),
(3,'pandas','pd.____(sales_info)로 표를 만듭니다.','DataFrame','열 이름과 값으로 표를 구성합니다.','교과서 131쪽 7②'),
(3,'pandas','sales_df.____()로 수치형 요약 통계를 구합니다.','describe','평균·분위수 등을 확인합니다.','교과서 131쪽 7③'),
(3,'모델','model.____(X_train,y_train)으로 학습합니다.','fit','학습 데이터를 전달합니다.','교과서 105쪽'),
(3,'모델','model.____(X_test)로 새 입력을 예측합니다.','predict','테스트 정답은 입력하지 않습니다.','교과서 105쪽'),
(3,'평가','TP=6, FP=2일 때 정밀도는? 소수로 쓰세요.','0.75','6/(6+2)입니다.','보강'),
(3,'평가','실제 [1,3], 예측 [2,2]의 MSE는?','1','(1²+1²)/2입니다.','보강'),
(4,'검출','CascadeClassifier에 사용하는 정면 얼굴 파일 이름은?','haarcascade_frontalface_default.xml','OpenCV의 haarcascades 폴더에 있습니다.','교과서 195쪽 3①'),
(4,'검출','face_cascade.____(gray,1.1,5)에서 빈칸은?','detectMultiScale','여러 크기로 얼굴 영역을 찾습니다.','교과서 195쪽 3②'),
(4,'입출력','cv2.____("Result",img)로 화면을 표시합니다.','imshow','키 입력 처리는 waitKey로 합니다.','교과서 195쪽 3③'),
(4,'입출력','cv2.____("photo.jpg")로 이미지를 읽습니다.','imread','읽기 실패 시 None을 확인합니다.','교과서 162쪽'),
(4,'변환','cv2.____(img,cv2.COLOR_BGR2GRAY)로 회색조 변환합니다.','cvtColor','색 공간 변환입니다.','교과서 162쪽'),
(4,'반전','8비트 밝기 40의 반전 값은?','215','255-40입니다.','보강')]:q(u,topic_name,'빈칸',p,a,'예제의 함수 이름 또는 식을 확인하세요.',e,ref=ref)
for u,topic_name,p,a,e in [
(3,'과정','데이터 누수 없이 예측 모델을 구성하는 순서를 정하세요.',['입력과 정답 정의','훈련·테스트 분할','훈련 데이터로 전처리 학습','모델 학습·검증','최종 테스트 평가'],'테스트에서 평균·스케일을 배우지 않습니다.'),
(3,'평가','설정 후보를 고르고 최종 평가하는 순서를 정하세요.',['최종 테스트 보관','훈련 부분 교차 검증','설정 선택','전체 훈련 부분 재학습','테스트 점수 보고'],'교차 검증과 테스트의 역할을 나눕니다.'),
(4,'문서 스캔','기울고 어두운 문서의 처리 경로 예를 배열하세요.',['원근 변환','가우시안 블러','대비 조정','이진화'],'교과서 194쪽 2의 경로입니다. 실제 최적 순서는 입력을 비교해 정합니다.'),
(4,'카메라','카메라 프로그램의 기본 순서를 정하세요.',['카메라 열기','연결 성공 확인','프레임 읽고 처리','종료 입력 확인','카메라·창 자원 해제'],'실패해도 자원을 정리합니다.')]:q(u,topic_name,'순서',p,a,'입력이 준비되어야 다음 작업을 할 수 있습니다.',e)
for u,topic_name,p,starter,answer,checks,hint in [
(3,'평가','mae(actual,pred)가 평균 절대 오차를 반환하게 만드세요.','def mae(actual,pred):\n    pass','def mae(actual,pred):\n    return sum(abs(a-p) for a,p in zip(actual,pred))/len(actual)','assert mae([1,3],[2,2])==1\nassert mae([0,0],[2,-4])==3','길이가 같은 비어 있지 않은 목록을 입력받는다고 가정합니다.'),
(3,'평가','precision(tp,fp)가 정밀도를 반환하게 하세요. 분모 0은 0으로 처리합니다.','def precision(tp,fp):\n    pass','def precision(tp,fp):\n    return tp/(tp+fp) if tp+fp else 0','assert precision(6,2)==0.75\nassert precision(0,0)==0\nassert precision(0,3)==0','양성이라고 예측한 전체 개수를 분모로 씁니다.'),
(3,'전처리','fill(values)가 None을 관측값 평균으로 채운 새 목록을 반환하게 만드세요. 관측값은 한 개 이상입니다.','def fill(values):\n    pass','def fill(values):\n    valid=[v for v in values if v is not None]\n    mean=sum(valid)/len(valid)\n    return [mean if v is None else v for v in values]','v=[0,None,4]\nassert fill(v)==[0,2,4]\nassert v==[0,None,4]\nassert fill([None,6])==[6,6]','0은 결측값이 아닙니다.'),
(3,'회귀','predict(x,w,b)가 선형 예측값을 반환하도록 고치세요.','def predict(x,w,b):\n    return x+w+b','def predict(x,w,b):\n    return w*x+b','assert predict(3,2,1)==7\nassert predict(-2,3,4)==-2','가중치×입력 + 절편입니다.'),
(4,'이진화','binary(values,t)가 OpenCV THRESH_BINARY와 같은 기준으로 0/255 목록을 반환하게 하세요.','def binary(values,t):\n    pass','def binary(values,t):\n    return [255 if v>t else 0 for v in values]','assert binary([0,127,128,255],127)==[0,0,255,255]\nassert binary([255],255)==[0]','기준과 같으면 0입니다.'),
(4,'색상','bgr_to_rgb(pixel)이 채널 순서를 바꾼 튜플을 반환하게 만드세요.','def bgr_to_rgb(pixel):\n    pass','def bgr_to_rgb(pixel):\n    b,g,r=pixel\n    return (r,g,b)','assert bgr_to_rgb((20,80,240))==(240,80,20)\nassert bgr_to_rgb((0,0,0))==(0,0,0)','가운데 G는 유지합니다.'),
(4,'좌표','global_point(origin,local)이 ROI 좌표를 원본 좌표로 바꾸게 만드세요.','def global_point(origin,local):\n    pass','def global_point(origin,local):\n    return (origin[0]+local[0],origin[1]+local[1])','assert global_point((100,50),(20,10))==(120,60)\nassert global_point((0,0),(4,5))==(4,5)','두 좌표는 모두 (x,y)입니다.'),
(4,'계수','counts(names)가 현재 프레임의 클래스별 개수 딕셔너리를 반환하게 만드세요.','def counts(names):\n    pass','def counts(names):\n    result={}\n    for name in names:\n        result[name]=result.get(name,0)+1\n    return result','assert counts(["person","car","person"])=={"person":2,"car":1}\nassert counts([])=={}','매 호출마다 새 딕셔너리를 만듭니다.')]:q(u,topic_name,'구현',p,answer,hint,'조건을 바꾸어 검사하고 반환값의 의미를 설명하세요.',starter=starter,checks=checks)
# One transfer task per topic; model answer remains behind the answer control.
for u in [3,4]:
 for l in units[u]:
  q(u,l['title'],'서술',l['tasks'][0] if l['tasks'] else l['lead'],l['paragraphs'][-1],l['visual'][1][0]+'에서 시작해 입력과 출력을 연결하세요.','개념의 정확성, 구체적인 예, 결과 또는 한계의 근거를 스스로 점검하세요.',ref='교과서 '+l['pages']+' 연계·확장')

# Match each explanation answer to the actual transfer task, not to a generic paragraph.
TRANSFER_ANSWERS={
'ml-overview':'예: 음악 추천의 입력은 이전 청취 기록과 곡 특성, 출력은 추천 순위입니다. 추천 서비스의 일부는 데이터에서 선호 패턴을 학습합니다. 모든 기능이 딥러닝일 필요는 없습니다.',
'ml-use':'날짜·요일·학사 일정·이전 날짜까지의 대출 권수와 다음 날 대출 권수를 모읍니다. 다음 날 대출 권수는 정답이며 예측 시점의 입력에 넣지 않습니다.',
'ml-process':'예: 다음 날 총 대출 권수를 예측하고 MAE가 단순 과거 평균 예측보다 낮은지 비교합니다. 시간 순서를 지켜 미래 자료를 테스트로 남기고 오차의 단위는 권으로 적습니다.',
'ml-terms':'미래 대출 수는 예측할 정답이므로 실제 예측 때 사용할 수 없습니다. X에 넣으면 테스트 점수가 높아져도 현실에서는 사용할 수 없는 데이터 누수가 됩니다.',
'ml-methods':'예: 출구 도착 +100, 벽 충돌 -10, 이동마다 -1로 보상을 정할 수 있습니다. 제자리 반복이 이득이 되지 않는지 확인하며 정책은 장기 누적 보상을 높이도록 학습합니다.',
'ml-libraries':'banana 항목을 두 개 추가하면 해당 막대의 높이가 2 커집니다. Counter 또는 빈도표의 수와 그래프 높이를 함께 확인합니다.',
'ml-preprocess':'시험 만점·입력 단위·원래 기록을 확인하고 1000이 100의 오타인지 묻습니다. 확인 없이 삭제하지 않으며 수정 또는 제외의 근거를 기록합니다.',
'ml-classification':'같은 분할·같은 스케일 처리에서 n_neighbors만 3과 7로 바꿉니다. 검증 점수와 달라진 오분류를 표로 기록하며 테스트를 반복 선택에 사용하지 않습니다.',
'ml-regression':'그림의 정답은 y=2x이므로 기울기 2에서 예측과 정답이 겹쳐 MSE=0입니다. 기울기를 1로 바꾸면 네 제곱 오차 평균은 7.5입니다.',
'ml-cluster':'K를 늘리면 같은 데이터가 더 많은 그룹으로 나뉘며 중심 위치도 달라집니다. 군집 번호를 정답이나 순위로 해석하지 않고 점 분포와 중심을 근거로 그룹의 의미를 설명합니다.',
'ml-metrics':'임계값을 올리면 양성 예측 수가 줄어 FP는 줄거나 같고 FN은 늘거나 같습니다. 정밀도는 항상 단조롭게 오르는 것은 아니며, 양성 예측이 없으면 분모가 0입니다.',
'ml-selection':'best_score_는 훈련 부분 교차 검증의 평균이고 최종 테스트는 따로 보관한 데이터의 점수입니다. 평가에 사용한 데이터와 학습 표본이 달라 점수도 달라질 수 있습니다.',
'ml-project':'후보 k=9를 param_grid에 추가하고 같은 교차 검증 조건에서 비교합니다. 평균 검증 점수로 선택하고 변경 이유·최종 테스트 결과·오류 사례를 저널에 남깁니다.',
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
for u in [3,4]:
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
