
# coding: utf-8

# # 鉅亨網 台股新聞爬蟲



import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import os
    
def Main(New_DB_path):
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
            new_title = soup.select_one("._uo1").text.strip()
            new_time = soup.select_one("time").text.strip().replace("/","_").replace(" ","_").replace(":","_")
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
            news_content += soup.select_one("._uo1").text.strip() + "\n" + soup.select_one("time").text.strip()
            ## 發現每個內文的標籤為p，故以迴圈讀取每個上的文字，以累計的方式寫在news_content
            for p in soup.select_one("article").select("p"):
                news_content += "\n"
                news_content += p.text
            ## 最後把news_content存成txt檔，編碼為utf8
            with open(os.path.join(News_DB_path, file_name), "w", encoding="utf8") as writer:
                writer.write(news_content)
    
    
    # # 建立鉅亨網新聞API類別
    
    
    
    class cnyesAPI:
        def __init__(self, start_date, end_date):
            self.cnyes_home_api = "https://news.cnyes.com/api/v3/news/category/tw_stock?startAt=" + start_date +        "&endAt="+ end_date + "&limit=100"
            api_data = json.loads(BeautifulSoup(requests.get(self.cnyes_home_api).text, "lxml").text)
            self.last_page = api_data["items"]["last_page"]
            
        def get_news_list(self, page):
            target_page_api = self.cnyes_home_api + "&page=%d"%page
            api_data = json.loads(BeautifulSoup(requests.get(target_page_api).text, "lxml").text)
            new_url_list = ["https://news.cnyes.com/news/id/%d"%item["newsId"] for item in api_data["items"]["data"]]
            return new_url_list
    
    
    # # 定義爬蟲完成例外以及離開爬蟲變數
    
    
    
    class Cralwer_Done(Exception):
        pass
    
    terminal_cralwer = False
    repeat = 0
    
    
    # # 主要程式開始
    
    
    
    ## 指定時間
    #start_date = str(int(datetime.datetime(2018, 8, 10).timestamp()))
    ## 固定15天
    start_date = str(int((datetime.datetime.today() - datetime.timedelta(days=15)).timestamp()))
    end_date   = str(int(time.mktime(datetime.date.today().timetuple())))  ## 今天
    
    
    
    ## 檢查資料夾路徑是否存在
    News_DB_path = os.path.join(New_DB_path, "cnyes")
    check_and_mkdir(News_DB_path)
    
    ## 進入api
    api = cnyesAPI(start_date, end_date)
    ## 取得最後一頁頁碼
    final_page = api.last_page
    ## 以迴圈讀取api每一頁
    for page in range(1, final_page + 1 ):
        ## 取得每一頁新聞清單
        new_url_list = api.get_news_list(page)
        ## 以迴圈讀取新聞清單的每一個新聞的網址
        for news_url in new_url_list:
            try:
                save_news(news_url)
            except AttributeError:
                time.sleep(5)
                save_news(news_url)
            except Cralwer_Done:
                if repeat < 3:
                    repeat+=1
                else:
                    terminal_cralwer = True
                    break
        if terminal_cralwer:
            break
    print("cnyes crawler done !! ")
    
