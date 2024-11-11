import {
  LitElement,
  html,
} from "https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js";

class BasicAuthComponent extends LitElement {
  static properties = {
    isSignedIn: { type: Boolean },
    authChanged: { type: String },
    error: { type: String },
    username: { type: String },
    password: { type: String },
    authenticatedUser: { type: String }
  };

  constructor() {
    super();
    this.isSignedIn = false;
    this.error = '';
    this.username = '';
    this.password = '';
  }

  firstUpdated() {
    // Initialize form state
    const form = this.shadowRoot.querySelector('form');
    if (form) {
      form.reset();
    }

    if (this.authenticatedUser === "" || this.authenticatedUser === null) {
      // Initial auth state notification
      this.dispatchEvent(new MesopEvent(this.authChanged, null));
    } else {
      this.isSignedIn = true;
      this.username = this.authenticatedUser;
    }
  }

  async handleSubmit(e) {
    e.preventDefault();

    if (!this.username || !this.password) {
      this.error = 'Please fill in all fields';
      return;
    }

    try {
      const credentials = {
        username: this.username,
        password: this.password
      };

      // Dispatch auth event with credentials using MesopEvent
      this.dispatchEvent(new MesopEvent(this.authChanged, credentials));

      // Clear form
      this.username = '';
      this.password = '';
      this.error = '';
      this.isSignedIn = true;


    } catch (error) {
      this.error = error.message || 'Authentication failed';
      console.error("Auth error:", error);
    }
  }

  handleUsernameChange(e) {
    this.username = e.target.value;
    this.error = '';
  }

  handlePasswordChange(e) {
    this.password = e.target.value;
    this.error = '';
  }

  signOut() {
    try {
      // this.isSignedIn = false;
      this.username = '';
      this.password = '';

      // Notify about sign out using MesopEvent
      this.dispatchEvent(new MesopEvent(this.authChanged, null));

      // Reset form
      const form = this.shadowRoot.querySelector('form');
      if (form) {
        form.reset();
      }
    } catch (error) {
      console.error("Sign out error:", error);
    }
  }

  render() {
    // Use conditional rendering without style display properties
    return html`
          <div
            class="auth-container"
            style="${this.isSignedIn ? "" : "display: none"}"
          >
            <button
              style="background-color:#ffffff"
              class="auth-button"
              @click="${this.signOut}"
            >
              <span class="button-text">Sign out</span>
            </button>
          </div>
          <div
            class="auth-container"
            style="${this.isSignedIn ? "display: none" : ""}"
          >
            <form @submit="${this.handleSubmit}">
              ${this.error ? html`<div class="error">${this.error}</div>` : ''}

              <div class="input-group">
                <input
                  type="email"
                  placeholder="Email"
                  .value="${this.username}"
                  @input="${this.handleUsernameChange}"
                  required
                />
              </div>

              <div class="input-group">
                <input
                  type="password"
                  placeholder="Password"
                  .value="${this.password}"
                  @input="${this.handlePasswordChange}"
                  required
                />
              </div>

              <button
                type="submit"
                class="auth-button"
                ?disabled="${!this.username || !this.password}"
              >
                <span class="button-text">Sign in</span>
              </button>
            </form>
          </div>
        `;
  }
}

customElements.define("basic-auth-component", BasicAuthComponent);
