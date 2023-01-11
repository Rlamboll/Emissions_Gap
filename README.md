# Emissions gap calculations

Calculation of long-term temperature implications from short-term (2030) emissions trajectories plus net zero commitments.

This repository requires an estimate of the short-term emissions and net zero estimates, which can be obtained from [zenodo](https://doi.org/10.5281/zenodo.7526226) plus the set of complete global emissions from the SR1.5 database, which can be downloaded via [pyam](https://pyam-iamc.readthedocs.io/en/stable/tutorials/iiasa_dbs.html) or zenodo [1-2]. This should be put in the input folder. All other requirements for running it are contained within. 

To get results, you then run notebooks 01-03 and then the scripts run_fair to generate the temperature distribution and calc_temp_quants to summarise this. 

[1] Huppmann, D., Rogelj, J., Kriegler, E., Krey, V. and Riahi, K.: A new scenario resource for integrated 1.5 °C research, Nat. Clim. Chang., 8(12), 1027–1030, doi:10.1038/s41558-018-0317-4, 2018.
[2] Huppmann, D., Kriegler, E., Krey, V., Riahi, K., Rogelj, J., Calvin, K., Humpenoeder, F., Popp, A., Rose, S. K., Weyant, J., Bauer, N., Bertram, C., Bosetti, V., Doelman, J., Drouet, L., Emmerling, J., Frank, S., Fujimori, S., Gernaat, D., … Zhang, R. (2019). IAMC 1.5°C Scenario Explorer and Data hosted by IIASA. https://doi.org/10.5281/ZENODO.3363345