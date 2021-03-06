# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from models import CrawlerData, db_connect, create_memex_table
import os


# Pipeline writes scraped websites into a folderstructure under the ./files folder
class OnionCrawlerFilesystemPipeline(object):
            
    def process_item(self, item, spider):
        if spider.pipelineFile:
            if spider.pipelineFile.lower() == 'true':
                # Clean filename from domain, path, and protocol
                urlWithoutProtocol = item['url'].split("://")[1].strip('/')
                if '/' not in urlWithoutProtocol:
                    filename = 'files/' + urlWithoutProtocol + '/index.html'
                else:
                    filename = 'files/' + urlWithoutProtocol + '.html'        
                # Directory is only path to file without filename at the end
                directory = filename[0:(len(filename)-len(filename.split('/')[-1]))]
                # Check if directory already exists. If not, create it.
                if not os.path.exists(directory):
                    os.makedirs(directory)
                # Write HTML to file named filename
                with open(filename, 'wb') as f:
                    f.write(item['body'])
            
        return item


# Pipeline writes scraped websites into a Postgres SQL database
class OnionCrawlerPostgresPipeline(object):
    
    def open_spider(self, spider):
        self.pipelinePostgres = spider.pipelinePostgres
        if self.pipelinePostgres:
            if self.pipelinePostgres.lower() == 'true':
                engine = db_connect()
                create_memex_table(engine)
                self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if self.pipelinePostgres:
            if self.pipelinePostgres.lower() == 'true':
                session = self.Session()
                websitedata = CrawlerData(**item)
        
                try:
                    session.add(websitedata)
                    session.commit()
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
                    
        return item