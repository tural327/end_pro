#import pandas as pd
#import plotly.graph_objs as go
from flask import Flask, render_template, request, make_response
import time
import json
import subprocess
import os
import pymysql

# --- Database Configuration (It is recommended to use environment variables for security) ---
endpoint = "awskobia.cl06c8y2st5d.eu-north-1.rds.amazonaws.com"
username = "admin"
password = "Yerik2ral1995"
database_name = "test1"

# IMPORTANT: Change 'app' to 'application' for Elastic Beanstalk
application = Flask(__name__)

# --- Helper Function for Plotly (Unchanged) ---
def create_plot(x, y, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=title))
    fig.update_layout(title=title, xaxis_title='Date', yaxis_title=title)
    return fig.to_html(full_html=False)

# --- Flask Routes ---

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        
        if user == 'admin' and pw == 'admin12345':
            conn_local = None 
            data_table = [] # Initialize list for table data

            try:
                # Establish connection to fetch data for the table
                conn_local = pymysql.connect(
                    host=endpoint,
                    user=username,
                    password=password,
                    database=database_name,
                    port=3306 
                )
                
                table_name = "sensors"
                # 🚨 KEY CHANGE: Fetch ALL data and ORDER BY created_at DESC (newest first)
                sql_query = f"""
                    SELECT created_at, temperature, humidity, vibiration, flow, voltage 
                    FROM {table_name} 
                    ORDER BY created_at DESC; 
                """
                
                # Fetch data
                df = pd.read_sql(sql_query, conn_local)
                
                # Pre-process data
                df = df.dropna()
                # Select and convert only the columns needed for the table
                data_table = df[['created_at', 'temperature', 'humidity',
                                 'vibiration','flow','voltage']].values.tolist()
                
            except Exception as e:
                # Print error but allow the page to render, potentially with an empty table
                print(f"Database error during login: {e}") 

            finally:
                if conn_local:
                    conn_local.close()

            # Pass the fetched data (or empty list if error) to the template
            return render_template('test1.html', username=user, sensor_data=data_table)
        elif user == 'sistem1' and pw == 'kobia1':
            conn_local = None 
            data_table = [] # Initialize list for table data

            try:
                # Establish connection to fetch data for the table
                conn_local = pymysql.connect(
                    host=endpoint,
                    user=username,
                    password=password,
                    database=database_name,
                    port=3306 
                )
                
                table_name = "sistem1"
                # 🚨 KEY CHANGE: Fetch ALL data and ORDER BY created_at DESC (newest first)
                sql_query = f"""
                    SELECT created_at, p1, p2, p3, p4, p5 
                    FROM {table_name} 
                    ORDER BY created_at DESC; 
                """
                
                # Fetch data
                df = pd.read_sql(sql_query, conn_local)
                
                # Pre-process data
                df = df.dropna()
                # Select and convert only the columns needed for the table
                data_table = df[['created_at', 'p1', 'p2',
                                 'p3','p4','p5']].values.tolist()
                
            except Exception as e:
                # Print error but allow the page to render, potentially with an empty table
                print(f"Database error during login: {e}") 

            finally:
                if conn_local:
                    conn_local.close()

            # Pass the fetched data (or empty list if error) to the template
            return render_template('sistem1.html', username=user, sensor_data=data_table)
        elif user == 'sistem2' and pw == 'kobia2':
            conn_local = None 
            data_table = [] # Initialize list for table data

            try:
                # Establish connection to fetch data for the table
                conn_local = pymysql.connect(
                    host=endpoint,
                    user=username,
                    password=password,
                    database=database_name,
                    port=3306 
                )
                
                table_name = "sistem2"
                # 🚨 KEY CHANGE: Fetch ALL data and ORDER BY created_at DESC (newest first)
                sql_query = f"""
                    SELECT created_at, p1, p2, p3, p4, p5 
                    FROM {table_name} 
                    ORDER BY created_at DESC; 
                """
                
                # Fetch data
                df = pd.read_sql(sql_query, conn_local)
                
                # Pre-process data
                df = df.dropna()
                # Select and convert only the columns needed for the table
                data_table = df[['created_at', 'p1', 'p2',
                                 'p3','p4','p5']].values.tolist()
                
            except Exception as e:
                # Print error but allow the page to render, potentially with an empty table
                print(f"Database error during login: {e}") 

            finally:
                if conn_local:
                    conn_local.close()

            # Pass the fetched data (or empty list if error) to the template
            return render_template('sistem2.html', username=user, sensor_data=data_table)
        elif user == 'sistem3' and pw == 'kobia3':
            conn_local = None 
            data_table = [] # Initialize list for table data

            try:
                # Establish connection to fetch data for the table
                conn_local = pymysql.connect(
                    host=endpoint,
                    user=username,
                    password=password,
                    database=database_name,
                    port=3306 
                )
                
                table_name = "sistem3"
                # 🚨 KEY CHANGE: Fetch ALL data and ORDER BY created_at DESC (newest first)
                sql_query = f"""
                    SELECT created_at, p1, p2, p3, p4, p5 
                    FROM {table_name} 
                    ORDER BY created_at DESC; 
                """
                
                # Fetch data
                df = pd.read_sql(sql_query, conn_local)
                
                # Pre-process data
                df = df.dropna()
                # Select and convert only the columns needed for the table
                data_table = df[['created_at', 'p1', 'p2',
                                 'p3','p4','p5']].values.tolist()
                
            except Exception as e:
                # Print error but allow the page to render, potentially with an empty table
                print(f"Database error during login: {e}") 

            finally:
                if conn_local:
                    conn_local.close()

            # Pass the fetched data (or empty list if error) to the template
            return render_template('sistem3.html', username=user, sensor_data=data_table)
        else:
            return render_template('error.html', username=user)
    
    return render_template('login2.html')

