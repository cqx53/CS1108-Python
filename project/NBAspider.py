import requests
import re
import csv
# import numpy as np
from parsel import Selector

class NBASpider:
 
    def __init__(self):

        # self.url是用於爬取每一場比賽是哪一隊比哪一隊, 具體是在crawl_team_opponent這個函數用到
        # self.url = "https://www.basketball-reference.com/leagues/NBA_2022.html"
        self.url = "https://www.basketball-reference.com/leagues/NBA_{}.html"




        # self.schedule_url = "https://www.basketball-reference.com/leagues/NBA_2022_games-{}.html"
        self.schedule_url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html"


        # self.advanced_team_url = "https://www.basketball-reference.com/leagues/NBA_2016.html"
        self.advanced_team_url = "https://www.basketball-reference.com/leagues/NBA_{}.html"







        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 "
                          "Safari/537.36"
        }
 
    # 发送请求，获取数据
    # note: 這個函數的功能是根據你餵進來的url去發送請求, 和你上面定義的self.url是什麼? self.schedule_url是什麼?沒有關係
    def send(self, url):
        response = requests.get(url, headers = self.headers) # 這和課程的jupyter notebook寫的一模一樣
        response.encoding = 'utf-8'
        return response.text
 
    # 解析html
    def parse(self, html):
        team_heads, team_datas = self.get_team_info(html)
        opponent_heads, opponent_datas = self.get_opponent_info(html)
        return team_heads, team_datas, opponent_heads, opponent_datas
 
    def get_team_info(self, html):
        """
        通过正则从获取到的html页面数据中team表的表头和各行数据
        :param html 爬取到的页面数据
        :return: team_heads表头
                 team_datas 列表内容
        """

        # print('this is message from line 57')
        # 1. 正则匹配数据所在的table
        team_table = re.search('<table.*?id="per_game-team".*?>(.*?)</table>', html, re.S).group(1)
        # 2. 正则从table中匹配出表头
        team_head = re.search('<thead>(.*?)</thead>', team_table, re.S).group(1)
        team_heads = re.findall('<th.*?>(.*?)</th>', team_head, re.S)
        # 3. 正则从table中匹配出表的各行数据
        team_datas = self.get_datas(team_table)
 
        return team_heads, team_datas
 
    # 解析opponent数据
    def get_opponent_info(self, html):
        """
        通过正则从获取到的html页面数据中opponent表的表头和各行数据
        :param html 爬取到的页面数据
        :return:
        """
        # 1. 正则匹配数据所在的table
        opponent_table = re.search('<table.*?id="per_game-opponent".*?>(.*?)</table>', html, re.S).group(1)
        # 2. 正则从table中匹配出表头
        opponent_head = re.search('<thead>(.*?)</thead>', opponent_table, re.S).group(1)
        opponent_heads = re.findall('<th.*?>(.*?)</th>', opponent_head, re.S)
        # 3. 正则从table中匹配出表的各行数据
        opponent_datas = self.get_datas(opponent_table)
 
        return opponent_heads, opponent_datas
 
    # 获取表格body数据
    def get_datas(self, table_html):
        """
        从tboday数据中解析出实际数据（去掉页面标签）
        :param table_html 解析出来的table数据
        :return:
        """
        tboday = re.search('<tbody>(.*?)</tbody>', table_html, re.S).group(1)
        contents = re.findall('<tr.*?>(.*?)</tr>', tboday, re.S)
        for oc in contents:
            rk = re.findall('<th.*?>(.*?)</th>', oc)
            datas = re.findall('<td.*?>(.*?)</td>', oc, re.S)
            datas[0] = re.search('<a.*?>(.*?)</a>', datas[0]).group(1)
            datas = rk + datas
            # yield 声明这个方法是一个生成器， 返回的值是datas
            yield datas
 
    def get_schedule_datas(self, table_html):
        """
        从tboday数据中解析出实际数据（去掉页面标签）
        :param table_html 解析出来的table数据
        :return:
        """
        tboday = re.search('<tbody>(.*?)</tbody>', table_html, re.S).group(1) # <- 現在問題應該是這個正則表達式有問題: fixed
        contents = re.findall('<tr.*?>(.*?)</tr>', tboday, re.S)

        # print(len(contents))


        # 這裡有一個for loop
        for oc in contents:
            rk = re.findall('<th.*?><a.*?>(.*?)</a></th>', oc)
            datas = re.findall('<td.*?>(.*?)</td>', oc, re.S)
            if datas and len(datas) > 0:
                datas[1] = re.search('<a.*?>(.*?)</a>', datas[1]).group(1)
                
                datas[3] = re.search('<a.*?>(.*?)</a>', datas[3]).group(1)

                datas[5] = re.search('<a.*?>(.*?)</a>', datas[5]).group(1)
 
            datas = rk + datas

            # yield 声明这个方法是一个生成器， 返回的值是datas
            yield datas

    def parse_schedule_info(self, html): 
        """
        通过正则从获取到的html页面数据中team表的表头和各行数据
        :param html 爬取到的页面数据
        :return: team_heads表头
                 team_datas 列表内容
        """
        # print('this is line 107')
        # 1. 正则匹配数据所在的table
        # table = re.search('<table.*?id="schedule" data-cols-to-freeze=",1">(.*?)</table>', html, re.DOTALL).group(1)
        table = re.search('<table.*?id="schedule" data-cols-to-freeze=",1">(.*?)</table>', html, re.DOTALL)

        if table is None:
            return None
        else:
            table = table.group(1)

        table = table + "</tbody>"
        # print(table)

        # ----- 以下的邏輯應該要包在if-else裡面, 因為每年季後賽什麼時候開始不一樣, 所以你要先確保你正則表達式搜出來有東西再對string做處理 -----



        # 2. 正则从table中匹配出表头
        head = re.search('<thead>(.*?)</thead>', table, re.S).group(1)
        # print(head)
        heads = re.findall('<th.*?>(.*?)</th>', head, re.S)
        # print(heads)









        # 3. 正则从table中匹配出表的各行数据
        datas = self.get_schedule_datas(table) # datas是在這裡產生的
        # print(datas)


        return heads, datas
 
    # 存储成csv文件
    def save_csv(self, title, heads, rows):
        f = open(title + '.csv', mode='w', encoding='utf-8', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=heads)
        csv_writer.writeheader()

        heads[5] = 'PTS_v'
        for row in rows:
            # print('hello')
            # print(row) # <- row沒問題
            dict = {}
            if heads and len(heads) > 0:
                for i, v in enumerate(heads):
                    dict[v] = row[i] if len(row) > i else "" 

            # print(dict)
            csv_writer.writerow(dict)




    def get_advanced_team_datas(self, table):
        trs = table.xpath('./tbody/tr')
        for tr in trs:
            rk = tr.xpath('./th/text()').get()
            datas = tr.xpath('./td[@data-stat!="DUMMY"]/text()').getall()
            datas[0] = tr.xpath('./td/a/text()').get()
            datas.insert(0, rk)
            yield datas

    # bug fixED: https://blog.csdn.net/qq_63585329/article/details/143810588
    def parse_advanced_team(self, html):
        """
        通过xpath从获取到的html页面数据中表头和各行数据
        :param html 爬取到的页面数据
        :return: heads表头
                 datas 列表内容
        """

        # print(type(html))
        selector = Selector(text=html) # <- 問題在這邊!




        # 1. 获取对应的table
        table = selector.xpath('//table[@id="advanced-team"]')

        
        # 2. 从table中匹配出表头
        res = table.xpath('./thead/tr')[1].xpath('./th/text()').getall()
        heads = []
        for i, head in enumerate(res):
            if '\xa0' in head:
                continue
            heads.append(head)
        # 3. 匹配出表的各行数据
        table_data = self.get_advanced_team_datas(table)
        return heads, table_data
    
    def save_csv_advanced(self, title, heads, rows):
        f = open(title + '.csv', mode='w', encoding='utf-8', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(heads)
        for row in rows:
            csv_writer.writerow(row)

        f.close()

    def crawl_advanced_team(self):
        start_year = 2024
        end_year = 2024

        for year in range(start_year, end_year + 1):
            res = self.send(self.advanced_team_url.format(year)) # <- 真的有爬到東西

            heads, datas = self.parse_advanced_team(res) # <- 問題出在這個parse_advanced_team
            # self.parse_advanced_team(res)
            self.save_csv_advanced("advanced_team_" + str(year), heads, datas)

 
    def crawl_team_opponent(self): 
        # print('line 171 is undergoing execution')

        start_year = 2015
        end_year = 2024

        for year in range(start_year, end_year + 1):
            res = self.send(self.url.format(year))

            team_heads, team_datas, opponent_heads, opponent_datas = self.parse(res)

            self.save_csv("team_" + str(year) , team_heads, team_datas)

            self.save_csv("opponent_" + str(year), opponent_heads, opponent_datas)



        # 1. 发送请求
        # res = self.send(self.url)
        # 2. 解析数据
        # team_heads, team_datas, opponent_heads, opponent_datas = self.parse(res) 
        # 3. 保存数据为csv
        # self.save_csv("team", team_heads, team_datas)
        # self.save_csv("opponent", opponent_heads, opponent_datas)
 
    def crawl_schedule(self): # 爬所有數據
        months = ["october", "november", "december", "january", "february", "march", "april", "may", "june", "july"] # 這個必須要加上july因為 -> nba他媽的每一年季後賽開打的時間不一樣, 更間接導致結束的時間也不一樣



        start_year = 2015
        end_year = 2024
        # a = range(start_year, end_year + 1) # 整數產生器
        # years = [str(x) for x in a]


        for year in range(start_year, end_year + 1):
        #    months = ["october", "november", "december", "january", "february", "march", "april", "may", "june", "july"] # 這個必須要加上july因為 -> nba他媽的每一年季後賽開打的時間不一樣, 更間接導致結束的時間也不一樣
            for month in months:
                # string = "now the month is {}"
                # print(string.format(month))

                html = self.send(self.schedule_url.format(year, month))
                if self.parse_schedule_info(html) is None:
                    # print("now it's %s and self.parse_schedule_info return None", month)
                    continue
                else:
                    heads, datas = self.parse_schedule_info(html) # <- 現在問題是datas是空的東西
                    # print(list(datas)) # <- 做到這邊datas都是沒問題的
                    # 3. 保存数据为csv
                    self.save_csv("schedule_" + month + "_" + str(year) , heads, datas)
            
        #for month in months:
        #    html = self.send(self.schedule_url.format(month))
            # print(html) # <- 是有爬到東西的


            # 2. 這個if-else邏輯是必要的不然self.parse_schedule_info(html)回傳None你還往下做, 就會報錯
        #    if self.parse_schedule_info(html) is None:
                # print("now it's %s and self.parse_schedule_info return None", month)
        #        continue
        #    else:
        #        heads, datas = self.parse_schedule_info(html) # <- 現在問題是datas是空的東西
                
                # 3. 保存数据为csv
        #        self.save_csv("schedule_" + month, heads, datas)

            # 3. 保存数据为csv
            # self.save_csv("schedule_"+month, heads, datas)
  
    def crawl(self):
        self.crawl_schedule()
        # self.crawl_team_opponent()
        # self.crawl_advanced_team()

if __name__ == '__main__':
    # 运行爬虫
    spider = NBASpider() # 先instantiate一個爬蟲實體
    spider.crawl()