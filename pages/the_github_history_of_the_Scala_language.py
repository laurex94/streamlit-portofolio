import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objs as go

def app():
    st.markdown('''
        # Scala's real-world project repository data

        With almost 30k commits and a history spanning over ten years, Scala is a mature programming language. It is a general-purpose programming language that has recently become another prominent language for data scientists.

        Scala is also an open source project. Open source projects have the advantage that their entire development histories -- who made changes, what was changed, code reviews, etc. -- are publicly available.

        We're going to read in, clean up, and visualize the real world project repository of Scala that spans data from a version control system (Git) as well as a project hosting site (GitHub). We will find out who has had the most influence on its development and who are the experts.

        The dataset we will use, which has been previously mined and extracted from GitHub, is comprised of three files:

        - **pulls_2011-2013.csv**: contains the basic information about the pull requests, and spans from the end of 2011 up to (but not including) 2014.
        - **pulls_2014-2018.csv** contains identical information, and spans from 2014 up to 2018.
        - **pull_files.csv** contains the files that were modified by each pull request.
    ''')

    # Loading in the data
    pulls_one = pd.read_csv('./pages/datasets/pulls_2011-2013.csv')
    pulls_two = pd.read_csv('./pages/datasets/pulls_2014-2018.csv')
    pull_files = pd.read_csv('./pages/datasets/pull_files.csv')

    # Append pulls_one to pulls_two
    pulls = pulls_one.append(pulls_two, ignore_index=True)

    # Convert the date for the pulls object
    pulls['date'] = pd.to_datetime(pulls['date'], utc=True)

    # Merge the two DataFrames
    data = pulls.merge(pull_files, on='pid')

    st.markdown('''
    ##  Is the project still actively maintained?

    The activity in an open source project is not very consistent. Some projects might be active for many years after the initial release, while others can slowly taper out into oblivion. Before committing to contributing to a project, it is important to understand the state of the project. Is development going steadily, or is there a drop? Has the project been abandoned altogether?

    The data used in this project was collected in January of 2018. We are interested in the evolution of the number of contributions up to that date.

    For Scala, we will do this by plotting a chart of the project's activity. We will calculate the number of pull requests submitted each year during the project's lifetime. We will then plot these numbers to see the trend of contributions.
    ''')

    # Create a column that will store the month
    data['month'] = data['date'].dt.month

    # Create a column that will store the year
    data['year'] = data['date'].dt.year

    # Show the plot
    fig1, ax1 = plt.subplots()
    data.groupby('year')['pid'].count().plot(kind='bar', ax=ax1, figsize = (12,4))
    ax1.set_xlabel('Year')
    ax1.set_ylabel('N° of contibutions')
    ax1.set_title('Number of contributions per year')
    st.pyplot(fig1)

    st.markdown('''
    ## Is there camaraderie in the project?

    The organizational structure varies from one project to another, and it can influence your success as a contributor. A project that has a very small community might not be the best one to start working on. The small community might indicate a high barrier of entry. This can be caused by several factors, including a community that is reluctant to accept pull requests from "outsiders," that the code base is hard to work with, etc. However, a large community can serve as an indicator that the project is regularly accepting pull requests from new contributors. Such a project would be a good place to start.

    In order to evaluate the dynamics of the community, we will plot a bar chart of the number of pull requests submitted by each user. The plot shows that there are few people that only contribute a small number of pull requests can be used as in indicator that the project is not welcoming of new contributors.
    ''')
    fig2 = go.Figure()
    x2 = data.groupby('user')['pid'].count()
    fig2.add_trace(go.Bar(x=x2.index, y=x2, name='Mean'))
    fig2.update_layout(
        xaxis_title="Users",
        yaxis_title="N° of contributions",
    )
    
    #fig.show()
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('''
    ## What files were changed in the last ten pull requests?

    Choosing the right place to make a contribution is as important as choosing the project to contribute to. Some parts of the code might be stable, some might be dead. Contributing there might not have the most impact. Therefore it is important to understand the parts of the system that have been recently changed. This allows us to pinpoint the "hot" areas of the code where most of the activity is happening. Focusing on those parts might not the most effective use of our times.
    ''')

    # Identify the last 10 pull requests
    last_10 = pulls.sort_values(by = 'date').tail(10)
    joined_pr = pull_files.merge(last_10, on='pid')
    st.write(joined_pr)

    st.markdown('''
    ## Who made the most pull requests to a given file?

    When contributing to a project, we might need some guidance. We might find ourselves needing some information regarding the codebase. It is important direct any questions to the right person. Contributors to open source projects generally have other day jobs, so their time is limited. It is important to address our questions to the right people. One way to identify the right target for our inquiries is by using their contribution history.

    We identified *src/compiler/scala/reflect/reify/phases/Calculate.scala* as being recently changed. We are interested in the top 3 developers who changed that file. Those developers are the ones most likely to have the best understanding of the code.
    ''')

    # This is the file we are interested in:
    file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

    # Identify the commits that changed the file
    file_pr = data[data['file'] == file]

    # Count the number of changes made by each developer
    author_counts = file_pr.groupby('user').count()

    # Print the top 3 developers
    st.write(author_counts.nlargest(3, 'file'))

    st.markdown('''
    ## Who made the last ten pull requests on a given file?

    Open source projects suffer from fluctuating membership. This makes the problem of finding the right person more challenging: the person has to be knowledgeable and still be involved in the project. A person that contributed a lot in the past might no longer be available (or willing) to help. To get a better understanding, we need to investigate the more recent history of that particular part of the system.

    We will look at the history of *src/compiler/scala/reflect/reify/phases/Calculate.scala*.
    ''')

    # Select the pull requests that changed the target file
    file_pr = pull_files[pull_files['file'] == file]

    # Merge the obtained results with the pulls DataFrame
    joined_pr = pulls.merge(file_pr, on='pid')

    # Find the users of the last 10 most recent pull requests
    users_last_10 = joined_pr.nlargest(10, 'date')

    # Printing the results
    st.write(users_last_10)

    st.markdown('''
    ## The pull requests of two special developers

    Now that we have identified two potential contacts in the projects, we need to find the person who was most involved in the project in recent times. That person is most likely to answer our questions. For each calendar year, we are interested in understanding the number of pull requests the authors submitted. This will give us a high-level image of their contribution trend to the project.
    ''')
    # The developers we are interested in
    authors = ['xeno-by', 'soc']

    # Get all the developers' pull requests
    by_author = pulls[pulls['user'].isin(authors)]

    # Count the number of pull requests submitted each year
    counts = by_author.groupby(['user', by_author['date'].dt.year]).agg({'pid': 'count'}).reset_index()

    # Convert the table to a wide format
    counts_wide = counts.pivot_table(index='date', columns='user', values='pid', fill_value=0)

    # Plot the results
    fig3, ax3 = plt.subplots()
    counts_wide.plot(kind='bar', ax=ax3)
    ax3.set_xlabel('Year')
    ax3.set_ylabel('N° of pull requests')
    ax3.set_title('Number of contributions per year')
    st.pyplot(fig3)

    st.markdown('''
    ## Visualizing the contributions of each developer

    As mentioned before, it is important to make a distinction between the global expertise and contribution levels and the contribution levels at a more granular level (file, submodule, etc.) In our case, we want to see which of our two developers of interest have the most experience with the code in a given file (*src/compiler/scala/reflect/reify/phases/Calculate.scala*). We will measure experience by the number of pull requests submitted that affect that file and how recent those pull requests were submitted.
    ''')

    # Select the pull requests submitted by the authors, from the `data` DataFrame
    by_author = data[data['user'].isin(authors)]

    # Select the pull requests that affect the file
    by_file = by_author[by_author['file'] == file]

    # Group and count the number of PRs done by each user each year
    grouped = by_file.groupby(['user', by_file['date'].dt.year]).count()['pid'].reset_index()

    # Transform the data into a wide format
    by_file_wide = grouped.pivot_table(index='date', columns='user', values='pid', fill_value=0)

    # Plot the results
    fig4, ax4 = plt.subplots()
    by_file_wide.plot(kind='bar', ax=ax4)
    ax4.set_xlabel('Year')
    ax4.set_ylabel('N° of pull requests')
    ax4.set_title('Number of contributions per year')
    st.pyplot(fig4)
