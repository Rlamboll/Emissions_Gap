import os

version = "v23.6"
outdir = '../output/{}/fair_{}/'

scen_file_dir = f'../output/scens/{version}/'
scens_to_run = [
    x[:-5] for x in os.listdir(scen_file_dir)
    if x.endswith('.SCEN')
]


ran_scens = [
    x[:-4] for x in os.listdir(outdir.format(version, "temperatures"))
    if x.endswith('.csv')
]

unrun_scens = [s for s in scens_to_run if s not in ran_scens]
unrun_indices = [i for i, s in enumerate(scens_to_run) if s in unrun_scens]

print(scens_to_run[0])
print(ran_scens[0])
print("\n\n HAVE NOT RUN: \n")

print(unrun_indices)