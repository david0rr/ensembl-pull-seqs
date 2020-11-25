### ENSEMBL-PULL-SEQS README
---

Ensembl-pull-seqs.py pulls orthologous sequences from the Ensembl API. By specifing the gene name as it is recognised in humans the API pulls out the gene tree from the Ensembl API and extracts the sequences from a specified list of species

Type of gene list input is specified through "type" parameter. Can be set as symbol ("symbol") or Ensembl ID of gene ("id"). 

#### Use:

python ensembl_seq_run.py -genes gene_list.txt -species species_list.txt -type symbol

* The species should be written in their binomial format i.e. homo sapiens
