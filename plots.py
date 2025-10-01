# functions to create plots for the paper

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Creating the graphs
"""
def graph_1(df, save_path=None):
    """
    Graph 1 - standardized rates: italy vs europe from 2020 to 2022.
    """
    df_final_m = df.loc[df["Sex"]== "M"]
    df_final_f = df.loc[df["Sex"]== "F"]
    years = sorted(df_final_m["Year"].unique())
    rate_std_it_m = df_final_m["Std It"].values.tolist()
    rate_std_it_f = df_final_f["Std It"].values.tolist()
    rate_std_eu_m = df_final_m["Std EU"].values.tolist()
    rate_std_eu_f = df_final_f["Std EU"].values.tolist()
    for column in ["Year", "Sex", "Std It", "Std EU", "95% CI lower It Std", "95% CI upper It Std", "95% CI lower EU Std", "95% CI upper EU Std"]:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")
    for column in ["Std It", "Std EU", "95% CI lower It Std", "95% CI upper It Std", "95% CI lower EU Std", "95% CI upper EU Std"]:
        assert (df[column]>=0).all(), f"Negative values found: {column}"
    assert (df["95% CI lower It Std"] <= df["Std It"]).all(), "Lower CI bigger than Std It"
    assert (df["95% CI lower EU Std"] <= df["Std EU"]).all(), "Lower CI bigger than Std EU"
    assert (df["95% CI upper It Std"] >= df["Std It"]).all(), "Upper CI lower than Std It"
    assert (df["95% CI upper EU Std"] >= df["Std EU"]).all(), "Upper CI lower than Std EU"
    assert set(df_final_m["Year"].unique()) == set(df_final_f["Year"].unique()), "Differente years between males and females"
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(years, rate_std_it_m, label = "Italy-M", marker=".", yerr=[df_final_m["Std It"] - df_final_m["95% CI lower It Std"], df_final_m["95% CI upper It Std"] - df_final_m["Std It"]], capsize=5)
    ax.errorbar(years, rate_std_it_f, label = "Italy-F", marker=".", yerr=[df_final_f["Std It"] - df_final_f["95% CI lower It Std"], df_final_f["95% CI upper It Std"] - df_final_f["Std It"]], capsize=5)
    ax.errorbar(years, rate_std_eu_m, label = "Europe-M", marker=".", yerr=[df_final_m["Std EU"] - df_final_m["95% CI lower EU Std"], df_final_m["95% CI upper EU Std"] - df_final_m["Std EU"]], capsize=5)
    ax.errorbar(years, rate_std_eu_f, label = "Europe-F", marker=".", yerr=[df_final_f["Std EU"] - df_final_f["95% CI lower EU Std"], df_final_f["95% CI upper EU Std"] - df_final_f["Std EU"]], capsize=5)
    ax.set_xticks(years)
    ax.set_xticklabels(years)
    ax.set_xlabel("Year")
    ax.set_ylabel("Standardized rate (per 100.000)")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.5)
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)

def graph_2(df, save_path=None):
    """
    Graph 2 - raw rates: italy vs europe from 2020 to 2022.
    """
    df_final_m = df.loc[df["Sex"] == "M"]
    df_final_f = df.loc[df["Sex"] == "F"]
    years = sorted(df_final_m["Year"].unique())
    rate_raw_it_m = df_final_m["Crude It"].values.tolist()
    rate_raw_it_f = df_final_f["Crude It"].values.tolist()
    rate_raw_eu_m = df_final_m["Crude EU"].values.tolist()
    rate_raw_eu_f = df_final_f["Crude EU"].values.tolist()
    for column in ["Year", "Sex", "Crude It", "Crude EU", "95% CI lower It Crude", "95% CI upper It Crude", "95% CI lower EU Crude", "95% CI upper EU Crude"]:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")
    for column in ["Crude It", "Crude EU", "95% CI lower It Crude", "95% CI upper It Crude", "95% CI lower EU Crude", "95% CI upper EU Crude"]:
        assert (df[column]>=0).all(), f"Negative values found: {column}"
    assert (df["95% CI lower It Crude"] <= df["Crude It"]).all(), "Lower CI bigger than Crude It"
    assert (df["95% CI lower EU Crude"] <= df["Crude EU"]).all(), "Lower CI bigger than Crude EU"
    assert (df["95% CI upper It Crude"] >= df["Crude It"]).all(), "Upper CI lower than Crude It"
    assert (df["95% CI upper EU Crude"] >= df["Crude EU"]).all(), "Upper CI lower than Crude EU"
    assert set(df_final_m["Year"].unique()) == set(df_final_f["Year"].unique()), "Differente years between males and females"
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(years, rate_raw_it_m, label = "Italy-M", marker=".", yerr=[df_final_m["Crude It"] - df_final_m["95% CI lower It Crude"], df_final_m["95% CI upper It Crude"] - df_final_m["Crude It"]], capsize=5)
    ax.errorbar(years, rate_raw_it_f, label = "Italy-F", marker=".", yerr=[df_final_f["Crude It"] - df_final_f["95% CI lower It Crude"], df_final_f["95% CI upper It Crude"] - df_final_f["Crude It"]], capsize=5)
    ax.errorbar(years, rate_raw_eu_m, label = "Europe-M", marker=".", yerr=[df_final_m["Crude EU"] - df_final_m["95% CI lower EU Crude"], df_final_m["95% CI upper EU Crude"] - df_final_m["Crude EU"]], capsize=5)
    ax.errorbar(years, rate_raw_eu_f, label = "Europe-F", marker=".", yerr=[df_final_f["Crude EU"] - df_final_f["95% CI lower EU Crude"], df_final_f["95% CI upper EU Crude"] - df_final_f["Crude EU"]], capsize=5)
    ax.set_xticks(years)
    ax.set_xticklabels(years)
    ax.set_xlabel("Year")
    ax.set_ylabel("Crude rate (per 100.000)")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.5)
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)

def graph_3(df, df1, df2, save_path=None):
    """
    Graph 3 - standardized rates: italy vs europe age distribution.
    """
    ratio_it_tot_2020 = df["Ratio_Exp_It_on_Std"].values.tolist()
    ratio_eu_tot_2020 = df["Ratio_Exp_EU_on_Std"].values.tolist()
    ratio_it_tot_2021 = df1["Ratio_Exp_It_on_Std"].values.tolist()
    ratio_eu_tot_2021 = df1["Ratio_Exp_EU_on_Std"].values.tolist()
    ratio_it_tot_2022 = df2["Ratio_Exp_It_on_Std"].values.tolist()
    ratio_eu_tot_2022 = df2["Ratio_Exp_EU_on_Std"].values.tolist()
    ages = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    for column in ["Age", "Year", "Ratio_Exp_It_on_Std", "Ratio_Exp_EU_on_Std"]:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")
    for column in ["Ratio_Exp_It_on_Std", "Ratio_Exp_EU_on_Std"]:
        assert (df[column]>=0).all(), f"Negative rates found: {column}"
    fig, axs = plt.subplots(1, 3, figsize=(20, 8))
    axs[0].plot(ratio_it_tot_2020, label="Italy")
    axs[0].plot(ratio_eu_tot_2020, label="Europe")
    axs[0].set_xticks(np.arange(len(ages)))
    axs[0].set_xticklabels(ages)
    axs[0].set_xlabel("Age")
    axs[0].set_ylabel("Age-Specific rate")
    axs[0].set_title("2020")
    axs[0].legend(loc="upper left", fontsize=9, framealpha=0.5)
    axs[1].plot(ratio_it_tot_2021, label="Italy")
    axs[1].plot(ratio_eu_tot_2021, label="Europe")
    axs[1].set_xticks(np.arange(len(ages)))
    axs[1].set_xticklabels(ages)
    axs[1].set_xlabel("Age")
    axs[1].set_ylabel("Age-Specific rate")
    axs[1].set_title("2021")
    axs[1].legend(loc="upper left", fontsize=9, framealpha=0.5)
    axs[2].plot(ratio_it_tot_2022, label="Italy")
    axs[2].plot(ratio_eu_tot_2022, label="Europe")
    axs[2].set_xticks(np.arange(len(ages)))
    axs[2].set_xticklabels(ages)
    axs[2].set_xlabel("Age")
    axs[2].set_ylabel("Age-Specific rate")
    axs[2].set_title("2022")
    axs[2].legend(loc="upper left", fontsize=9, framealpha=0.5)
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)

def graph_4(df, save_path=None):
    """
    Graph 4 - bar graphs: standardized rates vs raw rates each year in Italy and Europe.
    """
    df_final_tot = df.loc[df["Sex"] == "Tot"]
    df_final_tot_2020 = df_final_tot.loc[df_final_tot["Year"] == 2020]
    df_final_tot_2021 = df_final_tot.loc[df_final_tot["Year"] == 2021]
    df_final_tot_2022 = df_final_tot.loc[df_final_tot["Year"] == 2022]
    rate_raw_it_2020 = float(df_final_tot_2020["Crude It"].iloc[0])
    rate_raw_it_2021 = float(df_final_tot_2021["Crude It"].iloc[0])
    rate_raw_it_2022 = float(df_final_tot_2022["Crude It"].iloc[0])
    rate_std_it_2020 = float(df_final_tot_2020["Std It"].iloc[0])
    rate_std_it_2021 = float(df_final_tot_2021["Std It"].iloc[0])
    rate_std_it_2022 = float(df_final_tot_2022["Std It"].iloc[0])
    rate_raw_eu_2020 = float(df_final_tot_2020["Crude EU"].iloc[0])
    rate_raw_eu_2021 = float(df_final_tot_2021["Crude EU"].iloc[0])
    rate_raw_eu_2022 = float(df_final_tot_2022["Crude EU"].iloc[0])
    rate_std_eu_2020 = float(df_final_tot_2020["Std EU"].iloc[0])
    rate_std_eu_2021 = float(df_final_tot_2021["Std EU"].iloc[0])
    rate_std_eu_2022 = float(df_final_tot_2022["Std EU"].iloc[0])
    years = df_final_tot["Year"].values.tolist()
    italy = {"Raw Rate": [rate_raw_it_2020, rate_raw_it_2021, rate_raw_it_2022], "Standardized Rate": [rate_std_it_2020, rate_std_it_2021, rate_std_it_2022]}
    europe = {"Raw Rate": [rate_raw_eu_2020, rate_raw_eu_2021, rate_raw_eu_2022], "Standardized Rate": [rate_std_eu_2020, rate_std_eu_2021, rate_std_eu_2022]}
    df_italy = pd.DataFrame(data=italy)
    df_europe = pd.DataFrame(data=europe)
    fig, axs = plt.subplots(1, 2, figsize=(20, 8), layout="constrained")
    section = np.arange(len(years))
    width = 0.25
    shift = 0
    for attribute, measurment in df_italy.items():
        if attribute == "Raw Rate":
            lower = df_final_tot.loc[df_final_tot["Year"].isin(years), "95% CI lower It Crude"].values
            upper = df_final_tot.loc[df_final_tot["Year"].isin(years), "95% CI upper It Crude"].values
        else:
            lower = df_final_tot.loc[df_final_tot["Year"].isin(years), "95% CI lower It Std"].values
            upper = df_final_tot.loc[df_final_tot["Year"].isin(years), "95% CI upper It Std"].values
        error_lower = measurment - lower
        error_upper = upper - measurment
        errors = [error_lower, error_upper]
        offset = width*shift
        rects = axs[0].bar(section + offset, measurment, width, label=attribute, yerr=errors, capsize=5)
        axs[0].bar_label(rects, padding=3)
        shift += 1
    axs[0].set_xlabel("Year")
    axs[0].set_ylabel("Rate")
    axs[0].set_title("Italy")
    axs[0].set_xticks(section + width/2, years)
    axs[0].legend(loc="upper right")
    shift = 0
    for attribute, measurment in df_europe.items():
        if attribute == "Raw Rate":
            lower = df_final_tot.loc[df_final_tot["Year"].isin(years), "95% CI lower EU Crude"].values
            upper = df_final_tot.loc[df_final_tot["Year"].isin(years), "95% CI upper EU Crude"].values
        else:
            lower = df_final_tot.loc[df_final_tot["Year"].isin(years), "95% CI lower EU Std"].values
            upper = df_final_tot.loc[df_final_tot["Year"].isin(years), "95% CI upper EU Std"].values
        error_lower = measurment - lower
        error_upper = upper - measurment
        errors = [error_lower, error_upper]
        offset2 = width*shift
        rects = axs[1].bar(section + offset2, measurment, width, label=attribute, yerr=errors, capsize=5)
        axs[1].bar_label(rects, padding=3)
        shift += 1
    axs[1].set_xlabel("Year")
    axs[1].set_ylabel("Rate")
    axs[1].set_title("Europe")
    axs[1].set_xticks(section + width/2, years)
    axs[1].legend(loc="upper right")
    if save_path:
        fig.savefig(save_path, dpi=300)
    plt.close(fig)

def table_1(df, save_path=None, csv_path=None):
    """
    Table 1 - raw and standardized mortality rate per years, sex and country.
    """
    df["Crude It"] = df["Crude It"].round(2)
    df["Std It"] = df["Std It"].round(2)
    df["Crude EU"] = df["Crude EU"].round(2)
    df["Std EU"] = df["Std EU"].round(2)
    df["95% CI lower It Crude"] = df["95% CI lower It Crude"].round(2)
    df["95% CI lower EU Crude"] = df["95% CI lower EU Crude"].round(2)
    df["95% CI lower It Std"] = df["95% CI lower It Std"].round(2)
    df["95% CI lower EU Std"] = df["95% CI lower EU Std"].round(2)
    df["95% CI upper It Crude"] = df["95% CI upper It Crude"].round(2)
    df["95% CI upper EU Crude"] = df["95% CI upper EU Crude"].round(2)
    df["95% CI upper It Std"] = df["95% CI upper It Std"].round(2)
    df["95% CI upper EU Std"] = df["95% CI upper EU Std"].round(2)
    base_table = {"Year": df["Year"], "Sex": df["Sex"], 
                  "Crude Rate It (95% CI)": df["Crude It"].astype(str)+" ("+df["95% CI lower It Crude"].astype(str)+"-"+df["95% CI upper It Crude"].astype(str)+")", 
                  "Crude Rate EU (95% CI)": df["Crude EU"].astype(str)+" ("+df["95% CI lower EU Crude"].astype(str)+"-"+df["95% CI upper EU Crude"].astype(str)+")",
                  "Std Rate It (95% CI)": df["Std It"].astype(str) + " ("+df["95% CI lower It Std"].astype(str) + "-"+ df["95% CI upper It Std"].astype(str) + ")",
                  "Std Rate EU (95% CI)": df["Std EU"].astype(str)+" ("+df["95% CI lower EU Std"].astype(str)+"-"+df["95% CI upper EU Std"].astype(str)+")"}
    df_table = pd.DataFrame(base_table)
    for column in ["Year", "Sex", "Std It", "Std EU", "Crude It", "Crude EU", "95% CI lower It Std", "95% CI upper It Std", "95% CI lower EU Std", "95% CI upper EU Std", "95% CI lower It Crude", "95% CI upper It Crude", "95% CI lower EU Crude", "95% CI upper EU Crude"]:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")
    for column in ["Std It", "Std EU", "Crude It", "Crude EU", "95% CI lower It Std", "95% CI upper It Std", "95% CI lower EU Std", "95% CI upper EU Std", "95% CI lower It Crude", "95% CI upper It Crude", "95% CI lower EU Crude", "95% CI upper EU Crude"]:
        assert (df[column]>=0).all(), f"Negative values found: {column}"
    assert (df["95% CI lower It Std"] <= df["Std It"]).all(), "Lower CI bigger than Std It"
    assert (df["95% CI lower EU Std"] <= df["Std EU"]).all(), "Lower CI bigger than Std EU"
    assert (df["95% CI upper It Std"] >= df["Std It"]).all(), "Upper CI lower than Std It"
    assert (df["95% CI upper EU Std"] >= df["Std EU"]).all(), "Upper CI lower than Std EU"
    assert (df["95% CI lower It Crude"] <= df["Crude It"]).all(), "Lower CI bigger than Crude It"
    assert (df["95% CI lower EU Crude"] <= df["Crude EU"]).all(), "Lower CI bigger than Crude EU"
    assert (df["95% CI upper It Crude"] >= df["Crude It"]).all(), "Upper CI lower than Crude It"
    assert (df["95% CI upper EU Crude"] >= df["Crude EU"]).all(), "Upper CI lower than Crude EU"
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    table = ax.table(cellText=df_table.values, colLabels=df_table.columns, loc="center", cellLoc="center")
    table.scale(1.25, 1)
    cellDict=table.get_celld()
    numbers = range(10)
    for i in numbers:
        cellDict[(i,0)].set_width(0.075)
        cellDict[(i, 1)].set_width(0.05)
        cellDict[(i,2)].set_width(0.225)
        cellDict[(i, 3)].set_width(0.225)
        cellDict[(i,4)].set_width(0.225)
        cellDict[(i,5)].set_width(0.225)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for key, cell in table.get_celld().items():
        if key[0]==0:
            cell.set_fontsize(10)
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#f0f0f0")
    plt.title("Raw and standardized mortality rates (per 100.000)", loc="center")
    if save_path:
        fig.savefig(save_path, dpi=300)
    if csv_path:
        df_table.to_csv(csv_path, index=False)
    plt.close(fig)

def table_2(df, df1, save_path=None, csv_path=None):
    """
    Table 2 - raw and standardized mortality rate per years, sex and country for the sensitivity analysis.
    """
    df["Crude EU-It"] = df["Crude EU-It"].round(2)
    df["Std EU-It"] = df["Std EU-It"].round(2)
    df1["Crude EU"] = df1["Crude EU"].round(2)
    df1["Std EU"] = df1["Std EU"].round(2)
    df["95% CI lower EU-It Crude"] = df["95% CI lower EU-It Crude"].round(2)
    df1["95% CI lower EU Crude"] = df1["95% CI lower EU Crude"].round(2)
    df["95% CI lower EU-It Std"] = df["95% CI lower EU-It Std"].round(2)
    df1["95% CI lower EU Std"] = df1["95% CI lower EU Std"].round(2)
    df["95% CI upper EU-It Crude"] = df["95% CI upper EU-It Crude"].round(2)
    df1["95% CI upper EU Crude"] = df1["95% CI upper EU Crude"].round(2)
    df["95% CI upper EU-It Std"] = df["95% CI upper EU-It Std"].round(2)
    df1["95% CI upper EU Std"] = df1["95% CI upper EU Std"].round(2)
    base_table = {"Year": df["Year"], "Sex": df["Sex"], 
                  "Crude Rate EU (95% CI)": df1["Crude EU"].astype(str)+" ("+df1["95% CI lower EU Crude"].astype(str)+"-"+df1["95% CI upper EU Crude"].astype(str)+")", 
                  "Crude Rate EU-It (95% CI)": df["Crude EU-It"].astype(str)+" ("+df["95% CI lower EU-It Crude"].astype(str)+"-"+df["95% CI upper EU-It Crude"].astype(str)+")",
                  "Std Rate EU (95% CI)": df1["Std EU"].astype(str) + " ("+df1["95% CI lower EU Std"].astype(str) + "-"+ df1["95% CI upper EU Std"].astype(str) + ")",
                  "Std Rate EU-It (95% CI)": df["Std EU-It"].astype(str)+" ("+df["95% CI lower EU-It Std"].astype(str)+"-"+df["95% CI upper EU-It Std"].astype(str)+")"}
    df_table = pd.DataFrame(base_table)
    for column in ["Year", "Sex", "Crude Rate EU (95% CI)", "Crude Rate EU-It (95% CI)", "Std Rate EU (95% CI)", "Std Rate EU-It (95% CI)"]:
        if column not in df_table.columns:
            raise ValueError(f"Required column missing: {column}")
    for column in ["Std EU-It", "Crude EU-It", "95% CI lower EU-It Std", "95% CI upper EU-It Std", "95% CI lower EU-It Crude", "95% CI upper EU-It Crude"]:
        assert (df[column]>=0).all(), f"Negative values found: {column}"
    for column in ["Std EU", "Crude EU", "95% CI lower EU Std", "95% CI upper EU Std", "95% CI lower EU Crude", "95% CI upper EU Crude"]:
        assert (df1[column]>=0).all(), f"Negative values found: {column}"
    assert (df1["95% CI lower EU Std"] <= df1["Std EU"]).all(), "Lower CI bigger than Std EU"
    assert (df["95% CI lower EU-It Std"] <= df["Std EU-It"]).all(), "Lower CI bigger than Std EU-It"
    assert (df1["95% CI upper EU Std"] >= df1["Std EU"]).all(), "Upper CI lower than Std EU"
    assert (df["95% CI upper EU-It Std"] >= df["Std EU-It"]).all(), "Upper CI lower than Std EU-It"
    assert (df1["95% CI lower EU Crude"] <= df1["Crude EU"]).all(), "Lower CI bigger than Crude EU"
    assert (df["95% CI lower EU-It Crude"] <= df["Crude EU-It"]).all(), "Lower CI bigger than Crude EU-It"
    assert (df1["95% CI upper EU Crude"] >= df1["Crude EU"]).all(), "Upper CI lower than Crude EU"
    assert (df["95% CI upper EU-It Crude"] >= df["Crude EU-It"]).all(), "Upper CI lower than Crude EU-It"
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    table = ax.table(cellText=df_table.values, colLabels=df_table.columns, loc="center", cellLoc="center")
    table.scale(1.25, 1)
    cellDict=table.get_celld()
    numbers = range(10)
    for i in numbers:
        cellDict[(i,0)].set_width(0.075)
        cellDict[(i, 1)].set_width(0.05)
        cellDict[(i,2)].set_width(0.225)
        cellDict[(i, 3)].set_width(0.225)
        cellDict[(i,4)].set_width(0.225)
        cellDict[(i,5)].set_width(0.225)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for key, cell in table.get_celld().items():
        if key[0]==0:
            cell.set_fontsize(10)
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#f0f0f0")
    plt.title("Raw and standardized mortality rates (per 100.000)", loc="center")
    if save_path:
        fig.savefig(save_path, dpi=300)
    if csv_path:
        df_table.to_csv(csv_path, index=False)
    plt.close(fig)

def table_3(df, save_path=None, csv_path=None):
    """
    Table 3 - values of the Kitagawa decomposition.
    """
    df["Effect of Age Structure"] = df["Effect of Age Structure"].round(2)
    df["Effect of Rates"] = df['Effect of Rates'].round(2)
    df["Difference"] = df["Difference"].round(2)
    for column in ["Year", "Sex", "Effect of Age Structure", "Effect of Rates", "Difference"]:
        if column not in df.columns:
            raise ValueError(f"Required column missing: {column}")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    table = ax.table(cellText=df.values, colLabels=df.columns, loc="center", cellLoc="center")
    table.scale(1.25, 1)
    cellDict=table.get_celld()
    numbers = range(10)
    for i in numbers:
        cellDict[(i,0)].set_width(0.075)
        cellDict[(i, 1)].set_width(0.05)
        cellDict[(i,2)].set_width(0.225)
        cellDict[(i, 3)].set_width(0.225)
        cellDict[(i,4)].set_width(0.225)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for key, cell in table.get_celld().items():
        if key[0]==0:
            cell.set_fontsize(10)
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#f0f0f0")
    if save_path:
        fig.savefig(save_path, dpi=300)
    if csv_path:
        df_table = pd.DataFrame(df)
        df_table.to_csv(csv_path, index=False)
    plt.close(fig)
