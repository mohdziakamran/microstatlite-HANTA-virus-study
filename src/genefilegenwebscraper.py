
from operator import index
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd


def prepareGENEFileFromAccnNum(accnNum:str,faulterList):
    try:
        print('~~~~~# Came in for GENE file preperation for Accetion number : '+accnNum+' #~~~~~') #logger*****
        df = pd.DataFrame()

        # driver=webdriver.Chrome('../chromedriver')

        # -------for silent chrome--------
        opt = Options()
        opt.headless = True
        opt.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver=webdriver.Chrome('./chromedriver',options=opt)
        # ------------------------------
        
        # -----for visible chrome but no logging-------------
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--log-level=3')
        # driver=webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
        # ----------------------------------------------------

        # -----start web scraping--------------------------
        link="https://www.ncbi.nlm.nih.gov/nuccore/"+accnNum
        print("OPENING PAGE... : "+link) #logger*****
        driver.get(link)
        cds=WebDriverWait(driver, 60).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'genbank'))
        )
        spnlist=cds[0].find_elements(by=By.TAG_NAME, value='span')
        # print(cds)
        # print(spnlist)

        for e in spnlist:
            if('CDS' in e.text):
                print('-> Found CDS') #logger*****
                dict={}
                cdsTextList=e.text.split('\n')
                for txt in cdsTextList:
                    if 'CDS' in txt:
                        startend=txt.split('             ')[1].split('..')
                        dict['START']=int(startend[0])
                        dict['END']=int(startend[1])
                        print('START : '+startend[0]+'\nEND : '+startend[1]) #logger*****
                    elif 'product' in txt:
                        product=txt.split('product=')[1].replace('"','')
                        dict['PRODUCT']=product
                        print('PRODUCT : '+product)#logger*****
                df = pd.concat([df, pd.DataFrame([[dict['PRODUCT'],dict['START'],dict['END']]],columns=['GENE','START','END'])], ignore_index = True, axis = 0)
        # -----------------------------------------------------

        # -----Write gene excel file---------------------------
        df.to_excel("gene_data/Gene_File_"+accnNum+".xlsx",index=False)
        print('~~~~~# GENE_FILE_'+accnNum+' GENERATED #~~~~~')#logger*****
        # -----------------------------------------------------
    
    except :
        print('GENE FILE GENRATION FAILED FOR ACCN NUM : '+an)
        faulterList.append(accnNum,'FAILED AT GENE FILE GENRATION')


# #################################################
if __name__ == '__main__':
    faulterList=[]
    prepareGENEFileFromAccnNum("AB186420",faulterList)
    print(faulterList)
