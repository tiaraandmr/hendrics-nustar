# Automation Code for NuSTAR Light Curves Extraction 

This code utilizes [HENDRICS v8.1](https://hendrics.stingray.science/en/latest/) to extract 1-second bin light curves from NuSTAR FPMA observation-long X-ray archival data based on good time intervals (GTIs) with a minimum length of 800 seconds. Additional statistics, such as fractional rms and hardness ratios, will be generated together with the light curves.

## Dependencies
This code was made to run inside a Docker Container containing HEASOFT v.6-34, but can also be used natively with HEASOFT (minimum of v.6-32) and Python 3.9+ installed. Docker images for the newest version of HEASOFT (v.6-34) built to run on top of ARM64 machines are available in this [repository](https://hub.docker.com/r/tiaraandmr/heasoft-6.34). 

The main dependency of HENDRICS is:
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

It is advised to clone the entire hendrics-nustar repository. This is done by using the following commands to clone the directory over HTTPS.
```
cd /path/to/directory
git clone https://github.com/tiaraandmr/hendrics-nustar.git
```
Then the dependencies can be installed. It is recommended to install conda (or another wrapper). A conda environment with nearly all the dependencies can be installed via the provided "environment.yml" file. If you do not wish to use conda, you can install the dependencies enumerated in the "environment.yml" file.
```
cd /path/to/hendrics-nustar/directory
conda env create -f environment.yml
```
or using pip:
```
pip install hendrics numba emcee statsmodels netcdf4 matplotlib stingray>=1.1
```

In case the conda option is chosen, the environment will then be installed under the name hendrics-nustar and can then be activated.

```
conda activate hendrics-nustar
```

## Running the Scripts
The hendrics-auto.py script will reduce, extract, and calculate the statistics for the raw NuSTAR FPMA data provided in steps as follows:

### Setting the 'obj_name' variable
