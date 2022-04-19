import pandas as pd
from openpyxl import Workbook
import openpyxl


def readHANTAAndWriteSSRFile():
    print('~~~~~# Came in for Read HANTA... File and Generate SSR File #~~~~~') #logger*****
    inpFile='HANTAAAAAAA.xlsx'
    print('reading file from : '+inpFile)
    mainDict={}

    # ------panda aproach---------
    df=pd.read_excel(inpFile,sheet_name=0)
    df['ID']=df['ID'].apply(lambda x:x.split('.')[0])
    # change HDR
    df.rename(columns={'SSR nr.':'S.No','SSR':'Consensus','start':'Start','end':'End'},inplace=True)
    grpDf=df.groupby('ID')
    print(df)
    for accnNum, eachDf in grpDf:
        # remove row with sst type as c or c*
        eachDf=eachDf[(eachDf['SSR type'] != 'c') & (eachDf['SSR type'] != 'c*')]
        # select columns
        eachDf=eachDf[['S.No','Consensus','Start','End']]
        # add empty colummn
        eachDf['SSR Location in Gene'] = ''
        # write excel file
        eachDf.to_excel("ssr_data/SSR_File_"+accnNum+".xlsx",index=False)

        # print(accnNum)
        # print(eachDf)
        # print()

    print('~~~~~# ALL SSR FILE GENERATED #~~~~~') #logger*****
    


# ##############################################
if __name__=='__main__':
    readHANTAAndWriteSSRFile()