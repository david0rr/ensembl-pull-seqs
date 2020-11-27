#!/usr/bin/env python3

# David Orr
# Usage python3 ensembl_seq_run.py <files_to_consider>

import requests, sys
import json
import argparse
import os

#species_list = ["panthera_leo","monodelphis_domestica","camelus_dromedarius"]
#GENE="ANXA2"

def run(args):
	genes = create_genelist(args.genelist)
	species = create_specieslist(args.specieslist)
	pull_seqs_from_ensembl(genes, species)
	

def create_genelist(gene_file):
	'''From given gene file create list to iterate over''' 
	genelist=[]
	genes = open(gene_file, "r")
	
	for lines in genes:
		line = lines.strip()
		genelist.append(line)
		#print (genelist)
	return genelist

def create_specieslist(species_file):
	'''From given species file create list to iterate over''' 
	specieslist=[]
	species = open(species_file, "r")

	for lines in species:
		line = lines.strip()
		lower_chr = line.lower()
		no_space = lower_chr.replace(" ", "_")
		specieslist.append(no_space)
	return specieslist

def pull_seqs_from_ensembl(genelist, specieslist):
	'''Use Ensembl API to pull unaligned sequences given the common human gene name -
	currently set using mammal clade taxom id'''
	
	taxonid = "32523"

	if not os.path.exists("seqs_out"):
		os.makedirs("seqs_out")

	for GENE in genelist:
		with open("seqs_out/" + GENE + ".fa", 'w') as go:
			fasta_dict = {}
	
			server = "https://rest.ensembl.org"
			ext = "/homology/symbol/human/" + GENE + "?target_taxon=32523;sequence=cdna;type=orthologues;aligned=False"
	
			r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	
			if not r.ok:
				r.raise_for_status()
				sys.exit()
	
			decoded = r.json()
	
	
			for k, v in decoded.items():
				if isinstance(v,list):
					for i in v:
						#print (i)
						for k, v in i.items():
							if isinstance(v,list):
								for i in v:
									for k, v in i.items():
										if k == 'source':
											if v["species"] in specieslist:
												#print (v)
												species = str(v["species"])
												gene_id = str(v["id"])
												protein_id = str(v["protein_id"])
												gene_name = GENE
												seq = str(v["align_seq"])
												fasta_dict[">" + species + "|" + protein_id + "|" + gene_id + "|" + gene_name] = seq.replace("-","")
										if k == 'target':
											if v["species"] in specieslist:
												#print (v)
												species = str(v["species"])
												gene_id = str(v["id"])
												protein_id = str(v["protein_id"])
												gene_name = GENE
												seq = str(v["align_seq"])
												fasta_dict[">" + species + "|" + protein_id + "|" + gene_id + "|" + gene_name] = seq.replace("-","")

			for k, v in fasta_dict.items():
				go.write(k + '\n' + v + '\n')

def main():
	
	parse = argparse.ArgumentParser()
	
	#Specify input and output files on the command line
	parse.add_argument("--genelist", "-genes",type=str,help="file containing required genes, e.g. BCRA1",required=True)
	parse.add_argument("--specieslist", "-species", type=str,help="file containing required species, e.g. homo_sapiens",required=True)
	parse.set_defaults(func=run)

	args = parse.parse_args()
	args.func(args)

if __name__=="__main__":
	main()
										
