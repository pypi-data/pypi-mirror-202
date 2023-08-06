#!/usr/bin/python3

import xrayutilities as xu
from xarray import DataArray
import numpy as np

import logging

class LazyQMap:
    '''
    Container class for a stack of experimental data frames
    and associated metadata.

    The raw / authoritative data is stored in the `Chunk.data`
    container, which has a Python `dict()` like interface.
    Beyond that, this class also offers a number of processed
    data entries that are all lazily evaluated (i.e. only processed
    on first access):

      - `qimg`: A single 2D image of the Q-space converted data stack,
        on a rectantular grid (using an `xrayutilities` gridder, meaning
        that *all* of the original image stack is being used)

      - `qxaxis`: The X-axis of the gridder that produced `qimg`

      - `qyaxis`: The Y-axis of the gridder that produced `qimg`

    All of the computed data being *lazily* evaluated means that any
    processing that must take place on the raw (i.e. untransformed)
    data can -- and must -- take place before first access to any
    of the `q...` properties. E.g. for intensity normalization, you
    could do simething like: `chunk.data['img'] *= intensity` and
    only then proceed to accessing `chunk.qimg`.
    '''

    def __init__(self, setup=None, **data):
        '''
        Parameters:
          - `data`: A dicitonary with string keys (names) and arrays
            as the data fields.

          - `setup`: Experiment definition dictionary (see for instance
            nx5d.xrd.kmc3.ExperimentTemplate).

        '''
        
        self.data = data
        
        self.angles = {}
        if len(self.angles) == 0:
            self.angles.update(**(setup['goniometerAngles']))
            self.angles.update(**(setup['detectorTARAngles']))
            
        self.hxrd = self.__init_experiment(setup)
        self.Ang2Q = self.hxrd.Ang2Q


    def __init_experiment(self, setup):
        '''
        Initializes the Experiment part (i.e. xrayutilities HXRD object etc)
        with specified device and sample geometry. The optional parameter `roi`
        restricts angle-to-Q conversion to solely this region, if it is
        specified. This is a good way to save significant amounts of computing
        time.

        '''

        logging.debug("Expriment setup: %r" % setup)

        detAxes = [x for x in filter(lambda x: x is not None, setup['detectorTARAxes'])]

        qconv = xu.experiment.QConversion(sampleAxis=setup['goniometerAxes'],
                                          detectorAxis=detAxes,
                                          r_i=setup['beamDirection'],
                                          en=setup['beamEnergy'])

        hxrd = xu.HXRD(idir=setup['beamDirection'],
                       ndir=setup['sampleNormal'],
                       sampleor=setup['sampleFaceUp'],
                       qconv=qconv,
                       # Workaround for buggy xrayutilities: repeat the beam energy
                       en=setup['beamEnergy'])

        imageCenter = setup['imageCenter']
        if imageCenter is None:
            raise RuntimeError("Incomplete experimental definition (image center not defined)")

        assert len(imageCenter) == 2

        if imageCenter[0] <= 1 and imageCenter[1] <= 1:
            # It's a single number, all-in-one
            imgs = setup['imageSize']
            assert imgs is not None
            assert imgs[0] is not None
            assert imgs[1] is not None
            imageCenter = tuple([c*s for c,s in zip(setup['imageCenter'], imgs)])

        chSizeParm = {}
        if ('imageChannelSpan' in setup) and (setup['imageChannelSpan'] is not None):
            # channelSpan is degrees/channel, but we need to pass channels/degree to Ang2Q
            chSizeParm = {'chpdeg1': 1.0/setup['imageChannelSpan'][0],
                          'chpdeg1': 1.0/setup['imageChannelSpan'][1] }

        elif ('imageChannelSize' in setup) and (setup['imageChannelSize'] is not None):
            # Ang2Q takes one explicit distance parameter, but we're assuming that channelSize
            # is relative to the distance itself (putting the distance always at 1.0 units)
            chSizeParm = { 'pwidth1':  setup['imageChannelSize'][0],
                           'pwidth2':  setup['imageChannelSize'][1],
                           'distance': setup['imageDistance'] }

        else:
            raise RuntimeError("Experiment setup needs either the channel span or channel size")

        tarAngles = setup.get('detectorTARAngles', [0, 0, 0])

        roi = setup.get('roi', (0, setup['imageSize'][0], 0, setup['imageSize'][1]))

        hxrd.Ang2Q.init_area(detectorDir1=setup['imageAxes'][0],
                             detectorDir2=setup['imageAxes'][1],
                             cch1=imageCenter[0],
                             cch2=imageCenter[1],
                             Nch1=setup['imageSize'][0],
                             Nch2=setup['imageSize'][1],
                             tiltazimuth=0, #tarAngles[1],
                             tilt=0,        #tarAngles[0],
                             detrot=0,      #tarAngles[2],
                             roi=roi,
                             **chSizeParm)

        return hxrd    


    def __getitem__(self, label):
        return self.data[label]


    def __call__(self, *datasets, **kwargs):
        return self.area_qconv(*datasets, **kwargs)

    def area_qconv(self, *datasets, **kwargs):
        '''
        Front to the ang-to-Q conversion, currently only for area data. Parameters:
        `datasets` is either empty, or a single data label. (No multiple label support
        yet.)
        
        Accepted `kwargs`:

          - `qsize`: Tuple (w, h) of the resulting Q image, or `None` (default).
            If it is `None`, the size of the original angular image(s) is used.

          - `dims`: List with dimension names for resulting Q image.
            Defaults to `["qw", "qh"]`.

          - `_gridderDict`: If specified, this is a dictionary with extra named
            parameters to be passed on to the gridder. Note that this is not portable,
            only works as long as we're using xrayutilities under the hood.

          - `_ang2qDict`: Extra set of parameters to be passed to the data-specific
            `Ang2Q` function (typically `Ang2Q.area()` for stacks of 2D datasets).
        '''

        if len(datasets) > 1:
            raise RuntimeError("Can't transform more than one dataset at a time")

        label = next(iter(datasets  if len(datasets)>0 else self.data.keys()))
        img = self.data[label]
        
        dims = kwargs.setdefault('dims', ('qx', 'qy', 'qz'))

        if isinstance(dims, str):
            dims = (dims,)

        if len(dims) < 1 or len(dims) > 3:
            raise RuntimeError("Bad Q-axis specification: %r" % dims)
        
        if len(img.shape) != 3:
            raise RuntimeError("Don't know how to transform objects of shape %r" % (img.shape,))


        # Make sure all angles are arrays (even those that might have been passed as floats)
        ang = [a if hasattr(a, "__len__") else np.array([a]*len(img)) \
               for a in self.angles.values()]
            
        self.q = self.Ang2Q.area(*ang, **(kwargs.get('_ang2qDict', {})))

        # For transforming strings to dimension indices
        qspec = { 'x': 0, 'qx': 0,
                  'y': 1, 'qy': 1,
                  'z': 2, 'qz': 2 }

        # The list of individual Q directions/coordinates, according to user input 'dims'
        qcoord = [self.q[qspec[d]] for d in dims]

        # Default for 'qsize' is the size of the final Q-image -- make sure we account
        # for the possibly twisted order of Q-coordinates the user specified in 'dims'
        kwargs.setdefault('qsize', [img.shape[qspec[d]] for d in dims])

        # Call scheme of all the xrayutilities Gridders is pretty similar.
        Gridder = getattr(xu, "FuzzyGridder%dD" % len(dims))
        grd = Gridder(*(kwargs['qsize']))
        grd( *qcoord, img, **(kwargs.get('_gridderDict', {})) )

        # ...the tricky part is creating the DataArrays. Specifically,
        # retrieving the q coordinates from the gridder. They are in `grd`
        # attributes called 'xaxis', 'yaxis', ... according to dimension.
        # We always use qx/qy/qz for dimension keys.
        coords = {}
        for i,d in enumerate(dims):
            axname = d if len(d)>1 else 'q%s' % d
            axvals = getattr(grd, "%saxis" % ('x', 'y', 'z')[i])
            coords[axname] = axvals

        return DataArray(data=grd.data, coords=coords)

    
## Example for a class that does more than LazyQMap (namely accept angle offsets
## in its constructor), but still uses LazyQMap under the hood.
class OffsetQMap(LazyQMap):
    def __init__(self, offsets=None, **kwargs):
        super().__init__(**kwargs)
        if offsets is not None:
            for k,v in offsets.items():
                self.angles[k] += v
