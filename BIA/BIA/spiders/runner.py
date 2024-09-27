import os
from scrapy.cmdline import execute

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    try:
        execute([
            'scrapy',
            'crawl',
            'comunicados_spider',
            '-o',
            'comunicados.json'
        ])
    except SystemExit:
        pass
