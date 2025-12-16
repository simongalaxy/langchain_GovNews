import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.ChromaDBHandler import ChromaDBHandler
from tools.urls_Generator import generate_urls_by_years, generate_url_by_date

import json
from pprint import pformat

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
    
    # initiate logger.
    logger = Logger(__name__).get_logger()
    logger.info("Class Logger initiated.")
    
    # initiate webcrawler.
    crawler = WebCrawler(logger=logger)
    logger.info("Class WebCrawler initiated.")
    
    # initiate chromadb.
    DBHandler = ChromaDBHandler(logger=logger)

    # prepere urls for years.
    date = input("Enter the date in format '%Y%m%d' like '20250101': ")
    url = generate_url_by_date(date=date)
    logger.info(f"url: {url}")
    
    # start scraping
    # results = asyncio.run(crawler.concurrent_crawling(urls=urls))
    results = asyncio.run(crawler.crawl(url=url))
    display_results(results=results, logger=logger)
    
    # load data to chromaDB.
    DBHandler.add_News_to_chromaDB(results=results)
               
    return



# program entry point.
if __name__ == "__main__":
    main()
