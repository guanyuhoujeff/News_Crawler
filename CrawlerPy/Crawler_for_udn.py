
# coding: utf-8

# # 聯合新聞網 股市 爬蟲


import requests
from bs4 import BeautifulSoup
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
            new_title = soup.select_one(".story_art_title").text.strip()
            new_time = soup.select_one(".story_bady_info_author").span.text.replace("-","_").replace(" ","_").replace(":","_")
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
            news_content += soup.select_one(".story_art_title").text.strip() + "\n" + soup.select_one(".story_bady_info_author").span.text.strip() 
            ## 發現每個內文的標籤為p，故以迴圈讀取每個上的文字，以累計的方式寫在news_content
            for p in soup.select_one("#story_body").select("p"):
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
    News_DB_path = os.path.join(New_DB_path, "udn")
    check_and_mkdir(News_DB_path)
    ## 進入主頁
    News_home_url = "https://udn.com/news/cate/2/6645"
    ## 取得區域網頁元素
    soup = BeautifulSoup(requests.get(News_home_url).text, "lxml")
    area_list = soup.select_one("#cate")
    ## 以迴圈讀取每一區域
    for one_area in area_list.select(".listing"):
        ## 每一區域的新聞清單
        for one_area_news_list in one_area.select("dt"):
            ## 以迴圈讀取新聞清單的每一個新聞
            for one_news_element in one_area_news_list:
                ## 取得新聞的網址
                ## try 先試試，遇到錯誤跳過
                try:
                    one_news_url = "https://udn.com" + one_news_element.get("href")
                    save_news(one_news_url)
                except Cralwer_Done:
                    if repeat < 3:
                        repeat+=1
                    else:
                        terminal_cralwer = True
                        break
                except:
                    pass
            if terminal_cralwer:
                break
        if terminal_cralwer:
            break 
    print("udn crawler done !! ")

