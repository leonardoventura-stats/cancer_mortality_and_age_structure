# functions for the sensitivity analysis, comparing Italy to EU-27 (without Italy)

import pandas as pd
import numpy as np
from scipy.stats import chi2

def sensitivity(df, df1, df2, df3, df_pop_std):
    """
    Function used to merge 4 dfs and to calculate expected deaths for Europe without Italy.
    First it merges the dfs with Italian data, then it merges the df with the european data
    In the end it merges the two new dataframes
    All 4 dfs must have the column Age
    Return a df with Age, Deaths_It, Total_It, Deaths_EU, Total_EU, Deaths_EU_no_It, Total_EU_no_It, Raw_rate_EU_no_It, Exp_Deaths_EU_no_It
    """
    # Creating a df with Age, Deaths_It, Total_It with Deaths and Total referring to Italy.
    df_part1 = pd.merge(df, df1, on="Age", how = "inner")
    assert set(df["Age"]) == set(df1["Age"]), "Ages don't coincides between the dataframes (df and df1)"
    df_part1 = df_part1.rename(columns={"Deaths": "Deaths_It", "Total": "Total_It"})
    # Creating a df with Age, Deaths_EU, Total_EU with Deaths and Total referring to Europe.
    df_part2 = pd.merge(df2, df3, on="Age", how = "inner")
    df_part2 = df_part2.rename(columns={"Deaths": "Deaths_EU", "Total": "Total_EU"})
    assert set(df2["Age"]) == set(df3["Age"]), "Ages don't coincides between the dataframes (df2 and df3)"
    # Creating a new df with deaths and population of Europe without Italy and it calculate expected deaths of Europe without Italy on the standard population.
    df_sensitivity = pd.merge(df_part1, df_part2, how="inner", on="Age")
    assert set(df_part1["Age"]) == set(df_part2["Age"]), "Ages don't coincides between the dataframes (df_part1 and df_part2)"
    df_sensitivity["Deaths_It"] = df_sensitivity["Deaths_It"].fillna(0)
    df_sensitivity["Deaths_EU"] = df_sensitivity["Deaths_EU"].fillna(0)
    df_sensitivity[["Deaths_It", "Deaths_EU", "Total_It", "Total_EU"]]=df_sensitivity[["Deaths_It", "Deaths_EU", "Total_It", "Total_EU"]].apply(pd.to_numeric)
    for column in ["Deaths_It", "Deaths_EU", "Total_It", "Total_EU"]:
      if column not in df_sensitivity:
        raise ValueError(f"Required column missing: {column}")
    df_sensitivity["Deaths_EU_no_It"] = df_sensitivity["Deaths_EU"] - df_sensitivity["Deaths_It"]
    df_sensitivity["Total_EU_no_It"] = df_sensitivity["Total_EU"] - df_sensitivity["Total_It"]
    assert not (df_sensitivity["Deaths_EU_no_It"]<0).any(), "Negative Deaths after subtraction EU-It"
    assert not (df_sensitivity["Total_EU_no_It"]<0).any(),"Negative Population after subtraction EU-It"
    df_sensitivity["Raw_rate_EU_no_It"] = (df_sensitivity["Deaths_EU_no_It"]/df_sensitivity["Total_EU_no_It"])*100000
    df_sens_std = pd.merge(df_sensitivity, df_pop_std, how="inner", on="Age")
    df_sens_std["Exp_Deaths_EU_no_It"] = (df_sens_std["Raw_rate_EU_no_It"]/100000) * df_sens_std["Pop_Std"]
    return df_sens_std

def final_sens(df, year, sex, alpha=0.05):
    """
    Function used to calulate Standardized rates and use them to creathe the final df for the sensitivity analysis
    You need a df with the columns Deaths_It, Total_It, Deaths_EU, Total_EU, Deaths_EU_no_It and Total_EU_no_It which will be used to calculate general raw mortality rate
    The df must also contain the columns Exp_Deaths_EU_no_It, Pop_Std, which will be used to calculate standardized rates
    Returns a dictionary.
    """
    if df["Total_EU_no_It"].sum() <= 0:
      raise ValueError("Total_EU_no_It sum is negative or zero, cannot calculate crude rates")
    rate_raw_eu_no_it = (df["Deaths_EU_no_It"].sum()/df["Total_EU_no_It"].sum())*100000
    lower_count_eu_no_it = 0.5 * chi2.ppf(alpha/2, 2*(df["Deaths_EU_no_It"].sum())) if df["Deaths_EU_no_It"].sum() > 0 else 0.0
    upper_count_eu_no_it = 0.5 * chi2.ppf(1 - alpha/2, 2*(df["Deaths_EU_no_It"].sum()+1))
    lower_rate_eu_no_it = lower_count_eu_no_it / df["Total_EU_no_It"].sum() * 100000
    upper_rate_eu_no_it = upper_count_eu_no_it / df["Total_EU_no_It"].sum() * 100000
    # Calculating standardized rates and 95% CIs.
    if df["Pop_Std"].sum() <= 0:
      raise ValueError("Pop_Std sum is negative or zero, cannot calculate standardize rates")
    df["weights"] = df["Pop_Std"]/(df["Pop_Std"].sum())
    rate_std_eu_no_it = (df["Exp_Deaths_EU_no_It"].sum()/df["Pop_Std"].sum())
    num_eu_no_it = (np.sum(df["weights"] * (df["Deaths_EU_no_It"]/df["Total_EU_no_It"]) ))**2
    den_eu_no_it = np.sum((df["weights"]**2) * (df["Deaths_EU_no_It"] / (df["Total_EU_no_It"]**2)))
    k = num_eu_no_it/den_eu_no_it if den_eu_no_it > 0 else 0
    if k>0:
        lower_std_eu_no_it = ((rate_std_eu_no_it*2*k) / ((chi2.ppf(1-(alpha/2), 2*k))))
        lower_std_eu_no_it = lower_std_eu_no_it*100000
        upper_std_eu_no_it = ((rate_std_eu_no_it*2*(k+1)) / (chi2.ppf(alpha/2, 2*(k+1))))
        upper_std_eu_no_it = upper_std_eu_no_it*100000
    else:
        lower_std_eu_no_it, upper_std_eu_no_it = 0, 0
    rate_std_eu_no_it = rate_std_eu_no_it*100000

    return {"Year": year, "Sex": sex, "Crude EU-It": rate_raw_eu_no_it, "95% CI lower EU-It Crude": lower_rate_eu_no_it, "95% CI upper EU-It Crude": upper_rate_eu_no_it, 
            "Std EU-It": rate_std_eu_no_it, "95% CI lower EU-It Std": lower_std_eu_no_it, "95% CI upper EU-It Std": upper_std_eu_no_it}

def dataframe_final_sens(results):
    """
    From the results of the previous function it returns a df with the sensitivity analysis (crude and standardized rates for EU and EU without Italy stratified by sex and year)
    """
    df_final_sens = pd.DataFrame(results)
    assert (df_final_sens["Crude EU-It"]>=0).all(), "Negative Europe-Italy crude rates found"
    assert (df_final_sens["Std EU-It"]>=0).all(), "Negative Europe-Italy standardized rates found"
    return df_final_sens
