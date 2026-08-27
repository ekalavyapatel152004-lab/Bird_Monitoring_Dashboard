
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Bird Species Observation Analysis",
    page_icon="🐦",
    layout="wide"
)

st.title("🐦 Bird Species Observation Analysis Dashboard")


# ============================================================
# DASHBOARD PAGES
# ============================================================

page = st.sidebar.radio(
    "📑 Dashboard Pages",
    [
        "📊 Overview",
        "🐦 Species Analysis",
        "🌦️ Environment & Behaviour",
        "👥 Observer & Conservation"
    ]
)


# ============================================================
# LOAD CLEANED DATA
# ============================================================
import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "bird_monitoring.db")

conn = sqlite3.connect(db_path)

df_clean = pd.read_sql_query(
    "SELECT * FROM bird_observations",
    conn
) 
st.write("DEBUG - Rows loaded from SQLite:", len(df_clean))
conn.close()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_observations = len(df_clean)

unique_bird_species = df_clean["Scientific_Name"].nunique()

unique_common_names = df_clean["Common_Name"].nunique()

forest_count = (
    df_clean["Habitat"] == "Forest"
).sum()

grassland_count = (
    df_clean["Habitat"] == "Grassland"
).sum()


# ============================================================
# KPI CARDS
# ============================================================

st.markdown("## 📊 Key Metrics")
st.caption("Summary of the current bird monitoring dataset")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Observations",
        f"{total_observations:,}"
    )

with col2:
    st.metric(
        "Unique Bird Species",
        f"{unique_bird_species:,}"
    )

with col3:
    st.metric(
        "Common Names",
        f"{unique_common_names:,}"
    )

with col4:
    st.metric(
        "Forest",
        f"{forest_count:,}"
    )

with col5:
    st.metric(
        "Grassland",
        f"{grassland_count:,}"
    )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("## 🔎 Filters")
st.sidebar.caption("Use the filters below to explore the bird observations.")

selected_habitat = st.sidebar.multiselect(
    "Habitat",
    options=sorted(
        df_clean["Habitat"].dropna().unique()
    ),
    default=sorted(
        df_clean["Habitat"].dropna().unique()
    )
)

selected_season = st.sidebar.multiselect(
    "Season",
    options=sorted(
        df_clean["Season"].dropna().unique()
    ),
    default=sorted(
        df_clean["Season"].dropna().unique()
    )
)

selected_year = st.sidebar.multiselect(
    "Year",
    options=sorted(
        df_clean["Year"].dropna().unique()
    ),
    default=sorted(
        df_clean["Year"].dropna().unique()
    )
)

selected_visit = st.sidebar.multiselect(
    "Visit",
    options=sorted(
        df_clean["Visit"].dropna().unique()
    ),
    default=sorted(
        df_clean["Visit"].dropna().unique()
    )
)

selected_observer = st.sidebar.multiselect(
    "Observer",
    options=sorted(
        df_clean["Observer"].dropna().unique()
    ),
    default=sorted(
        df_clean["Observer"].dropna().unique()
    )
)

selected_sex = st.sidebar.multiselect(
    "Sex",
    options=sorted(
        df_clean["Sex"].dropna().unique()
    ),
    default=sorted(
        df_clean["Sex"].dropna().unique()
    )
)

selected_species = st.sidebar.multiselect(
    "Common Name",
    options=sorted(
        df_clean["Common_Name"].dropna().unique()
    ),
    default=sorted(
        df_clean["Common_Name"].dropna().unique()
    )
)

# ============================================================
# PAGE 1 — OVERVIEW
# Charts: 1, 2, 6
# ============================================================

