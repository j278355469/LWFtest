from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import schedule
import json

class store():
    
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")

        self.browser = webdriver.Chrome(options=self.options)
        
    def title_check(self,product,title):
        products=product.split(" ")
        
        for product in products:
            if product.lower() in title.lower():
                check=True
            else:
                check=False
        
        return check
            
    
    def save_results(self,results,product):
        
        results_df=pd.DataFrame(results)
        
        results_df.index = results_df.index + 1
        # results_df = results_df.head(3)
            
        sorted_results_df = results_df.sort_values(by="price")

        # print(sorted_results_df)

        # sorted_results_df.to_csv(f"{product}.csv",encoding='utf-8-sig')

        return sorted_results_df
        
        
 
       
    def Carrefour(self,product,results):

        self.browser.get("https://online.carrefour.com.tw/zh/search/?q="+product)
    
    # element = WebDriverWait(browser, 3, 0.1).until(
    # expected_conditions.presence_of_element_located((By.CLASS_NAME, 'Cm_C'))
    # )
    
    # for i in range(6):
    #     browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END) 
    
        try: 
            soup=BeautifulSoup(self.browser.page_source,"html.parser")
            
            titles=soup.select("div.commodity-desc a")
            monys=soup.select("div.current-price")
            imgs=soup.select("div.box-img img")
           
        
            for title,img,mony in zip(titles,imgs,monys):
                
                href=title.get("href")
                img=img.get("src")
                
                mony = eval(mony.text.split("$")[1].replace(",", ""))
                title=title.text
                check=self.title_check(product,title)
                if check == True:
                    results.append({"title":title,"price":mony,"link":"https://online.carrefour.com.tw"+href,"pic":img})
                    time.sleep(1)
                    # print("Carrefour")
        
            self.save_results(results,product)
            
            # print("down!")
        except Exception as e:
            print(e)
            # print("找不到")
            self.browser.close()

    def PC(self, product,results):
        self.browser.get("https://ecshweb.pchome.com.tw/search/v3.3/?q="+product)
        
        # element = WebDriverWait(self.browser, 3, 0.1).until(
        #     expected_conditions.presence_of_element_located((By.CLASS_NAME, 'Cm_C'))
        # )
        
        try: 
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            
            titles = soup.select("h5.prod_name a")
            monys = soup.find_all("span", id=re.compile('price_[^text]'))
            imgs = soup.select("a.prod_img img")
            for title, mony ,img in zip(titles, monys,imgs):
                href = title.get("href")
                img=img.get("src")
                mony=eval(mony.text)
                title=title.text
                check=self.title_check(product,title)
                if check == True:
                    
                    results.append({"title": title, "price": mony, "link":"https:"+ href,"pic":img})
                    
                    time.sleep(1)
                    # print(results)
    
            self.save_results(results,product)

        except Exception as e:
            print(e)
            # print("找不到")
        
        self.browser.close()
    
    def Poya(self,product,results):
    
        self.browser.get("https://www.poyabuy.com.tw/v2/Search?q="+product)
    
        # element = WebDriverWait(self.browser, 3, 0.1).until(
        # expected_conditions.presence_of_element_located((By.CLASS_NAME, 'Cm_C'))
        # )
    
        # for i in range(6):
        #     self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END) 
    
        try: 
            soup=BeautifulSoup(self.browser.page_source,"html.parser")
            
            tables=soup.select("li.column-grid-container__column")
            
        
            for table in tables:
                
                tableE1=table.find("img")
                tableE2=table.find("a")
                monyfind=table.select_one("div.sc-kVmAmP").text
                
                mony=eval(monyfind.split("NT$")[1].replace(",", ""))

                href=tableE2.get("href")
                img=tableE1.get("src")
                title=tableE1.get("alt")
                check=self.title_check(product,title)
                if check == True:
                    results.append({"title":title,"price":mony,"link":"https://www.poyabuy.com.tw"+href,"pic":"https:"+img})
                    time.sleep(1)
                    # print("Poya")
        
            self.save_results(results,product)
            # print("down!")
        except Exception as e:
            print(e)
            # print("找不到")
        self.browser.close()
    def momo(self,product,results):


        try:
            self.browser.get(
                f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={product}"
            )
            # browser.get(f"https://shopee.tw/search?keyword={product}")
        

        
            soup=BeautifulSoup(self.browser.page_source,'lxml')
            # totalpage=eval(soup.find_all('div',class_="pageArea")[1].find_all('span')[1].text.split('/')[1])
        except Exception as e :
            print(e)
            print('很抱歉，找不到你要的商品')
            return 
        # print(totalpage)
        for i in range(1,2):
            # print(f'第{i}頁')
            self.browser.get(f'https://www.momoshop.com.tw/search/searchShop.jsp?keyword={product}&searchType=1&cateLevel=0&cateCode=&curPage={i}&_isFuzzy=0&showType=chessboardType&isBrandCategory=N&serviceCode=MT01')

            soup=BeautifulSoup(self.browser.page_source,'lxml')
            # print(soup)
            # ul=soup.select("ul.clearfix")
            # title=soup.find('ul',class_='clearfix').find('h3')
            # price=soup.find('ul',class_='clearfix').find('span',class_='price').find('b')
            # print(title.text)
            # print(price.text)

            lis=soup.select("ul.clearfix li")
            

            for li in lis:
                # title
                title=li.select_one('div.prdNameTitle h3').text
                # price
                price=li.find('span',class_='price').find('b').text
                # pic
                pic = li.find('img',class_="prdImg").get('src')
                # link
                link = f"https://www.momoshop.com.tw{li.find('a',class_='goodsUrl').get('href')}"
                # 排除千分符號
                if ',' in price:
                    price = eval(price.replace(',',''))
                else:
                    price=eval(price)
                    
                check=self.title_check(product,title)
                if check == True:

                # self.datas.append([title,price,link,pic])
                    results.append({'title':title,'price':price,'link':link,'pic':pic})
                    # print("momo")
                    time.sleep(1)
            self.save_results(results,product)
            
        self.browser.close()
    def job(self, product, results):
        # print(f"Starting job for {product}")
        self.PC(product, results)
        # print(f"Job for {product} completed.")
    
    # 可以根据需要调整定时执行的时间间隔
        schedule.every().day.at("24:00").do(self.job, product=product, results=results)

        while True:
            schedule.run_pending()
            time.sleep(1)

# Usage




