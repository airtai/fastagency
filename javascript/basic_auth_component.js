import {
  LitElement,
  css,
  html,
} from "https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js";

class BasicAuthComponent extends LitElement {
  static styles = css`
    :host {
      display: block;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    .auth-container {
      width: 100%;
      max-width: 400px;
      margin: 1rem auto;
      padding: 2rem;
      border-radius: 8px;
      background: white;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    form {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    .input-group {
      position: relative;
    }

    .input-group input {
      width: 96%;
      padding: 0.75rem 0 0.75rem 0.5rem;
      font-size: 1rem;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      background: #f8fafc;
      transition: all 0.2s ease;
    }

    .input-group input:focus {
      outline: none;
      border-color: #3b82f6;
      background: white;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    .input-group input::placeholder {
      color: #94a3b8;
    }

    .auth-button {
      width: 100%;
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      font-weight: 500;
      color: white;
      background: #3b82f6;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .auth-button:hover {
      background: #2563eb;
      transform: translateY(-1px);
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .auth-button:active {
      transform: translateY(0);
      box-shadow: none;
    }

    .auth-button:disabled {
      background: #94a3b8;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }

    .error {
      padding: 0.75rem 1rem;
      margin-bottom: 1rem;
      color: #dc2626;
      background: #fee2e2;
      border: 1px solid #fecaca;
      border-radius: 6px;
      font-size: 0.875rem;
    }

    /* Sign out button specific styles */
    .auth-container:has(> .auth-button) {
      padding: 0rem;
      box-shadow: none;
      background: transparent;
      margin-top:0rem;
    }

    .auth-container:has(> .auth-button) .auth-button {
      width: auto;
      max-width: 200px;
      background: #ef4444;
      border: 1px solid #dc2626;
      padding: 0.5rem 0.75rem;
      font-size: 0.75rem;
    }

    .auth-container:has(> .auth-button) .auth-button:hover {
      background: #dc2626;
    }

    /* Loading state styles */
    .auth-button.loading {
      position: relative;
      color: transparent;
    }

    .auth-button.loading::after {
      content: '';
      position: absolute;
      left: 50%;
      top: 50%;
      width: 20px;
      height: 20px;
      border: 2px solid white;
      border-radius: 50%;
      border-top-color: transparent;
      animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
      to {
        transform: translate(-50%, -50%) rotate(360deg);
      }
    }
  `;
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

      this.username = '';
      this.password = '';
      // this.error = '';
      // this.isSignedIn = true;

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

      // Refresh the browser
      window.location.reload();
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
      <h1>Sign in to your account</h1>
      <form @submit="${this.handleSubmit}">
        ${this.error ? html`<div class="error">${this.error}</div>` : ''}

        <div class="input-group">
          <input
            type="text"
            placeholder="Username"
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
          class="auth-button ${this.loading ? 'loading' : ''}"
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
