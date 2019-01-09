
# coding: utf-8

# # MoneyDJ 台股 新聞爬蟲



import requests
from bs4 import BeautifulSoup
import os 

def Main(New_DB_path):
    # # 輸入一個新聞專欄的主頁面，會回傳最後一頁的頁碼
    
    def get_final_page(News_home_url):
        ## soup -> 取得該網頁頁面的 html 標籤
        soup = BeautifulSoup(requests.get(News_home_url).text, "lxml")   
        ## 要找到最後一頁的網址 要從class為 "paging3"擷取
        final_page = int(soup.select_one(".paging3").select("td")[-1].select_one("a").get("href").split("index1=")[1].split("&svc=")[0]) 
        return final_page
    
    
    # # 輸入一個新聞頁面的網站，會回傳該頁面上的新聞清單
    
    
    
    def get_new_list(News_page_url):
        soup = BeautifulSoup(requests.get(News_page_url).text, "lxml")
        ## 取得一頁面的全部新聞清單
        news_list = soup.select_one(".forumgrid").select(".ArticleTitle")
        return news_list
    
    
    # # 輸入一個路徑，會檢查該路徑是否存在，若不在則產生資料夾
    
    
    
    def check_and_mkdir(News_DB_path):
        ## os.path.isdir -> 檢查路徑是否存在
        if not(os.path.isdir(News_DB_path)):
            ## 若不存在，使用os.makedirs -> 來建立路徑資料夾
            os.makedirs(News_DB_path)
    
    
    # # 輸入一個新聞的網址，可以爬取標題、時間及內文，並儲存為TXT檔
    
    
    
    def save_news(one_news_url):
        ## 此自訂函式會取得新聞的標題及時間，並組合為要存檔的檔名
        ## 因為檔名不能存在 #,%,*,&,|,\,/,?,>,<,:," 等符號，故如果檔名有不符合符號則取代為 _
        def get_file_name():
            new_title = soup.select_one(".viewer_tl").text.strip()
            new_time = soup.select_one("#ctl00_ctl00_MainContent_Contents_lbDate").text.strip().replace("/","_").replace(" ","_").replace(":","_")
            file_name = new_time + " " + new_title
            symbol=["#","%","*",'&','|','\\','/','?','>','<',":",'"']
            for s in file_name:
                if s in symbol:
                    file_name = file_name.replace(s,"_")
            return file_name + ".txt" 
    
    
        ## 取得新聞的HTML標籤
        soup = BeautifulSoup(requests.get(one_news_url).text, "lxml")
        ## 取得要存檔的檔名
        file_name = get_file_name()
    
        ##如果檔案已經在我們資料夾中，則Pass
        if file_name in os.listdir(News_DB_path):
            #print("Pass News : ", file_name)
            raise Cralwer_Done
        
        else:
            ## news_content 為要寫入TXT檔的內文
            news_content = ""
            ## 文本一開始為新聞標題及時間
            news_content += soup.select_one(".viewer_tl").text.strip() + "\n" + soup.select_one("#ctl00_ctl00_MainContent_Contents_lbDate").text.strip() 
            ## 發現每個內文的標籤為p，故以迴圈讀取每個上的文字，以累計的方式寫在news_content
            for p in soup.select_one("article").select("p"):
                news_content += "\n"
                news_content += p.text
            ## 最後把news_content存成txt檔，編碼為utf8
            with open(os.path.join(News_DB_path, file_name), "w", encoding="utf8") as writer:
                writer.write(news_content)
    
    
    # # 定義爬蟲完成例外以及離開爬蟲變數
    
    
    
    class Cralwer_Done(Exception):
        pass
    
    terminal_cralwer = False
    repeat = 0
    
    
    # # 主要程式開始
    
    
    
    ## 檢查資料夾路徑是否存在
    ## 檢查資料 
    News_DB_path = os.path.join(New_DB_path, "moneydj")
    check_and_mkdir(News_DB_path)
    ## 進入主頁
    News_home_url = "https://www.moneydj.com/KMDJ/Common/ListNewArticles.aspx?index1=2&svc=NW&a=X0100001"
    ## 取得最後一頁頁碼
    final_page = get_final_page(News_home_url)
    ## 以迴圈讀取每一頁
    for page in range(1, final_page + 1 ):
        News_page_url = "https://www.moneydj.com/KMDJ/Common/ListNewArticles.aspx?index1=%d&svc=NW&a=X0100001"%page
        ## 取得一頁上的新聞清單
        news_list = get_new_list(News_page_url)
        ## 以迴圈讀取新聞清單的每一個新聞
        for news_el in news_list:
            ## 取得新聞的網址
            one_news_url = "https://www.moneydj.com" + news_el.select_one("a").get("href")
            try:
                save_news(one_news_url)
            except Cralwer_Done:
                if repeat < 3:
                    repeat+=1
                else:
                    terminal_cralwer = True
                    break
        if terminal_cralwer:
            break
    print("moneydj crawler done !! ")

