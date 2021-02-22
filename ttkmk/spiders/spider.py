import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import TtkmkItem
from itemloaders.processors import TakeFirst


class TtkmkSpider(scrapy.Spider):
	name = 'ttkmk'
	start_urls = ['http://www.ttk.com.mk/?ItemID=41C74CCBE56B8A4F9B8BA7BC72B444EE']

	def parse(self, response):
		year_pages = response.xpath('//a[@class="WB_TTKBANKA_YahooMenuSubmenu"]/@href').getall()
		yield from response.follow_all(year_pages, self.parse_year)

	def parse_year(self, response):
		post_links = response.xpath('//a[@class="WB_TTKBANKA_ArticleTitle"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		if 'pdf' in response.url:
			return
		title = response.xpath('//span[@id="ArticleTitle"]//text()').getall()
		title = [p.strip() for p in title]
		title = ' '.join(title)
		description = response.xpath('//table[@style="border: 1px #4F4F4F solid"]//td[@class="WB_TTKBANKA_Normal"]//text()[normalize-space() and not(ancestor::span[@id="ArticleTitle"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//table[@style="border: 1px #4F4F4F solid"]//p[last()]//text()').get()
		print(date)
		try:
			date = re.findall(r'\d+.\d+.\d+', date)[0]
		except:
			date = ''

		item = ItemLoader(item=TtkmkItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
