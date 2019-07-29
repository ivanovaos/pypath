#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#
#  Copyright
#  2014-2019
#  EMBL, EMBL-EBI, Uniklinik RWTH Aachen, Heidelberg University
#
#  File author(s): Dénes Türei (turei.denes@gmail.com)
#                  Nicolàs Palacio
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.org/
#

from future.utils import iteritems

import re

import time
import datetime
import timeloop

import pypath.urls as urls
import pypath.curl as curl
import pypath.session_mod as session_mod
import pypath.settings as settings

_logger = session_mod.Logger(name = 'uniprot_input')

db = {}
_cleanup_period = settings.get('mapper_cleanup_interval')
_lifetime = 300
_last_used = {}


def _all_uniprots(organism = 9606, swissprot = None):
    
    swissprot = 'yes' if swissprot == True else swissprot
    rev = '' if not swissprot else ' AND reviewed: %s' % swissprot
    url = urls.urls['uniprot_basic']['url']
    get = {
        'query': 'organism:%s%s' % (str(organism), rev),
        'format': 'tab',
        'columns': 'id',
    }
    c = curl.Curl(url, get = get, silent = False)
    data = c.result
    
    return [
        l.strip() for l in data.split('\n')[1:] if l.strip()
    ]


def all_uniprots(organism = 9606, swissprot = None):
    
    return get_db(organism = organism, swissprot = swissprot)


def init_db(organism = 9606, swissprot = None):
    
    _logger._log(
        'Loading list of all UniProt IDs for '
        'organism `%u` (only SwissProt: %s).' % (
            organism,
            str(swissprot == True),
        )
    )
    
    key = (organism, swissprot == True)
    
    globals()['db'][key] = _all_uniprots(
        organism = organism,
        swissprot = swissprot,
    )
    globals()['_last_used'][key] = time.time()


def get_db(organism = 9606, swissprot = None):
    
    key = (organism, swissprot == True)
    
    if key not in globals()['db']:
        
        init_db(organism = organism, swissprot = swissprot)
    
    globals()['_last_used'][key] = time.time()
    
    return globals()['db'][key]


def is_uniprot(name, organism = 9606, swissprot = None):
    """
    Tells if ``name`` is a UniProt ID of ``organism``.
    """
    
    return name in get_db(organism = organism, swissprot = swissprot)



_cleanup_timeloop = timeloop.Timeloop()


@_cleanup_timeloop.job(
    interval = datetime.timedelta(
        seconds = _cleanup_period
    )
)
def _cleanup():
    
    keys = list(globals()['db'].keys())
    
    for key in keys:
        
        if time.time() - globals()['_last_used'][key] > _lifetime:
            
            _remove(key)


def _remove(key):
    
    if key in globals()['db']:
        
        _logger._log(
            'Removing UniProt ID list for '
            'organism `%u` (only SwissProt: %s)' % (
                key[0],
                str(key[1]),
            )
        )
        del globals()['db'][key]
    
    if key in globals()['_last_used']:
        
        del globals()['_last_used'][key]
