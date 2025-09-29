# functions to compute standardized mortality rates

import pandas as pd
import numpy as np
from scipy.stats import chi2

def expected_deaths_year(df, df1, df2):
    """
    Function used to merge 3 dfs and to calculate expected deaths and the ratio exp/pop_std
    First it merges the dfs with Italian and European raw rates and then it merges the df created with the df with standard population
    All 3 dfs must have the column Age
    It's used to calculate expected deaths on the standard population, which will be used to calculate the standardized rate
    Return a df with Age, Deaths_It, Total_It, Death_Rate_per_100k_It, Deaths_EU, Total_EU, Death_Rate_per_100k_EU, Exp_Deaths_on_Std_IT, Exp_Deaths_on_Std_EU
    """
    df1 = df1.drop(columns=["Year"], errors="ignore")
    df_merged_df1 = pd.merge(df, df1, how="inner", on="Age")
    assert set(df["Age"]) == set(df1["Age"]), "Ages don't coincides between the dataframes (df and df1)"
    df_ratio_std = pd.merge(df_merged_df1, df2, how="inner", on="Age")
    assert set(df_merged_df1["Age"]) == set(df2["Age"]), "Ages don't coincides between the dataframes (df_merged_df1 and df2)"
    df_ratio_std = df_ratio_std.rename(columns={"Deaths_x": "Deaths_It", "Total_x": "Total_It", "Death_Rate_per_100k_x": "Death_Rate_per_100k_It", 
                                          "Deaths_y": "Deaths_EU", "Total_y": "Total_EU", "Death_Rate_per_100k_y": "Death_Rate_per_100k_EU"
                                          })
    df_ratio_std[["Deaths_It", "Deaths_EU", "Total_It", "Total_EU", "Death_Rate_per_100k_It", "Death_Rate_per_100k_EU"]]=df_ratio_std[["Deaths_It", "Deaths_EU", "Total_It", "Total_EU", "Death_Rate_per_100k_It", "Death_Rate_per_100k_EU"]].apply(pd.to_numeric)
    df_ratio_std["Deaths_It"] = df_ratio_std["Deaths_It"].fillna(0)
    df_ratio_std["Deaths_EU"] = df_ratio_std["Deaths_EU"].fillna(0)
    for column in ["Death_Rate_per_100k_It", "Death_Rate_per_100k_EU", "Pop_Std"]:
      if column not in df_ratio_std.columns:
        raise ValueError(f"Required column missing: {column}")
    df_ratio_std["Exp_Deaths_on_Std_It"] = (df_ratio_std["Death_Rate_per_100k_It"]/100000)*(df_ratio_std["Pop_Std"])
    df_ratio_std["Exp_Deaths_on_Std_EU"] =(df_ratio_std["Death_Rate_per_100k_EU"]/100000)*(df_ratio_std["Pop_Std"])
    df_ratio_std["Ratio_Exp_It_on_Std"] = (df_ratio_std["Exp_Deaths_on_Std_It"]/df_ratio_std["Pop_Std"])
    df_ratio_std["Ratio_Exp_EU_on_Std"] = (df_ratio_std["Exp_Deaths_on_Std_EU"]/df_ratio_std["Pop_Std"])
    return df_ratio_std

