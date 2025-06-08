import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import folium
from streamlit_folium import st_folium
import numpy as np
from shapely.geometry import Polygon, Point
from streamlit_autorefresh import st_autorefresh

# 机场设施数据
entrances = [
    {'pos': (39.12994, 117.35211), 'name': '1号入口', 'terminal': 'T1'},
    {'pos': (39.12993, 117.35259), 'name': '2号入口', 'terminal': 'T1'},
    {'pos': (39.1299, 117.35314), 'name': '3号入口', 'terminal': 'T1'},
    {'pos': (39.13008, 117.35505), 'name': '4号入口', 'terminal': 'T2'},
    {'pos': (39.13024, 117.35552), 'name': '5号入口', 'terminal': 'T2'},
    {'pos': (39.13037, 117.35602), 'name': '6号入口', 'terminal': 'T2'},
    {'pos': (39.13058, 117.35648), 'name': '7号入口', 'terminal': 'T2'},
    {'pos': (39.13073, 117.35695), 'name': '8号入口', 'terminal': 'T2'},
]
checkins = [
    {'pos': (39.13032, 117.35700), 'name': 'H值机柜台', 'terminal': 'T2'},
    {'pos': (39.13019, 117.35650), 'name': 'G值机柜台', 'terminal': 'T2'},
    {'pos': (39.13006, 117.35598), 'name': 'F值机柜台', 'terminal': 'T2'},
    {'pos': (39.12986, 117.35547), 'name': 'E值机柜台', 'terminal': 'T2'},
    {'pos': (39.12961, 117.35307), 'name': 'D值机柜台', 'terminal': 'T1'},
    {'pos': (39.12964, 117.35266), 'name': 'C值机柜台', 'terminal': 'T1'},
]
gates = [
    # T2登机口 201-230
    {'pos': (39.13071, 117.35865), 'name': '230登机口', 'terminal': 'T2'},
    {'pos': (39.13028, 117.35799), 'name': '229登机口', 'terminal': 'T2'},
    {'pos': (39.12904, 117.35752), 'name': '228登机口', 'terminal': 'T2'},
    {'pos': (39.12825, 117.35789), 'name': '227登机口', 'terminal': 'T2'},
    {'pos': (39.12787, 117.35812), 'name': '226登机口', 'terminal': 'T2'},
    {'pos': (39.12751, 117.35833), 'name': '225登机口', 'terminal': 'T2'},
    {'pos': (39.12713, 117.35855), 'name': '224登机口', 'terminal': 'T2'},
    {'pos': (39.12678, 117.35878), 'name': '223登机口', 'terminal': 'T2'},
    {'pos': (39.12606, 117.36002), 'name': '222登机口', 'terminal': 'T2'},
    {'pos': (39.12599, 117.36032), 'name': '221登机口', 'terminal': 'T2'},
    {'pos': (39.12569, 117.36052), 'name': '220登机口', 'terminal': 'T2'},
    {'pos': (39.12552, 117.36045), 'name': '219登机口', 'terminal': 'T2'},
    {'pos': (39.12537, 117.36002), 'name': '218登机口', 'terminal': 'T2'},
    {'pos': (39.12519, 117.35958), 'name': '217登机口', 'terminal': 'T2'},
    {'pos': (39.12502, 117.35911), 'name': '216登机口', 'terminal': 'T2'},
    {'pos': (39.12485, 117.35863), 'name': '215登机口', 'terminal': 'T2'},
    {'pos': (39.12472, 117.35829), 'name': '214登机口', 'terminal': 'T2'},
    {'pos': (39.12472, 117.35799), 'name': '213登机口', 'terminal': 'T2'},
    {'pos': (39.12486, 117.35792), 'name': '212登机口', 'terminal': 'T2'},
    {'pos': (39.12505, 117.35779), 'name': '211登机口', 'terminal': 'T2'},
    {'pos': (39.12531, 117.35791), 'name': '210登机口', 'terminal': 'T2'},
    {'pos': (39.12551, 117.35808), 'name': '209登机口', 'terminal': 'T2'},
    {'pos': (39.12604, 117.35818), 'name': '208登机口', 'terminal': 'T2'},
    {'pos': (39.12684, 117.35778), 'name': '207登机口', 'terminal': 'T2'},
    {'pos': (39.12722, 117.35756), 'name': '206登机口', 'terminal': 'T2'},
    {'pos': (39.12759, 117.35732), 'name': '205登机口', 'terminal': 'T2'},
    {'pos': (39.12794, 117.35709), 'name': '204登机口', 'terminal': 'T2'},
    {'pos': (39.12831, 117.35686), 'name': '203登机口', 'terminal': 'T2'},
    {'pos': (39.12864, 117.35655), 'name': '202登机口', 'terminal': 'T2'},
    {'pos': (39.12912, 117.35585), 'name': '201登机口', 'terminal': 'T2'},
    {'pos': (39.12916, 117.35466), 'name': '118登机口', 'terminal': 'T2'},
    {'pos': (39.12897, 117.35384), 'name': '117登机口', 'terminal': 'T2'},
    {'pos': (39.12871, 117.35307), 'name': '116登机口', 'terminal': 'T1'},
    {'pos': (39.12786, 117.35273), 'name': '115登机口', 'terminal': 'T1'},
    {'pos': (39.12746, 117.35268), 'name': '114登机口', 'terminal': 'T1'},
    {'pos': (39.12702, 117.35262), 'name': '113登机口', 'terminal': 'T1'},
    {'pos': (39.12661, 117.35262), 'name': '112登机口', 'terminal': 'T1'},
    {'pos': (39.12622, 117.35259), 'name': '111登机口', 'terminal': 'T1'},
    {'pos': (39.12579, 117.35257), 'name': '110登机口', 'terminal': 'T1'},
    {'pos': (39.12589, 117.35209), 'name': '109登机口', 'terminal': 'T1'},
    {'pos': (39.12631, 117.35214), 'name': '108登机口', 'terminal': 'T1'},
    {'pos': (39.12688, 117.35216), 'name': '107登机口', 'terminal': 'T1'},
    {'pos': (39.12738, 117.35221), 'name': '106登机口', 'terminal': 'T1'},
    {'pos': (39.12788, 117.35227), 'name': '105登机口', 'terminal': 'T1'},
    {'pos': (39.12891, 117.35177), 'name': '104登机口', 'terminal': 'T1'},
    {'pos': (39.12932, 117.35061), 'name': '103登机口', 'terminal': 'T1'},
    {'pos': (39.12944, 117.35012), 'name': '102登机口', 'terminal': 'T1'},
    {'pos': (39.12962, 117.35014), 'name': '101登机口', 'terminal': 'T1'},

]

