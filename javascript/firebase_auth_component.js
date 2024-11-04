import {
  LitElement,
  html,
} from "https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js";

import "https://www.gstatic.com/firebasejs/10.0.0/firebase-app-compat.js";
import "https://www.gstatic.com/firebasejs/10.0.0/firebase-auth-compat.js";
import "https://www.gstatic.com/firebasejs/ui/6.1.0/firebase-ui-auth.js";

const uiConfig = {
  signInSuccessUrl: "/",
  signInFlow: "popup",
  signInOptions: [firebase.auth.GoogleAuthProvider.PROVIDER_ID],
  // tosUrl and privacyPolicyUrl accept either url string or a callback
  // function.
  // Terms of service url/callback.
  //   tosUrl: "<your-tos-url>",
  // Privacy policy url/callback.
  //   privacyPolicyUrl: () => {
  //     window.location.assign("<your-privacy-policy-url>");
  //   },
};

let firebaseUI = null;

class FirebaseAuthComponent extends LitElement {
  static properties = {
    isSignedIn: { type: Boolean },
    authChanged: { type: String },
    apiKey: { type: String },
    authDomain: { type: String },
    projectId: { type: String },
    storageBucket: { type: String },
    messagingSenderId: { type: String },
    appId: { type: String },
  };

  constructor() {
    super();
    this.isSignedIn = false;
  }

  createRenderRoot() {
    // Render in light DOM so firebase-ui-auth works.
    return this;
  }

  _initializeFirebase() {
    const firebaseConfig = {
      apiKey: this.apiKey,
      authDomain: this.authDomain,
      projectId: this.projectId,
      storageBucket: this.storageBucket,
      messagingSenderId: this.messagingSenderId,
      appId: this.appId,
    };

    // Check if Firebase is already initialized
    try {
      firebase.app();
    } catch {
      firebase.initializeApp(firebaseConfig);
    }
  }

  _initFirebaseUI() {
    if (!firebaseUI) {
      firebaseUI = new firebaseui.auth.AuthUI(firebase.auth());
    }
    firebaseUI.start("#firebaseui-auth-container", uiConfig);
  }

  firstUpdated() {
    this._initializeFirebase();

    firebase.auth().onAuthStateChanged(
      async (user) => {
        if (user) {
          this.isSignedIn = true;
          const token = await user.getIdToken();
          this.dispatchEvent(new MesopEvent(this.authChanged, token));
        } else {
          this.isSignedIn = false;
          this.dispatchEvent(new MesopEvent(this.authChanged, ""));
        }
      },
      (error) => {
        console.log(error);
      }
    );

    this._initFirebaseUI();
  }

  signOut() {
    try {
      firebase.auth().signOut();
    } catch (error) {
      console.error("Sign out error:", error);
    }
  }

  render() {
    return html`
      <div
        id="firebaseui-auth-container"
        style="${this.isSignedIn ? "display: none" : ""}"
      ></div>
      <div
        class="firebaseui-container firebaseui-page-provider-sign-in firebaseui-id-page-provider-sign-in firebaseui-use-spinner"
        style="${this.isSignedIn ? "" : "display: none"}"
      >
        <button
          style="background-color:#ffffff"
          class="firebaseui-idp-button mdl-button mdl-js-button mdl-button--raised firebaseui-idp-google firebaseui-id-idp-button"
          @click="${this.signOut}"
        >
          <span
            style="padding-left:0px"
            class="firebaseui-idp-text firebaseui-idp-text-long"
            >Sign out</span
          >
        </button>
      </div>
    `;
  }
}

customElements.define("firebase-auth-component", FirebaseAuthComponent);
