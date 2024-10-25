
from .utils.seq_to_embedding import extract_embeddings_from_fasta

import argparse
import sys 
import pathlib
import os 


def main():
    args = parse_args()
    
    fasta_file = args.i
    model_name = args.model
    device = args.device
    output_file = args.o

    extract_embeddings_from_fasta(fasta_file, output_file, device, model_name)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='name of input fasta file')
    parser.add_argument('--model', type=str, default='esm2_t48_15B_UR50D', help='name of model to extract embeddings')
    parser.add_argument('--device', type=str, default='cpu', help='cpu or gpu device to use')
    parser.add_argument('-o', type=str, required=True, help='name of output .h5 file')
    args = parser.parse_args()
    return args 


if __name__ == '__main__':
    main()
