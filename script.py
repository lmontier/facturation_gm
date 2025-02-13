import pandas as pd
import json

df = pd.read_excel("data/R3.xls")


def format_name(_df: pd.DataFrame) -> pd.Series:
    return _df.resa_ocup_civi + " " + _df.resa_ocup_prenom + " " + _df.resa_ocup_nom


GROUP_COLUMS = [
    "resa_dossier",
    "resa_ocup_nom",
    "resa_ocup_prenom",
    "resa_ocup_civi",
    "lot_ref",
    "resa_deb",
    "resa_fin",
]


groups = {}
for name, group in df.groupby(GROUP_COLUMS):
    data = (
        group.loc[:, ["prest_titre_fra", "resa_prest_qte"]]
        .set_index("prest_titre_fra")
        .resa_prest_qte.to_dict()
    )
    groups[name] = data


# %%
exploded_df = (
    pd.DataFrame(groups)
    .T.reset_index()
    .rename(columns={f"level_{i}": GROUP_COLUMS[i] for i in range(len(GROUP_COLUMS))})
    .assign(Nom=lambda _df: _df.pipe(format_name))
)


# %% Map data
exploded_df.to_csv("data/predone.csv")

with open("column_mapping.json", "r") as file:
    column_mapping = json.load(file)
final_df = exploded_df.rename(columns=column_mapping).reindex(
    columns=column_mapping.values()
)
final_df.to_csv("data/done.csv")