@application.route('/data')
def data():
    # Initialize connection to None
    conn_local = None 
    try:
        # 1. Establish a new connection for this request
        conn_local = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            database=database_name,
            port=3306 
        )
        
        table_name = "sensors"
        # pd.read_sql will execute the query and fetch the latest data
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn_local)
        
        df1 = df.dropna()
        print(df1.shape)
        # Ensure 'created_at' is treated as string for JSON serialization
        df1['created_at'] = df1['created_at'].astype(str) 
        
        data = df1[['created_at', 'temperature', 'humidity',
                    'vibiration','flow','voltage']].values.tolist()
        
        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response
    
    except Exception as e:
        # Log the error for debugging
        print(f"Database error: {e}") 
        return json.dumps({"error": str(e)}), 500
    
    finally:
        # 2. Always close the connection
        if conn_local:
            conn_local.close()

@application.route('/data_sistem1')
def data_sistem1():
    conn_local = None
    try:
        conn_local = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            database=database_name,
            port=3306 
        )

        table_name = "sistem1"
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn_local)
        df['created_at'] = df['created_at'].astype(str)

        data = df[['created_at','p1','p2','p3','p4','p5']].values.tolist()

        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response

    finally:
        if conn_local:
            conn_local.close()


@application.route('/data_sistem2')
def data_sistem2():
    conn_local = None
    try:
        conn_local = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            database=database_name,
            port=3306 
        )

        table_name = "sistem2"
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn_local)
        df['created_at'] = df['created_at'].astype(str)

        data = df[['created_at','p1','p2','p3','p4','p5']].values.tolist()

        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response

    finally:
        if conn_local:
            conn_local.close()

@application.route('/data_sistem3')
def data_sistem3():
    conn_local = None
    try:
        conn_local = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            database=database_name,
            port=3306 
        )

        table_name = "sistem3"
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn_local)
        df['created_at'] = df['created_at'].astype(str)

        data = df[['created_at','p1','p2','p3','p4','p5']].values.tolist()

        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response

    finally:
        if conn_local:
            conn_local.close()

# Health check endpoint for Elastic Beanstalk
#@application.route('/health')
#def health():
#    return json.dumps({"status": "healthy"}), 200


#if __name__ == '__main__':
    # Remove host and port for EB deployment
#    application.run(host="0.0.0.0", port=5000)
