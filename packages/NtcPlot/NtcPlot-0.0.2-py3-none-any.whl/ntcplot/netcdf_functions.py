from netCDF4 import Dataset
import subprocess

def close(self):
    """Closes the NetCDF file."""
    if not self.fp.closed:
        try:
            self.flush()
        finally:
            self.fp.close()

# get all groups from just one netcdf
def walktree(top):
    yield top.groups.values()
    for value in top.groups.values():
        yield from walktree(value)

# return ncdump -h file.nc as string for IHM
def ncdump_fuction(ntc_file):
    subpro = subprocess.run(["ncdump", "-h", ntc_file], capture_output=True, text=True)
    stri = subpro.stdout
    return stri

def nc_variables(ntc_file):
    # read netcdf
    nc_dts = Dataset(ntc_file, "r")

    # get all groups from netcdf
    groups = []
    for topgroup in walktree(nc_dts):
        for u_group in topgroup:
            gr_path = u_group.path
            # remove "/" from beginning of string
            groups.append(gr_path[1:])

    # close  netcdf
    nc_dts.close()

    # dict with all datasets
    var_dict = {}

    group_ds = Dataset(ntc_file)
    for var in [i for i in group_ds.variables]:
        var_dict[var] = {}
        var_dict[var]["values"] = group_ds.variables[var][:]
        var_dict[var]["dims"] = group_ds.variables[var].dimensions

        try:
            var_dict[var]["units"] = group_ds.variables[var].units
            if var_dict[var]["units"] == "-":
                var_dict[var]["units"] = "NoUnits"
        except:
            var_dict[var]["units"] = "NoUnits"

    # work by group on all netcdfs
    for group_id in groups:
        for var in [i for i in group_ds[group_id].variables]:
            var_dict[var] = {}
            var_dict[var]["values"] = group_ds[group_id].variables[var][:]
            var_dict[var]["dims"] = group_ds[group_id].variables[var].dimensions
            try:
                var_dict[var]["units"] = group_ds[group_id].variables[var].units
                if var_dict[var]["units"] == "-":
                    var_dict[var]["units"] = "NoUnits"
            except:
                var_dict[var]["units"] = "NoUnits"
    group_ds.close()
    return var_dict


