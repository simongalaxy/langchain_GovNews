import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from tools.logger import Logger
from tools.webCrawler import WebCrawler
from tools.urls_Generator import generate_urls_by_years


# main function.
def main():
    
    # initiate logger.
    logger = Logger(__name__).get_logger()
    logger.info("Class Logger initiated.")
    
    # initiate webcrawler.
    crawler = WebCrawler(logger=logger)
    logger.info("Class WebCrawler initiated.")

    # prepere urls for years.
    startYear = os.getenv("start_year")
    endYear = os.getenv("end_year")
    logger.info(f"start year: {startYear}, end year: {endYear}")
    
    urls = generate_urls_by_years(startYear=int(startYear), endYear=int(endYear))
    logger.info(f"total {len(urls)} generated.")
    
    # start scraping
    results = asyncio.run(crawler.concurrent_crawling(urls=urls[:2]))
    
    for i, result in enumerate(results):
        logger.info(f"i={i}:")
        for j, item in enumerate(result):
            logger.info(f"j={j}: {item.url}")
            logger.info(item.markdown)
        
    return



# program entry point.
if __name__ == "__main__":
    main()
