#!/usr/bin/python3

from silx.io import commonh5 as ch5
from numpy import array as np_array
from itertools import product as itr_product

from numpy import array as np_array

from xarray import DataArray, Dataset, concat

import logging

'''
Reading XFEL Data
=================

This module implements analysis and transformation routines which enable
use of the :class:`ScanReader` module with data acquired at the
[European X-ray Free Electron Laser (XFEL)](https://www.xfel.eu/).
It uses the [EXtra-data](https://pypi.org/project/EXtra-data/) library,
the official XFEL data extraction library.

Understanding the XFEL Data Format
----------------------------------

There is [good documentation available](https://extra-data.readthedocs.io/en/latest/)
for the EXtra-data package, also containing an introduction to
[the on-disk XFEL data](https://extra-data.readthedocs.io/en/latest/data_format.html).
A conceptual overview of how the data is organized can be inferred from
there.

Here we outline the main features of the XFEL data, and how they relate
to our data [concepts](concepts.md):

  - **run**: the main unit is a "run", which is a not further specified "series"
    of measurements. This is similar to our
    [scan](concepts.md#scan_streak_frame), 
    but with the notable difference that a *scan* consists of a series
    of simlar *streaks*, while an XFEL "run" bears no such restrictions.

  - The datapoints themselves is organized in "detector data" and
    "other data", similarly to the *measurement* and *positioners*
    we've come to know from the ESRF falvors of Nexus.

  - A "run" may be broken down into "sequences". There is apparently
    no semantic restriction on what goes into a sequence, so it can't
    be related to any of our *frame* or *streak* concepts. Also,
    different sequences from different acquisition devices don't
    necessarily align, which is a requirement for our frames and
    streaks.

  - **train**: this is the usefully organized sub-unit of data acquisition;
    it holds all the data points (a.k.a. *frames*, in nx5d lingo) that
    come with a pulse train. (A pulse train is one "shot" of the XFEL, taking
    place within a a significant fraction of a second, and containing
    up to several hundreds of pulses at once.)

    Each of the instruments saves their data according to the current
    *train ID*, which is unique. Not every instrument does, however, necessarily
    save any data for each train, and those that do, don't necessarily save
    only a single data point; in fact, many save several, e.g. one data point
    for each pulse. The number of data points one specific instrument
    saves may also vary from one train to the next.

    As such, trains do not neatly align with our initial idea of *frames*,
    but don't outright contradict it.


Data Adapter Strategy
---------------------

Analyzing XFEL data is a two-step process:

  1. Data needs to be extracted from the pecular XFEL storage
     and translated into a more "handy" stucture, imitating
     the ESRF Nexus flavor nx5d is expecting. This can be
     done abusing the `ScanReader` infrastructure, but needs
     specific HDF5-like interfaces around EXtra-data's API elements,
     primarily the
     [`DataCollection`](https://extra-data.readthedocs.io/en/latest/reading_files.html)
     family of objects and generators.

  2. Standard nx5d tools can be applied to the output of step 1
     to further process and ingest
     data according to standard nx5d methods for specific experiments,
     e.g. the [X-ray diffraction]() module. This is also done using
     `ScanReader`, but in its own element. For this, of course,
     the output of step 1 needs to be a HDF5-like object itself.

So in essence, producing scientific insight from XFEL data involves
a stacked use of `ScanReader`. This module implements the necessary
HDF5-like input classes and output composers to magic the raw XFEL
produced data into something that "off-the-shelf" experimental analysis
modules of nx5d can make sense of.

Data Set Addressing
-------------------

Similarly to the way nx5d expects it, the XFEL data storage system
offers device labels to address the data. The main difference is that
not all devices go in-sync when *collecting* data: some collect
one datapoint per pulse train (but on a different pulse than another),
others collect several at different times, and yet others don't collect
any data at all.

In the first phase -- extracting and preparing -- we make it the
user's (or: higher API level's) responsibility to address only those
devices that have a similar storage scheme, e.g. the 16 modules
that make up one particular detector. To simplify and encourage
"correct behavior", addressing scheme will have syntactic sugar
to address a whole class of devices at once (e.g. selecting
`detector="AGIPD1M-1"` instead of `("MID_DET_AGIPD1M-1/DET/*CH0:xtdf")`),
in addition to regular, completely free key addressing.

This in turn also means that we are offering a list of special XFEL
devices, detectors in particular, with their naming scheme and data
processing particualrities. Beyond addressing, this is important for
a variety of reasons: XFEL detectors are not single pieces of equipment,
they are (sometimes?) made up of distinct components -- e.g. up to 16
individual chips. These have a non-trivial geometry and spatial relation
to one another, and need supplementary data (and API elements from
EXtra-data) in order to assemle a full, "regular" x-ray diffraction
pattern picture.
'''

