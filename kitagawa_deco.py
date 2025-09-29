# functions for the kitagawa decomposition

import pandas as pd

def initial_kit(df, df1):
    """
    This function starts the Kitagawa decomposition by merging two dataframes: the firt one with the Italian deaths, population and rates; 
    the second one with the same informations but for Europe.
    Both dataframes must have the following columns: "Age", "Deaths", "Total" and "Death_Rate_per_100k".
    Returns a df with both the "Structure_Effect" and "Rates_Effect" in each age class.
    """
    df_initial_kit = pd.merge(df, df1, how="inner", on="Age")
    assert set(df["Age"]) == set(df1["Age"]), "Ages don't coincides between the dataframes (df and df1)"
    df_initial_kit = df_initial_kit.rename(columns={"Deaths_x": "Deaths_It", "Total_x": "Total_It", "Death_Rate_per_100k_x": "Death_Rate_per_100k_It", 
                                          "Deaths_y": "Deaths_EU", "Total_y": "Total_EU", "Death_Rate_per_100k_y": "Death_Rate_per_100k_EU"
                                          })
    df_initial_kit[["Deaths_It", "Deaths_EU", "Total_It", "Total_EU", "Death_Rate_per_100k_It", "Death_Rate_per_100k_EU"]]=df_initial_kit[["Deaths_It", "Deaths_EU", "Total_It", "Total_EU", "Death_Rate_per_100k_It", "Death_Rate_per_100k_EU"]].apply(pd.to_numeric)
    for column in ["Total_It", "Total_EU", "Death_Rate_per_100k_It", "Death_Rate_per_100k_EU"]:
      if column not in df_initial_kit:
        raise ValueError(f"Required column missing: {column}")
    df_initial_kit["Total_It"] = df_initial_kit["Total_It"].fillna(0)
    df_initial_kit["Total_EU"] = df_initial_kit["Total_EU"].fillna(0)
    if df_initial_kit["Total_It"].sum() <= 0:
      raise ValueError("Total_It sum is negative or zero, cannot calculate proportion")
    if df_initial_kit["Total_EU"].sum() <= 0:
      raise ValueError("Total_EU sum is negative or zero, cannot calculate proportion")
    df_initial_kit["Prop_It"] = df_initial_kit["Total_It"]/(df_initial_kit["Total_It"].sum())
    df_initial_kit["Prop_EU"] = df_initial_kit["Total_EU"]/(df_initial_kit["Total_EU"].sum())
    df_initial_kit["Death_Rate_per_100k_It"] = df_initial_kit["Death_Rate_per_100k_It"]/100000
    df_initial_kit["Death_Rate_per_100k_EU"] = df_initial_kit["Death_Rate_per_100k_EU"]/100000
    df_initial_kit["Structure_Effect"] = (df_initial_kit["Prop_It"] - df_initial_kit["Prop_EU"]) * ((df_initial_kit["Death_Rate_per_100k_It"]+df_initial_kit["Death_Rate_per_100k_EU"])/2)
    df_initial_kit["Rates_Effect"] = (df_initial_kit["Death_Rate_per_100k_It"] - df_initial_kit["Death_Rate_per_100k_EU"]) * ((df_initial_kit["Prop_It"]+df_initial_kit["Prop_EU"])/2)
    return df_initial_kit

def final_kit(df, year, sex):
    """
    Starting from the df of the previous function, it returns a dictionary with the "Year", "Sex", "Effect of Age Structure", "Effect of Rates" and "Difference".
    Initial df must have the following columns: "Structure_Effect" and "Rates_Effect".
    Returns a dictionary.
    """
    structure_effect = (df["Structure_Effect"].sum())*100000
    rates_effect = (df["Rates_Effect"].sum())*100000
    difference = structure_effect + rates_effect
    return {"Year": year, "Sex": sex, "Effect of Age Structure": structure_effect, "Effect of Rates": rates_effect, "Difference": difference}

def dataframe_final_kit(results):
    """
    It creates a df from the results of the previous function.
    """
    df_final_kit = pd.DataFrame(results)
    return df_final_kit
