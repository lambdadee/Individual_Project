import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
import numpy as np
import seaborn as sns

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title(":bar_chart: Revenue Exploratory Data Analysis Dashboard")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

st.subheader("Data Cleaning")

st.markdown("Loading dataset into Pandas DataFrame df by using pd.read_csv() method")
df = pd.read_csv("SalesForCourse/SalesForCourse_quizz_table.csv", encoding="latin1")
df = df.sort_values('Month')
df = df.drop("Column1", axis=1)
df["Profit"] = df["Revenue"] - df["Cost"]
st.write(df.head(26).style.background_gradient(cmap="cividis_r"))


st.markdown("Checking if there is NA element in any of the column by using df.isna().sum() method")
st.write(np.array(list(df.isna().sum())).reshape(1, -1))

st.markdown("Generating descriptive statistic by usnig df.describe() method for numeric data and df.describe(include='O') for object (strings and timestamps data)")
st.write(df.describe().style.background_gradient(cmap="magma_r"))
st.write(df.describe(include="O").style.background_gradient(cmap="magma_r"))

st.markdown("checking if there is any duplicate entry in the dataset by df.duplicated(keep='first') method")
st.write(df[df.duplicated(keep="first")])

st.write(df.info())


st.subheader("Data Visualization")

col1, col2 = st.columns((2))

df["Date"] = pd.to_datetime(df["Date"])

startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()
    

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()

st.sidebar.header("Choose Filter")

country = st.sidebar.multiselect("Select Country", df["Country"].unique())
if not country:
    df1 = df.copy()
else:
    df1 = df[df["Country"].isin(country)]

state = st.sidebar.multiselect("Select State", df1["State"].unique())

if not country and not state:
    filtered_df = df
elif not state:
    filtered_df = df[df["Country"].isin(country)]
elif state:
    filtered_df = df1[df1["State"].isin(state)]
    
else:
    filtered_df = df1[(df1["Country"].isin(country)) & (df1["State"].isin(state))]


category_df = filtered_df.groupby(by = "Product Category", as_index= False)["Revenue"].sum()

with col1:
    st.subheader("Category wise Revenue")
    fig = px.bar(category_df, x="Product Category", y="Revenue", text=["${:,.2f}".format(x) for x in category_df["Revenue"]], template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)
    st.markdown("Insights: ")
    st.markdown("- The business seems to be heavily reliant on bike sales, which could be a risk if the market demand for bikes fluctuates.")
    st.markdown("- Accessories are a significant contributor to revenue, suggesting opportunities for growth in this category.")
    st.markdown("- Clothes may not be a priority for the business, but could still be a viable market if targeted effectively.")

with col2:
    st.subheader("Country wise Revenue")
    fig1 = px.pie(filtered_df, values= "Revenue", names= "Country", hole=0.5)
    fig1.update_traces(text = filtered_df["Country"], textposition = "inside")
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("Insights: ")
    st.markdown("- The United States generates the largest share of revenue (46.4%), indicating a strong market presence or high demand for the product in this region.")
    st.markdown("- The United Kingdom, Germany, and France collectively account for 53.5% of the revenue, highlighting the significance of the European market. However, France generates the smallest share of revenue (15.4%), indicating a relatively smaller market size or lower demand compared to the other three countries.")
    st.markdown("- The United Kingdom and Germany have similar revenue shares (19.1% and 19%, respectively), suggesting comparable market sizes or demand levels.")


country_df = filtered_df.groupby(by = ["Country"], as_index = False)["Revenue"].sum()

with col1:
    with st.expander("View Category_Data"):
        st.write(category_df.style.background_gradient(cmap="Greens"))
        csv = category_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Category.CSV", mime="txt/csv", help= "Click here to download product category data as csv file" )

with col2:
    with st.expander("View Country Data"):
        st.write(country_df.style.background_gradient(cmap="Oranges_r"))
        csv = country_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Region.CSV", mime="txt/csv", help="Click here to download country data as csv file")


filtered_df["Month_Year"] = filtered_df["Date"].dt.to_period("M")


st.subheader('Time Series Analysis')
linechart_df = pd.DataFrame(filtered_df.groupby(by = filtered_df["Month_Year"].dt.strftime("%Y : %b"))["Revenue"].sum()).reset_index()
fig = px.line(linechart_df, x = "Month_Year", y= "Revenue", labels = {"Revenue": "Amount"}, height = 500, width= 1000, 
               template = "gridon")
st.plotly_chart(fig, use_container_width=True)
st.markdown("Insights: ")

st.markdown("- This Linechart shows the monthly revenue generated over a two-year period, from January 2015 to May 2016")
st.markdown("- In year 2015")
st.markdown("- Revenue increases steadily from January (230,549) to December (2,116,097) with a peak in August (1,248,185) and November (1,438,928).")
st.markdown("- The highest revenue months are August, November, and December, indicating a strong fourth quarter.")
st.markdown("- The lowest revenue months are January, February, and March, suggesting a slower start to the year.")

st.markdown("- In year 2016")
st.markdown("- Revenue increases significantly in the first quarter, with January (1,720,072),  February (1,734,376), and March (1,884,978) showing substantial growth.")
st.markdown("- The revenue peak shifts to June  (2,344,229) and May  (2,305,191) indicating a strong second quarter.")
st.markdown("- April (1,916,347)  and  July  (491,612) show a decline in revenue compared to the previous months.")

with st.expander("View TimeSeries Data"):
    st.write(linechart_df.T.style.background_gradient(cmap="magma_r"))
    csv = linechart_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data="csv", file_name="TimeSeries.CSV", mime="txt/csv", help="Click here to download TimeSeries data as csv file")

age_df = filtered_df.groupby(by = "Customer Age", as_index= False)["Revenue"].sum()

