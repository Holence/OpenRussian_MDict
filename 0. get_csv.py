import time
import requests
import os
from tqdm import tqdm

def download(url: str, fname: str, chunk_size=1024):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)

if not os.path.exists("russian3"):
    os.makedirs("russian3")

structure=requests.get("https://ger1.togetherdb.com/connections/fwoedz5fvtwvq03v/databases/russian3/structure").json()

table_names=[]
for table in structure["result"]["tables"]:
    table_names.append(table["name"])

time.sleep(1)

for table_name in table_names:
    print(table_name)
    key=requests.post("https://ger1.togetherdb.com/connections/fwoedz5fvtwvq03v/databases/russian3/tables/%s/export?expand=false&filter=&separator=%%2C"%table_name).json()["result"]["exportKey"]
    
    url="https://ger1.togetherdb.com/exports/%s"%key
    print(url)

    download(url, "russian3/russian3 - %s.csv"%table_name)
    print()

    time.sleep(1)