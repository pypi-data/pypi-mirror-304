import Icon__Mappings from './Icon__Mappings.mjs'

export default class Icon {
    constructor(options = {}) {
        this.element = document.createElement(options.element || 'span')
        this.setup(options)
    }

    setup(options) {
        // Always add base icon class
        this.element.classList.add('icon')

        // Add icon content if provided
        if (options.icon) {
            const iconContent = Icon__Mappings.getIcon(options.icon)
            this.element.textContent = iconContent
        }

        // Add any additional classes
        if (options.class) {
            const classes = options.class.split(' ')
            this.element.classList.add(...classes)
        }

        // Add any additional attributes
        if (options.attributes) {
            Object.entries(options.attributes).forEach(([key, value]) => {
                this.element.setAttribute(key, value)
            })
        }

        // Handle size
        if (options.size) {
            this.element.classList.add(`icon-${options.size}`)
        }

        // Handle color
        if (options.color) {
            this.element.classList.add(`icon-${options.color}`)
        }

        // Handle rotation
        if (options.rotate) {
            this.element.classList.add(`icon-rotate-${options.rotate}`)
        }

        // Handle animation
        if (options.spin) {
            this.element.classList.add('icon-spin')
        }

        if (options.pulse) {
            this.element.classList.add('icon-pulse')
        }

        // Handle spacing
        if (options.spacing) {
            this.element.classList.add(`icon-spacing-${options.spacing}`)
        }
    }

    html() {
        return this.element.outerHTML
    }
}