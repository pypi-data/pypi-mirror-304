import re
import pandas as pd
import numpy as np

import argparse

from Bio import SeqIO


# argument parser defaults 
MASTER_KINASE_LIST = '../data/STYE_KinaseNames_finalkeyV2.csv'


def main():
    # parse arguments
    args = parse_args()
    
    # load variant data 
    fname = args.i
    if args.o is None:
        fname_out = fname[:-4] + '_filtered.txt'
    else:
        fname_out = args.o
    df = pd.read_csv(fname, delimiter='\t') 
    
    print("shape of unfiltered data:", df.shape)
    
    # load kinase names 
    kinase_names = pd.read_csv('../data/STYE_KinaseNames_finalkeyV2.csv')

    # drop proteins where the ProteinName column is undefined
    kinase_names = kinase_names.dropna(axis=0, subset=['ProteinName'])

    # get kinase sequences 
    records = SeqIO.parse('../../../alt_splicing/rawdata/uniprot_sprot.fasta', 'fasta')
    query = r'^.+OS=Homo sapiens.+GN=(\S+).+$'
    records = list(filter(lambda rec: re.search(query, rec.description) is not None, records))
    records = dict(map(lambda rec: (re.search(query, rec.description).group(1), str(rec.seq)), 
                       records))

    kinase_names['Kinase_seq'] = kinase_names['ProteinName'].apply(lambda name: records[name])
    
    # filter out non-valid kinase entries  
    filtered_df = filter_kinases(df, kinase_names)
    
    # print shape of final data 
    print("filtered dataframe shape:", filtered_df.shape)
    
    # write to file 
    filtered_df.to_csv(fname_out)
    print("wrote filtered dataframe to file", fname_out)


def get_protein_change_from_name(s, query):
    search = re.search(query, s)
    if search:
        return search.group(2)
    else:
        return np.nan
        

def filter_kinases(variant_data, kinase_info):
    query_protein_name = r'^NM_[0-9.]+\((.+)\):c\.\S+\s\(p.([A-Za-z]{3}[0-9]+[A-Za-z]{3})\)'
    query_gene_names = r'^NM_[0-9.]+\((.+)\).+$'
    
    kinase_set = set(kinase_info['ProteinName'].tolist())
    
    # filtering based on kinase_names 
    is_kinase = variant_data['Name'].apply(lambda s: (re.search(query_gene_names, s) is not None) and (re.search(query_gene_names, s).group(1) in kinase_set))
    
    variant_data = variant_data[is_kinase]
    
    return variant_data 


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='name of input variant file')
    parser.add_argument('-o', type=str, required=False, default=None, help='name of output (filtered) variant file')
    parser.add_argument('--kinase-list', type=str, required=False, default=MASTER_KINASE_LIST, help='name of master kinase list file')
    args = parser.parse_args()
    return args 


if __name__ == '__main__': 
    main()