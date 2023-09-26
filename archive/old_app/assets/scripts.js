

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {

        show_dcc_stored_items: function (data, category_chips, provider_chips, load_more, search, items_in_cart) {

            let filtereddata = data.filter((country) => country.product_name.toLowerCase().startsWith(search));
           
             if (category_chips) {
                if (category_chips.length !== 0)  {
                    filtereddata = filtereddata.filter( item => category_chips.includes( item.category ) );
                }
            }

             if (provider_chips) {
                if (provider_chips.length !== 0)  {
              
                    filtereddata = filtereddata.filter( item => provider_chips.includes( item.provider ) );
                }
              
            }
            let filteredDataLength = filtereddata.length
            let paginations_size = 2
            let start = load_more * paginations_size
            let end = start + paginations_size
            let remaining_items = filteredDataLength - end

            filtereddata = filtereddata.slice(0, end)

            let article_card = []
            filtereddata.forEach((article)=> {
              
            quantity = 0
            if (article.product_code in items_in_cart) {
                quantity = items_in_cart[article.product_code].quantity
    
            }


                article_card.push(
                    {'props': {'children': [
                        {'props': {'children': {'props': {'children': {'props': {'src': `assets/images/${article.product_code}.png`, 'width': 150, 'height' :150, 'fit':'contain'}, 'type': 'Image', 'namespace': 'dash_mantine_components'}}, 'type': 'Center', 'namespace': 'dash_mantine_components'}, 'p': 30}, 'type': 'CardSection', 'namespace': 'dash_mantine_components'},
                         {'props': {'children': [{'props': {'children': article.product_name, 'id':  article.product_code, 'className': 'article_name'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}]}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 
                         {'props': {'children': 
    
                         {'props': {'children': [
                                {'props': {'children': {'props': {'children': `${article.price} DA`, 'id': `price_${ article.product_code}`, 'className': 'price_test'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': 'item_type_column', 'span': 4}, 'type': 'Col', 'namespace': 'dash_mantine_components'},
                                {'props': {'children': {'props': {'id': `number_input_card_${ article.product_code}`, 'className': 'item_type_number_input', 'hideControls': true, 'value': quantity}, 'type': 'NumberInput', 'namespace': 'dash_mantine_components'}, 'className': 'item_type_column', 'span': 2}, 'type': 'Col', 'namespace': 'dash_mantine_components'}, 
                                {'props': {'children': {'props': {'children': '0 DA', 'id': `sum_${ article.product_code}`, 'className': 'price_test'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': 'item_type_column', 'span': 4}, 'type': 'Col', 'namespace': 'dash_mantine_components'}
                            ], 'align': 'center', 'className': 'item_type_grid', 'gutter': 'xl', 'justify': 'center'}, 'type': 'Grid', 'namespace': 'dash_mantine_components'}
                        
                        
                        }, 'type': 'Paper', 'namespace': 'dash_mantine_components'}
                        ], 'radius': 'md', 'shadow': 'sm', 'style': {'width': 396}, 'withBorder': true}, 'type': 'Card', 'namespace': 'dash_mantine_components'}
                )
                });
        
                if(remaining_items > 0) {
                    return [{'props': {'children': article_card}, 'type': 'Div', 'namespace': 'dash_html_components'}, remaining_items, 'block']


                }
            return [{'props': {'children': article_card}, 'type': 'Div', 'namespace': 'dash_html_components'},  remaining_items, 'none']
       
     

    },
        update_cart_itmes: function (number_input_card, item_name, price, data) {
            price = price.match(/\d+/)[0]
            item_code = window.dash_clientside.callback_context.states_list[0]['id']

            if (number_input_card) {
   
                data[item_code] = {
                    'price':price,
                    'quantity':number_input_card,
                    'total': price*number_input_card
                    }
                let total = number_input_card*price
            
                return [data,  `${total.toFixed(2)} DA`]
            }

        return [ window.dash_clientside.no_update,'0 DA']
        
        },

    show_cart_items: function (data) {
   
        
        // if (Object.keys(data).length !== 0 ) {
         
        // }
        // console.log(data)
        var articles = []
        Object.entries(data).forEach(([item_name, item_order]) => {
            
           
            articles.push(
                {'props': {'children': [
                    {'props': {'children': {'props': {'src':  `assets/images/${item_name}.png`, 'width': 40}, 'type': 'Image', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 3}, 'type': 'Col', 'namespace': 'dash_mantine_components'},
                    {'props': {'children': {'props': {'children': item_name}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 3}, 'type': 'Col', 'namespace': 'dash_mantine_components'}, 
                    {'props': {'children': {'props': {'children': `${ item_order['price']} DA`, 'id': `price_cart_${ item_name}`, 'className': 'price_test'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 2}, 'type': 'Col', 'namespace': 'dash_mantine_components'}, 
                    {'props': {'children': {'props': {id :`number_input_cart_${item_name}`, 'hideControls': true, 'value': item_order['quantity']},  'type': 'NumberInput', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 2}, 'type': 'Col', 'namespace': 'dash_mantine_components'}, 
                    {'props': {'children': {'props': {'children': item_order['total'],  id:`sum_cart_${ item_name}`}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 2}, 'type': 'Col', 'namespace': 'dash_mantine_components'}
                ], 
                'align': 'center', 
                'className': 'checkout_grids',
                 'gutter': 'xl', 'justify': 'center'
                }, 'type': 'Grid', 'namespace': 'dash_mantine_components'}

            )
            
        
        });

        let items = {'props': {'children': articles}, 'type': 'Div', 'namespace': 'dash_html_components'}
        let header = {'props': {'children': [
            {'props': {'children': '', 'className': '', 'span': 3}, 'type': 'Col', 'namespace': 'dash_mantine_components'},
            {'props': {'children': {'props': {'children': 'Article'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 3}, 'type': 'Col', 'namespace': 'dash_mantine_components'}, 
            {'props': {'children': {'props': {'children': 'Prix Unite'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 2}, 'type': 'Col', 'namespace': 'dash_mantine_components'}, 
            {'props': {'children': {'props': {'children': 'Quantite'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 2}, 'type': 'Col', 'namespace': 'dash_mantine_components'}, 
            {'props': {'children': {'props': {'children': 'Total'}, 'type': 'Text', 'namespace': 'dash_mantine_components'}, 'className': '', 'span': 2}, 'type': 'Col', 'namespace': 'dash_mantine_components'}
        ], 
        'align': 'center', 
        'className': 'checkout_grids',
         'gutter': 'xl', 'justify': 'center'
        }, 'type': 'Grid', 'namespace': 'dash_mantine_components'}

        return {'props': {'children': [header, items]}, 'type': 'Div', 'namespace': 'dash_html_components'}

    },
   
    },


    
});