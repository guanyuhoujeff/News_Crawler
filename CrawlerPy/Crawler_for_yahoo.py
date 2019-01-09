    
# coding: utf-8

# # Yahoo 財經 台股新聞爬蟲

# * Yahoo 的爬蟲需要 header
# * 時間有時區的問題
    
    

import requests
from bs4 import BeautifulSoup
import os 
try:
    import arrow
except ModuleNotFoundError:
    ## 如果沒有arrow套件，就會自動安裝
    os.system("pip install arrow")
    import arrow


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
            new_title = soup.select_one(".canvas-header").text.strip()
            new_time =  "%d_%d_%d_%d_%d_%d"%(year, month, day, hr, minute, second)
            file_name = new_time + " " + new_title
            symbol=["#","%","*",'&','|','\\','/','?','>','<',":",'"']
            for s in file_name:
                if s in symbol:
                    file_name = file_name.replace(s,"_")
            return file_name + ".txt" 
        
        
        ## 取得新聞的HTML標籤
        soup = BeautifulSoup(requests.get(one_news_url, headers = header).text, "lxml")
        
        ## 新聞的時間
        new_datetime = arrow.get(soup.select_one("time").get("datetime"))
        year = new_datetime.date().year
        month =new_datetime.date().month
        ## 因為yahoo 的時間是以時區0為紀錄，故台灣時間要小時+8，若hr超過24就會進位1天，沒有就保持
        hr = new_datetime.time().hour + 8 - 24
        if hr < 0:
            hr += 24
            day = new_datetime.date().day
        else:
            day =  new_datetime.date().day + 1
        minute = new_datetime.time().minute
        second = new_datetime.time().second
        
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
            news_content += soup.select_one(".canvas-header").text.strip() + "\n" + "%d年%d月%d日 %d時%d分%d秒"%(year, month, day, hr, minute, second)
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
    repeat = 0
    
    
    # # 主要程式開始
    
    
    
    ## 檢查資料夾路徑是否存在
    News_DB_path = os.path.join(New_DB_path, "yahoo")
    check_and_mkdir(News_DB_path)
    ## 進入主頁
    News_home_url = "https://tw.news.yahoo.com/stock"
    ## 需要 header來模擬人在上網，不然yahoo的會檔
    header = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    ## 取得區域網頁元素
    soup = BeautifulSoup(requests.get(News_home_url, headers = header).text, "lxml")
    
    ## 取得新聞清單
    # find_all 的 attrs={} 可以搜索包含特殊属性的tag
    news_list = soup.select_one("#YDC-Stream").find_all(attrs={"data-test-locator": "mega"})
    for one_news_element in news_list:
        one_news_url = "https://tw.news.yahoo.com" + one_news_element.a.get("href")
        try:
            save_news(one_news_url)
        except Cralwer_Done:
            if repeat < 3:
                repeat+=1
            else:
                break
                
    print("yahoo crawler done !! ")
    
