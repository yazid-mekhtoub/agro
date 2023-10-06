

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
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],
)

data = pd.read_csv('products.csv').tail(15)
data = data.to_dict('records')


def shop_card(product_name, product_code, product_price,  product_quantity, image_path):
    return dmc.Grid(
            className = 'card-grid',
            justify = 'center',
            children = [
                dmc.Col(
                className = 'card-image-column',
                p = 5,
                    span = 3,
                    children = [
                        dmc.ActionIcon(dmc.Image(src=image_path, className = 'card-image').to_plotly_json() , style = {'width':'100%', 'height':'100%'}, id={"type": "card_image_action", "index":product_code}).to_plotly_json() 
                    ]
                ).to_plotly_json(),
                dmc.Col(
                    span = 'auto',
                    children = [
                        dmc.Grid(
                            children=[
                                dmc.Col(dmc.Text(product_name, size="lg", weight=500,).to_plotly_json(), span=7, px = 0).to_plotly_json(),
                                dmc.Col(dmc.Text(product_price, size="md", weight=900, align="right" , color = 'green',  id={"type": "card_item_price", "index":product_code}).to_plotly_json(), span=5,  px = 0).to_plotly_json(),
                            ],
                        ).to_plotly_json(),
                        dmc.Grid(
                            justify = 'flex-end',
                            children=[
                                dmc.Col( 
                                span=4, px = 0,
                                    children =[
                                        dmc.Stack(
                                            align="center",
                                            children = [
                                                dmc.NumberInput(min=0, w = 50, h = 30, mih = 20, size = 'lg', hideControls =  True, className='card-quantity-input', value = product_quantity, id={"type": "card_item_quantity", "index": product_code}, placeholder=0).to_plotly_json(),
                                                dmc.Text("Quantity", size="md", weight=600, align="right" ).to_plotly_json(),

                                            ]
                                        ).to_plotly_json() 
                                    ]
                                ).to_plotly_json(),
                                dmc.Col(    
                                    span=5, px = 0,
                                    children =[
                                        dmc.Stack(
                                            align="center",
                                            children = [
                                                dmc.Text(id={"type": "card_item_total", "index":product_code}, size="md", lh = '30px', weight='bolder').to_plotly_json(),
                                                dmc.Text("Total", size="md", weight=600, align="right" ).to_plotly_json(),                                               

                                            ]
                                        ).to_plotly_json()
                                    ]
                                ).to_plotly_json()
                            ]
                        ).to_plotly_json()
                    ]
                ).to_plotly_json()
            ]
        ).to_plotly_json()


shop = dmc.Paper(
    id = id_dict('page_layout_id', 'shop'),
    style = {'display':'block'},
    className = 'page',

    children = [
        html.Div(id = 'filter_chips_container'),
        

        dmc.TextInput(
            id = 'search_item',
            size = 'md',
            placeholder="Search",
            rightSection=icon(icon="guidance:search"),
        ),
        dmc.Container(id = 'products_container'),




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
# print( html.Div([html.Div(['visible']).to_plotly_json(), html.Div(['hidden'],style = {'display':f'none'},).to_plotly_json()]).to_plotly_json())
# print(pprint.pformat( shop_card('product_name', 'product_code', 'product_price',  'product_quantity', 'image_path')))
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
            id="drawer-position",
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
                dcc.Store(id = 'all_stored_products'),
                dcc.Store(id = 'items_pushed_to_cart', data = {}),
                dmc.Text(id='void'),
                    ]
                )
            ]
        ) 
    ]
)
@callback(
        Output('all_stored_products', 'data'),
        Output('filter_chips_container', 'children'),
        Input('void', 'children'))
def on_data_set_graph(void):

    filters = {
         "category": set(),
         "provider": set()
        }
    
    for item in data:
        filters["category"].add(item['category'])
        filters["provider"].add(item['provider'])
    filters["category"] =  list(filters["category"])
    filters["provider"] =  list(filters["provider"])

    chips_category  = dmc.ChipGroup(
                children = [
                     dmc.Chip(x, value=x, size = 'lg') for x in  filters["category"]
                ],
                multiple=True,
                value= filters["category"][0],
                id = 'product_category'
            )
    chips_provider  = dmc.ChipGroup(
                children = [
                     dmc.Chip(x, value=x, size = 'lg') for x in  filters["provider"]
                ],
                # multiple=True,
                id = 'product_povider',
                value= filters["provider"][0]
            )

    return data, html.Div([chips_category, chips_provider])

clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='make_cards'
    ),
        Output('products_container', 'children'),
        Input('product_povider', 'value'),
        State("items_pushed_to_cart", "data"),
        State("all_stored_products", "data"),
)

# @app.callback(
#         Output('products_container', 'children'),
#         Input('product_povider', 'value'),
#         State("items_pushed_to_cart", "data"),
#         State("all_stored_products", "data"),
#     )

# def on_data_set_graph(product_povider, items_pushed_to_cart, _data):

#     visible  = []
#     hidden = []
#     items_in_cart_and_filtered_data = []
#     items_in_cart_not_in_filtered_data = []
#     not_in_cart_and_filtered_data = []
#     for item in _data:

#         product_code = item['product_code']
#         _product_provider = item['provider']
#         if  product_code in items_pushed_to_cart and  _product_provider == product_povider:
#             items_in_cart_and_filtered_data.append(item)
#         elif product_code in items_pushed_to_cart and  _product_provider != product_povider:
#             items_in_cart_not_in_filtered_data.append(item)
#         elif product_code not in items_pushed_to_cart and  _product_provider == product_povider:
#             not_in_cart_and_filtered_data.append(item)


#     product_quantity = None
#     for item in not_in_cart_and_filtered_data + items_in_cart_and_filtered_data:

#         product_code = item['product_code']
#         if item in items_in_cart_and_filtered_data:
#             product_quantity = items_pushed_to_cart[item['product_code']]['item_quantity']

   
#         visible.append(
#                 shop_card(
#                     item['product_name'], 
#                     product_code, 
#                     item['price'],  
#                     product_quantity, 
#                     f'/assets/images/{product_code}.png',
#                 ),
#             )
        
#     for item in items_in_cart_not_in_filtered_data:
#         product_quantity = items_pushed_to_cart[item['product_code']]['item_quantity']
#         product_code = item['product_code']
#         hidden.append(
#                 shop_card(
#                     item['product_name'], 
#                     product_code, 
#                     item['price'],  
#                     product_quantity, 
#                     f'/assets/images/{product_code}.png',
#                 ),
#             )

#     return html.Div([html.Div(visible), html.Div(hidden,style = {'display':f'none'},)])

# @app.callback(
#         Output({"type": "card_item_total", "index": MATCH}, "children"), 
#         Input({"type": "card_item_quantity", "index": MATCH}, "value"),
#         State({"type": "card_item_price", "index": MATCH}, "children"))

# def item_card_add_item(card_item_quantity, item_price):
#     if  not card_item_quantity:
#         card_item_quantity = 0

#     return round(card_item_quantity*item_price, 2)

# @app.callback(
#         Output({"type": "card_item_total", "index": MATCH}, "children"), 
#         Input({"type": "card_item_quantity", "index": MATCH}, "value"),
#         State({"type": "card_item_price", "index": MATCH}, "children"))

# def item_card_add_item(card_item_quantity, item_price):
#     if  not card_item_quantity:
#         card_item_quantity = 0

#     return round(card_item_quantity*item_price, 2)

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
 

# @app.callback(
#         Output({"type": "cart_item_total", "index": MATCH}, "children"), 
#         Input({"type": "card_item_quantity", "index": MATCH}, "value"),
#         State({"type": "card_item_price", "index": MATCH}, "children"))

# def item_card_add_item(card_item_quantity,item_price ):
#     if  not card_item_quantity:
#         card_item_quantity = 0
        
#     return round(card_item_quantity*item_price, 2)

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

# @app.callback(
#         Output({"type": "cart_item_quantity", "index": MATCH}, "value"), 
#         Output({"type": "card_item_quantity", "index": MATCH}, "value"), 
         
#         Input({"type": "card_item_quantity", "index": MATCH}, "value"),
#         Input({"type": "cart_item_quantity", "index": MATCH}, "value"),
#         prevent_initial_call=True,
#     )

# def stored_items(card_item_quantity, cart_item_quantity):


#     if ctx.triggered_id['type'] =='card_item_quantity':
#         return  card_item_quantity, card_item_quantity

#     elif ctx.triggered_id['type'] =='cart_item_quantity':
#         return  cart_item_quantity, cart_item_quantity
        


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


