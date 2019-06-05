#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#
#  Copyright (c) 2014-2015 - EMBL-EBI
#
#  File author(s): Dénes Türei (denes@ebi.ac.uk)
#
#  Distributed under the GNU GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.org/
#

import codecs
import sys
import copy

import pypath.settings as settings

__all__ = [
    'FileMapping', 'PickleMapping', 'ReadSettings', 'ReadList',
    'Reference', 'UniprotListMapping',
]


class MappingInput(object):


    def __init__(
            self,
            type_,
            id_type_a,
            id_type_b,
            ncbi_tax_id = None,
        ):

        self.type = type_
        self.id_type_a = id_type_a
        self.id_type_b = id_type_b
        self.ncbi_tax_id = ncbi_tax_id or settings.get('default_organism')


class FileMapping(MappingInput):

    def __init__(
            self,
            id_type_a,
            id_type_b,
            input_,
            col_a,
            col_b,
            separator = None,
            header = 0,
            ncbi_tax_id = None,
            entity_type = 'protein',
        ):

        MappingInput.__init__(
            self,
            type_ = 'file',
            id_type_a = id_type_a,
            id_type_b = id_type_b,
            ncbi_tax_id = ncbi_tax_id,
        )

        self.input = input_
        self.col_a = col_a
        self.col_b = col_b
        self.separator = separator
        self.header = header
        self.entity_type = entity_type
        self.input_args = {'organism': self.ncbi_tax_id}


    def set_organism(self, ncbi_tax_id):

        other_organism = copy.deepcopy(self)
        other_organism.ncbi_tax_id = ncbi_tax_id

        if 'organism' in other_organism.input_args:

            other_organism.input_args['organism'] = ncbi_tax_id

        return other_organism


class UniprotMapping(MappingInput):

    def __init__(
            self,
            id_type_a,
            id_type_b = 'uniprot',
            ncbi_tax_id = 9606,
            swissprot = 'yes',
        ):
        """
        Defines an ID conversion table to retrieve from UniProt.

        id_type : str
            Type of accession numbers you would like to translate.
        target_id_type : str
            Type of accession numbers you would like to translate to.
        tax : int
            NCBI Taxonomy ID of the organism of interest.
        swissprot : str
            Look for SwissProt or Trembl.
            Passed directly to UniProt`s `reviewed` parameter. `yes` or `no`
            To fetch Trembl and SwissProt together, set value to None.
        mapping : bool
            Get the data from UniProt`s programmatic access query interface,
            (uniprot.org/uniprot) or the batch retrieval/id mapping service
            (uniprot.org/mapping). These have slightly different APIs and
            capabilities. Some IDs can be obtained from the former, some
            from the latter.
        """

        self.type = 'uniprot'

        MappingInput.__init__(
            self,
            type_ = 'uniprot',
            id_type_a = id_type_a,
            id_type_b = id_type_b,
            ncbi_tax_id = ncbi_tax_id,
        )

        self.ncbi_tax_id = int(ncbi_tax_id)
        self.typ = 'protein'
        self.swissprot = swissprot
        self.field = None if id_type_a not in ac_query \
            else ac_query[self.id_type_a][0]
        self.subfield = None if id_type_a not in ac_query \
            else ac_query[self.id_type_a][1]


    def set_organism(self, ncbi_tax_id):

        other_organism = copy.deepcopy(self)
        other_organism.ncbi_tax_id = ncbi_tax_id
        return other_organism


class UniprotListMapping(MappingInput):

    def __init__(
            self,
            id_type_a,
            id_type_b,
            uniprot_id_type_a = None,
            uniprot_id_type_b = None,
            ncbi_tax_id = 9606,
            swissprot = True,
        ):
        """
        Provides parameters for downloading mapping table from UniProt
        `Upload Lists` webservice.

        :arg str id_type_a:
            Custom name for one of the ID types.
        :arg str id_type_a:
            Custom name for the other ID type.
        :arg str uniprot_id_type_a:
            This is the symbol the UniProt webservice uses for the first
            name type. These are included in the module and set
            automatically, the argument only gives a way to override this.
        :arg str uniprot_id_type_b:
            Same as above just for the other ID type.
        :arg bool swissprot:
            DOwnload data only for SwissProt IDs.
        """

        MappingInput.__init__(
            self,
            type_ = 'uniprot_list',
            id_type_a = id_type_a,
            id_type_b = id_type_b,
            ncbi_tax_id = ncbi_tax_id,
        )

        self.swissprot = swissprot
        self.ac_mapping = ac_mapping

        self.uniprot_id_type_a = (
            uniprot_id_type_a or self.ac_mapping[self.id_type_a]
        )
        self.uniprot_id_type_b = (
            uniprot_id_type_b or self.ac_mapping[self.id_type_b]
        )

        self.entity_type = 'protein'


    def set_organism(self, ncbi_tax_id):

        other_organism = copy.deepcopy(self)
        other_organism.ncbi_tax_id = ncbi_tax_id
        return other_organism


