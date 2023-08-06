from typing import Dict, Union, List, Optional, Tuple

import numpy as np

from quickstats import semistaticmethod
from quickstats.interface.cppyy.vectorize import as_np_array, as_vector, np_type_str_maps
from .TH1 import TH1
from .TArrayData import TArrayData

class RooAbsPdf:
    
    @staticmethod
    def extract_sum_pdfs_by_category(pdf:"ROOT.RooAbsPdf", poi:Optional["ROOT.RooRealVar"]=None):
        pdf_class = pdf.ClassName()
        if pdf_class != "RooSimultaneous":
            raise RuntimeError(f"input pdf must be a RooSimultaneous instance (`{pdf_class}` received)")
        cat = pdf.indexCat()
        n_cat = cat.size()
        result = {}
        for i in range(n_cat):
            cat.setBin(i)
            cat_name = cat.getLabel()
            cat_pdf = pdf.getPdf(cat_name)
            cat_pdf_class = cat_pdf.ClassName()
            if cat_pdf_class != "RooProdPdf":
                raise RuntimeError(f"category pdf must be a RooProdPdf instance (`{cat_pdf_class}` received)")
            target_pdf = [i for i in cat_pdf.pdfList() if i.ClassName() == "RooRealSumPdf" and i != cat_pdf]
            if not target_pdf:
                raise RuntimeError(f"category pdf does not contain a RooRealSumPdf component")
            if len(target_pdf) > 1:
                raise RuntimeError(f"expect only one RooRealSumPdf component from category pdf but {len(target_pdf)} found")
            target_pdf = target_pdf[0]
            if poi is None:
                result[cat_name] = [i for i in pdf.getComponents()]
            else:
                result[cat_name] = [i for i in pdf.getComponents() if i.dependsOn(poi)]
        return result
    
    @semistaticmethod
    def get_values(self, pdf:"RooAbsPdf",
                   observables:"ROOT.RooArgSet",
                   bin_centers:np.ndarray):
        import ROOT
        vec_bin_centers = as_vector(bin_centers)
        type_str = np_type_str_maps.get(bin_centers.dtype, None)
        if type_str is None:
            bin_centers = bin_centers.astype(float)
            type_str = 'double'
        vec_values = ROOT.RFUtils.GetPdfValues[type_str](pdf, observables, vec_bin_centers)
        values = TArrayData.vec_to_array(vec_values)
        return values
    
    @semistaticmethod
    def get_distribution(self, pdf:"RooAbsPdf",
                         observables:"ROOT.RooArgSet", 
                         nbins:Optional[int]=None,
                         bin_range:Optional[Tuple[float]]=None,
                         weight_scale:Optional[float]=None):
        # the observables are needed for normalization
        pdf_obs = pdf.getObservables(observables)
        target_obs = pdf_obs.first()
        if nbins is None:
            nbins = target_obs.numBins()
        if bin_range is None:
            obs_name = target_obs.GetName()
            histogram = pdf.createHistogram(obs_name, nbins)
            py_histogram = TH1(histogram)
            binning_class = target_obs.getBinning().ClassName()
            if binning_class == "RooUniformBinning":
                bin_widths = py_histogram.bin_width
            else:
                bin_widths = RooRealVar.get_bin_widths(target_obs)
            x = py_histogram.bin_center
            y = py_histogram.bin_content * bin_widths
            # free memory to avoid memory leak
            histogram.Delete()
        else:
            assert len(bin_range) == 2
            from quickstats.maths.statistics import get_bin_centers_from_range
            x = get_bin_centers_from_range(bin_range[0], bin_range[1], nbins)
            y = self.get_values(pdf, observables, x)
            normalization = pdf.expectedEvents(pdf_obs)
            bin_width = round((bin_range[1] -  bin_range[0]) / nbins, 8)
            y = y * normalization * bin_width
        if weight_scale is not None:
            y *= weight_scale
        result = {
            'x': x,
            'y': y
        }
        return result