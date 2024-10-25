
import re 

import pickle 
import argparse 

import os
import sys
import time

import functools

# string io operations 
from io import StringIO

# BioPython
from Bio import Entrez
from Bio.Entrez import efetch
from Bio import SeqIO

from Bio.Data.IUPACData import protein_letters_3to1

from urllib.error import HTTPError

Entrez.email = 'aditya.parekh@duke.edu'

# custom functions 
sys.path.append('/hpc/home/aap100/src')
from aprkh_utils.stringops import apply_subs
from aprkh_utils import delay 
from aprkh_utils import batch_list

# for parsing mutations 
# Note that there are three queries which have complex (non-simple) substitutions:
# ['VCV000003030', 'VCV000140897', 'VCV001701565']
SUB_QUERY = re.compile(r'^p.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})$')
SUB_QUERY2 = re.compile(r'^p.([A-Z][a-z]{2}\d+(_([A-Z][a-z]{2})(\d+))+)delins(([A-Z][a-z]{2})+)$')

SIMPLE_QUERY = re.compile(r'^p.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})$')
DELINS_QUERY = re.compile(r'^p.(\S+)delins(\S+)$')


def main():
    fname = '../data/clinvar_to_protein_accessions_of_interest.pkl'
    fname_out = '../data/clinvar_to_protein_accessions_of_interest_with_seqs.pkl'
    
    with open(fname, 'rb') as f:
        results_dict = pickle.load(f)
    
    # get sequence accession list 
    seq_acc_list = functools.reduce(lambda x, y: x + y, [[d['seq_accession'] for d in v] for v in results_dict.values()])
    print('number of sequence accessions:', len(seq_acc_list))
    # map seq accessions to sequences
    fname_seqs = '../data/fetch_wt_and_mut_seqs_sequences.pkl'  # for saving progress 
    seq_acc_to_seqs = {k: None for k in seq_acc_list}
    # load partial progress
    if os.path.isfile(fname_seqs):
        with open(fname_seqs, 'rb') as f:
            seq_acc_to_seqs.update(pickle.load(f))
    # remove keys we already have sequences for 
    seq_acc_list = [k for k, v in seq_acc_to_seqs.items() if v is None]
    seq_acc_list = batch_list(seq_acc_list, 150)  # batch by 150 to make retrieval more efficient
    for i, batch in enumerate(seq_acc_list):
        seqs_batch = get_wild_type(batch)
        seq_acc_to_seqs.update(seqs_batch)
        
        print("on batch", i+1, "/", len(seq_acc_list))
        if i % 5 == 0:
            with open(fname_seqs, 'wb') as fout:
                print("saving partial sequences dictionary to", fname_seqs)
                pickle.dump(seq_acc_to_seqs, fout)
    
    with open(fname_seqs, 'wb') as fout:
        print("saving full sequences dictionary to", fname_seqs)
        pickle.dump(seq_acc_to_seqs, fout)
    
    # update the results dictionary 
    for var_accession, missense_list in results_dict.items():
        for change_dict in missense_list:
            seq_acc = change_dict['seq_accession']
            change = change_dict['change']
            
            # update sequence
            seq = seq_acc_to_seqs[seq_acc]
            if not seq_acc_to_seqs[seq_acc]:
                continue
                
            change_dict['original_seq'] = seq
            
            try: 
                if re.search(SUB_QUERY2, change):
                    change_dict['mutated_seq'] = apply_multiple_mutation(seq, change)
                else:
                    assert re.search(SUB_QUERY, change)
                    change_dict['mutated_seq'] = apply_simple_mutation(seq, change)
            except KeyError:
                print("skipping variant", var_accession, "of sequence", seq_acc, "with change", change)
                
    # now save the results
    with open(fname_out, 'wb') as fout:
        print("saving final results to", fname_out)
        pickle.dump(results_dict, fout)


@delay(limit=0.35, time_delay=0.35)  # to avoid getting banned by NCBI
def get_wild_type(accession_list):
    try:
        s_fasta = efetch(db='protein', id=accession_list, rettype='fasta', retmode='text').read()
    except HTTPError as e:
        raise e
    return parse_efetch_output(s_fasta)


def parse_efetch_output(s_fasta):
    s_split = s_fasta.split('\n')
    s_split = list(filter(lambda s: len(s.strip()) > 0, s_split))
    s_fasta = '\n'.join(s_split)
    records = list(SeqIO.parse(StringIO(s_fasta), 'fasta'))
    return {r.id: str(r.seq) for r in records}


# def apply_mutation
def apply_simple_mutation(s, change):
    # we assume this is a valid change and the regex will match change string
    before, index, after = re.findall(SIMPLE_QUERY, change)[0]
    before = protein_letters_3to1[before]
    after = protein_letters_3to1[after]
    subs = ((before, after, int(index)),)
    return apply_subs(s, subs, zero_based=False)


def apply_multiple_mutation(s, change):
    # we assume this is a valid change and the regex will match change string
    before, after = re.findall(DELINS_QUERY, change)[0]
    
    # parse before 
    before_aa = []
    for aanum in before.split('_'):
        aa = protein_letters_3to1[aanum[:3]]
        num = aanum[3:]
        assert num.isdigit()
        before_aa.append((aa, int(num)))
    
    # parse after 
    after_aa = [protein_letters_3to1[after[i:i+3]] for i in range(0, len(after), 3)]
    
    # should have same number of amino acids deleted and inserted 
    if len(before_aa) != len(after_aa):
        return None 
    
    # otherwise apply substitutions 
    subs = [(aa, bb, ii) for (aa, ii), bb in zip(before_aa, after_aa)]
    return apply_subs(s, subs, zero_based=False)
    
    
    
    
    
    
if __name__ == '__main__': 
    main()
