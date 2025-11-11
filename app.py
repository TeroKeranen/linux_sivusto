from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    # Yhdistetään MySQL:ään
    conn = mysql.connector.connect(
        host="localhost",
        user="exampleuser",
        password="change_this_strong_password",  # sama salasana jolla kirjaudut
        database="exampledb"
    )
    cursor = conn.cursor()

    # Haetaan SQL-serverin aika ja +1 tunti
    cursor.execute("SELECT NOW(), DATE_ADD(NOW(), INTERVAL 1 HOUR)")
    current_time, plus_one_hour = cursor.fetchone()

    cursor.close()
    conn.close()

    # Renderöidään yksinkertainen HTML
    return f"""
        <h1>Oli kyllä hassunhauska tehtävä ei hkhkkhkhk</h1>
        <h1>SQL server time: {current_time}</h1>
        <h2>SQL server time +1 hour: {plus_one_hour}</h2>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
