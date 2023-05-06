import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Mutual Fund Analysis')

df = pd.read_csv('comprehensive_mutual_funds_data.csv')

# imputing missing values
df['returns_3yr'] = df.groupby('category')['returns_3yr'].apply(lambda x: x.fillna(x.mean()))
df['returns_5yr'] = df.groupby('category')['returns_5yr'].apply(lambda x: x.fillna(x.mean()))


# create a function to make a category columns with above fund size
def fund_size_group(fund_size):
    if 0.0 <= fund_size <= 500.0:
        return '0-500'
    elif 500.0 < fund_size <= 750.0:
        return '500-750'
    elif 750.0 < fund_size <= 2000.0:
        return '750-2000'
    elif 2000.0 < fund_size <= 5000.0:
        return '2000-5000'
    elif 5000.0 < fund_size <= 10000.0:
        return '5000-10000'
    elif 10000.0 < fund_size <= 50000.0:
        return '10000-50000'
    else:
        return '>50000'


# create a column with above fund size group
df['fund_size_group'] = df['fund_size_cr'].apply(fund_size_group)


# overall analysis
def load_overall_analysis():
    st.title('Overall Analysis of Mutual Funds- March 2023')

    # number of schemes
    total_schemes = df['scheme_name'].nunique()

    # number of AMC
    total_amc = df['amc_name'].nunique()

    # total funds invested
    total_investment = round(df['fund_size_cr'].sum())

    # average funds raised by amc
    avg_fund_amc = round(df['fund_size_cr'].sum() / df['amc_name'].nunique())

    # average fund size of scheme
    avg_fund_scheme = round(df['fund_size_cr'].sum() / df['scheme_name'].nunique())

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric('Number of Schemes active', str(total_schemes))
    with col2:
        st.metric('Number of AMCs', str(total_amc))
    with col3:
        st.metric('Total Funds raised by AMC', str(total_investment) + ' Cr')
    with col4:
        st.metric('Average Funds raised by AMC', str(avg_fund_amc) + ' Cr')
    with col5:
        st.metric('Average Fund size of scheme', str(avg_fund_scheme) + ' Cr')

    # category wise analysis
    st.header('Category Wise Analysis')
    col1, col2 = st.columns(2)

    with col1:
        # category wise fund size
        category_series_amt = df.groupby('category')['fund_size_cr'].sum().sort_values(ascending=True)

        st.subheader('Funds Size by Category')
        fig, ax = plt.subplots()
        ax.barh(category_series_amt.index, category_series_amt.values)
        plt.xlabel('Values in Crore')
        st.pyplot(fig)

    with col2:
        # category wise scheme size
        category_series_count = df.groupby('category')['scheme_name'].count().sort_values(ascending=True)

        st.subheader('Number of Schemes in Category')
        fig, ax = plt.subplots()
        ax.barh(category_series_count.index, category_series_count.values)
        plt.xlabel('Number of Schemes')
        st.pyplot(fig)

    col1, col2, col3 = st.columns(3)

    with col1:
        # category wise 1 year returns
        category_series_return_1 = df.groupby('category')['returns_1yr'].mean().sort_values(ascending=True)

        st.subheader('Average 1 Year Returns By Category')
        fig, ax = plt.subplots()
        ax.barh(category_series_return_1.index, category_series_return_1.values)
        plt.xlabel('Average 1 Year Returns')
        st.pyplot(fig)

    with col2:
        # category wise 3 year returns
        category_series_return_3 = df.groupby('category')['returns_3yr'].mean().sort_values(ascending=True)

        st.subheader('Average 3 Year Returns By Category')
        fig, ax = plt.subplots()
        ax.barh(category_series_return_3.index, category_series_return_3.values)
        plt.xlabel('Average 3 Year Returns')
        st.pyplot(fig)

    with col3:
        # category wise 5 year returns
        category_series_return_5 = df.groupby('category')['returns_5yr'].mean().sort_values(ascending=True)

        st.subheader('Average 5 Year Returns By Category')
        fig, ax = plt.subplots()
        ax.barh(category_series_return_5.index, category_series_return_5.values)
        plt.xlabel('Average 5 Year Returns')
        st.pyplot(fig)

    # sub-category wise analysis
    st.header('Sub-Category Wise Analysis')
    col1, col2 = st.columns(2)

    with col1:
        # sub_category wise fund size
        sub_category_series_amt = df.groupby('sub_category')['fund_size_cr'].sum().sort_values(ascending=True)

        st.subheader('Fund Size By Sub-Category')
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.barh(sub_category_series_amt.index, sub_category_series_amt.values)
        ax.tick_params(labelsize=20)
        plt.xlabel('Values in Crore', fontsize=18)
        st.pyplot(fig)

    with col2:
        # sub_category wise scheme size
        sub_category_series_count = df.groupby('sub_category')['scheme_name'].count().sort_values(ascending=True)

        st.subheader('Number of Schemes in Sub-Category')
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.barh(sub_category_series_count.index, sub_category_series_count.values)
        ax.tick_params(labelsize=20)
        plt.xlabel('Number of Schemes', fontsize=18)
        st.pyplot(fig)

    # expense ratio analysis
    st.header('Expense Ratio Analysis')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Expense Ratio Variation with Fund Size Group')
        fig1, ax1 = plt.subplots()
        ax1.barh(y=df['fund_size_group'], width=df['expense_ratio'])
        plt.ylabel('Fund Size Group in Crores')
        plt.xlabel('Expense Ratio in %')
        st.pyplot(fig1)

    with col2:
        st.subheader('Average Expense Ratio variation with Category')
        fig2, ax2 = plt.subplots()
        expense_ratio_category = df.groupby('category')['expense_ratio'].mean().sort_values()
        ax2.barh(expense_ratio_category.index, expense_ratio_category.values)
        plt.xlabel('Expense Ratio in %')
        st.pyplot(fig2)

    # top 5 Schemes Category Wise
    st.header('Top 5 Schemes Category & Sub-Category Wise')
    option_top = st.selectbox('Select One', df['category'].unique())
    option_bot = st.selectbox('Select One', df[df['category'] == option_top]['sub_category'].unique())

    top_scheme = df[df['sub_category'] == option_bot].sort_values(by='returns_5yr', ascending=False).head()
    top_scheme = top_scheme[['scheme_name', 'returns_5yr']].sort_values(by='returns_5yr', ascending=True)

    fig, ax = plt.subplots()
    ax.barh(top_scheme.scheme_name, top_scheme.returns_5yr)
    plt.xlabel('5 Year Returns')

    st.pyplot(fig)

    # top 5 fund manager by aum
    st.header('Fund Manager Analysis')
    top_5_fund_manager_aum = df.groupby('fund_manager')['fund_size_cr'].sum().sort_values(ascending=False).head()
    top_5_fund_manager_aum = top_5_fund_manager_aum.sort_values(ascending=True)

    # top 5 fund manager by no of schemes
    top_5_fund_manager_scheme = df.groupby('fund_manager')['scheme_name'].count().sort_values(ascending=False).head()
    top_5_fund_manager_scheme = top_5_fund_manager_scheme.sort_values(ascending=True)

    col1, col2 = st.columns(2)
    with col1:
        st.header('Top 5 Fund Manager by AUM')
        fig, ax = plt.subplots()
        ax.barh(top_5_fund_manager_aum.index, top_5_fund_manager_aum.values)
        plt.xlabel('Amount in Crores')

        st.pyplot(fig)

    with col2:
        st.header('Top 5 Fund Manager by Schemes')
        fig, ax = plt.subplots()
        ax.barh(top_5_fund_manager_scheme.index, top_5_fund_manager_scheme.values)
        plt.xlabel('Number of Schemes')
        st.pyplot(fig)

    # AMC analysis
    st.header('AMC Analysis')

    # top 5 AMC by AUM
    top_5_amc_fund = df.groupby('amc_name')['fund_size_cr'].sum().sort_values(ascending=False).head()
    top_5_amc_fund = top_5_amc_fund.sort_values(ascending=True)

    # top 5 AMC by number of schemes
    top_5_amc_scheme = df.groupby('amc_name')['scheme_name'].count().sort_values(ascending=False).head()
    top_5_amc_scheme = top_5_amc_scheme.sort_values(ascending=True)

    col1, col2 = st.columns(2)

    with col1:
        st.header('Top 5 AMC by AUM')
        fig, ax = plt.subplots()
        ax.barh(top_5_amc_fund.index, top_5_amc_fund.values)
        plt.xlabel('Amount in Crores')
        st.pyplot(fig)

    with col2:
        st.header('Top 5 AMC by Schemes')
        fig, ax = plt.subplots()
        ax.barh(top_5_amc_scheme.index, top_5_amc_scheme.values)
        plt.xlabel('Number of Schemes')
        st.pyplot(fig)


