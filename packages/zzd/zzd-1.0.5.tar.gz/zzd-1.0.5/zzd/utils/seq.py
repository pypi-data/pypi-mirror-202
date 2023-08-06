from Bio import SeqIO

def read_seq(file_name):
    return {k.id:str(v) for k,v in SeqIO.parse(file_name,"fasta")}

def write_seq(file_name, seq):
    with open(file_name, "w") as f:
        for k,v in seq.items():
            f.write(f">{k}\n{v}\n")

    

