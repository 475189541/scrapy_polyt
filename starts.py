from scrapy.cmdline import execute
import sys
import os

# 设置工程的目录，可以在任何路径下运行execute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "spiders_polyt"])