import Web_Component        from '../../core/Web_Component.mjs'
import Layout               from '../../css/grid/Layout.mjs'
import CSS__Grid            from '../../css/grid/CSS__Grid.mjs'
import CSS__Typography      from '../../css/CSS__Typography.mjs'
import CSS__Side_Menu       from "../../css/menus/CSS__Side_Menu.mjs"
import Left_Menu            from "../../css/menus/Left_Menu.mjs";
import CBR__Left_Footer     from "../elements/CBR__Left_Footer.mjs";
import CBR__Top_Banner      from "../elements/CBR__Top_Banner.mjs";

export default class WebC__CBR__Layout__Default extends Web_Component {
    load_attributes() {
        new CSS__Grid      (this).apply_framework()
        new CSS__Typography(this).apply_framework()
        new CSS__Side_Menu (this).apply_framework()

        this.add_css_rules(CBR__Top_Banner.css_rules())
    }

    render() {
        let layout, row_banner, row_content

        layout      = new Layout({ id:'main-page', class: 'h-100vh p-0' })
        row_banner  = layout.add_row()
        row_content = layout.add_row({class: 'flex-fill flex-nowrap'                           })

        row_banner .add_col({ id: 'top-banner' , class: 'p-3 h-50px bg-blue'                   })
        row_content.add_col({                    class: 'w-250px flex-column d-flex'           })
                   .add_col({ id: 'left-menu'  , class: 'flex-fill bg-white'                   }).parent()
                   .add_col({ id: 'left-footer', class: 'h-50px p-3 bg-light-black color-white'})
        row_content.add_col({ id: 'content'    , class: 'p-3 flex-fill bg-light-gray'          })

        layout.with_id('left-menu').add_tag({ tag: 'webc-api-side-menu' })

            // Define menu structure
        let menu_items = [{ icon: 'home'    , label: 'Home'            , href: '/'             },
                            { icon: 'robot'  , label: 'Athena'          , href: '/web_components/html/webc-dev.html' },
                            { icon: 'person' , label: 'Personas'        , href: '/personas'     },
                            { icon: 'history', label: 'Past Chats'      , href: '/past-chats'   },
                            { icon: 'profile', label: 'Profile'         , href: '/profile'      },
                            { icon: 'chat'   , label: 'Chat with LLMs'  , href: '/chat'         },
                            { icon: 'docs'   , label: 'Docs'            , href: '/docs'         }]

        // Add side menu
        layout.with_id('left-menu' ).add_element(new Left_Menu({ menu_items: menu_items }))
        layout.with_id('top-banner').add_element(new CBR__Top_Banner({ username: 'guest'}))



        this.set_inner_html(layout.html())
    }
}

WebC__CBR__Layout__Default.define()
