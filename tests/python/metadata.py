# -*- coding: utf-8 -*-
"""Metadata for datasets and models used for testing"""

import collections
import os

_current_dir = os.path.dirname(__file__)
_dpath = os.path.abspath(os.path.join(_current_dir, os.path.pardir, 'examples'))

Dataset = collections.namedtuple(
    'Dataset', 'model dtrain dtest libname expected_prob expected_margin is_multiclass')

_dataset_db = {
    'mushroom': Dataset(model='mushroom.model', dtrain='agaricus.train', dtest='agaricus.test',
                        libname='agaricus', expected_prob='agaricus.test.prob',
                        expected_margin='agaricus.test.margin', is_multiclass=False),
    'dermatology': Dataset(model='dermatology.model', dtrain='dermatology.train',
                           dtest='dermatology.test', libname='dermatology',
                           expected_prob='dermatology.test.prob',
                           expected_margin='dermatology.test.margin', is_multiclass=True)
}


def _qualify_path(prefix, path):
    return os.path.join(_dpath, prefix, path)


dataset_db = {
    k: v._replace(model=_qualify_path(k, v.model), dtrain=_qualify_path(k, v.dtrain),
                  dtest=_qualify_path(k, v.dtest), expected_prob=_qualify_path(k, v.expected_prob),
                  expected_margin=_qualify_path(k, v.expected_margin))
    for k, v in _dataset_db.items()
}
