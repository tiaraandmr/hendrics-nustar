# Automation Code for NuSTAR Light Curves Extraction 

This code utilizes [HENDRICS v8.1](https://hendrics.stingray.science/en/latest/) to extract 1-second bin light curves from NuSTAR FPMA observation-long X-ray archival data based on good time intervals (GTIs) with a minimum length of 800 seconds. Additional statistics, such as fractional rms and hardness ratios, will be generated together with the light curves.

## Dependencies
This code was made to run inside a Docker Container containing HEASOFT v.6-34, but can also be used natively with HEASOFT (minimum of v.6-32) and Python 3.9+ installed. The main dependency of HENDRICS is:
- Stingray

which in turn depends on:
- NumPy
- Matplotlib
- Scipy
- Astropy

Optional but recommended dependencies are:
- netCDF 4 library with its Python bindings 
- Numba
- statsmodels
- emcee
- pint

```
pip install hendrics numba emcee statsmodels netcdf4 matplotlib stingray>=1.1
```

After successfully installing HENDRICS and its dependency, clone the entire hendrics-nustar repository. This is done by using the following commands to clone the directory over HTTPS.

```
cd /path/to/directory
git clone https://github.com/tiaraandmr/hendrics-nustar.git
```