# fund manager analysis
def load_fund_manager_analysis(fund_manager):
    # Fund manager working in AMC
    amc_name = df[df['fund_manager'] == fund_manager]['amc_name']
    amc_name = amc_name.iloc[0]

    st.title(fund_manager)
    st.subheader(amc_name)

    # number of schemes managed by fund manager
    num_scheme = df[df['fund_manager'] == fund_manager]['scheme_name'].nunique()

    # Funds managed
    fund_manager_fund_size = df[df['fund_manager'] == fund_manager]
    fund_manager_fund_size = fund_manager_fund_size['fund_size_cr'].sum()

    # highest return
    highest_return = df[df['fund_manager'] == fund_manager]['returns_1yr'].sort_values(ascending=False).iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric('Schemes', num_scheme)
    with col2:
        st.metric('AUM', str(fund_manager_fund_size) + ' Cr')
    with col3:
        st.metric('Highest 1 Year Return', highest_return)

    # schemes
    scheme_fund_managed = df[df['fund_manager'] == fund_manager][
        ['scheme_name', 'expense_ratio', 'rating', 'category', 'sub_category', 'returns_1yr',
         'returns_3yr', 'returns_5yr']]
    st.header('Schemes Managed')
    st.dataframe(scheme_fund_managed)


# amc analysis
def load_amc_analysis(amc):
    st.title(amc)

    amc_df = df[df['amc_name'] == amc]

    # aum size
    aum = amc_df['fund_size_cr'].sum()

    # no of scheme
    amc_scheme = amc_df['scheme_name'].count()

    # no of fund manager
    amc_mgr = amc_df['fund_manager'].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric('AUM', str(aum) + ' Cr')
    with col2:
        st.metric('No. of Schemes', str(amc_scheme))
    with col3:
        st.metric('No. of Fund Manager', str(amc_mgr))

    # creating dataframe for the selected category
    st.header('Schemes By Category')
    sel_opt = st.selectbox('Select One',df['category'].unique())

    st.dataframe(amc_df[amc_df['category'] == sel_opt][['scheme_name', 'expense_ratio', 'rating', 'category', 'sub_category','fund_manager',
                                                        'returns_1yr', 'returns_3yr', 'returns_5yr']])


st.sidebar.title('Mutual Fund Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Fund Manager Analysis', 'AMC Analysis'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Fund Manager Analysis':
    selected_fund_manager = st.sidebar.selectbox('Select Fund Manager', sorted(set(df['fund_manager'])))
    load_fund_manager_analysis(selected_fund_manager)

else:
    selected_amc = st.sidebar.selectbox('Select AMC Name', sorted(set(df['amc_name'])))
    load_amc_analysis(selected_amc)
