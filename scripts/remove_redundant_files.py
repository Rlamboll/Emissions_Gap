import os

version = "v22.6"

scen_file_dir = '../output/scens/v22.6/'
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