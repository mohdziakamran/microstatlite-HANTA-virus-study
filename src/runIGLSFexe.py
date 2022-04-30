# from pywinauto import application
import logging
import os
import subprocess
import time
from socket import timeout
import multiprocessing
import concurrent.futures

from pywinauto.application import Application
import pywinauto
from ctypes import *

from .mplogger import create_logger


def runIGLSFapp(accetionCode:str , lock:multiprocessing.Lock, faulter:dict):
    # logger=logging.getLogger(__name__)
    logger=create_logger(__name__)
    if accetionCode in faulter.keys(): return
    try:
        logger.info('~~~~~# STARTED RUNNING IGLSF APP FOR Accession Number : '+accetionCode+' #~~~~~') #logger*****
        wait_time=5

        # TODO replace the path with os path 
        # mainPath=os.getcwd()
        # print(mainPath)
        # geneinputfile:str=r"C:\Users\User\OneDrive\Desktop\gitrepo\Gene_File_GR203.xlsx"
        # ssrinputfile:str=r"C:\Users\User\OneDrive\Desktop\gitrepo\SSR_File_GR203.xlsx"
        geneinputfile:str="gene_data\Gene_File_"+accetionCode+".xlsx"
        ssrinputfile:str="ssr_data\SSR_File_"+accetionCode+".xlsx"
        if not  (os.path.exists(ssrinputfile) and os.path.exists(geneinputfile) ):
            logger.info('ACCN NUM : %s, SSR_File Exist : %s | GENE_File Exist : %s',accetionCode,str(os.path.exists(ssrinputfile)),str(os.path.exists(geneinputfile)))
            raise Exception()

        pid = subprocess.Popen(["IGLSF.exe"]).pid
        # lock acquire
        app=Application().connect(process=pid,timeout=60)
        app.IGLSF.wait('visible',timeout=60)
        time.sleep(wait_time)

        # for Gene input file----------------
        # obj=app.IGLSF.SunAwtCanvas7
        # obj.draw_outline()
        # obj.click_input()
        # dirwin=Application().connect(title='Choose a gene file:',found_index=0,timeout=60)
        # dirwin.ChooseAGeneFile.wait('visible')

        # edt=dirwin.ChooseAGeneFile.FileNameEdit
        # # edt.draw_outline()
        # # edt.click_input()
        # edt.type_keys(geneinputfile)
        # dirwin.ChooseAGeneFile.Open.click_input()
        # ---------------------------------------
        # time.sleep(2)
        with lock:
            app.IGLSF.SunAwtCanvas7.set_focus().click_input()
            dirwin=Application().connect(title='Choose a gene file:',found_index=0,timeout=60)
            dirwin.ChooseAGeneFile.wait('visible')
            dirwin.ChooseAGeneFile.FileNameEdit.set_focus().set_edit_text(geneinputfile)
            dirwin.ChooseAGeneFile.Open.set_focus().click_input()
        # ==========================================
        time.sleep(wait_time)

        # # for SSR input file----------------
        # obj=app.IGLSF.SunAwtCanvas5
        # obj.draw_outline()
        # obj.click_input()
        # dirwin=Application().connect(title='Choose an SSR file:',found_index=0,timeout=20)
        # dirwin.ChooseAGeneFile.wait('visible')

        # edt=dirwin.ChooseAGeneFile.FileNameEdit
        # # edt.draw_outline()
        # # edt.click_input()
        # edt.type_keys(ssrinputfile)
        # dirwin.ChooseAGeneFile.Open.click_input()
        # # ------------------------------------
        with lock:
            app.IGLSF.SunAwtCanvas5.set_focus().click_input()
            dirwin=Application().connect(title='Choose an SSR file:',found_index=0,timeout=60)
            dirwin.ChooseAGeneFile.wait('visible')
            dirwin.ChooseAGeneFile.FileNameEdit.set_focus().set_edit_text(ssrinputfile)
            dirwin.ChooseAGeneFile.Open.set_focus().click_input()
        # ===============================================
        time.sleep(wait_time)

        # # for Simulation Click---------------
        # obj=app.IGLSF.SunAwtCanvas3
        # obj.draw_outline()
        # obj.click_input()
        # # -----------------------------------
        with lock:
            app.IGLSF.SunAwtCanvas3.set_focus().click_input()
        # ====================================
        time.sleep(wait_time)

        try :
            
            exl=Application().connect(title='SSR_File_'+accetionCode+' - Excel',timeout=120)
            time.sleep(wait_time)
            exl.window(title_re=u'SSR_File_'+accetionCode+' - Excel').wait('visible').set_focus().close()
        except:
            logger.error('Failed To Close Excel For ACCN NUM : %s',accetionCode)    

        logger.info('~~~~~# UPDATED SSR FILE FOR Accession Number : '+accetionCode+' #~~~~~') #logger*****
    except :
        logger.error('IGLSF APP EXECUTION FAILED FOR ACCN NUM : '+accetionCode)
        # with lock:
        # faulter.append((accetionCode,'FAILED AT IGLSF APP EXECUTION'))
        faulter[accetionCode]='FAILED AT IGLSF APP EXECUTION ~ {SSR file Path : '+os.getcwd()+'\\'+ssrinputfile+' | GENE file Path : '+os.getcwd()+'\\'+geneinputfile+' }'
        logger.info('ACCN NUM : %s, Added To Faulter',accetionCode)
    finally:
        app.kill()


# ##################################################################
if __name__=='__main__':
    # multiprocessing.log_to_stderr(level=logging.INFO, handlers=[
    #                 logging.FileHandler("logfile.log"),
    #                 logging.StreamHandler()
    #             ])
    # logging.basicConfig(handlers=[
    #                 logging.FileHandler("logfile.log"),
    #                 logging.StreamHandler()
    #             ],
    #             format = "%(levelname)s %(asctime)s - %(name)s : %(message)s", 
    #             level = logging.INFO)

    executor = concurrent.futures.ProcessPoolExecutor(1)
    m = multiprocessing.Manager()
    lock = m.Lock()
    faulter=m.dict()
    futures = [executor.submit(runIGLSFapp, an, lock, faulter) for an in ["AF482717"]]#,"AF005727"]]
    concurrent.futures.wait(futures)
    # runIGLSFapp(accetionCode="AB186420",lock= multiprocessing.Lock(), faulter=faulter)

    print(faulter)
