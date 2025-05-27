import pandas as pd
from utils.constants import DATA_DIRECTORY

#-- Kurser

def sammanfoga_kurser():
    filer_och_ar = {
        "resultat-2022-for-kurser-inom-yh.xlsx": 2022,
        "resultat-2023-for-kurser-inom-yh.xlsx": 2023,
        "resultat-2024-for-kurser-inom-yh.xlsx": 2024,
    }

#-- Relevanta kolumner

    kolumner = [
        "Beslut",
        "Anordnare namn",
        "Utbildningsområde",
        "Totalt antal beviljade platser",
        "Kommun",
        "Län"
    ]

    alla_data = []

    for filnamn, ar in filer_och_ar.items():
        full_sokvag = DATA_DIRECTORY / filnamn
        df = pd.read_excel(full_sokvag, sheet_name=0)
        df.columns = df.columns.str.strip()

        for kolumn in kolumner:
            if kolumn not in df.columns:
                df[kolumn] = pd.NA

        df = df[kolumner].copy()
        df["År"] = ar
        alla_data.append(df)

    sammanfogad_df = pd.concat(alla_data, ignore_index=True)
    output_fil = DATA_DIRECTORY / "sammanfogad_kurser_2021-202466.xlsx"
    sammanfogad_df.to_excel(output_fil, index=False)

#-- Program    

def sammanfoga_program():
    filer_och_ar = {
        "resultat_ansokningsomgang_program_2020.xlsx": 2020,
        "resultat_ansokningsomgang_program_2021.xlsx": 2021,
        "resultat_ansokningsomgang_program_2022.xlsx": 2022,
        "resultat_ansokningsomgang_program_2023.xlsx": 2023,
        "resultat_ansokningsomgang_program_2024.xlsx": 2024
    }

    alla_program = []
    for filnamn, ar in filer_och_ar.items():
        df = pd.read_excel(DATA_DIRECTORY / filnamn, sheet_name="Tabell 3", engine="openpyxl")
        df["År"] = ar
        alla_program.append(df)

    sammanfogat = pd.concat(alla_program, ignore_index=True)
    sammanfogat.to_excel(DATA_DIRECTORY / "sammanfogad_program_2020-202466.xlsx", index=False)

if __name__ == "__main__":
    sammanfoga_kurser()
    sammanfoga_program()
