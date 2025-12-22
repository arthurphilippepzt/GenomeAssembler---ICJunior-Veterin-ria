#!/usr/bin/env python3

### library
import sys
from Bio import SeqIO
import re

### function
def name_constructor(assembly):
    records = list(SeqIO.parse(assembly, "fasta"))
    description = records[0].description
    description = description.lower()
    strain_name = re.findall(strain_code, description)
    strain_name = strain_name[0].strip()
    strain_name = strain_name.replace(' ', '_')
    name = re.split(' ', description)
    name.pop(0)
    final_name = name[0][0] + name[1][0] + '_' + strain_name
    return final_name

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: name_constructor.py <assembly_file>")
        sys.exit(1)
    assembly = sys.argv[1]
    strain_code = r'([a-z]+[ _]?\d+\s)'  # pattern stays inside main
    name = name_constructor(assembly)
    print(name)
