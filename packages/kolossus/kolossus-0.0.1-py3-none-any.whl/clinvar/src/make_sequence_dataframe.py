
import pickle 
import pandas as pd 


def main():
    fname = '../data/clinvar_to_protein_accessions_of_interest_with_seqs.pkl'
    df = get_seq_dataframe(fname)

    fname_out = '../data/clinvar_protein_sequences.csv'
    df.to_csv(fname_out)


def get_seq_dataframe(fname):
    with open(fname, 'rb') as f:
        results = pickle.load(f)
    
    data = []
    cols = ['accession', 'seq_accession', 'change', 'mane_select', 'original_seq', 'mutated_seq']
    for acc, dlist in results.items():
        for d in dlist:
            data.append(tuple([acc] + [d.get(c) for c in cols[1:]]))
    
    return pd.DataFrame(data, columns=cols)
            
        

if __name__ == '__main__':
    main()