if page == "📊 Overview":

    st.header("📊 Dashboard Overview")


    # ========================================================
    # CHART 1 — BIRD OBSERVATIONS BY HABITAT
    # ========================================================

    habitat_counts = df_clean["Habitat"].value_counts()

    fig = px.bar(
        x=habitat_counts.index,
        y=habitat_counts.values,
        text=habitat_counts.values,
        color=habitat_counts.index,
        title="Bird Observations by Habitat",
        labels={
            "x": "Habitat",
            "y": "Number of Observations",
            "color": "Habitat"
        },
        color_discrete_map={
            "Forest": "green",
            "Grassland": "gold"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 2 — UNIQUE BIRD SPECIES BY HABITAT
    # ========================================================

    species_diversity = (
        df_clean.groupby("Habitat")["Scientific_Name"]
        .nunique()
        .reset_index(name="Unique_Species")
    )

    fig = px.bar(
        species_diversity,
        x="Habitat",
        y="Unique_Species",
        text="Unique_Species",
        color="Habitat",
        title="Unique Bird Species by Habitat",
        labels={
            "Habitat": "Habitat",
            "Unique_Species": "Number of Unique Species"
        },
        color_discrete_map={
            "Forest": "blue",
            "Grassland": "orange"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 6 — TOP 10 BIODIVERSITY HOTSPOTS BY PLOT
    # ========================================================

    plot_species = (
        df_clean.groupby(["Habitat", "Plot_Name"])["Common_Name"]
        .nunique()
        .reset_index(name="Unique_Species")
    )

    top_plots = (
        plot_species
        .sort_values("Unique_Species", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_plots.sort_values("Unique_Species"),
        x="Unique_Species",
        y="Plot_Name",
        orientation="h",
        text="Unique_Species",
        title="Top 10 Biodiversity Hotspots by Plot",
        labels={
            "Unique_Species": "Number of Unique Bird Species",
            "Plot_Name": "Plot Name"
        }
    )

    fig.update_traces(
        marker_color="#1F77B4",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 2 — SPECIES ANALYSIS
# Charts: 5, 17, 20, 21, 22
# ============================================================

if page == "🐦 Species Analysis":

    st.header("🐦 Species Analysis")


    # ========================================================
    # CHART 5 — TOP 10 BIRD SPECIES BY HABITAT
    # ========================================================

    species_counts = (
        df_clean.groupby(["Habitat", "Common_Name"])
        .size()
        .reset_index(name="Observation_Count")
    )

    forest_top10 = (
        species_counts[
            species_counts["Habitat"] == "Forest"
        ]
        .nlargest(10, "Observation_Count")
    )

    grassland_top10 = (
        species_counts[
            species_counts["Habitat"] == "Grassland"
        ]
        .nlargest(10, "Observation_Count")
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_forest = px.bar(
            forest_top10.sort_values("Observation_Count"),
            x="Observation_Count",
            y="Common_Name",
            orientation="h",
            text="Observation_Count",
            title="Top 10 Bird Species - Forest"
        )

        fig_forest.update_traces(
            marker_color="#1F77B4",
            textposition="outside"
        )

        fig_forest.update_layout(
            xaxis_title="Number of Observations",
            yaxis_title="Bird Species"
        )

        st.plotly_chart(
            fig_forest,
            use_container_width=True
        )

    with col2:

        fig_grassland = px.bar(
            grassland_top10.sort_values("Observation_Count"),
            x="Observation_Count",
            y="Common_Name",
            orientation="h",
            text="Observation_Count",
            title="Top 10 Bird Species - Grassland"
        )

        fig_grassland.update_traces(
            marker_color="#6BAED6",
            textposition="outside"
        )

        fig_grassland.update_layout(
            xaxis_title="Number of Observations",
            yaxis_title="Bird Species"
        )

        st.plotly_chart(
            fig_grassland,
            use_container_width=True
        )


    # ========================================================
    # CHART 17 — TOP 10 BIRD SPECIES BY NUMBER OF OBSERVATIONS
    # ========================================================

    top_species = (
        df_clean.groupby("Common_Name")
        .size()
        .reset_index(name="Observation_Count")
        .sort_values("Observation_Count", ascending=False)
        .head(10)
        .sort_values("Observation_Count")
    )

    fig = px.bar(
        top_species,
        x="Observation_Count",
        y="Common_Name",
        orientation="h",
        text="Observation_Count",
        title="Top 10 Bird Species by Number of Observations",
        labels={
            "Observation_Count": "Number of Observations",
            "Common_Name": "Bird Species"
        }
    )

    fig.update_traces(
        marker_color="#1F77B4",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 20 — TOP 10 BIRD SPECIES BY HABITAT
    # ========================================================

    species_habitat = (
        df_clean.groupby(["Habitat", "Common_Name"])
        .size()
        .reset_index(name="Observation_Count")
    )

    top_forest = (
        species_habitat[
            species_habitat["Habitat"] == "Forest"
        ]
        .nlargest(10, "Observation_Count")
    )

    top_grassland = (
        species_habitat[
            species_habitat["Habitat"] == "Grassland"
        ]
        .nlargest(10, "Observation_Count")
    )

    top_species_habitat = pd.concat(
        [top_forest, top_grassland]
    )

    top_species_habitat = top_species_habitat.sort_values(
        "Observation_Count",
        ascending=True
    )

    fig = px.bar(
        top_species_habitat,
        x="Observation_Count",
        y="Common_Name",
        color="Habitat",
        orientation="h",
        barmode="group",
        text="Observation_Count",
        title="Top 10 Bird Species by Habitat",
        labels={
            "Observation_Count": "Number of Observations",
            "Common_Name": "Bird Species",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1565C0",
            "Grassland": "#FFFFC5"
        }
    )

    fig.update_traces(
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(
            size=12
        ),
        width=0.45
    )

    fig.update_layout(
        height=850,
        bargap=0.65,
        bargroupgap=0.35,
        margin=dict(
            l=190,
            r=80,
            t=80,
            b=70
        ),
        legend_title_text="Habitat"
    )

    fig.update_yaxes(
        tickfont=dict(size=11)
    )

    fig.update_xaxes(
        title="Number of Observations",
        tickfont=dict(size=11),
        rangemode="tozero"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 21 — RARE SPECIES BY HABITAT
    # ========================================================

    species_counts = (
        df_clean.groupby("Common_Name")
        .size()
        .reset_index(name="Observation_Count")
    )

    rare_species = species_counts[
        species_counts["Observation_Count"] <= 5
    ]

    rare_by_habitat = (
        df_clean[
            df_clean["Common_Name"].isin(
                rare_species["Common_Name"]
            )
        ]
        .groupby("Habitat")["Common_Name"]
        .nunique()
        .reset_index(name="Rare_Species")
    )

    fig = px.bar(
        rare_by_habitat,
        x="Habitat",
        y="Rare_Species",
        color="Habitat",
        text="Rare_Species",
        title="Rare Species by Habitat",
        labels={
            "Habitat": "Habitat",
            "Rare_Species": "Number of Rare Species"
        },
        color_discrete_map={
            "Forest": "#1565C0",
            "Grassland": "#64B5F6"
        }
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=13),
        width=0.55
    )

    fig.update_layout(
        height=550,
        showlegend=False,
        bargap=0.45,
        margin=dict(
            l=80,
            r=80,
            t=80,
            b=70
        )
    )

    fig.update_yaxes(
        rangemode="tozero"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 22 — SPECIES FOUND ONLY IN ONE HABITAT
    # ========================================================

    forest_only = [
        "Black-capped Chickadee",
        "Black-throated Blue Warbler",
        "Blue-winged Warbler",
        "Cerulean Warbler",
        "Dark-eyed Junco",
        "Double-crested Cormorant",
        "Green Heron",
        "Hooded Warbler",
        "Louisiana Waterthrush",
        "Mallard",
        "Nashville Warbler",
        "Osprey",
        "Peregrine Falcon",
        "Red-headed Woodpecker",
        "Tennessee Warbler",
        "Unidentified Woodpecker",
        "Worm-eating Warbler",
        "Yellow-rumped Warbler",
        "Yellow-throated Warbler"
    ]

    grassland_only = [
        "American Kestrel",
        "Bald Eagle",
        "Blue Grosbeak",
        "Bobolink",
        "Chestnut-sided Warbler",
        "Chinese Pond-Heron",
        "Cooper's Hawk",
        "Least Flycatcher",
        "Northwestern Crow",
        "Purple Martin",
        "Rock Dove",
        "Savannah Sparrow",
        "Tree Swallow",
        "Unidentified Swallow",
        "Unidentified Warbler",
        "Vesper Sparrow",
        "White-throated Sparrow",
        "Willow Flycatcher"
    ]

    forest_data = pd.DataFrame({
        "Species": forest_only,
        "Count": range(len(forest_only), 0, -1)
    })

    grassland_data = pd.DataFrame({
        "Species": grassland_only,
        "Count": range(len(grassland_only), 0, -1)
    })

    col1, col2 = st.columns(2)

    with col1:

        fig_forest = px.bar(
            forest_data,
            x="Count",
            y="Species",
            orientation="h",
            text="Count",
            title="Forest-Only Species"
        )

        fig_forest.update_traces(
            marker_color="#1565C0",
            textposition="outside",
            width=0.55,
            textfont=dict(size=9)
        )

        fig_forest.update_layout(
            height=750,
            showlegend=False,
            margin=dict(
                l=10,
                r=30,
                t=60,
                b=50
            )
        )

        fig_forest.update_xaxes(
            title="Species",
            dtick=2
        )

        fig_forest.update_yaxes(
            title="",
            autorange="reversed",
            tickfont=dict(size=9)
        )

        st.plotly_chart(
            fig_forest,
            use_container_width=True
        )

    with col2:

        fig_grassland = px.bar(
            grassland_data,
            x="Count",
            y="Species",
            orientation="h",
            text="Count",
            title="Grassland-Only Species"
        )

        fig_grassland.update_traces(
            marker_color="#64B5F6",
            textposition="outside",
            width=0.55,
            textfont=dict(size=9)
        )

        fig_grassland.update_layout(
            height=750,
            showlegend=False,
            margin=dict(
                l=10,
                r=30,
                t=60,
                b=50
            )
        )

        fig_grassland.update_xaxes(
            title="Species",
            dtick=2
        )

        fig_grassland.update_yaxes(
            title="",
            autorange="reversed",
            tickfont=dict(size=9)
        )

        st.plotly_chart(
            fig_grassland,
            use_container_width=True
        )


# ============================================================
# PAGE 3 — ENVIRONMENT & BEHAVIOUR
# Charts: 3, 4, 7, 8, 9, 10, 11, 18, 19
# ============================================================

if page == "🌦️ Environment & Behaviour":

    st.header("🌦️ Environment & Behaviour")


    # ========================================================
    # CHART 3 — SEASONAL BIRD OBSERVATIONS BY HABITAT
    # ========================================================

    seasonal_counts = (
        df_clean.groupby(["Habitat", "Season"])
        .size()
        .reset_index(name="Observation_Count")
    )

    seasons = ["Spring", "Summer"]

    fig = px.bar(
        seasonal_counts,
        x="Season",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        category_orders={
            "Season": seasons
        },
        title="Seasonal Bird Observations by Habitat",
        labels={
            "Season": "Season",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 4 — BIRD OBSERVATIONS BY START HOUR AND HABITAT
    # ========================================================

    hourly_counts = (
        df_clean.groupby(["Habitat", "Start_Hour"])
        .size()
        .reset_index(name="Observation_Count")
    )

    hours = sorted(
        df_clean["Start_Hour"].dropna().unique()
    )

    fig = px.bar(
        hourly_counts,
        x="Start_Hour",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        category_orders={
            "Start_Hour": hours
        },
        title="Bird Observations by Start Hour and Habitat",
        labels={
            "Start_Hour": "Start Hour",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=hours,
        ticktext=[
            f"{int(hour)} AM"
            for hour in hours
        ]
    )

    fig.update_traces(
        textposition="outside",
        textfont_size=8
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 7 — BIRD OBSERVATIONS BY SKY CONDITION AND HABITAT
    # ========================================================

    sky_habitat = (
        df_clean.groupby(["Habitat", "Sky"])
        .size()
        .reset_index(name="Observation_Count")
    )

    fig = px.bar(
        sky_habitat,
        x="Sky",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        title="Bird Observations by Sky Condition and Habitat",
        labels={
            "Sky": "Sky Condition",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_xaxes(
        tickangle=30
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 8 — BIRD OBSERVATIONS BY WIND CONDITION AND HABITAT
    # ========================================================

    wind_habitat = (
        df_clean.groupby(["Habitat", "Wind"])
        .size()
        .reset_index(name="Observation_Count")
    )

    fig = px.bar(
        wind_habitat,
        x="Wind",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        title="Bird Observations by Wind Condition and Habitat",
        labels={
            "Wind": "Wind Condition",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_xaxes(
        tickangle=35
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 9 — BIRD OBSERVATIONS BY DISTURBANCE EFFECT AND HABITAT
    # ========================================================

    disturbance_habitat = (
        df_clean.groupby(["Disturbance", "Habitat"])
        .size()
        .reset_index(name="Observation_Count")
    )

    fig = px.bar(
        disturbance_habitat,
        x="Disturbance",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        title="Bird Observations by Disturbance Effect and Habitat",
        labels={
            "Disturbance": "Disturbance Effect",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_xaxes(
        tickangle=20
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 10 — BIRD OBSERVATIONS BY DISTANCE AND HABITAT
    # ========================================================

    distance_habitat = (
        df_clean.groupby(["Habitat", "Distance"])
        .size()
        .reset_index(name="Observation_Count")
    )

    distance_habitat = distance_habitat.dropna(
        subset=["Distance"]
    )

    fig = px.bar(
        distance_habitat,
        x="Distance",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        title="Bird Observations by Distance and Habitat",
        labels={
            "Distance": "Distance from Observer",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_xaxes(
        type="category"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 11 — FLYOVER OBSERVATIONS BY HABITAT
    # ========================================================

    flyover_habitat = (
        df_clean.groupby(["Habitat", "Flyover_Observed"])
        .size()
        .reset_index(name="Observation_Count")
    )

    fig = px.bar(
        flyover_habitat,
        x="Flyover_Observed",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        title="Flyover Observations by Habitat",
        labels={
            "Flyover_Observed": "Flyover Observed",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_xaxes(
        type="category"
    )

    fig.update_traces(
        textposition="outside",
        textfont_size=9
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 18 — TEMPERATURE RANGE VS OBSERVATION COUNT BY HABITAT
    # ========================================================

    temperature_range = (
        df_clean.groupby(
            ["Habitat", "Temperature_Range"]
        )
        .size()
        .reset_index(name="Observation_Count")
    )

    temp_order = [
        "≤15°C",
        "16–20°C",
        "21–25°C",
        "26–30°C",
        "31–35°C",
        ">35°C"
    ]

    temperature_range["Temperature_Range"] = pd.Categorical(
        temperature_range["Temperature_Range"],
        categories=temp_order,
        ordered=True
    )

    fig = px.bar(
        temperature_range,
        x="Temperature_Range",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        category_orders={
            "Temperature_Range": temp_order
        },
        title="Temperature Range vs Observation Count by Habitat",
        labels={
            "Temperature_Range": "Temperature Range",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 19 — HUMIDITY RANGE VS OBSERVATION COUNT BY HABITAT
    # ========================================================

    humidity_range = (
        df_clean.groupby(
            ["Habitat", "Humidity_Range"]
        )
        .size()
        .reset_index(name="Observation_Count")
    )

    humidity_order = [
        "≤40%",
        "41–60%",
        "61–80%",
        "81–90%",
        ">90%"
    ]

    humidity_range["Humidity_Range"] = pd.Categorical(
        humidity_range["Humidity_Range"],
        categories=humidity_order,
        ordered=True
    )

    fig = px.bar(
        humidity_range,
        x="Humidity_Range",
        y="Observation_Count",
        color="Habitat",
        barmode="group",
        text="Observation_Count",
        category_orders={
            "Humidity_Range": humidity_order
        },
        title="Humidity Range vs Observation Count by Habitat",
        labels={
            "Humidity_Range": "Humidity Range",
            "Observation_Count": "Number of Observations",
            "Habitat": "Habitat"
        },
        color_discrete_map={
            "Forest": "#1F77B4",
            "Grassland": "#6BAED6"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 4 — OBSERVER & CONSERVATION
# ============================================================

if page == "👥 Observer & Conservation":

    st.header("👥 Observer & Conservation")


    # ========================================================
    # CHART 12 — BIRD OBSERVATIONS BY OBSERVER
    # ========================================================

    observer_counts = (
        df_clean.groupby("Observer")
        .size()
        .reset_index(name="Observation_Count")
        .sort_values("Observation_Count", ascending=False)
    )

    fig = px.bar(
        observer_counts,
        x="Observer",
        y="Observation_Count",
        text="Observation_Count",
        title="Bird Observations by Observer",
        labels={
            "Observer": "Observer",
            "Observation_Count": "Number of Observations"
        }
    )

    fig.update_traces(
        marker_color="#1F77B4",
        textposition="outside"
    )

    fig.update_xaxes(
        type="category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 13 — UNIQUE BIRD SPECIES RECORDED BY OBSERVER
    # ========================================================

    observer_species = (
        df_clean.groupby("Observer")["Scientific_Name"]
        .nunique()
        .reset_index(name="Unique_Species")
        .sort_values("Unique_Species", ascending=False)
    )

    fig = px.bar(
        observer_species,
        x="Observer",
        y="Unique_Species",
        text="Unique_Species",
        title="Unique Bird Species Recorded by Observer",
        labels={
            "Observer": "Observer",
            "Unique_Species": "Number of Unique Species"
        }
    )

    fig.update_traces(
        marker_color="#1F77B4",
        textposition="outside"
    )

    fig.update_xaxes(
        type="category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 14 — BIRD OBSERVATIONS ACROSS VISITS
    # ========================================================

    visit_data = (
        df_clean.groupby("Visit")
        .size()
        .reset_index(name="Observation_Count")
    )

    fig = px.line(
        visit_data,
        x="Visit",
        y="Observation_Count",
        markers=True,
        text="Observation_Count",
        title="Bird Observations Across Visits",
        labels={
            "Visit": "Visit Number",
            "Observation_Count": "Number of Observations"
        }
    )

    fig.update_traces(
        line_color="#1F77B4",
        line_width=3,
        marker_size=9,
        textposition="top center"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[1, 2, 3]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CHART 15 — PIF WATCHLIST STATUS BY HABITAT
    # ========================================================

    pif_data = (
        df_clean.groupby(
            ["Habitat", "PIF_Watchlist_Status"]
        )
        .size()
        .reset_index(name="Observation_Count")
    )

    col1, col2 = st.columns(2)

    for col, habitat in zip(
        [col1, col2],
        ["Forest", "Grassland"]
    ):

        habitat_data = pif_data[
            pif_data["Habitat"] == habitat
        ]

        counts = (
            habitat_data
            .set_index(
                "PIF_Watchlist_Status"
            )["Observation_Count"]
            .reindex(
                [False, True],
                fill_value=0
            )
            .reset_index()
        )

        counts["Status"] = counts[
            "PIF_Watchlist_Status"
        ].map({
            False: "Not Watchlist",
            True: "Watchlist"
        })

        with col:

            fig = px.pie(
                counts,
                names="Status",
                values="Observation_Count",
                hole=0.45,
                title=f"{habitat} — PIF Watchlist"
            )

            fig.update_traces(
                textinfo="label+value",
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.subheader(
        "PIF Watchlist Status by Habitat"
    )


    # ========================================================
    # CHART 16 — REGIONAL STEWARDSHIP STATUS BY HABITAT
    # ========================================================

    regional_data = (
        df_clean.groupby(
            ["Habitat", "Regional_Stewardship_Status"]
        )
        .size()
        .reset_index(name="Observation_Count")
    )

    col1, col2 = st.columns(2)

    for col, habitat in zip(
        [col1, col2],
        ["Forest", "Grassland"]
    ):

        habitat_data = regional_data[
            regional_data["Habitat"] == habitat
        ]

        counts = (
            habitat_data
            .set_index(
                "Regional_Stewardship_Status"
            )["Observation_Count"]
            .reindex(
                [False, True],
                fill_value=0
            )
            .reset_index()
        )

        counts["Status"] = counts[
            "Regional_Stewardship_Status"
        ].map({
            False: "Not Stewardship",
            True: "Stewardship"
        })

        with col:

            fig = px.pie(
                counts,
                names="Status",
                values="Observation_Count",
                hole=0.45,
                title=f"{habitat} — Regional Stewardship"
            )

            fig.update_traces(
                textinfo="label+value",
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.subheader(
        "Regional Stewardship Status by Habitat"
    )

