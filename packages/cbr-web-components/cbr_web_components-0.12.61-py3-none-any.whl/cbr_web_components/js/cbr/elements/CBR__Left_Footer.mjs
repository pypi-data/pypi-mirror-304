import Div  from "../../core/Div.mjs"
import Icon from "../../css/icons/Icon.mjs"

export default class CBR__Left_Footer extends Div {
    constructor({id, ...kwargs}={}) {
        kwargs.class = `left-footer ${kwargs.class || ''}`
        super({id, ...kwargs})

        const settingsContainer = new Div({
            class: 'settings-container'
        })

        const settingsIcon = new Icon({
            icon: 'settings',
            class: 'icon-md'
        })

        const logoutIcon = new Icon({
            icon: 'logout',
            class: 'icon-md'
        })

        settingsContainer.add_elements(
            settingsIcon,
            new Div({ class: 'version-text', value: '© Cyber Boardroom - v0.208.12' }),
            logoutIcon
        )

        this.add_element(settingsContainer)
    }

    static css_rules() {
        return {
            ".left-footer": {
                display: "flex",
                alignItems: "center",
                padding: "0 1rem",
                height: "100%",
                backgroundColor: "#2D3436",
                color: "#ffffff"
            },
            ".settings-container": {
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                width: "100%"
            },
            ".version-text": {
                fontSize: "0.75rem",
                color: "#96a5ac"
            },
            ".icon": {
                color: "#96a5ac",
                cursor: "pointer",
                transition: "color 0.2s ease-in-out"
            },
            ".icon:hover": {
                color: "#ffffff"
            }
        }
    }
}