import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import pickle
from tabs import tab_1, tab_2, tab_4
from utils import display_eval_metrics, Viridis


df=pd.read_csv('resources/final_probs.csv')


## Instantiante Dash
app = dash.Dash()
application = app.server
app.config['suppress_callback_exceptions'] = True
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
app.title='Peaceagreement!'


## Layout
app.layout = html.Div([
    html.H1('Failure of Implementation of Peaceagreement'),
    dcc.Tabs(id="tabs-template", value='tab-1-template', children=[
        dcc.Tab(label='Introduction', value='tab-1-template'),
        dcc.Tab(label='Model Evaluation', value='tab-2-template'),
#        dcc.Tab(label='Testing Results', value='tab-3-template'),
        dcc.Tab(label='User Inputs', value='tab-4-template'),
    ]),
    html.Div(id='tabs-content-template')
])


############ Callbacks

@app.callback(Output('tabs-content-template', 'children'),
              [Input('tabs-template', 'value')])
def render_content(tab):
    if tab == 'tab-1-template':
        return tab_1.tab_1_layout
    elif tab == 'tab-2-template':
        return tab_2.tab_2_layout
#    elif tab == 'tab-3-template':
#        return tab_3.tab_3_layout
    elif tab == 'tab-4-template':
        return tab_4.tab_4_layout

# Tab 2 callbacks

@app.callback(Output('page-2-graphic', 'figure'),
              [Input('page-2-radios', 'value')])
def radio_results(value):
    return display_eval_metrics(value)

# Tab 3 callback # 1
#@app.callback(Output('page-3-content', 'children'),
#              [Input('page-3-dropdown', 'value')])
#def page_3_dropdown(value):
#    name=df.loc[value, 'Name']
#    return f'You have selected "{name}"'

# Tab 3 callback # 2
#@app.callback(Output('survival-prob', 'children'),
#              [Input('page-3-dropdown', 'value')])
#def page_3_survival(value):
#    survival=df.loc[value, 'survival_prob']
#    actual=df.loc[value, 'Survived']
#    survival=round(survival*100)
#    return f'Predicted probability of survival is {survival}%, Actual survival is {actual}'

# Tab 3 callback # 2
#@app.callback(Output('survival-characteristics', 'children'),
#              [Input('page-3-dropdown', 'value')])
#def page_3_characteristics(value):
#    mydata=df.drop(['Survived', 'survival_prob', 'Name'], axis=1)
#    return html.Table(
#        [html.Tr([html.Th(col) for col in mydata.columns])] +
#        [html.Tr([
#            html.Td(mydata.iloc[value][col]) for col in mydata.columns
#        ])]
#    )

# Tab 4 Callback # 1
@app.callback(Output('user-inputs-box', 'children'),
            [
              Input('SymbolicReparation_dropdown', 'value'),
              Input('Amnesty', 'value'),
              Input('Ceasefire', 'value')
              ])
def update_user_table(SymbolicReparation, Amnesty, Ceasefire):
    return html.Div([
        html.Div(f'SymbolicReparation: {SymbolicReparation}'),
        html.Div(f'Amnesty: {Amnesty}'),
        html.Div(f'Ceasefire: {Ceasefire}'),
    ])

# Tab 4 Callback # 2
@app.callback(Output('final_prediction', 'children'),
            [
              Input('SymbolicReparation_dropdown', 'value'),
              Input('Amnesty_dropdown', 'value'),
              Input('Ceasefire_dropdown', 'value')
              ])
def final_prediction(SymbolicReparation, Amnesty, Ceasefire):
    inputs=[SymbolicReparation, Amnesty, Ceasefire]
    keys=['SymbolicReparation', 'Amnesty', 'Ceasefire']
    dict6=dict(zip(keys, inputs))
    df=pd.DataFrame([dict6])
    # create the features we'll need to run our logreg model.
    df['SymbolicReparation']=np.where(df.SymbolicReparation=='Yes',1,0)
    df['Amnesty']=np.where(df.Amnesty=='Yes',1,0)
    df['Ceasefire']=np.where(df.Ceasefire=='Yes',1,0)

    # drop unnecessary columns, and reorder columns to match the logreg model.
    df=df.drop(['SymbolicReparation', 'Amnesty', 'Ceasefire'], axis=1)
    df=df[['SymbolicReparation', 'Amnesty', 'Ceasefire']]
    # unpickle the final model
    file = open('resources/final_logreg_model.pkl', 'rb')
    logreg=pickle.load(file)
    file.close()
    # predict on the user-input values (need to create an array for this)
    firstrow=df.loc[0]
    print('firstrow', firstrow)
    myarray=firstrow.values
    print('myarray', myarray)
    thisarray=myarray.reshape((1, myarray.shape[0]))
    print('thisarray', thisarray)


    # tryagain=np.array([4, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0])
    # tryagain=tryagain.reshape((1, tryagain.shape[0]))
    prob=logreg.predict_proba(thisarray)
    final_prob=round(float(prob[0][1])*100,1)
    return(f'Probability of Failure: {final_prob}%')









####### Run the app #######
if __name__ == '__main__':
    application.run(debug=True, port=8080)