# @callback(
#         Output("items_pushed_to_cart", "data"),
#         Output('cart-items', 'children'),
#         Input({"type": "card_item_quantity", "index": ALL}, "value"),
#         Input({"type": "page_switcher_action", "index": ALL}, "n_clicks"),
#         Input({"type": "x_out_from_cart", "index": ALL}, "n_clicks"),
#         State("items_pushed_to_cart", "data"),
#         prevent_initial_call=True,
# )

# def item_card_add_item(cart_click, x_click, card_item_quantity, items_pushed_to_cart):

#     for item in ctx.inputs_list[0]:
#         item_quantity = item.get("value")
#         item_id = item['id']['index']
#         if item_quantity or item_quantity ==0: 
#             items_pushed_to_cart[item_id] = {
#                     'product_code':item_id,
#                     'item_quantity': item_quantity,
#                 }
#     if ctx.triggered_id['type'] == 'x_out_from_cart':
#         items_pushed_to_cart[ctx.triggered_id['index']][ 'item_quantity'] = 0
    

#     if ctx.triggered_id['type'] == 'card_item_quantity':
#         return items_pushed_to_cart, no_update
    
#     cart_items = []
#     header =    dmc.Grid(
#             m = 0,
#             align ='center',
#                 children=[
#                     dmc.Col(
#                         span=2,
                        
#                         children = [
#                            dmc.Text('', className='cart-items-headers').to_plotly_json()
#                         ]
#                     ).to_plotly_json(),
#                     dmc.Col(
#                         span=6,
#                         children = [
#                              dmc.Text('Produit', className='cart-items-headers').to_plotly_json()
#                         ]
#                     ).to_plotly_json(),
#                     dmc.Col(
#                         span=2,
#                         children = [
#                              dmc.Text('Quantity', className='cart-items-headers').to_plotly_json()
#                         ]
#                     ).to_plotly_json(),        
#                     dmc.Col(
#                         span=2,
#                         children = [
#                              dmc.Text('Total', className='cart-items-headers', ta = 'center').to_plotly_json()
#                         ]
#                     ).to_plotly_json()

#                 ]
#             ).to_plotly_json()
    
#     cart_items.append(header)


#     def cart_item (item_image_path, product_code, product_quantity, style):
#         return dmc.Grid(
#               style=style,
#             m = 0,
#             align ='center',
#                 children=[
#                     dmc.Col(
#                         span=2,
                      
#                         children = [
#                             dmc.Image(src=item_image_path,  height = 30, fit = 'contain').to_plotly_json()  
#                         ]
#                     ).to_plotly_json(),
#                     dmc.Col(
#                         span=6,
#                         children = [
#                             dmc.Text(product_code[:40], maw = 150, size = 'sm').to_plotly_json()
#                         ]
#                     ).to_plotly_json(),
#                     dmc.Col(
#                         span=2,
#                         children = [
#                             dmc.NumberInput(id={"type": "cart_item_quantity", "index": product_code}, value = product_quantity, hideControls =  True, className='cart-quantity-input'
#                                             # min=0, w = 40, h = 30, mih = 20, size = 'sm',className='cart-quantity-input'
#                                             ).to_plotly_json()
#                         ]
#                     ).to_plotly_json(),        
#                     dmc.Col(
#                         span=2,
#                          pos = 'relative',
#                         children = [
#                             dmc.Text( 0, id={"type": "cart_item_total", "index":product_code}, style = {'float':'right'}, 
#                                      size = 'sm').to_plotly_json(),
#                                    dmc.ActionIcon(
#                                 id={"type": "x_out_from_cart", "index":product_code},
#                                 variant='transparent',  
#                                 pos = 'absolute',
#                                 top = '-10px',
#                                 right= '-10px',

                            
#                                 children = [
#                                    icon(icon="ph:x-light", width=15).to_plotly_json(),
#                                 ]
#                             ).to_plotly_json(),
#                         ]
#                     ).to_plotly_json()

#                 ]
#             ).to_plotly_json()
#     print(pprint.pformat( cart_item ('item_image_path', 'product_code', 'product_quantity', 'stylessssss') ))
#     for _, item in items_pushed_to_cart.items():
#         product_code= item['product_code']
#         product_quantity = item['item_quantity']
#         if product_quantity ==0:
#             style = {'display':'none'}
#         else:
#             style = {}
#         cart_items.append(
#             cart_item ( f'/assets/images/{product_code}.png', item['product_code'], product_quantity, style)
#         )


