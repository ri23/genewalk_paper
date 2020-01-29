from nose.tools import raises
from genewalk.gene_lists import *


def test_map_lists():
    refs = map_hgnc_symbols(['BRAF', 'KRAS'])
    assert refs[0]['HGNC'] == '1097', refs
    assert refs[0]['UP'] == 'P15056', refs
    assert refs[0]['HGNC_SYMBOL'] == 'BRAF', refs
    assert refs[1]['HGNC'] == '6407', refs
    assert refs[1]['UP'] == 'P01116', refs
    assert refs[1]['HGNC_SYMBOL'] == 'KRAS', refs

    refs = map_hgnc_ids(['1097', '6407'])
    assert refs[0]['HGNC'] == '1097', refs
    assert refs[0]['UP'] == 'P15056', refs
    assert refs[0]['HGNC_SYMBOL'] == 'BRAF', refs
    assert refs[1]['HGNC'] == '6407', refs
    assert refs[1]['UP'] == 'P01116', refs
    assert refs[1]['HGNC_SYMBOL'] == 'KRAS', refs

    refs = map_mgi_ids(['MGI:892970'])
    assert refs[0]['HGNC'] == '6817', refs
    assert refs[0]['HGNC_SYMBOL'] == 'MAL', refs
    assert refs[0]['UP'] == 'P21145', refs

    refs = map_ensembl_ids(['ENSG00000157764'])
    assert refs[0]['HGNC'] == '1097', refs
    assert refs[0]['UP'] == 'P15056', refs
    assert refs[0]['HGNC_SYMBOL'] == 'BRAF', refs

    refs = map_ensembl_ids(['ENSG00000157764.9'])
    assert refs[0]['HGNC'] == '1097', refs
    assert refs[0]['UP'] == 'P15056', refs
    assert refs[0]['HGNC_SYMBOL'] == 'BRAF', refs


def test_read_gene_list():
    with open('test_gene_list.txt', 'w') as fh:
        fh.write('HGNC:1097')
    refs = read_gene_list('test_gene_list.txt', 'hgnc_id')
    assert len(refs) == 1


@raises(ValueError)
def test_read_gene_list_bad():
    with open('test_gene_list.txt', 'w') as fh:
        fh.write('HGNC:1097')
    refs = read_gene_list('test_gene_list.txt', 'ensembl_id')
    assert len(refs) == 1
