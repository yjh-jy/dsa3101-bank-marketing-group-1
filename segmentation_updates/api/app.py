"""
Real-Time Customer Segmentation Dashboard Entry Point

This script sets up a Flask web server with a Dash frontend to visualize real-time customer segmentation data.
It connects to a PostgreSQL database, retrieves customer segment data, and updates a live dashboard with
a table and scatter plot visualization.

Technologies Used:
- Flask: REST API framework
- SQLAlchemy: Database ORM for Flask
- Dash: Data visualization framework
- Plotly: Interactive visualizations
- PostgreSQL: Relational database
- Docker
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import psycopg2

# Flask App Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dsa3101project@postgres:5433/postgres'
db = SQLAlchemy(app)

# Initialize Dash app, mounted onto the Flask server
dash_app = Dash(__name__, server=app, routes_pathname_prefix='/dashboard/')

def get_cluster_data():
    """
    Fetches the latest customer segment data from the PostgreSQL database.
    
    Returns:
        pd.DataFrame: DataFrame containing customer segmentation details.
    """
    conn = psycopg2.connect("dbname=postgres user=postgres password=dsa3101project host=postgres")
    query = """
        SELECT customer_id, balance, income, debt, avg_transaction_amt, segment 
        FROM customer_segments 
        ORDER BY last_updated DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Dash Layout: Defines the dashboard structure
dash_app.layout = html.Div([
    html.H1("Group 1's Real-Time Customer Segmentation Dashboard for Bank Marketing Campaigns", style={'text-align':'center', 'font-size': '40px'}),
    html.H2("Live Customer Information Table", style={'text-align':'center', 'font-size': '30px', 'text-decoration':'underline'}),
    
    # Data Table for Customer Segments
    dash_table.DataTable(
        id='customer-table',
        columns=[
            {'name': 'Customer ID', 'id': 'customer_id'},
            {'name': 'Balance', 'id': 'balance'},
            {'name': 'Income', 'id': 'income'},
            {'name': 'Debt', 'id': 'debt'},
            {'name': 'Average Transaction Amount', 'id': 'avg_transaction_amt'},
            {'name': 'Cluster', 'id': 'segment'},
        ],
        style_table={'width': '99%'},
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold', 'fontSize': '18px'},
        style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white', 'border': '0px', 'fontSize': '16px'},
        style_data_conditional=[
            {'if': {'column_id': 'segment', 'filter_query': '{segment} = "High-value"'}, 'backgroundColor': '#28A745', 'color': 'white'},
            {'if': {'column_id': 'segment', 'filter_query': '{segment} = "Budget-conscious"'}, 'backgroundColor': '#007BFF', 'color': 'white'},
            {'if': {'column_id': 'segment', 'filter_query': '{segment} = "At risk / inactive customers"'}, 'backgroundColor': '#FF4136', 'color': 'white'},
        ],
        page_size=10,
    ),

    html.H2("Live Customer Segment Clusters", style={'text-align':'center', 'font-size': '30px', 'text-decoration':'underline'}),

    # Scatter Plots for Customer Segments
    dcc.Graph(id='scatter-balance', style={'height': '500px'}),
    dcc.Graph(id='scatter-income', style={'height': '500px'}),
    dcc.Graph(id='scatter-debt', style={'height': '500px'}),
    
    # Auto-refresh interval
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
], style={'backgroundColor': '#111111', 'color': 'white', 'height': '100vh', 'width': '100vw', 'margin-top': '-25px', 'margin-left': '-8px'})

@dash_app.callback(
    [Output('scatter-balance', 'figure'),
     Output('scatter-income', 'figure'),
     Output('scatter-debt', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    """
    Updates the scatter plots with the latest customer segmentation data.
    
    Args:
        n (int): Number of intervals passed (unused, but required by Dash callback mechanism).
    
    Returns:
        tuple: Updated scatter plot figures.
    """
    color_map = {
        "High-value": "#28A745",
        "Budget-conscious": "#007BFF",
        "At risk / inactive customers": "#FF4136",
    }
    df = get_cluster_data()
    
    fig_balance = px.scatter(df, x='balance', y='avg_transaction_amt', color='segment', hover_data=['customer_id'], color_discrete_map=color_map)
    fig_income = px.scatter(df, x='income', y='avg_transaction_amt', color='segment', hover_data=['customer_id'], color_discrete_map=color_map)
    fig_debt = px.scatter(df, x='debt', y='avg_transaction_amt', color='segment', hover_data=['customer_id'], color_discrete_map=color_map)
    
    for fig in [fig_balance, fig_income, fig_debt]:
        fig.layout.template = 'plotly_dark'
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=1.05, font=dict(size=16)),
            legend_title=dict(text='Segment Types'),
            xaxis=dict(title_font=dict(size=24)),
            yaxis=dict(title_font=dict(size=24))
        )
    
    return fig_balance, fig_income, fig_debt

@dash_app.callback(
    Output('customer-table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_table(n):
    """
    Fetches the latest customer data and updates the table.
    
    Args:
        n (int): Number of intervals passed (unused, but required by Dash callback mechanism).
    
    Returns:
        list[dict]: List of dictionaries representing updated customer data.
    """
    df = get_cluster_data()
    return df[['customer_id', 'balance', 'income', 'debt', 'avg_transaction_amt', 'segment']].to_dict('records')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)