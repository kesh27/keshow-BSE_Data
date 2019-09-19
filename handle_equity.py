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

# Tuple structure = (price_diff, code, name, open, high, low, close)
data_list = []
for row in rows:
    values = row.split(",")
    equity_code = values[equity_code_index]
    equity_name = values[equity_name_index]
    equity_open_value = float(values[equity_open_index])
    equity_high_value = float(values[equity_high_index])
    equity_low_value = float(values[equity_low_index])
    equity_close_value = float(values[equity_close_index])
    data = (equity_close_value - equity_open_value, equity_code, equity_name, equity_open_value, equity_high_value, equity_low_value, equity_close_value)
    data_list.append(data)
data_list = sorted(data_list, reverse=True)
print(data_list)