import os
import shutil
import concurrent.futures
from datetime import datetime 
import multiprocessing

from src.allssrfilegen import readHANTAAndWriteSSRFile
from src.genefilegenwebscraper import prepareGENEFileFromAccnNum
from src.runIGLSFexe import runIGLSFapp


# # --------generage Gene file -------------------

# def GenGeneFile(an):
#     try:
#         prepareGENEFileFromAccnNum(an)
#     except :
#         print('GENE FILE GENRATION FAILED FOR ACCN NUM : '+an)
#         faulterList.append(an,'FAILED AT GENE FILE GENRATION')
#     print()


# # -------run IGLSF app for all accn number except for faulter list ------------
# def runIGLSF(an,lock):
#     if not an in faulterList:
#             try:
#                 runIGLSFapp(an,lock)
#             except :
#                 print('IGLSF APP EXECUTION FAILED FOR ACCN NUM : '+an)
#                 faulterList.append(an)
#             print()



# ##############################################################

if __name__=='__main__':
    startTime=datetime.now()

    if not os.path.exists('src/chromedriver.exe'):
        print('~~~~~# COPYING CHROME DRIVER IN /SRC #~~~~~')
        shutil.copyfile('chromedriver.exe','src/chromedriver.exe')
    
    executor = concurrent.futures.ProcessPoolExecutor(10)
    faulterList=[]

    # --------generating SSR file from HANTA... -----------------
    inpFile='HANTAAAAAAA.xlsx'
    print('MAIN INPUT FILE : '+inpFile)
    accnList=readHANTAAndWriteSSRFile(inpFile)


    # --------generage Gene file -------------------
    # executor = concurrent.futures.ProcessPoolExecutor(20)
    futures = [executor.submit(prepareGENEFileFromAccnNum, an, faulterList) for an in accnList]
    concurrent.futures.wait(futures)
    # ---sequential--
    # for an in accnList:
    #     GenGeneFile(an)


    # -------run IGLSF app for all accn number except for faulter list ------------
    
    # executor = concurrent.futures.ProcessPoolExecutor(2)
    m = multiprocessing.Manager()
    lock = m.Lock()
    futures = [executor.submit(runIGLSFapp, an, lock, faulterList) for an in accnList]
    concurrent.futures.wait(futures)
    # -----sequential----
    # for an in accnList:
    #     runIGLSF(an)


    # ------process Modified SSR file-----------------------



    # -------
    print('~~~~~# REPORT :')
    print('TIME TAKEN : '+str(datetime.now()-startTime))
    print('FAILED ACCN NUMs : '+str(len(faulterList)))
    for an in faulterList:
        print(an[0]+'\t: '+an[1])



