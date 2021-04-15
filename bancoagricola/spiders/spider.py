import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbancoagricolaItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BbancoagricolaSpider(scrapy.Spider):
	name = 'bancoagricola'
	start_urls = ['https://www.bancoagricola.com/salaprensa/notas-de-prensa']

	def parse(self, response):
		post_links = response.xpath('//a[@class="ver-mas"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//label[@class="post-date-publicacion"]/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//section[@class="colorsection"]//text()[not (ancestor::h1 or ancestor::label)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=BbancoagricolaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
