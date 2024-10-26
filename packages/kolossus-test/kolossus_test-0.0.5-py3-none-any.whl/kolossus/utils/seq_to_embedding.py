
import os
import sys
import pathlib

import h5py

import numpy as np
import torch 

from Bio import SeqIO


# alternative function for getting embeddings
def extract_junk(seq_list, device, model_name='esm2_t48_15B_UR50D', output_dir=None, 
                       tokens_per_batch=4096, seq_length=1022,repr_layers=[48]):

    out = {}
    for seqid, seq in seq_list:
        out[seqid] = torch.rand(5120).to(device)

    return out


def extract_junk_from_fasta(fasta_file, output_file, device, model_name, 
                       tokens_per_batch=4096, seq_length=1022,repr_layers=[48],layer_to_use=48):
    # assert valid output and input files 
    assert os.path.isfile(fasta_file)
    assert os.path.isdir(os.path.join(*os.path.split(output_file)[:-1]))
    if not output_file.endswith('.h5'):
        output_file += '.h5'

    with h5py.File(output_file, 'w') as fout:
        for record in SeqIO.parse(fasta_file, 'fasta'):
            fout[record.id] = torch.rand(5120)


# in case we need to modify later
def load_model():
    return esm.pretrained.esm2_t48_15B_UR50D()