class PickleMapping(MappingInput):


    def __init__(
            self,
            id_type_a,
            id_type_b,
            fname,
            ncbi_tax_id = None,
        ):

        MappingInput.__init__(
            self,
            type_ = 'pickle',
            id_type_a = id_type_a,
            id_type_b = id_type_b,
            ncbi_tax_id = ncbi_tax_id,
        )

        self.fname = fname


class ReadSettings:


    def __init__(
            self,
            name = "unknown",
            separator = None,
            id_col_a = 0,
            id_col_b = 1,
            id_type_a = "uniprot",
            id_type_b = "uniprot",
            entity_type_a = "protein",
            entity_type_b = "protein",
            is_directed = False,
            sign = False,
            input = None,
            references = False,
            extra_edge_attrs = None,
            extra_node_attrs_a = None,
            extra_node_attrs_b = None,
            header = False,
            taxon_a = 9606,
            taxon_b = 9606,
            ncbi_tax_id = 9606,
            interaction_type = 'PPI',
            positive_filters = None,
            negative_filters = None,
            mark_source  =  None,
            mark_target  =  None,
            input_args = None,
            curl_args = None,
            must_have_references = True,
            huge = False,
            resource = None,
            unique_fields = None,
            expand_complexes = None,
        ):
        """
        :param str mark_source:
            Creates a boolean vertex attribute and sets it True for the
            source vertex of directed interactions from this particular
            resource.
        :param str mark_target:
            Same as ``mark_source`` but for target vertices.
        """

        self.entity_type_a = entity_type_a
        self.entity_type_b = entity_type_b
        self.id_col_a = id_col_a
        self.id_col_b = id_col_b
        self.id_type_a = id_type_a
        self.id_type_b = id_type_b
        self.is_directed = is_directed
        self.input = input
        self.extra_edge_attrs = extra_edge_attrs or {}
        self.extra_node_attrs_a = extra_node_attrs_a or {}
        self.extra_node_attrs_b = extra_node_attrs_b or {}
        self.name = name
        self.separator = separator
        self.header = header
        self.refs = references
        self.sign = sign
        self.taxon_a = taxon_a
        self.taxon_b = taxon_b
        self.ncbi_tax_id = ncbi_tax_id
        self.interaction_type = interaction_type
        self.positive_filters = positive_filters or []
        self.negative_filters = negative_filters or []
        self.input_args = input_args or {}
        self.curl_args = curl_args or {}
        self.must_have_references = must_have_references and bool(references)
        self.huge = huge
        self.resource = self.name if resource is None else resource
        self.mark_source = mark_source
        self.mark_target = mark_target
        self.unique_fields = unique_fields or set()
        self.expand_complexes = expand_complexes


class ReadList:


    def __init__(
            self,
            name = 'unknown',
            separator = None,
            id_col = 0,
            id_type = 'uniprot',
            entity_type = 'protein',
            input = None,
            extra_attrs = None,
            header = False,
        ):

        self.enity_type = entity_type
        self.id_col = id_col
        self.id_type = id_type
        self.input = input
        self.extra_attrs = extra_attrs or {}
        self.name = name
        self.separator = separator
        self.header = header


ac_query = {
    'genesymbol': ['genes', 'PREFERRED'],
    'genesymbol-syn': ['genes', 'ALTERNATIVE'],
    'hgnc': ['database', 'HGNC'],
    'embl': ['database', 'embl'],
    'entrez': ['database', 'geneid'],
    'refseqp': ['database', 'refseq'],
    'enst': ['database', 'ensembl'],
    'uniprot-entry': ['entry name', None],
    'protein-name': ['protein names', None]
}

ac_mapping = {
    'uniprot': 'ACC',
    'uniprot_id': 'ID',
    'embl': 'EMBL',
    'embl_id': 'EMBL_ID',
    'pir': 'PIR',
    'entrez': 'P_ENTREZGENEID',
    'gi': 'P_GI',
    'refseqp': 'P_REFSEQ_AC',
    'refseqn': 'REFSEQ_NT_ID',
    'ensembl': 'ENSEMBL_ID',
    'ensp': 'ENSEMBL_PRO_ID',
    'enst': 'ENSEMBL_TRS_ID',
    'ensg': 'ENSEMBLGENOME_ID',
    'ensgp': 'ENSEMBLGENOME_PRO_ID',
    'ensgt': 'ENSEMBLGENOME_TRS_ID',
    'hgnc': 'HGNC_ID'
}
