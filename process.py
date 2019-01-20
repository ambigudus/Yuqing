from crawl import crawler
from fenciAndQutingyongci import fenci
from lshforest import calres_big, calres_small, delspace
from sort import sort2txt
from tfbidf import calculate, merge
from update import Update


def Process(path,filename):
    #crawler(sum=1000)
    sort2txt(path)
    fenci()
    delspace()
    calres_big()
    merge()
    Update(filename)



if __name__=='__main__':
    Process('e:/yuqing/process/data/test.csv','test')
