import pandas as pd
import numpy as np
from scipy.spatial import distance
import os
import geopandas as gpd
import pydeck as pdk
from sklearn.preprocessing import StandardScaler
import json
import importlib.resources


def Spatial_Clustering(region, category):

    # 분석데이터 읽어오기
    with importlib.resources.open_text('SKIE.data', "data/" + region + "_all_store.txt") as f:
        df_all_stores = pd.read_csv(f, sep=',', engine='python', encoding='UTF-8')

    with importlib.resources.open_text('SKIE.data', "data/" + region + "_" + category + "_store.txt") as f:
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
    print("geojson전까지 완료")

    with importlib.resources.open_text('SKIE.data', "Data/mapo-gu.geojson") as f:
        gdf_mapo = gpd.read_file(f, encoding='utf-8')

    # gdf_mapo = gpd.read_file('Data/Mapo-gu.shp', encoding='utf-8')
    gdf_df = gpd.GeoDataFrame(df_SC_LQ_Z_E_O, geometry=gpd.points_from_xy(df_SC_LQ_Z_E_O['X'], df_SC_LQ_Z_E_O['Y']),
                              crs='epsg:5179')
    gdf_df = gdf_df.to_crs(crs=4326)
    gdf_mapo = gdf_mapo.to_crs(crs=4326)
    gdf_df['xx'], gdf_df['yy'] = gdf_df.geometry.x, gdf_df.geometry.y

    geojson_str = gdf_mapo.to_json()
    geojson = json.loads(geojson_str)

    # 적용
    # gdf_mapo['coordinates'] = gdf_mapo['geometry'].apply(lambda x: [[list(coord) for coord in x.exterior.coords]])

    # 정규화
    a = gdf_df['Z']
    arr = np.array(a)
    arr = arr.reshape(-1, 1)
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(arr)

    gdf_df['zz'] = normalized_data
    gdf_df['hh'] = gdf_df['Z'] + 10
    gdf_df['hh'] = gdf_df['hh'] ** 2.3

    # 파이덱에 사용될 데이터
    deck_df = pd.DataFrame(gdf_df)
    deck_gdf = pd.DataFrame(gdf_mapo)

    deck_df['coordinates'] = deck_df['geometry'].apply(lambda geom: [geom.x, geom.y]).tolist()
    del deck_df['geometry']

    deck_df_plus = deck_df[deck_df['zz'] > 0]
    deck_df_mi = deck_df[deck_df['zz'] < 0]

    layer1 = pdk.Layer(
        "ScatterplotLayer",
        deck_df_plus,
        get_position=['xx', 'yy', 'hh'],
        get_radius=15,  # 반경
        get_fill_color='[255, 255 - zz * 100, 255 - zz * 100]',
        get_color='zz',
        get_line_color=[0, 0, 255],
        get_line_width=5,
        get_elevation="value",
        elevation_scale=100,
        elevation_range=[0, 1000],
        auto_highlight=True,  # 마우스 올릴 때 하이라이트
        extruded=True,
        pickable=True,
        get_time='time'  # 시간 값을 설정
    )

    layer2 = pdk.Layer(
        "ScatterplotLayer",
        deck_df_mi,
        get_position=['xx', 'yy', 'hh'],
        get_radius=15,  # 반경
        get_fill_color='[255 + zz * 70, 255 + zz * 70, 255]',
        get_color='zz',
        get_line_color=[0, 0, 255],
        get_line_width=5,
        get_elevation="value",
        elevation_scale=100,
        elevation_range=[0, 1000],
        auto_highlight=True,  # 마우스 올릴 때 하이라이트
        extruded=True,
        pickable=True,
        get_time='time'  # 시간 값을 설정
    )

    poly = pdk.Layer(
        'GeoJsonLayer',
        geojson,
        get_fill_color=[255, 255, 255, 99.99],  # RGBA color values
        get_line_color=[0, 0, 0, 255],  # RGBA color values
        opacity=0.9,
        get_line_width=12,
        pickable=True
    )

    # 지도 중심 위치 설정
    center = [127.010, 37.490]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=13)

    r = pdk.Deck(layers=[layer1, layer2, poly], map_style='dark', initial_view_state=view_state)

    r.to_html('c:/마포구 음식업 특화 장소.html')

    return "공간 군집 함수 실행 완료"
