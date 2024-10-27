import Div from '../../core/Div.mjs'
import Col from './Col.mjs'

export default class Row extends Div {
    constructor({...kwargs}={}) {
        kwargs.class = `row ${kwargs.class || ''}`
        super({...kwargs})
    }

    add_col({size, ...kwargs}={}) {
        kwargs.class = `col${size ? `-${size}` : ''} ${kwargs.class || ''}`
        const col = new Col({...kwargs})
        this.add_element(col)
        return col
    }
}