class ExdatLazyDataset(ch5.LazyLoadableDataset):
    ''' Node to lazily load `extra_data.KeyData` datasets.
    '''
    def __init__(self, keydata, name, parent=None, attrs=None, array_like='dask_array'):
        super().__init__(name, parent, attrs)
        self._kdata = keydata
        self._array_like = array_like

    def _create_data(self):

        # FIXME: Loading a dask_array() from _kdata and using it by default
        # is a pointless exercise in burning CPU cycles.
        # This is because we're most likely going to slice the dataset anyway
        # (using ScanReader.streaks()), and we're  typically going to load
        # a lot less than the whole data into memory.
        # Which means that we're likely to not have to _ever_ use dask_array(),
        # unless for the seldom cases where we do arithmetics on the dataset
        # itself.
        #
        # Typical usage scenario will rather be something like "dataset[xxx]",
        # and xxx will be small enough to be returned as a ndarray on virtually
        # every occasion.
        #
        # This needs to be fixed.
        #
        # Not sure how to do that, though... most likely we need to extend
        # __getitem__() below to actually intercept slicing requests on
        # dask arrays, and peform _kdata.ndarray(roi=(...)) selections when
        # that happens. This will allow us to have fast ndarray-based data
        # management when loading small(-ish) streaks.
        #
        # On the other hand, the danger is that the user is stupid and will
        # store all the streaks before starting to process them... which
        # will fill up the memory, again.
    
        
        d = getattr(self._kdata, self._array_like)()
        logging.debug("Creating data: %s#%s with shape %r" % \
                      (self._kdata.source, self._kdata.key, d.shape))
        return d

    def __getitem__(self, item):
        ''' Overriding __getitem__() from silx's LazyLoadableDataset.

        The guys over at ESRF were a little bit too ambitious, respectively lacking in
        phantasy :) and they're checking whether the dataset is an ndarray instance.
        Which, of course, it isn't, since we're (sometimes?) using dask arrays.
        So we need to catch for this here. So what we're doing is catching the
        case where data is a container (with "__len__"), but not an ellipsis or
        a tuple, and instead of raising an error, we're passing the call on
        to data's __getitem__().

        This will probably break at some point, and then some poor soul will have
        to cross-check again with the silx's commonh5.LazyLoadableDataset sources
        and see how to work around that. Good luck!
        '''
        if hasattr(self._get_data(), "__getitem__"):
            return self._get_data().__getitem__(item)
        else:
            return super().__getitem__(item)


    @property
    def shape(self):
        ''' Same problem as __getitem__(): overzealous superclass discards data if it's not numpy.
        '''
        return self._get_data().shape \
            if hasattr(self._get_data(), "shape") \
               else super().shape

    @property
    def size(self):
        ''' Same problem as __getitem__(): overzealous superclass discards data if it's not numpy.
        '''
        return self._get_data().size \
            if hasattr(self._get_data(), "size") \
               else super().size


    def __len__(self):
        ''' Same problem as __getitem__(): overzealous superclass discards data if it's not numpy.
        '''
        return self._get_data().__len__() \
            if hasattr(self._get_data(), "__len__") \
               else super().__len__()
    
        