#     return items_pushed_to_cart, html.Div(cart_items)
    


@callback(
    Output("drawer-position", "opened"),
    Input({"type": "card_image_action", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def toggle_drawer(n_clicks):
    if any(n_clicks):
        return True
    return False


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050 )

#     // Assuming you have imported necessary modules and defined variables like `card_item_quantity` and `cart_item_quantity`

# // Define the client-side callback
# app.clientside_callback(
#     """
#     function(card_item_quantity, cart_item_quantity) {
#         if(card_item_quantity !== undefined) {
#             return card_item_quantity;
#         } else if(cart_item_quantity !== undefined) {
#             return cart_item_quantity;
#         } else {
#             return null;
#         }
#     }
#     """,
#     Output({"type": "card_item_quantity", "index": MATCH}, "value"),
#     Output({"type": "cart_item_quantity", "index": MATCH}, "value"),
#     Input({"type": "card_item_quantity", "index": MATCH}, "value"),
#     Input({"type": "cart_item_quantity", "index": MATCH}, "value")
# );

# app.clientside_callback(
#     """
#     function itemCardAddItem(cartClick, xClick, cardItemQuantity, itemsPushedToCart, itemsPushedToCartPrev) {
#         // Assuming ctx and dmc are defined as global variables
#         for (var i = 0; i < cardItemQuantity.length; i++) {
#             var item = cardItemQuantity[i];
#             var itemQuantity = item.value;
#             var itemID = item.id.index;
            
#             if (itemQuantity || itemQuantity === 0) {
#                 itemsPushedToCart[itemID] = {
#                     product_code: itemID,
#                     item_quantity: itemQuantity
#                 };
#             }
#         }
        
#         if (xClick.some(Boolean)) {
#             var xOutIndex = xClick.findIndex(Boolean);
#             itemsPushedToCart[xOutIndex].item_quantity = 0;
#         }
        
#         var cartItems = [];
        
#         if (cartClick.some(Boolean)) {
#             // Assuming 'ctx' and 'dmc' are defined as global variables
#             console.log('all', itemsPushedToCart);
#             return [itemsPushedToCart, null];
#         }
        
#         // Rest of your code to build 'cartItems' goes here
        
#         return [itemsPushedToCart, cartItems];
#     }
#     """,
#     Output("items_pushed_to_cart", "data"),
#     Output('cart-items', 'children'),
#     Input({"type": "card_item_quantity", "index": ALL}, "value"),
#     Input({"type": "page_switcher_action", "index": ALL}, "n_clicks"),
#     Input({"type": "x_out_from_cart", "index": ALL}, "n_clicks"),
#     State("items_pushed_to_cart", "data"),
#     State("items_pushed_to_cart", "data_previous"),
#     prevent_initial_call=True
# )

# Assuming 'app' is your Dash app instance

# app.clientside_callback(
#     """
#     function(card_item_quantity, page_switcher_action, x_out_from_cart, items_pushed_to_cart) {
#         // This is the client-side callback function
        
#         // Initialize items_pushed_to_cart if it's undefined
#         if (items_pushed_to_cart === undefined) {
#             items_pushed_to_cart = {};
#         }

#         // Loop through card_item_quantity
#         for (var i = 0; i < card_item_quantity.length; i++) {
#             var item = card_item_quantity[i];
#             var item_quantity = item.value;
#             var item_id = item.id.index;

#             if (item_quantity || item_quantity === 0) {
#                 console.log(item_quantity);
#                 items_pushed_to_cart[item_id] = {
#                     'product_code': item_id,
#                     'item_quantity': item_quantity,
#                 };
#             }
#         }

#         // Add code for page_switcher_action and x_out_from_cart if needed

#         // Define cart_items
#         var cart_items = [];

#         // Add code to generate cart_items

#         // Return the updated items_pushed_to_cart and cart_items
#         return [items_pushed_to_cart, cart_items];
#     }
#     """,
#     Output("items_pushed_to_cart", "data"),
#     Output("cart-items", "children"),
#     Input({"type": "card_item_quantity", "index": ALL}, "value"),
#     Input({"type": "page_switcher_action", "index": ALL}, "n_clicks"),
#     Input({"type": "x_out_from_cart", "index": ALL}, "n_clicks"),
#     State("items_pushed_to_cart", "data"),
#     prevent_initial_call=True
# )
