import numpy as np
from astropy.io import fits
from ccd_io import *


def ccd_pre_processed(ccd_science_name, ccd_bias_name, ccd_flat_name, new_ccd_name, OVER_EXPOSURE_ADU = 65535):
    #===============================================================================#
    #                           Read the hdulist                                    #
    # science fits
    ccd_science_hdulist = fits.open(ccd_science_name)
    ccd_science_header = ccd_science_hdulist[0].header
    ccd_science_array = ccd_science_hdulist[0].data
    ccd_science_hdulist.close()
    # bias fits
    ccd_bias_hdulist = fits.open(ccd_bias_name)
    ccd_bias_header = ccd_bias_hdulist[0].header
    ccd_bias_array = ccd_bias_hdulist[0].data
    ccd_bias_hdulist.close()
    # flat fits
    ccd_flat_hdulist = fits.open(ccd_flat_name)
    ccd_flat_header = ccd_flat_hdulist[0].header
    ccd_flat_array = ccd_flat_hdulist[0].data
    ccd_flat_hdulist.close()

    if "HISTORY1" not in ccd_science_header:          #Judge whether this image has already been processed
        #===============================================================================#
        #                    Bias and Flat correction                                   #
        #                                                                               #
        ##                             science - bias
        ##             science out = ------------------
        ##                              flat - bias (>>> normalizing)
        # Science - bias
        science_subtract_bias = ccd_science_array - ccd_bias_array
        # flat - bias
        flat_subtract_bias = ccd_flat_array - ccd_bias_array
        # flat normalize
        flat_max = np.max(flat_subtract_bias)
        flat_normalize = flat_subtract_bias / flat_max
        #           ↓
        #           ↓
        #           ↓
        # Science out
        science_out_array = science_subtract_bias / flat_normalize
        # Judge whether overexposure

        if (science_out_array > OVER_EXPOSURE_ADU).any():
            print("There is over-exposure pixel after the processed image %s"%(ccd_science_name))

        #===============================================================================#
        #                            New fit save                                       #
        new_science_header = ccd_science_header
        new_science_header["HISTORY1"] = "Processed with master %s"%(ccd_bias_name)
        new_science_header["HISTORY2"] = "Processed with master %s"%(ccd_flat_name)
        save_new_fit_image(ccd_header = new_science_header, ccd_array = science_out_array, ccd_name = new_ccd_name, overwrite = True)
    else:
        print("%s has already been precessed, no operation has been done! "%(ccd_science_name))
    
    pass