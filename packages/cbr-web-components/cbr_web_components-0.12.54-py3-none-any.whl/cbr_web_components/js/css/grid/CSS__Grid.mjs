export default class CSS__Grid {
    constructor(target_element) {
        this.target_element = target_element
    }

    apply_framework() {
        if (this.target_element) {
            this.target_element.add_css_rules(this.css_rules__standard())
        }
    }

    css_rules__standard() {
        return {
            // Breakpoint definitions as CSS custom properties for reuse
            ":host": {
                "--breakpoint-xs": "0",
                "--breakpoint-sm": "576px",
                "--breakpoint-md": "768px",
                "--breakpoint-lg": "992px",
                "--breakpoint-xl": "1200px",
                "--breakpoint-xxl": "1400px",
                "--grid-gutter": "1.5rem",
                "--grid-columns": "12"
            },

            // Container
            ".container": {
                width: "100%",
                marginLeft: "auto",
                marginRight: "auto",
                paddingLeft: "calc(var(--grid-gutter) / 2)",
                paddingRight: "calc(var(--grid-gutter) / 2)",
                boxSizing: "border-box",

                "@media (min-width: 576px)": {
                    maxWidth: "540px"
                },
                "@media (min-width: 768px)": {
                    maxWidth: "720px"
                },
                "@media (min-width: 992px)": {
                    maxWidth: "960px"
                },
                "@media (min-width: 1200px)": {
                    maxWidth: "1140px"
                },
                "@media (min-width: 1400px)": {
                    maxWidth: "1320px"
                }
            },

            ".container-fluid": {
                width: "100%",
                marginLeft: "auto",
                marginRight: "auto",
                paddingLeft: "calc(var(--grid-gutter) / 2)",
                paddingRight: "calc(var(--grid-gutter) / 2)",
                boxSizing: "border-box"
            },

            // Row
            ".row": {
                display: "flex",
                flexWrap: "wrap",
                marginLeft: "calc(var(--grid-gutter) / -2)",
                marginRight: "calc(var(--grid-gutter) / -2)",
                boxSizing: "border-box"
            },

            // Basic columns
            ".col": {
                position: "relative",
                width: "100%",
                paddingRight: "calc(var(--grid-gutter) / 2)",
                paddingLeft: "calc(var(--grid-gutter) / 2)",
                flexGrow: "1",
                flexShrink: "0",
                maxWidth: "100%",
                boxSizing: "border-box"
            },

            // Generate column widths
            ...[...Array(12)].reduce((acc, _, i) => ({
                ...acc,
                [`.col-${i + 1}`]: {
                    position: "relative",
                    paddingRight: "calc(var(--grid-gutter) / 2)",
                    paddingLeft: "calc(var(--grid-gutter) / 2)",
                    flex: "0 0 auto",
                    width: `${(i + 1) * 100 / 12}%`,
                    boxSizing: "border-box"
                }
            }), {}),

            // Responsive columns for each breakpoint
            ...[
                ['sm', '576px'],
                ['md', '768px'],
                ['lg', '992px'],
                ['xl', '1200px'],
                ['xxl', '1400px']
            ].reduce((acc, [breakpoint, width]) => ({
                ...acc,
                [`@media (min-width: ${width})`]: {
                    ...[...Array(12)].reduce((cols, _, i) => ({
                        ...cols,
                        [`.col-${breakpoint}-${i + 1}`]: {
                            flex: "0 0 auto",
                            width: `${(i + 1) * 100 / 12}%`
                        }
                    }), {})
                }
            }), {}),

            // Gap utilities
            ...[0, 1, 2, 3, 4, 5].reduce((acc, i) => ({
                ...acc,
                [`.gap-${i}`]: {
                    gap: `${i * 0.25}rem`
                },
                [`.gap-x-${i}`]: {
                    columnGap: `${i * 0.25}rem`
                },
                [`.gap-y-${i}`]: {
                    rowGap: `${i * 0.25}rem`
                }
            }), {}),

            // Alignment utilities
            ".justify-start": { justifyContent: "flex-start" },
            ".justify-center": { justifyContent: "center" },
            ".justify-end": { justifyContent: "flex-end" },
            ".justify-between": { justifyContent: "space-between" },
            ".justify-around": { justifyContent: "space-around" },

            ".align-start": { alignItems: "flex-start" },
            ".align-center": { alignItems: "center" },
            ".align-end": { alignItems: "flex-end" },
            ".align-stretch": { alignItems: "stretch" },

            // Order utilities
            ...[0, 1, 2, 3, 4, 5].reduce((acc, i) => ({
                ...acc,
                [`.order-${i}`]: {
                    order: i
                }
            }), {}),

            // Offset utilities
            ...[...Array(11)].reduce((acc, _, i) => ({
                ...acc,
                [`.offset-${i + 1}`]: {
                    marginLeft: `${(i + 1) * 100 / 12}%`
                }
            }), {}),

            // Display utilities
            ".d-none": { display: "none" },
            ".d-flex": { display: "flex" },
            ".d-block": { display: "block" },

            // Responsive display utilities
            ...[
                ['sm', '576px'],
                ['md', '768px'],
                ['lg', '992px'],
                ['xl', '1200px'],
                ['xxl', '1400px']
            ].reduce((acc, [breakpoint, width]) => ({
                ...acc,
                [`@media (min-width: ${width})`]: {
                    [`.d-${breakpoint}-none`]: { display: "none" },
                    [`.d-${breakpoint}-flex`]: { display: "flex" },
                    [`.d-${breakpoint}-block`]: { display: "block" }
                }
            }), {})
        }
    }
}