import pandas as pd
import numpy as np
from scipy.spatial import distance
import os
import geopandas as gpd
import pydeck as pdk
from sklearn.preprocessing import StandardScaler
import json
import importlib.resources
import warnings
warnings.filterwarnings('ignore')

class SpatialAnalysis:
    def __init__(self, region, category):
        # 초기화 메서드에서 지역과 카테고리를 인스턴스 변수로 설정
        self.region = region
        self.category = category

    def spatial_clustering(self):
        # 분석데이터 읽어오기
        with importlib.resources.open_text('sskie.data', self.region + "_all_store.txt") as f:
            df_all_stores = pd.read_csv(f, sep=',', engine='python', encoding='UTF-8')

        with importlib.resources.open_text('sskie.data', self.region + "_" + self.category + "_store.txt") as f:
            df_food_stores = pd.read_csv(f, sep=',', engine='python', encoding='UTF-8')


        # xy 좌표 할당하기
        x1, y1 = np.array(df_all_stores['X']), np.array(df_all_stores['Y'])
        x2, y2 = np.array(df_food_stores['X']), np.array(df_food_stores['Y'])

        # xy 좌표 구조화하기
        pts_matrix_all = np.stack([x1, y1], 1)  # 마포구 내 모든 업종
        pts_matrix_part = np.stack([x2, y2], 1)  # 마포구 내 음식 업종

        # xy 좌표 간 거리 계산
        OD_Dist_Observed = distance.cdist(pts_matrix_part, pts_matrix_part)
        OD_Dist_Expected = distance.cdist(pts_matrix_part, pts_matrix_all)

        # 임계거리 내 점 선택하기
        h = 500  # 임계거리
        N_Observed = np.where(OD_Dist_Observed < h, 1, 0)
        N_Expected = np.where(OD_Dist_Expected < h, 1, 0)

        # 임계거리 내 점 합산하기 (K-function의 정의상 중심점은 제외! 1을 빼줌)
        obs_cnt = np.sum(N_Observed, axis=1) - 1
        exp_cnt = np.sum(N_Expected, axis=1) - 1

        # 국지적 z-값(SC_Z) 및 전역적 z-값(SC_Global) 계산하기 : Rossi transformation 공식 적용
        N, C = df_all_stores.shape[0], df_food_stores.shape[0]
        per_capita = C / N
        exp_cnt = exp_cnt * per_capita
        SC_LQ = obs_cnt / exp_cnt
        SC_Z = (obs_cnt - 3 * exp_cnt + 2 * ((obs_cnt * exp_cnt) ** 0.5)) / (2 * (exp_cnt ** 0.5))
        SC_Global = np.sum(SC_LQ) / C

        # 분석결과를 데이터프레임으로 전환하기 위하여 표 형태로 구조화하기
        SC_LQ_Z_E_O = np.stack([SC_LQ, SC_Z, exp_cnt, obs_cnt], 1)

        # 표 형태로 구조화한 분석결과를 데이터프레임으로 변환하고 텍스트파일로 저장하기
        df_SC_LQ_Z_E_O = pd.DataFrame(SC_LQ_Z_E_O, index=range(C), columns=['LQ', 'Z', 'ExpCnt', 'ObsCnt'])
        df_SC_LQ_Z_E_O['X'], df_SC_LQ_Z_E_O['Y'] = x2, y2
        # df_SC_LQ_Z_E_O.to_csv("../Result/SC_LQ_Z_Rossi" + str(h) + ".txt")
        print(df_SC_LQ_Z_E_O.head(10))

        return "공간 군집 함수 실행 완료"