class ExdatSourcesGroup(ch5.Group):
    '''Mock HDF5 node for a subset of `extra_data.DataCollection` keys.
    '''
    def __init__(self, name, parent, selection, array_like='auto'):
        super().__init__(name=name, parent=parent)
        self.sel = selection

        for src in self.sel.all_sources:
            snode = self._ensure_group(self, src)
            logging.debug("Have node: %s" % snode.name)
            
            for key in self.sel.keys_for_source(src):
                kdata = self.sel[src,key]

                if array_like == 'auto':
                    numpts = np_array(kdata.shape).prod()
                    array_like = 'dask_array' if numpts > 1e6 else 'ndarray'
                
                snode.add_node(ExdatLazyDataset(kdata, name=key, parent=snode,
                                                array_like=array_like))
                
                logging.debug("  Dataset: %s" % key)
                


    def _ensure_group(self, parent, source_path):
        '''Makes sure all path components of source_path exist.

        Returns:
            The corresponding group node object.
        '''
        parts = source_path.split('/') if isinstance(source_path, str) else source_path
        me = parts[:1][0]
        them = parts[1:] if len(parts)>1 else None
        
        if me not in parent:
            parent.add_node(ch5.Group(name=me, parent=parent))

        return parent[me] if them is None \
            else self._ensure_group(parent[me], them)
        
        
class ExdatH5(ch5.File):
    '''Generic class to offer HDF5-like access to a `DataCollection` object.

    This implementation is not necessarily fully h5py-API compatible. It contains
    just enough of a mock up to be able to work nicely with nx5d.scan.ScanReader.
    
    Currently the HDF5 mock is flat, i.e. no groups, just the base data sets.
    '''

    def __init__(self, dsel, array_like='auto'):
        '''Initializes the ExdatH5 instance.
        
        Args:
            dsel (extra_data.DataCollection): the data collection (selection) to expose.
        
            array_like: One of "numpy", "dask" or "auto", representing the default
              array mechanism to use when retrieving data from DataCollection.
              "numpy" is strongly suggested if the data will fit in memory,
              since it's considerably faster. However, "dask" will provide you
              with distribuited arrays that work across a large number of nodes,
              should you need it. The default "auto" will always try "numpy"
              first, and fall back to "dask" if that fails.
        '''
        super().__init__()

        self.add_node(ExdatSourcesGroup(name="measurement", parent=self,
                                        selection=dsel.select([
                                            (k, '*') for k in dsel.all_sources
                                        ]),
                                        array_like=array_like))
        
        #self.add_node(ch5.Group(name="instrument", parent=self))
        #self['instrument'].add_node(ExdatGroup(name="positioners", parent=self['instrument'],
        #                                       selection=None))
        
        self.dsel = dsel

        # could split these in instrument_sources and control_sources.
        #self.datasets = {k:self.dsel.get_virtual_dataset(k) \
        #                 for k in self.datc.all_sources}

    def __enter__(self, *args, **kwargs):
        ''' Overriding the `silx.io.commonh5.File` enter/exit mechanism.
        
        ScanReader depends on using nested with-guards (enter/exit), i.e.
        entering/exitting multiple times on the same object.
        This is an extension to do just that.
        '''
        if not hasattr(self, "_enter_cnt") or self._enter_cnt == 0:
            self._enter_data = super().__enter__(*args, **kwargs)
            self._enter_cnt = 0
        self._enter_cnt += 1
        return self._enter_data


    def __exit__(self, *args, **kwargs):
        if self._enter_cnt > 0:
            self._enter_cnt -= 1
        if self._enter_cnt == 0:
            super().__exit__(*args, **kwargs)


from extra_data.components import AGIPD1M
            
