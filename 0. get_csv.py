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

if not os.path.exists("openrussian_public"):
    os.makedirs("openrussian_public")

structure=requests.get("https://ger1.togetherdb.com/connections/fwoedz5fvtwvq03v/databases/openrussian_public/structure").json()

table_names=[]
for table in structure["result"]["tables"]:
    table_names.append(table["name"])

time.sleep(1)

for table_name in table_names:
    print(table_name)
    key=requests.post("https://ger1.togetherdb.com/connections/fwoedz5fvtwvq03v/databases/openrussian_public/tables/%s/export?expand=false&filter=&separator=%%2C"%table_name).json()["result"]["exportKey"]
    
    url="https://ger1.togetherdb.com/exports/%s"%key
    print(url)

    download(url, "openrussian_public/openrussian_public - %s.csv"%table_name)
    print()

    time.sleep(1)