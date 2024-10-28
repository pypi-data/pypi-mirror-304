import Web_Component   from '../../core/Web_Component.mjs'
import Layout          from '../../css/grid/Layout.mjs'
import CSS__Grid       from '../../css/grid/CSS__Grid.mjs'
import CSS__Typography from '../../css/CSS__Typography.mjs'

export default class WebC__CBR__Layout__Default extends Web_Component {
    load_attributes() {
        this.css_grid = new CSS__Grid(this)
        this.css_typography = new CSS__Typography(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    extra_css_rules() {
        return {
            // Using colors from CSS__Typography
            ".layout": {
                border: "2px solid #4A90E2",     // blue
                padding: "2px",
                minHeight: "50px"
            },
            ".row": {
                border: "2px solid #198754",     // success color
                padding: "2px",
                minHeight: "30px",
                margin: "2px"
            },
            ".col, [class*='col-']": {
                border: "2px solid #DD00ee",     // accent color
                padding: "2px",
                minHeight: "20px",
                margin: "2px"
            }
        }
    }

    render() {
        let layout, content_row, menu_row

        layout      = new Layout({ class: 'h-500px' })                                                       // Initialize main layout
        layout      .add_row()                                                                               // Add top banner
                    .add_col({ class: 'p-3 h-50px bg-blue'                       ,  value: 'Top Banner'  })

        content_row = layout     .add_row({ class: 'flex-fill flex-nowrap'                               })  // Add content row
        menu_row    = content_row.add_col({ width: 200                                                   })  //Add sidebar with menu and fixed section
                                 .add_row({ class: 'flex-column h-100pc'                                 })
        menu_row    .add_col({ class: 'p-3 flex-fill bg-light-green'             , value: 'Left Menu'    }).parent()
                    .add_col({ class: 'h-50px p-3 bg-light-black color-white'    , value: 'Fixed section'})

        content_row .add_col({class: 'p-3 flex-fill bg-light-gray'               ,  value: 'Content area'})


        if (this.apply_css) {
            this.css_grid.apply_framework()
            this.css_typography.apply_framework()
            //this.add_css_rules(this.extra_css_rules())
        }

        this.set_inner_html(layout.html())
    }
}

WebC__CBR__Layout__Default.define()
