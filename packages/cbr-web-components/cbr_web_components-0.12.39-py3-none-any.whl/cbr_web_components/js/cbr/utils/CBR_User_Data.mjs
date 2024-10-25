import API__Invoke from "../../data/API__Invoke.mjs";

export default class CBR_User_Data {

    target_server             = ''
    url__api__user_profile    = '/api/user-data/user/user-profile'
    url__api__current_session = '/api/user-session/session/current-session'
    auth_header               = null

    constructor() {
        this.setup()
    }

    setup() {
        this.api_invoke = new API__Invoke()
    }

    async current_session() { return await this.api_invoke.invoke_api(this.target_server + this.url__api__current_session ,'GET',null, this.auth_header) }
    async user_profile   () { return await this.api_invoke.invoke_api(this.target_server + this.url__api__user_profile    ,'GET',null, this.auth_header) }

    async login_as_guest_one()  {
        this.login_as_a_guest('6f6df621-42e5-4579-99d8-969e592c1f2b')
    }
    async login_as_guest_two()  {
        this.login_as_a_guest('686a35ef-f78d-4158-a240-11e296cd187a')
    }
    async login_as_guest_three()  {
        this.login_as_a_guest('7a43a0e0-499f-4110-8923-441a7f5028db')
    }
    async login_as_a_guest(guest_id) {
        const api_path = `/api/user-session/guest/login-as-guest?guest_id=${guest_id}`
        await this.api_invoke.invoke_api(api_path)
        location.reload()
    }
}