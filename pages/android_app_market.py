import streamlit as st 
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns
import warnings
import matplotlib.pyplot as plt

def app():
    st.markdown('''
        # Google Play Store apps and reviews
        Mobile apps are everywhere. They are easy to create and can be lucrative. Because of these two factors, more and more apps are being developed. In this app, we will do a comprehensive analysis of the Android app market by comparing over ten thousand apps in Google Play across different categories. We'll look for insights in the data to devise strategies to drive growth and retention.
        Let's take a look at the data, which consists of two files:
        - **apps.csv**: contains all the details of the applications on Google Play. There are 13 features that describe a given app
        - **user_reviews.csv**: contains 100 reviews for each app. The text in each review has been pre-processed and attributed with three new features: Sentiment (Positive, Negative or Neutral), Sentiment Polarity and Sentiment Subjectivity.
    ''')


    # Load app.csv
    apps_with_duplicates = pd.read_csv('./pages/datasets/apps.csv', index_col=0)
    # Load user_reviews.csv
    reviews_df = pd.read_csv('./pages/datasets/user_reviews.csv')

    # Drop duplicates from apps_with_duplicates
    apps = apps_with_duplicates.drop_duplicates(subset="App")

    # List of characters to remove
    chars_to_remove = ["+", "$", ","]
    # List of column names to clean
    cols_to_clean = ["Installs", "Price", "Content Rating"]

    # Loop for each column in cols_to_clean
    for col in cols_to_clean:
        # Loop for each char in chars_to_remove
        for char in chars_to_remove:
            # Replace the character with an empty string
            apps[col] = apps[col].apply(lambda x: x.replace(char,''))
            
    st.markdown('### The total number of apps and head of dataset')
    st.write('Total number of apps in the dataset = ', apps["App"].value_counts().sum())
    # Have a look at 10 head's row
    st.write(apps.head(n=10))

    # Convert Installs to float data type
    apps["Installs"] = apps["Installs"].astype(float)

    # Convert Price to float data type
    apps["Price"] = apps["Price"].astype(float)

    st.markdown('''
    ## Exploring app categories
    With more than 1 billion active users in 190 countries around the world, Google Play continues to be an important distribution platform to build a global audience. For businesses to get their apps in front of users, it's important to make them more quickly and easily discoverable on Google Play. To improve the overall search experience, Google has introduced the concept of grouping apps into categories.

    This brings us to the following questions:

    - Which category has the highest share of (active) apps in the market?
    - Is any specific category dominating the market?
    - Which categories have the fewest number of apps?
    ''')

    # Print the total number of unique categories
    num_categories = len(apps['Category'].unique())
    print('Number of categories = ', num_categories)

    # Count the number of apps in each 'Category'. 
    num_apps_in_category = apps.groupby('Category')['Category'].count()

    # Sort num_apps_in_category in descending order based on the count of apps in each category
    sorted_num_apps_in_category = num_apps_in_category.sort_values(ascending=False)
    print(sorted_num_apps_in_category.head())

    fig_1 = go.Figure(data=[go.Bar(
            x = num_apps_in_category.index,
            y = num_apps_in_category.values)])

    fig_1.update_layout(
        xaxis_title="Category",
        yaxis_title="N° of App",
    )

    st.plotly_chart(fig_1, use_container_width=True)

    st.markdown('''
        ## Distribution of app ratings
        After having witnessed the market share for each category of apps, let's see how all these apps perform on an average. App ratings (on a scale of 1 to 5) impact the discoverability, conversion of apps as well as the company's overall brand image. Ratings are a key performance indicator of an app.

        From our research, we found that the average volume of ratings across all app categories is 4.17. The histogram plot is skewed to the left indicating that the majority of the apps are highly rated with only a few exceptions in the low-rated apps.
    ''')

    # Average rating of apps
    avg_app_rating = apps['Rating'].mean()
    st.write('Average app rating = ', avg_app_rating)

    # Distribution of apps according to their ratings
    fig_2 = go.Figure(data=[go.Histogram(x=apps['Rating'])])

    fig_2.update_layout(
        xaxis_title="Rating",
        yaxis_title="N° of App per Rating",
    )

    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown('''
    ## Size and price of an app
    Let's now examine app size and app price. For size, if the mobile app is too large, it may be difficult and/or expensive for users to download. Lengthy download times could turn users off before they even experience your mobile app. Plus, each user's device has a finite amount of disk space. For price, some users expect their apps to be free or inexpensive. These problems compound if the developing world is part of your target market; especially due to internet speeds, earning power and exchange rates.

    How can we effectively come up with strategies to size and price our app?

    - Does the size of an app affect its rating?
    - Do users really care about system-heavy apps or do they prefer light-weighted apps?
    - Does the price of an app affect its rating?
    - Do users always prefer free apps over paid apps?

    We find that the majority of top rated apps (rating over 4) range from 2 MB to 20 MB. We also find that the vast majority of apps price themselves under $10.
    ''')


    sns.set_style("darkgrid")
    warnings.filterwarnings("ignore")

    # Select rows where both 'Rating' and 'Size' values are present (ie. the two values are not null)
    apps_with_size_and_rating_present = apps[apps['Rating'].notnull() & apps['Size'].notnull()]
    #print(apps_with_size_and_rating_present.sample(n=5))

    # Subset for categories with at least 250 apps
    large_categories = apps_with_size_and_rating_present.groupby('Category').filter(lambda x: len(x) >= 250)
    #print(large_categories.head())

    # Plot size vs. rating
    fig_3 = sns.jointplot(x = large_categories['Size'], y = large_categories['Rating'])
    st.pyplot(fig_3, use_container_width=True)

    # Select apps whose 'Type' is 'Paid'
    paid_apps = apps[apps['Type'] == 'Paid']

    # Plot price vs. rating
    fig_4 = sns.jointplot(x = paid_apps['Price'], y = paid_apps['Rating']) 
    st.pyplot(fig_4, use_container_width=True)

    st.markdown('''
    ## Relation between app category and app price
    So now comes the hard part. How are companies and developers supposed to make ends meet? What monetization strategies can companies use to maximize profit? The costs of apps are largely based on features, complexity, and platform.

    There are many factors to consider when selecting the right pricing strategy for your mobile app. It is important to consider the willingness of your customer to pay for your app. A wrong price could break the deal before the download even happens. Potential customers could be turned off by what they perceive to be a shocking cost, or they might delete an app they’ve downloaded after receiving too many ads or simply not getting their money's worth.

    Different categories demand different price ranges. Some apps that are simple and used daily, like the calculator app, should probably be kept free. However, it would make sense to charge for a highly-specialized medical app that diagnoses diabetic patients. Below, we see that **Medical and Family** apps are the most expensive. Some medical apps extend even up to \$80! All game apps are reasonably priced below $20.
    ''')

    fig_5, ax = plt.subplots()
    fig_5.set_size_inches(15, 8)

    # Select a few popular app categories
    popular_app_cats = apps[apps.Category.isin(['GAME', 'FAMILY', 'PHOTOGRAPHY',
                                                'MEDICAL', 'TOOLS', 'FINANCE',
                                                'LIFESTYLE','BUSINESS'])]

    # Examine the price trend by plotting Price vs Category
    ax = sns.stripplot(x = popular_app_cats['Price'], y = popular_app_cats['Category'], jitter=True, linewidth=1)
    ax.set_title('App pricing trend across categories')
    st.pyplot(fig_5, use_container_width=True)


    st.markdown('### Apps whose Price is greater than 200')
    apps_above_200 = apps[apps['Price'] > 200]
    apps_above_200[['Category', 'App', 'Price']]
    st.write(apps_above_200[['Category', 'App', 'Price']])

    st.markdown('''
    ## Filter out "junk" apps

    It looks like a bunch of the really expensive apps are "junk" apps. That is, apps that don't really have a purpose. Some app developer may create an app called **I Am Rich Premium** or **most expensive app (H)** just for a joke or to test their app development skills. Some developers even do this with malicious intent and try to make money by hoping people accidentally click purchase on their app in the store.

    Let's filter out these junk apps and re-do our visualization.
    ''')

    # Select apps priced below $100
    apps_under_100 = apps[apps['Price'] < 100]

    fig_6, ax = plt.subplots()
    fig_6.set_size_inches(15, 8)

    # Examine price vs category with the authentic apps (apps_under_100)
    ax = sns.stripplot(x = apps_under_100['Price'], y = apps_under_100['Category'], data =apps_under_100, jitter = True, linewidth = 1)
    ax.set_title('App pricing trend across categories after filtering for junk apps')
    st.pyplot(fig_6, use_container_width=True)

    st.markdown('''
    ## Popularity of paid apps vs free apps
    For apps in the Play Store today, there are five types of pricing strategies: free, freemium, paid, paymium, and subscription. Let's focus on free and paid apps only. Some characteristics of free apps are:

    - Free to download.
    - Main source of income often comes from advertisements.
    - Often created by companies that have other products and the app serves as an extension of those products.
    - Can serve as a tool for customer retention, communication, and customer service.

    Some characteristics of paid apps are:

    - Users are asked to pay once for the app to download and use it.
    - The user can't really get a feel for the app before buying it.

    Are paid apps installed as much as free apps? It turns out that paid apps have a relatively lower number of installs than free apps, though the difference is not as stark as I would have expected!
    ''')

    trace0 = go.Box(
        # Data for paid apps
        y = apps[apps['Type'] == 'Paid']['Installs'],
        name = 'Paid'
    )

    trace1 = go.Box(
        # Data for free apps
        y = apps[apps['Type'] == 'Free']['Installs'],
        name = 'Free'
    )

    layout = go.Layout(
        title = "Number of downloads of paid apps vs. free apps",
        yaxis = dict(title = "Log number of downloads",
                    type = 'log',
                    autorange = True)
    )

    # Add trace0 and trace1 to a list for plotting
    fig_6 = [trace0, trace1]
    st.plotly_chart({'data': fig_6, 'layout': layout}, use_container_width=True)

    st.markdown('''
    ## Sentiment analysis of user reviews

    Mining user review data to determine how people feel about your product, brand, or service can be done using a technique called sentiment analysis. User reviews for apps can be analyzed to identify if the mood is positive, negative or neutral about that app. For example, positive words in an app review might include words such as 'amazing', 'friendly', 'good', 'great', and 'love'. Negative words might be words like 'malware', 'hate', 'problem', 'refund', and 'incompetent'.

    By plotting sentiment polarity scores of user reviews for paid and free apps, we observe that free apps receive a lot of harsh comments, as indicated by the outliers on the negative y-axis. Reviews for paid apps appear never to be extremely negative. This may indicate something about app quality, i.e., paid apps being of higher quality than free apps on average. The median polarity score for paid apps is a little higher than free apps, thereby syncing with our previous observation.

    In this work, we analyzed over ten thousand apps from the Google Play Store. We can use our findings to inform our decisions should we ever wish to create an app ourselves.
    ''')

    # Join the two dataframes
    merged_df = apps.merge(reviews_df, on='App')

    # Drop NA values from Sentiment and Review columns
    merged_df = merged_df.dropna(subset = ['Sentiment', 'Review'])

    sns.set_style('ticks')
    fig_7, ax = plt.subplots()
    fig_7.set_size_inches(11, 8)

    # User review sentiment polarity for paid vs. free apps
    ax = sns.boxplot(x = merged_df['Type'] , y = merged_df['Sentiment_Polarity'], data = merged_df)
    ax.set_title('Sentiment Polarity Distribution')
    st.pyplot(fig_7)