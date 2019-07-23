Webservice
==========

**New webservice** from 14 June 2018: the queries slightly changed, have been
largely extended. See the examples below.

The webservice implements a very simple REST style API, you can make requests
by the HTTP protocol (browser, wget, curl or whatever). After defining the
query type and optionally a set of molecular entities (proteins) you can
add further GET parameters encoded in the URL.

Query types
-----------

The webservice currently recognizes 7 types of queries: ``interactions``,
``ptms``, ``annotations``, ``complexes``, ``intercell``, ``queries`` and
``info``.
The query types ``resources``, ``network`` and ``about`` have not been
implemented yet in the new webservice.

Interaction datasets
--------------------

The instance of the ``pypath`` webserver running at the domain
http://omnipathdb.org/, serves not only the OmniPath data but also other
datasets. Each of them has a short name what you can use in the queries
(e.g. ``&datasets=omnipath,pathwayextra``).

* ``omnipath``: the OmniPath data as defined in the paper, an arbitrary
  optimum between coverage and quality
* ``pathwayextra``: activity flow interactions without literature reference
* ``kinaseextra``: enzyme-substrate interactions without literature reference
* ``ligrecextra``: ligand-receptor interactions without literature reference
* ``tfregulons``: transcription factor (TF)-target interactions from DoRothEA
* ``mirnatarget``: miRNA-mRNA and TF-miRNA interactions

TF-target interactions from TF Regulons, a large collection additional
enzyme-substrate interactions, and literature curated miRNA-mRNA interacions
combined from 4 databases. 

Mouse and rat
-------------

Except the miRNA interactions all interactions are available for human, mouse
and rat. The rodent data has been translated from human using the NCBI
Homologene database. Many human proteins do not have known homolog in rodents
hence rodent datasets are smaller than their human counterparts. Note, if you
work with mouse omics data you might do better to translate your dataset to
human (for example using the ``pypath.homology`` module) and use human
interaction data.


Examples
--------

A request without any parameter provides the main webpage:

    http://omnipathdb.org

The ``info`` returns a HTML page with comprehensive information about the
resources. The list here should be and will be updated as currently OmniPath
includes much more databases:

    http://omnipathdb.org/info

Molecular interaction network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``interactions`` query accepts some parameters and returns interactions in
tabular format. This example returns all interactions of EGFR (P00533), with
sources and references listed.

    http://omnipathdb.org/interactions/?partners=P00533&fields=sources,references

By default only the OmniPath dataset used, to include any other dataset you
have to set additional parameters. For example to query the transcriptional regulators of EGFR:

    http://omnipathdb.org/interactions/?targets=EGFR&types=TF

The TF Regulons database assigns confidence levels to the interactions. You
might want to select only the highest confidence, *A* category:

    http://omnipathdb.org/interactions/?targets=EGFR&types=TF&tfregulons_levels=A

Show the transcriptional targets of Smad2 homology translated to rat including
the confidence levels from TF Regulons:

    http://omnipathdb.org/interactions/?genesymbols=1&fields=type,ncbi_tax_id,tfregulons_level&organisms=10116&sources=Smad2&types=TF

Query interactions from PhosphoNetworks which is part of the *kinaseextra*
dataset:

    http://omnipathdb.org/interactions/?genesymbols=1&fields=sources&databases=PhosphoNetworks&datasets=kinaseextra

Get the interactions from Signor, SPIKE and SignaLink3:

    http://omnipathdb.org/interactions/?genesymbols=1&fields=sources,references&databases=Signor,SPIKE,SignaLink3

All interactions of MAP1LC3B:

    http://omnipathdb.org/interactions/?genesymbols=1&partners=MAP1LC3B

By default ``partners`` queries the interaction where either the source or the
arget is among the partners. If you set the ``source_target`` parameter to
``AND`` both the source and the target must be in the queried set:

    http://omnipathdb.org/interactions/?genesymbols=1&fields=sources,references&sources=ATG3,ATG7,ATG4B,SQSTM1&targets=MAP1LC3B,MAP1LC3A,MAP1LC3C,Q9H0R8,GABARAP,GABARAPL2&source_target=AND

