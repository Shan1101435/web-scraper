import requests
from bs4 import BeautifulSoup
import csv
import json
import os

# 主函式：爬取書籍資料並根據參數選擇輸出格式（json ）
def scrape_books(output_format='json'):
    # 起始頁面網址（從第一頁開始）
    url = "http://books.toscrape.com/catalogue/page-1.html"
    
    # 儲存所有書籍資料的清單
    books = []

    # 當還有下一頁時持續迴圈爬取
    while url:
        # 發送 GET 請求並解析 HTML
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取所有 class="product_pod" 的書籍項目
        for book in soup.select(".product_pod"):
            title = book.h3.a["title"]  # 書名
            price = book.select_one(".price_color").text[1:]  # 價格（去除貨幣符號 £）
            stock = "In stock" in book.select_one(".availability").text.strip()  # 是否有庫存（True/False）
            rating = book.p["class"][1]  # 評價星數（例如：One, Two, Three, Four, Five）

            # 加入這本書的資料進入 books 清單中
            books.append({
                "title": title,
                "price": price,
                "stock": stock,
                "rating": rating
            })
        
        # 尋找下一頁的連結，若有則更新 URL；否則設為 None 結束迴圈
        next_page = soup.select_one("li.next > a")
        url = f"http://books.toscrape.com/catalogue/{next_page['href']}" if next_page else None

    # 設定輸出路徑
    output_path = os.path.join("static", f"static.{output_format}")
    
    # 根據輸出格式寫入 JSON 檔案
    if output_format == 'json':
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(books, f, indent=4, ensure_ascii=False)
    else:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "price", "stock", "rating"])
            writer.writeheader()
            writer.writerows(books)

    print(f"✅ 爬蟲完成！資料已儲存至：{output_path}")

# 主程式入口，這樣才能在執行此檔案時啟動爬蟲
if __name__ == "__main__":
    scrape_books("json") 
