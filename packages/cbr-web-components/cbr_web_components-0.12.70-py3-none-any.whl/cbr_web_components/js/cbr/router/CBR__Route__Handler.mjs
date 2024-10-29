export default class CBR__Route__Handler {
    constructor(component) {
        this.component = component
        this.setupEventListeners()
    }

    setupEventListeners() {
        // Listen for popstate events (browser back/forward)
        window.addEventListener('popstate', (event) => {
            this.handleRoute(window.location.pathname)
        })

        // Intercept navigation clicks
        document.addEventListener('click', (event) => {
            const path = event.composedPath();
            const link = path.find(el => el.tagName === 'A');

            if (link && link.href.startsWith(window.location.origin)) {
                event.preventDefault()
                const path = link.href.replace(window.location.origin, '')
                this.navigate(path)
            }
        })
    }

    navigate(path) {
        window.history.pushState({}, '', path)
        this.handleRoute(path)
    }

    async handleRoute(path) {
        const contentEl = this.component.shadowRoot.querySelector('#content')
        if (!contentEl) return

        const placeholder = contentEl.querySelector('.placeholder-container')
        if (!placeholder) return

        const basePath = '/webc/cbr-webc-dev'                                       // Extract the relevant part of the path after cbr-webc
        const routePath = path.replace(basePath, '').replace(/^\/+/, '') || 'home'

        // Show loading state
        placeholder.innerHTML = '<div class="content-loader">Loading...</div>'

        try {
            const content = await this.component.routeContent.load_content(routePath)
            placeholder.innerHTML = ''
            placeholder.appendChild(content)
        } catch (error) {
            console.error('Error loading content:', error)
            placeholder.innerHTML = '<div class="content-error">Error loading content. Please try again.</div>'
        }
    }
}