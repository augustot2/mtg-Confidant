import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
from dash.exceptions import PreventUpdate
import urllib
import json
# database
unique_card_list = pd.read_csv("database/unique_card_list.csv")

#relational_card = [ {"label": row.printed_name ,"value": row.oracle_id } for i,row in unique_card_list.iterrows()]
lang_list = [ {"label": lang,"value": lang } for lang in unique_card_list.lang.unique()]

artwork_cards = pd.read_csv("database/artwork_card.csv")




#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

app.layout= html.Div([
    html.P("Select Language"),
    dcc.Dropdown(options = lang_list,
                 id="dropdown_language",
                 value="en"),
    html.P("Search Card :"),
    dcc.Dropdown(options = [],
                 value="Orbe Estática",
                 id = "dropdown_card_name"),
    html.Button("Confirm",id="button_confirm"),
    html.Div( id="div_output")
])




@app.callback(
    dash.dependencies.Output('dropdown_card_name', 'options'),
    [dash.dependencies.Input("dropdown_language","value")]
)
def get_cards_by_lang(lang_value):
    lang_card_list = unique_card_list[unique_card_list.lang == lang_value]
    relational_card = [ {"label": row.printed_name ,"value": row.oracle_id } for i,row in lang_card_list.iterrows()]

    return relational_card

@app.callback(
    dash.dependencies.Output('div_output', 'children'),
    [dash.dependencies.Input("button_confirm","n_clicks")],
    [dash.dependencies.State('dropdown_card_name', 'value')])
def update_output(n_click,value):
    if n_click == None:
        raise PreventUpdate

    # Parser Card
    select_artwork = artwork_cards[artwork_cards.oracle_id.isin([value])]
    dicio = select_artwork.image_uris.values[0]
    json_acceptable_string = dicio.replace("'", "\"")
    
    image_url = json.loads(json_acceptable_string)["normal"]
    
    return html.Img(src=image_url)
    

if __name__ == '__main__':
    app.run_server(debug=True)

