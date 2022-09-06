import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from navbar import create_navbar

# Toggle the themes at [dbc.themes.LUX]
# The full list of available themes is:
# BOOTSTRAP, CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA, MINTY, PULSE, SANDSTONE,
# SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, YETI, ZEPHYR.
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/

navbar = create_navbar()
FA47 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
FA512 = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"

dash_app = dash.Dash(__name__,
                     suppress_callback_exceptions=True,
                     external_stylesheets=[dbc.themes.FLATLY,
                                      FA47,
                                      FA512,
                                      ],
                     use_pages=True,
                     )


dash_app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NYC Street Trees</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        
    </body>
</html>
'''

dash_app.layout = dcc.Loading(
    id='loading_page_content',
    children=[
        html.Div(
            [
                navbar,
                dash.page_container
            ]
        )
    ],
    color='#333B52',
    fullscreen=True
)

app = dash_app.server

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='8000')
