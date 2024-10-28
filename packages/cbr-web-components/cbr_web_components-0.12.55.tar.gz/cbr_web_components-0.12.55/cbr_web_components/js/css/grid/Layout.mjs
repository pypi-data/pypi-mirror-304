import Div from '../../core/Div.mjs'

export default class Layout extends Div {
        constructor({...kwargs}={}) {
        kwargs.class = `layout ${kwargs.class || ''}`
        super({...kwargs})
    }
}