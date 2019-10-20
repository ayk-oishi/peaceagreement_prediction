import dash
import dash_core_components as dcc
import dash_html_components as html
import base64

boat_photo=base64.b64encode(open('resources/CAR_peaceagreement.png', 'rb').read())


tab_1_layout = html.Div([
    html.H3('Introduction'),
    html.Div([
    html.Div([
        dcc.Markdown("This dashboard shows a predictive model on failure or success of peaceagreement."),
        dcc.Markdown("* The model was built based on PA-X dataset which includes 1,500 agreements."),
        dcc.Markdown("* A predictive model that has been trained on a portion of the data, and tested on a set-aside portion."),
        dcc.Markdown("* Evaluation metrics showing the performance of the model on the testing data."),
        dcc.Markdown("* A feature to receive new user inputs that makes predictions based on the new data."),
        dcc.Markdown("* An interactive user interface deployed on a cloud platform and accessible to potential reviewers."),
        html.A('View code on github', href='https://github.com/austinlasseter/titanic_classifier'),
    ],className='ten columns'),
    html.Div([
    html.Img(src='data:image/png;base64,{}'.format(boat_photo.decode()), style={'height':'200px'}),
    ],className='two columns'),


    ],className='nine columns'),

])
