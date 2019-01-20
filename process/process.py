from crawl import crawler
from sort import sort2txt
from fenciAndQutingyongci import fenci
from tfbidf import calculate,merge
from update import Update


crawler(count=200000)
sort2txt()
fenci()
#calculate()
#merge()
#Update()
#os.getcwd()+"\\"+'sorted.txt'
