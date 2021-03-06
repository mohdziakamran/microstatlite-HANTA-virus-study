
import logging
import multiprocessing
from operator import index
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd

from mplogger import create_logger


def prepareGENEFileFromAccnNum(accnNum:str,accnList_segment,faulterList):
    # logger=logging.getLogger(__name__)
    logger=create_logger(__name__)
    try:
        logger.info('~~~~~# Came in for GENE file preperation for Accetion number : '+accnNum+' #~~~~~') #logger*****
        df = pd.DataFrame()

        # driver=webdriver.Chrome('../chromedriver')

        # -------for silent chrome--------
        opt = Options()
        opt.headless = True
        opt.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver=webdriver.Chrome('chromedriver',options=opt)
        # ------------------------------
        
        # -----for visible chrome but no logging-------------
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--log-level=3')
        # driver=webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
        # ----------------------------------------------------

        # -----start web scraping--------------------------
        link="https://www.ncbi.nlm.nih.gov/nuccore/"+accnNum
        logger.info("OPENING PAGE... : "+link) #logger*****
        driver.get(link)
        cds=WebDriverWait(driver, 60).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'genbank'))
        )
        # ------ADD SEGMENT to new list---------
        heading=driver.find_element(by=By.XPATH, value='//*[@id="maincontent"]/div/div[5]/div[1]/h1')
        try : 
            segment=(heading.text.split('segment ')[1].split(', ')[0])
            if len(segment)!=1 : raise Exception()
        except: 
            logger.error('No Segment Found In Possition for ACCN Num : %s', accnNum)
            segment=''
        accnList_segment.append((accnNum,segment))

        spnlist=cds[0].find_elements(by=By.TAG_NAME, value='span')
        # print(cds)
        # print(spnlist)

        for e in spnlist:
            if('CDS' in e.text):
                logger.info('%s : -> Found CDS',accnNum) #logger*****
                dict={}
                cdsTextList=e.text.split('\n')
                for txt in cdsTextList:
                    if ' CDS ' in txt:
                        startend=txt.split('             ')[1].split('..')
                        dict['START']=int(startend[0])
                        dict['END']=int(startend[1])
                        logger.info('%s : START : '+startend[0],accnNum) #logger*****
                        logger.info('%s : END : '+startend[1],accnNum) #logger*****
                    elif 'product=' in txt:
                        product=txt.split('product=')[1].replace('"','')
                        dict['PRODUCT']=product
                        logger.info('%s : PRODUCT : '+product,accnNum)#logger*****
                df = pd.concat([df, pd.DataFrame([[dict['PRODUCT'],dict['START'],dict['END']]],columns=['GENE','START','END'])], ignore_index = True, axis = 0)
        # -----------------------------------------------------

        # -----Write gene excel file---------------------------
        if df.shape[0] == 0: raise Exception
        # if os.path.exists("gene_data/Gene_File_"+accnNum+".xlsx"):
        #     os.remove("gene_data/Gene_File_"+accnNum+".xlsx")
        df.to_excel("gene_data/Gene_File_"+accnNum+".xlsx",index=False)
        logger.info('~~~~~# GENE_FILE_'+accnNum+' GENERATED #~~~~~')#logger*****
        # -----------------------------------------------------

    except :
        logger.error('GENE FILE GENRATION FAILED FOR ACCN NUM : '+accnNum)
        faulterList[accnNum]='FAILED AT GENE FILE GENRATION ~ { LINK : '+link+'}'


# #################################################
if __name__ == '__main__':
    # logging.basicConfig(handlers=[
    #                 logging.FileHandler("logfile.log"),
    #                 logging.StreamHandler()
    #             ],
    #             format = "%(levelname)s %(asctime)s - %(name)s : %(message)s", 
    #             level = logging.INFO)
    faulterList={}
    segment_list=[]
    prepareGENEFileFromAccnNum("KF892048",segment_list,faulterList)
    print(segment_list)
    print(faulterList)
