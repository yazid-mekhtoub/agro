
# print(pprint.pformat( shop_card('product_name', 'product_code', 'product_price',  'product_quantity', 'image_path')))
from dash import Dash, dcc, html, Input, Output, State, ALL,  MATCH, callback, ctx, no_update,   clientside_callback, ClientsideFunction
from dash_iconify import DashIconify as icon
import dash_mantine_components as dmc
import pprint
from appshell import  footer, header
from utils import id_dict
import pandas as pd
# from pages.shop import  shop

app = Dash(
    __name__,
    # suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],   
)


data = pd.read_csv('products.csv')

product_provider_options = data[['category','provider']].drop_duplicates().groupby('category')['provider'].apply(list).reset_index()
product_provider_options = dict(zip(product_provider_options.category, product_provider_options.provider))

data = data.to_dict('records')
# print(data)




shop = dmc.Paper(
    id = id_dict('page_layout_id', 'shop'),
    style = {'display':'block'},
    className = 'page',

    children = [
        # html.Div(id = 'product_category_options_div'),
        dmc.ChipGroup(
                id = 'product_category'
            ),
        dmc.ChipGroup(
            id = 'product_povider'
        ),
        

        dmc.TextInput(
            id = 'search_item',
            size = 'md',
            placeholder="Search",
            rightSection=icon(icon="guidance:search"),
        ),
        dmc.Container(id = 'products_container'),
        dmc.Button("Load more", id = 'load_more',variant="default", size = 'sm', radius='xl', compact=True, n_clicks=0, leftIcon = dmc.Badge("23", id = 'load_more_number') ),




    ]
)

account = dmc.Paper(
    id = id_dict('page_layout_id', 'account'),
    className = 'page',
    style = {'display':'none'},
    children = [
        dmc.Text("account_page", size="md", color ='yellow'),
        dmc.Text("account_page", size="md"),
        dmc.Text("account_page", size="md"),
        dmc.Text("Default text", size="md"),
        dmc.Text("Default text", size="md"),
    ]
)

cart = dmc.Paper(
    m = 0,
    p = 0,
    id = id_dict('page_layout_id', 'cart'),
    style = {'display':'none'},
    className = 'page',
    children = [
            html.Div(id = 'cart-items')

    ]
)
content = dmc.Container(
    className = 'content',
    children = [
        shop,
        account,
        cart,
         dmc.Drawer(
            id="card_item_detail_drawer",
            zIndex=10000,
            position = 'bottom',
            size="65%",
            withCloseButton=False
        ),
    ]
)
   
app.layout = html.Div(
    children=[  
        dmc.MantineProvider(
            id = 'theme',
            withGlobalStyles=True,
            children=[
                html.Div(
                    children = [
                        header,
                        content,
                        footer,
                dcc.Store(id = 'all_stored_products', data = data),
                dcc.Store(id = 'items_pushed_to_cart', data = {}),
                dcc.Store(id = 'chip_prodcut_provider_optoins', data = product_provider_options),
                dmc.Text(id='void'),
                    ]
                )
            ]
        ) 
    ]
)

@callback(
    Output("void","children"),
    Input("product_povider","value")
)
def set_product_category_options(data):
    print(data)

    return no_update

clientside_callback(
    """
    function updateProviderChips( data){
    data = Object.keys(data)

    let chips = []
    data.forEach(function(x) {
        chips.push( {
            'namespace': 'dash_mantine_components',
            'props': {'children': x,
                    'size': 'lg',
                    'value': x},
            'type': 'Chip'}
        )
    })
    return [chips, data[2]]
    }
    """,
    Output("product_category","children"),
    Output("product_category","value"),
    Input("chip_prodcut_provider_optoins","data")
)



clientside_callback(
    """
    function updateProviderChips(product_category, data){
    console.log()
    let chips = []
    data[product_category].forEach(function(x) {
        chips.push( {
            'namespace': 'dash_mantine_components',
            'props': {'children': x,
                    'size': 'lg',
                    'value': x},
            'type': 'Chip'}
        )
    })

    return [chips, data[product_category][0]]
    }
    """,
    Output("product_povider","children"),
    Output("product_povider","value"),

    Input("product_category","value"),
    State("chip_prodcut_provider_optoins","data"),
    prevent_initial_call=True,
)
clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='make_cards'
    ),
        Output('products_container', 'children'),
        Output("load_more_number", "children"),
        Output("load_more", "display"),

        Input('product_povider', 'value'),
        Input('product_category', 'value'),
        Input("search_item", "value"),
        Input("load_more", "n_clicks"),
        State("items_pushed_to_cart", "data"),
        State("all_stored_products", "data"),
)


clientside_callback(
    """
    function updateCardItemTotal(card_item_quantity, item_price) {
        if (!card_item_quantity) {
            card_item_quantity = 0;
        }
        return (card_item_quantity * item_price).toFixed(2);
    }
    """,
    Output({"type": "card_item_total", "index": MATCH}, "children"),
    Input({"type": "card_item_quantity", "index": MATCH}, "value"),
    State({"type": "card_item_price", "index": MATCH}, "children")
)
 


clientside_callback(
    """
    function updateCartItemTotal(card_item_quantity, item_price) {
        if (!card_item_quantity) {
            card_item_quantity = 0;
        }
        return (card_item_quantity * item_price).toFixed(2);
    }
    """,
    Output({"type": "cart_item_total", "index": MATCH}, "children"),
    Input({"type": "card_item_quantity", "index": MATCH}, "value"),
    State({"type": "card_item_price", "index": MATCH}, "children")
)

clientside_callback(
    """
    function(card_item_quantity, cart_item_quantity) {
        const ctx = window.dash_clientside.callback_context;
        triggered_input = JSON.parse(ctx.triggered[0]['prop_id'].split(".")[0]).type
        

        if (triggered_input ==='card_item_quantity') {
        
            return [card_item_quantity, card_item_quantity]
        } else{
        return [cart_item_quantity, cart_item_quantity]
        }
        return window.dash_clientside.no_update
    }
    """,
        Output({"type": "cart_item_quantity", "index": MATCH}, "value"), 
        Output({"type": "card_item_quantity", "index": MATCH}, "value"), 
         
        Input({"type": "card_item_quantity", "index": MATCH}, "value"),
        Input({"type": "cart_item_quantity", "index": MATCH}, "value"),
        prevent_initial_call=True,
)



clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='page_switcher'
    ),
    Output({"type": "page_layout_id", "index": ALL}, "style"), 
    Output({"type": "page_switcher_action", "index": ALL}, "style"),
    Output({"type": "page_switcher_action_text", "index": ALL}, "style"),
    Input({"type": "page_switcher_action", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)

clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='theme_switcher'
    ),
    Output("theme", "theme"),
    Output("theme_switcher", "children"),
    Input("theme_switcher", "n_clicks"),
)


clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='item_card_add_item'
    ),
    Output("items_pushed_to_cart", "data"),
    Output('cart-items', 'children'),
    Input({"type": "card_item_quantity", "index": ALL}, "value"),
    Input({"type": "page_switcher_action", "index": ALL}, "n_clicks"),
    Input({"type": "x_out_from_cart", "index": ALL}, "n_clicks"),
    State("items_pushed_to_cart", "data"),
    prevent_initial_call=True,
)



clientside_callback(
    ClientsideFunction(
    namespace='clientside',
    function_name='CardItemDetails'
),
Output("card_item_detail_drawer", "opened"),
Output("card_item_detail_drawer", "children"),
Input({"type": "card_image_action", "index": ALL}, "n_clicks"),
State("all_stored_products", "data"),
prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050 )

