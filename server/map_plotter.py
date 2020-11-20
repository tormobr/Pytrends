from pytrends.request import TrendReq
import altair as alt
import pandas as pd

world_url = "https://raw.githubusercontent.com/deldersveld/topojson/master/world-countries.json"
us_url = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/united-states/us-albers.json"
nor_url = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/norway/norway-counties.json"

world = alt.topo_feature(world_url, "countries1")
us = alt.topo_feature(us_url, "us")
norway = alt.topo_feature(nor_url, "NOR_adm1")

# The properties name in the topo json
properties = {
    "norway": "properties.NAME_1",
    "usa": "properties.name",
    "world": "properties.name"
}

# Topo json for different countries
topo = {
    "norway": norway,
    "usa": us,
    "world": world,
}

# How to project different countries
projections = {
    "norway": "naturalEarth1",
    "usa": "albersUsa",
    "world": "naturalEarth1"
}

# Gets a trend and creates maps
def get_trend(country="norway", key_words=["apple"], geo="NO"):
    pytrend = TrendReq()
    # Prepare the data
    trend = key_words[0]
    pytrend.build_payload(key_words, cat=0, timeframe="now 1-H", geo=geo, gprop="")
    df = pytrend.interest_by_region()
    df.reset_index(inplace=True)
    df = clean_df(df)
    print(df)

    # Make the chart
    nearest = alt.selection(type="single", on="mouseover", fields=[properties[country]], empty="none")

    fig = alt.Chart(topo[country]).mark_geoshape().encode(
        color=alt.Color(f"{trend}:Q", scale=alt.Scale(scheme="oranges")),
        tooltip=[
            alt.Tooltip(f"{properties[country]}:N", title="Country"),
            alt.Tooltip(f"{trend}:Q", title=f"{trend}"),
        ],
        stroke=alt.condition(nearest, alt.value("gray"), alt.value(None)),
    ).transform_lookup(
        lookup=properties[country],
        from_=alt.LookupData(df, "geoName", [f"{trend}"])
    ).project(
        type=projections[country]
    ).properties(
        width=1400,
        height=500,
        title=f"Seach trend for {trend}",
    ).add_selection(nearest)

    print("saving file here")
    return fig.to_json(indent=None)

def clean_df(df):
    df["geoName"] = df["geoName"].str.replace("Nord-Trondelag", "Nord-Trøndelag")
    df["geoName"] = df["geoName"].str.replace("Sor-Trondelag", "Sør-Trøndelag")
    df["geoName"] = df["geoName"].str.replace("Ostfold", "Østfold")
    df["geoName"] = df["geoName"].str.replace("More og Romsdal", "Møre og Romsda")
    df["geoName"] = df["geoName"].str.replace("United States", "United States of America")
    return df

