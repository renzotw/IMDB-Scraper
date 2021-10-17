# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy
class ImdbSpider(scrapy.Spider):
    
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt1074638/']

    def parse(self, response):

        next_page = response.css("li.ipc-inline-list__item a")[2].attrib["href"]

        if next_page:
            next_page = response.urljoin(next_page)
            
            # Where and what
            yield scrapy.Request(next_page, callback = self.parse_full_credits)


        #This works


    #def parse_full_credits(self, response):
         #page = response.url.split("/")[-1]
         #filename = f"imdb-{page}.html"
         #with open(filename, "wb") as f:
            #f.write(response.body)





    def parse_full_credits(self, response):

        for i in range(len(response.css("table.cast_list td:not([class]) a"))):
            cast_page = response.css("table.cast_list td:not([class]) a")[i].attrib["href"] # Get cast member id
            cast_page = response.url.rsplit("/", 4)[0] + cast_page # Specific cast member url
            yield scrapy.Request(cast_page, callback = self.parse_actor_page)

    def parse_actor_page(self, response):

        for project in response.css("div.filmo-category-section")[0].css("b a::text"):
            actor_name = response.css("span.itemprop::text").get()
            movie_or_TV_name = project.get()

            yield {
                "actor" : actor_name,
                "movie_or_TV_name" : movie_or_TV_name
            }

