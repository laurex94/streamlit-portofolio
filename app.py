import os
import streamlit as st
# Custom imports 
from multipage import MultiPage
from pages import android_app_market, home, investigating_netflix_movies, the_github_history_of_the_Scala_language

# Create an instance of the app 
app = MultiPage()

# Add all your application here
app.add_page("Profile", home.app)
app.add_page("The Android App Market on Google Play", android_app_market.app)
app.add_page("Investigating Netflix Movies and Guest Stars in The Office", investigating_netflix_movies.app)
app.add_page("The GitHub History of the Scala Language", the_github_history_of_the_Scala_language.app)

# The main app
app.run()