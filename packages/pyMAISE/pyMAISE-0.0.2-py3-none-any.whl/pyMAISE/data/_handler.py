from pyMAISE.preprocessing import PreProcesser
from pkg_resources import resource_filename

# Get full pyMAISE data file path
def get_full_path(path: str):
    return resource_filename("pyMAISE", path)


# Load benchmark BWR cross section data
def load_xs():
    return PreProcesser(get_full_path("data/xs.csv"), slice(0, -1), slice(-1, None))


# Load benchmark MIT reactor data
def load_MITR():
    return PreProcesser(
        [get_full_path("data/crx.csv"), get_full_path("data/powery.csv")],
    )


# Load benchmark fuel perfromance data
def load_fp():
    return PreProcesser(
        [get_full_path("data/fp_inp.csv"), get_full_path("data/fp_out.csv")]
    )


# Load benchmark fuel centerline temperature data
def load_heat():
    return PreProcesser(get_full_path("data/heat.csv"), slice(0, -1), slice(-1, None))

# Rod ejection accident data
def load_rea():
    return PreProcesser(
        [get_full_path("data/rea_inputs.csv"), get_full_path("data/rea_outputs.csv")],
    )
