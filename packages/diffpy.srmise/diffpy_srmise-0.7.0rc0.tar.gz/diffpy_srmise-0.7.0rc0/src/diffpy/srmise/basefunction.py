#!/usr/bin/env python
##############################################################################
#
# SrMise            by Luke Granlund
#                   (c) 2014 trustees of the Michigan State University
#                   (c) 2024 trustees of Columbia University in the City of New York
#                   All rights reserved.
#
# File coded by:    Luke Granlund
#
# See LICENSE.txt for license information.
#
##############################################################################
"""Defines BaseFunction, the base class for mathematical functions in srmise."""

import logging
import re
import sys

import numpy as np

from diffpy.srmise.srmiseerrors import SrMiseDataFormatError

logger = logging.getLogger("diffpy.srmise")


class BaseFunction(object):
    """Base class for mathematical functions which model numeric sequences.

    Attributes
    -------------
    parameterdict : dict
        The dictionary mapping string keys to their index in the
        sequence of parameters.  These keys apply only to the
        default "internal" format.
    parformats : array-like
        The sequence of strings defining what formats are recognized
        by a function.
    default_formats : dict
        The dictionary which maps the strings "default_input" and
        "default_output" to strings also appearing in parformats.
        "default_input"-> format used internally within the class
        "default_output"-> Default format to use when converting
         parameters for outside use.
    metadict : dict
        The Dictionary mapping string keys to tuple (v, m) where v is an
        additional argument required by function, and m is a method
        whose string output recreates v when passed to eval().
    base : BaseFunction subclass
        The basefunction subclass instance which this one decorates with
        additional functionality.

    Class methods (implemented by inheriting classes)
    -------------------------------------------------
    actualize()
    estimate_parameters() (optional)
    _jacobianraw() (optional, but strongly recommended)
    _transform_derivatives() (optional, supports propagation of uncertainty for different paramaterizations)
    _transform_parametersraw()
    _valueraw()

    Class methods
    -------------
    jacobian()
    value()
    transform_derivatives()
    transform_parameters()
    """

    def __init__(
        self,
        parameterdict,
        parformats,
        default_formats,
        metadict,
        base=None,
        Cache=None,
    ):
        """Set parameterdict defined by subclass

        Parameters
        ----------
        parameterdict : dict
            The dictionary mapping string keys (e.g. "position")
            to their index in a sequence of parameters for this
            PeakFunction subclass.  Every parameter must appear.
        parformats : array-like
            The sequence of strings containing all allowed input/output
            formats defined for the function's parameters.
        default_formats : dict
            The dictionary mapping the string keys "internal" and
            "default_output" to formats from parformats.
        metadict : dict
            The dictionary mapping string keys to additional arguments
            required by function.
        base : basefunction subclass
            The basefunction subclass instance which this one decorates with
            additional functionality.
        Cache : class
            The class (not instance) which implements caching of BaseFunction
            evaluations.
        """

        self.parameterdict = parameterdict
        self.npars = len(self.parameterdict)

        # Checking all these things at run-time is a bit heavy-handed, but the
        # overhead is small and it may prevent considerable confusion when
        # developing new functions.

        # Check validity of parameterdict.  Although dictionaries handle
        # arbitrary types, parameters are indexed by these keys as well as
        # integer indices.  Restricting keys to strings keeps things sane.
        for p in self.parameterdict.keys():
            if not isinstance(p, str):
                emsg = "Argument parameterdict's keys must be strings."
                raise ValueError(emsg)

        # Convert values to list and sort
        vals = list(self.parameterdict.values())
        vals.sort()

        # Check if the sorted values match the sequence from 0 to npars-1
        if vals != list(range(self.npars)):
            emsg = (
                "Argument parameterdict's values must uniquely specify "
                + "the index of each parameter defined by its keys."
            )
            raise ValueError(emsg)

        self.parformats = parformats

        # Check validity of default_formats
        self.default_formats = default_formats
        if not ("default_input" in self.default_formats and "default_output" in self.default_formats):
            emsg = "Argument default_formats must specify 'default_input' " + "and 'default_output' as keys."
            raise ValueError(emsg)
        for f in self.default_formats.values():
            if f not in self.parformats:
                emsg = "Keys of argument default_formats must map to a " + "value within argument parformats."
                raise ValueError()

        # Set metadictionary
        self.metadict = metadict

        # Set base function (for modifying existing functions)
        self.base = base

        # Implement caching here.
        # Defined in this way, each cache is associated with a single instance
        # of PeakFunction.
        # Object to cache: (basefunctioninstance, tuple of parameters)
        if Cache is not None:
            # self.value = Cache(self.value, "value")
            # self.jacobian = Cache(self.jacobian, "jacobian")
            pass
        return

    # "Virtual" class methods ####

    def actualize(self, *args, **kwds):
        """Create ModelPart instance of self with given parameters.  ("Virtual" method)"""
        emsg = "actualize() must be implemented in a BaseFunction subclass."
        raise NotImplementedError(emsg)

    def estimate_parameters(self, *args, **kwds):
        """Estimate BaseFunction parameters from supplied data. ("Virtual" method)"""
        emsg = "estimate_parameters() must be implemented in a BaseFunction subclass."
        raise NotImplementedError(emsg)

    def _jacobianraw(self, *args, **kwds):
        """Calculate the jacobian. ("Virtual" method)"""
        emsg = "_jacobianraw() must be implemented in a BaseFunction subclass."
        raise NotImplementedError(emsg)

    def _transform_derivativesraw(self, *args, **kwds):
        """Convert BaseFunction parameters to another form. ("Virtual" method)"""
        emsg = "transform_parameters() must be implemented in a BaseFunction subclass."
        raise NotImplementedError(emsg)

    def _transform_parametersraw(self, *args, **kwds):
        """Convert BaseFunction parameters to another form. ("Virtual" method)"""
        emsg = "transform_parameters() must be implemented in a BaseFunction subclass."
        raise NotImplementedError(emsg)

    def _valueraw(self, *args, **kwds):
        """Calculate value of function. ("Virtual" method)"""
        emsg = "_valueraw must() be implemented in a BaseFunction subclass."
        raise NotImplementedError(emsg)

    # Class methods ####

    def jacobian(self, p, r, rng=None):
        """Calculate jacobian of p, possibly restricted by range.

        Parameters
        ----------
        p : ModelPart instance
            The ModelPart to be evaluated
        r ：array-like
            sequence or scalar over which function is evaluated
        rng : slice object
            Optional slice object restricts which r-values are evaluated.
            The output has same length as r, but unevaluated objects have
            a default value of 0.  If caching is enabled these may be
            previously calculated values instead.
        """
        if self is not p._owner:
            emsg = "Argument 'p' must be evaluated by the BaseFunction " + "subclass which owns it."
            raise ValueError(emsg)

        # normally r will be a sequence, but also allow single numeric values
        try:
            if rng is None:
                rng = slice(0, len(r))
            rpart = r[rng]
            jac = self._jacobianraw(p.pars, rpart, p.free)
            output = [None for j in jac]
            for idx in range(len(output)):
                if jac[idx] is not None:
                    output[idx] = r * 0.0
                    output[idx][rng] = jac[idx]
            return output
        except TypeError:
            return self._jacobianraw(p.pars, r, p.free)

    def transform_derivatives(self, pars, in_format=None, out_format=None):
        """Return gradient matrix for pars converted from in_format to out_format.

        Parameters
        ----------
        pars : array-like
            The sequence of parameters
        in_format : str
            The format defined for this class
        out_format : str
            The format defined for this class

        Returns
        -------
        array-like
            The gradient matrix for pars converted from in_format to out_format.
        """
        # Map unspecified formats to specific formats defined in default_formats
        if in_format is None:
            in_format = self.default_formats["default_input"]
        if out_format is None:
            out_format = self.default_formats["default_output"]

        # Map generic formats to specific formats defined in default_formats
        if in_format == "default_input":
            in_format = self.default_formats["default_input"]
        elif in_format == "default_output":
            in_format = self.default_formats["default_output"]
        if out_format == "default_output":
            out_format = self.default_formats["default_output"]
        elif out_format == "default_input":
            out_format = self.default_formats["default_input"]

        if in_format not in self.parformats:
            raise ValueError("Argument 'in_format' must be one of %s." % self.parformats)
        if out_format not in self.parformats:
            raise ValueError("Argument 'out_format' must be one of %s." % self.parformats)
        if in_format == out_format:
            return np.identity(self.npars)
        return self._transform_derivativesraw(pars, in_format=in_format, out_format=out_format)

    def transform_parameters(self, pars, in_format=None, out_format=None):
        """Return new sequence with pars converted from in_format to out_format.

        Also restores parameters to a preferred range if it permits multiple
        values that correspond to the same physical result.

        Parameters
        ----------
        pars : array-like
            The sequence of parameters
        in_format ： str
            The format defined for this class
        out_format : str
            The format defined for this class

        Returns
        -------
        array-like
            The new sequence of parameters with out_format.
        """
        # Map unspecified formats to specific formats defined in default_formats
        if in_format is None:
            in_format = self.default_formats["default_input"]
        if out_format is None:
            out_format = self.default_formats["default_output"]

        # Map generic formats to specific formats defined in default_formats
        if in_format == "default_input":
            in_format = self.default_formats["default_input"]
        elif in_format == "default_output":
            in_format = self.default_formats["default_output"]
        if out_format == "default_output":
            out_format = self.default_formats["default_output"]
        elif out_format == "default_input":
            out_format = self.default_formats["default_input"]

        if in_format not in self.parformats:
            raise ValueError("Argument 'in_format' must be one of %s." % self.parformats)
        if out_format not in self.parformats:
            raise ValueError("Argument 'out_format' must be one of %s." % self.parformats)
        # if in_format == out_format:
        #    return pars
        return self._transform_parametersraw(pars, in_format=in_format, out_format=out_format)

    def value(self, p, r, rng=None):
        """Calculate value of ModelPart over r, possibly restricted by range.

        Parameters
        ----------
        p : ModelPart instance
            The ModelPart to be evaluated
        r : array-like or float
            The sequence or scalar over which function is evaluated
        rng : slice object
            Optional slice object restricts which r-values are evaluated.
            The output has same length as r, but unevaluated objects have
            a default value of 0.  If caching is enabled these may be
            previously calculated values instead.

        Returns
        -------
        array-like
            The value of ModelPart over r, possibly restricted by range.
        """
        if self is not p._owner:
            emsg = "Argument 'p' must be evaluated by the BaseFunction " + "subclass which owns it."
            raise ValueError(emsg)

        # normally r will be a sequence, but also allow single numeric values
        try:
            if rng is None:
                rng = slice(0, len(r))
            rpart = r[rng]
            output = r * 0.0
            output[rng] = self._valueraw(p.pars, rpart)
            return output
        except TypeError:
            return self._valueraw(p.pars, r)

    def pgradient(self, p, format):
        """Return gradient matrix of parameterization in specified format wrt "internal" format at p.

        Consider the "internal" parameterization given by (i0, i1, ..., in).
        Each parameter in a different format, say (o0, o1, ..., om), is a
        function of the internal parameters.

        The gradient matrix is
        [[do0/di0 do0/di1 ... do0/din]
         [do1/di0 do1/di1 ... do1/din]
         ...
         [dom/di0 dom/di1 ... dom/din]]
        In the trivial case where format="internal", returns an identity matrix.

        Parameters
        ----------
        p : ModelPart instance
            The ModelPart instance to be evaluated for gradient calculation.
        format : str
            The format of the parameters

        Returns
        -------
        array-like
            A 2D array containing the partial derivatives.
        """
        return

    def getmodule(self):
        """Return 'diffpy.srmise.basefunction'"""
        return "diffpy.srmise.basefunction"

    def writestr(self, baselist):
        """Return string representation of self.

        References to other BaseFunction instances are replaced by their index
        in baselist.

        Parameters
        ----------
        baselist : array-like
            The list of BaseFunction (or subclass) instances.

        Returns
        -------
            The string representation of self.
        """
        if self.base is not None and self.base not in baselist:
            emsg = "baselist does not include this BaseFunction's base function."
            raise ValueError(emsg)
        lines = []
        # Write function type
        lines.append("function=%s" % repr(self.__class__.__name__))
        lines.append("module=%s" % repr(self.getmodule()))
        # Write base
        if self.base is not None:
            lines.append("base=%s" % repr(baselist.index(self.base)))
        else:
            lines.append("base=%s" % repr(None))
        # Write all other metadata
        for k, (v, f) in self.metadict.items():
            lines.append("%s=%s" % (k, f(v)))
        datastring = "\n".join(lines) + "\n"
        return datastring

    @staticmethod
    def factory(functionstr, baselist):
        """Instantiate a BaseFunction (or any subclass) from a string.

        References to other BaseFunction instances in functionstr use the corresponding
        index of that instance in baselist.

        Parameters
        ----------
        functionstr : str
            The string representation of the BaseFunction instance
        baselist : array-like
            The list of BaseFunction (or subclass) instances.

        Returns
        Basefunction instance
            The BaseFunction instance based on the parameter strings
        """
        data = functionstr.splitlines()
        data = "\n".join(data)

        # populate dictionary with parameter definition
        # "key=value"->{"key":"value"}
        data = re.split(r"(?:[\r\n]+|\A)(\S+)=", data)
        ddict = {}
        for i in range(len(data) // 2):
            ddict[data[2 * i + 1]] = data[2 * i + 2]

        # dictionary of parameters
        pdict = {}
        for k, v in ddict.items():
            try:
                pdict[k] = eval(v)
            except Exception as e:
                logger.exception(e)
                emsg = "Invalid parameter: %s=%s" % (k, v)
                raise SrMiseDataFormatError(emsg)

        function_name = pdict["function"]
        del pdict["function"]

        module_name = pdict["module"]
        del pdict["module"]

        #  __import()__ returns the top-level module (so spam in spam.foo.whatever)
        # so I need to perform a secondary look-up
        __import__(module_name)
        module = sys.modules[module_name]
        functionclass = getattr(module, function_name)

        # Correctly initialize the base function, if one exists.
        if pdict["base"] is not None:
            idx = pdict["base"]
            if idx > len(baselist):
                emsg = "Dependent base function not in baselist."
                raise ValueError(emsg)
            pdict["base"] = baselist[idx]
        else:
            del pdict["base"]

        return functionclass(**pdict)

    @staticmethod
    def safefunctionlist(fs):
        """Return list of BaseFunction instances where any dependencies occur earlier in list.

        Any functions with hidden dependent functions (i.e. those not in fs)
        are included in the returned list.  This list provides an order that
        is guaranteed to be safe for saving/reinstantiating peak functions.

        Parameters
        fs: List of BaseFunction instances."""
        fsafe = []
        for f in fs:
            BaseFunction.safefunction(f, fsafe)
        return fsafe

    @staticmethod
    def safefunction(f, fsafe):
        """Append BaseFunction instance f to fsafe, but adding dependent functions first.

        Does not handle circular dependencies.

        Parameters
        ----------
        f : BaseFunction instance
            The BaseFunction instance
        fsafe : array-like
            The list of BaseFunction instances being built.

        Returns
        -------
        None
        """
        if f not in fsafe:
            if f.base is not None:
                BaseFunction.safefunction(f.base, fsafe)
            fsafe.append(f)

        return


# end of class BaseFunction

if __name__ == "__main__":

    from diffpy.srmise.peaks.gaussianoverr import GaussianOverR
    from diffpy.srmise.peaks.terminationripples import TerminationRipples

    p = GaussianOverR(0.8)
    outstr = p.writestr([])

    p2 = BaseFunction.factory(outstr, [])

    pt = TerminationRipples(p, 20)
    outstr2 = pt.writestr([p])
    print(outstr)

    pt2 = BaseFunction.factory(outstr2, [p])
    print(type(pt2))
