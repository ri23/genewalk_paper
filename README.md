# genewalk_paper

in folder genewalk: starting code = current master branch of genewalk repo (Latest commit 8d732bb).
On top are different cli_REVXXXXX.py and necessary adjustments to run each control described below.

### 0. Rerun with latest churchmanlab/genewalk/master code
no changes, used as control comparison.  
### 1. REV1NOGG 
GW without the gene-gene interactions: this would shows that we need the gene-gene interactions to 
help deciding what are the relevant gene functions. 
NB: no difference between indra and pc because neither is used so I only ran with flag pc 
### 2. REV2DEGS
GW with all input genes (irrespective of whether it is directly connected with another input gene). This ensures that not many DE genes drop out of the analysis.
### 3. REV3TRAN 
GW with direct edges to all parent GO terms (transitivity): should lose the functionality. In my opinion this approach is not useful but perhaps required as a negative control run.
### 4. REV4NOGO 
GW with only GO annotations, no GO ontology: should loose functionality as the ontology structure provides information and connectivity between different annotations and different genes that are not directly connected. CODE:
### 5. REV5ALLG 
GW with all expressed genes in there rather than DE genes.
Do not pursue this for indra as that would require using their whole db, not feasible / necessary for reviewers.
### 6. REV6GRAN: not yet pushed, work in progress
GW with randomization of only gene-gene interactions to generate null distribution.
### 7. REV7PARA
Run some more tests with other hyperparameters: N_iteration=50, unlikely to make a difference.
### 8. REV8N2VE (by Ben Gyori)
Node2vec approach to assess how biased random walks (breadth first or depth first) as opposed to unbiased random walk (DeepWalk) affect the results. Expected outcome: depth search will underperform as it does not query local neighborhood sufficiently.
### 9. REV9GDGO
GW with random walks only starting in the genes and direct GO annotations. Test to see if it lowers run time / maintains good results. NB: with normal null distribution, so no speed up in that part of code.


