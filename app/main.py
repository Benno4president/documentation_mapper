import sys
import argparse
from loguru import logger
import pandas as pd
from scrapers import IScraper, active_scrapers

def parse_args():
    desc = """
            Hello there!, welcome to a low code documentation fetcher.
            Start scraping any source using only very litte and 
            very googlable python code.
        """
    parser = argparse.ArgumentParser(prog='Doc Fetcher',description=desc, usage='just press play')
    parser.add_argument('-t', '--test', action='store_true', help="Log level debug")
    parser.add_argument('-s', '--scraper', choices=['all']+list(active_scrapers.keys()), 
                        default='all', help='Specify a single scraper to run')
    return parser.parse_args()
    

def run_scrape():
    for scraper_name in active_scrapers:
        #try:
            scraper:IScraper = active_scrapers[scraper_name]()

            articles: pd.DataFrame = scraper.run()
            articles['origin'] = scraper_name

            articles = articles[['origin','url','title','updated','doc_links','vid_links','text']]

            logger.info('finished scraping {} | entries: {}', scraper_name, len(articles))
            print('Labels:')
            print(articles.columns)
            print('-'*45)
            print(articles)
            articles.to_csv(f'./xfetcher_{scraper_name}.csv', index=False)
        #except Exception as e:
        #    logger.error('{} thrown on {}', e, scraper_name)


def main():
    """
    """
    global active_scrapers # yes, i mutate a global, embrace chaos.
    args = parse_args()
    print(args)
    
    # Remove to reset logging level to something else
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>"
    )
    logger.remove(0)
    logger.add(sys.stderr, format=logger_format, level="INFO" if not args.test else "DEBUG")

    if args.scraper != 'all':
        active_scrapers = {args.scraper:active_scrapers.pop(args.scraper)}
    
    #:repeat
    run_scrape()
    # sleep
    

if __name__ == '__main__':
    main()