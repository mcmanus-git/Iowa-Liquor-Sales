import dash_bootstrap_components as dbc
import dash.html as html
from dash import dcc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink([html.I(className="fab fa-github")],
                                    href="https://github.com/mcmanus-git",
                                    target="_blank")
                        ),
            dbc.NavItem(dbc.NavLink([html.I(className="fab fa-medium")],
                                    href="https://medium.com/@mcmanus_data_works",
                                    target="_blank")
                        ),
            dbc.NavItem(dbc.NavLink([html.I(className="fab fa-linkedin")],
                                    href="https://www.linkedin.com/in/michael-mcmanus/",
                                    target="_blank")
                        ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("About", href='/about'),
                    dbc.DropdownMenuItem("Contact Us", href='/contact-us'),
                ],
            ),
        ],
        brand="Iowa Liquor",
        brand_href="/",
        sticky="top",
        color="primary",  # Change this to change color of the navbar e.g. "primary", "secondary", "dark" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar
