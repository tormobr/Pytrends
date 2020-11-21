import altair as alt
import pandas as pd
import os

def get_names(names=["Robin", "Oliver"]):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(THIS_FOLDER, "./static/Personer.csv")

    df = pd.read_csv(filename, sep=";", encoding="ISO-8859-1")
    df = prepare_data(df, names)

    # Nerest selection
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['år'], empty='none')
    highlight = alt.selection(type='single', on='mouseover', fields=['name'], nearest=True)


    base = alt.Chart(df).encode(
        x='år:T',
        y='Antall:Q',
        color='name:N'
    )

    points = base.mark_circle().encode(
        opacity=alt.value(0)
    ).add_selection(
        highlight
    ).properties(
        width=600
    )

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )

    fig = alt.layer(lines, points).properties(width=1200, height=700)

    return fig.to_json(indent=None)

def prepare_data(df, names):
    df = df.drop(["statistikkvariabel"], axis=1)
    df = df.replace('\.', 0, regex=True)
    df=df.astype(float)
    df["år"] = pd.to_datetime(df["år"], format="%Y")
    df = df.melt('år', var_name='name', value_name='Antall')
    df = df[df["name"].isin(names)]
    return df
