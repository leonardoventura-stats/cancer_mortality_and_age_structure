# Cancer mortality and age structure analysis (Italy vs Europe)

This repository contains the script to calculate crude and standardized mortality rates, and to conduct a sensitivity analysis and a Kitagawa decomposition.

## Code structure

- `analysis.py` –-> Main script that runs the analysis.
- `compute_rates.py` –-> Functions to calculate crude mortality rates.
- `standardize.py` –-> Functions to directly standardize the rates (using ESP2013) and to calculate CI (with Exact Poisson limits method and Gamma method by Fay and Feuer).
- `kitagawa_deco.py` –-> Functions to conduct the Kitagawa decomposition.
- `sensitivity_analysis.py` –-> Sensitivity analysis (EU vs EU without Italy).
- `plots.py` –-> Functions to create tables and graphs.
- `utils.py` –-> Functions to load and clean data.
- `requirements.txt` –->  List with requirements.
- `download_data.md` –-> File with the instructions to download the official data used in the analysis.

## Data used

If you want to download the data follow the instructions in [download_data.md](download_data.md)
Data should be positioned into the folder `data/`.

## How to conduct the analysis

1. Clone the repository;
2. Install the dependencies;
3. Download the dataset necessary;
4. Run the main script:
   ```bash
   python analysis.py --input data/ --output output/
5. Results (Tables and Graphs) will be saved in the folder (output/).

## Output

The analysis creates tables and graphs that will be saved in the folder `output/`:

- **Graphs**
  - `Standardized_rates_Italy_vs_Europe.png` --> comparison between standardized rates in Italy and Europe from 2020 to 2022 for males and females.
  - `Raw_rates_Italy_vs_Europe.png` --> comparison between crude rates in Italy and Europe from 2020 to 2022 for males and females.
  - `Age_distribution.png` --> Age-specific rates distribution in Italy and Europe in 2020, 2021 and 2022.
  - `Raw_vs_Std.png` --> comparison between crude rates and standardized rates in Italy and Europe for each year.

- **Tables**
  - `Table_Results.png` --> Table with the crude and standardized rates by year, sex and country.
  - `Table_Results_Sens.png` --> Table with the results of the sensitivity analysis (EU vs EU without Italy).
  - `Table_Results_Kit.png` --> Table with the results of the Kitagawa decomposition.
  - Tables are also provided in .csv format.

## Download data

See [download_data.md](download_data.md) for the step-by-step instructions to download the official datasets (ISTAT and Eurostat) and to select the correct variables and save the CSV file with the names used in the script.
All files must be located in the folder `data/` before running `analysis.py`.

## References

- ISTAT and Eurostat datasets as explained in [download_data.md](download_data.md)
- All the references related to the paper can be found at arXiv: xxxx.xxxx

## Requirements

- Python >= 3.10 (tested on v3.13.7)
- See [requirements.txt](requirements.txt) for the full list of dependencies.
- It's recommended to use a virtual environment.

## License
This code is released under the MIT License.
Data must be downloaded from official sources (ISTAT and Eurostat) as explained in [download_data.md](download_data.md)

## Citation
If you use this code, please cite:
Ventura L. The Influence of Age Structure on Cancer Mortality: Evidence from Italy and Europe, 2020-2022. arXiv: xxxx.xxxx.
