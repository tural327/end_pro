from flask import Flask, render_template, request, make_response
import json
import pymysql
import plotly.graph_objs as go

# --- Database Configuration ---
endpoint = "awskobia.cl06c8y2st5d.eu-north-1.rds.amazonaws.com"
username = "admin"
password = "Yerik2ral1995"
database_name = "test1"

# IMPORTANT: Elastic Beanstalk üçün application
application = Flask(__name__)

# -------------------------------
# Helper function (Plotly)
# -------------------------------
def create_plot(x, y, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))
    fig.update_layout(title=title)
    return fig.to_html(full_html=False)

# -------------------------------
# DB helper
# -------------------------------
def fetch_all(sql):
    conn = pymysql.connect(
        host=endpoint,
        user=username,
        password=password,
        database=database_name,
        port=3306,
        cursorclass=pymysql.cursors.Cursor
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

# -------------------------------
# Routes
# -------------------------------
@application.route('/')
def home():
    return render_template('index.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')

        # -------- ADMIN --------
        if user == 'admin' and pw == 'admin12345':
            sql = """
                SELECT created_at, temperature, humidity, vibiration, flow, voltage
                FROM sensors
                ORDER BY created_at DESC
            """
            data_table = fetch_all(sql)
            return render_template('test1.html', username=user, sensor_data=data_table)

        # -------- SISTEM 1 --------
        elif user == 'sistem1' and pw == 'kobia1':
            sql = """
                SELECT created_at, p1, p2, p3, p4, p5
                FROM sistem1
                ORDER BY created_at DESC
            """
            data_table = fetch_all(sql)
            return render_template('sistem1.html', username=user, sensor_data=data_table)

        # -------- SISTEM 2 --------
        elif user == 'sistem2' and pw == 'kobia2':
            sql = """
                SELECT created_at, p1, p2, p3, p4, p5
                FROM sistem2
                ORDER BY created_at DESC
            """
            data_table = fetch_all(sql)
            return render_template('sistem2.html', username=user, sensor_data=data_table)

        # -------- SISTEM 3 --------
        elif user == 'sistem3' and pw == 'kobia3':
            sql = """
                SELECT created_at, p1, p2, p3, p4, p5
                FROM sistem3
                ORDER BY created_at DESC
            """
            data_table = fetch_all(sql)
            return render_template('sistem3.html', username=user, sensor_data=data_table)

        else:
            return render_template('error.html')

    return render_template('login2.html')

# -------------------------------
# JSON APIs (charts üçün)
# -------------------------------
@application.route('/data')
def data():
    sql = """
        SELECT created_at, temperature, humidity, vibiration, flow, voltage
        FROM sensors
        ORDER BY created_at ASC
    """
    rows = fetch_all(sql)

    data = []
    for r in rows:
        data.append([
            str(r[0]), r[1], r[2], r[3], r[4], r[5]
        ])

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@application.route('/data_sistem1')
def data_sistem1():
    sql = "SELECT created_at, p1, p2, p3, p4, p5 FROM sistem1 ORDER BY created_at ASC"
    rows = fetch_all(sql)

    data = [[str(r[0]), r[1], r[2], r[3], r[4], r[5]] for r in rows]

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@application.route('/data_sistem2')
def data_sistem2():
    sql = "SELECT created_at, p1, p2, p3, p4, p5 FROM sistem2 ORDER BY created_at ASC"
    rows = fetch_all(sql)

    data = [[str(r[0]), r[1], r[2], r[3], r[4], r[5]] for r in rows]

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@application.route('/data_sistem3')
def data_sistem3():
    sql = "SELECT created_at, p1, p2, p3, p4, p5 FROM sistem3 ORDER BY created_at ASC"
    rows = fetch_all(sql)

    data = [[str(r[0]), r[1], r[2], r[3], r[4], r[5]] for r in rows]

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

# -------------------------------
# Health check
# -------------------------------
@application.route('/health')
def health():
    return json.dumps({"status": "healthy"}), 200

# -------------------------------
# Local run
# -------------------------------

