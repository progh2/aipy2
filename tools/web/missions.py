"""3단원 변형 미션 (#135-3). 예제id → [dict(level, text, hint, check), ...].

check는 학생 코드(main.py)를 실행한 뒤 같은 이름공간(namespace)에서 이어서 실행하는
검사 코드다(기존 examples[id]['checks']와 같은 실행 방식 — python-worker.js가
runpy.run_path(entry)의 namespace에 exec한다). assert 실패·예외가 나면 미완료로 본다.

각 미션에는 solution(그 미션을 만족하는 main.py 전체 코드)도 함께 둔다. verify.py가
"solution + check → 통과, 원본 예제 코드 + check → 실패"를 CPython으로 검사한다.

대상은 tools/web/deck_u3.py의 practice 목록에 있고 mode='web'이며, 브라우저에서
실제로 실행 가능한 예제만 고른다. python-worker.js는 sklearn/scipy/cv2/ultralytics를
쓰는 예제를 "PC 실습 경로"로 보고 웹 실행 자체를 막는다(정규식 가드, mode='web'이라도
차단됨) — 그런 예제(ml-sklearn-exam, ml-knn-exam, ml-linear-regression, ml-clustering,
ml-normalization, ml-standardization, ml-train-test-split, ml-performance-metrics,
ml-train-test-split2, ml-cross-val-score, ml-grid-search-cv, ml-learning-curve)는
"확인" 버튼을 눌러도 그 가드에서 바로 실패하므로 미션 대상에서 뺀다. ml-read-data·
ml-regression-metrics는 mode='pc'(엑셀 저장·인터넷 데이터셋)라 원래도 제외 대상이다.
이 6개(모두 pandas/numpy/matplotlib만 쓰는 순수 웹 실행 예제)만 미션을 둔다.
"""

