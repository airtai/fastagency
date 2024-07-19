import { DISCORD_URL } from '../../shared/constants';

function deepFreeze(object: any) {
  // Retrieve the property names defined on object
  var propNames = Object.getOwnPropertyNames(object);

  // Freeze properties before freezing self
  for (let name of propNames) {
    let value = object[name];

    object[name] = value && typeof value === 'object' ? deepFreeze(value) : value;
  }

  return Object.freeze(object);
}

export const SECRETS_TO_MASK = ['api_key', 'gh_token', 'fly_token'];

export const DEPLOYMENT_INSTRUCTIONS = `<div class="leading-loose ml-2 mr-2"><span class="text-l inline-block my-2 underline">GitHub Repository Created</span>
<span class="ml-5">- We have created a new <a class="underline" href="<gh_repo_url>" target="_blank" rel="noopener noreferrer">GitHub repository</a> in your GitHub account.</span>
<span class="ml-5">- The application code will be pushed to this repository in a few seconds.</span>
<span class="text-l inline-block my-2 underline">Checking Deployment Status</span>
<span class="ml-5">- Once the application code is pushed, new workflows will be triggered to test and deploy the application</span>
<span class="ml-10">to Fly.io. You can check the status of the same on the GitHub repository's <a class="underline" href="<gh_repo_url>/actions" target="_blank" rel="noopener noreferrer">actions</a> page.</span>
<span class="text-l inline-block my-2 underline">Next Steps</span>
<span class="ml-5">- Wait for the workflows to complete:
<span class="ml-13">- Workflow to run tests and verify the build (approx. 2 mins).</span>
<span class="ml-13">- Workflow to deploy the application to Fly.io (approx. 8 - 10 mins).</span>
<span class="ml-5">- Adding the fly.io configuration files:</span>
<span class="ml-10">- The above workflow might have also created a pull request in your GitHub repository</span>
<span class="ml-13">to update the <b>fly.toml</b> configuration files.</span>
<span class="ml-10">- Go to the <b>Pull requests</b> tab in your repository and merge the PR named "Add Fly.io configuration files".</span>
<span class="ml-13">You will be needing this to deploy your application to Fly.io in the future.</span></span>
<span class="text-l inline-block my-2 underline">Access the application:</span>
<span class="ml-10">- Once the "Fly Deployment Pipeline" completes. The application URL will be automatically added to the repository's description.</span>
<span class="ml-10">- Detailed steps to access the application can be found in the README.md file of the repository.</span>
<span class="text-l inline-block my-2 underline">Need Help?</span>
<span class="ml-10">- If you encounter any issues or need assistance, please reach out to us on <a class="underline" href=${DISCORD_URL} target="_blank" rel="noopener noreferrer">discord</a>.</span>
</div>
`;

export const DEPLOYMENT_PREREQUISITES = `<div class="ml-2 mr-2 leading-loose">We've automated the application generation and deployment process so you can focus on building your application
without worrying about deployment complexities.

The deployment process includes:
<span class="ml-5">- Automatically creating a new GitHub repository with the generated application code in your GitHub account.</span>
<span class="ml-5">- Automatically deploying the application to Fly.io using GitHub Actions.</span>
<span class="text-xl inline-block my-2 underline">Prerequisites: </span>
Before you begin, ensure you have the following:
<span class="ml-5">1. GitHub account:</span>
<span class="ml-10">- If you don't have a GitHub account, you can create one <a class="underline" href="https://github.com/signup" target="_blank" rel="noopener noreferrer">here</a>.</span>
<span class="ml-10">- A GitHub personal access token. If you don't have one, you can generate it by following this <a class="underline" href="https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic" target="_blank" rel="noopener noreferrer">guide</a>.</span>
<span class="ml-10"><b><u>Note</u></b>: The minimum required scopes for the token are: <b>repo</b>, <b>workflow</b>, <b>read:org</b>, <b>gist</b> and <b>user:email</b>.</span>

<span class="ml-5">2. Fly.io account:</span>
<span class="ml-10">- If you don't have a Fly.io account, you can create one <a class="underline" href="https://fly.io/app/sign-up" target="_blank" rel="noopener noreferrer">here</a>. Fly provides free allowances for up to 3 VMs, so deploying a Wasp app </b></u></span>
<span class="ml-12">to a new account is free <u><b>but all plans require you to add your credit card information</b></u></span>
<span class="ml-10">- A Fly.io API token. If you don't have one, you can generate it by following the steps below.</span>
<span class="ml-15">- Go to your <a class="underline" href="https://fly.io/dashboard" target="_blank" rel="noopener noreferrer">Fly.io</a> dashboard and click on the <b>Tokens</b> tab (the one on the left sidebar).</span>
<span class="ml-15">- Enter a name and set the <b>Optional Expiration</b> to 999999h, then click on <b>Create Organization Token</b> to generate a token.</span>
<span class="ml-10"><b><u>Note</u></b>: If you already have a Fly.io account and created more than one organization, make sure you choose "Personal" as the organization </span>
<span class="ml-10"> while creating the Fly.io API Token in the deployment steps below.</span>
</div>
`;
