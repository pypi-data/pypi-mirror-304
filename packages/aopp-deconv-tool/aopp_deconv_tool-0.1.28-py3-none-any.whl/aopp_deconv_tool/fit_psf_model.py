"""
Tool for fitting a PSF to a particular model
"""

import sys
from pathlib import Path
import datetime as dt
from functools import partial


import numpy as np
import scipy as sp
from astropy.io import fits

import aopp_deconv_tool.numpy_helper as nph

import aopp_deconv_tool.astropy_helper as aph
import aopp_deconv_tool.astropy_helper.fits.specifier
import aopp_deconv_tool.astropy_helper.fits.header
from aopp_deconv_tool.fpath import FPath
import aopp_deconv_tool.plot_helper as plot_helper
import aopp_deconv_tool.arguments


from aopp_deconv_tool.optimise_compat import PriorParam, PriorParamSet
from aopp_deconv_tool.optimise_compat.ultranest_compat import UltranestResultSet, fitting_function_factory


from aopp_deconv_tool.psf_model.dependency_injector import (
	RadialPSFModelDependencyInjector, 
	GaussianPSFModelDependencyInjector,
	TurbulencePSFModelDependencyInjector,
	MUSEAdaptiveOpticsPSFModelDependencyInjector,	
)

import aopp_deconv_tool.psf_data_ops as psf_data_ops

import aopp_deconv_tool.cfg.logs
_lgr = aopp_deconv_tool.cfg.logs.get_logger_at_level(__name__, 'WARN')


# Library of PSF model dependency injector classes.
# See the psf_model.dependency_injector.params_and_psf_model_di.py file for the
# base class of all dependency injectors.
psf_models = {
	'radial' : RadialPSFModelDependencyInjector,
	'gaussian' : GaussianPSFModelDependencyInjector,
	'tubulence' : TurbulencePSFModelDependencyInjector,
	'muse_ao' : MUSEAdaptiveOpticsPSFModelDependencyInjector,
}

FITTING_METHODS=('ultranest', 'scipy.minimize')

PSF_MODEL_DI_CLASS = None
PSF_MODEL_DI = None

def set_psf_model_dependency_injector(name, fits_spec):
	"""
	Module-wide method. Sets the dependency injector class and initialises the dependency injector instance.
	"""
	global PSF_MODEL_DI_CLASS
	global PSF_MODEL_DI
	PSF_MODEL_DI_CLASS = psf_models[name]
	_lgr.debug(f'{name=} {fits_spec=} {PSF_MODEL_DI_CLASS=} {PSF_MODEL_DI=}')
	with fits.open(Path(fits_spec.path)) as data_hdul:
		with nph.axes.to_end(data_hdul[fits_spec.ext].data[fits_spec.slices], fits_spec.axes['CELESTIAL']) as data:
			PSF_MODEL_DI = PSF_MODEL_DI_CLASS(data[tuple(0 for i in range(data.ndim-2))])
	return

def get_psf_model_dependency_injector():
	"""
	Gets the dependecy injector instance
	"""
	return PSF_MODEL_DI

def get_new_psf_model_dependency_injector(data):
	"""
	Creates a new instance of the dependency injector based upon the module-wide dependency injector class. Copies the module-wide dependency injector parameters.
	"""
	di = PSF_MODEL_DI_CLASS(data)
	di._params = PriorParamSet(*PSF_MODEL_DI._params.prior_params)
	return di



def set_psf_model_dependency_injector_params(variables=[], **kwargs):
	"""
	Sets the parameters of the module-wide dependency injector
	"""
	global PSF_MODEL_DI
	new_params = []
	_lgr.debug(f'{variables=}')
	_lgr.debug(f'{kwargs=}')
	for p in PSF_MODEL_DI._params.prior_params:
		new_params.append(p)
		new_params[-1].const_value = kwargs.get(p.name, p.const_value)
		new_params[-1].domain = kwargs.get(p.name+'_domain', p.domain)
		new_params[-1].is_const = p.name not in variables
	
	PSF_MODEL_DI._params = PriorParamSet(*new_params)
		
		

	
