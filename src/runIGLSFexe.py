# from pywinauto import application
import os
import subprocess
import time
from socket import timeout
import multiprocessing
import concurrent.futures

from pywinauto.application import Application
import pywinauto
from ctypes import *


def runIGLSFapp(accetionCode:str , lock:multiprocessing.Lock, faulter):
    try:
        print('~~~~~# STARTED RUNNING IGLSF APP FOR Accession Number : '+accetionCode+' #~~~~~') #logger*****
        wait_time=5

        # TODO replace the path with os path 
        # mainPath=os.getcwd()
        # print(mainPath)
        # geneinputfile:str=r"C:\Users\User\OneDrive\Desktop\gitrepo\Gene_File_GR203.xlsx"
        # ssrinputfile:str=r"C:\Users\User\OneDrive\Desktop\gitrepo\SSR_File_GR203.xlsx"
        geneinputfile:str="gene_data\Gene_File_"+accetionCode+".xlsx"
        ssrinputfile:str="ssr_data\SSR_File_"+accetionCode+".xlsx"

        pid = subprocess.Popen(["IGLSF.exe"]).pid
        # lock acquire
        app=Application().connect(process=pid,timeout=120)
        app.IGLSF.wait('visible',timeout=120)
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


        exl=Application().connect(title='SSR_File_'+accetionCode+' - Excel',timeout=60)
        exl.window(title_re=u'SSR_File_'+accetionCode+' - Excel').wait('ready').close()
        app.kill()
        
        print('~~~~~# UPDATED SSR FILE FOR Accession Number : '+accetionCode+' #~~~~~') #logger*****
    except :
        print('IGLSF APP EXECUTION FAILED FOR ACCN NUM : '+accetionCode)
        faulter.append((accetionCode,'FAILED AT IGLSF APP EXECUTION'))
        print('ACCN NUM : '+accetionCode+', Added To Faulter')



# ##################################################################
if __name__=='__main__':
    executor = concurrent.futures.ProcessPoolExecutor(1)
    m = multiprocessing.Manager()
    lock = m.Lock()
    fut=[]
    futures = [executor.submit(runIGLSFapp, an, lock, fut) for an in ["AB186420","AF005727"]]
    concurrent.futures.wait(futures)
    # runIGLSFapp(accetionCode="AB186420",lock= multiprocessing.Lock())

    print(fut)
