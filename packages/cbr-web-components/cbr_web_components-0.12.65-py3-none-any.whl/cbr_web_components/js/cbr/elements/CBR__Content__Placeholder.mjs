import Div from "../../core/Div.mjs"
import Raw_Html from "../../core/Raw_Html.mjs"

export default class CBR__Content__Placeholder extends Div {
    constructor({id, ...kwargs}={}) {
        kwargs.class = `content-placeholder ${kwargs.class || ''}`
        super({id, ...kwargs})

        const div_container = new Div({ class: 'placeholder-container'                                    })
        const html_code = new Raw_Html()
        html_code.raw_html = `
<webc-api-markdown-to-html content-path='en/web-site/home-page/welcome.md' apply-css> </webc-api-markdown-to-html>

<webc-container>
    <webc-video title="An Introduction to The Cyber Boardroom"         width="100%" height="275" url="https://470426667096-cbr.s3.eu-west-2.amazonaws.com/cbr_website_static/assets/videos/video-tcb__introduction__27-feb-2024.mp4"> </webc-video>
    <webc-video title="Meet Athena, your GenAI Cyber Security Advisor" width="100%" height="275" url="https://470426667096-cbr.s3.eu-west-2.amazonaws.com/cbr_website_static/assets/videos/video-tcb__meet-athena__25-feb-2024.mp4"></webc-video>
</webc-container>

<webc-container>
    <webc-markdown-card content-path='en/web-site/home-page/card-1.md' apply-css> </webc-markdown-card>
    <webc-markdown-card content-path='en/web-site/home-page/card-2.md' apply-css> </webc-markdown-card>
</webc-container>
`

        div_container.add_element(html_code)
        this.add_element(div_container)


    }

    static css_rules() {
        return {
            ".placeholder-container": { height          : '100%',
                                        width           : '100%',
                                        backgroundColor : "#eef5f9",                          // Light base color
                                        boxShadow       : "inset 10px 20px 30px rgba(0,0,0,0.07)",  // Soft shadow
            }
        }
    }
}