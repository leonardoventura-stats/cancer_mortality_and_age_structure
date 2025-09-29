# functions to compute crude mortality rates

import pandas as pd

def ratio(df, df2):
    """
    Function used to merge 2 dfs and to calculate the death ratio
    Both dfs must contain the column Age
    df must contain the column Deaths (with number of deaths per age class)
    df2 must contain the column Total (with total population per age class)
    Return a df with Age, Deaths, Total and Death_Rate_per_100k
    """
    df_ratio = pd.merge(df, df2, how="inner", on="Age")
    df_ratio["Deaths"] = df_ratio["Deaths"].fillna(0)
    df_ratio.loc[df_ratio["Total"] == 0, "Death_Rate_per_100k"] = pd.NA
    df_ratio.loc[df_ratio["Total"] > 0, "Death_Rate_per_100k"] = (df_ratio["Deaths"]/df_ratio["Total"])*100000
    assert set(df["Age"]) == set(df2["Age"]), "Ages don't coincides between the dataframes"
    assert (df_ratio["Deaths"]<=df_ratio["Total"]).all(), "Deaths exceed population"
    assert (df_ratio["Death_Rate_per_100k"]>=0).all(), "Negative raw rates found"
    return df_ratio