''' Quick'n Dirty database of XFEL detectors and their data.

This is what we need to convert detector tiles into XRD images.
'''
detectors = {
    'AGIPD1M-1': {
        'selection': [
            ('MID_DET_AGIPD1M-1/DET/*CH0:xtdf', '*'),
            ('MID_AGIPD_MOTION/MDL/DOWNSAMPLER', '*ActualPosition.value'),
            ('MID_EXP_EPIX-1/DET/RECEIVER:daqOutput','data.image.pixels'),
            ('SA2_XTD1_XGM/XGM/DOOCS:output','data.intensityTD'),
            ('MID_EXP_SAM/MDL/DOWNSAMPLER','ssryActualPosition.value'),
        ],

        'data_template': {
            'tmp':  tuple([ '@{measurement}/MID_DET_AGIPD1M-1/DET/%dCH0:xtdf/'
                              'image.data' % i \
                              for i in range(1) ]),

            'tiles': lambda h5, nodeOnly, slicer: \
            AGIPD1M(h5.dsel).get_dask_array('image.data').transpose('train_pulse', 'module', 'dim_0', 'dim_1')[slicer],
            
            'motors': tuple([ ('@{measurement}/MID_AGIPD_MOTION/MDL/DOWNSAMPLER/q%dm1ActualPosition.value' % i,
                               '@{measurement}/MID_AGIPD_MOTION/MDL/DOWNSAMPLER/q%dm2ActualPosition.value' % i)
                              for i in range(1,5) ]),

            'angles': {
                'theta': '@{measurement}/MID_EXP_SAM/MDL/DOWNSAMPLER/ssryActualPosition.value',
            },

            'norm': {
                'epix': '@{measurement}/MID_EXP_EPIX-1/DET/RECEIVER:daqOutput/data.image.pixels',
                'xgm':  '@{measurement}/SA2_XTD1_XGM/XGM/DOOCS:output/data.intensityTD',
            }
        },
    },
}


