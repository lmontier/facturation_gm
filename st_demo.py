from datetime import datetime
import os
import pandas as pd
import streamlit as st
import json

GROUP_COLUMS = [
    "resa_dossier",
    "resa_ocup_nom",
    "resa_ocup_prenom",
    "resa_ocup_civi",
    "lot_ref",
    "resa_deb",
    "resa_fin",
]


with open("column_mapping.json", "r") as file:
    COLUMN_MAPPING = json.load(file)


def format_name(_df: pd.DataFrame) -> pd.Series:
    return _df.resa_ocup_civi + " " + _df.resa_ocup_prenom + " " + _df.resa_ocup_nom


def format_date(date_series: pd.Series) -> pd.Series:
    return date_series.strftime("%Y %m %d")


def move_menage_price_into_qte(df: pd.DataFrame) -> pd.Series:
    return df.assign(
        resa_prest_qte=lambda _df: _df.resa_prest_qte.mask(
            _df.prest_titre_fra == "Ménage Fin de séjour",
            _df.resa_prest_qte * _df.resa_prest_total,
        )
    )


def get_excel_filename():
    return "extract_converted_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".xlsx"


def main():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        with st.expander("Voir le fichier:", expanded=False):
            st.dataframe(df)

        preproc_df = df.pipe(move_menage_price_into_qte)
        groups = {}
        for name, group in preproc_df.groupby(GROUP_COLUMS):
            data = (
                group.loc[:, ["prest_titre_fra", "resa_prest_qte"]]
                .set_index("prest_titre_fra")
                .resa_prest_qte.to_dict()
            )
            groups[name] = data

        # %%
        final_df = (
            (
                pd.DataFrame(groups)
                .T.reset_index()
                .rename(
                    columns={
                        f"level_{i}": GROUP_COLUMS[i] for i in range(len(GROUP_COLUMS))
                    }
                )
                .assign(
                    Nom=lambda _df: _df.pipe(format_name),
                    resa_deb=lambda _df: _df.resa_deb.map(format_date),
                    resa_fin=lambda _df: _df.resa_fin.map(format_date),
                )
            )
            .rename(columns=COLUMN_MAPPING)
            .reindex(columns=COLUMN_MAPPING.values())
        )

        st.subheader("Tableau Final:")
        st.dataframe(final_df)

        # %% Export to excel
        excel_filename = get_excel_filename()
        excel_filepath = os.path.join("data", excel_filename)

        final_df.to_excel(excel_filepath, index=False)

        with open(excel_filepath, "rb") as f:
            st.download_button(
                "Télécharger",
                f,
                file_name=excel_filename,
                mime="application/octet-stream",
            )


if __name__ == "__main__":
    main()
