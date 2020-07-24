import requests
import json

url = 'http://127.0.0.1:21110/api/ai/antenna/'


text = json.dumps({"0": {'ONAIR_SITE_TABLE_ID': 20249035.0,
                         'SITE_IS_OIS': 0.0,
                         'SITE_ENVIRONMENT_TYPE_ID': 1.0,
                         'SITE_SITE_TYPE_ID': 113.0,
                         'SITE_MONTAGE_TYPE_ID': 12.0,
                         'SITE_RN_SUBREGION_ID': 53.0,
                         'SITE_RN_REGION_ID': 16.0,
                         'SITE_RN_MAIN_REGION_ID': 1.0,
                         'SITE_COUNTY_ID': 788.0,
                         'SITE_CITY_ID': 77.0,
                         'ONAIR_CABINET_TYPE_ID': 12.0,
                         'ONAIR_ANTENNA_TYPE_ID': 1392.0,
                         'ONAIR_BBU_TYPE_ID': 241.0,
                         'ONAIR_RFU_TYPE_ID': 345.0,
                         'SIR_CREATED_BY_USER_ID': 20680.0,
                         'SIR_MONTH_ID': 11.0,
                         'SIR_YEAR_ID': 2019.0,
                         'SIR_REASON_ID': 45.0,
                         'IR_TYPE_ID': 93}
                   })



headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=text, headers=headers)
print(r, r.text)