# 安检点数据
security_checks = [
    {'pos': (39.12874, 117.35255), 'name': 'T1航站楼安检', 'terminal': 'T1'},
    {'pos': (39.12931, 117.35676), 'name': 'T2航站楼安检', 'terminal': 'T2'}
]

# 航站楼多边形
terminal_polygon = Polygon([
    [39.13001, 117.35412], [39.13130, 117.35759], [39.13073, 117.35800], [39.13107, 117.35861],
    [39.13079, 117.35887], [39.13013, 117.35789], [39.129865, 117.357636], [39.129261, 117.357556],
    [39.128675, 117.357695], [39.126756, 117.358838], [39.126486, 117.359047], [39.126236, 117.359471],
    [39.12611, 117.35995], [39.126111, 117.360297], [39.12558, 117.360608], [39.124646, 117.358049],
    [39.125175, 117.357711], [39.125412, 117.357969], [39.125695, 117.358097], [39.126061, 117.358135],
    [39.126307, 117.358065], [39.12837, 117.3568150], [39.128645, 117.356542], [39.129149, 117.355791],
    [39.129207, 117.355286], [39.128945, 117.353725], [39.128608, 117.352942], [39.12831, 117.35286],
    [39.12572, 117.35263],
    [39.12576, 117.35204], [39.12835, 117.35226], [39.128679, 117.352127], [39.128883, 117.351730],
    [39.129182, 117.351070], [39.12942, 117.35004], [39.12967, 117.35015], [39.129307, 117.351558],
    [39.13005, 117.35164], [39.12998, 117.35359], [39.12915, 117.35359], [39.12935, 117.35450],
])

SAFE_MARGIN = 0.0001
safe_polygon = terminal_polygon.buffer(-SAFE_MARGIN)


def constrain_points_to_safe_area(points, safe_poly):
    new_points = []
    for pt in points:
        p = Point(pt)
        if safe_poly.contains(p):
            new_points.append(pt)
        else:
            nearest = safe_poly.exterior.interpolate(safe_poly.exterior.project(p))
            new_points.append((nearest.x, nearest.y))
    return new_points


