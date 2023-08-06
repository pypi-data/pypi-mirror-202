from typing import Dict, Union, List, Optional, Tuple

import numpy as np

from quickstats import semistaticmethod, AbstractObject
from quickstats.interface.cppyy.vectorize import as_np_array
from quickstats.maths.statistics import (dataset_is_binned, fill_missing_bins,
                                         rebin_dataset, bin_edge_to_bin_center)

class RooDataSet(AbstractObject):
    
    def __init__(self, dataset:"ROOT.RooDataSet",
                 verbosity:Optional[Union[int, str]]=None):
        super().__init__(verbosity=verbosity)
        self.parse(dataset)
        self.ghost_threshold = 1e-8
        self.bin_precision = 8
        self.error_option = 'poisson'
        
    def parse(self, dataset:"ROOT.RooDataSet"):
        category = self.get_dataset_category(dataset)
        if not category:
            raise RuntimeError('no category defined in the dataset')
        self.set_category_variable(category)
        observables = self.get_dataset_observables(dataset)
        self.set_observable_variables(observables)
        self.data = self.to_numpy(dataset, copy=True, rename_columns=False,
                                  category_label=False)
        self.name = dataset.GetName()
        self.title = dataset.GetTitle()
        self.set_weight_variable(dataset.weightVar())
        
        obs_cat_pairing = self.pair_category_and_observable(dataset)
        category_map = {}
        for pairing in obs_cat_pairing:
            category_map[pairing['category_label']] = {
                'observable': pairing['observable'],
                'category_index': pairing['category_index']
            }
        self.category_map = category_map
            
    @semistaticmethod
    def to_numpy(self, dataset:"ROOT.RooDataSet", copy:bool=True,
                 rename_columns:bool=True, category_label:bool=True,
                 split_category:bool=False):
        # use ROOT's built-in method if available
        if hasattr(dataset, "to_numpy"):
            data = dataset.to_numpy(copy=copy)
        # just copy the implementation from ROOT
        else:
            import ROOT

            data = {}

            if isinstance(dataset.store(), ROOT.RooVectorDataStore):
                for name, array in dataset.store().to_numpy(copy=copy).items():
                    data[name] = array
            elif isinstance(dataset.store(), ROOT.RooTreeDataStore):
                # first create a VectorDataStore so we can read arrays
                store = dataset.store()
                variables = dataset.get()
                store_name = dataset.GetName()
                tmp_store = ROOT.RooVectorDataStore(store, variables, store_name)
                for name, array in tmp_store.to_numpy(copy=copy).items():
                    data[name] = array
            else:
                raise RuntimeError(
                    "Exporting RooDataSet to numpy arrays failed. The data store type "
                    + dataset.store().__class__.__name__
                    + " is not supported."
                )
                
        category = self.get_dataset_category(dataset)
        if category is not None:
            category_col = category.GetName()
        else:
            category_col = None
            
        weight_var = dataset.weightVar()
        if weight_var:
            weight_col = weight_var.GetName()
        else:
            weight_col = None

        if category_label and (category is not None):
            index_values = data[category_col]
            category_map = {d.second:d.first for d in category}
            label_values = np.vectorize(category_map.get)(index_values)
        else:
            label_values = None
            
        if rename_columns:
            if weight_col is not None:
                data['weight'] = data.pop(weight_col)
                weight_col = 'weight'
            if category_col is not None:
                data['category_index'] = data.pop(category_col)
                category_col = 'category_index'
                
        if label_values is not None:
            data['category_label'] = label_values
            
        if split_category and (category is not None):
            cat_obs_info_list = self.pair_category_and_observable(dataset)
            cat_data = {}
            for cat_obs_info in cat_obs_info_list:
                cat_label = cat_obs_info['category_label']
                cat_index = cat_obs_info['category_index']
                observable = cat_obs_info['observable']
                mask = data[category_col] == cat_index
                cat_data[cat_label] = {
                    observable: data[observable][mask],
                    weight_col: data[weight_col][mask]
                }
            return cat_data
            
        return data
    
    @staticmethod
    def from_numpy(data:Dict[str, "numpy.ndarray"],
                   variables:"ROOT.RooArgSet",
                   name:str=None, title:str=None,
                   weight_name:str=None, clip_to_limits=True):
        import ROOT
        if name is None:
            name = ""
        if title is None:
            title = ""
            
        if weight_name is None:
            dataset = ROOT.RooDataSet(name, title, variables)
        else:
            dataset = ROOT.RooDataSet(name, title, variables, weight_name)
            
        real_variables = {}
        cat_variables = {}
        for v in variables:
            var_name = v.GetName()
            class_name = v.ClassName()
            if var_name == weight_name:
                continue
            if var_name not in data:
                if (class_name == "RooCategory") and ("category_index" in data):
                    var_name = "category_index"
                else:
                    raise RuntimeError(f"missing data for the variable `{var_name}`")
            if class_name == "RooCategory":
                cat_variables[var_name] = v
            else:
                real_variables[var_name] = v
                if clip_to_limits:
                    data[var_name] = np.clip(data[var_name], 
                                             a_min=v.getMin(),
                                             a_max=v.getMax())
        if weight_name not in data:
            if "weight" in data:
                weight_name = "weight"
            else:
                raise RuntimeError(f"missing data for the variable `{weight_name}`")
                
        data_sizes = [len(data[k]) for k in data]
        if len(set(data_sizes)) > 1:
            raise RuntimeError("data has inconsistent sizes")
        if weight_name is None:
            for i in range(data_sizes[0]):
                for name, variable in real_variables.items():
                    variable.setVal(data[name][i])
                for name, variable in cat_variables.items():
                    variable.setIndex(data[name][i])
                dataset.add(variables, 1.)
        else:
            for i in range(data_sizes[0]):
                for name, variable in real_variables.items():
                    variable.setVal(data[name][i])
                for name, variable in cat_variables.items():
                    variable.setIndex(int(data[name][i]))
                weight = data[weight_name][i]
                dataset.add(variables, weight)
            
        return dataset
    
    @semistaticmethod
    def to_pandas(self, dataset:"ROOT.RooDataSet", copy:bool=True,
                  rename_columns:bool=True, category_label:bool=True,
                  split_category:bool=False):
        numpy_data = self.to_numpy(dataset, copy=copy,
                                   rename_columns=rename_columns,
                                   category_label=category_label,
                                   split_category=split_category)
        import pandas as pd
        if split_category:
            df_cat = {}
            for category, category_data in numpy_data.items():
                df_cat[category] = pd.DataFrame(category_data)
            return df_cat
        df = pd.DataFrame(numpy_data)
        return df
    
    to_dataframe = to_pandas
    
    @staticmethod
    def get_dataset_map(dataset_dict:Dict):
        import ROOT
        dsmap = ROOT.std.map('string, RooDataSet*')()
        dsmap.keepalive = list()
        for c, d in dataset_dict.items():
            dsmap.keepalive.append(d)
            dsmap.insert(dsmap.begin(), ROOT.std.pair("const string, RooDataSet*")(c, d))
        return dsmap
    
    @staticmethod
    def from_RooDataHist(source:"ROOT.RooDataHist", pdf:"ROOT.RooAbsPdf",
                         name:Optional[str]=None):
        import ROOT
        if name is None:
            name = source.GetName()
        parameters = source.get()
        category = None
        for parameter in parameters:
            if parameter.ClassName() == "RooCategory":
                category = parameter
                break
      # case multi-category data
        if category is not None:
            dataset_map = {}
            data_cat = source.split(category, True)
            n_cat = len(category)
            observables = ROOT.RooArgSet()
            for i in range(n_cat):
                category.setBin(i)
                cat_name = category.getLabel()
                pdf_i = pdf.getPdf(cat_name)
                data_i = data_cat.FindObject(cat_name)                
                obs_i = pdf_i.getObservables(data_i).first()
                _obs_i = data_i.get().find(obs_i.GetName())
                w_i = ROOT.RooRealVar(f"weight_{i}", f"weight_{i}", 1)
                dataset_i = ROOT.RooDataSet(f"dataset_{i}", f"dataset_{i}",
                                            ROOT.RooArgSet(obs_i, w_i),
                                            ROOT.RooFit.WeightVar(w_i))
                ROOT.RFUtils.CopyData(data_i, dataset_i, _obs_i, obs_i, w_i)
                dataset_map[cat_name] = dataset_i
                observables.add(obs_i)
            w = ROOT.RooRealVar("weight", "weight", 1)
            observables.add(w)
            cpp_dataset_map = RooDataSet.get_dataset_map(dataset_map)
            dataset = ROOT.RooDataSet(name, name, observables,
                                      ROOT.RooFit.Index(category),
                                      ROOT.RooFit.Import(cpp_dataset_map),
                                      ROOT.RooFit.WeightVar(w))
        # case single-category data
        else:
            obs = pdf.getObservables(source).first()
            _obs = source.get().find(obs.GetName())
            w = ROOT.RooRealVar("weight", "weight", 1)
            dataset = ROOT.RooDataSet(name, name, ROOT.RooArgSet(obs, w),
                                      ROOT.RooFit.WeightVar(w))
            ROOT.RFUtils.CopyData(source, dataset, _obs, obs, w)
        return dataset

    @staticmethod
    def _get_cat_and_obs(variables:"ROOT.RooArgSet"):
        cat_variable = None
        observables = {}
        for v in variables:
            class_name = v.ClassName()
            if class_name == "RooCategory":
                if cat_variable is not None:
                    raise RuntimeError("found multiple RooCategory instances")
                cat_variable = v
            else:
                var_name = v.GetName()
                observables[var_name] = v
        if cat_variable is None:
            raise RuntimeError("missing RooCategory instance from variables")
        return cat_variable, observables
    
    @staticmethod
    def get_dataset_observables(dataset:"ROOT.RooDataSet", fmt:str="argset"):
        """
        Extract the observables from the dataset.
        """
        import ROOT
        observables = ROOT.RFUtils.GetDatasetObservables(dataset)
        if fmt == "list":
            return [obs for obs in observables]
        elif fmt == "argset":
            return observables
        else:
            raise ValueError(f'unsupported output format: {fmt}')
    
    @staticmethod
    def get_dataset_category(dataset:"ROOT.RooDataSet"):
        """
        Extract the category variable from the dataset.
        """
        import ROOT
        category = ROOT.RFUtils.GetDatasetCategory(dataset)
        if not category:
            return None
        return category
    
    @semistaticmethod
    def pair_category_and_observable(self, dataset):
        category = self.get_dataset_category(dataset)
        if category is None:
            return None
        observables = self.get_dataset_observables(dataset)
        observables = [obs.GetName() for obs in observables]
        numpy_data = self.to_numpy(dataset, copy=False,
                                   rename_columns=True,
                                   category_label=False)
        result = []
        for cat_data in category:
            cat_label = cat_data.first
            cat_index = cat_data.second
            mask = numpy_data['category_index'] == cat_index
            obs_with_changing_values = []
            for observable in observables:
                obs_values = numpy_data[observable][mask]
                if len(np.unique(obs_values)) > 1:
                    obs_with_changing_values.append(observable)
            if len(obs_with_changing_values) != 1:
                raise RuntimeError(f'unable to deduce observable for the category: {cat_label}')
            paired_data = {
                'observable': obs_with_changing_values[0],
                'category_index': cat_index,
                'category_label': cat_label
            }
            result.append(paired_data)
        return result

    @semistaticmethod
    def create_binned_category_dataset(self, data:Dict[str, "numpy.ndarray"],
                                       pdf:"ROOT.RooAbsPdf",
                                       variables:"ROOT.RooArgSet",
                                       weight_name:str="weightVar",
                                       name:str=None, title:str=None):
        import ROOT
        if name is None:
            name = ""
        if title is None:
            title = ""        
        cat_variable, observables = self._get_cat_and_obs(variables)
        n_cat = cat_variable.size()
        cat_names = []
        cat_obs_names = []
        for i in range(n_cat):
            cat_variable.setIndex(i)
            cat_name = cat_variable.getLabel()
            cat_names.append(cat_name)
            pdf_cat = pdf.getPdf(cat_name)
            obs = pdf_cat.getObservables(variables)
            cat_obs = obs.first()
            cat_obs_names.append(cat_obs.GetName())
        if set(cat_obs_names) != set(observables):
            raise RuntimeError("the given variables are insistent with the category observables")
        if not set(cat_names).issubset(set(data)):
            missing = list(set(cat_names) - set(data))
            raise RuntimeError("missing data for the following categories: {}".format(",".join(missing)))
        dataset = ROOT.RooDataSet(name, title, variables, weight_name)
        for i, (cat_name, obs_name) in enumerate(zip(cat_names, cat_obs_names)):
            observable = observables[obs_name]
            data_i = data[cat_name]
            cat_variable.setIndex(i)
            n_bins = observable.getBins()
            n_bins_data = len(data_i)
            if n_bins_data != n_bins:
                raise RuntimeError(f"the observable has `{n_bins}` bins but data has `{n_bins_data}`")
            for j in range(n_bins_data):
                observable.setBin(j)
                dataset.add(variables, data_i[j])
        return dataset
    
    @semistaticmethod
    def to_category_data(self, dataset:"ROOT.RooDataSet",
                         pdf:"ROOT.RooAbsPdf"):
        cat_and_obs = self.get_category_and_observables(dataset)
        cat_variable = cat_and_obs['category']
        if cat_variable is None:
            raise RuntimeError('no category defined in the dataset')
        n_cat = cat_variable.size()
        data = self.to_numpy(dataset)
        result = {}
        for i in range(n_cat):
            cat_variable.setIndex(i)
            cat_name = cat_variable.getLabel()
            pdf_cat = pdf.getPdf(cat_name)
            obs = pdf_cat.getObservables(variables)
            cat_obs = obs.first()
            obs_name = cat_obs.GetName()
            mask = (data['index'] == i)
            bin_value = data[obs_name][mask]
            ind = np.argsort(bin_value)
            bin_weight = data['weight'][mask][ind]
            result[cat_name] = bin_weight
        return result
    
    @staticmethod
    def fill_from_TH1(dataset:"ROOT.RooDataSet", hist:"ROOT.TH1",
                      skip_out_of_range:bool=True,
                      blind_range:Optional[List[float]]=None,
                      min_bin_value:float=0,
                      weight_scale:float=1):
        import ROOT
        parameters = dataset.get()
        if parameters.size() > 1:
            raise RuntimeError("multiple observables are not allowed")
        x = parameters.first()
        weight_var = dataset.weightVar()
        # blinding will be taken care of
        xmin = x.getMin()
        xmax = x.getMax()
        n_bins = hist.GetNbinsX()
        for i in range(1, n_bins + 1):
            bin_center = hist.GetBinCenter(i)
            # skip bins that are out of range
            if skip_out_of_range and ((bin_center > xmax) or (bin_center < xmin)):
                continue
            # skip bins in the blind range
            if (blind_range and (bin_center > blind_range[0]) and (bin_center < blind_range[1])):
                continue
            x.setVal(bin_center)
            bin_content = hist.GetBinContent(i)
            weight = bin_content * weight_scale
            # if the weight is negligible, consider it as zero
            if (weight < min_bin_value):
                continue;
            if weight_var:
                weight_var.setVal(weight)
                dataset.add(ROOT.RooArgSet(x, weight_var), weight)
            else:
                dataset.add(ROOT.RooArgSet(x), weight)
    
    @staticmethod
    def get_x_and_weight(dataset:"ROOT.RooDataSet"):
        parameters = dataset.get()
        if parameters.size() > 1:
            raise RuntimeError("multiple observables are not allowed")
        x = parameters.first()
        weight_var = dataset.weightVar()
        return x, weight_var
    
    @staticmethod
    def to_TH1(dataset:"ROOT.RooDataSet", name:str,
               blind_range:Optional[List[float]]=None,
               weight_scale:float=1):
        x, weight_var = RooDataSet.get_x_and_weight(dataset)
        n_bins = x.getBins()
        x_min = x.getMin()
        x_max = x.getMax()
        import ROOT
        hist = ROOT.TH1D(name, name, n_bins, x_min, x_max)
        hist.Sumw2()
        for i in range(dataset.numEntries()):
            dataset.get(i)
            x_val = x.getVal()
            obs.setVal(x_val)
            weight = dataset.weight() * weight_scale
            # ignore data in the blind range
            if (blind_range and (x_val > blind_range[0]) and (x_val < blind_range[1])):
                continue
            hist.Fill(x_val, weight)
        return hist
    
    @staticmethod
    def add_ghost_weights(dataset:"ROOT.RooDataSet",
                          blind_range:Optional[List[float]]=None,
                          ghost_weight:float=1e-9):
        x, weight_var = RooDataSet.get_x_and_weight(dataset)
        xmin = x.getMin()
        xmax = x.getMax()
        n_bins = x.getBins()
        bin_width = (xmax - xmin) / n_bins
        data = RooDataSet.to_numpy(dataset)
        x_data = data[x.GetName()]
        weight_data = data["weight"]
        hist, bin_edges = np.histogram(x_data, bins=n_bins, range=(xmin, xmax), weights=weight_data)
        from quickstats.maths.statistics import bin_edge_to_bin_center
        bin_centers = bin_edge_to_bin_center(bin_edges)
        import ROOT
        for bin_val, bin_center in zip(hist, bin_centers):
            if (bin_val != 0):
                continue
            if (blind_range and (bin_center > blind_range[0]) and (bin_center < blind_range[1])):
                continue
            x.setVal(bin_center)
            weight_var.setVal(ghost_weight)
            dataset.add(ROOT.RooArgSet(x, weight_var), ghost_weight)
         
    @semistaticmethod
    def compare_category_data(self, ds1:"ROOT.RooDataSet", ds2:"ROOT.RooDataSet", rtol=1e-8):
        ds1_data = self.to_numpy(ds1, split_category=True)
        ds2_data = self.to_numpy(ds1, split_category=True)
        ds1_has_cat = self.get_dataset_category(ds1) is not None
        ds2_has_cat = self.get_dataset_category(ds2) is not None
        if (not ds1_has_cat) or  (not ds2_has_cat):
            raise RuntimeError('all input datasets must have category index')
        df1_cats = list(ds1_data.keys())
        df2_cats = list(ds2_data.keys())
        common_cats = list(set(df1_cats).intersection(df2_cats))
        unique_cats_left = list(set(df1_cats) - set(common_cats))
        unique_cats_right = list(set(df2_cats) - set(common_cats))
        def get_sorted_obs_and_weight(data):
            columns = list(data.keys())
            try:
                obs_col = [i for i in columns if i != 'weight'][0]
            except:
                raise RuntimeError('unable to deduce observable column from data')
            obs_values = data[obs_col]
            weight_values = data['weight']
            indices = np.argsort(obs_values)
            return obs_values[indices], weight_values[indices]
        result = {
            'identical': [],
            'modified': [],
            'unique_left': unique_cats_left,
            'unique_right': unique_cats_right
        }
        for category in common_cats:
            obs_values_1, weight_values_1 = get_sorted_obs_and_weight(ds1_data[category])
            obs_values_2, weight_values_2 = get_sorted_obs_and_weight(ds2_data[category])
            if (np.allclose(obs_values_1, obs_values_2, rtol=rtol) and 
                np.allclose(weight_values_1, weight_values_2, rtol=rtol)):
                result['identical'].append(category)
            else:
                result['modified'].append(category)
        return result
    
    @semistaticmethod
    def dataset_equal(self, ds1:"ROOT.RooDataSet", ds2:"ROOT.RooDataSet", rtol=1e-8):
        result = self.compare_category_data(ds1, ds2)
        return (len(result['modified']) == 0) and (len(result['unique_left']) == 0) and (len(result['unique_right']) == 0)
    
    
    def set_observable_variables(self, observables):
        _observables = []
        from .RooRealVar import RooRealVar
        for observable in observables:
            _observables.append(RooRealVar(observable))
        self.observables = _observables
        
    def set_category_variable(self, category):
        from .RooCategory import RooCategory
        self.category = RooCategory(category)
        
    def set_weight_variable(self, weight):
        if weight:
            from .RooRealVar import RooRealVar
            self.weight = RooRealVar(weight)
        else:
            self.weight = None
    
    def clip_to_range(self, ranges:Optional[Union[Tuple[float], Dict[str, Tuple[float]]]]=None,
                      inplace:bool=True):
        index_map = {}
        
        for category in self.category_map:
            category_index = self.category_map[category]['category_index']
            observable = self.category_map[category]['observable']
            if observable not in index_map:
                index_map[observable] = []
            index_map[observable].append(category_index)
            
        if ranges is None:
            ranges = {observable.name: observable.range for observable in self.observables}
        elif not isinstance(ranges, dict):
            ranges = {observable.name: ranges for observable in self.observables}
        
        range_mask = np.ones_like(list(self.data.values())[0], dtype=bool)

        def in_range(arr, variable):
            return (arr >= ranges[variable][0]) & (arr <= ranges[variable][1])
        
        def in_cat(arr, variable):
            return np.isin(arr, index_map[variable])
        
        cat_name = self.category.name
        range_mask = np.logical_and.reduce([(in_range(self.data[obs], obs) | \
                                            ~in_cat(self.data[cat_name], obs)) \
                                            for obs in ranges])
        
        if range_mask.all():
            if inplace:
                return None
            else:
                return self.data.copy()
        result = {column: self.data[column][range_mask] for column in self.data}
        if inplace:
            self.data = result
            return None
        else:
            return result
    
    def scale_category_weights(self, scale_factors:Union[float, Dict[str, float]]):
        if not isinstance(scale_factors, dict):
            scale_factors = {category: scale_factors for category in self.category_map}
        category_name = self.category.name
        weight_name = self.weight.name
        for category, scale_factor in scale_factors.items():
            if category not in self.category_map:
                raise ValueError(f'dataset has no category "{category}"')
            category_index = self.category_map[category]['category_index']
            mask = self.data[category_name] == category_index
            self.data[weight_name][mask] *= scale_factor
    
    def get_category_data(self, category:str):
        category_name = self.category.name
        weight_name = self.weight.name
        category_index = self.category_map[category]['category_index']
        observable_name = self.category_map[category]['observable']
        mask = self.data[category_name] == category_index
        category_data = {
            observable_name: self.data[observable_name][mask],
            weight_name: self.data[weight_name][mask]
        }
        return category_data
    
    def get_category_distribution(self, category:str, nbins:Optional[int]=None,
                                  bin_range:Optional[Tuple[float]]=None,
                                  weight_scale:Optional[float]=None,
                                  include_error:bool=True):
        data = self.get_category_data(category)
        observable_name = self.category_map[category]['observable']
        weight_name = self.weight.name
        x, y = data[observable_name], data[weight_name]
        idx = np.argsort(x)
        x, y = x[idx], y[idx]
        observable = [v for v in self.observables if v.name == observable_name]
        assert len(observable) == 1
        observable = observable[0]
        default_nbins = observable.n_bins
        if nbins is None:
            nbins = default_nbins
        if bin_range is None:
            bin_range = observable.range
        else:
            #remove bins outside custom range
            range_mask = (x >= bin_range[0]) & (x <= bin_range[1])
            x, y = x[range_mask], y[range_mask]
        binned_dataset = dataset_is_binned(x, y, xlow=bin_range[0],
                                           xhigh=bin_range[1],
                                           nbins=default_nbins,
                                           ghost_threshold=self.ghost_threshold,
                                           bin_precision=self.bin_precision)
        # binned dataset with blinded range
        if binned_dataset and (len(x) != default_nbins):
            x, y = fill_missing_bins(x, y, xlow=bin_range[0],
                                     xhigh=bin_range[1],
                                     nbins=default_nbins,
                                     bin_precision=self.bin_precision)
        # rebin binned dataset
        if binned_dataset and (nbins != default_nbins):
            x, y = rebin_dataset(x, y, nbins)
            self.stdout.warning(f"WARNING: Rebinned dataset ({self.name}, category = {category}) "
                                f"from nbins = {default_nbins} to nbins = {nbins}")
        if not binned_dataset:
            non_ghost_mask = (y > self.ghost_threshold)
            if non_ghost_mask.all():
                x_non_ghost = x
                y_non_ghost = y
            else:
                x_non_ghost = x[non_ghost_mask]
                y_non_ghost = y[non_ghost_mask]
            hist, bin_edges = np.histogram(x_non_ghost, bins=nbins,
                                           range=(bin_range[0], bin_range[1]),
                                           density=False, weights=y_non_ghost)
            bin_centers = bin_edge_to_bin_center(bin_edges)
            x = bin_centers
            y = hist

        if include_error:
            yerrlo, yerrhi = self.get_weight_error(y)
        else:
            yerrlo, yerrhi = None, None
            
        if weight_scale is not None:
            y *= weight_scale
            if (yerrlo is not None) and (yerrhi is not None):
                yerrlo *= weight_scale
                yerrhi *= weight_scale
        result = {
            "x": x,
            "y": y
        }
        if (yerrlo is not None) and (yerrhi is not None):
            result["yerrlo"] = yerrlo
            result["yerrhi"] = yerrhi
        return result
    
    def create_binned_dataset(self, binnings:Optional[Union[Dict[str, int], int]]=None) -> "RooDataSet":
        pass
    
    def get_merged_distribution(self, categories:Optional[List[str]]=None,
                                nbins:Optional[int]=None,
                                bin_range:Optional[Tuple[float]]=None,
                                include_error:bool=True,
                                weight_scales:Optional[Union[float, Dict[str, float]]]=None):
        if categories is None:
            categories = list(self.category_map)
        if weight_scales is None:
            weight_scales = {}
        if not isinstance(weight_scales, dict):
            weight_scales = {category: weight_scales for category in categories}
        x, y, yerrlo, yerrhi = None, None, None, None
        for category in categories:
            weight_scale = weight_scales.get(category, None)
            distribution = self.get_category_distribution(category=category,
                                                          nbins=nbins,
                                                          bin_range=bin_range,
                                                          weight_scale=weight_scale,
                                                          include_error=include_error)
            if x is None:
                x = distribution['x']
                y = distribution['y']
            elif not np.array_equal(x, distribution['x']):
                raise RuntimeError('can not merge categories with different binnings')
            else:
                y += distribution['y']
            if ('yerrlo' in distribution) and ('yerrhi' in distribution):
                if (yerrlo is None) and (yerrhi is None):
                    yerrlo = distribution['yerrlo'] ** 2
                    yerrhi = distribution['yerrhi'] ** 2
                else:
                    yerrlo += distribution['yerrlo'] ** 2
                    yerrhi += distribution['yerrhi'] ** 2
        result = {
            'x': x,
            'y': y
        }
        if (yerrlo is not None) and (yerrhi is not None):
            result["yerrlo"] = np.sqrt(yerrlo)
            result["yerrhi"] = np.sqrt(yerrhi)
        return result
    
    def get_weight_error(self, weight:np.ndarray):
        if self.error_option == "poisson":
            from quickstats.interface.root import TH1
            weight_error = TH1.GetPoissonError(weight)
            return weight_error['lo'], weight_error['hi']
        elif self.error_option == "sumw2":
            weight_error = np.sqrt(y)
            return weight_error, weight_error
        else:
            raise RuntimeError(f'unknown error option: {self.error_option}')
    
    def new(self) -> "ROOT.RooDataSet":
        import ROOT
        variables = ROOT.RooArgSet()
        for observable in self.observables:
            variables.add(observable.new())
        variables.add(self.category.new())
        if self.weight is not None:
            weight_var = self.weight.new()
            variables.add(weight_var)
            weight_name = weight_var.GetName()
        else:
            weight_name = None
        dataset = ROOT.RooDataSet.from_numpy(self.data, variables,
                                             name=self.name,
                                             title=self.title,
                                             weight_name=weight_name)
        return dataset
    