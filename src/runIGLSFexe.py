# from pywinauto import application
import os
import subprocess
import time
from asyncio import Handle
from cgitb import handler
from socket import timeout
from turtle import title

from pywinauto.application import Application


def runIGLSFapp(accetionCode:str):
    print('~~~~~# STARTED RUNNING IGLSF APP FOR Accession Number : '+accetionCode+' #~~~~~') #logger*****

    # TODO replace the path with os path 
    mainPath=os.getcwd()
    # print(mainPath)
    # geneinputfile:str=r"C:\Users\User\OneDrive\Desktop\gitrepo\Gene_File_GR203.xlsx"
    # ssrinputfile:str=r"C:\Users\User\OneDrive\Desktop\gitrepo\SSR_File_GR203.xlsx"
    geneinputfile:str="gene_data\Gene_File_"+accetionCode+".xlsx"
    ssrinputfile:str="ssr_data\SSR_File_"+accetionCode+".xlsx"

    pid = subprocess.Popen(["IGLSF.exe"]).pid
    app=Application().connect(process=pid,timeout=120)
    myapp=app.IGLSF.wait('visible',timeout=120)

    # for Gene input file----------------
    obj=app.IGLSF.SunAwtCanvas7
    obj.draw_outline()
    obj.click_input()
    dirwin=Application().connect(title='Choose a gene file:',found_index=0,timeout=60)
    dirwin.ChooseAGeneFile.wait('visible')

    edt=dirwin.ChooseAGeneFile.FileNameEdit
    # edt.draw_outline()
    # edt.click_input()
    edt.type_keys(geneinputfile)
    dirwin.ChooseAGeneFile.Open.click_input()
    # ------------------------------------

    app.IGLSF.wait('visible')


    # for SSR input file----------------
    obj=app.IGLSF.SunAwtCanvas5
    obj.draw_outline()
    obj.click_input()
    dirwin=Application().connect(title='Choose an SSR file:',found_index=0,timeout=20)
    dirwin.ChooseAGeneFile.wait('visible')

    edt=dirwin.ChooseAGeneFile.FileNameEdit
    # edt.draw_outline()
    # edt.click_input()
    edt.type_keys(ssrinputfile)
    dirwin.ChooseAGeneFile.Open.click_input()
    # ------------------------------------

    # for Simulation Click---------------
    obj=app.IGLSF.SunAwtCanvas3
    obj.draw_outline()
    obj.click_input()
    # -----------------------------------

    # open the lock
    # and wait logic
    Application().connect(title='SSR_File_'+accetionCode+' - Excel',found_index=0,timeout=60)
    time.sleep(10)
    # Application().connect(title='SSR_File_GR203 - Excel',found_index=0,timeout=60)
    print('~~~~~# UPDATED SSR FILE FOR Accession Number : '+accetionCode+' #~~~~~') #logger*****


# ##################################################################
if __name__=='__main__':
    runIGLSFapp("AB186420")
