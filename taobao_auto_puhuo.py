import os
import time
import json
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests

# 配置
KEYWORD = "无线耳机"
NUM_PAGES = 2
OUTPUT_DIR = "puhuo_products"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def scrape_taobao(keyword, num_pages):
    products = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for page in range(1, num_pages + 1):
        url = f"https://s.taobao.com/search?q={keyword}&s={(page-1)*44}"
        try:
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.item')
            for item in items[:5]:
                try:
                    title = item.select_one('.title').text.strip() if item.select_one('.title') else 'N/A'
                    price = item.select_one('.price').text.strip() if item.select_one('.price') else '0'
                    products.append({'title': title + ' [公子精选]', 'price': price, 'desc': '自动采集热销品', 'images': []})
                except:
                    continue
        except:
            continue
        time.sleep(2)
    return products

def save_to_excel(products, date_str):
    ensure_dir(OUTPUT_DIR)
    df = pd.DataFrame(products)
    excel_path = os.path.join(OUTPUT_DIR, f"products_{date_str}.xlsx")
    df.to_excel(excel_path, index=False)
    print(f"Excel exported: {excel_path}")

def main():
    print("公子赚钱脚本启动~")
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    products = scrape_taobao(KEYWORD, NUM_PAGES)
    save_to_excel(products, date_str)
    with open(os.path.join(OUTPUT_DIR, f"products_{date_str}.json"), 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print("采集完成！")

if __name__ == "__main__":
    main()