def final(df, year, sex, alpha=0.05):
    """
    Function used to calulate Standardized rates and use them to creathe the final df.
    You need a df with the columns Deaths_It, Total_It, Deaths_EU and Total_EU, which will be used to calculate general raw mortality rate.
    The df must also contain the columns Exp_Deaths_on_Std_It, Exp_Deaths_on_Std_EU and Pop_Std, which will be used to calculate standardized rates.
    Returns a dictionary.
    """
    # Calculating the crude rates and lower and upper limits for 95% CIs.
    if df["Total_It"].sum() <= 0:
      raise ValueError("Total_It sum is negative or zero, cannot calculate crude rates")
    rate_raw_it = (df["Deaths_It"].sum()/df["Total_It"].sum())*100000
    lower_count_it = 0.5 * chi2.ppf(alpha/2, 2*(df["Deaths_It"].sum())) if df["Deaths_It"].sum() > 0 else 0.0
    upper_count_it = 0.5 * chi2.ppf(1 - alpha/2, 2*(df["Deaths_It"].sum()+1))
    lower_rate_it = lower_count_it / df["Total_It"].sum() * 100000
    upper_rate_it = upper_count_it / df["Total_It"].sum() * 100000
    if df["Total_EU"].sum() <= 0:
      raise ValueError("Total_EU sum is negative or zero, cannot calculate crude rates")
    rate_raw_eu = (df["Deaths_EU"].sum()/df["Total_EU"].sum())*100000
    lower_count_eu = 0.5 * chi2.ppf(alpha/2, 2*(df["Deaths_EU"].sum())) if df["Deaths_EU"].sum() > 0 else 0.0
    upper_count_eu = 0.5 * chi2.ppf(1 - alpha/2, 2*(df["Deaths_EU"].sum()+1))
    lower_rate_eu = lower_count_eu / df["Total_EU"].sum() * 100000
    upper_rate_eu = upper_count_eu / df["Total_EU"].sum() * 100000
    """
    Calculating standardized rates and 95% CIs using gamma method by Fay & Feuer.
    """
    if df["Pop_Std"].sum() <= 0:
      raise ValueError("Pop_Std sum is negative or zero, cannot calculate standardized rates")
    df["weights"] = df["Pop_Std"]/(df["Pop_Std"].sum())
    rate_std_it = (df["Exp_Deaths_on_Std_It"].sum()/df["Pop_Std"].sum())
    num_it = (np.sum(df["weights"] * (df["Deaths_It"]/df["Total_It"]) ))**2
    den_it = np.sum((df["weights"]**2) * (df["Deaths_It"] / (df["Total_It"]**2)))
    k_it = num_it/den_it if den_it > 0 else 0
    if k_it>0:
        lower_std_it = ((rate_std_it*2*k_it) / ((chi2.ppf(1-(alpha/2), 2*k_it))))
        lower_std_it = lower_std_it*100000
        upper_std_it = ((rate_std_it*2*(k_it+1)) / (chi2.ppf(alpha/2, 2*(k_it+1))))
        upper_std_it = upper_std_it*100000
    else:
        lower_std_it, upper_std_it = 0, 0
    rate_std_eu = (df["Exp_Deaths_on_Std_EU"].sum()/df["Pop_Std"].sum())
    num_eu = (np.sum(df["weights"] * (df["Deaths_EU"]/df["Total_EU"]) ))**2
    den_eu = np.sum((df["weights"]**2) * (df["Deaths_EU"] / (df["Total_EU"]**2)))
    k_eu = num_eu/den_eu if den_eu > 0 else 0
    if k_eu>0:
        lower_std_eu = ((rate_std_eu*2*k_eu) / ((chi2.ppf(1-(alpha/2), 2*k_eu))))
        lower_std_eu = lower_std_eu*100000
        upper_std_eu = ((rate_std_eu*2*(k_eu+1)) / (chi2.ppf(alpha/2, 2*(k_eu+1))))
        upper_std_eu = upper_std_eu*100000
    else:
        lower_std_eu, upper_std_eu = 0, 0
    rate_std_it = rate_std_it*100000
    rate_std_eu = rate_std_eu*100000
    return {"Year": year, "Sex": sex, "Crude It": rate_raw_it, "95% CI lower It Crude": lower_rate_it, "95% CI upper It Crude": upper_rate_it, 
            "Crude EU": rate_raw_eu, "95% CI lower EU Crude": lower_rate_eu, "95% CI upper EU Crude": upper_rate_eu, 
            "Std It": rate_std_it, "95% CI lower It Std": lower_std_it, "95% CI upper It Std": upper_std_it, 
            "Std EU": rate_std_eu, "95% CI lower EU Std": lower_std_eu, "95% CI upper EU Std": upper_std_eu}

def dataframe_final(results):
    """
    From the results of the previous function it returns a df with the crude and standardized rates of Italy and Europe stratified by year and sex.
    """
    df_final = pd.DataFrame(results)
    assert (df_final["Std It"]>=0).all(), "Negative italian standardized rates found"
    assert (df_final["Std EU"]>=0).all(), "Negative european standardized rates found"
    assert (df_final["Crude It"]>=0).all(), "Negative italian crude rates found"
    assert (df_final["Crude EU"]>=0).all(), "Negative european crude rates found"
    return df_final
