# genewalk_paper

Different cli_REVXXXXX.py and necessary adjustments to run each GeneWalk test version described below.

### 0. Rerun with default GeneWalk as comparison.
no changes. Exact code version that was used: master branch of genewalk repo (Latest commit 8d732bb). 
### 1. REV1NOGG 
GW without the gene-gene interactions: this would shows that we need the gene-gene interactions to 
help deciding what are the relevant gene functions. 
NB: no difference between indra and pc because neither is used so I only ran with flag pc 
### 2. REV2DEGS
GW with all input genes (irrespective of whether it is directly connected with another input gene). This ensures that not many DE genes drop out of the analysis.
### 3. REV3TRAN 
GW with direct edges to all parent GO terms (transitivity): should lose the functionality. In my opinion this approach is not useful but perhaps required as a negative control run.
### 4. REV4NOGO 
GW with only GO annotations, no GO ontology: should loose functionality as the ontology structure provides information and connectivity between different annotations and different genes that are not directly connected.
### 5. REV5ALLG 
GW with all expressed genes in there rather than DE genes using Pathway Commons.
Not pursued this for indra. 
### 6. REV6GRAN
GW with randomization of only gene-gene and gene-GO term edges to generate null distribution.
### 7. REV7PARA
Run some more tests with other hyperparameters: N_iteration=50, unlikely to make a difference.
### 8. REV8N2VE (by Ben Gyori)
Node2vec approach to assess how biased random walks (breadth first or depth first) as opposed to unbiased random walk (DeepWalk) affect the results.
### 9. REV9GDGO
GW with random walks only starting in the genes and direct GO annotations. Test to see if it lowers run time / maintains good results. NB: with normal null distribution, so no speed up in that part of code.
### 10. REV10_269
GW with REV6, REV9 and REV2 implemented.
### 11. REV11LINF
GW with long random walk lengths of 1000 steps and N_iteration=1. This version approximates a network representation learning algorithm through spectral decomposition (matrix factorization) as it is mathematically equivalent to DeepWalk with infinite walk lengths.
