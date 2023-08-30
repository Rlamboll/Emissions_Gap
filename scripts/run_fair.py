import errno
import json
from multiprocessing import Pool, cpu_count, freeze_support

import fair
from fair.tools.magicc import scen_open
import os
import numpy as np
import pandas as pd
from tqdm import tqdm

with open('../input/fair-1.6.2-ar6/fair-1.6.2-wg3-params.json') as f:
    config_list = json.load(f)
natural_ems = pd.read_csv(
    "../input/fair-1.6.2-ar6/fair_wg3_natural_ch4_n2o.csv", sep=","
)

emissions_in = {}
results_out = {}
WORKERS = cpu_count() - 1
version = "v23"
outdir = '../output/{}/fair_{}/'
parallel_processing = True
end_year = 2100
start_year = natural_ems.loc[0, "year"]
inter_start_year = 1850   # First year we actually care about values from
natural_ems = natural_ems.iloc[:end_year-start_year+1, 1:].values

scen_file_dir = f"../output/scens/{version}/"
scens_to_run = [
    x for x in os.listdir(scen_file_dir)
    if x.endswith('.SCEN')
]

# Often want to restrict number of runs in one go
scens_to_run = scens_to_run[:]

scenarios = [x[:-5] for x in scens_to_run]
check_prehist = np.loadtxt(
    '../input/fair-1.6.2-ar6/ssp245_constant-2020-ch4.csv',
    delimiter=','
)
for i, scenario in enumerate(scenarios):
    tmp = scen_open(scen_file_dir + scens_to_run[i])
    if tmp[0, 0] != start_year:
        if check_prehist[0, 0] == start_year:
            needed_rows = int(tmp[0, 0] - start_year)
            tmp = np.concatenate([check_prehist[:needed_rows, :], tmp])

    emissions_in[scenario] = tmp

def mkdir_p(path):
    """Check to see if directory exists, and if not, create it.
    Parameters
    ----------
        path : str
            directory to create
    Raises
    ------
        OSError:
            if directory cannot be created
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def run_fair(args):
    thisC, thisF, thisT, _, thisOHU, _, thisAF = fair.forward.fair_scm(**args)
    return (thisC[:, 0], thisC[:, 1], thisT, thisF[:, 1], np.sum(thisF, axis=1))


def fair_process(emissions):
    updated_config = []
    for i, cfg in enumerate(config_list):
        updated_config.append({})
        for key, value in cfg.items():
            if isinstance(value, list):
                updated_config[i][key] = np.asarray(value)
            else:
                updated_config[i][key] = value
        emissions_length = len(emissions)
        project_length = len(updated_config[i]["F_solar"])
        updated_config[i]['emissions'] = emissions
        updated_config[i]['diagnostics'] = 'AR6'
        updated_config[i]["efficacy"] = np.ones(45)
        updated_config[i]["gir_carbon_cycle"] = True
        updated_config[i]["temperature_function"] = "Geoffroy"
        updated_config[i]["aerosol_forcing"] = "aerocom+ghan2"
        updated_config[i]["fixPre1850RCP"] = False
        #    updated_config[i]["scale"][43] = 0.6
        updated_config[i]["F_solar"][270:] = 0
        updated_config[i]["natural"] = natural_ems
        if project_length < emissions_length:
            updated_config[i]["F_volcanic"] = np.pad(updated_config[i]["F_volcanic"], (0, emissions_length-project_length))
            updated_config[i]["F_solar"] = np.pad(updated_config[i]["F_solar"], (0, emissions_length-project_length))
        elif project_length > emissions_length:
            updated_config[i]["F_volcanic"] = updated_config[i]["F_volcanic"][: emissions_length]
            updated_config[i]["F_solar"] = updated_config[i]["F_solar"][: emissions_length]

    if __name__ == '__main__':
        if parallel_processing:
            with Pool(WORKERS) as pool:
                result = list(pool.imap(run_fair, updated_config))

            result_t = np.array(result).transpose(1, 2, 0)
            c_co2, c_ch4, t, f_ch4, f_tot = result_t
        else:
            shape = (end_year - start_year + 1, len(updated_config))
            c_co2 = np.ones(shape) * np.nan
            c_ch4 = np.ones(shape) * np.nan
            t = np.ones(shape) * np.nan
            f_ch4 = np.ones(shape) * np.nan
            f_tot = np.ones(shape) * np.nan
            for i, cfg in tqdm(enumerate(updated_config), total=len(updated_config),
                               position=0, leave=True):
                c_co2[:, i], c_ch4[:, i], t[:, i], f_ch4[:, i], f_tot[:, i] = run_fair(
                    updated_config[i])
        temp_rebase = t - t[100:151, :].mean(axis=0)
    else:
        raise RuntimeError

    return c_co2, c_ch4, temp_rebase, f_ch4, f_tot

def main():
    freeze_support()
    for scenario in tqdm(scenarios, position=0, leave=True):
        results_out[scenario] = {}
        (
            results_out[scenario]['co2_concentrations'],
            results_out[scenario]['ch4_concentrations'],
            results_out[scenario]['temperatures'],
            _, _
        ) = fair_process(emissions_in[scenario])

    for scenario in scenarios:
        for var in [
            'co2_concentrations', 'ch4_concentrations', 'temperatures',
        ]:
            mkdir_p(outdir.format(version, var.replace("effective_radiative_forcing", "erf")))
            df_out = pd.DataFrame(
                results_out[scenario][var][
                inter_start_year - start_year: end_year + 1 - start_year, :]
            )
            df_out['year'] = np.arange(inter_start_year, end_year + 1)
            df_out.set_index('year', inplace=True)
            df_out.to_csv(
                outdir.format(version, var.replace("effective_radiative_forcing", "erf")
            ) + '{}.csv'.format(scenario), float_format="%6.4f")

if __name__ == "__main__":
    main()