# utility functions for loading and saving data
import pandas as pd
# dict used to change the age column for european data
age_conversion_eu = {"Less than 1 year": "0", "From 1 to 4 years": "1-4", "From 5 to 9 years": "5-9", 
                  "From 10 to 14 years": "10-14", "From 15 to 19 years": "15-19", "From 20 to 24 years": "20-24", 
                  "From 25 to 29 years": "25-29", "From 30 to 34 years": "30-34", "From 35 to 39 years": "35-39", 
                  "From 40 to 44 years": "40-44", "From 45 to 49 years": "45-49", "From 50 to 54 years": "50-54", 
                  "From 55 to 59 years": "55-59", "From 60 to 64 years": "60-64", "From 65 to 69 years": "65-69", 
                  "From 70 to 74 years": "70-74", "From 75 to 79 years": "75-79", "From 80 to 84 years": "80-84",
                  "From 85 to 89 years": "85-89", "From 90 to 94 years": "90-94", "95 years or over": "95+"}
# dict used to change the age column for italian data
age_conversion_it = {"0 anni": "0", "1-4 anni": "1-4", "5-9 anni": "5-9", "10-14 anni": "10-14", "15-19 anni": "15-19",
                  "20-24 anni": "20-24", "25-29 anni": "25-29", "30-34 anni": "30-34", "35-39 anni": "35-39",
                  "40-44 anni": "40-44", "45-49 anni": "45-49", "50-54 anni": "50-54", "55-59 anni": "55-59",
                  "60-64 anni": "60-64", "65-69 anni": "65-69", "70-74 anni": "70-74", "75-79 anni": "75-79",
                  "80-84 anni": "80-84", "85-89 anni": "85-89", "90-94 anni": "90-94", "95 anni e più": "95+"}

def rename_age_column(df, type_of_conversion):
    """
    Function used to change the age columns, based on the type of conversion choosed (european or italian)
    The df used must have the column "Age"
    Returns a df
    """
    if "Age" in df.columns:
        df["Age"] = df["Age"].replace(type_of_conversion)
    return df

def load_data_ISTAT_Deaths(Istat_Deaths):
    """
    Function to read ISTAT deaths files.
    The file must contain the Età, TIME_PERIOD and Osservazione columns
    Changes the Age column to simplify the merging of dfs (from "Età" to "Age")
    Returns df with Age, Year and Deaths for Italy
    """
    df = pd.read_csv(Istat_Deaths, usecols=["Età", "TIME_PERIOD", "Osservazione"])
    df = df.rename(columns={"Età": "Age", 
                            "TIME_PERIOD": "Year", 
                            "Osservazione": "Deaths"
                            })
    df[["Year", "Deaths"]]=df[["Year", "Deaths"]].apply(pd.to_numeric)
    df = rename_age_column(df, age_conversion_it)
    assert df["Year"].isin([2020, 2021, 2022]).all(), "Unexpected years found"
    return df

def load_data_EUROSTAT_Deaths(Eurostat_Deaths):
    """
    Function to read Eurostat deaths files.
    The file must contain the Age class, TIME_PERIOD and OBS_VALUE columns
    Returns df with Age, Year and Deaths for Europe
    Changes the Age column to simplify the merging of dfs (from "Age class" to "Age")
    The Eurostat file must have the Age column as "Less than 1 year, From 1 to 4 years, ..., From 90 to 94 years, 95 years and more
    which is the standard description for age classes in Eurostat file. This function changes it to the ISTAT standard
    """
    df = pd.read_csv(Eurostat_Deaths, usecols=["Age class", "TIME_PERIOD", "OBS_VALUE"])
    df = df.rename(columns={"Age class": "Age", 
                            "TIME_PERIOD": "Year", 
                            "OBS_VALUE": "Deaths"
                            })
    df[["Year", "Deaths"]]=df[["Year", "Deaths"]].apply(pd.to_numeric)
    df = rename_age_column(df, age_conversion_eu)
    assert df["Year"].isin([2020, 2021, 2022]).all(), "Unexpected years found"
    return df

def load_standard_pop(std_pop):
    """
    Function used to read the file with the standard population (in this case the ESP2013)
    The file with the standard population must contain 2 columns: Age group and Standard population (ESP2013)
    Changes the Age column to simplify the merging of dfs (from "Age group" to "Age")
    Returns: df with Age and Pop_Std
    """
    df = pd.read_csv(std_pop, sep=";")
    df = df.rename(columns={"Age group": "Age", 
                            "Standard population (ESP2013)": "Pop_Std"})
    assert (df["Pop_Std"]>0).all(), "Found zero or negative population values"
    return df

def year_subdivision(df):
    """
    Function used to divide a df into 3 different dfs, each one with one of the 3 years in study (2020, 2021, 2022)
    The df must have the Year column
    Returns 3 dfs: df_2020, df_2021 and df_2022, each one with the information in the original file, but only for the year specified
    """
    df_2020 = df.loc[df["Year"]==2020]
    df_2021 = df.loc[df["Year"]==2021]
    df_2022 = df.loc[df["Year"]==2022]
    return df_2020, df_2021, df_2022

