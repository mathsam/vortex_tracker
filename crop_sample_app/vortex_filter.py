"""
filter the vorticity data and highlights the vortices
"""
import PIL.Image
import scipy.ndimage.interpolation
import numpy as np
from matplotlib import cm
import scipy.ndimage.measurements as me
import scipy.ndimage.filters

def array2imag(field_in, scale=3, filter_func=None, cmap=cm.gray):
    """interpolate an input array and turn it into PIL image
    Args:
        field_in: 2d numpy array
        scale: how many times to interpolate to
        filter_func: which filter function to use
    Returns:
        imag: PIL image
    """
    if filter_func is None:
        filter_func = highlight_local_extremes
    hires_field = scipy.ndimage.interpolation.zoom(field_in, scale, mode='wrap')
    hires_field = filter_func(hires_field)
    mapper = cm.ScalarMappable(cmap=cmap)
    imag_array = mapper.to_rgba(hires_field, alpha=None, bytes=True)
    imag = PIL.Image.fromarray(imag_array)
    return imag

def highlight_extremes(in_field, cutoff_val=None, background=0.):
    tmp_field = abs(in_field - np.mean(in_field.flatten()))
    if cutoff_val is None:
        cutoff_val = 1.5*np.std(in_field)
    out_field = np.zeros_like(tmp_field)
    out_field[tmp_field >= cutoff_val] = (tmp_field - cutoff_val)[tmp_field >= cutoff_val]
    peaks = me.label(out_field)[0]
    peak_labels = np.unique(peaks)
    for i_label in peak_labels:
        mask = (peaks == i_label)
        out_field[mask] = out_field[mask]/np.max(out_field[mask])
    out_field[tmp_field < cutoff_val] = background
    return out_field

def highlight_local_extremes(in_field, cutoff_ratio=1., size=80):
    tmp_field = abs(in_field - np.mean(in_field.flatten()))
    tmp_field2 = tmp_field**2
    tmp_field2 = scipy.ndimage.filters.uniform_filter(tmp_field2, size=size, mode='wrap')
    tmp_field_std = np.sqrt(tmp_field2)
    out_field = np.zeros_like(tmp_field)
    out_field[tmp_field >= cutoff_ratio*tmp_field_std] = (tmp_field - cutoff_ratio*tmp_field_std)[tmp_field >= cutoff_ratio*tmp_field_std]
    peaks = me.label(out_field)[0]
    peak_labels = np.unique(peaks)
    for i_label in peak_labels:
        mask = (peaks == i_label)
        out_field[mask] = out_field[mask]/np.max(out_field[mask])
    out_field[tmp_field <=cutoff_ratio*tmp_field_std] = 0.5 
    return out_field