As you see above you can use UniProt IDs and Gene Symbols in the queries and
also mix them. Get the miRNA regulating NOTCH1:

    http://omnipathdb.org/interactions/?genesymbols=1&fields=sources,references&datasets=mirnatarget&targets=NOTCH1

Note: with the exception of mandatory fields and genesymbols, the columns
appear exactly in the order you provided in your query.

Enzyme-substrate interactions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another query type available is ``ptms`` which provides enzyme-substrate
interactions. It is very similar to the ``interactions``:

    http://omnipathdb.org/ptms?genesymbols=1&fields=sources,references,isoforms&enzymes=FYN

Is there any ubiquitination reaction?

    http://omnipathdb.org/ptms?genesymbols=1&fields=sources,references&types=ubiquitination

And acetylation in mouse?

    http://omnipathdb.org/ptms?genesymbols=1&fields=sources,references&types=acetylation&organisms=10090

Rat interactions, both directly from rat and homology translated from human,
from the PhosphoSite database:

    http://omnipathdb.org/ptms?genesymbols=1&fields=sources,references&organisms=10116&databases=PhosphoSite,PhosphoSite_noref


Molecular complexes
^^^^^^^^^^^^^^^^^^^

The ``complexes`` query provides a comprehensive database of more than 22,000
protein complexes. For example, to query all complexes from CORUM and PDB
containing MTOR (P42345):

    http://omnipathdb.org/complexes?proteins=P42345&databases=CORUM,PDB


Annotations
^^^^^^^^^^^

The ``annotations`` query provides a large variety of data about proteins,
complexes and in the future other kinds of molecules. For example an
annotation can tell if a protein is a kinase, or if it is expressed in the
hearth muscle. These data come from dozens of databases and each kind of
annotation record contains different fields. Because of this here we have
a ``record_id`` field which is unique within the records of each database.
Each row contains one key value pair and you need to use the ``record_id``
to connect the related key-value pairs. You can easily do this with ``tidyr``
and ``dplyr`` in R or ``pandas`` in Python. An example to query the pathway
annotations from SignaLink:

    http://omnipathdb.org/annotations?databases=SignaLink3

Or the tissue expression of BMP7 from Human Protein Atlas:

    http://omnipathdb.org/annotations?databases=HPA&proteins=BMP7


Roles in inter-cellular communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another query type is ``intercell`` providing information on the roles in
inter-cellular signaling. E.g. if a protein is a ligand, a receptor, an
extracellular matrix (ECM) component, etc. This query type is very similar
to ``annotations`` but here the data does not come from original sources but
combined from several databases by us. However we refer also to the original
databases whenever the ``class_type`` is ``sub`` (subclass). E.g. the main
class ``ligand`` is a combination of ``Ramilowski 2015``, ``CellPhoneDB``,
``HPMR`` and many other databases, hence besides the ``ligand`` category you
will find sub-categories like ``ligand_ramilowski``, ``ligand_cellphonedb``
and so on. An example how to get all intercell annotations for 4 selected
proteins:

    http://omnipathdb.org/intercell?proteins=EGFR,ULK1,ATG4A,BMP8B

Or all the main classes for one protein:

    http://omnipathdb.org/intercell?levels=main&proteins=P00533

Or a list of all ECM proteins:

    http://omnipathdb.org/intercell?categories=ecm


Exploring possible parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes the names and values of the query parameters are not intuitive,
even though in many cases the server accepts multiple alternatives. To see
the possible parameters with all possible values you can use the ``queries``
query type. The server checks the paremeter names and values exactly against
these rules and if any of them don't match you will get an error message
instead of reply. To see the parameters for the ``interactions`` query:

    http://omnipathdb.org/queries/interactions
