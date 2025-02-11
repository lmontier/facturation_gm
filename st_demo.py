import streamlit as st
import pandas as pd


st.write("Coucou")


value = st.selectbox("kikou", options=[1, 3, 4])

st.write(f"Show selected value: {value}")


df = pd.read_csv("test.csv", sep="\t")


group_colums = ["resa_dossier", "resa_ocup_nom", "resa_ocup_prenom", "lot_ref"]


groups = {}
for name, group in df.groupby(group_colums):
    data = (
        group.loc[:, ["prest_titre_fra", "resa_prest_qte"]]
        .set_index("prest_titre_fra")
        .resa_prest_qte.to_dict()
    )
    groups[name] = data
# data = df.groupby(group_colums).apply(
#     lambda g: {g["prest_titre_fra"]: g["resa_prest_qte"]}
# )

# print(data.to_csv("done.csv"))
print(groups)
print("coucou")


dff = pd.DataFrame(groups).T.fillna(0)
dff.to_csv("done.csv")
# pd.DataFrame(groups).to_csv("done.csv")


st.dataframe(dff)
