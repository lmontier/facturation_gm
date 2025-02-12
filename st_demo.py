import pandas as pd
import streamlit as st

GROUP_COLUMS = ["resa_dossier", "resa_ocup_nom", "resa_ocup_prenom", "lot_ref"]


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

        dff = pd.DataFrame(groups).T.fillna(0)

        st.dataframe(dff)


if __name__ == "__main__":
    main()
