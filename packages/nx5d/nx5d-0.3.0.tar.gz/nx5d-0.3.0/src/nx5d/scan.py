#!/usr/bin/python3

import time
from numpy import array as np_array

import logging

class HdfPathTemplateRestrictor:
    '''
    Takes a dictionary which may contain HDF5 paths in the values
    and "restricts" the template by replacing the templated values
    by the data at the corresponding HDF5 path.

    Works recursively on the data, i.e. if the dicitonary contains
    sub-structured data, the structure is retained. All values that
    don't contain HDF5 references are returned verbatim.

    For instance, using this template:
    ```
    {
       "h5data": "@/path/to/dataset",
       "static": 3.14,
       "nested": {
          "static": [3, 4, 5],
          "h5data": "@/path/to/another/dataset",
       }
    }
    ```

    Would return something like this (assuming that "/path/to/dataset"
    and "/path/to/another/dataset" are arrays containing `[1, 2]` and `[3, 4]`,
    respectively):
    ```
    {
       "h5data": [1, 2],
       "static": 3.14,
       "nested": {
          "static": [3, 4, 5],
          "h5data": [3, 4],
       }
    }
    ```
    
    '''
    
    def __init__(self, template,
                 accept=None,
                 paths=None,
                 passthrough=False):
        '''
        Initialises the template restrictor.

        Parmeters:
        
          - `template`: the configuration template dictionaray

          - `accept`: Places a whitelist restriction on the template
             keys to process and return. This is useful e.g. when
             template dictionaries are to be processed
             only partially. Note that unprocessed keys are _not_
             returned. Default is `None`, which disables the whitelist
             restriction.

          - `paths`: If specified, it's expected to contain a
            for path format substitutes, i.e. this enables the template
            to contain references liek "h5:#{key}", where `{key}` will
            be replaced with whatever is in `paths` at the corresponding
            dict slot.

          - `passthrough`: If set to `True`, instead of returning the
            the actual data for HDF5 references, the HDF5-like Python
            container will be returned (e.g. the dataset HDF5 node object).
            This is useful for accessing metadata provided by HDF5 (e.g.
            dataset sizes and shapes) without actually reading out
            possibly large amounts of data. Default is `False`.
        '''
        
        self._tmpl = { k:v for k,v in template.items() }
        self._paths = {k:v for k,v in (paths or {}).items() }
        self._accepted = accept or [k for k in template.keys()]
        self._pass = passthrough


    def __value(self, h5like, value, fmtKeys, nodeOnly=False, slicer=slice(None)):
        '''
        This is the heard of the HDF5 address data lookup system: it checks
        the contents of `value` and returns the corresponding data as expected.
        The trick is in correctly determining the meaning of `value` here.

        The simples assumption here is that `value` is, indeed, a real piece
        of data (i.e. a number or an array with numbers), in which case it
        should be returned verbatim.

        But mostly this isn't the case. `value` might typically differ from
        a pure value in two ways (or any combination thereof):

          1. `value` is a string reference to a path within a HDF5-like
             object (file or node) -- here referenced by `h5like`.

          2. `value` is a container (tuple or dict) that we need to recursively
             descend into and look at each item individually.

        
        For the case of (1), the distinction is the following:
        
          - If `value` is a string that begins with `@`, then it is taken
            as a HDF5 address relative to `h5like`. The string is assumed
            to be a format (e.g. "contain {key}") where the keys to be
            substituted are taken from `fmtKeys`.

          - If `value` is a tuple which's first item is a string that begins
            with "@", and *all* other items are `slice()` objects, then
            the first item of the tuple is assumed to be the HDF5 path
            (as above), but instead of returning the value as-is, it is
            sliced using the provided slicer.

          - Everything else is returned as-is.


        We enter the case of (2) if neither of the above is the case, i.e.
        if `value` is either a dict, or another type of container (tuple
        with different items than (string, slice, ...),

          - If `value` is a tuple that doesn't fit the ("addr", slice()...)
            form, or is a dictionary, we need to recursively call
            `__valyue()` for each of the items.

        
        The function finally returns something that has the same
        structure as `value`, but eventual HDF5 paths are replaced by
        actual data as requested.
        '''

        my_slicer = slicer

        # Check if value is a fancy ("addr", slice(), ...) tuple.
        # If it is, rewrite `value` to actually contain only the address,
        # and append the slicing part `value` to the slicer argument.
        if isinstance(value, tuple) and \
           len(value)>=2 and \
           (isinstance(value[0], str) and value[0][0] == '@') and \
           np_array([isinstance(v, slice) for v in value[1:]]).all():
            if isinstance(slicer, tuple):
                my_slicer = (*slicer, *value[1:])
            else:
                my_slicer = (slicer, *value[1:])
            value = value[0]


        if isinstance(value, str):
            # The main feature: loading data from HDF5 if we encounter an "@..." string.
            # FIXME: need to actually rewrite this and base this on the __call__() feature
            # (see below). This will simplify many things.

            if len(value) == 0 or value[0] != '@':
                return value
            
            nodeAddrFmt = value[1:]
            
            try:
                nodeAddr = nodeAddrFmt.format(**fmtKeys)

                node = h5like[nodeAddr]
                
                logging.debug("Loading data from %s (only node: %r)" % (nodeAddr, nodeOnly))
                
                if nodeOnly:
                    return node
                else:
                    try:
                        s = tuple(my_slicer[:len(node.shape)]) if isinstance(my_slicer, tuple) else my_slicer
                        return node[s]
                    #except TypeError:  # ...not sure when this happens (?)
                    #    return node
                    except ValueError: # This happens when value is a scalar and needs to be sliced by ()
                        return node[()]
                        

            except KeyError as e:
                logging.error("Path substitition error in '%s': %s" % (nodeAddrFmt, str(e)))
                raise
                    
            except Exception as e:
                logging.error("%s: error reading node (%r)" % (nodeAddr, str(e)))
                raise
                
        elif isinstance(value, dict):
            # Descending into each of the elements
            return dict({k:self.__value(h5like, v, fmtKeys, nodeOnly, slicer) for k,v in value.items()})
        
        elif hasattr(value, "__len__"):
            # It's not a string and it's not a dict, but is iterable?
            # descend and find out.
            return tuple([self.__value(h5like, v, fmtKeys, nodeOnly, slicer) for v in value])

        elif hasattr(value, "__call__"):
            # This allows us to create custom objects that retrieve
            # data from unconventional sources.
            return value(h5like, nodeOnly, slicer)

        else:
            return value

        
    def __call__(self, h5like=None, paths=None, nodeOnly=False, slicer=slice(None)):
        '''
        Uses the stored template to generate meaningful content based on the
        data from `h5like`. Typically, this involves going through all the
        templates' values and checking whether they consist of real data
        or H5 paths that need to be read. All paths are relative to `h5like`.

        If `nodeOnly` is set to `True`, the HDF5 nodes at the "nx5:" dataset
        paths is returned. Otherwise the `.value` property is read.

          - `slicer`: If specified, it is applied to any data that is to
            be retrieved from the HDF5-like node, insofar as the data shape
            matches the dimensionality of the slicer; if the slicer has
            too many components (e.g. a 3D-slicer on 1D data), the slicer
            is sliently truncated.        
        '''

        if h5like is None:
            return {k:v for k,v in self._tmpl.items()}

        combinedPaths = {k:v for k,v in self._paths.items()}
        combinedPaths.update((paths or {}))

        retr = {}
        for k,v in self._tmpl.items():
            if k in self._accepted:
                val = self.__value(h5like, v, fmtKeys=combinedPaths,
                                   nodeOnly=nodeOnly, slicer=slicer)
                retr[k] = val
                continue

            if self._pass:
                retr[k] = v

        return retr


