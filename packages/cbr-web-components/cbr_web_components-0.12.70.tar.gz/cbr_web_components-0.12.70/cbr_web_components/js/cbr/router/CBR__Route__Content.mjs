import CBR__Content__Loader from './CBR__Content__Loader.mjs';
import CBR__Error__Boundary from './CBR__Error__Boundary.mjs';

export default class CBR__Route__Content {
    constructor(config = {}) {
        this.content_loader = new CBR__Content__Loader(config);
        this.error_boundary = new CBR__Error__Boundary();
    }

    async load_content(route_path) {
        const content_div = document.createElement('div');
        content_div.className = 'route-content';

        try {
            // Map routes to content sections
            const page    = this.map_route_to_page(route_path);
            const content = await this.content_loader.load_content(page);

            if (content && content.html) {
                content_div.innerHTML = content.html;
            } else {
                throw new Error('Invalid content format received');
            }
        } catch (error) {
            console.error('Route content error:', error);
            return this.error_boundary.render_error(error);
        }

        return content_div;
    }

    map_route_to_page(route_path) {     // in case we need to map routes to content sections
        return route_path;
    }

    set_language(language) {
        this.content_loader.set_language(language);
    }

    set_version(version) {
        this.content_loader.set_version(version);
    }
}