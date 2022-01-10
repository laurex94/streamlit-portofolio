import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

def app():

    st.markdown('''
        # Investigating Netflix Movies and Guest Stars in The Office

        Netflix! What started in 1997 as a DVD rental service has since exploded into the largest entertainment/media company by market capitalization, boasting over 200 million subscribers as of January 2021.

        Given the large number of movies and series available on the platform, it is a perfect opportunity to dive into the entertainment industry. For their first order of business, they have been performing some analyses, and they believe that the average duration of movies has been declining.

        As evidence of this, they have provided us with the following information. For the years from 2011 to 2020, the average movie durations are 103, 101, 99, 100, 100, 95, 95, 96, 93, and 90, respectively.
    ''')

    # Read in the CSV as a DataFrame
    netflix_df = pd.read_csv('./pages/datasets/netflix_data.csv')

    # Create the years and durations lists
    years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    durations = [103, 101, 99, 100, 100, 95, 95, 96, 93, 90]

    # Create a dictionary with the two lists
    movie_dict = {"years": years, "durations": durations}

    # Create a DataFrame from the dictionary
    durations_df = pd.DataFrame(movie_dict)

    fig_1, ax_1= plt.subplots()

    # Draw a line plot of release_years and durations
    ax_1 = plt.plot(durations_df["years"], durations_df["durations"])

    # Create a title
    plt.title("Netflix Movie Durations 2011-2020")
    plt.xlabel('Release Year')
    plt.ylabel('Duration (min)')

    # Show the plot
    st.pyplot(fig_1)

    st.markdown('''
        ## Loading the rest of the data

        Well, it looks like there is something to the idea that movie lengths have decreased over the past ten years! But equipped only with our aggregations, we're limited in the further explorations we can perform. There are a few questions about this trend that we are currently unable to answer, including:

        - What does this trend look like over a longer period of time?
        - Is this explainable by something like the genre of entertainment?
        
        We need to access to the CSV file and create a DataFrame with our data.
    ''')

    st.write(netflix_df.head())

    st.markdown('''
        ## Filtering for movies!

        Now we can dive in and start looking at movie lengths.

        Looking at the first five rows of our new DataFrame, we notice a column type. Scanning the column, it's clear there are also TV shows in the dataset! Moreover, the duration column we planned to use seems to represent different values depending on whether the row is a movie or a show (perhaps the number of minutes versus the number of seasons)?

        Filtering our data, we selected rows where type is Movie. While we're at it, we don't need information from all of the columns, so let's create a new DataFrame containing only title, country, genre, release_year, and duration.
    ''')

    # Subset the DataFrame for type "Movie"
    netflix_df_movies_only = netflix_df.loc[netflix_df['type'] == 'Movie']

    # Select only the columns of interest
    netflix_movies_col_subset = netflix_df_movies_only[['title', 'country', 'genre', 'release_year', 'duration']]

    # Print the first five rows of the new DataFrame
    st.write(netflix_movies_col_subset[:5])

    st.markdown('''
        ## Creating a scatter plot

        Let's try visualizing the data again to inspect the data over a longer range of time.
    ''')

    # Create the scatter plot figure 

    fig_2, ax_2 = plt.subplots()
    ax_2 = sns.scatterplot(data = netflix_df_movies_only, x = "release_year", y = "duration")

    # Set title
    plt.title('Movie Duration by Year of Release')
    # Set x-axis label
    plt.xlabel('Release Year')
    # Set y-axis label
    plt.ylabel('Duration')

    # Show the plot
    st.pyplot(fig_2)

    st.markdown('''
        ## Digging deeper
        
        This is already much more informative than the simple plot we created with our first data. We can also see that, while newer movies are overrepresented on the platform, many short movies have been released in the past two decades.

        Upon further inspection, something else is going on. Some of these films are under an hour long! Let's filter our DataFrame for movies with a duration under 60 minutes and look at the genres. This might give us some insight into what is dragging down the average.
    ''')

    # Filter for durations shorter than 60 minutes
    short_movies = netflix_movies_col_subset.loc[netflix_movies_col_subset['duration'] < 60]

    # Print the first 20 rows of short_movies
    st.write(short_movies[0:20])

    st.markdown('''
        ## Marking non-feature films

        Interesting! It looks as though many of the films that are under 60 minutes fall into genres such as "Children", "Stand-Up", and "Documentaries". This is a logical result, as these types of films are probably often shorter than 90 minute Hollywood blockbuster.

        We could eliminate these rows from our DataFrame and plot the values again. But another interesting way to explore the effect of these genres on our data would be to plot them, but mark them with a different color.
    ''')

    # Define an empty list
    colors = []

    # Iterate over rows of netflix_movies_col_subset
    for label,row in netflix_movies_col_subset.iterrows():
        if row["genre"] == "Children":
            colors.append("red")
        elif row["genre"] == "Documentaries":
            colors.append("blue")
        elif row["genre"] == "Stand-Up":
            colors.append("green")
        else:
            colors.append("black")

    # Set the figure style and initalize a new figure
    plt.style.use('fivethirtyeight')
    fig_3, ax_3 = plt.subplots()

    # Create a scatter plot of duration versus release_year
    ax_3 = plt.scatter(netflix_df_movies_only[["release_year"]], netflix_df_movies_only[["duration"]], color = colors)

    # Create a title and axis labels
    plt.title("Movie duration by year of release")
    plt.xlabel("Release year")
    plt.ylabel("Duration (min)")

    # Show the plot
    st.pyplot(fig_3)

    st.markdown('''
        These allowed us to visualize the genres responsible for the decrease in the average length of the films.
        
        Well, as we suspected, non-typical genres such as children's movies (red) and documentaries (blue) are all clustered around the bottom half of the plot.
    ''')

