
import numpy as np
from ztfimg.astrometry import WCSHolder, WCS



def get_source_ellipses(sourcedf, sourcescale=5, system="xy",
                        wcs=None, wcsout=None, **kwargs):
    """ 
    Parameters
    ----------
    sourcedf: pandas.DataFrame
        This dataframe must contain the sep/sextractor ellipse information: \n
        x,y for the centroid\n
        a,b for the second moment (major and minor axis) \n
        theta for the angle (in degree) \n
        Must be in units of xy 
        
    sourcescale: float -optional-
        This multiply a and b. 1 means second moment (1 sigma)
           
    system: string -optional-
        Coordinate system of the returned ellipses \n
        - xy: native coordinates of the input source dataframe \n
        - radec: RA, Dec assuming the input wcs and the xy system.(xy->radec) \n
        - out: xy system of an alternative wcs solution (wcsout).(xy->radec->out) 
        
    wcs,wcsout: astropy WCS -optional-
        astropy WCS solution instance to convert xy<->radec \n
        wcs is needed if system is 'radec' or 'out' \n
        wcsout is need if system is 'out'

    Returns
    -------
    matplotlib patch (Ellipse/Polygon)
    
    """
    from matplotlib.patches import Ellipse, Polygon
    
    # = Baseline xy
    if system in ["xy", "pixels", "pix","pixel"]:
        return [Ellipse((d.x,d.y), d.a*sourcescale, d.b*sourcescale, d.theta*180/np.pi, **kwargs)
                for d in sourcedf.itertuples()]
    
    # RA, Dec
    if system in ["radec", "world"]:
        if wcs is None:
            raise ValueError("no wcs provided. Necessary for radec projection")
        
        e_xy = get_source_ellipses(sourcedf, sourcescale=sourcescale, system="xy")
        return [Polygon(wcs.all_pix2world(e_.get_verts(), 0), **kwargs) for e_ in e_xy]
    
    # alternative xy    
    elif system in ["out", "xyout", "xy_out"]:
        if wcsout is None or wcs is None:
            raise ValueError("no wcs or no wcsout provided. Necessary for out projection")
        e_radec = get_source_ellipses(sourcedf, sourcescale, system="radec", wcs=wcs)
        return [Polygon(wcsout.all_world2pix(e_.get_verts(), 0), **kwargs) for e_ in e_radec]
        
    else:
        raise NotImplementedError(f"Only xy, radec or out system implemented, {system} given")
