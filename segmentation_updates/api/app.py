from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import psycopg2
import plotly.io as pio



# Flask App Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dsa3101project@postgres:5433/postgres'
db = SQLAlchemy(app)

dash_app = Dash(__name__, server=app, routes_pathname_prefix='/dashboard/')

def get_cluster_data():
    """Fetch latest customer segment data from PostgreSQL."""
    conn = psycopg2.connect("dbname=postgres user=postgres password=dsa3101project host=postgres")
    query = "SELECT customer_id, balance, avg_transaction_amt, segment FROM customer_segments ORDER BY last_updated DESC;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Dash Layout
dash_app.layout = html.Div([
    html.H1("  Real-Time Customer Segmentation Dashboard"),
    html.H2("  Live Customer Table (Sorted by last updated)"),
    dash_table.DataTable(
        id='customer-table',
        columns=[
            {'name': 'Customer ID', 'id': 'customer_id'},
            {'name': 'Balance', 'id': 'balance'},
            {'name': 'Average Transaction Amount', 'id': 'avg_transaction_amt'},
            {'name': 'Cluster', 'id': 'segment'},
        ],
        style_table={'width':'99%'},
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white',
            'fontWeight':'bold',
            'fontSize': '18px'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white',
            'border': '0px',
            'fontSize': '16px'
        },
        style_data_conditional=[ 
            {
                'if': {'column_id': 'segment', 'filter_query': '{segment} = "High-value"'},
                'backgroundColor': '#28A745',  
                'color': 'white',
            },
            {
                'if': {'column_id': 'segment', 'filter_query': '{segment} = "Budget-conscious"'},
                'backgroundColor': '#007BFF',  
                'color': 'white',
            },
            {
                'if': {'column_id': 'segment', 'filter_query': '{segment} = "At risk / inactive customers"'},
                'backgroundColor': '#FF4136', 
                'color': 'white',
            }
        ],
        page_size=10,
    ),
    dcc.Graph(id='cluster-graph-scatter', style={'height': '800px'},),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  # Update every 1 sec
    ],
    style={'backgroundColor': '#111111', 'color': 'white', 'height': '100vh', 'width':'100vw', 'margin-top':'-20px',  'margin-left':'-9px'}
    )

@dash_app.callback(
    Output('cluster-graph-scatter', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    color_map = {
        "High-value": "#28A745",  # Cluster A color
        "Budget-conscious": "#007BFF",  # Cluster B color
        "At risk / inactive customers": "#FF4136",  # Cluster C color
    }
    df = get_cluster_data()
    fig = px.scatter(df, x='balance', y='avg_transaction_amt', color='segment', hover_data=['customer_id'], color_discrete_map=color_map)
    fig.layout.template = 'plotly_dark'
    fig.update_layout(
    legend=dict(
        orientation="h",     
        yanchor="bottom",      
        xanchor="center",
        x= 0.5, 
        y=1.05,               
        font=dict(size=20),    
    ),
    legend_title=dict(text='Customer Segments'),  # Optional: Add a title to the legend
)
    return fig


@dash_app.callback(
    Output('customer-table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_table(n):
    df = get_cluster_data()
    # Convert the dataframe to a list of dictionaries for the table
    return df[['customer_id', 'balance', 'avg_transaction_amt', 'segment']].to_dict('records')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
