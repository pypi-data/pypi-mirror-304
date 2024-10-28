import Div from '../../core/Div.mjs'

export default class Col extends Div {
    constructor({size, ...kwargs}={}) {
        kwargs.class = `col${size ? `-${size}` : ''} ${kwargs.class || ''}`
        super({...kwargs})
    }
}