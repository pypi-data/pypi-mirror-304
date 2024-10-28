import Web_Component    from '../../core/Web_Component.mjs';
import Layout           from '../grid/Layout.mjs';
import Row              from '../grid/Row.mjs';
import Col              from '../grid/Col.mjs';
import CSS__Grid        from '../grid/CSS__Grid.mjs';
import CSS__Typography  from '../CSS__Typography.mjs';

export default class WebC__CSS__Layout_1 extends Web_Component {
    load_attributes() {
        this.css_grid       = new CSS__Grid(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css      = this.hasAttribute('no-css') === false
    }

    css_rules__layout() {
        return {
            //".layout-root"   : { height       : "500px"                     },
            ".layout-content": { flex         : "1 1 auto"                  },
            ".sidebar-col"   : { maxWidth     : "250px"                     },
            ".content-col"   : { minWidth     : 0                           ,
                                flex          : "1 1 1px"                   ,},
        }
    }

    render() {
        let layout      = new Layout({ class: 'h-500px layout-root' })
        let banner_row  = new Row   ()
        let banner_col  = new Col   ({ class: 'h-75px p-3 bg-blue',  value: 'Top Banner' })
        let content_row = new Row   ({ class: 'layout-content' })
        let main_col    = new Col   ({ class: 'content-col p-3 bg-light-gray',  value: 'Content area' })
        let sidebar_col = new Col   ({ class: 'sidebar-col'                                                                })
        let menu_row    = new Row   ({ class: 'flex-column h-100pc'                                                        })
        let menu_col    = new Col   ({ class: 'flex-fill p-3 bg-light-green'                       ,  value: 'Left Menu'   })
        let fixed_col   = new Col   ( {class: 'h-50px p-3 bg-light-black fixed-section color-white', value: 'Fixed section'})

        banner_row.add_elements(banner_col)
        menu_row.add_elements(menu_col, fixed_col)
        sidebar_col.add_elements(menu_row)

        // Main content column


        content_row.add_elements(sidebar_col, main_col)
        layout.add_elements(banner_row, content_row)

        if (this.apply_css) {
            this.css_grid.apply_framework()
            this.css_typography.apply_framework()
            this.add_css_rules(this.css_rules__layout())
        }

        this.set_inner_html(layout.html())
    }
}

WebC__CSS__Layout_1.define()