MISSIONS = {
    'ml-numpy-exam': [
        dict(level='쉬움',
             text='5를 더하는 대신 10을 더하도록 바꾸고, result가 [20, 30, 40]이 되게 하세요.',
             hint='result = my_array + 5 줄의 5를 10으로 바꾸면 됩니다.',
             check='assert list(result) == [20, 30, 40], "result가 [20, 30, 40]이 아닙니다."',
             solution='''import numpy as np
my_array = np.array([10, 20, 30])
print("NumPy 배열:", my_array)

result = my_array + 10
print("5를 더한 결과:", result)

# 여러 개의 배열 합치기
array_part1 = np.array([1, 2])
array_part2 = np.array([3, 4])
combined_array = np.concatenate((array_part1, array_part2))
print("\\n합쳐진 배열:", combined_array)
'''),
        dict(level='보통',
             text='array_part1과 array_part2를 이어붙일 때 array_part2를 한 번 더 이어붙여, combined_array가 [1, 2, 3, 4, 3, 4]가 되도록 바꾸세요.',
             hint='np.concatenate((a, b))의 튜플 안에 array_part2를 한 번 더 넣어 보세요: (array_part1, array_part2, array_part2)',
             check='assert list(combined_array) == [1, 2, 3, 4, 3, 4], "combined_array가 [1, 2, 3, 4, 3, 4]가 아닙니다."',
             solution='''import numpy as np
my_array = np.array([10, 20, 30])
print("NumPy 배열:", my_array)

result = my_array + 5
print("5를 더한 결과:", result)

array_part1 = np.array([1, 2])
array_part2 = np.array([3, 4])
combined_array = np.concatenate((array_part1, array_part2, array_part2))
print("\\n합쳐진 배열:", combined_array)
'''),
    ],
    'ml-pandas-exam': [
        dict(level='쉬움',
             text="'민수', 88점인 학생을 한 명 추가해 표에 3명이 나오도록 하세요.",
             hint="data 딕셔너리의 '이름' 리스트에 '민수'를, '점수' 리스트에 88을 추가하세요.",
             check='assert len(my_df) == 3 and 88 in list(my_df["점수"]), "3명 표에 88점 학생이 있어야 합니다."',
             solution='''import pandas as pd
data = {'이름': ['철수', '영희', '민수'], '점수': [85, 92, 88]}
my_df = pd.DataFrame(data)
print("학생 점수표:")
print(my_df)
print("\\n'점수' 칼럼:\\n", my_df['점수'])
'''),
        dict(level='보통',
             text="모든 학생에게 '등급' 칼럼을 추가하고 값을 전부 'A'로 채우세요.",
             hint="my_df['등급'] = 'A' 한 줄을 표를 만든 뒤에 추가하면 모든 행에 같은 값이 채워집니다.",
             check='assert "등급" in my_df.columns and list(my_df["등급"]) == ["A"]*len(my_df), "등급 칼럼이 모두 A여야 합니다."',
             solution='''import pandas as pd
data = {'이름': ['철수', '영희'], '점수': [85, 92]}
my_df = pd.DataFrame(data)
my_df['등급'] = 'A'
print("학생 점수표:")
print(my_df)
print("\\n'점수' 칼럼:\\n", my_df['점수'])
'''),
    ],
    'ml-matplot-exam': [
        dict(level='쉬움',
             text="과일 목록에 'cherry'를 추가해 data_for_plot이 4개 행이 되도록 하세요.",
             hint="'fruits' 리스트 ['apple', 'banana', 'apple']에 'cherry'를 추가하세요.",
             check='assert data_for_plot.shape == (4, 1), "data_for_plot이 4행이어야 합니다."',
             solution='''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data_for_plot = pd.DataFrame({'fruits': ['apple', 'banana', 'apple', 'cherry']})

plt.figure(figsize=(8, 6))
sns.countplot(x='fruits', data=data_for_plot)
plt.savefig("matplot_exam.png")
'''),
        dict(level='보통',
             text='banana를 두 번 더 추가해서 banana 개수가 apple 개수보다 많아지게 하세요.',
             hint="'fruits' 리스트에 'banana'를 두 번 더 넣으면 banana 3개, apple 2개가 됩니다.",
             check='assert (data_for_plot["fruits"]=="banana").sum() > (data_for_plot["fruits"]=="apple").sum(), "banana가 apple보다 많아야 합니다."',
             solution='''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data_for_plot = pd.DataFrame({'fruits': ['apple', 'banana', 'apple', 'banana', 'banana']})

plt.figure(figsize=(8, 6))
sns.countplot(x='fruits', data=data_for_plot)
plt.savefig("matplot_exam.png")
'''),
    ],
    'ml-head-describe-info': [
        dict(level='쉬움',
             text="Score 88점, City 'Seoul'인 'Grace'라는 학생을 추가해 표가 7명이 되도록 하세요.",
             hint="세 리스트(Name, Score, City) 끝에 각각 'Grace', 88, 'Seoul'을 추가하세요.",
             check='assert df.shape == (7, 3) and "Grace" in list(df["Name"]), "Grace가 포함된 7행 표여야 합니다."',
             solution='''import pandas as pd
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace'],
        'Score': [90, 85, 78, 92, 65, 70, 88],
        'City': ['Seoul', 'Busan', 'Seoul', 'Jeju', 'Busan', 'Seoul', 'Seoul']}

df = pd.DataFrame(data)
print("--- 데이터프레임 상위 3행 (df.head(3)) ---")
print(df.head(3))

print("\\n--- 숫자 데이터 통계 요약 (df.describe()) ---")
print(df.describe())

print("\\n--- 데이터프레임 요약 정보 (df.info()) ---")
df.info()
'''),
        dict(level='보통',
             text="City별 인원 수를 value_counts()로 구해 city_counts 변수에 저장하세요.",
             hint="df['City'].value_counts()를 city_counts 변수에 담고 print로 확인하세요.",
             check='assert city_counts["Seoul"] == 3, "Seoul이 3명이어야 합니다."',
             solution='''import pandas as pd
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

city_counts = df['City'].value_counts()
print("\\n--- City별 인원 수 ---")
print(city_counts)
'''),
    ],
    'ml-missing-values': [
        dict(level='쉬움',
             text="Score의 결측치를 0 대신 -1로 채우는 df_fill_neg를 만드세요.",
             hint="df_missing.fillna({'Score': -1})을 df_fill_neg에 저장하세요.",
             check='assert df_fill_neg["Score"][1] == -1, "Bob의 Score가 -1로 채워져야 합니다."',
             solution='''import pandas as pd
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

df_fill_zero = df_missing.fillna(0)
print("\\n결측치를 0으로 채운 후 데이터:")
print(df_fill_zero)

df_fill_neg = df_missing.fillna({'Score': -1})
print("\\nScore 결측치를 -1로 채운 후 데이터:")
print(df_fill_neg)

df_fill_unknown_name = df_missing.fillna({'Name': 'Unknown'})
print("\\nName 결측치를 'Unknown'으로 채운 후 데이터:")
print(df_fill_unknown_name)

score_mean = df_missing['Score'].mean()
df_fill_mean = df_missing.fillna({'Score': score_mean})
print(f"\\n'Score' 결측치를 평균({score_mean:.2f})으로 채운 후 데이터:")
print(df_fill_mean)

score_median = df_missing['Score'].median()
df_fill_median = df_missing.fillna({'Score': score_median})
print(f"\\n'Score' 결측치를 중앙값({score_median:.2f})으로 채운 후 데이터:")
print(df_fill_median)
'''),
        dict(level='보통',
             text='평균 대신 Score 열의 최솟값으로 결측치를 채우는 score_min, df_fill_min을 만드세요.',
             hint="df_missing['Score'].min()을 score_min에, df_missing.fillna({'Score': score_min})을 df_fill_min에 저장하세요.",
             check='assert score_min == 70 and df_fill_min["Score"][1] == 70, "최솟값 70으로 채워져야 합니다."',
             solution='''import pandas as pd
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

df_fill_zero = df_missing.fillna(0)
print("\\n결측치를 0으로 채운 후 데이터:")
print(df_fill_zero)

df_fill_unknown_name = df_missing.fillna({'Name': 'Unknown'})
print("\\nName 결측치를 'Unknown'으로 채운 후 데이터:")
print(df_fill_unknown_name)

score_mean = df_missing['Score'].mean()
df_fill_mean = df_missing.fillna({'Score': score_mean})
print(f"\\n'Score' 결측치를 평균({score_mean:.2f})으로 채운 후 데이터:")
print(df_fill_mean)

score_min = df_missing['Score'].min()
df_fill_min = df_missing.fillna({'Score': score_min})
print(f"\\n'Score' 결측치를 최솟값({score_min:.2f})으로 채운 후 데이터:")
print(df_fill_min)

score_median = df_missing['Score'].median()
df_fill_median = df_missing.fillna({'Score': score_median})
print(f"\\n'Score' 결측치를 중앙값({score_median:.2f})으로 채운 후 데이터:")
print(df_fill_median)
'''),
    ],
    'ml-one-hot-encoding': [
        dict(level='쉬움',
             text="drop_first=True를 False로 바꿔 '도시_부산' 칼럼도 남도록 하세요.",
             hint='get_dummies(...) 호출의 drop_first=True를 drop_first=False로 바꾸세요.',
             check='assert "도시_부산" in df_encoded.columns, "도시_부산 칼럼이 있어야 합니다."',
             solution='''import pandas as pd

data_onehot = {'도시': ['서울', '부산', '서울', '제주', '부산'],
               '직업': ['학생', '직장인', '직장인', '학생', '학생']}
df_onehot = pd.DataFrame(data_onehot)
print(" - 원본 데이터")
print(df_onehot)

df_encoded = pd.get_dummies(df_onehot, columns=['도시', '직업'], drop_first=False, dtype=int)
print("\\n--- 2. 원-핫 인코딩된 데이터 ---")
print(df_encoded)
'''),
        dict(level='보통',
             text="직업이 '자영업'이고 도시가 '서울'인 사람을 한 명 추가해 df_onehot이 6명이 되도록 하세요.",
             hint="'도시' 리스트에 '서울', '직업' 리스트에 '자영업'을 추가하세요.",
             check='assert df_onehot.shape[0] == 6, "df_onehot이 6행이어야 합니다."',
             solution='''import pandas as pd

data_onehot = {'도시': ['서울', '부산', '서울', '제주', '부산', '서울'],
               '직업': ['학생', '직장인', '직장인', '학생', '학생', '자영업']}
df_onehot = pd.DataFrame(data_onehot)
print(" - 원본 데이터")
print(df_onehot)

df_encoded = pd.get_dummies(df_onehot, columns=['도시', '직업'], drop_first=True, dtype=int)
print("\\n--- 2. 원-핫 인코딩된 데이터 ---")
print(df_encoded)
'''),
    ],
}