def bezier_curve(start, control, end, n=30):
    t = np.linspace(0, 1, n)
    curve = []
    for ti in t:
        x = (1 - ti) ** 2 * start[0] + 2 * (1 - ti) * ti * control[0] + ti ** 2 * end[0]
        y = (1 - ti) ** 2 * start[1] + 2 * (1 - ti) * ti * control[1] + ti ** 2 * end[1]
        curve.append((x, y))
    return curve


def haversine(p1, p2):
    R = 6371e3
    lat1, lon1 = np.radians(p1)
    lat2, lon2 = np.radians(p2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return round(R * c, 1)


st.title("天津机场导航系统（Streamlit版）")

tab1, tab2 = st.tabs(["实时GPS导航", "自定义路径规划"])

with tab1:
    # 初始化 gps_key
    if 'gps_key' not in st.session_state:
        st.session_state['gps_key'] = 0

    # 刷新定位按钮
    if st.button("刷新定位"):
        st.session_state['gps_key'] += 1
        if 'gps_pos' in st.session_state:
            del st.session_state['gps_pos']

    # 启动/停止GPS自动刷新
    if 'gps_active' not in st.session_state:
        st.session_state['gps_active'] = False
    col1, col2 = st.columns(2)
    with col1:
        if st.button("启动GPS自动刷新"):
            st.session_state['gps_active'] = True
    with col2:
        if st.button("停止GPS自动刷新"):
            st.session_state['gps_active'] = False
    # 自动刷新（每2秒）
    gps_autorefresh = 0


    # 获取GPS
    result = streamlit_js_eval(
        js_expressions="""
            new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(
                    pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}),
                    err => resolve(null)
                );
            })
        """,
        key=f"get_gps_{st.session_state['gps_key']}_{gps_autorefresh}",  # 每次自动刷新都变化
        return_value=True
    )
    if isinstance(result, dict) and 'lat' in result and 'lon' in result:
        st.session_state['gps_pos'] = [result['lat'], result['lon']]
        st.success(f"手机定位：{result['lat']}, {result['lon']}")
    else:
        if 'gps_pos' not in st.session_state:
            st.session_state['gps_pos'] = [39.1300, 117.3560]
        st.info("请允许浏览器获取定位权限")

    # 选择航站楼及目标
    terminal_options = ['T1', 'T2']
    selected_terminal = st.selectbox("选择航站楼", terminal_options, index=1, key='gps_terminal')
    checkin_options = [i for i, c in enumerate(checkins) if c['terminal'] == selected_terminal]
    gate_options = [i for i, g in enumerate(gates) if g['terminal'] == selected_terminal]

    target_type = st.selectbox("目标类型", ["值机柜台", "登机口"], key='gps_target_type')
    if target_type == "值机柜台":
        target_idx = st.selectbox("目标值机柜台", checkin_options, format_func=lambda i: checkins[i]['name'],
                                  key='gps_checkin')
        target_pos = checkins[target_idx]['pos']
        target_name = checkins[target_idx]['name']
    else:
        target_idx = st.selectbox("目标登机口", gate_options, format_func=lambda i: gates[i]['name'], key='gps_gate')
        target_pos = gates[target_idx]['pos']
        target_name = gates[target_idx]['name']

    # 路径规划：起点为当前GPS
    start = st.session_state['gps_pos']
    end = target_pos
    route = [start, end]

    m = folium.Map(location=start, zoom_start=17,
                   tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                   attr='Esri World Imagery', crs="EPSG3857")
    folium.Marker(location=start, popup="当前位置", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=end, popup=f"目标: {target_name}", icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine(route, color='blue', weight=4, opacity=0.7, tooltip='导航路径').add_to(m)
    st_folium(m, width=800, height=600)
    st.write(f"当前GPS: {start}")

    if st.session_state['gps_active']:
        gps_autorefresh = st_autorefresh(interval=2000, key="gps_autorefresh")
with tab2:
    # 传统路径规划
    terminal_options = ['T1', 'T2']
    selected_terminal = st.selectbox("选择航站楼", terminal_options, index=1, key='plan_terminal')
    entrance_options = [i for i, e in enumerate(entrances) if e['terminal'] == selected_terminal]
    checkin_options = [i for i, c in enumerate(checkins) if c['terminal'] == selected_terminal]
    gate_options = [i for i, g in enumerate(gates) if g['terminal'] == selected_terminal]
    security_options = [i for i, s in enumerate(security_checks) if s['terminal'] == selected_terminal]

    entrance_idx = st.selectbox("选择入口", entrance_options, format_func=lambda i: entrances[i]['name'],
                                key=f"entrance_{selected_terminal}")
    checkin_idx = st.selectbox("选择值机柜台", checkin_options, format_func=lambda i: checkins[i]['name'],
                               key=f"checkin_{selected_terminal}")
    gate_idx = st.selectbox("选择登机口", gate_options, format_func=lambda i: gates[i]['name'],
                            key=f"gate_{selected_terminal}")
    security_idx = st.selectbox("选择安检点", security_options, format_func=lambda i: security_checks[i]['name'],
                                key=f"security_{selected_terminal}")

    if st.button("生成路径", key='plan_btn'):
        st.session_state['route'] = {
            'entrance_idx': entrance_idx,
            'security_idx': security_idx,
            'checkin_idx': checkin_idx,
            'gate_idx': gate_idx
        }

    if 'route' in st.session_state:
        e_idx = st.session_state['route']['entrance_idx']
        s_idx = st.session_state['route']['security_idx']
        c_idx = st.session_state['route']['checkin_idx']
        g_idx = st.session_state['route']['gate_idx']

        m = folium.Map(location=entrances[e_idx]['pos'], zoom_start=16,
                       tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                       attr='Esri World Imagery', crs="EPSG3857")
        folium.Marker(
            location=entrances[e_idx]['pos'],
            popup=f"入口: {entrances[e_idx]['name']}",
            icon=folium.Icon(color='green', icon='sign-in', prefix='fa')
        ).add_to(m)
        folium.Marker(
            location=checkins[c_idx]['pos'],
            popup=f"值机柜台: {checkins[c_idx]['name']}",
            icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa')
        ).add_to(m)
        folium.Marker(
            location=security_checks[s_idx]['pos'],
            popup=f"安检口: {security_checks[s_idx]['name']}",
            icon=folium.Icon(color='orange', icon='shield', prefix='fa')
        ).add_to(m)
        folium.Marker(
            location=gates[g_idx]['pos'],
            popup=f"登机口: {gates[g_idx]['name']}",
            icon=folium.Icon(color='red', icon='plane', prefix='fa')
        ).add_to(m)

        # 路径：入口->值机柜台->安检->登机口
        route1 = [entrances[e_idx]['pos'], checkins[c_idx]['pos']]
        route1 = constrain_points_to_safe_area(route1, safe_polygon)
        control2 = ((checkins[c_idx]['pos'][0] + security_checks[s_idx]['pos'][0]) / 2 + 0.0005,
                    (checkins[c_idx]['pos'][1] + security_checks[s_idx]['pos'][1]) / 2 + 0.0005)
        route2 = bezier_curve(checkins[c_idx]['pos'], control2, security_checks[s_idx]['pos'])
        route2 = constrain_points_to_safe_area(route2, safe_polygon)
        control3 = ((security_checks[s_idx]['pos'][0] + gates[g_idx]['pos'][0]) / 2 + 0.0005,
                    (security_checks[s_idx]['pos'][1] + gates[g_idx]['pos'][1]) / 2 + 0.0005)
        route3 = bezier_curve(security_checks[s_idx]['pos'], control3, gates[g_idx]['pos'])
        route3 = constrain_points_to_safe_area(route3, safe_polygon)
        folium.PolyLine(route1, color='blue', weight=4, opacity=0.7, tooltip='入口到值机柜台').add_to(m)
        folium.PolyLine(route2, color='green', weight=4, opacity=0.7, tooltip='值机柜台到安检点').add_to(m)
        folium.PolyLine(route3, color='red', weight=4, opacity=0.7, tooltip='安检点到登机口').add_to(m)

        d1 = haversine(entrances[e_idx]['pos'], checkins[c_idx]['pos'])
        d2 = haversine(checkins[c_idx]['pos'], security_checks[s_idx]['pos'])
        d3 = haversine(security_checks[s_idx]['pos'], gates[g_idx]['pos'])
        st.info(
            f"入口到值机柜台距离：{d1} 米，值机柜台到安检点距离：{d2} 米，安检点到登机口距离：{d3} 米，总计：{d1 + d2 + d3} 米")

        st_folium(m, width=800, height=600)
