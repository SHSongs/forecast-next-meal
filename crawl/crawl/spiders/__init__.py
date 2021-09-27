import scrapy
import pandas as pd
from scrapy.selector import Selector
from urllib.request import urlopen

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    def __init__(self):
        super().__init__()
        self.save_image_path = '../image/'
        self.save_txt_path = '../food.tsv'

        self.food_db = pd.DataFrame(columns = ['date','food'])

    def make_url(self):
        urls = []
        metas = []
        for year in range(2017,2022):
            for month in range(1,13):
                urls.append('http://gsm.gen.hs.kr/xboard/board.php?mode=list&tbnum=8&sCat=0&page=1&keyset=&searchword=&sYear='+str(year)+'&sMonth='+str(month).zfill(2))
                metas.append({'year':str(year),'month':str(month).zfill(2)})
        return urls, metas

    def start_requests(self):
        urls, metas = self.make_url()
        for url,meta in zip(urls,metas):
            yield scrapy.Request(url=url, callback=self.parse,meta=meta)

    def parse(self, response):
        sel = Selector(response)

        self.dates = []
        self.txt = []

        for day in sel.xpath('//div[@class="food_list_box"]'):
            day_num = day.xpath('div[@class="day_num"]/text()').get()


            for times in day.xpath('div[@class="slider_food_list slider_food11 cycle-slideshow"]/div'):
                time = times.xpath('div[@class="food_photo"]/img/@alt').get()
                
                if time is None:
                    continue

                if '아침' in time:
                    date = (response.meta['year'] + response.meta['month'] + day_num + str(1))

                elif '점심' in time:
                    date = (response.meta['year'] + response.meta['month'] + day_num + str(2))

                elif '저녁' in time:
                    date = (response.meta['year'] + response.meta['month'] + day_num + str(2))
                
                else:
                    print('\n\nerror\n\n')

                self.dates.append(date)
                self.txt.append(','.join([ t.strip() for t in day.xpath('div[@class="content_info"]/span/text()').getall()]))
                    
                if day.xpath('div[@class="food_photo"]/img/@src').get() == None:
                    continue
                
                with urlopen(day.xpath('div[@class="food_photo"]/img/@src').get()) as f:
                    with open(self.save_image_path+date+'.png','wb') as h: # 이미지 + 사진번호 + 확장자는 jpg
                        img = f.read() #이미지 읽기
                        h.write(img) # 이미지 저장

        self.food_db = pd.DataFrame()
        self.food_db['date'] = pd.Series(self.dates)
        self.food_db['food'] = pd.Series(self.txt)
        self.food_db.to_csv(self.save_txt_path,sep='\t',index=False)
                    