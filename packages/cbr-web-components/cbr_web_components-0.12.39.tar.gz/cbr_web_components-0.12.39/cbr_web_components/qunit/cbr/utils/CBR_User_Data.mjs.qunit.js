import CBR_User_Data  from "../../../js/cbr/utils/CBR_User_Data.mjs";
import API__Invoke from "../../../js/data/API__Invoke.mjs";


QUnit.module('CBR_User_Data', function(hooks) {

    let url__guest_users  = 'https://static.dev.aws.cyber-boardroom.com/cbr-content/latest/en/web-site/demo-users/guests-users.toml.json'

    let session_id
    let cbr_user_data;


    hooks.before(async () => {
        // todo: reimplement this when the url__guest_data doesn't take more than 1 second to fetch
        //let url__guest_data   = 'https://community.dev.aws.cyber-boardroom.com/api/user-session/guest/data?guest_id='
        //let guest_id
        //let guest_name        = 'guest-one'
        //let guest_data
        // const guest_users = await fetch(url__guest_users).then(response => response.json())
        //     const startTime = performance.now();
        //     guest_id          = guest_users[guest_name].guest_id
        //     guest_data = await fetch(url__guest_data + guest_id).then(response => response.json())
        //     guest_data
        // const endTime = performance.now(); const timeTaken = endTime - startTime;
        // console.log(`Fetch time: ${timeTaken}ms`);
        session_id = '19ac690e-c9c6-484f-a940-6a1588b47c0d'         // for now hard code this value (which will not be very stable, but should work for a while)
    })

    hooks.beforeEach(() => {
        cbr_user_data = new CBR_User_Data()
        cbr_user_data.target_server = 'https://community.dev.aws.cyber-boardroom.com'
    })

    QUnit.test('.constructor()', (assert)=> {
        assert.ok   (cbr_user_data            instanceof CBR_User_Data)
        assert.ok   (cbr_user_data.api_invoke instanceof API__Invoke  )

        assert.equal(cbr_user_data.url__api__user_profile    , '/api/user-data/user/user-profile'         )
        assert.equal(cbr_user_data.url__api__current_session , '/api/user-session/session/current-session')
    })

    //
    QUnit.test('.current_session()', async (assert)=> {
        cbr_user_data.auth_header = session_id
        let response = await cbr_user_data.current_session()
        assert.deepEqual(response, {  data: { username: 'guest_er2uf' },
                                      security: {
                                        is_admin_global: false,
                                        is_admin_site: false,
                                        is_blocked: false,
                                        is_customer: false,
                                        is_guest: false,
                                        is_malicious: false,
                                        is_user: false,
                                        is_user_qa: false,
                                        is_suspended: false,
                                        is_suspicious: false
                                      },
                                      session_id: '19ac690e-c9c6-484f-a940-6a1588b47c0d',
                                      user_name: 'guest_er2uf',
                                      user_id: '9da9279c-1fd8-4f61-8645-38cf21a69658',
                                      created__date: '2024-10-24',
                                      created__time: '17:10:01',
                                      timestamp: 1729789801637
                                    } )
        // assert.deepEqual(response, { data   : null                                             ,
        //                              error  : null                                             ,
        //                              message: 'Session did not exist',
        //                              status : 'error'} )
        //assert.ok(1)
    })
})