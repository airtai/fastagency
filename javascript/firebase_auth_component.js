import {
  LitElement,
  html,
} from "https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js";

import "https://www.gstatic.com/firebasejs/10.0.0/firebase-app-compat.js";
import "https://www.gstatic.com/firebasejs/10.0.0/firebase-auth-compat.js";
import "https://www.gstatic.com/firebasejs/ui/6.1.0/firebase-ui-auth.js";

// TODO: replace this with your web app's Firebase configuration
// Convert the keys from snake case to camel case and pass it to the firebaseConfig
// const firebaseConfig = {
//   apiKey: "****",
//   authDomain: "****",
//   projectId: "****",
//   storageBucket: "****",
//   messagingSenderId: "****",
//   appId: "****",
// };
const firebaseConfig = "<REPLACE_WITH_FIREBASE_CONFIG_DICT>";

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

const uiConfig = {
  // TODO: change this to your Mesop page path.
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

// Initialize the FirebaseUI Widget using Firebase.
const ui = new firebaseui.auth.AuthUI(firebase.auth());

class FirebaseAuthComponent extends LitElement {
  static properties = {
    isSignedIn: { type: Boolean },
    authChanged: { type: String },
  };

  constructor() {
    super();
    this.isSignedIn = false;
  }

  createRenderRoot() {
    // Render in light DOM so firebase-ui-auth works.
    return this;
  }

  firstUpdated() {
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

    ui.start("#firebaseui-auth-container", uiConfig);
  }

  signOut() {
    firebase.auth().signOut();
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
          <span class="firebaseui-idp-text firebaseui-idp-text-long"
            >Sign out</span
          >
        </button>
      </div>
    `;
  }
}

customElements.define("firebase-auth-component", FirebaseAuthComponent);
