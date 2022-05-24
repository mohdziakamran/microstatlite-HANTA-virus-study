
from asyncio.windows_events import NULL
import os
import pandas as pd


def aggrigate_data():
    df=pd.read_excel("geneId_gene_start_end.xlsx",sheet_name=0)

    new_df = df.apply(lambda row: pd.Series(run(row['Accession No.']), index =['GENE','START','END']), axis=1)
    df=pd.concat([df, new_df], axis=1, join='inner')

    print(df)
    df.to_excel("new_geneId_gene_start_end.xlsx",index=False)

    pass


def run(accn:str):
    if os.path.exists("../../gene_data/Gene_File_"+str(accn)+".xlsx"):
        if pd.isna(accn):
                return NULL
        accn=accn.split(".")[0]
        df2=pd.read_excel("../../gene_data/Gene_File_"+accn+".xlsx",sheet_name=0)
        if df2.shape[0] >1:
            return ["more than one gene data found","",""]
        return [df2["GENE"][0],df2["START"][0],df2["END"][0]]
    return NULL

# ######################################

if __name__=="__main__":
    aggrigate_data()
    pass