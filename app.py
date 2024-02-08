import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')

#url = "https://drive.google.com/file/d/1oWNd33JXCK8OLVHTueFuEA-jbW9GXwPC/view?usp=drive_link"
df = pd.read_csv(r"C:\Users\jayma\OneDrive\One drive backup\Startup Funding project\startup_cleaned.csv")
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups',num_startups)

    col5,col6 = st.columns(2)

    with col5:

        st.subheader('MoM graph')
        selected_option = st.selectbox('Select Type',['Total','Count'])
        if selected_option == 'Total':
            temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        else:
            temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

        temp_df['x_axis'] =  temp_df['year'].astype('str')

        fig3, ax3 = plt.subplots()
        ax3.bar(temp_df['x_axis'], temp_df['amount'])

        st.pyplot(fig3)

    with col6:
        st.subheader("Top Sector Analysis")
        top_sector = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
        fig4, ax4 = plt.subplots()
        ax4.pie(top_sector,labels = top_sector.index,autopct="%0.01f%%")

        st.pyplot(fig4)

    col7,col8 = st.columns(2)
    with col7:
        st.subheader("Most Type of Funding")
        funding_type = df.groupby('round')['amount'].sum().sort_values(ascending = False).head()
        st.dataframe(funding_type)

    with col8:
        st.subheader("Top Startups")
        top_startup = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.dataframe(top_startup)

    col9,col10 = st.columns(2)
    with col9:
        st.subheader("Top Investors")
        top_investors = df.groupby('investors')['amount'].sum().sort_values(ascending=False).head()
        st.dataframe(top_investors)

    with col10:
        st.subheader("Top cities on the basis of Investemnt")
        df['city'].replace('Bangalore', 'Bengaluru', inplace=True)
        top_citites = df.groupby('city')['amount'].sum().sort_values(ascending = False).head()
        st.dataframe(top_citites)

def load_startup_details(startup):
    st.title(startup)
    # load the recent investments
    five_df = df[df['startup'].str.contains(startup)].head()[['investors', 'vertical','amount','round']]
    st.subheader('Top Investors in startup')
    st.dataframe(five_df)

    col11,col12 = st.columns(2)
    with col11:

        df['year'] = df['date'].dt.year
        year_series = df[df['startup'].str.contains(startup)].groupby('year')['amount'].sum()

        st.subheader('YoY Investment')
        fig5, ax5 = plt.subplots()
        ax5.plot(year_series.index,year_series.values)

        st.pyplot(fig5)

    with col12:
        total_value = df[df['startup'].str.contains(startup)]['amount'].sum()
        st.subheader("Total Valuation",)
        st.metric('In crores',str(total_value))





def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    print(df.info())

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)
    
else:
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

