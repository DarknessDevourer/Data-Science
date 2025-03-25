import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lab Work", layout="wide")
sns.set_style("whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv("G:\\Univer_part4\\AD\\Lab_3\\df.csv")
    return df

df = load_data()

DEFAULT_METRIC = "VCI"
DEFAULT_AREA = df["Area"].unique()[0]
DEFAULT_WEEK_RANGE = (int(df["Week"].min()), int(df["Week"].max()))
DEFAULT_YEAR_RANGE = (int(df["Year"].min()), int(df["Year"].max()))

if "selected_metric" not in st.session_state:
    st.session_state["selected_metric"] = DEFAULT_METRIC
if "selected_area" not in st.session_state:
    st.session_state["selected_area"] = DEFAULT_AREA
if "week_range" not in st.session_state:
    st.session_state["week_range"] = DEFAULT_WEEK_RANGE
if "year_range" not in st.session_state:
    st.session_state["year_range"] = DEFAULT_YEAR_RANGE
if "sort_asc" not in st.session_state:
    st.session_state["sort_asc"] = False
if "sort_desc" not in st.session_state:
    st.session_state["sort_desc"] = False

#HI

def reset_filters():
    st.session_state["selected_metric"] = DEFAULT_METRIC
    st.session_state["selected_area"] = DEFAULT_AREA
    st.session_state["week_range"] = DEFAULT_WEEK_RANGE
    st.session_state["year_range"] = DEFAULT_YEAR_RANGE
    st.session_state["sort_asc"] = False
    st.session_state["sort_desc"] = False

col_filters, col_output = st.columns([1, 3])

with col_filters:
    st.header("Filters")

    st.session_state["selected_metric"] = st.selectbox(
        "Select time series:",
        options=["VCI", "TCI", "VHI"],
        index=["VCI", "TCI", "VHI"].index(st.session_state["selected_metric"])
    )

    st.session_state["selected_area"] = st.selectbox(
        "Select region:",
        options=df["Area"].unique(),
        index=list(df["Area"].unique()).index(st.session_state["selected_area"])
    )

    st.session_state["week_range"] = st.slider(
        "Select week range:",
        min_value=int(df["Week"].min()),
        max_value=int(df["Week"].max()),
        value=st.session_state["week_range"]
    )

    st.session_state["year_range"] = st.slider(
        "Select year range:",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=st.session_state["year_range"]
    )

    st.session_state["sort_asc"] = st.checkbox("Sort ascending", value=st.session_state["sort_asc"])
    st.session_state["sort_desc"] = st.checkbox("Sort descending", value=st.session_state["sort_desc"])

    if st.button("Reset filters"):
        reset_filters()

year_min, year_max = st.session_state["year_range"]
week_min, week_max = st.session_state["week_range"]

filtered_df = df[
    (df["Year"] >= year_min) & (df["Year"] <= year_max) &
    (df["Week"] >= week_min) & (df["Week"] <= week_max)
]

metric_col = st.session_state["selected_metric"]
sort_asc = st.session_state["sort_asc"]
sort_desc = st.session_state["sort_desc"]

if sort_asc and not sort_desc:
    filtered_df = filtered_df.sort_values(by=metric_col, ascending=True)
elif sort_desc and not sort_asc:
    filtered_df = filtered_df.sort_values(by=metric_col, ascending=False)

area_data = filtered_df[filtered_df["Area"] == st.session_state["selected_area"]]

with col_output:
    tabs = st.tabs(["Table", "Chart (selected region)", "Comparison with other regions"])

    with tabs[0]:
        st.subheader("Filtered data (selected region)")
        st.dataframe(area_data)

    with tabs[1]:
        st.subheader(f"Time series for region: {st.session_state['selected_area']}")
        if not area_data.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.lineplot(data=area_data, x="Week", y=metric_col, hue="Year", marker="o", ax=ax)
            ax.set_title(f"{metric_col} over weeks (selected region)")
            st.pyplot(fig)
        else:
            st.warning("No data to display.")

    with tabs[2]:
        st.subheader(f"Comparison of {metric_col} across all regions in selected interval")
        if not filtered_df.empty:
            fig_comp, ax_comp = plt.subplots(figsize=(10, 5))
            sns.lineplot(
                data=filtered_df,
                x="Week",
                y=metric_col,
                hue="Area",
                marker="o",
                ax=ax_comp
            )
            ax_comp.set_title(f"Comparison of {metric_col} across regions")

            ax_comp.legend(
                title="Region",
                loc="upper left",
                bbox_to_anchor=(1.02, 1),
                borderaxespad=0
            )

            st.pyplot(fig_comp)
        else:
            st.warning("No data to display.")
