import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


dash.register_page(
    __name__,
    name='About',
    top_nav=True,
    path='/about'
)

line_break = html.Div([dcc.Markdown("""___""")], style={'margin': '5% 0% 5% 0%'})

about_header = html.H1('About the Project', style={'textAlign': 'center', 'margin': '10% 0% 5% 0%'})
contact_creator_header = html.H4('-   Contact Me   -', style={'textAlign': 'center'})
about_the_project1 = dcc.Markdown("""This project is part of Plotly Autumn App blah blah blah""")
about_the_project2 = dcc.Markdown("""The dataset used in this project is from a Iowa Public data....  
""")



def layout():

    """
    Generates about page html
    :return: HTML/Dash Object(s)
    """

    layout = html.Div(
        [
            about_header,
            html.Br(),
            about_the_project1,
            html.Br(),
            html.Br(),
            about_the_project2,
            html.Br(),
            html.Br(),
        ],
        style={'margin': '5% 10% 5% 10%'}
    )

    return layout
