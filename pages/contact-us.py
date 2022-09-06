import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


dash.register_page(
    __name__,
    name='Contact Us',
    top_nav=True,
    path='/contact-us'
)

line_break = html.Div([dcc.Markdown("""___""")], style={'margin': '5% 0% 5% 0%'})

creator_header = html.H1('About the Creator', style={'textAlign': 'center', 'margin': '10% 0% 5% 0%'})
contact_creator_header = html.H4('-   Contact Me   -', style={'textAlign': 'center'})
about_the_creator = dcc.Markdown("""Michael McManus is a Senior Data Analyst for a regulated gas and electric utility 
in Michigan, U.S. His work focuses on electric grid reliability and resiliency as it relates to forestry related power 
outages. Michael graduated from the University of Michigan School of Information with a Master's Degree in Applied Data 
Science in May of 2022. Michael loves all things data and is constantly looking for new opportunities to do good with 
his Data Science skills and leave the world better than he found it.  

>  
>  "Information Changes Everything" - UMSI.  
>  
""")

other_projects_header = html.H4('Other Projects', style={'textAlign': 'center', 'margin': '0% 0% 5% 0%'})
other_projects = dcc.Markdown("""
#### Austin Animal Center   
I recently published a dashboard aimed at helping 
[Austin Animal Center](https://www.austintexas.gov/austin-animal-center) 
understand how they can use their data.  There are some data exploration visualizations, a lost pet map, and other tools
utilizing machine learning to help Austin Animal Center predict the length a pet may need care in their facility. [Check 
out the tool here](http://austinanimalcenter.herokuapp.com/).   
  
#### HDBestimate  
A colleague and I created a tool to help Singaporeans understand the why behind their resale HDB Flats.  We used over 
300 location features to help people better understand how location impacts their housing price. Using machine learning 
and other data science methodologies, we were able to create a tool that not only estimates the resale value of a flat 
but also begins to explain a bit of the 'why' behind the resale price.  Check out the tool at 
[HDBestimate.com](https://www.hdbestimate.com/)  

  
""")


contact_links = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(dbc.NavLink([html.I(className="fab fa-github"), " GitHub"],
                                             href="https://github.com/mcmanus-git",
                                             target="_blank"))
                    ], width={"size": 3, 'offset': 2}
                ),
                dbc.Col(
                    [
                        html.Div(dbc.NavLink([html.I(className="fab fa-medium"), " Medium"],
                                             href="https://medium.com/@mcmanus_data_works",
                                             target="_blank")),
                    ], width={"size": 3}
                ),
                dbc.Col(
                    [
                        html.Div(dbc.NavLink([html.I(className="fab fa-linkedin"), " LinkedIn"],
                                             href="https://www.linkedin.com/in/michael-mcmanus/",
                                             target="_blank"))
                    ], width={"size": 3}
                )
            ], justify="center"
        )
    ]
)


def layout():

    """
    Generates contact-us page html
    :return: HTML/Dash Object(s)
    """

    layout = html.Div(
        [
            creator_header,
            html.Br(),
            about_the_creator,
            html.Br(),
            html.Br(),
            line_break,
            html.Br(),
            other_projects_header,
            html.Br(),
            other_projects,
            html.Br(),
            line_break,
            html.Br(),
            contact_creator_header,
            html.Br(),
            html.Br(),
            contact_links
        ],
        style={'margin': '5% 10% 5% 10%'}
    )

    return layout
