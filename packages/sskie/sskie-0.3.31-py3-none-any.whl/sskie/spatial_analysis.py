import pandas as pd
import numpy as np
from scipy.spatial import distance
import geopandas as gpd
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


    def find_apt(self):

        with importlib.resources.open_text('sskie.data', "building_seoul_5179.geojson") as f:
            gdf_building = gpd.read_file(f, encoding='utf-8')

        with importlib.resources.open_text('sskie.data', "subway_5179.geojson") as f:
            gdf_subway = gpd.read_file(f, encoding='utf-8')

        with importlib.resources.open_text('sskie.data', "실거래가_서울.txt") as f:
            df_hs_p = pd.read_csv(f, sep='|', encoding='utf-8', low_memory=False)


        gdf_building_region = gdf_building[gdf_building['A3'].str.split(' ').str.get(1) == self.region]
        gdf_building_region['A12'] = gdf_building_region['A12'].fillna(0)
        gdf_building_region['key'] = gdf_building_region['A2'].astype(str) + '_' + gdf_building_region['A12'].astype(
            str)

        ## 실거래가 필터
        df_hs_p['key'] = df_hs_p['법정동시군구코드'].astype(str) + df_hs_p['법정동읍면동코드'].astype(str) + '_' + df_hs_p['아파트']
        df_hs_p_flt = df_hs_p[df_hs_p['거래금액'] >= 100000]
        df_hs_p_flt_2 = df_hs_p_flt.drop_duplicates('key')

        ## 지하철역 필터
        gdf_subway['buffer'] = gdf_subway.buffer(500)
        gdf_subway['geometry'] = gdf_subway['buffer']

        # merge
        gdf_merge = pd.merge(gdf_building_region, df_hs_p_flt_2, left_on='key', right_on='key')
        gdf_merge.set_crs(epsg=5179, inplace=True, allow_override=True)  # 좌표계 설정
        gdf_subway.set_crs(epsg=5179, inplace=True, allow_override=True)  # 좌표계 설정

        # 건물데이터 중 지하철역 반경에 들어오는 건물 추출
        gdf_sjoin = gpd.sjoin(gdf_merge, gdf_subway, predicate='intersects', how='left')
        gdf_sjoin_flt = gdf_sjoin[~gdf_sjoin['index_right'].isnull()]

        print(gdf_sjoin_flt.head(10))

        print("실거래가 상위 아파트 분석 완료")



    def analyze_facility_access(facility_name):
        # 기본 경로 설정
        with importlib.resources.open_text('sskie.data', f"{facility_name}_서울_5174.geojson") as f:
            facility_file_path = gpd.read_file(f, encoding='utf-8')

        with importlib.resources.open_text('sskie.data', "직방_아파트_서울_5174.geojson") as f:
            apartment_file_path = gpd.read_file(f, encoding='utf-8')

        # 출력 파일 경로 설정
        with importlib.resources.open_text('sskie.data', f"상위100_{facility_name}.csv") as f:
            output_path_top_100 = pd.read_csv(f)

        with importlib.resources.open_text('sskie.data', f"전체_{facility_name}.csv") as f:
            output_path_all = pd.read_csv(f)


        # 시설 및 아파트 단지 SHP 파일 불러오기
        facilities = gpd.read_file(facility_file_path)
        apartment_buffers = gpd.read_file(apartment_file_path)

        # 시설 개수 카운트
        facility_count = len(facilities)
        print(f"시설 개수: {facility_count}")

        # 서울시 전체 면적 (km²)
        seoul_area = 605.2  # 서울시 면적

        # 재화의 도달 거리 계산 함수
        def calculate_reach_distance(area, facility_count):
            tsw = area * 1_000_000  # 면적을 제곱미터로 변환
            d_ij = np.sqrt(tsw / facility_count)  # 도달 거리 계산
            return d_ij

        # 도달 거리 계산
        reach_distance = calculate_reach_distance(seoul_area, facility_count)
        print(f"재화의 도달 거리: {reach_distance:.2f} m")

        # 시설 1개의 효용 값 계산
        utility_per_unit = 1 / facility_count
        print(f"시설 1개의 효용 값: {utility_per_unit:.6f}")

        # 시설에 대한 재화의 도달거리와 효용 정보 설정
        facility_info = {'reach_distance': reach_distance, 'utility_per_unit': utility_per_unit}

        # 'utility' 컬럼이 없으면 새로 생성 (기본값을 설정)
        if 'utility' not in facilities.columns:
            facilities['utility'] = facility_info['utility_per_unit']

        # 아파트 단지 주변 시설 효용을 계산하는 함수
        def calculate_utility_for_facility(apartment, facilities, info):
            facilities['distance_to_apartment'] = facilities.distance(apartment.geometry)
            within_reach_facilities = facilities[facilities['distance_to_apartment'] <= info['reach_distance']]

            if len(within_reach_facilities) == 0:
                return 0

            total_base_utility = within_reach_facilities['utility'].sum()
            total_utility = total_base_utility * 0.8  # 한계효용 감소율 적용

            return total_utility

        # '시설_편익' 컬럼을 추가하고, 각 아파트 단지에 시설 효용 계산
        apartment_buffers['bp'] = 0.0
        for idx, apartment in apartment_buffers.iterrows():
            facility_utility = calculate_utility_for_facility(apartment, facilities, facility_info)
            apartment_buffers.at[idx, 'bp'] = facility_utility

        # 결과 확인
        print(apartment_buffers[['bp']])

        # bp 값을 기준으로 내림차순 정렬 후 상위 100개만 추출
        top_100_apartments = apartment_buffers.sort_values(by='bp', ascending=False).head(100)

        # 상위 100개 아파트 단지의 결과 확인
        print(top_100_apartments[['bp']])

        # 중복 제거 기준은 'danji_name', 'X', 'Y' 컬럼으로 설정 (필드 이름 확인 필요)
        apartment_buffers_unique = apartment_buffers.drop_duplicates(subset=['danji_name', 'X', 'Y'])

        # bp 값을 기준으로 내림차순 정렬 후 상위 100개 추출
        top_100_apartments = apartment_buffers_unique.sort_values(by='bp', ascending=False).head(100)

        print(top_100_apartments.head(10))

        print(f"{facility_name} 접근성 상위 100개 아파트 추출")

