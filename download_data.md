Script to download the required dataset and save them in the folder data/.
> Neither ISTAT nor Eurostat provide direct download links, you must manually filter and export data as explained below.

## ISTAT - Mortality
[ISTAT Mortality Data](https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0810HEA,1.0/HEA_DEATH/DCIS_CMORTE1_EV/IT1,39_493_DF_DCIS_CMORTE1_EV_2,1.0)
Accessed on September 2025.

Follow these steps to correctly download the ISTAT Mortality data:
1. go to the URL above;
2. select "Criteri";
3. "Territorio" --> select "[IT] Italia";
4. "Età" --> click on "Seleziona tutto" and then remove "[NSP] non indicato" and "[TOTAL] totale";
5. "Sesso" --> click on "Seleziona tutto"
6. "Causa iniziale di morte - European Short List" --> select "[2_1] tumori maligni";
7. "Tempo" --> click on "Seleziona" and select "Range personalizzato" then change "Inizio" to 2020 and "Fine" to 2022;
8. click on "Applica";
9. Select "Total" and download the file as CSV as "data/Deaths_Italy_Tot.csv" using "," as separator;
10. change "Sesso" to "Maschi" and download the file as CSV as "data/Deaths_Italy_M.csv" using "," as separator;
11. change "Sesso" to "Femmine" and download the file as CSV as "data/Deaths_Italy_F.csv" using "," as separator.

