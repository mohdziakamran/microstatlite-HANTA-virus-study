import logging
import pandas as pd

from .mplogger import create_logger



def process_ssr_file_for_accnum(accn:str, segment:str, dict_list:list, faulter:dict):
    # logger= logging.getLogger(__name__)
    logger=create_logger(__name__)
    if accn in faulter.keys(): return
    try:
        logger.info('~~~~~# Came in for Process SSR file And Generate Main Excel File for ACCn Num : %s #~~~~~',accn) #logger*****

        input_file_path="ssr_data/SSR_File_"+accn+".xlsx"
        df=pd.read_excel(input_file_path,sheet_name=0)
        df['Consensus']=df['Consensus'].apply(lambda x:x.replace('(',')').split(')')[1])

        total_count=df.shape[0]
        
        # ---------------For NC Part------------------------
        NC_df=df.loc[df['SSR Location in Gene'] == 'NC']
        # total_NC_count=NC_df.shape[0]

        # Mono CDS count
        # mono_cds_count=NC_df.query("Consensus.str.len() == 6", engine="python").shape[0]
        # print(mono_cds_count)
        
        # ---------------For CDS part-------------------------
        CDS_df=df.loc[df['SSR Location in Gene'] != 'NC']
        # total_CDS_count=CDS_df.shape[0]


        # -------------------create dict for df--------------------
        try:
            dict_for_df={
                'Genome ID'     : 0,
                'Accn Num'      : accn,
                'SEGMENT'       : segment,
                'Total CDS'     : CDS_df.shape[0],
                'Total NCS'     : NC_df.shape[0],
                'Mono CDS'      : CDS_df.query("Consensus.str.len() == 1", engine="python").shape[0],
                'Di CDS'        : CDS_df.query("Consensus.str.len() == 2", engine="python").shape[0],
                'Tri CDS'	    : CDS_df.query("Consensus.str.len() == 3", engine="python").shape[0],
                'Tetra CDS'	    : CDS_df.query("Consensus.str.len() == 4", engine="python").shape[0],
                'Penta CDS'	    : CDS_df.query("Consensus.str.len() == 5", engine="python").shape[0],
                'Hexa CDS'	    : CDS_df.query("Consensus.str.len() == 6", engine="python").shape[0],
                'Mono NCS'	    : NC_df.query("Consensus.str.len() == 1", engine="python").shape[0],
                'Di NCS'        : NC_df.query("Consensus.str.len() == 2", engine="python").shape[0],
                'Tri NCS'	    : NC_df.query("Consensus.str.len() == 3", engine="python").shape[0],
                'Tetra NCS'	    : NC_df.query("Consensus.str.len() == 4", engine="python").shape[0],
                'Penta NCS'	    : NC_df.query("Consensus.str.len() == 5", engine="python").shape[0],
                'Hexa NCS'      : NC_df.query("Consensus.str.len() == 6", engine="python").shape[0]
            }
            logger.info('%s : DICT PREPARED - '+str(dict_for_df),accn)
        except:
            logger.error('PREP BASIC DICT DETAIL FAILED FOR ACCN NUM : %s',accn)
            faulter[accn]='SEG='+segment+'FAILED AT PROCESSING SSR DATA FOR PREP BASIC DICT DETAIL'
            return
        # -------------Add additional column to dict----------------------
        try:
            CDS_df['SSR Location in Gene']=CDS_df['SSR Location in Gene'].apply(lambda x:x.strip(",.").lower())
            CDS_grpDf=CDS_df.groupby('SSR Location in Gene')
            for protien, eachDf in CDS_grpDf:
                dict_for_df[protien]=eachDf.shape[0]
        except:
            logger.error('PREP SPECIAL DICT DETAIL FAILED FOR ACCN NUM : %s',accn)
            faulter[accn]='SEG='+segment+'FAILED AT PROCESSING SSR DATA FOR PREP PROTIEN SPECIAL DICT DETAIL'
            return

        # -------Add Dict to list------------------------------
        dict_list.append(dict_for_df)

        # print(dict_for_df)
        
        logger.info('~~~~~# ADDED PREPARED DICT TO LIST FOR ACCN NUM : '+accn+' #~~~~~') #logger*****

    except:
        logger.error('PREPARING DICT FAILED FOR ACCN NUM : '+accn)
        faulter[accn]='SEG='+segment+'FAILED AT PROCESSING SSR DATA FOR DICT PREP'




######################################################

if __name__=='__main__':
    # logging.basicConfig(handlers=[
    #          # logging.FileHandler("logfile.log"),
    #             logging.StreamHandler()
    #         ],
    #         format = "%(levelname)s %(asctime)s - %(name)s : %(message)s", 
    #         level = logging.INFO)
    dictls=[]
    ls={}
    dict=process_ssr_file_for_accnum('L36930','',dictls,ls)
    print(dictls)
    print(ls)
    pass