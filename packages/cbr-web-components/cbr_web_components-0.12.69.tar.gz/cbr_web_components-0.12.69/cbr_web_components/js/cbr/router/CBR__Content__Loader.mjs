export default class CBR__Content__Loader {
    constructor(config = {}) {
        this.dev_mode = config.dev_mode !== undefined ?  config.dev_mode :
                                                         (window.location.protocol === 'http:');
        this.base_url     = config.base_url     || 'https://static.dev.aws.cyber-boardroom.com';
        this.version      = config.version      || 'latest';
        this.language     = config.language     || 'en';
        this.content_type = config.content_type || 'web-site';
    }

    async load_content(section, page = 'layout') {
        try {
            const url = this.dev_mode ?
                this._build_dev_url(section, page) :
                this._build_prod_url(section, page);

            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Failed to load content: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Content loading error:', error);
            throw new Error(`Failed to load content for section: ${section}`);
        }
    }

    _build_prod_url(section, page) {
        return `${this.base_url}/cbr-content/${this.version}/${this.language}/${this.content_type}/${section}/${page}.md.json`;
    }

    _build_dev_url(section, page) {
        return `/markdown/render/markdown-file-to-html-and-metadata?path=${this.language}/${this.content_type}/${section}/${page}.md`;
    }

    set_language(language) {
        this.language = language;
    }

    set_version(version) {
        this.version = version;
    }
}