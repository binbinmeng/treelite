# -*- coding: utf-8 -*-
"""Suite of basic tests"""

import os
import sys

import pytest
import numpy as np
import treelite
import treelite_runtime
from treelite.contrib import _libext
from .util import os_compatible_toolchains, load_txt
from .metadata import dataset_db


def check_predictor(predictor, dataset):
    dtest = treelite.DMatrix(dataset_db[dataset].dtest)
    batch = treelite_runtime.Batch.from_csr(dtest)
    expected_prob = load_txt(dataset_db[dataset].expected_prob)
    expected_margin = load_txt(dataset_db[dataset].expected_margin)
    if dataset_db[dataset].is_multiclass:
        nrow = dtest.shape[0]
        expected_prob = expected_prob.reshape((nrow, -1))
        expected_margin = expected_margin.reshape((nrow, -1))
    out_prob = predictor.predict(batch)
    out_margin = predictor.predict(batch, pred_margin=True)
    np.testing.assert_almost_equal(out_prob, expected_prob, decimal=6)
    np.testing.assert_almost_equal(out_margin, expected_margin, decimal=6)


@pytest.mark.parametrize('dataset', ['mushroom', 'dermatology'])
@pytest.mark.parametrize('use_annotation', [True, False])
@pytest.mark.parametrize('quantize', [True, False])
@pytest.mark.parametrize('parallel_comp', [None, 2])
@pytest.mark.parametrize('toolchain', os_compatible_toolchains())
def test_basic(tmpdir, dataset, use_annotation, quantize, parallel_comp, toolchain):
    libpath = os.path.join(tmpdir, dataset_db[dataset].libname + _libext())
    model = treelite.Model.load(dataset_db[dataset].model, model_format='xgboost')
    dtrain = treelite.DMatrix(dataset_db[dataset].dtrain)

    if use_annotation:
        annotator = treelite.Annotator()
        annotator.annotate_branch(model=model, dmat=dtrain, verbose=True)
        annotator.save(path='./annotation.json')

    params = {
        'annotate_in': ('./annotation.json' if use_annotation else 'NULL'),
        'quantize': (1 if quantize else 0),
        'parallel_comp': (parallel_comp if parallel_comp else 0)
    }
    model.export_lib(toolchain=toolchain, libpath=libpath, params=params, verbose=True)
    predictor = treelite_runtime.Predictor(libpath=libpath, verbose=True)
    check_predictor(predictor, dataset)


@pytest.mark.parametrize('dataset', ['mushroom', 'dermatology'])
@pytest.mark.parametrize('use_elf', [True, False] if sys.platform.startswith('linux') else [False])
@pytest.mark.parametrize('toolchain', os_compatible_toolchains())
def test_failsafe_compiler(tmpdir, dataset, use_elf, toolchain):
    libpath = os.path.join(tmpdir, dataset_db[dataset].libname + _libext())
    model = treelite.Model.load(dataset_db[dataset].model, model_format='xgboost')
    dtrain = treelite.DMatrix(dataset_db[dataset].dtrain)

    params = {'dump_array_as_elf': (1 if use_elf else 0)}
    model.export_lib(compiler='failsafe', toolchain=toolchain, libpath=libpath, params=params,
                     verbose=True)
    predictor = treelite_runtime.Predictor(libpath=libpath, verbose=True)
    check_predictor(predictor, dataset)
