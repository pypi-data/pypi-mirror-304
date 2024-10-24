import pandas as pd
import geopandas as gpd
import pydeck as pdk
import numpy as np
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import libpysal
from esda.getisord import G_Local
import importlib.resources

os.chdir('D:/R&D/자료/230317_공간질의함수/4월_마포구 2020년 이후 폐업 점포가 많은 지역/')

# gdf_grid = gpd.read_file('Data/seoul_50m_grid.shp', encoding='utf-8')
# df = pd.read_csv("Data/서울_지자체인허가(년월일,읍면동추가).csv", encoding='cp949')
# gdf_mapo = gpd.read_file('Data/Mapo-gu.shp', encoding='')

with importlib.resources.open_text('sskie.data', "seoul_50m_grid.geojson") as f:
    gdf_grid = gpd.read_file(f, encoding='utf-8')

with importlib.resources.open_text('sskie.data', "mapo-gu.geojson") as f:
    gdf_mapo = gpd.read_file(f, encoding='utf-8')

with importlib.resources.open_text('sskie.data', "seoul_store.csv") as f:
    df = pd.read_csv(f, encoding='cp949')

gdf_grid['key'] = gdf_grid.index
gdf_gird = gdf_grid.to_crs(crs=5179)
gdf_mapo = gdf_mapo.to_crs(crs=4326)

def G_Local(region, day, threshold):
    df_c = df[(df.영업상태명 == '폐업') & (df.폐업일자 > day)]
    df_c_region = df_c[df_c['시군구'] == region]
    gdf_c_region = gpd.GeoDataFrame(df_c_region, geometry=gpd.points_from_xy(df_c_region['X_5179'], df_c_region['Y_5179']), crs='epsg:5179')

    gdf_sjoin = gpd.sjoin(gdf_gird, gdf_c_region)
    gdf_sjoin_gby = gdf_sjoin.groupby('key').count()
    gdf_sjoin_gby = gdf_sjoin_gby['id']
    df_merge = pd.merge(gdf_grid, gdf_sjoin_gby, left_index=True, right_index=True)
    df_merge.rename(columns={"id_y":"NUMPOINTS"}, inplace=True)

    gdf = df_merge.copy()

    x_crd, y_crd = tuple(np.array(gdf.centroid.x)), tuple(np.array(gdf.centroid.y))
    points = list(zip(x_crd, y_crd))
    w = libpysal.weights.DistanceBand(points, threshold=threshold)
    y = np.array(list(gdf['NUMPOINTS']))
    lg = G_Local(y, w, transform='B', star=True)
    df_lg_Zs = pd.DataFrame(lg.Zs, columns=['Z-Val'])
    df_lg_Zs['X'] = x_crd
    df_lg_Zs['Y'] = y_crd

    result = df_lg_Zs.copy() # type : Point

    ### 시각화
    gdf_df = gpd.GeoDataFrame(result, geometry=gpd.points_from_xy(result['X'], result['Y']), crs='epsg:5179')
    del gdf_df['Unnamed: 0']

    # gdf_grid.set_crs(crs=5179, inplace=True, allow_override=True)
    gdf_df = gdf_df.to_crs(crs=4326)
    # gdf_mapo = gdf_grid.to_crs(crs=4326)

    result_sjoin = gpd.sjoin(gdf_grid, gdf_df, how='left')
    result_sjoin2 = result_sjoin[['Z-Val', 'X', 'Y', 'geometry']] # type : grid
    result = result_sjoin2.copy()

    result = result.to_crs(crs=4326)

    def multipolygon_to_coordinates(x):
        coords = []
        if x.geom_type == 'Polygon':
            lon, lat = x.exterior.xy
            coords = [[x, y] for x, y in zip(lon, lat)]
        elif x.geom_type == 'MultiPolygon':
            for polygon in x:
                lon, lat = polygon.exterior.xy
                coords += [[x, y] for x, y in zip(lon, lat)]
        return coords

    gdf_mapo['coordinates'] = gdf_mapo['geometry'].apply(multipolygon_to_coordinates)
    del gdf_mapo['geometry']

    deck_result = pd.DataFrame(result)
    deck_gdf = pd.DataFrame(gdf_mapo)

    a = deck_result['Z-Val']
    arr = np.array(a)
    arr = arr.reshape(-1, 1)
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(arr)

    deck_result['zz'] = normalized_data
    deck_result['hh'] = deck_result['Z-Val'] + 10
    deck_result['hh'] = deck_result['hh'] ** 2.3

    layer = pdk.Layer(
        'PolygonLayer',
        deck_result,
        get_polygon='coordinates',
        get_elevation='hh',
        elevation_scale=1,
        extruded=True,
        pickable=True,
        get_fill_color='[255, 255 - zz * 66, 255 - zz * 66]',
        # get_fill_color='[0, 255 * -(zz), 0]',
        # get_fill_color="interpolate_color(zz, color_scale)",
        auto_highlight=True,
        opacity=0.5,
    )
    poly = pdk.Layer(
        'PolygonLayer',
        data=deck_gdf,
        get_polygon='coordinates',
        get_fill_color=[255, 255, 255, 99.99],  # RGBA color values
        get_line_color=[0, 0, 0, 255],  # RGBA color values
        opacity=0.9,
        get_line_width=5,
        pickable=True
    )
    center = [127.010, 37.490]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=13)
    view_state.pitch = 45

    r = pdk.Deck(layers=[layer, poly], map_style='light', initial_view_state=view_state)

    r.to_html('Reulst/4월_마포구 2020년 이후 폐업 점포가 많은 지역.html')
