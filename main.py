import os
import asyncio
import json
from pprint import pformat
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.ChromaDBHandler import ChromaDBHandler
from tools.urls_Generator import generate_urls_by_year_month, generate_url_by_date
from tools.llmChat import NewsChat



# display results.
def display_results(results, logger) -> None:
    for i, item in enumerate(results):
        if item.success:
            logger.info(f"{i} - {len(results)}. Press release url: {item.url}")
            logger.info(f"Metadata:\n%s", pformat(item.metadata))
            logger.info("Content:")
            logger.info(item.markdown)
            logger.info("-"*100)
    
    return



# main function.
def main():
    
    # initiate Class logger, webcrawler, chromaDBHandler, NewsChat.
    logger = Logger(__name__).get_logger()
    crawler = WebCrawler(logger=logger)
    DBHandler = ChromaDBHandler(logger=logger)
    newsChat = NewsChat(logger=logger, DBHandler=DBHandler)
    
    # prepare urls for specific month in certain year.
    year = input("Enter year:")
    month = input("Enter month:")
    
    urls = generate_urls_by_year_month(year=int(year), month=int(month))
    logger.info(f"urls for year={year}, month={month}: total {len(urls)} urls")
    # results = asyncio.run(crawler.concurrent_crawling(urls=urls))
    
    # prepere urls for years.
    # date = input("Enter the date in format '%Y%m%d' like '20250101': ")
    # url = generate_url_by_date(date=date)
    # logger.info(f"url: {url}")
    
    
    for url in urls:
        # # start scraping
        results = asyncio.run(crawler.crawl(url=url))
        display_results(results=results, logger=logger)
    
    # load data to chromaDB.
        DBHandler.add_News_to_chromaDB(results=results)
    
    # run chat loop.
    newsChat.run_chat_loop()
        
    return



# program entry point.
if __name__ == "__main__":
    main()