class DetectorTiler:
    ''' Combines images of individual XFEL detector modules into an 'XRD-like detector image.'

    This is a higly specialized class which generates exacly *one* kind of
    image, in exactly *one* kind of way.  [FIXME: document how!]
    '''

    def __init__(self, geom_class=None, geom=None,  mask=None, tiles=None,
                 norm=None, motors=None, passthrough=True, **passthrough_data):
        ''' Initializes the tiler with a dataset and all metadata necessary for tiling.
        '''

        # This is the trick part that we'll need to fix: it's a major pain in the
        # ass to tile together the detector images from its individual modules.
        # The best thing is to use the desginated detector object (e.g. AGPID1M(...)),
        # but this means that this needs to be done on a HDF5-like level.
        self.tiles  = tiles

        
        self.norm   = norm
        self.motors = motors
        self.geom   = geom
        self.mask   = mask
        self.geom_class = geom_class        
        self.passthrough_data = passthrough_data.copy() if passthrough else {}

        try:
            epix = self.norm['epix'].compute().mean(axis=(1,2))
            xgm = self.norm['xgm'].compute()[:,0]
            print ("EPIX:", epix.shape)
            print ("XGM:", xgm.shape)
            self.valid_data_selector = \
                self._norm_filter(epix) * \
                self._norm_filter(xgm)
        except Exception as e:
            logging.error("While calculating norm: Oops, %r" % str(e))


    def _geom_from_motors(self, q1m, q2m, q3m, q4m):
        ''' Returns a geometry object from the specified quadrant motor positions.
        '''
        quad_pos = (
            (-542 + 0*q1m[0],  660 + -5*q1m[1]),
            (-608 + 0*q2m[0],  -35 +  5*q2m[1]),
            ( 534 + 0*q3m[0], -221 +  5*q3m[1]),
            ( 588 + 0*q4m[0],  474 + -5*q4m[1]),
        )
        
        #print ("Quad positions:", [(i[0].compute()[()], i[1].compute()[()]) for i in  quad_pos])
        
        return self.geom_class.from_quad_positions(quad_pos=quad_pos)
        

    def _norm_filter(self, data):
        ''' Filter normalization values.

        Filtering criteria are:
        
           - exclude everything that stands out by more than one order
             of magnitude from the ful dataset
        
           - then exclude everything that stands out by more than half
             from the remaining dataset

        Returns:
            A data selector (boolean array slicer) with valid data,
            based on the fitlering criteria.
        '''
        norm_data = data.mean()/data
        sel_data = (norm_data>0.1) * (norm_data<10)
        norm_data = data[sel_data].mean()/data
        sel_data = (norm_data>0.5) * (norm_data<2)
        return sel_data
        
    
    def __call__(self, pulse_slicer, mask=None, tiles=None, **pulse_reducers):
        '''Returns the sum of full detector images specified by pulse_list

        Args:
        
            pulse_slicer: Slicer of pulses to select (e.g. `numpy.s_[2,3,17]`)
        
            mask: Array of shape `(N, width, height)`, where `N` is the number
              of detector modules (typically 16), and `width` and `height` are
              the geometry of the detector module images, as they come in
              the tiles argument of `__init__()`.
        
            tiles: Callable for reducing multiple detector tile(s)
              (i.e. as many as there are pulses) into one. The callable may
              receive either a 3D (shape: `(N, width, height)`) or a 4D
              xarray (shape: `(P, N, width, height)`), where `P` is the number
              of pulses, `N` the number of detector tiles, and `width` / `height`
              are the image sizes of the tiles themselves. This depends on how
              `pulse_slicer` is set.
              It is expected to return a 3D array `(N, width, height)` by custom
              transformation (e.g. summing up data along the first dimension).

            pulse_reducers: Hashable which contains a data key (as passed
              to `__init__()`) as key, and a pulse-reducing callable as value.
              The pulse-reducing callable has a similar use as `tiles`, i.e.
              reducing the data to one single instance. The callable is passed
              the entire dataset with the corresponding name and is expected
              to return the reduced data payload (either as array or as a scalar).
              Every data set for which a pulse-reducer is present, is also
              returned in the output dictionary.

        Returns:
            A dictioanry containing at least the following keys:
        
            - "image": this is the composed detector image made up
              of all the tiles.

            - "metrics": a Python `dict` with as many of the fields that need to
              to be passed on for XRD Q-space transformation (e.g. inside the
              "setup" parameter of the `nx5d.xrd.LazyQMap` object) as can be
              computed from the tile data.
              Note that some of the metrics values might be wrong, or require
              manual offsetting to account for alignment issues.
        
              Typically, these fields are:
        
              - "imageChannelSize": the virtual "pixel size" of the full detector,
                inferred from the x, y, z return values
                of `.get_pixel_positions()` of a suitable geometry class.

              - "imageSize": the size of the full 'virtual' detector image generate,
                in pixels

              - "imageCenter": the center pixel of the 'virtual' detector image,
                as received from `.position_modules()` of a suitable geometry clas.

              - "imageDistance": the detector distance from sample, inferred from
                the z coordinates. (ACHTUNG, this is particularly likely to be wrong
                in many occasions, e.g. if the coresponding motors haven't been
                initialized properly.)

            Additional keys are generated for every dataset for which there is an
            entry available in `pulse_reducers`, with the corresponding output.
            For instance: requesting to generate a $\theta$ angle by picking the
            first one from a list of such angles would imply an invocation like
            this: `.(s_[...], angles=lambda a: {k:v[0] for k,v in a.items()})`.
        '''

        # FIXME: this lambda assumes a structure different than the one
        # in the "motors" keys (this assumes a single x/y set for one quadrant,
        # while the dataset has all 4 quadrants -- this needs to be changed)
        motors = pulse_reducers.get('motors', lambda m: m[0])
        
        if tiles is None:
            tiles = lambda t: t.sum("train_pulse") if len(t.shape)>3 else t

        if mask is None:
            mask = self.mask if self.mask is not None else 1
             
        motorset = [(motors(x), motors(y)) for x,y in self.motors]
        geom = self._geom_from_motors(*tuple(motorset))

        tileset = tiles(self.tiles[pulse_slicer])
       
        xrd_image, xrd_center = geom.position_modules(tileset * mask)
        x, y, z = geom.get_pixel_positions().T

        result = {
            "image": DataArray(data=xrd_image,
                               coords={"x": np_array(range(xrd_image.shape[-2])) - xrd_center[-2],
                                       "y": np_array(range(xrd_image.shape[-1])) - xrd_center[-1]}),
            "metrics": {
                "imageChannelSize": ((x[-1,0,0] - x[0,0,0]) / x.shape[0],
                                     (y[0,-1,0] - y[0,0,0]) / y.shape[1]),
                "imageSize": xrd_image.shape,
                "imageCenter": tuple(xrd_center),
                "imageDistance": z.mean()
            }
        }

        result.update({k:pulse_reducers[k](self.passthrough_data[k]) \
                       for k in pulse_reducers.keys()})

        return result
