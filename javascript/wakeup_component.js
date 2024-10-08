import {
    LitElement,
    html,
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class WakeupComponent extends LitElement {
    static properties = {
        wakeupEvent: { type: String },
    };

    constructor() {
        super();
        this.wakeupEvent = '';
    }

    render() {
        return html`<span />`;
    }

    connectedCallback() {
        setTimeout(
            () => {
                this.dispatchEvent(
                    new MesopEvent(this.wakeupEvent, {
                    }),
                );
            },
            100
        );
    }
}

customElements.define('wakeup-component', WakeupComponent);
