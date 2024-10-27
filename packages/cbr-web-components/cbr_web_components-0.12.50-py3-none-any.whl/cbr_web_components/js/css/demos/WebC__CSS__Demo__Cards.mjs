import Web_Component   from '../../core/Web_Component.mjs';
import Button          from '../../core/Button.mjs';
import Div             from '../../core/Div.mjs';
import H               from '../../core/H.mjs';
import HR              from '../../core/HR.mjs';
import P               from '../../core/P.mjs';
import Img             from '../../core/Img.mjs';
import Text            from '../../core/Text.mjs';
import CSS__Cards      from '../CSS__Cards.mjs';
import CSS__Typography from '../CSS__Typography.mjs';
import CSS__Buttons    from '../CSS__Buttons.mjs';


export default class WebC__CSS__Demo__Cards extends Web_Component {
    load_attributes() {
        this.css_cards = new CSS__Cards(this)
        this.css_typography = new CSS__Typography(this)
        this.css_buttons = new CSS__Buttons(this)
        this.apply_css = this.hasAttribute('no-css') === false
    }

    render() {
        let div_root = new Div({ id: 'cards-demo' })

        // Header
        let header = [
            new HR(),
            new Text({ value: 'Cards Demo' + (this.apply_css ? ' (with CSS)' : '') }),
            new HR()
        ]

        // Basic Card
        let h_basic = new H({ level: 2, value: 'Basic Card' })
        let basic_card = new Div({ class: 'card' }).add_elements(
            new Div({ class: 'card-body' }).add_elements(
                new H({ level: 5, class: 'card-title', value: 'Card title' }),
                new H({ level: 6, class: 'card-subtitle', value: 'Card subtitle' }),
                new P({ class: 'card-text', value: 'Some quick example text to build on the card title and make up the bulk of the card\'s content.' }),
                new Button({ class: 'btn btn-primary', value: 'Go somewhere' })
            )
        )

        // Card with Header and Footer
        let h_header_footer = new H({ level: 2, value: 'Card with Header and Footer' })
        let header_footer_card = new Div({ class: 'card' }).add_elements(
            new Div({ class: 'card-header', value: 'Featured' }),
            new Div({ class: 'card-body' }).add_elements(
                new H({ level: 5, class: 'card-title', value: 'Special title treatment' }),
                new P({ class: 'card-text', value: 'With supporting text below as a natural lead-in to additional content.' }),
                new Button({ class: 'btn btn-primary', value: 'Go somewhere' })
            ),
            new Div({ class: 'card-footer', value: '2 days ago' })
        )

        // Card with Image
        let h_image = new H({ level: 2, value: 'Card with Image' })
        let image_card = new Div({ class: 'card' }).add_elements(
            new Img({ class: 'card-img-top', src: '/assets/dev/img/400x200.png', alt: 'Card image cap' }),
            new Div({ class: 'card-body' }).add_elements(
                new H({ level: 5, class: 'card-title', value: 'Card title' }),
                new P({ class: 'card-text', value: 'This is a wider card with supporting text below as a natural lead-in to additional content.' })
            )
        )

        // Horizontal Card
        let h_horizontal = new H({ level: 2, value: 'Horizontal Card' })
        let horizontal_card = new Div({ class: 'card card-horizontal' }).add_elements(
            new Img({ class: 'card-img', src: '/assets/dev/img/400x200.png', alt: 'Card image' }),
            new Div({ class: 'card-body' }).add_elements(
                new H({ level: 5, class: 'card-title', value: 'Card title' }),
                new P({ class: 'card-text', value: 'This is a wider card with supporting text below as a natural lead-in to additional content.' })
            )
        )

        // Card Group
        let h_group = new H({ level: 2, value: 'Card Group' })
        let card_group = new Div({ class: 'card-group' }).add_elements(
            new Div({ class: 'card' }).add_elements(
                new Div({ class: 'card-body' }).add_elements(
                    new H({ level: 5, class: 'card-title', value: 'Card 1' }),
                    new P({ class: 'card-text', value: 'This is a wider card with supporting text below as a natural lead-in to additional content.' })
                )
            ),
            new Div({ class: 'card' }).add_elements(
                new Div({ class: 'card-body' }).add_elements(
                    new H({ level: 5, class: 'card-title', value: 'Card 2' }),
                    new P({ class: 'card-text', value: 'This card has supporting text below as a natural lead-in to additional content.' })
                )
            ),
            new Div({ class: 'card' }).add_elements(
                new Div({ class: 'card-body' }).add_elements(
                    new H({ level: 5, class: 'card-title', value: 'Card 3' }),
                    new P({ class: 'card-text', value: 'This is a wider card with supporting text below as a natural lead-in to additional content.' })
                )
            )
        )

        // Card Deck
        let h_deck = new H({ level: 2, value: 'Card Deck (Grid Layout)' })
        let card_deck = new Div({ class: 'card-deck' }).add_elements(
            new Div({ class: 'card card-hover' }).add_elements(
                new Div({ class: 'card-body' }).add_elements(
                    new H({ level: 5, class: 'card-title', value: 'Hoverable Card 1' }),
                    new P({ class: 'card-text', value: 'This is a wider card with supporting text below as a natural lead-in to additional content.' })
                )
            ),
            new Div({ class: 'card card-hover' }).add_elements(
                new Div({ class: 'card-body' }).add_elements(
                    new H({ level: 5, class: 'card-title', value: 'Hoverable Card 2' }),
                    new P({ class: 'card-text', value: 'This card has supporting text below as a natural lead-in to additional content.' })
                )
            ),
            new Div({ class: 'card card-hover' }).add_elements(
                new Div({ class: 'card-body' }).add_elements(
                    new H({ level: 5, class: 'card-title', value: 'Hoverable Card 3' }),
                    new P({ class: 'card-text', value: 'This is a wider card with supporting text below as a natural lead-in to additional content.' })
                )
            )
        )

        // Image Overlay Card
        let h_overlay = new H({ level: 2, value: 'Image Overlay Card' })
        let overlay_card = new Div({ class: 'card' }).add_elements(
            new Img({ class: 'card-img', src: '/assets/dev/img/400x200.png', alt: 'Card image' }),
            new Div({ class: 'card-img-overlay' }).add_elements(
                new H({ level: 5, class: 'card-title', value: 'Card title', style: 'color: white;' }),
                new P({ class: 'card-text', value: 'This is a wider card with supporting text below as a natural lead-in to additional content.', style: 'color: white;' })
            )
        )

        // Add all sections to root
        div_root.add_elements(
            ...header,
            h_basic, basic_card,
            h_header_footer, header_footer_card,
            h_image, image_card,
            h_horizontal, horizontal_card,
            h_group, card_group,
            h_deck, card_deck,
            h_overlay, overlay_card
        )

        // Apply CSS if needed
        if (this.apply_css) {
            this.css_cards.apply_framework()
            this.css_typography.apply_framework()
            this.css_buttons.apply_framework()
        }

        this.set_inner_html(div_root.html())
    }
}

WebC__CSS__Demo__Cards.define()