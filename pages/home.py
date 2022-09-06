from dash import html, dcc
import dash

dash.register_page(
    __name__,
    name='NYC Street Trees',
    top_nav=True,
    path='/'
)


def layout():

    """
    Generates home page html
    :return: HTML/Dash Object(s)
    """

    layout = html.Div(
        [
            dcc.Markdown(f"# Home Placeholder Text"),
            dcc.Markdown(f"""Lorem ipsum""")
        ],
        style={'margin': '5% 5% 5% 5%'}
    )
    return layout
