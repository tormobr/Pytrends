from matplotlib import pyplot as plt
from pytrends.request import TrendReq
from vega_datasets import data
import altair as alt
import pandas as pd

pytrend = TrendReq()
world_url = "https://raw.githubusercontent.com/deldersveld/topojson/master/world-countries.json"
us_url = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/united-states/us-albers.json"
world = alt.topo_feature(world_url, "countries1")
us = alt.topo_feature(us_url, "us")


def get_trend(country="", key_words=["apple"]):
    # Prepare the data
    trend = key_words[0]
    geo = country[:2].upper()
    pytrend.build_payload(key_words, cat=0, timeframe="today 5-y", geo=geo, gprop="")
    df = pytrend.interest_by_region()
    df.reset_index(inplace=True)
    df["geoName"] = df["geoName"].str.replace("United States", "United States of America")

    # Make the chart
    nearest = alt.selection(type="single", on="mouseover", fields=["properties.name"], empty="none")

    fig = alt.Chart(world).mark_geoshape().encode(
        color=alt.Color(f"{trend}:Q", scale=alt.Scale(scheme="oranges")),
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip(f"{trend}:Q", title=f"{trend}"),
        ],
        stroke=alt.condition(nearest, alt.value("gray"), alt.value(None)),
    ).transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(df, "geoName", [f"{trend}"])
    ).project(
        type="naturalEarth1"
    ).properties(
        width=1400,
        height=500,
        title=f"Seach trend for {trend}",
    ).add_selection(nearest)

    print("saving file here")
    return fig.to_json(indent=None)

"""
def us():
    kw_list = ["Biden", "Trump", "hurricane"]
    pytrend.build_payload(kw_list, cat=0, timeframe="2019-10-01 2020-11-03", geo="US", gprop="")
    df = pytrend.interest_by_region()

    us = alt.topo_feature("https://raw.githubusercontent.com/deldersveld/topojson/master/countries/united-states/us-albers.json", "us")
    nearest = alt.selection(type="single", on="mouseover", fields=["properties.name"], empty="none")

    df.reset_index(inplace=True)
    df["geoName"] = df["geoName"].str.replace("United States", "United States of America")

    fig = alt.Chart(us).mark_geoshape().encode(
        color=alt.Color("hurricane:Q", scale=alt.Scale(scheme="reds")),
        tooltip=[
            alt.Tooltip("properties.name:N", title="Country"),
            alt.Tooltip("hurricane:Q", title="Trend"),
        ],
        stroke=alt.value("gray"),
    ).transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(df, "geoName", ["hurricane"])
    ).project(
        type="albersUsa"
    )

    fig.save("fig.html")
"""
