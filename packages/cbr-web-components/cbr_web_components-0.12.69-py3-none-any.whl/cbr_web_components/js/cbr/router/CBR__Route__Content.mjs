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
            const section = this._map_route_to_section(route_path);
            const content = await this.content_loader.load_content(section);

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

    _map_route_to_section(route_path) {
        // Map application routes to content sections
        const route_map = {
            'home': 'home-page',
            'athena': 'athena',
            'personas': 'personas',
            'past-chats': 'past-chats',
            'pastchats': 'past-chats',
            'profile': 'profile',
            'chat': 'chat',
            'docs': 'documentation'
        };

        const section = route_map[route_path.toLowerCase()];
        if (!section) {
            throw new Error(`No content mapping for route: ${route_path}`);
        }

        return section;
    }

    set_language(language) {
        this.content_loader.set_language(language);
    }

    set_version(version) {
        this.content_loader.set_version(version);
    }
}