from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

from lxml import etree

import pandas as pd

import numpy as np

import os 

import time

class AlibabaBought:

    '''

    抓取个人淘宝订单的已购买的订单

    '''

    url= 'https://www.taobao.com'

    mytaobao_xpath= '//*[@id="J_SiteNavMytaobao"]/div[@class="site-nav-menu-hd"]/a'

    bought_xpath= '//*[@id="bought"]'

    # page_xpath= '//*[@id="tp-bought-root"]/div[19]/div[2]/ul/li[@class="pagination-next"]'
    page_xpath = '//*[@id="tp-bought-root"]/div[@class="row-mod__row___1aPep js-actions-row-bottom"]/div[2]/ul/li[@class="pagination-next"]'

    date_list= []

    order_list= []

    title_list= []

    shop_list= []

    num_list= []

    price_list= []

    statecode_list= []

    unit_price_list= []

    page = 1

    def __init__(self):

        '''

        实例化的时候自动设置浏览器的参数

        '''

        chrome_options= Options()

        chrome_options.add_argument('--window-size=1500,1366')

        self.browser= webdriver.Chrome(chrome_options=chrome_options)

        if not os.path.exists("./data"):
            os.mkdir("./data")

    def click_case(self, my_xpath):

        '''

        点击事件

        '''

        button= WebDriverWait(self.browser, 20).until(

            EC.element_to_be_clickable(

            (By.XPATH, my_xpath))

        )

        button.click()

    def click_mytaobao(self):

        '''

        打开需要访问的网站,点击我的淘宝

        '''

        self.browser.get(self.url)

        self.click_case(my_xpath=self.mytaobao_xpath)

        # 扫码登录

    def click_bought(self):

        '''

        点击已买到的宝贝

        '''

        self.click_case(self.bought_xpath)

    def click_next_page(self):

        '''

        点击下一页

        '''

        self.click_case(self.page_xpath)

    def analysis_web(self,order_list_xpath,order_list):

        '''解析网页源代码'''

        print(order_list_xpath)

        page_taobao_html= self.browser.page_source

        my_data = etree.HTML(page_taobao_html).xpath(order_list_xpath)

        print(my_data)
        # try:
        order_list.append(my_data[0])

        print(my_data[0])
        
        # except:
        # order_list.append("")
        print("")

        print('-' * 100)

    def make_data_xpath(self):

        '''构造订单信息的xpath路径并解析源码保存到列表中'''

        i = 4

        while True:
            try:
                date_xpath= '//*[@id="tp-bought-root"]/div[%s]/div/table/tbody[1]/tr/td[1]/label/span[2]/text()' % i
                self.analysis_web(date_xpath,self.date_list)
            except:
                return 

            try:
                order_xpath= '//*[@id="tp-bought-root"]/div[%s]/div/table/tbody[1]/tr/td[1]/span/span[3]/text()' % i
                self.analysis_web(order_xpath,self.order_list)
            except:
                self.order_list.append("")
            
            try:
                title_path = '//*[@id="tp-bought-root"]/div[%s]/div/table/tbody[2]/tr/td[1]/div/div[2]/p[1]/a/span[2]/text()' % i
                self.analysis_web(title_path,self.title_list)
            except:
                self.title_list.append("")

            try:
                shop_path= '//*[@id="tp-bought-root"]/div[%s]/div/table/tbody[1]/tr/td[2]/span/a/text()' % i
                self.analysis_web(shop_path,self.shop_list)
            except:
                self.shop_list.append("")

            try:
                num_path= '//*[@id="tp-bought-root"]/div[%s]/div/table/tbody[2]/tr/td[3]/div/p/text()' % i
                self.analysis_web(num_path,self.num_list)
            except:
                self.num_list.append(None)
            
            try:
                price_path= '//*[@id="tp-bought-root"]/div[%s]/div/table/tbody[2]/tr/td[5]/div/div[1]/p/strong/span[2]/text()' % i
                self.analysis_web(price_path,self.price_list)
            except:
                self.price_list.append(None)
            
            try:
                statecode_path= '//*[@id="tp-bought-root"]/div[%s]/div/table/tbody[2]/tr/td[6]/div/p/span/text()' % i
                self.analysis_web(statecode_path,self.statecode_list)
            except:
                self.statecode_list.append("")

            try:
                unit_price_path= '//*[@id="tp-bought-root"]/div[%s]/div/table/tbody[2]/tr/td[2]/div/p/span[2]/text()' % i
                self.analysis_web(unit_price_path,self.unit_price_list)
            except:
                self.unit_price_list.append(None)
            
            i += 1

    def save_date(self):

        '''保存到指定路径下面为excel'''

        taobao_dic = {
            'date': self.date_list,
            'order': self.order_list,
            'title': self.title_list,
            'shop': self.shop_list,
            'num': self.num_list,
            'unit_price': self.unit_price_list,
            'price': self.price_list,
            'statecode': self.statecode_list
            }

        print(taobao_dic)

        df= pd.DataFrame(taobao_dic)

        df.to_excel(f"./data/page_{self.page}.xlsx")

    
    def clear_lists(self):

        self.date_list= []

        self.order_list= []

        self.title_list= []

        self.shop_list= []

        self.num_list= []

        self.price_list= []

        self.statecode_list= []

        self.unit_price_list= []


    def run(self):

        self.click_mytaobao()

        self.click_bought()

        while True:

            if self.page <= 6:
                self.click_next_page()
                time.sleep(max(np.random.normal(5, 1), 0))
                self.page += 1
                continue 

            self.make_data_xpath()

            self.save_date()

            self.clear_lists()

            # is_go_on= int(input("继续抓取请输入 1 ；退出请输入 2："))

            # if is_go_on== 1:

            try:

                self.click_next_page()

                self.page += 1

                time.sleep(max(np.random.normal(5, 1), 0))

            # elif is_go_on== 2:
            except:

                print("Close at", self.page)

                self.browser.close()

                break

        # self.save_date()

def main():

    alibaba_bought = AlibabaBought()

    alibaba_bought.run()

if __name__== '__main__':

    main()
