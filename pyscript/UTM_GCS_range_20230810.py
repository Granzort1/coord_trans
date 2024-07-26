from pyproj import CRS, Transformer
import pandas as pd
from datetime import datetime


#위경도 좌표가 10진수가 아닌 도, 분, 초 일때 변환해주는 함수이며, "convert_to_utm" 함수 3번째 값 "dms" 입력시 자동 사용됨
def dms_to_decimal(dms_str):
    degrees, minutes, seconds, direction = 0, 0, 0, 1
    parts = dms_str.split(' ')
    if len(parts) == 4:
        degrees, minutes, seconds, direction_str = parts
        if direction_str in ('S','W'):
            direction = -1
    degrees = direction * (float(degrees) + float(minutes)/60 + float(seconds)/3600)
    return degrees


# 위경도 좌표를 UTM좌표로 변환해주는 함수(10진수단위=좌표 2값만 입력 / 도분초단위=좌표와 3번째 인자"dms"입력)
def convert_to_utm(lat, lon, coordinate_type=None):
    if coordinate_type == "dms":
        lat = dms_to_decimal(lat)
        lon = dms_to_decimal(lon)

    utm_zone_number = 1 + int((lon + 180) / 6)
    if lat >= 0:
        utm_zone = f"{utm_zone_number}N"
    else:
        utm_zone = f"{utm_zone_number}S"

    utm_crs = CRS(f"+proj=utm +zone={utm_zone_number} +ellps=WGS84")
    transformer = Transformer.from_crs(CRS("EPSG:4326"), utm_crs)
    x, y = transformer.transform(lat, lon)
    x = round(x)
    y = round(y)

    return x, y, utm_zone

# 도분초 형태로 좌표를 입력할 경우 예시:
# lat = "35 54 8 N"
# lon = "126 20 44 E"
# x, y, zone = convert_to_utm(lat, lon, "dms")

# 10진수 형태로 좌표를 입력할 경우 예시 (coordinate_type 무입력시 자동으로 10진수 GCS로 인식):
lat = 37.1693
lon = 127.05271
x, y, zone = convert_to_utm(lat, lon)


#x, y, zone = 329285, 4113790, "52N"

print(f"UTM Coordinates in Zone {zone}: x = {x}m, y = {y}m")


def range_cal_for_xy(*ranges):
    headers = ["원점에서의 범위(m)", "x_min(m)", "x_max(m)", "y_min(m)", "y_max(m)", f"UTM zone", "원점x좌표(m)", "원점y좌표(m)"]
    rows = []


    for r in ranges:
        x_min, x_max = x - r * 1000, x + r * 1000
        y_min, y_max = y - r * 1000, y + r * 1000
        row = [f"{r*1000}", f"{x_min}", f"{x_max}", f"{y_min}", f"{y_max}", f"{zone}", f"{x}", f"{y}"]
        rows.append(row)

    df = pd.DataFrame(rows, columns=headers)
    current_time = datetime.now().strftime("%Y%m%d%H%M")
    df.to_csv(f'C:/coord_trans/output/ranges_{current_time}.csv', index=True, encoding="utf-8-sig")



#range_cal_for_xy(1.5)



def convert_to_geodetic(x, y, utm_zone):
    utm_crs = CRS(f"+proj=utm +zone={utm_zone[:-1]} +ellps=WGS84 +{utm_zone[-1].lower()}hem")
    transformer = Transformer.from_crs(utm_crs, CRS("EPSG:4326"))
    lat, lon = transformer.transform(x, y)
    return lat, lon


lat, lon = convert_to_geodetic(329285, 4113790, "52N")
# print(f"Geodetic coordinates: lat = {lat}, lon = {lon}")
print(f"Geodetic coordinates: {lat}N, {lon}E")


