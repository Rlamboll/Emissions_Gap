import os

version = "v22.7"

scen_file_dir = f'../output/scens/{version}/'
scens_to_run = [
    x[:-5] for x in os.listdir(scen_file_dir)
    if x.endswith('.SCEN')
]
print()
pointless = [s for s in scens_to_run if "nz_CO2_only_cert_higher" in s]
print(pointless)
for file in pointless:
    try:
        os.remove(scen_file_dir + file + ".SCEN")
    except FileNotFoundError:
        print(f"file {file} not found")