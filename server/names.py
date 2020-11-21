import altair as alt
import pandas as pd

def get_names(names=["Robin", "Oliver"]):
    filename = "Personer.csv"
    df = pd.read_csv(filename, sep=";", encoding="ISO-8859-1")
    df = prepare_data(df, names)

    # Nerest selection
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['år'], empty='none')

    # The chart itself
    fig = alt.Chart(df).mark_line().encode(
        x = "år",
        y = "Antall:Q",
        color = "name:N"
    )

    # Invisible selectors
    selectors = alt.Chart(df).mark_point().encode(
        x='år',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )


    # Dots on each line
    points = fig.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Text displaying number on dot
    text = fig.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'Antall', alt.value(' '))
    )

    # Vertical lines at x loc
    rules = alt.Chart(df).mark_rule(color='gray').encode(
        x='år:Q',
    ).transform_filter(
        nearest
    )


    # Layer together
    fig = alt.layer(
        fig, selectors, points, rules, text
    ).properties(
        width=1200, height=700
    )

    return fig.to_json(indent=None)

def prepare_data(df, names):
    df = df.drop(["statistikkvariabel"], axis=1)
    df = df.replace('\.', 0, regex=True)
    df=df.astype(float)
    print(df)
    df = df.melt('år', var_name='name', value_name='Antall')
    print(df)
    df = df[df["name"].isin(names)]
    return df
