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

"""
``pypath`` is a module primarily for building molecular interaction networks
but also with several submodules for accessing, preprocessing and serving
data from various resources.
"""

import sys
import os
import importlib

import pypath._version as _version_mod
import pypath.session_mod as _session_mod


class pypath(object):
    
    
    __version__ = _version.__version__
    __author__ = _version.__author__
    
    _session_mod.new_session()
    session = _session_mod.get_session()
    
    _disclaimer_text = (
        '\n\t=== d i s c l a i m e r ===\n\n'
        '\tAll data accessed through this module,\n'
        '\teither as redistributed copy or downloaded using the\n'
        '\tprogrammatic interfaces included in the present module,\n'
        '\tare free to use at least for academic research or\n'
        '\teducation purposes.\n'
        '\tPlease be aware of the licenses of all the datasets\n'
        '\tyou use in your analysis, and please give appropriate\n'
        '\tcredits for the original sources when you publish your\n'
        '\tresults. To find out more about data sources please\n'
        '\tlook at `pypath.descriptions` or\n'
        '\thttp://omnipathdb.org/info and \n'
        '\t`pypath.data_formats.urls`.\n\n'
    )
    
    def __init__(self):
        
        pass
    
    @classmethod
    def _disclaimer(cls):
        
        sys.stdout.write(cls._disclaimer_text)
        sys.stdout.flush()
    
    
    @classmethod
    def license(cls):
        
        cls_disclaimer()
    
    
    def __getattribute__(self, attr):
        
        try:
            
            return importlib.import_module('pypath.%s' % attr)
            
        except ImportError:
            
            return object.__getattribute__(self, attr)


#sys.modules['pypath'] = pypath()


# from now on we print this at import
# not at creation of PyPath object:
pypath._disclaimer()
_session_mod.get_log().msg(
    (
        '\n'
        '\t- session ID: `%s`\n'
        '\t- working directory: `%s`\n'
        '\t- logfile: `%s`\n'
        '\t- pypath version: %s' % (
            session_mod.get_session().label,
            os.getcwd(),
            session_mod.get_log().fname,
            pypath.__version__
        )
    ),
    label = 'pypath',
    level = -9,
    wrap = False,
)


#def __getattr__(attr):
    
    #try:
        
        #return importlib.import_module('pypath.%s' % attr)
        
    #except ImportError:
        
        #return __import__(__name__).__getattribute__(attr)


#def __dir__():
    
    #return object.__dir__(__import__(__name__)) + [
        #py[:-3]
        #for py in os.listdir(os.path.abspath(os.path.dirname(__file__)))
        #if py.endswith('.py')
    #]
