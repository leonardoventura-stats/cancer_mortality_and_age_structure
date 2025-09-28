# Main script for mortality analysis
from utility import rename_age_column, load_data_ISTAT_Deaths, load_data_EUROSTAT_Deaths, load_standard_pop, year_subdivision, load_data_ISTAT_Pop, load_data_Eurostat_Pop
from compute_rates import ratio
from standardize_rates import expected_deaths_year, final, dataframe_final
from plots import graph_1, graph_2, graph_3, graph_4, table_1, table_2, table_3
from sensitivity_analysis import sensitivity, final_sens, dataframe_final_sens
from kitagawa_deco import initial_kit, final_kit, dataframe_final_kit
from pathlib import Path

def main():
    DATA_DIR = Path("data")
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR = Path("output")
    OUTPUT_DIR.mkdir(exist_ok=True)
    # reading the files and preparing the dfs
    morti_it_tot = DATA_DIR / "Deaths_Italy_Tot.csv"
    df_Deaths_Italy_Tot = load_data_ISTAT_Deaths(morti_it_tot)
    morti_it_m = DATA_DIR / "Deaths_Italy_M.csv"
    df_Deaths_Italy_M = load_data_ISTAT_Deaths(morti_it_m)
    morti_it_f = DATA_DIR / "Deaths_Italy_F.csv"
    df_Deaths_Italy_F = load_data_ISTAT_Deaths(morti_it_f)
    morti_eu_tot = DATA_DIR / "Deaths_Europe_Tot.csv"
    df_Deaths_Europe_Tot = load_data_EUROSTAT_Deaths(morti_eu_tot)
    morti_eu_m = DATA_DIR / "Deaths_Europe_M.csv"
    df_Deaths_Europe_M = load_data_EUROSTAT_Deaths(morti_eu_m)
    morti_eu_f = DATA_DIR / "Deaths_Europe_F.csv"
    df_Deaths_Europe_F = load_data_EUROSTAT_Deaths(morti_eu_f)
    print("Mortality data loading completed")
    # dividing the dfs per year (2020, 2021, 2022)
    df_it_deaths_2020_Tot, df_it_deaths_2021_Tot, df_it_deaths_2022_Tot = year_subdivision(df_Deaths_Italy_Tot)
    df_it_deaths_2020_M, df_it_deaths_2021_M, df_it_deaths_2022_M = year_subdivision(df_Deaths_Italy_M)
    df_it_deaths_2020_F, df_it_deaths_2021_F, df_it_deaths_2022_F = year_subdivision(df_Deaths_Italy_F)
    df_eu_deaths_2020_Tot, df_eu_deaths_2021_Tot, df_eu_deaths_2022_Tot = year_subdivision(df_Deaths_Europe_Tot)
    df_eu_deaths_2020_M, df_eu_deaths_2021_M, df_eu_deaths_2022_M = year_subdivision(df_Deaths_Europe_M)
    df_eu_deaths_2020_F, df_eu_deaths_2021_F, df_eu_deaths_2022_F = year_subdivision(df_Deaths_Europe_F)
    print("Year subdivision completed")
    # reading the population files and creating the dfs
    Pop_2020_it = DATA_DIR / "Italian_Population_2020.csv"
    df_it_pop_2020_Tot, df_it_pop_2020_M, df_it_pop_2020_F = load_data_ISTAT_Pop(Pop_2020_it)
    Pop_2021_it = DATA_DIR / "Italian_Population_2021.csv"
    df_it_pop_2021_Tot, df_it_pop_2021_M, df_it_pop_2021_F = load_data_ISTAT_Pop(Pop_2021_it)
    Pop_2022_it = DATA_DIR / "Italian_Population_2022.csv"
    df_it_pop_2022_Tot, df_it_pop_2022_M, df_it_pop_2022_F = load_data_ISTAT_Pop(Pop_2022_it)
    Euro_Pop = DATA_DIR / "European_Population.csv"
    df_Tot_eu_2020, df_Tot_eu_2021, df_Tot_eu_2022, df_M_eu_2020, df_M_eu_2021, df_M_eu_2022, df_F_eu_2020, df_F_eu_2021, df_F_eu_2022 = load_data_Eurostat_Pop(Euro_Pop)
    print("Population data loading completed")
    # calulating the raw rates and renaming the age column for the EUROSTAT dfs
    df_ratio_it_2020_Tot = ratio(df_it_deaths_2020_Tot, df_it_pop_2020_Tot)
    df_ratio_it_2021_Tot = ratio(df_it_deaths_2021_Tot, df_it_pop_2021_Tot)
    df_ratio_it_2022_Tot = ratio(df_it_deaths_2022_Tot, df_it_pop_2022_Tot)
    df_ratio_it_2020_M = ratio(df_it_deaths_2020_M, df_it_pop_2020_M)
    df_ratio_it_2021_M = ratio(df_it_deaths_2021_M, df_it_pop_2021_M)
    df_ratio_it_2022_M = ratio(df_it_deaths_2022_M, df_it_pop_2022_M)
    df_ratio_it_2020_F = ratio(df_it_deaths_2020_F, df_it_pop_2020_F)
    df_ratio_it_2021_F = ratio(df_it_deaths_2021_F, df_it_pop_2021_F)
    df_ratio_it_2022_F = ratio(df_it_deaths_2022_F, df_it_pop_2022_F)
    df_ratio_eu_2020_Tot = ratio(df_eu_deaths_2020_Tot, df_Tot_eu_2020)
    df_ratio_eu_2021_Tot = ratio(df_eu_deaths_2021_Tot, df_Tot_eu_2021)
    df_ratio_eu_2022_Tot = ratio(df_eu_deaths_2022_Tot, df_Tot_eu_2022)
    df_ratio_eu_2020_M = ratio(df_eu_deaths_2020_M, df_M_eu_2020)
    df_ratio_eu_2021_M = ratio(df_eu_deaths_2021_M, df_M_eu_2021)
    df_ratio_eu_2022_M = ratio(df_eu_deaths_2022_M, df_M_eu_2022)
    df_ratio_eu_2020_F = ratio(df_eu_deaths_2020_F, df_F_eu_2020)
    df_ratio_eu_2021_F = ratio(df_eu_deaths_2021_F, df_F_eu_2021)
    df_ratio_eu_2022_F = ratio(df_eu_deaths_2022_F, df_F_eu_2022)
    print("Rates calculation completed")
    # reading the ESP2013 population file, used as standard population for the standardization
    Pop_Std = DATA_DIR / "ESP2013.csv"
    df_Pop_Std = load_standard_pop(Pop_Std)
    print("ESP2013 loading completed")
    # standardizing the rates
    df_ratio_std_2020_Tot = expected_deaths_year(df_ratio_it_2020_Tot, df_ratio_eu_2020_Tot, df_Pop_Std)
    df_ratio_std_2021_Tot = expected_deaths_year(df_ratio_it_2021_Tot, df_ratio_eu_2021_Tot, df_Pop_Std)
    df_ratio_std_2022_Tot = expected_deaths_year(df_ratio_it_2022_Tot, df_ratio_eu_2022_Tot, df_Pop_Std)
    df_ratio_std_2020_M = expected_deaths_year(df_ratio_it_2020_M, df_ratio_eu_2020_M, df_Pop_Std)
    df_ratio_std_2021_M = expected_deaths_year(df_ratio_it_2021_M, df_ratio_eu_2021_M, df_Pop_Std)
    df_ratio_std_2022_M = expected_deaths_year(df_ratio_it_2022_M, df_ratio_eu_2022_M, df_Pop_Std)
    df_ratio_std_2020_F = expected_deaths_year(df_ratio_it_2020_F, df_ratio_eu_2020_F, df_Pop_Std)
    df_ratio_std_2021_F = expected_deaths_year(df_ratio_it_2021_F, df_ratio_eu_2021_F, df_Pop_Std)
    df_ratio_std_2022_F = expected_deaths_year(df_ratio_it_2022_F, df_ratio_eu_2022_F, df_Pop_Std)
    print("Expected deaths calculated")
    # collecting the differente dfs and creating the final df, used as results table
    data = [(df_ratio_std_2020_Tot, 2020, "Tot"), 
            (df_ratio_std_2021_Tot, 2021, "Tot"), 
            (df_ratio_std_2022_Tot, 2022, "Tot"), 
            (df_ratio_std_2020_M, 2020, "M"), 
            (df_ratio_std_2021_M, 2021, "M"), 
            (df_ratio_std_2022_M, 2022, "M"), 
            (df_ratio_std_2020_F, 2020, "F"), 
            (df_ratio_std_2021_F, 2021, "F"), 
            (df_ratio_std_2022_F, 2022, "F")]
    collection = [final(df, year, sex) for df, year, sex in data]
    df_final = dataframe_final(collection)
    print("Creation of final dataframe completed")
    # sensitivity analysis
    df_sens_2020_Tot = sensitivity(df_it_deaths_2020_Tot, df_it_pop_2020_Tot, df_eu_deaths_2020_Tot, df_Tot_eu_2020, df_Pop_Std)
    df_sens_2021_Tot = sensitivity(df_it_deaths_2021_Tot, df_it_pop_2021_Tot, df_eu_deaths_2021_Tot, df_Tot_eu_2021, df_Pop_Std)
    df_sens_2022_Tot = sensitivity(df_it_deaths_2022_Tot, df_it_pop_2022_Tot, df_eu_deaths_2022_Tot, df_Tot_eu_2022, df_Pop_Std)
    df_sens_2020_M = sensitivity(df_it_deaths_2020_M, df_it_pop_2020_M, df_eu_deaths_2020_M, df_M_eu_2020, df_Pop_Std)
    df_sens_2021_M = sensitivity(df_it_deaths_2021_M, df_it_pop_2021_M, df_eu_deaths_2021_M, df_M_eu_2021, df_Pop_Std)
    df_sens_2022_M = sensitivity(df_it_deaths_2022_M, df_it_pop_2022_M, df_eu_deaths_2022_M, df_M_eu_2022, df_Pop_Std)
    df_sens_2020_F = sensitivity(df_it_deaths_2020_F, df_it_pop_2020_F, df_eu_deaths_2020_F, df_F_eu_2020, df_Pop_Std)
    df_sens_2021_F = sensitivity(df_it_deaths_2021_F, df_it_pop_2021_F, df_eu_deaths_2021_F, df_F_eu_2021, df_Pop_Std)
    df_sens_2022_F = sensitivity(df_it_deaths_2022_F, df_it_pop_2022_F, df_eu_deaths_2022_F, df_F_eu_2022, df_Pop_Std)
    data_sens = [(df_sens_2020_Tot, 2020, "Tot"), 
            (df_sens_2021_Tot, 2021, "Tot"), 
            (df_sens_2022_Tot, 2022, "Tot"), 
            (df_sens_2020_M, 2020, "M"), 
            (df_sens_2021_M, 2021, "M"), 
            (df_sens_2022_M, 2022, "M"), 
            (df_sens_2020_F, 2020, "F"), 
            (df_sens_2021_F, 2021, "F"), 
            (df_sens_2022_F, 2022, "F")]
    collection_sens = [final_sens(df, year, sex) for df, year, sex in data_sens]
    df_final_sens = dataframe_final_sens(collection_sens)
    print("Sensitivity analysis completed")
    # kitagawa decomposition
    df_kit_2020_Tot = initial_kit(df_ratio_it_2020_Tot, df_ratio_eu_2020_Tot)
    df_kit_2021_Tot = initial_kit(df_ratio_it_2021_Tot, df_ratio_eu_2021_Tot)
    df_kit_2022_Tot = initial_kit(df_ratio_it_2022_Tot, df_ratio_eu_2022_Tot)
    df_kit_2020_M = initial_kit(df_ratio_it_2020_M, df_ratio_eu_2020_M)
    df_kit_2021_M = initial_kit(df_ratio_it_2021_M, df_ratio_eu_2021_M)
    df_kit_2022_M = initial_kit(df_ratio_it_2022_M, df_ratio_eu_2022_M)
    df_kit_2020_F = initial_kit(df_ratio_it_2020_F, df_ratio_eu_2020_F)
    df_kit_2021_F = initial_kit(df_ratio_it_2021_F, df_ratio_eu_2021_F)
    df_kit_2022_F = initial_kit(df_ratio_it_2022_F, df_ratio_eu_2022_F)
    data_kit = [(df_kit_2020_Tot, 2020, "Tot"), 
            (df_kit_2021_Tot, 2021, "Tot"), 
            (df_kit_2022_Tot, 2022, "Tot"), 
            (df_kit_2020_M, 2020, "M"), 
            (df_kit_2021_M, 2021, "M"), 
            (df_kit_2022_M, 2022, "M"), 
            (df_kit_2020_F, 2020, "F"), 
            (df_kit_2021_F, 2021, "F"), 
            (df_kit_2022_F, 2022, "F")]
    collection_kit = [final_kit(df, year, sex) for df, year, sex in data_kit]
    df_final_kit = dataframe_final_kit(collection_kit)
    print("Kitagawa decomposition completed")
    # creating the graphs
    # creation of the "standardized rate: italy vs europe from 2020 to 2022" graph
    graph_1(df_final, save_path= OUTPUT_DIR / "Standardized_rates_Italy_vs_Europe.png")
    print("Graph 1 created, standardized rates: Italy vs Europe")
    # creation of the "raw rates: italy vs europe from 2020 to 2022" graph
    graph_2(df_final, save_path= OUTPUT_DIR / "Raw_rates_Italy_vs_Europe.png")
    print("Graph 2 created, crude rates: Italy vs Europe")
    # creation of the "standardized rates: italy vs europe age distribution" graph
    graph_3(df_ratio_std_2020_Tot, df_ratio_std_2021_Tot, df_ratio_std_2022_Tot, save_path="output/Age_distribution.png")
    print("Graph 3 created, age distribution")
    # creation of the "bar graphs: standardized rates vs raw rates each year in italy and europe" graph
    graph_4(df_final, save_path= OUTPUT_DIR / "Raw_vs_Std.png")
    print("Graph 4 created, standardized rates vs crude rates")
    # creation of the table with the final df with raw and standardized mortality rate per years, sex and country
    table_1(df_final, save_path= OUTPUT_DIR / "Table_Results.png", csv_path= OUTPUT_DIR / "Table_Results.csv")
    print("Table 1 created, standardized and crude rates for Italy and Europe stratified by sex and year")
    # creation of the table with the final df with raw and standardized mortality rate per years, sex and country, for EU and EU without Italy
    table_2(df_final_sens, df_final, save_path= OUTPUT_DIR / "Table_Results_Sens.png", csv_path= OUTPUT_DIR / "Table_Results_Sens.csv")
    print("Table 2 created, sensitivity analysis results")
    # creation of the table with the df for the kitagawa decomposition
    table_3(df_final_kit, save_path= OUTPUT_DIR / "Table_Results_Kit.png", csv_path= OUTPUT_DIR / "Table_Results_Kit.csv")
    print("Table 3 created, Kitagawa decomposition results")
    
if __name__ == "__main__":
    main()