class SetupGenerator(HdfPathTemplateRestrictor):
    '''
    Generic builder to generate an "experiment setup" dictionary.

    Concepts
    ========
    
    The structure of an experiment setup contains several types
    of data:

      - "Static" persistent device geometry data, e.g. the type
        and axes of the goniometer etc

      - "Static" transient data which is valid for a particular
        data set or scan, but not necessarily for others, e.g.
        current center of the detector plate, photon energy etc

      - "Dynamic" data which might changes from frame to frame
        (mostly positioners and auxiliary experimental data like
        ring gurrent etc.

    "Static" persistent data
    ------------------------
    
    All notations and conventions are analogous to `xrayutilities`
    device / goniometer setup:

      - `goniometerAxes`: The direction of each of the goniometer axes in
        the `[xyz][+-]` notation. This is a variable-sized array, as there
        can be several axes in any goniometer, and `xrayutilities` apparently
        magically knows what to do.

      - `detectorTARAxes`: The direction of each of the 3 possible movement
        axes of the detector (tilt, azimuth, rotation). Note that there are
        always 3 of these axes each with a very specific purpose in
        `xrayutilties`. If your detector lacks any, complement with `None`.

      - `imageAxes`: The direction of the image axes (x and y) at zero angles.
        The positive direction of the axes should coincide with increasing pixel
        index in the data.

      - `imageCenter`: This is the positio of the center pixel, either absolute
        (integer pixel numbers), or relative to the sensor size (as specified in
        `imageAxes`). If the number is in the range 0.0..1.0, then relative
        positioning is assumed.

      - `imageChannelSpan` / `imageDistAndPixsize`: for Q transformation,
        ultimately the relation between every specific on the detectors and the angle
        of the incoming beam activating that specific pixel is needed. There
        are two distinct ways of specifying this: either using the "channel span",
        i.e. the size, in degrees, of each pixel, in horizontal/vertical direction,
        or by a distance parameter (from detector to sample) and a pixel size.
        `imageChannelSpan` is either a single number or a 2-tuple specifying
        how many degrees one channel takes. `imageChannelSize` specifies the
        spatial size of a pixel relative to the distance between the sample
        and the sensor.

      - `sampleFaceUp`: Direction of the "sample surface facing up", a.k.a.
        "sampleor" in `xrayutilities` lingo. This is the orientation of
        the sample surface at zero angles. This is either an axis notation
        (`[xyz][+-]`) or one of the special words `det`, respectively `sam`.


    Example for device geometry:

    ```
    {
      "goniometerAxes": ('y+', 'z+', 'x+'),
    
      "detectorTARAxes": (None, "z+", None),
      "imageAxes": ("x+", "z+"),
      "imageSize": (1024, 768),
      "imageCenter": (0.5, 0.5),
      "imageChannelSpan": (None, None),
      "imageChannelSize": (None, None),
    
      "sampleFaceUp": 'x+',
      "beamDirection": (0, 1, 0),
    }

    ```

    "Static" itinerant data
    -----------------------

    Experiment setup contains additional parameters specific to the current
    experiment (as opposed to: typical for the experimentl setup). These
    include:

      - `sampleNormal`: Direction perpendicular to the surface. Please also
        consult the official `xrayutilites` documentation as to the exact meaning
        of the directions.

      - `beamEnergy`: energy of the x-ray beam (in eV).

      - `detectorTARAngles`: (optional) angle values for tilt, azimuth and
        rotation of the detector. Default values for each of these angles is
        0. Only angles which are not `None` in `detectorTARAxes` are accepted.

    Example for the sample geometry setup:
    ```
    {
      "sampleNormal": (0, 0, 1),
      "beamEnergy": 15000.0,
      "detectorTARAngles": (0, 0, 0),
    }
    ```

    
    "Dynamic" measurement data
    --------------------------

    These include mostly goniometer axes, homing offsets etc. There is either
    one of these per scan, or one per frame (i.e. a whole container/array of
    such elements per scan). These include:

      - `goniometerAngles`: positioning for each of the angles of the
        goniometer, as specified in `goniometerAxes`

      - `detectorTARAngles`: positioning for the detector tilt, azimuth
        and rotation (as in `detectorTARAxes`)

    Some of these configuration parameters (e.g. the goniometer angles) are
    inherently "not fixed" as they are an essential part of the measurement.
    Others, like the detector angles, may or may not be fixed (e.g. detector
    might be permanently fixed at an azimuth different from 0, or may
    change with every frame or with every scan, etc).

    For this reason, not only scalar numbers are accepted, but actually
    HDF5 dataset addresses as string. Here is an example of how such a
    setup definition might look like:

    ```
    {
      "goniometerAngles": ("Theta", "Phi", "Chi"),
      "detectorTARAngles": (0, "Psi", 0)
    }
    ```

    Here, the dataset "Theta" with respect to the default positioner path
    would be used as the first goniometer angle (for ESRF-style HDF5, this
    would be "instrument/positioners/Theta".)

    There might also be other positioning parameters relevant for data
    transformation and analysis, for instance "TwoTheta" instead of "Psi",
    which would have a similar meaning except for a different
    direction / offset, with respect to "Psi." In essence, it's the
    responsibility of higher layers to decide what addresses / angles should
    be used here.

    There is no data pendant to the `imageAxes` parameter because the angle
    information for each image is within the index of its own pixels.
    The data set may also contain other data of interest (e.g. "SBcurrent"),
    but that is viewed as something to be accessed in parallel to, and not
    as a basis of, the main image data.

    Each of the data fielts itself (e.g. "image", but also others like
    "SBcurrent", "delay", ...) which may be imporant for the physical analysis,
    but not to the transformation of data, is not a matter of `ExperimentalSetup`
    (FIXME: or is it?) but one of data collection fields within
    `ScanReader`.

    Placeholder variables
    ---------------------

    When using HDF5 paths as placeholders, `SetupGenerator` can use string
    formatting if a dictionary of keys is supplied at `__init__`
    or at `__call__`. `ScanReader` supplies the following keys, compatible
    with the ESRF flavor of HDF5/Nexus data format:

      - "instrument": The top level directory containing instrument information,
        typically of HDF5 type "NXinstrument" and located at "./instrument"
        within the scan.

      - "positioners": Typically at "./instrument/positioners", usually
        important for all the angle definitions

      - "measurement": Top-level folder (of type "NXcollection") containing
        the measurement data (typically "./measurement").

    Usage
    =====

    The idea is to make a 3-step process:

      1. Create dictionary (with keys above) that specify static
         parameters as far as possible, and contains HDF5 paths/addresses
         for the rest

      2. Pass on dictionary to `ExperimentSetup` class, which stores the
         explicitly passed values, and also offers an interface (upon
         construction or later) to override or modify keys

      3. Override `ExperimentSetup.__call__()` to export a "final" version
         of the data, hand-matched for the current scan dataset (passed on
         as parameter to `__call__()`) which does not contain anything
         else besides pure, usable values :-)

    (FIXME: the whole "\\*Angles" section is actually supposd to *not* know
    about loading data yet... isn't it? In a way, the Angles section is
    less like "experimental setup" and more like "measurement results.")
    '''

    # ( FIXME: not sure whether there is "the" / "only one" main image data,
    # or if there should be allowed for several. On one hand, scalar arrays
    # like "SBcurrent" suggest that there's nothing special about "the" image;
    # on the other hand, angles and goniometer parameters are valid for *one*
    # specific detector location, so if we were to accept several detector(-like)
    # images as data, we'd need to duplicate some of the "static" information,
    # and also account for that within the `ScanReader` object.
    # As it stands, the architecture is only for *one* detector, obviously.)

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         accept=[ "beamDirection",
                                  "beamEnergy",
                                  "goniometerAxes",
                                  "detectorTARAxes",
                                  "imageAxes",
                                  "imageCenter",
                                  "imageChannelSize",
                                  "imageChannelSpan",
                                  "imageSize",
                                  "sampleFaceUp",
                                  "sampleNormal" ],
                         **kwargs)


