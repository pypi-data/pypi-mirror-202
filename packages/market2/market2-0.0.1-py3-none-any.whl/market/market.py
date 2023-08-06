import pandas as pd
import matplotlib.pyplot as plt

plt.rc('font', family='NanumBarunGothic')

def print_stock_data(file_path):
    # 데이터 불러오기
    df = pd.read_csv(file_path)
    
    # 데이터 전처리: 일자를 일주일 단위로 선택
    df['일자'] = pd.to_datetime(df['일자'])  # 일자 컬럼을 datetime 타입으로 변환
    df = df.set_index('일자')  # 일자 컬럼을 인덱스로 설정
    df_week = df.resample('W').last()  # 일주일 단위로 마지막 날짜의 데이터 선택

    # 데이터 출력
    print(df_week)

def plot_stock(file_path, title):
    # 데이터 불러오기
    df = pd.read_csv(file_path)
    
    # 데이터 전처리: 일자를 일주일 단위로 선택
    df['일자'] = pd.to_datetime(df['일자'])  # 일자 컬럼을 datetime 타입으로 변환
    df = df.set_index('일자')  # 일자 컬럼을 인덱스로 설정
    df_week = df.resample('W').last()  # 일주일 단위로 마지막 날짜의 데이터 선택

    # 그래프 그리기
    plt.plot(df_week.index, df_week['종가'])
    plt.xlabel('일자')
    plt.ylabel('종가')
    plt.title(title)
    plt.show()
