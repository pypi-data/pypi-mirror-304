import os
import sys
import warnings
from .julia_helpers import *

# Check if JuliaCall is already loaded, and if so, warn the user
# about the relevant environment variables. If not loaded,
# set up sensible defaults.
if "juliacall" in sys.modules:
    #warnings.warn(
    #    "juliacall module already imported. "
    #    "Make sure that you have set the environment variable `PYTHON_JULIACALL_HANDLE_SIGNALS=yes` to avoid segfaults. "
    #    "Also note that truncatedgaussianmixtures will not be able to configure `PYTHON_JULIACALL_THREADS` or `PYTHON_JULIACALL_OPTLEVEL` for you."
    #)
    pass
else:
    # Required to avoid segfaults (https://juliapy.github.io/PythonCall.jl/dev/faq/)
    if os.environ.get("PYTHON_JULIACALL_HANDLE_SIGNALS", "yes") != "yes":
        warnings.warn(
            "PYTHON_JULIACALL_HANDLE_SIGNALS environment variable is set to something other than 'yes' or ''. "
            + "You will experience segfaults if running with multithreading."
        )

    if os.environ.get("PYTHON_JULIACALL_THREADS", "auto") != "auto":
        warnings.warn(
            "PYTHON_JULIACALL_THREADS environment variable is set to something other than 'auto', "
            "so truncatedgaussianmixtures was not able to set it. You may wish to set it to `'auto'` for full use "
            "of your CPU."
        )

    # TODO: Remove these when juliapkg lets you specify this
    for k, default in (
        ("PYTHON_JULIACALL_HANDLE_SIGNALS", "yes"),
        ("PYTHON_JULIACALL_THREADS", "auto"),
        ("PYTHON_JULIACALL_OPTLEVEL", "3"),
    ):
        os.environ[k] = os.environ.get(k, default)


from juliacall import Main as jl  # type: ignore

jl_version = (jl.VERSION.major, jl.VERSION.minor, jl.VERSION.patch)

# Next, automatically load the juliacall extension if we're in a Jupyter notebook
autoload_extensions = os.environ.get("PYSR_AUTOLOAD_EXTENSIONS", "yes")
if autoload_extensions in {"yes", ""} and jl_version >= (1, 9, 0):
    try:
        get_ipython = sys.modules["IPython"].get_ipython

        if "IPKernelApp" not in get_ipython().config:
            raise ImportError("console")

        print(
            "Detected Jupyter notebook. Loading juliacall extension. Set `PYSR_AUTOLOAD_EXTENSIONS=no` to disable."
        )

        # TODO: Turn this off if juliacall does this automatically
        get_ipython().run_line_magic("load_ext", "juliacall")
    except Exception:
        pass
elif autoload_extensions not in {"no", "yes", ""}:
    warnings.warn(
        "PYSR_AUTOLOAD_EXTENSIONS environment variable is set to something other than 'yes' or 'no' or ''."
    )


jl.seval("using Pkg: Pkg")
Pkg = jl.Pkg

needed_pkgs = ["Distributions", "LogExpFunctions", "Clustering", "LinearAlgebra", "Distributions", "MvNormalCDF", 
               "StatsBase", "InvertedIndices", "ProgressMeter", "DataFrames", "DiffRules", "ForwardDiff", "Roots"]

def force_install_tgmm(force=True, install_pkgs=False, needed_pkgs=needed_pkgs):
    if force:
        Pkg.rm("TruncatedGaussianMixtures")
    if install_pkgs:
        Pkg.add(url="https://github.com/Potatoasad/TruncatedGaussianMixtures.jl")
        for pkgname in needed_pkgs:
            Pkg.add(pkgname)

#Pkg.rm("TruncatedGaussianMixtures")
#Pkg.add(url="https://github.com/Potatoasad/TruncatedGaussianMixtures.jl")

### DEV 
#Pkg.develop(path="/Users/asadh/Documents/Github/TruncatedGaussianMixtures.jl" ,io=jl.devnull)

## Check if TGM is installed:
tgmm_is_installed = any( x.name == "TruncatedGaussianMixtures" for x in jl.values(jl.Pkg.dependencies()) )
if not tgmm_is_installed:
    print("Installing TruncatedGaussianMixtures")
    force_install_tgmm(force=False, install_pkgs=True, needed_pkgs=needed_pkgs)
    

jl.seval("using TruncatedGaussianMixtures: TruncatedGaussianMixtures")
jl.seval("using TruncatedGaussianMixtures")
TruncatedGaussianMixtures = jl.TruncatedGaussianMixtures