import pandas as pd
import streamlit as st

GROUP_COLUMS = [
    "resa_dossier",
    "resa_ocup_nom",
    "resa_ocup_prenom",
    "lot_ref",
    "resa_deb",
    "resa_fin",
]

FINAL_COLUMNS = [
    "Réf",
    "Nom",
    "ad1",
    "ad2",
    "cp-ville",
    "pays",
    "date arrivée",
    "date départ",
    "Kit serviette (serv + drap)",
    "Kit petit lit (dh + dplat + t)",
    "Kit couette petit lit (dh + hc + t)",
    "Kit bq gigogne (2 dh + 1 dplat + 2t)",
    "Kit gd lit (dh + dplat + 2t)",
    "Kit couette 140",
    "Kit couette 160",
    "Kit couette 180",
    "Tapis de bain",
    "ss total 1",
    "Kit arrivée",
    "Pose literie",
    "Nb lit fait",
    "Lit Bébé",
    "Chaise Bébé",
    "Baignoire",
    "Pose matériel bébé",
    "ss total 2",
    "Mt Ménage = total 3",
]


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def main():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep="\t")

        with st.expander("Voir le fichier:", expanded=False):
            st.dataframe(df)

        groups = {}
        for name, group in df.groupby(GROUP_COLUMS):
            data = (
                group.loc[:, ["prest_titre_fra", "resa_prest_qte"]]
                .set_index("prest_titre_fra")
                .resa_prest_qte.to_dict()
            )
            groups[name] = data

        result_df = pd.DataFrame(groups).T.fillna(0)

        st.dataframe(result_df)

        st.download_button(
            label="Download data as CSV",
            data=convert_df(result_df),
            file_name="extract_conversion.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
