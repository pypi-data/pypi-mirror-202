from astropy.io import fits

def save_new_fit_image(ccd_header, ccd_array, ccd_name, overwrite = True):
    hdulist = fits.HDUList()
    # Append the header and data
    hdulist.append(fits.PrimaryHDU(header= ccd_header, data = ccd_array))
    hdulist.writeto(ccd_name, overwrite=overwrite)
    
    pass