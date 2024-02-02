import streamlit as st
import pandas as pd
import preprocesser, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")
df = preprocesser.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image(
    "https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png"
)
user_menu = st.sidebar.radio(
    "Select an option",
    (
        "Medal tally",
        "overall analysis",
        "country-wise analysis",
        "athlete-wise analysis",
    ),
)
# st.dataframe(df)

if user_menu == "Medal tally":
    st.sidebar.header("Medal tally")
    years, country = helper.country_year_list(df)

    selected_years = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("select country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_years, selected_country)
    if selected_years == "overall" and selected_country == "overall":
        st.title("overall tally")
    if selected_years != "overall" and selected_country == "overall":
        st.title("medal tally in " + str(selected_years))
    if selected_years == "overall" and selected_country != "overall":
        st.title(selected_country + " overall performance")
    if selected_years != "overall" and selected_country != "overall":
        st.title(selected_country + " performance in " + str(selected_years))
    st.table(medal_tally)

if user_menu == "overall analysis":
    editions = df["Year"].unique().shape[0] - 1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    event = df["Event"].unique().shape[0]
    Nation = df["region"].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("events")
        st.title(event)
    with col2:
        st.header("athletes")
        st.title(athletes)
    with col3:
        st.header("Nation")
        st.title(Nation)

    st.title("Number of events overtime(Every Sport)")
    fig, ax = plt.subplots(figsize=(25, 25))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax = sns.heatmap(
        x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count")
        .fillna(0)
        .astype(int),
        annot=True,
    )
    st.pyplot(fig)

    st.title("Most successful athletes")
    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "overall")
    selected_sport = st.selectbox("Select a sport", sports_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == "country-wise analysis":
    st.sidebar.title("country-wise analysis")
    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a country", country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " medal tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == "athlete-wise analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ["overall list", "gold medalist", "silver medalist", "bronse medalist"],
        show_hist=False,
        show_rug=False,
    )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("How distribution of age effects chances of glory")
    st.plotly_chart(fig)

    famous_sports = [
        "Basketball",
        "Judo",
        "Football",
        "Tug-Of-War",
        "Athletics",
        "Swimming",
        "Badminton",
        "Sailing",
        "Gymnastics",
        "Art Competitions",
        "Handball",
        "Weightlifting",
        "Wrestling",
        "Water Polo",
        "Hockey",
        "Rowing",
        "Fencing",
        "Shooting",
        "Boxing",
        "Taekwondo",
        "Cycling",
        "Diving",
        "Canoeing",
        "Tennis",
        "Golf",
        "Softball",
        "Archery",
        "Volleyball",
        "Synchronized Swimming",
        "Table Tennis",
        "Baseball",
        "Rhythmic Gymnastics",
        "Rugby Sevens",
        "Beach Volleyball",
        "Triathlon",
        "Rugby",
        "Polo",
        "Ice Hockey",
    ]
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distrtibution of age wrt sport(Gold Medalist)")
    st.plotly_chart(fig)

    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Silver"]["Age"].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distrtibution of age wrt sport(Silver Medalist)")
    st.plotly_chart(fig)

    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "overall")
    st.title("Height vs Weight")
    selected_sport = st.selectbox("Select a sport", sports_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(
        x="Weight",
        y="Height",
        data=temp_df,
        hue=temp_df["Medal"],
        style=temp_df["Sex"],
        s=100,
    )
    st.pyplot(fig)

    st.title("Men vs Women Participation over the years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["male", "female"])
    st.plotly_chart(fig)
