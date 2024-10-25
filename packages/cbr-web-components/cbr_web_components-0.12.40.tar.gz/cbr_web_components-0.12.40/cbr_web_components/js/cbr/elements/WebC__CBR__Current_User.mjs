import CBR_User_Data              from "../utils/CBR_User_Data.mjs";
import Web_Component from "../../core/Web_Component.mjs";
import Div from "../../core/Div.mjs";
import Pre from "../../core/Pre.mjs";
import H   from "../../core/H.mjs";

export default class WebC__CBR__Current_User extends Web_Component {

    cbr_user_data = new CBR_User_Data()

    async connectedCallback() {
        super.connectedCallback()
        this.setup()
        await this.build()
        this.raise_event('build-complete')
    }
    setup() {
        window.cbr_user_data             = this.cbr_user_data
    }
    async build() {
        const current_session     = await this.cbr_user_data.current_session()
        const user_profile        = await this.cbr_user_data.user_profile()
        const div_current_user    = new Div({class:'current_user'})
        const h2_user_profile     = new H({level:1, value:'User Profile'})
        const pre_user_profile    = new Pre({value: JSON.stringify(user_profile, null, 2)})
        const h2_current_session  = new H({level:1, value:'Current Session'})
        const pre_current_session = new Pre({value: JSON.stringify(current_session, null, 2)})

        div_current_user.add_elements(h2_user_profile,pre_user_profile,  h2_current_session, pre_current_session)
        //div_current_user.add_elements(h2_user_profile,  h2_current_session, pre_current_session)

        this.set_inner_html(div_current_user.html())
    }
}

WebC__CBR__Current_User.define()