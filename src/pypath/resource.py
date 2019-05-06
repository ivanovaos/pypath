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

import pypath.dataio as dataio
import pypath.common as common


class AbstractResource(object):
    """
    Generic class for downloading, processing and serving
    data from a resource.
    """


    def __init__(
            self,
            name,
            ncbi_tax_id = 9606,
            input_method = None,
            input_args = None,
            **kwargs
        ):
        """
        name : str
            Custom name for the resource.
        input_method : callable
            Method providing the input data.
        """

        self.name = name
        self._input_method = input_method
        self.input_args = input_args or {}
        self.ncbi_tax_id = ncbi_tax_id


    def load(self):

        self.set_method()
        self.load_data()
        self.process()

        if hasattr(self, 'data'):

            delattr(self, 'data')


    def set_method(self):
        """
        Sets the data input method by looking up in ``dataio`` module if
        necessary.
        """

        if (
            isinstance(self._input_method, common.basestring) and
            hasattr(dataio, self._input_method)
        ):

            self.input_method = getattr(dataio, self._input_method)

        elif callable(self._input_method):

            self.input_method = self._input_method


    def load_data(self):
        """
        Loads the data by calling ``input_method``.
        """

        self.set_method()

        if hasattr(self, 'input_method'):

            self.data = self.input_method(**self.input_args)


    def process(self):
        """
        Calls the ``_process_method``.
        """

        self._process_method()


    def _process_method(self):

        pass
