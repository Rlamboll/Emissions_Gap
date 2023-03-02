import os
import pandas as pd

version = "v22.6"
outfile = f"../output/{version}/2022_emission_gap_temp_summary_data.csv"
fairdir = f"../output/{version}/fair_temperatures/"
scenariofiles = [
        x for x in os.listdir(fairdir)
        if x.endswith('.csv')
]
temp_quants = [0.1, 0.167, 0.2, 0.3, 0.33, 0.4, 0.5, 0.6, 0.66, 0.7, 0.8, 0.833, 0.9]
results = []
for file in scenariofiles:
    tmp = pd.read_csv(fairdir + file, index_col="year")
    for q in temp_quants:
        quant_res = tmp.quantile(q, axis=1)
        quant_res = pd.DataFrame(quant_res).T
        quant_res["quantile"] = q
        if file.split("_-_")[0] != "NDC_case":
            quant_res["scenario"] = file.split("_-_")[1]
            quant_res["model"] = file.split("_-_")[0]
        else:
            quant_res["scenario"] = file.split("_-_")[2]
            quant_res["model"] = file.split("_-_")[0] + "_-_" + file.split("_-_")[1]
        results.append(quant_res)

results = pd.concat(results)
results = results.loc[:, ["model", "scenario", "quantile"] + list(results.columns[:-3])]
results.to_csv(outfile, index=False)