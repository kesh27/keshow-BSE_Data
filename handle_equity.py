from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import redis
from etc import settings
import json
from datetime import datetime

try: 
    print("settings.REDIS_HOST",settings.REDIS_HOST)
    date = datetime.today().strftime('%d%m%y')
    equity_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{0}_CSV.ZIP".format(date)
    response = urlopen(equity_url)
    equity_file = ZipFile(StringIO(response.read()))
    csv_file = equity_file.namelist()[0]

    rows = equity_file.open(csv_file).readlines()
    columns = rows[0].split(",")
    rows.pop(0)

    equity_code_index = columns.index("SC_CODE")
    equity_name_index = columns.index("SC_NAME")
    equity_open_index = columns.index("OPEN")
    equity_high_index = columns.index("HIGH")
    equity_low_index = columns.index("LOW")
    equity_close_index = columns.index("CLOSE")

    # Tuple structure = (price_diff, code, name, open, high, low, close)
    data_list = []
    for row in rows:
        values = row.split(",")
        equity_code = values[equity_code_index].strip()
        equity_name = values[equity_name_index].strip().upper()
        equity_open_value = float(values[equity_open_index].strip())
        equity_high_value = float(values[equity_high_index].strip())
        equity_low_value = float(values[equity_low_index].strip())
        equity_close_value = float(values[equity_close_index].strip())
        data = (equity_close_value - equity_open_value, equity_code, equity_name, equity_open_value, equity_high_value, equity_low_value, equity_close_value)
        data_list.append(data)
    data_list = sorted(data_list, reverse=True)

    top_ten_equity = []
    for count in range(0,10):
        top_ten_equity.append(data_list[count][2])

    redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)

    for data in data_list:
        equity_code = data[1]
        equity_name = data[2]
        equity_open_value = data[3]
        equity_high_value = data[4]
        equity_low_value = data[5]
        equity_close_value = data[6]
        equity_data = {"code": equity_code, "open_value": equity_open_value, "high_value": equity_high_value, \
        "low_value": equity_low_value, "close_value": equity_close_value}
        redis_conn.set(equity_name, json.dumps(equity_data))
    redis_conn.set("top_ten_equity", json.dumps(top_ten_equity))
    redis_conn.set("last_updated_on", datetime.now().isoformat())

except:
    None