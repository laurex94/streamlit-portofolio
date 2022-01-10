import streamlit as st 
from PIL import  Image
import numpy as np

def app():
    st.markdown('''
        # Laurence Marcano
        ### Data analyst
    ''')

    col1, col2 = st.columns([3,1])

    with col1:
        st.markdown('''
            Hi, my name is Laurence, I am Data analyst. I have a degree in Physics (Universidad de Oriente - Venezuela).

            I have two years of experience in Computational Physics and six months of experience as a Data Analyst. 
        
            I consider myself enthusiastic, thoughtful, analytical and collaborative, motivated to achieve their goals and encourage my team to achieve theirs. I like challenges in which I can present ideas to find solutions. Always looking for quality, organization and use of good practices. Continuously learning, adapting to technological trends in the Physics and Data Science.

            **Contact**

            Email: laurencejose94@gmail.com

            Linkedin: [laurencejosem](https://www.linkedin.com/in/laurencejosem/)
        ''')

    with col2:
        display = Image.open('./pages/datasets/photo.jpg')
        display = np.array(display)
        st.image(display, width = 300)

    

    