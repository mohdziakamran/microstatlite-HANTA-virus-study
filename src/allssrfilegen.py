import logging
import pandas as pd


def readHANTAAndWriteSSRFile(inpFile:str):
    logger=logging.getLogger(__name__)
    logger.info('~~~~~# Came in for Read HANTA... File and Generate SSR File #~~~~~')
    # print('~~~~~# Came in for Read HANTA... File and Generate SSR File #~~~~~') #logger*****
    logger.info('READING INPUT FILE : %s',inpFile)
    # print('READING INPUT FILE : '+inpFile)
    accnNumList=[]

    # ------panda aproach---------
    df=pd.read_excel(inpFile,sheet_name=0)
    df['ID']=df['ID'].apply(lambda x:x.split('.')[0])
    # change HDR
    df.rename(columns={'SSR nr.':'S.No','SSR':'Consensus','start':'Start','end':'End'},inplace=True)
    grpDf=df.groupby('ID')
    # print(df)
    for accnNum, eachDf in grpDf:
        accnNumList.append(accnNum)
        # remove row with sst type as c or c*
        eachDf=eachDf[(eachDf['SSR type'] != 'c') & (eachDf['SSR type'] != 'c*')]
        # select columns
        eachDf=eachDf[['S.No','Consensus','Start','End']]
        # add empty colummn
        eachDf['SSR Location in Gene'] = ''
        # write excel file
        eachDf.to_excel("ssr_data/SSR_File_"+accnNum+".xlsx",index=False)

    # print('~~~~~# ALL SSR FILE GENERATED #~~~~~') #logger*****
    logger.info('~~~~~# ALL SSR FILE GENERATED #~~~~~')
    return accnNumList
    


# ##############################################
if __name__=='__main__':
    logging.basicConfig(handlers=[
                        logging.FileHandler("logfile.log"),
                        logging.StreamHandler()
                    ],
                    format = "%(levelname)s %(asctime)s - %(name)s : %(message)s", 
                    level = logging.DEBUG)
    inpFile='HANTAAAAAAA.xlsx'
    readHANTAAndWriteSSRFile(inpFile)