import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_resource
def mySql():
    # Initialize connection using secrets.toml
    conn = st.connection('mysql', type='sql')
    # Perform query, returns pandas DataFrame
    df = conn.query('SELECT TotalKg FROM powerlifting_28_12_24 LIMIT 100;', ttl=600)
    return df

def main():
    st.title("Plot data from MySql")
    st.write("TotalKg from powerlifting")

    df = mySql()

    # NÃ¤ytetÃ¤Ã¤n data taulukkona
    st.dataframe(df)

    # PiirretÃ¤Ã¤n kÃ¤yrÃ¤
    fig = px.line(df, x=df.index, y="TotalKg", title="TotalKg from powerlifting")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
