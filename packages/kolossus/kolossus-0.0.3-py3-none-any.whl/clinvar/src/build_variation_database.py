
import gzip
import pickle

import re

import pandas as pd 
import numpy as np

# for custom functions 
from clinvar_xml_parsing import get_variation_archive_info


def main():
    # note: I already checked, no accession overlap
    fnames = {'benign': '../data/clinvar_result_msmuts_benign_0930_filtered.txt',
              'pathogenic': '../data/clinvar_result_msmuts_pathogenic_09_24_filtered.txt'}
    
    accs = {key: set(pd.read_csv(fnames[key])['Accession'].tolist()) for key in fnames}
    
    # these are the accessions of interest 
    accessions_of_interest = accs['benign'].union(accs['pathogenic'])
    
    # query for start and end of variation archive 
    query_start = r'<VariationArchive.*>'
    query_end = r'</VariationArchive.*>'

    A = {}
    block_ct = 0    # target: 508,908
    with gzip.open('/hpc/group/singhlab/rawdata/ClinVarVCVRelease_00-latest.xml.gz', 'rt') as f:
#         ct = 0
        while True:
            line = f.readline()

            if not line: 
                break 

            # look for beginning of variation archive record 
            if re.search(query_start, line):
                accession, info = get_variation_archive_info(line, f, query_end)

                
                block_ct += 1
                # only save records for archives of interest 
                if accession not in accessions_of_interest:
                    continue
                    
                if accession not in A:
                    A[accession] = info
                else:
                    A[accession].append(info)
                
                print("wrote accession", accession, "to A,", len(A), "/", len(accessions_of_interest), "mapped so far")

#             ct += 1
#             if ct > 2000:
#                 break 

    print("parsed", block_ct, "blocks to obtain", len(A), "records")
    with open("../data/clinvar_to_protein_accessions_of_interest.pkl", 'wb') as f:
        pickle.dump(A, f)
    

if __name__ == '__main__': 
    main()