def plot_result(result, psf_data, suptitle=None, show=True):
	"""
	Plot the result of fitting a model to a PSF
	"""
	if not show: return

	residual = psf_data-result
	
	f, a = plot_helper.figure_n_subplots(7)
	
	a[0].set_title(f'data sum={np.nansum(psf_data)}')
	a[0].imshow(np.log(psf_data))
	a[0].plot([psf_data.shape[0]/2],[psf_data.shape[1]/2], 'r.')
	
	a[1].set_title(f'result sum={np.nansum(result)}')
	a[1].imshow(np.log(result))
	a[1].plot([result.shape[0]/2],[result.shape[1]/2], 'r.')
	
	a[2].set_title(f'residual sum={np.nansum(residual)}')
	a[2].imshow(np.log(residual))
	
	a[3].set_title(f'residual_squared sqrt(sum)={np.sqrt(np.nansum(residual**2))}')
	a[3].imshow(np.log((residual)**2))
	
	a[4].set_title('data and result slice (horizontal)')
	a[4].plot(np.log(psf_data[psf_data.shape[0]//2,:]).flatten())
	a[4].plot(np.log(result[result.shape[0]//2,:]).flatten())
	a[4].axvline(result.shape[0]//2, color='red', ls='--')

	
	a[5].set_title('data and result slice (vertical)')
	a[5].plot(np.log(psf_data[:,psf_data.shape[1]//2]).flatten())
	a[5].plot(np.log(result[:,result.shape[1]//2]).flatten())
	a[5].axvline(result.shape[1]//2, color='red', ls='--')
	
	offsets_from_centre = nph.array.offsets_from_point(psf_data.shape)
	offsets_from_centre = (offsets_from_centre.T - np.array([0.0,0.5])).T
	r_idx1 = np.sqrt(np.sum(offsets_from_centre**2, axis=0))
	r = np.linspace(0,np.max(r_idx1),30)
	psf_radial_data = np.array([np.nansum(psf_data[(r_min <= r_idx1) & (r_idx1 < r_max) ]) for r_min, r_max in zip(r[:-1], r[1:])])
	
	offsets_from_centre = nph.array.offsets_from_point(psf_data.shape)
	offsets_from_centre = (offsets_from_centre.T - np.array([0.5,0.5])).T
	r_idx2 = np.sqrt(np.sum(offsets_from_centre**2, axis=0))
	r = np.linspace(0,np.max(r_idx2),30)
	result_radial_data = np.array([np.nansum(result[(r_min <= r_idx2) & (r_idx2 < r_max) ]) for r_min, r_max in zip(r[:-1], r[1:])])
	
	a[6].set_title('radial data and result')
	a[6].plot(r[:-1], psf_radial_data)
	a[6].plot(r[:-1], result_radial_data)
	
	f.suptitle(suptitle)
	
	plot_helper.output(show)


def run(
		fits_spec,
		output_path,
		fit_result_dir : str | None = None,
		method : str = 'ultranest',
		error_factor = 1E-3,
	):
	
	original_data_type=None
	
	if fit_result_dir is None:
		fit_result_dir = Path(output_path).parent
	
	axes = fits_spec.axes['CELESTIAL']
	
	with fits.open(Path(fits_spec.path)) as data_hdul:
		
		
		_lgr.debug(f'{fits_spec.path=} {fits_spec.ext=} {fits_spec.slices=} {fits_spec.axes=}')
		#raise RuntimeError(f'DEBUGGING')
	
		data_hdu = data_hdul[fits_spec.ext]
		data = data_hdu.data
		hdr = data_hdu.header
		original_data_type = data_hdu.data.dtype
		axes = fits_spec.axes['CELESTIAL']
		
		# Currently only works with a single spectral axis
		# Assume if we only have a single dimension left over, the left over axis
		# is the spectral one, otherwise try and find it from the header.
		if data.ndim == (len(axes) + 1):
			spectral_axes = tuple(i for i in range(data.ndim) if i not in axes)
		else:
			spectral_axes = aph.fits.header.get_spectral_axes(hdr)
			if len(spectral_axes) != 1:
				raise RuntimeError('Data must have exactly one spectral axis')
		
		
		spectral_axes_slices = tuple(slice(None) if x in spectral_axes else 0 for x in range(data.ndim))
		_lgr.debug(f'{spectral_axes=}')
		
		spectral_coords = aph.fits.header.get_world_coords_of_axis(hdr, spectral_axes)
		_lgr.debug(f'{spectral_coords.shape=}')
		
		_lgr.debug(f'{PSF_MODEL_DI._params=}')
		
		timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
		result_set_directory = fit_result_dir / f'{timestamp}_psf_fit_result'
			
		match method:
			case 'ultranest':
				result_set = UltranestResultSet(Path(result_set_directory))
				result_set.metadata['wavelength_idxs'] = tuple((x,i) for i,x in enumerate(spectral_coords))
				result_set.save_metadata()
		
		result_callables = []
		
		result_data = np.full_like(data, np.nan)
		fitted_params = [None]*spectral_coords.shape[0]
		
		for i, idx in enumerate(nph.slice.iter_indices(data, fits_spec.slices, axes)):
			_lgr.debug(f'{spectral_axes_slices=}')
			j = idx[spectral_axes[0]]
			for _ in range(len(idx)-1):
				j = j[0]
			_lgr.debug(f'{i=} {j=}')
			
			psf_data = data[idx] #np.nan_to_num(data[idx])
			#psf_err = 1E-2*psf_data + 1E-3*abs(np.nanmax(psf_data))
			psf_err = error_factor*psf_data
			di = get_new_psf_model_dependency_injector(psf_data)
			
			if 'wavelength' in di._params.all_params:
				wavelength = spectral_coords[j]
				variables = [x.name for x in di._params.variable_params if x.name != wavelength]
				set_psf_model_dependency_injector_params(variables, {'wavelength' : wavelength})
	
	
			psf_model_name = di.get_psf_model_name()
			params = di.get_parameters()
			psf_model_callable = di.get_psf_model_flattened_callable()
			psf_result_postprocess = di.get_psf_result_postprocessor()
			result_callables.append(di.get_fitted_parameters_callable())
			
			
	
			

			# Get correct fitting function and objective function for fitting method
			fitting_function = None
			objective_function_factory = None
			
			match method:
				case 'ultranest':
					# NOTE: Alter the parameters here to make the nested sampling more exact/take longer vs less exact/run faster
					num_live_points = 20
					result_set.metadata['constant_parameters'] = [p.to_dict() for p in params.constant_params]
					result_set.save_metadata()
					fitting_function = fitting_function_factory(
						reactive_nested_sampler_kwargs = {
							'log_dir' : result_set.directory,
							'run_num' : j
						},
						sampler_run_kwargs = {
							'max_iters' : 500, #500, # 2000,
							'max_ncalls' : 5000, #5000
							'frac_remain' : 1E-2,
							'Lepsilon' : 1E-1,
							'min_num_live_points' : num_live_points, #20, #80
							'cluster_num_live_points' : num_live_points//5, #1, #40
							'min_ess' : num_live_points, #1, #40
							'widen_before_initial_plateau_num_warn' : (3*num_live_points)//2, #*min_live_points,
							'widen_before_initial_plateau_num_max' : 2*num_live_points #*min_live_points
						}
					)
					objective_function_factory = partial(psf_data_ops.objective_function_factory, mode='maximise')
				case 'scipy.minimize':
					fitting_function = psf_data_ops.scipy_fitting_function_factory(sp.optimize.minimize)
					objective_function_factory = partial(psf_data_ops.objective_function_factory, mode='minimise')
				case _:
					raise RuntimeError(f'Unknown fitting method "{method}". Should be one of {FITTING_METHODS}')
			
			
			# Perform fit
			fitted_psf, fitted_vars, consts = psf_data_ops.fit_to_data(
				params, 
				psf_model_callable, 
				psf_data, 
				psf_err,
				fitting_function,
				objective_function_factory,
				plot_mode=None
			)
			_lgr.info(f'{fitted_vars=}')
			_lgr.info(f'{consts=}')
			
			fitted_params[j] = {**fitted_vars, **consts}
			
			# Do any postprocessing if we need to
			if psf_result_postprocess is not None:
				result_data[idx] = psf_result_postprocess(params, psf_model_callable, fitted_vars, consts)
				plot_result(result_data[idx], psf_data, suptitle=f'{j=}\n{fitted_vars=}', show=False)
			
			
		
		match method:
			case 'ultranest':
				result_set.plot_params_vs_run_index(show=False, save=True)
				result_set.plot_results(
					result_callables,
					data,
					show=False,
					save=True
				)
		
		
	param_dict = {
		'method' : method,
		'model' : PSF_MODEL_DI._psf_model.__class__.__name__,
		'fit_result_dir' : None if (method not in ('ultranest',)) else fit_result_dir
	}
	
	hdr.update(aph.fits.header.DictReader(
		param_dict,
		prefix='fit_psf_model',
		pkey_count_start=aph.fits.header.DictReader.find_max_pkey_n(hdr)
	))
	


	_lgr.info('save the products to a FITS file')
	hdus = []

	hdus.append(fits.PrimaryHDU(
		header = hdr,
		data = result_data.astype(original_data_type)
	))
	
	
	
	hdus.append(fits.BinTableHDU.from_columns(
		columns = [
			fits.Column(name=k, format='D', array=[x[k] if x is not None else np.nan for x in fitted_params]) for k in fitted_params[[i for i,x in enumerate(fitted_params) if x is not None][0]].keys()
		],
		name = 'FITTED_MODEL_PARAMS',
		header = None,
	))
	
	hdul_output = fits.HDUList(hdus)
	hdul_output.writeto(output_path, overwrite=True)
	_lgr.info(f'Written fitted psf to {output_path.absolute().relative_to(Path().absolute(),walk_up=True)}')


def parse_args(argv):
	import os
	import aopp_deconv_tool.text
	import argparse
	
	DEFAULT_OUTPUT_TAG = '_modelled'
	DESIRED_FITS_AXES = ['CELESTIAL']
	OUTPUT_COLUMNS=80
	try:
		OUTPUT_COLUMNS = os.get_terminal_size().columns - 30
	except Exception:
		pass
	
	FITS_SPECIFIER_HELP = aopp_deconv_tool.text.wrap(
		aph.fits.specifier.get_help(DESIRED_FITS_AXES).replace('\t', '    '),
		OUTPUT_COLUMNS
	)
	
	class ArgFormatter (argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter, argparse.MetavarTypeHelpFormatter):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
	
	parser = argparse.ArgumentParser(
		description=__doc__, 
		formatter_class=ArgFormatter,
		epilog=FITS_SPECIFIER_HELP
	)
	
	parser.add_argument(
		'fits_spec',
		help = '\n'.join((
			f'FITS Specifier of the data to operate upon . See the end of the help message for more information',
			f'required axes: {", ".join(DESIRED_FITS_AXES)}',
		)),
		type=str,
		metavar='FITS Specifier',
	)
	
	#parser.add_argument('-o', '--output_path', type=str, help=f'Output fits file path. If None, is same as the `fits_spec` path with "{DEFAULT_OUTPUT_TAG}" appended to the filename')
	parser.add_argument(
		'-o', 
		'--output_path', 
		type=FPath,
		metavar='str',
		default='{parent}/{stem}{tag}_{model}{suffix}',
		help = '\n    '.join((
			f'Output fits file path, supports keyword substitution using parts of `fits_spec` path where:',
			'{parent}: containing folder',
			'{stem}  : filename (not including final extension)',
			f'{{tag}}   : script specific tag, "{DEFAULT_OUTPUT_TAG}" in this case',
			'{model} : model fitted to psf',
			'{suffix}: final extension (everything after the last ".", including the ".")',
			'\b'
		))
	)
	
	parser.add_argument('--fit_result_dir', type=str, default=None, help='Directory to store results of PSF fit in. Will create a sub-directory below the given path. If None, will create a sibling folder to the output file (i.e., output file parent directory is used).')

	parser.add_argument('--model', type=str, default='radial', choices=tuple(psf_models.keys()), help='Model to fit to PSF data.')

	parser.add_argument('--method', type=str, default='scipy.minimize', choices=FITTING_METHODS, help='What method should we use to perform the fitting')

	parser.add_argument('--error_factor', type=float, default=1E-3, help='What factor of the PSF value is error')

	parser.add_argument('--model_help', action='store_true', default=False, help='Show the help message for the selected model')

	args, psf_model_args = parser.parse_known_args(argv)
	
	args.fits_spec = aph.fits.specifier.parse(args.fits_spec, DESIRED_FITS_AXES)
	
	#if args.output_path is None:
	#	args.output_path =  (Path(args.fits_spec.path).parent / (str(Path(args.fits_spec.path).stem)+DEFAULT_OUTPUT_TAG+f'_{args.model}'+str(Path(args.fits_spec.path).suffix)))
	other_file_path = Path(args.fits_spec.path)
	args.output_path = args.output_path.with_fields(
		tag=DEFAULT_OUTPUT_TAG, 
		parent=other_file_path.parent, 
		stem=other_file_path.stem, 
		suffix=other_file_path.suffix,
		model=args.model,
	)
	
	set_psf_model_dependency_injector(args.model, args.fits_spec)
	
	di = get_psf_model_dependency_injector()
	params = di._params.all_params
	
	di_param_parser = argparse.ArgumentParser(
		prog=f'fit_psf_model.py --model {args.model}',
		description=get_psf_model_dependency_injector().__doc__, 
		formatter_class=ArgFormatter,
		add_help=False,
	)
	
	for item in params:
		di_param_parser.add_argument("--"+item.name, type=float, default=di._params[item.name].const_value, help=item.description)
		di_param_parser.add_argument("--"+item.name+'_domain', nargs=2, type=float, default=di._params[item.name].domain, help=f'domain parameter "{item.name}" for "{args.model}" psf model')
	
	default_variable_params = [x.name for x in di._params.variable_params]
	di_param_parser.add_argument('--variables', nargs='*', type=str, default=default_variable_params, choices=[x.name for x in params], help=f'Which parameters to vary when fitting, others will be held constant.')
	
	if args.model_help:
		di_param_parser.print_help()
		sys.exit()
	
	di_params = vars(di_param_parser.parse_args(psf_model_args))
	_lgr.debug(f'{di_params["variables"]=}')
	
	set_psf_model_dependency_injector_params(**di_params)
	
	
	
	
	
	
	
	
	return args

def go(
		fits_spec,
		output_path=None,
		fit_result_dir=None,
		model=None,
		method=None,
		model_help=None,
		error_factor=None,
		**kwargs
	):
	"""
	Thin wrapper around `run()` to accept string inputs.
	As long as the names of the arguments to this function 
	are the same as the names expected from the command line
	we can do this programatically
	"""
	# Add stuff to kwargs here if needed
	
	# This must be first so we only grab the arguments to the function
	fargs = dict(locals().items())
	arglist = aopp_deconv_tool.arguments.construct_arglist_from_locals(fargs, n_positional_args=1)
	exec_with_args(arglist)

def exec_with_args(argv):
	args = parse_args(argv)
	
	run(
		args.fits_spec, 
		args.output_path,
		args.fit_result_dir,
		args.method,
		args.error_factor,
	)


if __name__=='__main__':
	exec_with_args(sys.argv[1:])