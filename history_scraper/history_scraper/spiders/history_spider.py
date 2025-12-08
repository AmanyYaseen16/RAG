import scrapy
import re


class HistorySpider(scrapy.Spider):
    name = "egyptian_history"
    
    start_urls = [
        'https://en.wikipedia.org/wiki/History_of_Egypt',
        'https://www.britannica.com/topic/Pyramids-of-Giza',
        'https://www.britannica.com/topic/list-of-pharaohs-of-ancient-Egypt',
        'https://www.britannica.com/biography/Cleopatra-queen-of-Egypt',
        'https://kids.nationalgeographic.com/history/article/ancient-egypt',
        'https://en.wikipedia.org/wiki/History_of_ancient_Egypt',
        'https://en.wikipedia.org/wiki/Egypt_in_the_Middle_Ages',
        'https://en.wikipedia.org/wiki/History_of_modern_Egypt',
        'https://www.worldhistory.org/egypt/',
        'https://www.britannica.com/place/Memphis-ancient-city-Egypt',
        'https://www.worldhistory.org/Great_Sphinx_of_Giza/',
        'https://www.worldhistory.org/New_Kingdom_of_Egypt/',
        'https://www.worldhistory.org/article/933/daily-life-in-ancient-egypt/',
        'https://www.worldhistory.org/pharaoh/',
        'https://www.worldhistory.org/Nefertiti/'
    ]

    def parse(self, response):

        if 'wikipedia.org' in response.url:
            paragraphs = response.css('div.mw-parser-output > p')
        elif 'nationalgeographic' in response.url:
            paragraphs = response.css('section.Article__Content p')
        elif 'britannica.com' in response.url:
            paragraphs = response.css('p.topic-paragraph')
            if not paragraphs:
                paragraphs = response.css('div.article-body p')
        elif 'worldhistory.org' in response.url:
            paragraphs = response.css('div.body article p, div.text.body article p')
        else:
            self.logger.warning(f"No matching selector for URL: {response.url}")
            return

        for p in paragraphs:
            full_text = ''.join(p.css('::text').getall()).strip()
            cleaned_text = re.sub(r'\[\d+\]', '', full_text)  

            if ('@context' in cleaned_text and '@type' in cleaned_text) or \
                (cleaned_text.strip().startswith('{') and cleaned_text.strip().endswith('}')):
                continue  

            if re.search(r'":\s*"', cleaned_text) and len(cleaned_text.split()) > 5:
                continue

            if cleaned_text and len(cleaned_text.split()) > 20:
                yield{
                        'paragraph': cleaned_text,
                        'source': response.url
                }