## ISTAT - Population
[ISTAT 2020 Population](https://demo.istat.it/app/?l=it&a=2020&i=POS)
Accessed on September 2025.
Save as "data/Italian_Population_2020.csv"
Using ";" as separator.

[ISTAT 2021 population](https://demo.istat.it/app/?l=it&a=2021&i=POS)
Accessed on September 2025.
Save as "data/Italian_Population_2021.csv"
Using ";" as separator.

[2022 population](https://demo.istat.it/app/?l=it&a=2022&i=POS)
Accessed on September 2025.
Save as "data/Italian_Population_2022.csv"
Using ";" as separator.

You'll need to aggregate the ages into the age classes used in the mortality files as explained below.

## Eurostat - Mortality
[Eurostat Mortality Data](https://ec.europa.eu/eurostat/databrowser/view/hlth_cd_aro/default/table?lang=en&category=hlth.hlth_cdeath.hlth_cd_gmor)
Accessed on September 2025.

Follow these steps to correctly download the Eurostat Mortality data:
1. go to the URL above;
2. select "Customise your dataset";
3. "Age class" --> select "[Y_LT1] Less than 1 year", "[Y1-4] From 1 to 4 years", "[Y5-9] From 5 to 9 years", "[Y10-14] From 10 to 14 years", "[Y15-19] From 15 to 19 years", "[Y20-24] From 20 to 24 years", "[Y25-29] From 25 to 29 years", "[Y30-34] From 30 to 34 years", "[Y35-39] From 35 to 39 years", "[Y40-44] From 40 to 44 years", "[Y45-49] From 45 to 49 years", "[Y50-54] From 50 to 54 years", "[Y55-59] From 55 to 59 years", "[Y60-64] From 60 to 64 years", "[Y65-69] From 65 to 69 years", "[Y70-74] From 70 to 74 years", "[Y75-79] From 75 to 79 years", "[Y80-84] From 80 to 84 years", "[Y85-89] From 85 to 89 years", "[Y90-94] From 90 to 94 years", "[Y_GE95] 95 years or over";
4. "Geopolitical entity" --> select "[EU27_2020] European Union - 27 countries (from 2020)";
5. "International Statistical Classification" --> select only "[C] Malignant neoplasms (C00-C97)";
6. "Place of residence" --> select only "[TOT_IN] All deaths reported in the country";
7. "Sex" --> click on "All checked";
8. "Time" --> select "2020", "2021" and "2022";
9. click on "Save and go to data view";
10. Drag "Age class" to the row section;
11. Drag "Geopolitical entity" to the dimension section;
12. Select "Total" and download the file as CSV and "Only displayed dimensions" as "data/Deaths_Europe_Tot.csv" using "," as separator;
13. change "Sex" to "Male" and download the file as CSV and "Only displayed dimensions" as "data/Deaths_Europe_M.csv" using "," as separator;
14. change "Sex" to "Females" and download the file as CSV and "Only displayed dimensions" as "data/Deaths_Europe_F.csv" using "," as separator.

## Eurostat - Population
[Eurostat Population](https://ec.europa.eu/eurostat/databrowser/view/demo_pjan/default/table?lang=en&category=demo.demo_pop)
Accessed on September 2025.

Follow these steps to correctly download the Eurostat Population data:
1. go to the URL above;
2. select "Customise your dataset";
3. "Age class" --> select "All checked" and then remove "[TOTAL] Total" and "[UNK] Unknown";
4. "Geopolitical entity" --> select "[EU27_2020] European Union - 27 countries (from 2020)";
5. "Sex" --> click on "All checked";
6. "Time" --> select "2020", "2021" and "2022";
7. click on "Save and go to data view";
8. Drag "Age class" to the row section;
9. Drag "Geopolitical entity" to the dimension section;
10. Drag "Sex" in the column section;
11. Download the file as CSV and "Only displayed dimensions" as "data/Europe_Population.csv" using ";" as separator.

You'll need to aggregate the ages into the age classes used in the mortality files as explained below.

## Eurostat ESP2013
You can copy it from page 121 "Annex F" of the following PDF:
[Eurostat ESP2013](https://ec.europa.eu/eurostat/documents/3859598/5926869/KS-RA-13-028-EN.PDF)
Accessed on September 2025.
Save as "data/ESP2013.csv" using ";" as separator.

Or you can find the csv with the ESP2013 in the repository.

## Notes
- ISTAT files have an average dimension of 6-13KB 
- Eurostat files have an average dimension of 19-24KB 
- Eurostat files might contain extra columns (e.g. "Flag and Footnotes"), they should be removed before starting the analysis. 
- Eurostat sometimes default to .tsv instead of .csv, make sure to use .csv

## Age class aggregation
Since ISTAT and Eurostat population files have different dimensions than the mortality files they need to be aggregated.
You can use Excel to do it:
1. Open the .csv files;
2. Create a new "Age" column;
3. Aggregate the ages in the age class needed:
   - 0
   - 1-4
   - 5-9
   - ...
   - 90-94
   - 95+
4. Use the function SUM() or SUMIF() to aggregate the values;
5. Remove the original rows and keep only the aggregated age class.

## References
- ISTAT (2025). *Database with mortality by age and sex*. Accessed September 2025.
  
  Available at: [ISTAT Mortality](https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0810HEA,1.0/HEA_DEATH/DCIS_CMORTE1_EV/IT1,39_493_DF_DCIS_CMORTE1_EV_2,1.0)

- ISTAT (2025). *Resident Population on 1 January by age and sex*. Accessed September 2025.
  
  Available at: [ISTAT Population](https://demo.istat.it/app/?i=POS&l=it)

- Eurostat (2025). *Causes of death – deaths by country of residence, age, sex and cause*.
  
  Accessed September 2025.
  
  Available at: [Eurostat Mortality](https://ec.europa.eu/eurostat/databrowser/view/hlth_cd_aro/default/table?lang=en&category=hlth.hlth_cdeath.hlth_cd_gmor)

- Eurostat (2025). *Population on 1 January by age and sex*. Accessed September 2025.
  
  Available at: [Eurostat Population](https://ec.europa.eu/eurostat/databrowser/view/demo_pjan/default/table?lang=en&category=demo.demo_pop)

- Eurostat (2013). *Revision of the European Standard Population – Report of Eurostat’s task force*.
  
  Available at: [PDF](https://ec.europa.eu/eurostat/documents/3859598/5926869/KS-RA-13-028-EN.PDF)