class PositionerGenerator(HdfPathTemplateRestrictor):
    '''
    Template restrictor for positioner data (detector and goniometer angle data).
    Affects only "goniometerAngles" and "detectorTARAngles" keys.
    See also `SetupGenerator` for a detailed discussion.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         accept=[ "detectorTARAngles",
                                  "goniometerAngles" ],
                         **kwargs)

    
class ScanReader:
    '''
    Loads data from one X-ray diffraction (XRD) scan run and offers
    convesion of images to Q space for further analysis.
    
    The idea is to open/initialize metadata (experimental parameters,
    ROIs, sizes, ...) on construction, and then subsequently "pull out"
    image data. This is supposed to work on a "live" file, i.e. one
    being measured and having data added to it.

    It assumes that data is available in a HDF5-like interface.
    It opens/closes the data object with every use to account for
    parallel use by data acquistion and/or other consumers.

    The assumptions to the data are, essentially (see also `nx5d.xrd.kmc3`):

      - All relevant datasets (frame images, angles etc) are organized
        as (arrays) of datasets with the first coordinate corresponding
        to the progression of frames, i.e. Nx(WxH) for images N for a
        particular angle etc.

      - The frame number progression (index starting with 0) corresponds
        to one or two experimental scan parameters, i.e. time delay (for
        pump-probe experiments), or a particular tilt angle. The `Chunk`
        object reflects this.

      - Instrument definition and angles are compatible with `xrayutilities`,
        the package used for the Q-space conversion.

      - The data has a Nexus-like / ESRF-style layout; this means that
        all relevant measurement data is under a specific folder of type
        "NXcollection" (typically called "measurement", but this is
        configurable), and all relevant parameterisation is stored under
        another folder (typically "instrument/positioners", but again,
        configurable). Data specification is expected relative to these
        folders.

      - Quite generally, the assumption is that we're interested in one or
        more measurement sets, and each of those depends on a subset of
        positioners.
    
    '''
    
    def __init__(self, H5pyLike, scan,
                 h5kwargs=None,
                 pathKeys=None,
                 **dreq):
        '''
        Initializes the object and basic experimental parameters.
        Needs the following:

          - `H5pyLike`: A class or a factory which generates a `h5py`-like object for
            data access. Defaults to `h5py.File`, but objects with a similar API
            (e.g. the `silx.io.spech5.SpecH5` kind of loaders) are also accepted.        

          - `scan`: A parameter list that contains information to be passed to
            `H5pyLike` in order to locate the scan within the data container.
            If the first item in that list is a string (i.e. a file path), then
            the format "resource[#path]" is accepted to pass on both the file name
            ("resource") and the path inside the container ("path"). All other
            items are passed on as unnamed arguments to `H5pyFile`.
            A typical example of this is for instance
            `("/path/to/file.h5#scan23", "r")` if `H5pyLike` is a `h5py.File`
            object. For convenience, if `H5pyLike` is indeed a `h5py.File`.

          - `h5kwargs`: `None` by default, but can be passed a dictionary of named options
            to be passed on to `loader` in addition to the resource locator string.

          - `pathKeys`: Dictionary with shortcuts of standard (?) paths. Currently,
            `ScanReader` recognizes and uses the following paths:
        
              - "measurement": Where the data is

              - "positioners": Where the positioners are (e.g. angles)

          - `dreq`: This is a list of "data request" named parameters, i.e. each key is
            a measureables, to which the value is a list of other measureables or
            poisitioners. The names of the data are relative to `measurablePath`,
            respectively `positionerPath`. The data labels may also contain a path
            component (e.g. "detector/image"), in which case all path separators
            ("/") will be replaced by underscore when data naming is performed
            ("detector_image").

            FIXME: not exactly sure how this is supposed to work. There are two main
            problems with it.
        
             1. The angles: designation of axes (goniometer, detector and image)
                are already in the 'setup' parameter. But the _actual_ angles themselves
                are not. So we have two options here: squeeze them in 'setup' (in which
                case: what is this parameter for?), or squeeze them here (in which case:
                in which order? See also 2...)

             2. The data itself: most of the time the data is the actual detector
                image / frame data. But sometimes we have data of secondary interest,
                e.g. SBcurrent (ring curren) or similar, e.g. for normalization. *This*
                data does not depend on any kind of angles or positioners... or may
                only depend on _some_ positioners. How do we model that?
        '''

        self.pathKeys = pathKeys or {'measurement': 'measurement',
                                     'positioners': 'instrument/positioners',
                                     'instrument': 'instrument' }
        
        self.h5kwargs = h5kwargs or {}

        self.dataSource = self.__source_factory(scan, H5pyLike)

        self.setupTemplate = dreq.get("setup", {})

        self.requiredDatasets = dreq.copy()

        
    def __source_factory(self, params, H5pyLike):
        # Implements magic to parse out the '#path' part of the filename.
        # Returns a callable that creates a usable h5py-like object
        # for querying scan data.

        self.H5pyLike = H5pyLike
        fileUrl, fileArgs = (None, tuple())

        if isinstance(params, str):
            fileUrl = params
        elif isinstance(params, tuple):
            fileUrl, fileArgs = params[0], params[1:]
        else:
            fileUrl = params

        if isinstance(fileUrl, str):
            filePath, self.h5scan = fileUrl.split('#')
            self.h5args = tuple([filePath] + list(fileArgs))
        else:
            self.h5scan = None
            self.h5args = (fileUrl,)

        print("H5like: %r (%r, %r)" % (self.H5pyLike, self.h5args, self.h5kwargs))

        if self.h5scan:
            return lambda: self.H5pyLike(*(self.h5args), **(self.h5kwargs))[self.h5scan]
        else:
            return lambda: self.H5pyLike(*(self.h5args), **(self.h5kwargs))


    def __defPath(self, locator):
        ''' Translates "syntactic sugar" when specifying certain HDF5 data locators.
        
        Takes a HDF5 locator as accepted by `HdfPathTemplateRestrictor` and if it's
        a string, or a tuple (str, slice, ...) adds default paths in front
        of the string if necessary (e.g. turns "data" into "@{measurement}/data").

        Everything else is returned unchanged.

        Args:
            locator: eiter a string containing a HDF5 address (`"@..."`), or a tuple
              `("...", slice(), ...)` containing a HDF5 address as its first element
              and only slice objects for every other element.

        Returns:
            The locator, translated to contain a proper HDF5 addressing ("@..."),
            or verbatim if it's not a string or a slicing tuple.
        '''

        path_mangler = lambda p: p if p.find('/')>=0 \
            else '@%s/%s' % (self.pathKeys['measurement'], p)
        
        if isinstance(locator, str):
            return path_mangler(locator)
        
        elif isinstance(locator, tuple) and isinstance(locator[0], str):
            return (path_mangler(locator[0]), *(locator[1:]))

        else:
            return locator


    def read (self, frameSlicer, h5like=None, lean=True, **dataKeys):
        '''
        Returns a bunch of image(s) starting with `start`
        (default: last image taken). If `number` is None,
        all the images to the end of the scan are read.
        Parameters:
        
          - `frameSlicer`: A slice object for selecting frames within a scan
            series.

          - `roiSlicer`: Additional slicer or tuple of slicers to apply to the
            a data frame, e.g. for selecting only specific parts of the data
            frame (region-of-interest). Note that this slicer will be applied
            to *all* data keys to retrieve (see also the `dataKeys` parameter
            below), to the extent to which they have the correct dimensionality.

          - `h5like`: A h5py-like object to use for reading. If none is
            specified, the one generated by the internal `dataSource()`
            factory is used.

          - `lean`: If `True`, the "required datasets" (i.e. those that were
            specified with `__init__()`) are omitted from the result. This is
            the default.
        
          - `**dataKeys`: Data sets to retrieve; the name of the parameter will
            result in a key, and the value of the parameter should refer to the
            corresponding HDF5-like dataset path. This is passed to
            `HdfPathTemplateRestrictor`, so please also refer to the documentation
            of that class.
        
        '''        
        data = {} if lean else self.requiredDatasets.copy()
        data.update({k:self.__defPath(v) for k,v in dataKeys.items()})

        with h5like or self.dataSource() as h5:
            return HdfPathTemplateRestrictor(data, paths=self.pathKeys)\
                (h5, slicer=frameSlicer)
    

    def streaks(self, delta=None, length=None, by=None, h5like=None, retry=0, **dataKeys):
        '''
        Uses `read()` to return chunks of the data as specified by
        the `offset` and `increment parameters.
        The `addrproc` and `sliceproc` parameters are passed on to `read()`.
        
        Parameters:
        
          - `delta`: Take every `delta`-th frame to build a chunk
        
          - `length`: Take `length` consecutive frames to build a chunk
        
          - `h5like`: h5py-like object to use for reading. If none is specified
            (default), then the internal `dataSource()` method is being used,
            which initializes a new h5py object as specified in `__init__()`.

          - `worker`: Worker object ("Chunk object") to return. This
        
          - `retry`: If non-zero or not `None`, file opening/reading
            is retried on `OSError` type of exceptions up to `retry`
            number of seconds (fractional number also possible)
          
        Typically only either `delta` or `length` is necessary.
        '''

        def slicer_generator(numFrames):
            if length is None and delta is not None:
                for start in range(0, delta):
                    slicer = slice(start, None, delta)
                    yield slicer
            elif length is not None and delta is None:
                if numFrames == -1:
                    raise RuntimeError("Can't determine the number of frames from "
                                       "requested data keys")
                for start in range(0, numFrames, length):
                    slicer = slice(start, start+length, 1)
                    yield slicer
            elif length is None and delta is None:
                yield slice(None)
            else:
                raise RuntimeError("Specify either `length' or `delta' but not both.")


        with h5like or self.dataSource() as h5:

            numFrm = -1

            # read an explicit number of frames if there are any data keys,
            # otherwise we'll stick with -1 (undefined) and slicer_generator()
            # might still be able to get something out of it if enough
            # other parameters have been specified (specifically, 'delta')
            if len(dataKeys) > 0:
                tmp = next(iter(dataKeys.items()))[1]
                tmp2 = tmp if isinstance(tmp, str) else tmp[0]
                numFrm = self.numFrames(tmp2, h5like=h5like)

            scan = h5
            
            for slicer in slicer_generator(numFrm):
                begin = time.time()
                while True:
                    now = time.time()
                    try:
                        yield self.read(slicer, **dataKeys, h5like=h5, lean=False)
                        break

                    except OSError:
                        if not retry or (now-begin) > retry:
                            logging.error("Final error, %f seconds after initial start" % (now-begin))
                            raise
                        else:
                            logging.debug("OSError, retrying for another %f seconds" % (now-begin-retry))

    
    def numFrames(self, dataset, h5like=None):
        '''
        Reads (returns) the number of frames from the HDF5 file
        for the dataset refered to by `dataset`.
        '''

        with h5like or self.dataSource() as h5:

            # FIXME
            # The only reason we use "node only" here is to avoid loading
            # potentially large datasets (.shape is also available in a
            # HDF5 node without actually loading the data into memory).
            #
            # But this fucks up the HdfPathTemplateRestrictor design...
            # so we somehow need to get rid of it.
            
            data = HdfPathTemplateRestrictor({'data': self.__defPath(dataset)},
                                             paths=self.pathKeys)(h5, nodeOnly=True)
            return data['data'].shape[0]
