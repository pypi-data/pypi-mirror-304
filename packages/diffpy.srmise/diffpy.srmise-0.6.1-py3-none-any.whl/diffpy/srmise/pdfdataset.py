#!/usr/bin/env python
##############################################################################
#
# SrMise            by Luke Granlund
#                   (c) 2015 trustees of the Michigan State University.
#                   All rights reserved.
#
# File coded by:    Luke Granlund
#
# See LICENSE.txt for license information.
#
# This file uses source code from the PDFgui files pdfdataset.py and
# pdfcomponent.py, (c) 2006 trustees of the Michigan State University.  See
# LICENSE_PDFgui.txt for the full PDFgui license.
#
##############################################################################


"""class PDFDataSet for experimental PDF data.
"""


import os.path
import re
import time
from getpass import getuser

from diffpy.srmise.srmiseerrors import SrMiseFileError, SrMisePDFKeyError


class PDFComponent(object):
    """Common base class."""

    def __init__(self, name):
        """initialize the object

        Parameter
        ---------
        name : str
            object name
        """
        self.name = name

    def close(self, force=False):
        """close myself

        Parameter
        ---------
        force : bool
            Force to close if True, default is False.
        """
        pass


class PDFDataSet(PDFComponent):
    """PDFDataSet is a class for experimental PDF data.

    Attributes
    ----------
    robs : list
        The list of observed r points.
    Gobs : list
        The list of observed G values.
    drobs : list
        The list of standard deviations of `robs`.
    dGobs : list
        The list of standard deviations of `Gobs`.
    stype : str
        The scattering type, either 'X' or 'N'.
    qmax : float
        The maximum value of Q in inverse Angstroms. Termination ripples are neglected for qmax=0.
    qdamp : float
        Specifies width of Gaussian damping factor in pdf_obs due to imperfect Q resolution.
    qbroad : float
        The quadratic peak broadening factor related to the dataset.
    spdiameter : float
        The particle diameter for shape damping function. Note: This attribute was moved to PDFStructure.
        It is retained here for backward compatibility when reading PDFgui project files.
    dscale : float
        The scale factor of this dataset.
    rmin : float
        The same as `robs[0]`.
    rmax : float
        The same as `robs[-1]`.
    filename : str
        Set to the absolute path after reading from a file.
    metadata : dict
        The dictionary for other experimental conditions, such as temperature or doping.

    Class Members
    -------------
    persistentItems : list
        The list of attributes saved in the project file.
    refinableVars : set
        The set (or dict-like) of refinable variable names.
    """

    persistentItems = [
        "robs",
        "Gobs",
        "drobs",
        "dGobs",
        "stype",
        "qmax",
        "qdamp",
        "qbroad",
        "dscale",
        "rmin",
        "rmax",
        "metadata",
    ]
    refinableVars = dict.fromkeys(("qdamp", "qbroad", "dscale"))

    def __init__(self, name):
        """Initialize.

        name : str
            The name of the data set. It must be a unique identifier.
        """
        PDFComponent.__init__(self, name)
        self.clear()
        return

    def clear(self):
        """reset all data members to initial empty values

        The purpose of this method is to set the PDF dataset to initial empty values."""
        self.robs = []
        self.Gobs = []
        self.drobs = []
        self.dGobs = []
        self.stype = "X"
        # user must specify qmax to get termination ripples
        self.qmax = 0.0
        self.qdamp = 0.001
        self.qbroad = 0.0
        self.spdiameter = None
        self.dscale = 1.0
        self.rmin = None
        self.rmax = None
        self.filename = None
        self.metadata = {}
        return

    def setvar(self, var, value):
        """Assign a data member using PdfFit-style variable notation.
        This method is typically utilized by the `applyParameters()` function.

        Parameters
        ----------
        var : str
            String representation of the dataset PdfFit variable.
            Possible values include: 'qdamp', 'qbroad', 'dscale'.

        value : float
            The new value to which the variable `var` will be set.

        Returns
        -------
        None
        """
        barevar = var.strip()
        fvalue = float(value)
        if barevar in PDFDataSet.refinableVars:
            setattr(self, barevar, fvalue)
        else:
            emsg = "Invalid PdfFit dataset variable %r" % barevar
            raise SrMisePDFKeyError(emsg)
        return

    def getvar(self, var):
        """Obtain value corresponding to PdfFit dataset variable.
        Used by findParameters().

        Parameters
        ----------
        var : str
            string representation of dataset PdfFit variable.
            Possible values: qdamp, qbroad, dscale

        Returns
        -------
        float
            value of var
        """
        barevar = var.strip()
        if barevar in PDFDataSet.refinableVars:
            value = getattr(self, barevar)
        else:
            emsg = "Invalid PdfFit dataset variable %r" % barevar
            raise SrMisePDFKeyError(emsg)
        return value

    def read(self, filename):
        """load data from PDFGetX2 or PDFGetN gr file

        filename : str
            file to read from

        Returns
        -------
        self
        """
        try:
            # Open the file in binary mode, read it, and decode to convert bytes to string
            with open(filename, "rb") as file:
                file_content = file.read().decode("utf-8")
            self.readStr(file_content)
        except PDFDataFormatError as err:
            basename = os.path.basename(filename)
            emsg = ("Could not open '%s' due to unsupported file format " + "or corrupted data. [%s]") % (
                basename,
                err,
            )
            raise SrMiseFileError(emsg)
        self.filename = os.path.abspath(filename)
        return self

    def readStr(self, datastring):
        """read experimental PDF data from a string

        Parameter
        ---------
        datastring : str
            string of raw data

        Returns
        self
        """
        self.clear()
        # useful regex patterns:
        rx = {"f": r"[-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?"}
        # find where does the data start
        res = re.search(r"^#+ start data\s*(?:#.*\s+)*", datastring, re.M)
        # start_data is position where the first data line starts
        if res:
            start_data = res.end()
        else:
            # find line that starts with a floating point number
            regexp = r"^\s*%(f)s" % rx
            res = re.search(regexp, datastring, re.M)
            if res:
                start_data = res.start()
            else:
                start_data = 0
        header = datastring[:start_data]
        databody = datastring[start_data:].strip()

        # find where the metadata starts
        metadata = ""
        res = re.search(r"^#+ +metadata\b\n", header, re.M)
        if res:
            metadata = header[res.end() :]
            header = header[: res.start()]

        # parse header
        # stype
        if re.search("(x-?ray|PDFgetX)", header, re.I):
            self.stype = "X"
        elif re.search("(neutron|PDFgetN)", header, re.I):
            self.stype = "N"
        # qmax
        regexp = r"\bqmax *= *(%(f)s)\b" % rx
        res = re.search(regexp, header, re.I)
        if res:
            self.qmax = float(res.groups()[0])
        # qdamp
        regexp = r"\b(?:qdamp|qsig) *= *(%(f)s)\b" % rx
        res = re.search(regexp, header, re.I)
        if res:
            self.qdamp = float(res.groups()[0])
        # qbroad
        regexp = r"\b(?:qbroad|qalp) *= *(%(f)s)\b" % rx
        res = re.search(regexp, header, re.I)
        if res:
            self.qbroad = float(res.groups()[0])
        # spdiameter
        regexp = r"\bspdiameter *= *(%(f)s)\b" % rx
        res = re.search(regexp, header, re.I)
        if res:
            self.spdiameter = float(res.groups()[0])
        # dscale
        regexp = r"\bdscale *= *(%(f)s)\b" % rx
        res = re.search(regexp, header, re.I)
        if res:
            self.dscale = float(res.groups()[0])
        # temperature
        regexp = r"\b(?:temp|temperature|T)\ *=\ *(%(f)s)\b" % rx
        res = re.search(regexp, header)
        if res:
            self.metadata["temperature"] = float(res.groups()[0])
        # doping
        regexp = r"\b(?:x|doping)\ *=\ *(%(f)s)\b" % rx
        res = re.search(regexp, header)
        if res:
            self.metadata["doping"] = float(res.groups()[0])

        # parsing gerneral metadata
        if metadata:
            regexp = r"\b(\w+)\ *=\ *(%(f)s)\b" % rx
            while True:
                res = re.search(regexp, metadata, re.M)
                if res:
                    self.metadata[res.groups()[0]] = float(res.groups()[1])
                    metadata = metadata[res.end() :]
                else:
                    break

        # read actual data - robs, Gobs, drobs, dGobs
        inf_or_nan = re.compile("(?i)^[+-]?(NaN|Inf)\\b")
        has_drobs = True
        has_dGobs = True
        # raise PDFDataFormatError if something goes wrong
        try:
            for line in databody.split("\n"):
                v = line.split()
                # there should be at least 2 value in the line
                self.robs.append(float(v[0]))
                self.Gobs.append(float(v[1]))
                # drobs is valid if all values are defined and positive
                has_drobs = has_drobs and len(v) > 2 and not inf_or_nan.match(v[2])
                if has_drobs:
                    v2 = float(v[2])
                    has_drobs = v2 > 0.0
                    self.drobs.append(v2)
                # dGobs is valid if all values are defined and positive
                has_dGobs = has_dGobs and len(v) > 3 and not inf_or_nan.match(v[3])
                if has_dGobs:
                    v3 = float(v[3])
                    has_dGobs = v3 > 0.0
                    self.dGobs.append(v3)
            if not has_drobs:
                self.drobs = len(self.robs) * [0.0]
            if not has_dGobs:
                self.dGobs = len(self.robs) * [0.0]
        except (ValueError, IndexError) as err:
            raise PDFDataFormatError(err)
        self.rmin = self.robs[0]
        self.rmax = self.robs[-1]
        if not has_drobs:
            self.drobs = len(self.robs) * [0.0]
        if not has_dGobs:
            self.dGobs = len(self.robs) * [0.0]
        return self

    def write(self, filename):
        """Write experimental PDF data to a file.

        Parameters
        ----------
        filename : str
            name of file to write to

        Returns
        -------
        None
        """
        bytes = self.writeStr()
        f = open(filename, "w")
        f.write(bytes)
        f.close()
        return

    def writeStr(self):
        """String representation of experimental PDF data.


        Returns
        -------
        str
            The PDF data string.
        """
        lines = []
        # write metadata
        lines.extend(
            [
                "History written: " + time.ctime(),
                "produced by " + getuser(),
                "##### PDFgui",
            ]
        )
        # stype
        if self.stype == "X":
            lines.append("stype=X  x-ray scattering")
        elif self.stype == "N":
            lines.append("stype=N  neutron scattering")
        # qmax
        if self.qmax == 0:
            qmax_line = "qmax=0   correction not applied"
        else:
            qmax_line = "qmax=%.2f" % self.qmax
        lines.append(qmax_line)
        # qdamp
        lines.append("qdamp=%g" % self.qdamp)
        # qbroad
        lines.append("qbroad=%g" % self.qbroad)
        # dscale
        lines.append("dscale=%g" % self.dscale)
        # metadata
        if len(self.metadata) > 0:
            lines.append("# metadata")
            for k, v in self.metadata.items():
                lines.append("%s=%s" % (k, v))
        # write data:
        lines.append("##### start data")
        lines.append("#L r(A) G(r) d_r d_Gr")
        for i in range(len(self.robs)):
            lines.append("%g %g %g %g" % (self.robs[i], self.Gobs[i], self.drobs[i], self.dGobs[i]))
        # that should be it
        datastring = "\n".join(lines) + "\n"
        return datastring

    def copy(self, other=None):
        """copy self to other. if other is None, create new instance

        Parameters
        ----------
        other : PDFDataSet instance
            ref to other object

        Returns
        -------
        PDFDataSet instance
            reference to copied object
        """
        if other is None:
            other = PDFDataSet(self.name)
        elif isinstance(other, PDFDataSet):
            other.clear()
        # some attributes can be assigned, e.g., robs, Gobs, drobs, dGobs are
        # constant so they can be shared between copies.
        assign_attributes = (
            "robs",
            "Gobs",
            "drobs",
            "dGobs",
            "stype",
            "qmax",
            "qdamp",
            "qbroad",
            "dscale",
            "rmin",
            "rmax",
            "filename",
        )
        # for others we will assign a copy
        copy_attributes = ("metadata",)
        for a in assign_attributes:
            setattr(other, a, getattr(self, a))
        import copy

        for a in copy_attributes:
            setattr(other, a, copy.deepcopy(getattr(self, a)))
        return other


# End of class PDFDataSet


class PDFDataFormatError(Exception):
    """Exception class marking failure to proccess PDF data string."""

    pass


# simple test code
if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    dataset = PDFDataSet("test")
    dataset.read(filename)
    print("== metadata ==")
    for k, v in dataset.metadata.items():
        print(k, "=", v)
    print("== data members ==")
    for k, v in dataset.__dict__.items():
        if k in ("metadata", "robs", "Gobs", "drobs", "dGobs") or k[0] == "_":
            continue
        print(k, "=", v)
    print("== robs Gobs drobs dGobs ==")
    for i in range(len(dataset.robs)):
        print(dataset.robs[i], dataset.Gobs[i], dataset.drobs[i], dataset.dGobs[i])
    print("== writeStr() ==")
    print(dataset.writeStr())
    print("== datasetcopy.writeStr() ==")
    datasetcopy = dataset.copy()
    print(datasetcopy.writeStr())

# End of file
