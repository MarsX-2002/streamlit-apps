import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

#####################
# Page Title
#####################

image = Image.open('dna-logo.jpg')

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App
         
This app counts the nucleotide composition of query DNA!

"Check out my [GitHub](https://github.com/MarsX-2002/streamlit-apps/) profile! :joy:
***                  
""")

#####################
# Input Text Box
#####################
st.header("Input DNA sequency")
sequence_input = ">DNA Query 1\nGTATGTAGCCACGGAGCACCATTACCTGTCACCATTACCTGAATGGCTA\nACATGTAGCCACAAAGCACCATCACCTGTCACCATTACCTGAATGGCGC"

sequence = st.text_area("Sequence Input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:]  # skip the sequence name line
sequence = ''.join(sequence)    

st.write("""
***
""")

## Prints the input DNA
st.header('INPUT (DNA Query)')
sequence

## DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

## 1. Print dictionary :)
st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C'))
    ])
    return d

X = DNA_nucleotide_count(sequence)

# X_label = list(X)
# X_value = list(X.values())
X

## 2. Print text
st.subheader('2. Print text')
st.write('There are '+ str(X['A']) +' Adenine (A), ')
st.write('There are '+ str(X['T']) +' Thymine (T), ')
st.write('There are '+ str(X['G']) +' Guanine (G), ')
st.write('There are '+ str(X['C']) +' Cytosine (C).')

## 3. Display Dataframe
st.subheader('3. Display Dataframe')
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'nucleotide'})
st.write(df)

## 4. Display Bar Chart using Altair
st.subheader('4. Display Bar Chart using Altair')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
    )
p = p.properties(
    width=alt.Step(80)  # control width of the chart
    )

st.write(p)
