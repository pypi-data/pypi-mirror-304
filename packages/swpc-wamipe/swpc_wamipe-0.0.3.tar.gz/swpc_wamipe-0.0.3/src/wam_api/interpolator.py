import numpy as np
from scipy.interpolate import interp1d, interpn

class Interpolator():
    """
    Interpolator class for interpolating density values in space and time.
    """
    def spatial(self, ds, lat, lon, alt):
        """
        @param ds: xarray dataset containing density values
        @param lat: latitude of the point to interpolate
        @param lon: longitude of the point to interpolate
        @param alt: altitude of the point to interpolate
        @return: interpolated density

        Interpolates density values in space using 2D interpolation and in the vertical using logarithmic quadratic interpolation.
        """
        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        alts = ds.variables['hlevs'][:]
        density = ds.variables["den"][:]
        density = np.squeeze(density) # Remove singleton dimensions

        # 2D interpolation using interpn for each altitude level
        interp_densities = []
        for i in range(len(alts)): # Iterate over altitude levels
            density_slice = density[i, :, :] # Slice density values at the current altitude level
            interp_density = interpn((lats, lons), density_slice, (lat, lon), method='linear', bounds_error=False, fill_value=np.nan) # Interpolate density at the current altitude level
            interp_densities.append(interp_density[0]) # Append interpolated density to list

        # Logarithmic quadratic interpolation in the vertical
        log_alts = np.log(alts) # Logarithm of altitude levels
        log_alt = np.log(alt) # Logarithm of altitude to interpolate
        log_interp = interp1d(log_alts, np.log(interp_densities), kind='quadratic', bounds_error=False, fill_value='extrapolate') # Interpolate density in the vertical
        
        density_interp = np.exp(log_interp(log_alt)) # Exponentiate interpolated density to get the final density value

        return float(density_interp)
    
    def temporal(self, input_dt, surrounding_dts, densities):
        """
        @param input_dt: datetime object of the point to interpolate
        @param surrounding_dts: list of datetime objects of surrounding points
        @param densities: list of density values at the surrounding points
        @return: interpolated density

        Interpolates density values in time using linear interpolation.
        """

        times = np.array([(tdt - surrounding_dts[0]).total_seconds() for tdt in surrounding_dts])
        dt_seconds = (input_dt - surrounding_dts[0]).total_seconds()
        return np.interp(dt_seconds, times, densities) # Linear interpolation of density values in time