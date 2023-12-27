!pip install matplotlib
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.write("""# Welcome [Kingcode](https://github.com/MarsX-2002/streamlit-apps) :crown:""")

st.write('***')

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** `streamlit`, `pandas`, `base64`
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com)            
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2015, 2021))))

# Web scraping of NBA player stats data
@st.cache_data
def load_data(year):
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '_per_game.html'
    html = pd.read_html(url, header=0)  # here web scraping
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    platerstats = raw.drop(['Rk'], axis=1)
    return platerstats

playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_teams = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_teams)

# Sidebar - Position selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

#Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team) & playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and '+ str(df_selected_team.shape[1]) +' columns')
st.dataframe(df_selected_team)

# Downlaod NBA player stats data
# https://www.basketball-reference.com/leagues/NBA_2019_per_game.html
def fileDownlaod(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(fileDownlaod(df_selected_team), unsafe_allow_html=True)

# Heatmap 
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    # Convert non-numeric values to NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Check for NaN values and fill them with a specific value if needed
    df = df.fillna(0)  # You can choose another value if 0 is not appropriate

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)  # Pass the figure explicitly   
