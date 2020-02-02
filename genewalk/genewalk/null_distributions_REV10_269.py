"""This module implements functions related to the construction of a null
distribution for GeneWalk networks."""
import logging
import networkx as nx
import random #REV10_269
import copy #REV10_269

logger = logging.getLogger('genewalk.get_null_distributions')

#REV10_269
def get_rand_graph(mg):
    """Return a random graph with gene-gene and gene-GO annotation edges permuted whilst 
    keeping the same degree distributions for gene and GO annotations.

    Parameters
    ----------
    mg : networkx.MultiGraph
        An input graph based on which a random graph is generated.

    Returns
    -------
    networkx.MultiGraph
        A random graph whose degree distribution matches that of the output.
    """

    gene_nodes = []
    geneanno_nodes = []
    GO_nodes = []
    GOanno_nodes = []
    for node in nx.nodes(mg):
        node_dict = mg.nodes[node]
        if 'GO' in node_dict:#node is GO term
            GO_nodes.append(node)
            #test if node is GO annotation:
            for u,v,lab in graph.edges(nbunch=node,data='label', default='NA'):
                if lab == 'GO:annotation':#incident edge of node is a GO annotation: include node
                    GOanno_nodes.append(node)
                    break
        else:
            gene_nodes.append(node)
            #test if node is connected to GO term through annotation edge
            for u,v,lab in graph.edges(nbunch=node,data='label', default='NA'):
                if lab == 'GO:annotation':#incident edge of node is a GO annotation: include node
                    geneanno_nodes.append(node)
                    break


    #get randomized gene-gene subgraph
    submg_gene = mg.subgraph(gene_nodes)
    submg_gene_seq = sorted([submg_gene.degree(n) for n in gene_nodes], reverse=True)
    subrg_gene = nx.configuration_model(submg_gene_seq)#nb: output graph has numbers as nodes
    rndgene_nodes = copy.deepcopy(gene_nodes)
    random.shuffle(rndgene_nodes)#inplace shuffling
    #rndgenemapping is a random mapping from subrg_gene nodes, ie numbers, to shuffled (randomized) gene nodes
    rndgenemapping = {n: g for n,g in enumerate(rndgene_nodes)}
    subrg_gene = nx.relabel_nodes(subrg_gene, rndgenemapping, copy=False)

    #get randomized bipartite subgraph of genes and all GO terms.
    geneGOanno_nodes = copy.deepcopy(geneanno_nodes)
    geneGOanno_nodes.extend(GOanno_nodes)
    submg_geneGOanno = mg.subgraph(geneGOanno_nodes)    
    # generate from scratch a bipartite graph between goanno_nodes and geneanno_nodes
    # with edges only if the GWN has an edge with label=='GO:annotation
    bipart_geneGOanno = nx.MultiGraph()
    bipart_geneGOanno.add_nodes_from(geneGOanno_nodes)
    for u,v,lab in submg_geneGOanno.edges(data='label', default='NA'):
        if lab == 'GO:annotation':
            bipart_geneGOanno.add_edge(u,v)
    bipart_gene_seq = sorted([bipart_geneGOanno.degree(n) for n in geneanno_nodes], reverse=True)
    bipart_GOanno_seq = sorted([bipart_geneGOanno.degree(n) for n in GOanno_nodes], reverse=True)
    subrg_geneGOanno = nx.bipartite.configuration_model(bipart_gene_seq,bipart_GOanno_seq)
    #subrg_geneGOanno is composed of two partitions. Set A has nodes 0 to
    #(len(aseq) - 1) and set B has nodes len(aseq) to (len(bseq) - 1).
    nx.set_edge_attributes(subrg_geneGOanno, 'GO:annotation', name='label')#(for deepwalk start_nodes)
    rndgeneanno_nodes = copy.deepcopy(geneanno_nodes)
    random.shuffle(rndgeneanno_nodes)#inplace shuffling
    #rndmapping is a random mapping from subrg_geneGOanno nodes, ie numbers, to shuffled (randomized) gene nodes
    rndmapping = {n: g for n,g in enumerate(rndgeneanno_nodes)}
    rndGOanno_nodes = copy.deepcopy(GOanno_nodes)
    random.shuffle(rndGOanno_nodes)#inplace shuffling
    #append to rndmapping a random mapping from the last section of subrg_geneGOanno nodes, ie numbers, to shuffled GOannos
    rndmapping.update({n+len(geneanno_nodes): go for n,go in enumerate(rndGOanno_nodes)})#
    subrg_geneGOanno = nx.relabel_nodes(subrg_geneGOanno, rndmapping, copy=False)

    #merge random gene-gene and gene-GO annotation subgraphs
    subrg_geneGOs = nx.compose(subrg_gene,subrg_geneGOanno)
    submg_GO = mg.subgraph(GO_nodes)#create GO ontology subgraph
    rg = nx.compose(subrg_geneGOs,submg_GO)#append GO ontology to random subgraph

    return rg


def get_null_distributions(rg, nv):
    """Return a distribution with similarity values between (random) node 
       vectors originating from the input randomized graph.
    """
    srd = []
    #REV10_269: test not all connections, but only GO:annotations connections. 
    # Generate null distributions from random node vectors arising from rg
    for node in nx.nodes(rg):
        node_dict = rg.nodes[node]
        if 'GO' in node_dict:#node is GO term
            continue
        else:#node is a gene
            connections = list(rg[node])
            go_connections = []
            for con in connections:
                if 'GO' in rg.nodes[con]:
                    go_connections.append(con)
            n_con_source = len(go_connections)
            if n_con_source > 0:
                sim_dist = list(1-nv.distances(node, other_words=go_connections))
                srd += sim_dist         
    return srd
