import streamlit as st
import pandas as pd
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )
def get_weather_data():
    conn = mysql.connector.connect(
        host="localhost",
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
    )
    df = pd.read_sql(
        """
        SELECT city, temperature, description, timestamp
        FROM weather_data
        ORDER BY timestamp DESC
        LIMIT 50
        """,
        conn,
    )
    conn.close()
    return df

def get_iss_data():
    conn = get_db_connection()
    df = pd.read_sql("""
        SELECT latitude, longitude, altitude_km, velocity_kmh, visibility, timestamp
        FROM iss_data
        ORDER BY timestamp DESC
        LIMIT 50
    """, conn)
    conn.close()
    return df
def main():

    # --- ISS data ---
    st.header('ISS:n sijaintihistoria ("Where The ISS At?" API + cron + MySQL)')
    st.markdown("ISS (International Space station) on kansainvälinen avaruusasema, joka kiertää maata noin 400km korkeudessa. Se liikkuu noin **27 600 km/h**, eli se kiertää maapallon **noin 15 kertaa päivässä**. Tässä sovelluksessa näet ISS:n historian ja sen sijainnin muutoksia 10 minuutin välein kerättynä cronin ja MySQL-tietokannan avulla. ")

    try:
        df_iss = get_iss_data()
        if df_iss.empty:
            st.warning("Ei vielä ISS-havaintoja tietokannassa.")
        else:
            st.dataframe(df_iss)

            # Esimerkki: kuvataan korkeutta ajan funktiona
            chart_iss = df_iss.set_index("timestamp").sort_index()
            st.line_chart(chart_iss["altitude_km"], height=300)
    except Exception as e:
        st.error(f"ISS-datan lataus epäonnistui: {e}")

if __name__ == "__main__":
    main()