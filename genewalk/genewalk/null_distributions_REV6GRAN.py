"""This module implements functions related to the construction of a null
distribution for GeneWalk networks."""
import logging
import networkx as nx


logger = logging.getLogger('genewalk.get_null_distributions')


def get_rand_graph(mg):
    """Return a random graph with the same degree distribution as the input.

    Parameters
    ----------
    mg : networkx.MultiGraph
        An input graph based on which a random graph is generated.

    Returns
    -------
    networkx.MultiGraph
        A random graph whose degree distribution matches that of the output.
    """
    #REV6GRAN: UNFINISHED:
    #get subgraph corresponding to gene network
    #see REV9GDGO to select the nodes get gene_nodes and GO_nodes 
    submg_gene = mg.subgraph(gene_nodes)
    subrg_gene = nx.configuration_model(submg_gene)
    #get subrg_gene2GOanno: bipartite subgraph of genes and all GO terms.
    subrg_geneGOs = nx.compose(subrg_gene,subrg_gene2GOanno)
    GO_nodes = set(mg.nodes()).difference(gene_nodes)
    submg_GO = mg.subgraph(GO_nodes)
    rg = nx.compose(subrg_geneGOs,submg_GO)#append GO ontology
    
    
    # this is not randomized: order is same
    d_seq = sorted([mg.degree(n) for n in mg.nodes()], reverse=True)
    # creates random multigraph with same degree sequence
    rg = nx.configuration_model(d_seq)
    # the node labels are numbers which gives problems in word2vec
    # so adjust 0 to n0
    mapping = {n: 'n%s' % n for n in rg.nodes()}
    rg = nx.relabel_nodes(rg, mapping, copy=False)
    return rg

 
def get_null_distributions(rg, nv):#REV6GRAN
    """Return a distribution with similarity values between (random) node 
       vectors originating from the input randomized graph.
    """
    srd = []
    #REV6GRAN: define gene_nodes from rg and you need test not all connections, but all GO:annotations connections. 
    # Generate null distributions from random node vectors
    for node in gene_nodes:#nx.nodes(rg):#REV6GRAN
        connections = list(rg[node])
        # only get sims for non self connections
        if node in connections:
            connections.remove(node)
        n_con_source = len(connections)
        if n_con_source > 0:
            sim_dist = list(1-nv.distances(node, other_words=connections))
            srd += sim_dist
    return srd