st.subheader('Customer Age Analysis')
age_df = pd.DataFrame(filtered_df.groupby(by = "Customer Age", as_index= False)["Revenue"].sum()).reset_index()
fig = px.line(age_df, x = "Customer Age", y= "Revenue", labels = {"Revenue": "Amount"}, height = 500, width= 1000, 
               template = "gridon")
st.plotly_chart(fig, use_container_width=True)
st.markdown("- This Linechart shows the revenue generated by customers of different ages.")
st.markdown("- Insights: ")
st.markdown("- The highest revenue is generated by customers in their late 20s to early 30s, with a peak at 28 years old (962,044).")
st.markdown("- Customers under 25 generate a substantial amount of revenue, with a steady increase from 17 to 24 years old.")
st.markdown("- Revenue decreases gradually after 40 years old, with a more significant drop-off after 50.")
st.markdown("- Although revenue declines after 40, customers in their 30s and 40s still generate a notable amount of revenue.")
st.markdown("- Customers above 60 generate relatively little revenue, with a sharp decline after 65.")
st.markdown("- There is no revenue generated from customers above 87 years old.")


with st.expander("View Age Data"):
    st.write(age_df.T.style.background_gradient(cmap="magma_r"))
    csv = age_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data="csv", file_name="Customer Age.CSV", mime="txt/csv", help="Click here to download customer age data as csv file")


st.subheader("Hierarchical View of Revenue Using Treemap")
fig = px.treemap(filtered_df, path= ["Country", "Product Category", "Sub Category"], values="Revenue", hover_data=["Revenue"], color="Sub Category")
fig.update_layout(width=800, height= 650)
st.plotly_chart(fig, use_container_width=True)
st.markdown("- A treemap analysis is a visualization tool used to display hierarchical data. In this case, it shows the revenue distribution across different product categories, subcategories, and countries.")
st.markdown("- Insights: ")
st.markdown("- Mountain Bikes generate the highest revenue across all countries, indicating a strong demand for this product category.")
st.markdown("- Accessories, such as Tires and Tubes, Helmets, and Bottles and Cages, contribute substantially to revenue, especially in the United States and Germany")
st.markdown("- Each country has unique preferences: ")
st.markdown("- United States: Mountain Bikes, Tires and Tubes, and Helmets.")
st.markdown("- United Kingdom: Mountain Bikes, Road Bikes, and Helmets.")
st.markdown("- France: Mountain Bikes, Road Bikes, and Tires and Tubes.")
st.markdown("- Germany: Mountain Bikes, Road Bikes, and Helmets")
st.markdown("- Jerseys, Shorts, and Vests are the top-selling clothing items, with Jerseys being the most popular across all countries.")

chart1, chart2 =st.columns((2))

quantity_df = filtered_df.groupby(by = "Quantity", as_index= False)["Revenue"].sum()
gender_df = filtered_df.groupby(by = "Customer Gender", as_index= False)["Revenue"].sum()

with chart1:
    st.subheader("Gender Wise Revenue")
    fig = px.bar(gender_df, x ="Customer Gender", y="Revenue",  text=["${:,.2f}".format(x) for x in gender_df["Revenue"]], template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)
    st.markdown("- Insights: ")
    st.markdown("- The revenue generated by males (11,411,942) is slightly higher than that generated by females (10,932,634), with a difference of 479,308.")
    st.markdown("- Females contribute approximately 48.8% of the total revenue, while males contribute around 51.2%.")
    st.markdown("- The revenue split is relatively close, indicating a relatively balanced customer base in terms of gender.")
    


with chart2:
    st.subheader("Quantity Wise Revenue")
    fig = px.bar(quantity_df, x ="Quantity", y="Revenue",  text=["${:,.2f}".format(x) for x in quantity_df["Revenue"]], template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

    st.markdown("- Insights: ")
    st.markdown("- Each additional unit sold generates slightly more revenue, indicating a positive correlation between quantity and revenue.")
    st.markdown("- The revenue growth rate slows down as the quantity increases (1 unit to 2 units: 2.4% increase, 2 units to 3 units: 0.8% increase).")
    st.markdown("- The incremental revenue gain from selling additional units is decreasing, suggesting diminishing returns.")
    


import plotly.figure_factory as ff
st.subheader(":point_right: Month Wise Sub Category Revenue Summary")
with st.expander("Summary Table"):
    sample_df = df[0:5][["Country", "State", "Product Category", "Revenue", "Profit", "Quantity"]]
    fig = ff.create_table(sample_df, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)


with st.expander("Month Wise Sub Category Revenue Table"):
    filtered_df["Month"] = filtered_df["Date"].dt.month_name()
    Sub_Category_Year = pd.pivot_table(data=filtered_df, values="Revenue", index=['Sub Category'], columns="Month")
    st.write(Sub_Category_Year.style.background_gradient(cmap="magma_r"))

data1 =px.scatter(filtered_df, x="Revenue", y="Profit", size="Quantity")
data1["layout"].update(title="Relationship between Revenue and Profit Using Scatter Plot.", titlefont=dict(size=20), 
                   xaxis= dict(title="Revenue", titlefont=dict(size=19)), yaxis= dict(title="Profit", titlefont=dict(size=19)))
st.plotly_chart(data1, use_container_width=True)

st.subheader("Recommendations: ")

st.markdown("- Review pricing strategies to ensure they align with customer demand and willingness to pay.")
st.markdown("- Focus marketing efforts on high-value customers who purchase multiple units.")
st.markdown("- Investigate customer behavior to understand why they purchase specific quantities and adjust strategies accordingly.")
st.markdown("- Consider offering discounts for bulk purchases to incentivize customers to buy more.")
st.markdown("- Engage with customers through various channels, such as social media, to understand their needs and preferences better.")








