export default class CBR__Route__Content {
    constructor() {
        // Could add configuration or dependencies here if needed
    }

    async loadContent(routePath) {
        const contentDiv = document.createElement('div')
        contentDiv.className = 'route-content'

        switch(routePath.toLowerCase()) {
            case 'home':
                const url = 'https://static.dev.aws.cyber-boardroom.com/cbr-content/latest/en/web-site/home-page/layout.md.json'
                console.log('Loading home page content...', url)
                const response = await fetch(url).then(response => response.json())
                const html_content = response.html
                contentDiv.innerHTML = html_content
                break
            case 'athena':
                contentDiv.innerHTML = '<h1>Athena Interface</h1>'
                break
            case 'personas':
                contentDiv.innerHTML = '<h1>Personas Management</h1>'
                break
            case 'past-chats':
            case 'pastchats':
                contentDiv.innerHTML = '<h1>Past Conversations</h1>'
                break
            case 'profile':
                contentDiv.innerHTML = '<h1>User Profile...</h1>'
                break
            case 'chat':
                contentDiv.innerHTML = '<h1>Chat with LLMs</h1>'
                break
            case 'docs':
                contentDiv.innerHTML = '<h1>Documentation</h1>'
                break
            default:
                contentDiv.innerHTML = `<h1>Content for path: ${routePath}</h1>`
        }
        return contentDiv
    }
}