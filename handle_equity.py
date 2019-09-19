from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen

equity_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ190919_CSV.ZIP"
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

for row in rows:
    values = row.split(",")
    equity_code = values[equity_code_index]
    equity_name = values[equity_name_index]
    equity_open_value = float(values[equity_open_index])
    equity_high_value = float(values[equity_high_index])
    equity_low_value = float(values[equity_low_index])
    equity_close_value = float(values[equity_close_index])
    data = {"code": equity_code, "name": equity_name, "open_value": equity_open_value, "high_value": equity_high_value, "low_value": equity_low_value, "close_value": equity_close_value}
    print(data)