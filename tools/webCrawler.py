import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain

from typing import List
import os
from dotenv import load_dotenv
load_dotenv()

from tools.urls_Generator import dates_in_year

class WebCrawler:
    def __init__(self, logger):
        self.logger = logger
        self.url_filter = URLPatternFilter(patterns=[r"/P[^/]*\.htm$"])
        self.filter_chain = FilterChain(filters=[self.url_filter])
        self.crawl_config = CrawlerRunConfig(
                deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=2,  # Reduced depth for faster crawling
                include_external=False,
                filter_chain=self.filter_chain
            ),
            scraping_strategy=LXMLWebScrapingStrategy(),
            verbose=True,
            exclude_all_images=True,
            exclude_social_media_domains=True,
            # Use valid CSS attribute selectors for better compatibility
            target_elements=['span[id="PRHeadlineSpan"]', 'span[id="pressrelease"]', 'div[id="contentBody"]'],
            #target_elements=['div[id="content"]', 'div[id="contentBody"]'],
            )

    async def concurrent_crawling(self, urls: list[str]):
        async with AsyncWebCrawler() as crawler:
            tasks = [crawler.arun(url=url, config=self.crawl_config) for url in urls]
            results = await asyncio.gather(*tasks)

        return results
