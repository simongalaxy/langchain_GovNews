import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, CacheMode, BrowserConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain

from typing import List
import os
from dotenv import load_dotenv
load_dotenv()


class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.url_filter = URLPatternFilter(patterns=[r"/P[^/]*\.htm$"])
        self.filter_chain = FilterChain(filters=[self.url_filter])
        self.browser_config = BrowserConfig(headless=True)
        self.crawl_config = CrawlerRunConfig(
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=1,  # Reduced depth for faster crawling
                include_external=False,
                filter_chain=self.filter_chain
                ),
            scraping_strategy=LXMLWebScrapingStrategy(),
            exclude_all_images=True,
            exclude_social_media_domains=True,
            exclude_external_links=True,
            # Use valid CSS attribute selectors for better compatibility
            target_elements=['span[id="pressrelease"]'], # For gov news.
            cache_mode=CacheMode.BYPASS
        )
       

    async def concurrent_crawling(self, urls: list[str]):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            tasks = [crawler.arun(url=url, config=self.crawl_config) for url in urls]
            results = await asyncio.gather(*tasks)

        return results
    
    
    async def crawl(self, url: str):
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            results = await crawler.arun(
                url=url,
                config=self.crawl_config
            )
            
            return results


    # async def crawl_many(self, urls: list[str]):
    #     async with AsyncWebCrawler(config=self.browser_config) as crawler:
    #         results = await crawler.arun_many(
    #             urls=urls,
    #             config=self.crawl_config
    #         )
            
    #         return results