def load_data_ISTAT_Pop(Istat_Pop):
    """
    Function used to read ISTAT files with the italian population
    Usually ISTAT has files divided by years that's why for ISTAT we have a different function than Eurostat, which has everything togheter
    The file must have the columns Age_Group, Total, Total_M and Total_F
    Changes the Age column to simplify the merging of dfs (from "Age_Group" to "Age")
    Return 3 dfs: df_Tot, df_M and df_F each one with 2 columns, one with Age and one with Population
    """
    df_Tot = pd.read_csv(Istat_Pop, sep=";", usecols=["Age_Group", "Total"])
    df_Tot = df_Tot.rename(columns={"Age_Group": "Age", 
                           "Total": "Total"
                           })
    df_Tot = rename_age_column(df_Tot, age_conversion_it)
    assert (df_Tot["Total"]>=0).all(), "Found zero or negative population values"
    df_M = pd.read_csv(Istat_Pop, sep=";", usecols=["Age_Group", "Total_M"])
    df_M = df_M.rename(columns={"Age_Group": "Age", 
                           "Total_M": "Total"
                           })
    df_M = rename_age_column(df_M, age_conversion_it)
    assert (df_M["Total"]>=0).all(), "Found zero or negative population values"
    df_F = pd.read_csv(Istat_Pop, sep=";", usecols=["Age_Group", "Total_F"])
    df_F = df_F.rename(columns={"Age_Group": "Age", 
                           "Total_F": "Total"
                           })
    df_F = rename_age_column(df_F, age_conversion_it)
    assert (df_F["Total"]>=0).all(), "Found zero or negative population values"
    return df_Tot, df_M, df_F

def load_data_Eurostat_Pop(Eurostat_Pop):
    """
    Function used to read Eurostat files with population
    Eurostat usually has files with both year and sex, so we'll use one function to divide everything in 9 dfs
    The file must contain the columns: Age Group,
                                     Total 2020, Males 2020, Females 2020,
                                     Total 2021, Males 2021, Females 2021,
                                     Total 2022, Males 2022, Females 2022
    Changes the Age column to simplify the merging of dfs (from "Age Group" to "Age")
    Returns 9 dfs: df_Tot_2020, df_Tot_2021, df_Tot_2022,
                  df_M_2020, df_M_2021, df_M_2022,
                  df_F_2020, df_F_2021, df_F_2022
    """
    df_Tot_2020 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Total 2020"])
    df_Tot_2020 = df_Tot_2020.rename(columns={"Age Group": "Age", 
                                "Total 2020": "Total"})
    df_Tot_2020 = rename_age_column(df_Tot_2020, age_conversion_eu)
    assert (df_Tot_2020["Total"]>0).all(), "Found zero or negative population values"
    df_M_2020 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Males 2020"])
    df_M_2020 = df_M_2020.rename(columns={"Age Group": "Age", 
                                "Males 2020": "Total"})
    df_M_2020 = rename_age_column(df_M_2020, age_conversion_eu)
    assert (df_M_2020["Total"]>0).all(), "Found zero or negative population values"
    df_F_2020 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Females 2020"])
    df_F_2020 = df_F_2020.rename(columns={"Age Group": "Age", 
                                "Females 2020": "Total"})
    df_F_2020 = rename_age_column(df_F_2020, age_conversion_eu)
    assert (df_F_2020["Total"]>0).all(), "Found zero or negative population values"
    df_Tot_2021 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Total 2021"])
    df_Tot_2021 = df_Tot_2021.rename(columns={"Age Group": "Age", 
                                "Total 2021": "Total"})
    df_Tot_2021 = rename_age_column(df_Tot_2021, age_conversion_eu)
    assert (df_Tot_2021["Total"]>0).all(), "Found zero or negative population values"
    df_M_2021 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Males 2021"])
    df_M_2021 = df_M_2021.rename(columns={"Age Group": "Age", 
                                "Males 2021": "Total"})
    df_M_2021 = rename_age_column(df_M_2021, age_conversion_eu)
    assert (df_M_2021["Total"]>0).all(), "Found zero or negative population values"
    df_F_2021 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Females 2021"])
    df_F_2021 = df_F_2021.rename(columns={"Age Group": "Age", 
                                "Females 2021": "Total"})
    df_F_2021 = rename_age_column(df_F_2021, age_conversion_eu)
    assert (df_F_2021["Total"]>0).all(), "Found zero or negative population values"
    df_Tot_2022 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Total 2022"])
    df_Tot_2022 = df_Tot_2022.rename(columns={"Age Group": "Age", 
                                "Total 2022": "Total"})
    df_Tot_2022 = rename_age_column(df_Tot_2022, age_conversion_eu)
    assert (df_Tot_2022["Total"]>0).all(), "Found zero or negative population values"
    df_M_2022 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Males 2022"])
    df_M_2022 = df_M_2022.rename(columns={"Age Group": "Age", 
                                "Males 2022": "Total"})
    df_M_2022 = rename_age_column(df_M_2022, age_conversion_eu)
    assert (df_M_2022["Total"]>0).all(), "Found zero or negative population values"
    df_F_2022 = pd.read_csv(Eurostat_Pop, sep=";", usecols=["Age Group", "Females 2022"])
    df_F_2022 = df_F_2022.rename(columns={"Age Group": "Age", 
                                "Females 2022": "Total"})
    df_F_2022 = rename_age_column(df_F_2022, age_conversion_eu)
    assert (df_F_2022["Total"]>0).all(), "Found zero or negative population values"
    return df_Tot_2020, df_Tot_2021, df_Tot_2022, df_M_2020, df_M_2021, df_M_2022, df_F_2020, df_F_2021, df_F_2022