def for_example(eid):
    return (MISSIONS.get(eid) or []) + (AST_MISSIONS.get(eid) or [])


# (#135-2) 2단원 변형 미션(구조 검사, ast). tkinter는 브라우저에서 실제로 창을 띄울 수
# 없으므로(display 없음) 실행하지 않고, python-worker.js가 mode='pc' 예제에 대해 이미
# 하던 ast.parse 문법 확인 경로에 "학생 코드 문자열을 ast로 구조 검사"하는 단계를 덧붙였다
# (check가 있을 때만 exec — 기존 mode='pc' 예제는 checks가 비어 있어 그대로 동작한다).
# check 코드는 `source`(entry 파일 텍스트 그대로)를 입력으로 받아 assert한다.
AST_MISSIONS = {
    'hello-tk': [
        dict(level='쉬움',
             text="창 제목(title)을 '나의 인사 앱'으로 바꾸세요.",
             hint='root.title("인사 실습 · tkinter") 줄의 문자열을 "나의 인사 앱"으로 바꾸면 됩니다.',
             check='import ast\ntree = ast.parse(source)\ncalls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]\ntitles = [n for n in calls if isinstance(n.func, ast.Attribute) and n.func.attr=="title"]\nassert any(isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value=="나의 인사 앱" for n in titles for a in n.args), "root.title(...) 문구를 \\\'나의 인사 앱\\\'으로 바꿔야 합니다."',
             solution='import tkinter as tk\n\ndef greet():\n    name = entry.get().strip() or "여러분"\n    result.config(text=f"{name}님, 안녕하세요!")\n\ndef reset():\n    entry.delete(0, tk.END)\n    result.config(text="이름을 입력하세요.")\n\nroot = tk.Tk()\nroot.title("나의 인사 앱")\nroot.geometry("480x260")\ntk.Label(root, text="나의 첫 GUI", font=("sans-serif", 20)).pack(pady=16)\nentry = tk.Entry(root)\nentry.pack(fill="x", padx=30)\ntk.Button(root, text="인사하기", command=greet).pack(pady=8)\ntk.Button(root, text="초기화", command=reset).pack()\nresult = tk.Label(root, text="이름을 입력하세요.")\nresult.pack(pady=12)\nroot.mainloop()\n'),
    ],
    'widgets-tk': [
        dict(level='쉬움',
             text="Listbox에 새 항목 '컴퓨터 비전'을 추가하세요.",
             hint='listbox.insert(tk.END, "컴퓨터 비전")을 listbox.pack() 앞에 추가하세요.',
             check='import ast\ntree = ast.parse(source)\ninserts = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr=="insert"]\nassert any(isinstance(a, ast.Constant) and a.value=="컴퓨터 비전" for n in inserts for a in n.args), "listbox.insert(tk.END, \\\'컴퓨터 비전\\\')처럼 새 항목을 추가해야 합니다."',
             solution='import tkinter as tk\nroot = tk.Tk()\nroot.title("tkinter 위젯 도감")\nframe = tk.Frame(root, padx=16, pady=16)\nframe.pack(fill="both", expand=True)\ntk.Label(frame, text="Label: 설명을 표시합니다").pack()\ntk.Entry(frame).pack(fill="x")\ntk.Text(frame, height=3).pack(fill="x")\nchecked = tk.BooleanVar()\ntk.Checkbutton(frame, text="학습 완료", variable=checked).pack()\nchoice = tk.StringVar(value="A")\nfor value in ["A", "B"]:\n    tk.Radiobutton(frame, text=value, variable=choice, value=value).pack()\nlistbox = tk.Listbox(frame, height=3)\nfor value in ["모듈", "패키지", "GUI"]:\n    listbox.insert(tk.END, value)\nlistbox.insert(tk.END, "컴퓨터 비전")\nlistbox.pack()\ncanvas = tk.Canvas(frame, width=240, height=60, bg="white")\ncanvas.create_oval(10, 10, 50, 50, fill="gold")\ncanvas.pack()\ntk.Button(frame, text="상태 출력", command=lambda: print(checked.get(), choice.get())).pack()\nroot.mainloop()\n'),
    ],
    'layout-tk': [
        dict(level='쉬움',
             text="'좁게' 버튼을 눌렀을 때의 창 크기를 340x590에서 300x590으로 줄이세요.",
             hint='"좁게" 버튼의 command=lambda: root.geometry("340x590") 줄에서 340을 300으로 바꾸세요.',
             check='import ast\ntree = ast.parse(source)\ncalls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr=="geometry"]\nassert any(isinstance(a, ast.Constant) and a.value=="300x590" for n in calls for a in n.args), "geometry(\\\'300x590\\\')처럼 좁게 버튼의 크기를 300x590으로 바꿔야 합니다."',
             solution='import tkinter as tk\nroot = tk.Tk()\nroot.title("창 크기를 바꾸어 배치 비교")\nroot.geometry("560x590")\ncontrols = tk.Frame(root)\ncontrols.pack(fill="x", padx=12, pady=8)\ntk.Button(controls, text="넓게", command=lambda: root.geometry("560x590")).pack(side="left")\ntk.Button(controls, text="좁게", command=lambda: root.geometry("300x590")).pack(side="left")\n# 같은 두 입력칸과 확인 버튼입니다. 부모 Frame마다 배치를 나눕니다.\nfor kind in ["pack", "grid", "place"]:\n    frame = tk.LabelFrame(root, text=kind, height=150)\n    frame.pack(fill="x", padx=12, pady=8)\n    if kind == "pack":\n        for title in ["이름", "학번"]:\n            row = tk.Frame(frame)\n            row.pack(fill="x", padx=8, pady=6)\n            tk.Label(row, text=title, width=6).pack(side="left")\n            tk.Entry(row, width=8).pack(side="left", expand=True, fill="x")\n        tk.Button(frame, text="확인").pack(fill="x", padx=8, pady=8)\n    elif kind == "grid":\n        frame.columnconfigure(1, weight=1)\n        for row, title in enumerate(["이름", "학번"]):\n            tk.Label(frame, text=title).grid(row=row, column=0, sticky="e", padx=8, pady=6)\n            tk.Entry(frame, width=8).grid(row=row, column=1, sticky="ew", padx=8)\n        tk.Label(frame, text="두 칸 모두\\n입력하세요").grid(row=0, column=2, rowspan=2, sticky="ns", padx=8)\n        tk.Button(frame, text="확인").grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=8)\n    else:\n        # 좌표와 너비를 고정하면 좁은 창에서 입력칸·버튼이 잘립니다.\n        for row, title in enumerate(["이름", "학번"]):\n            tk.Label(frame, text=title).place(x=8, y=8 + row*36)\n            tk.Entry(frame).place(x=80, y=8 + row*36, width=400)\n        tk.Button(frame, text="확인").place(x=8, y=90, width=472)\nroot.mainloop()\n'),
    ],
    'memo-tk': [
        dict(level='보통',
             text="파일 메뉴에 '새로 만들기' 항목을 하나 더 추가하세요.",
             hint='file_menu.add_command(label="새로 만들기", command=...)을 다른 add_command 줄 사이에 추가하세요.',
             check='import ast\ntree = ast.parse(source)\ncalls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr=="add_command"]\nassert len(calls) >= 4, "파일 메뉴에 add_command 항목을 하나 더 추가해야 합니다."',
             solution='import tkinter as tk\nfrom tkinter import filedialog\n\ndef open_file():\n    file_path = filedialog.askopenfilename()\n    if file_path:\n        with open(file_path, "r", encoding="utf-8") as file:\n            content = file.read()\n        text_area.delete("1.0", tk.END)\n        text_area.insert(tk.END, content)\n\ndef save_file():\n    file_path = filedialog.asksaveasfilename(defaultextension=".txt")\n    if file_path:\n        with open(file_path, "w", encoding="utf-8") as file:\n            file.write(text_area.get("1.0", tk.END))\n\nwindow = tk.Tk()\nwindow.title("나만의 메모장")\nwindow.geometry("600x400")\ntext_area = tk.Text(window, wrap="word")\ntext_area.pack(expand=True, fill="both")\nmenu_bar = tk.Menu(window)\nwindow.config(menu=menu_bar)\nfile_menu = tk.Menu(menu_bar, tearoff=False)\nmenu_bar.add_cascade(label="파일", menu=file_menu)\nfile_menu.add_command(label="열기", command=open_file)\nfile_menu.add_command(label="저장", command=save_file)\nfile_menu.add_separator()\nfile_menu.add_command(label="새로 만들기", command=lambda: text_area.delete("1.0", tk.END))\nfile_menu.add_command(label="종료", command=window.quit)\nwindow.mainloop()\n'),
    ],
}
