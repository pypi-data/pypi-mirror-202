#!/usr/bin/python3

import extra_data as ex
import nx5d.h5like.xfel as xfel

import pytest

# Unit test for the XFEL data module (mostly nx5d.h5like.xfel).
# Needs XFEL data and API, predominantly extra_data.
# Tests therefore only work within the XFEL environment.
#
# Call with 'pytest -m xfel'

@pytest.fixture
def xfel_test_run():
    return { 'proposal': 3491,
             'run': 149,
             'data': 'all' } # proposal, run

@pytest.fixture
def xfel_test_data(xfel_test_run):
    run = ex.open_run(**xfel_test_run)

    return run.select([
        ('MID_DET_AGIPD1M-1/DET/*CH0:xtdf', '*'),
        ('SA2_XTD1_XGM/XGM/DOOCS:output', '*'),
        ('MID_EXP_EPIX-1/DET/RECEIVER:daqOutput','*'),
        ('MID_EXP_SAM/MDL/DOWNSAMPLER', '*')
    ])
    
@pytest.mark.xfel
def test_exdat_h5(xfel_test_data):
    eh = xfel.ExdatH5(xfel_test_data)

    assert "measurement" in eh

    node = eh["measurement/mid_det_agipd1m-1/det/1ch0:xtdf"]
    print (node.keys())

    assert "image.data" in node
    
    #assert "instrument" in eh
    #assert "positioners" in eh["instrument"]

    data = node['image.data']
    print(data.shape)
    
    subdata = data[13:15]
    print(subdata.shape)    

    
    assert len(data.shape) == 3
    assert len(subdata.shape) == 3

    # This is just to check that the data type supports some rudimentary
    # kind of ndarray API, i.e. can do simple arithmetics and return numbers :-)
    nr = subdata.sum()
    nr2 = (subdata*2).sum()

    assert (nr*1.9 < nr2) and (nr*2.1 > nr2)
