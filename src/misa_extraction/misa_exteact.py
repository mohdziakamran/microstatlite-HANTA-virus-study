
from datetime import datetime
import logging
import multiprocessing
from operator import index
import os
import shutil
from numpy import NaN
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import progressbar

exp=[]
barcount=0

def run_multiple():
    df=pd.read_excel("cssr_misa_update.xlsx",sheet_name=0)
    # print(df.shape[0])
    bar = progressbar.ProgressBar(maxval=df.shape[0], widgets=[progressbar.Bar('#', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    global barcount
    barcount=0
    # bar.update(barcount)
    
    new_df = df.apply(lambda row: pd.Series(extract_misa(row['GENOME ID'],row['SEGMENT'],row['Accession No.'],bar), index =['cSSR20','cSSR30','cSSR40','cSSR50']), axis=1)
    df=pd.concat([df, new_df], axis=1, join='inner')
    
    bar.finish()
    print(df)
    df.to_excel("cssr_misa_update.xlsx",index=False)
    pass

def replace_fasta_heading(fasta:str,name:str):
    strarr=fasta.split("\n")
    fasta=fasta.replace(strarr[0],">"+name)
    return fasta

def read_misa(accn):
            # copyfrom misa and return df sum of ssr (c or c*)
    df = pd.read_csv("seq_fasta/"+accn+".fasta.misa",
                   sep = '\t',
                   engine = 'python')
    df=df.loc[(df["SSR type"] == 'c') | (df["SSR type"] == 'c*')]
    sm=df["size"].count()
    print(sm)
    os.remove("seq_fasta/"+accn+".fasta.misa")
    os.remove("seq_fasta/"+accn+".fasta.statistics")
    return sm

def extract_misa(name:str,seg:str,accn:str,bar: progressbar.ProgressBar):
    global barcount
    # print(barcount)
    bar.update(barcount)
    barcount=barcount+1
    
    try:
        logger=logging.getLogger()
        if pd.isna(name) or pd.isna(seg) or pd.isna(accn) or (len(seg) != 1):
            return NaN

        accn=accn.split(".")[0]

        # step1-open broser
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
        # copy fasta
        # -----start web scraping--------------------------
        link="https://www.ncbi.nlm.nih.gov/nuccore/"+accn+"?report=fasta"
        logger.info("OPENING PAGE... : "+link)
        driver.get(link)
        fasta_seq=WebDriverWait(driver, 60).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="viewercontent1"]/pre'))
        )
        # print(fasta_seq[0].text)
        bar.update(0)###############################
        # write in new file & append to collection L/M file
        if not os.path.isdir("seq_fasta/"):
            os.system("mkdir seq_fasta")
        f = open("seq_fasta/"+accn+".fasta", "w")
        f.write(fasta_seq[0].text)
        f.close()
        if seg.upper() == 'L' :
            f = open("L_fasta_seq.txt", "a")
            f.write(replace_fasta_heading(fasta_seq[0].text,name)+"\n\n")
            f.close()
        if seg.upper() == 'M':
            f = open("M_fasta_seq.txt", "a")
            f.write(replace_fasta_heading(fasta_seq[0].text,name)+"\n\n")
            f.close()
        if seg.upper() == 'S':
            f = open("S_fasta_seq.txt", "a")
            f.write(replace_fasta_heading(fasta_seq[0].text,name)+"\n\n")
            f.close()
        
        bar.update(0)###############################
        # run misa
        ls=[]
        # for cssr20---------------------------------------
        with open("misa_backup.ini") as f:
            newText=f.read()
        with open("misa.ini", "w") as f:
            f.write(newText)
        os.system("perl misa.pl seq_fasta/"+accn+".fasta")
        bar.update(0)###############################
        ls.append(read_misa(accn))

        
        # for cssr30---------------------------------------
        with open("misa.ini") as f:
            newText=f.read().replace('20', '30')
        with open("misa.ini", "w") as f:
            f.write(newText)
        os.system("perl misa.pl seq_fasta/"+accn+".fasta")
        bar.update(0)###############################
        ls.append(read_misa(accn))

        
        # for cssr40----------------------------------------
        with open("misa.ini") as f:
            newText=f.read().replace('30', '40')
        with open("misa.ini", "w") as f:
            f.write(newText)
        os.system("perl misa.pl seq_fasta/"+accn+".fasta")
        bar.update(0)###############################
        ls.append(read_misa(accn))

        
        # for cssr50---------------------------------------------
        with open("misa.ini") as f:
            newText=f.read().replace('40', '50')
        with open("misa.ini", "w") as f:
            f.write(newText)
        os.system("perl misa.pl seq_fasta/"+accn+".fasta")
        bar.update(0)###############################
        ls.append(read_misa(accn))

        bar.update(0)###############################
        return ls
    except:
        bar.update(0)###############################
        exp.append(accn)
        return NaN
    # pass

###########################################################
if __name__=="__main__":
    start=datetime.now()
    exp=[]

    if os.path.exists("seq_fasta"):
        shutil.rmtree('seq_fasta')
    if os.path.exists("L_fasta_seq.txt"):
        os.remove("L_fasta_seq.txt")
    if os.path.exists("M_fasta_seq.txt"):
        os.remove("M_fasta_seq.txt")

    # extract_misa('BV1L','L','NC_003468')
    # extract_misa('BV1M','M','NC_003467')

    run_multiple()

    print("TIME : "+str(datetime.now()-start))
    print("Exceptions : "+str(len(exp)))
    print(exp)
    pass
