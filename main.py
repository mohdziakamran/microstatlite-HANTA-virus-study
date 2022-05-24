from ast import Return
import concurrent.futures
import logging
import multiprocessing
import os
import shutil
from datetime import datetime
import pyfiglet
import pandas as pd

from src.allssrfilegen import readHANTAAndWriteSSRFile
from src.genefilegenwebscraper import prepareGENEFileFromAccnNum
from src.procssr import process_ssr_file_for_accnum
from src.runIGLSFexe import runIGLSFapp


def main(inp:str):
    logger=logging.getLogger(__name__)
    startTime=datetime.now()

    try:
        os.system('TASKKILL /F /IM excel.exe')
    except:
        pass
    
    if not os.path.exists('src/chromedriver.exe'):
        logger.info('~~~~~# COPYING CHROME DRIVER IN /SRC #~~~~~')
        shutil.copyfile('chromedriver.exe','src/chromedriver.exe')
    
    executor = concurrent.futures.ProcessPoolExecutor(20)
    m = multiprocessing.Manager()
    faulterList=m.dict()
    accnList_segment=m.list()
    dict_list=m.list()
    

    # --------generating SSR file from HANTA... -----------------
    if inp in [1]:
        inpFile='HANTAAAAAAA.xlsx'
        logger.info('MAIN INPUT FILE : '+inpFile)
        accnList=readHANTAAndWriteSSRFile(inpFile)

    # ---read accn list from faulter and start from gene file generation-----
    if inp in [6]:
        try :
            accnList=[]
            with open('faulter_list.txt', 'r') as file:
                data_list = file.read().replace('\n', '').strip().split('|')
            for elem in data_list:
                elem_ls=elem.split(',')
                # accnList_segment.append((elem_ls[0],elem_ls[1]))
                # accnList=accnList_segment
                accnList.append(elem_ls[0])
            print("APP STARTED...")
        except:
            logger.error("EXCEPTION WHILE READING FILE FROM FAULTER_LIST.TXT-READ")
            return

    # --------generage Gene file -------------------
    if inp in [1,6]:
        # executor = concurrent.futures.ProcessPoolExecutor(20)
        futures = [executor.submit(prepareGENEFileFromAccnNum, an, accnList_segment, faulterList) for an in accnList]
        concurrent.futures.wait(futures)
        gene_file_gen_count=len(accnList)-len(faulterList)
        # ---sequential--
        # for an in accnList:
        #     GenGeneFile(an)


    if inp in [3,4]:
        # accnList=[]

        print("GIVE (ACCN NUMs,SEGMENT) :")
        print( "Eg:")
        print( "NC_003466,L")
        print( "L39949,S")
        print("...")
        print("TYPE 'DONE' WHEN FINISHED.\n")
        acc_ls_inp=input('>')
        while acc_ls_inp.upper() != 'DONE':
            if acc_ls_inp!='':
                inp_arr=acc_ls_inp.split(',')
                # accnList_segment.append((inp_arr[0].strip(),inp_arr[1].strip().upper()))
                try : accnList_segment.append((inp_arr[0].strip(),inp_arr[1].strip().upper()))
                except: print('WRONG DATA!!! PLEASE SEE EG.')
            acc_ls_inp=input('>')
        print("APP STARTED...")
        accnList=accnList_segment

    if inp in [5]:
        try :
            with open('faulter_list.txt', 'r') as file:
                data_list = file.read().replace('\n', '').strip().split('|')
            for elem in data_list:
                elem_ls=elem.split(',')
                accnList_segment.append((elem_ls[0],elem_ls[1]))
                accnList=accnList_segment
            print("APP STARTED...")
        except:
            logger.error("EXCEPTION WHILE READING FILE FROM FAULTER_LIST.TXT-READ")
            return

    # -------run IGLSF app for all accn number except for faulter list ------------
    if inp in [1,3,5,6]:
        # executor = concurrent.futures.ProcessPoolExecutor(2)
        lock = m.Lock()
        futures = [executor.submit(runIGLSFapp, ansg[0], lock, faulterList) for ansg in accnList_segment]
        concurrent.futures.wait(futures)
        # -----sequential----
        # for an in accnList:
        #     runIGLSF(an)


    # ------process Modified SSR file-----------------------
    if inp in [1,3,4,5,6]:
        futures = [executor.submit(process_ssr_file_for_accnum, ansg[0],ansg[1], dict_list, faulterList) for ansg in accnList_segment]
        concurrent.futures.wait(futures)
        main_df=pd.DataFrame.from_records(dict_list)
        if(inp in [5,6]):
            old_df=pd.read_excel("Main_Result_File.xlsx",sheet_name=0)
            main_df=main_df.append(old_df)
        main_df.to_excel("Main_Result_File.xlsx",index=False)

    # ------write faulter list file if possible to path---------
    try:
        faulter_str=''
        flk=faulterList.keys()
        for an_sg in accnList_segment:
            # if an_sg[0] in flk & 'FAILED AT GENE FILE GENRATION' not in an_sg[1] : faulter_str=faulter_str+an_sg[0]+','+an_sg[1]+'|'
            if an_sg[0] in flk : faulter_str=faulter_str+an_sg[0]+','+an_sg[1]+'|'
        if len(faulter_str)!=0:
            file=open('faulter_list.txt','w')
            file.write(faulter_str[:-1])
            file.close
            # faulterList['FAULTER_LIST.TXT-WRITE']="SUCCESS"
        # faulterList['FAULTER_LIST.TXT-WRITE']="EMPTY, NOT CREATED"
    except :
        logger.error("EXCEPTION WHILE CREATING FAULTER TEXT FILE")
        # faulterList['FAULTER_LIST.TXT-WRITE']="FAILED"

    # -------REPORT SECTION
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    report_banner = pyfiglet.figlet_format("REPORT")
    # print(ascii_banner)
    logger.info("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"+report_banner)        
    # logger.info('===================================================================')
    # logger.info('++++++++++++++++++++++++++++ REPORT : +++++++++++++++++++++++++++++')
    # logger.info('===================================================================')
    logger.info('TIME TAKEN : '+str(datetime.now()-startTime))
    logger.info('TOTAL INITIAL COUNT : '+str(len(accnList)))
    logger.info('TOTAL SUCCESS COUNT : '+str(len(accnList)-len(faulterList)))
    if inp in [1]:
        logger.info('TOTAL SSR FILE GENRATED : '+str(len(accnList)))
        logger.info('TOTAL GENE FILE GENERATED : '+str(gene_file_gen_count))
    if inp in [1,3,5]:
        logger.info('TOTAL SSR FILE MODEFIED BY IGLSF APP : '+str(len(accnList)-len(faulterList)))
    logger.info('FAILED ACCN NUMs : '+str(len(faulterList)))
    for an in faulterList.keys():
        logger.info(an+'\t: '+faulterList[an])
    
    logger.info("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    
    # if faulter file exist in path then give option for rerun with faulter list? from IGLSF default
    # step 1 write faulter accn nums to file 
    # y/n options 
    if os.path.exists("faulter_list.txt"):
        print()
        print()
        print("THERE IS SOME FAILURE CASE FOUND, DO YOU WISH TO RE-RUN THEM FROM IGLFS APP EXECUTION AGAIN?")
        re_inp=input("TYPE 'Y' FOR YES / 'N' FOR NO (Y/N)>")

        while re_inp.upper() not in ['Y','N']:
            re_inp=input("TYPE 'Y' FOR YES / 'N' FOR NO (Y/N)>")
        if re_inp.upper() == 'Y':
            main(6)
# ##############################################################


if __name__=='__main__':

    # ----------Print Banner-------------
    ascii_banner = pyfiglet.figlet_format("IGLSF Automation")
    print(ascii_banner)
    # ----SELECT OPTIONS --------
    print("***ALL CREDIT GOES TO ~ RANA TASKEEN")
    print()
    print("NOTE : DON'T USE MOUSE AND KEYBOARD WHILE EXECUTION")
    print("NOTE : MAKE SURE TO ADD / UPDATE DATA IN 'HANTAAAA.XLSX' FILE")
    print("NOTE : SEE LOGS FOR EXECUTION IN 'logfile.log' FILE")
    print("NOTE : SEE END RESULT IN 'MAIN RESULT FILE' EXCEL FILE")
    print("===================================================")
    print("\nSELECT AN OPTION TO START ")
    print("1. START FROM BGINNING")
    print("2. ADVANCE OPTIONS")
    print()
    opts=[1,2]
    inp=-1
    while inp not in [1,2]:
        inp=input('TYPE OPTION =>')
        try : inp=int(inp)
        except : 
            print("Please Select Above Options")
            inp=-1
    
    if inp in [1]:
        print("APP STARTED...")
    
    if inp==2:
        print("=> | (MAKE SURE THAT SSR FILE AND GENE FILE IS UPDATED), REQUIRE : ACCN NUMS")
        print("3. START FROM IGLSF APP RUN ")
        print("4. START FROM PROCESSING UPDATED SSR FILE AND GENERATE MAIN EXCEL FILE ")
        print("5. START FROM IGLSF APP RUN, READ DATA FROM FAULTER_LIST.TXT ")
        print("6. START FROM Gene Fiel Generation, READ DATA FROM FAULTER_LIST.TXT ")
        print()
        while not inp in [3,4,5,6]:
            inp=input('TYPE OPTION =>')
            try : inp=int(inp)
            except : 
                print("Please Select Above Options")
                inp=-1

    # --------- Start Executions ----------------
    if inp in [1] and os.path.exists("logfile.log"):
        os.remove("logfile.log")

    # --Logger config-----
    logging.basicConfig(handlers=[
                logging.FileHandler("logfile.log"),
                logging.StreamHandler()
            ],
            # format = "%(levelname)s %(asctime)s - %(name)s : %(message)s", 
            format=('[%(asctime)s| %(levelname)s| %(processName)s] - %(name)s : %(message)s'),
            level = logging.INFO)

    if inp in [1]:
        try:
            os.system('TASKKILL /F /IM excel.exe')
            if os.path.exists("ssr_data"):
                shutil.rmtree('ssr_data')
            if os.path.exists("gene_data"):
                shutil.rmtree('gene_data')
            os.makedirs('ssr_data')
            os.makedirs('gene_data')
        except :
            logging.error("Some Files Are Left Open,Unable To Get Access. \nPlease Try To Close Oppened File And Try Again !!!")
            os._exit(1)
    
    main(inp)








