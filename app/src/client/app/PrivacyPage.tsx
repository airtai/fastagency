export default function PrivacyPage() {
  return (
    <div>
      <div className='mx-auto max-w-2xl pl-10 pr-10 text-airt-font-base pt-10 pb-24 sm:pb-32 lg:gap-x-8 lg:py-5 lg:px-8'>
        <div className='container mx-auto py-8'>
          <h1 className='text-3xl font-semibold mb-4'>Privacy Policy</h1>
          <p className='text-airt-font-base mb-4'>Last updated January 29, 2024</p>

          <section className='mb-8'>
            <p>
              Airt technologies, Inc. ("we", "us", or "our") is committed to protecting the privacy of our users. This
              Privacy Policy explains how we collect, use, and disclose information through our SaaS tool,{' '}
              <b>FastAgency</b> (the "Service").
            </p>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Information We Collect</h2>
            <p>
              At FastAgency, we value your privacy and are committed to ensuring the highest level of confidentiality
              and security for your information. Here's what you need to know about the information we collect when you
              use our Service:
            </p>
            <br />
            <ul className='list-decimal pl-6'>
              <li>
                <b>Account Information:</b> When you create a FastAgency account, we collect your name and email
                address. This information is essential to personalize your experience and enable various features of the
                Service.
              </li>
              <li>
                <b>Integrations:</b> As you integrate your various marketing platforms with our Service, we collect
                information that you input, including the details about the platforms you're connecting and any
                associated data. This data is necessary to provide you with accurate analytics, reports, and insights.
                For data collected from Google APIs, we adhere to Google's API Services User Data Policy, including the
                Limited Use requirements. Continue reading for further information.
              </li>
              <li>
                <b>Chat Interactions and AI Data Sharing:</b> Your chat interactions and data from connected third-party
                services may be shared with our privately deployed OpenAI models hosted on Microsoft Azure. This sharing
                is essential for the service and is detailed in the section below: "Third-Party and Proprietary AI
                Tools."
              </li>
              <li>
                <b>Usage Information:</b> To help us understand how you interact with our Service and enable us to
                improve your user experience, we collect information about your usage. This may include log data, device
                information, and other data related to your activities within our Service.
              </li>
              <li>
                <b>Data Processing:</b> At FastAgency, your data's privacy is a top priority. We process data on-the-fly
                and do not store any data in databases, except for chat history as detailed in the "Third-Party and
                Proprietary AI Tools" section. This ensures your data stays where it belongs—with you.
              </li>
            </ul>
          </section>

          <section className='mb-8'>
            <p>We use the information we collect to:</p>
            <br />
            <ul className='list-disc pl-6'>
              <li>
                <b>Provide, Maintain, and Improve the Service:</b> We use your information to deliver the services you
                request, maintain your account, and enhance your experience with FastAgency.
              </li>
              <li>
                <b>Respond to Your Requests and Inquiries:</b> Your information helps us respond to your customer
                service requests, support needs, and other inquiries.
              </li>
              <li>
                <b>Communicate with You:</b> We use your information to communicate with you about the Service, updates,
                and other informational or promotional content.
              </li>
              <li>
                <b>Analyze and Monitor Usage:</b> We use analytics tools to track how users interact with the Service,
                which helps us make data-driven decisions for improvements.
              </li>
              <li>
                <b>Detect, Investigate, and Prevent Fraud and Other Illegal Activities:</b> We use your information to
                protect the security and integrity of the Service by detecting and preventing fraudulent or illegal
                activities.
              </li>
            </ul>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Authentication And Authorized Data Access</h2>
            <p>
              User authenticates with the 3rd party provider such as Google account. Upon authentication, user allows
              the application:
            </p>
            <br />
            <ul className='list-decimal pl-6'>
              <li>Associate user with personal info on Google</li>
              <li>See user's personal info, including any personal info user made publicly available</li>
              <li>View user's email address</li>
            </ul>
            <br />
            <p>
              Email address is stored in the database of the application while the other credentials of authenticated
              users are encrypted and stored within the infrastructure of Google. This can be used to restrict or fully
              block the service for a particular user in case of the breach of the <b>terms of use</b>. User's email
              address can be deleted upon the request.
            </p>
            <br />
            <h3 className='text-l font-semibold mb-2'>Revoke Access to Your Google Account</h3>

            <p>
              To remove access of the application to your account, you can do it directly in your Google account by
              following this link:{' '}
              <a
                // href="https://myaccount.google.com/permissions‍"
                href='https://myaccount.google.com/connections'
                target='_black'
                className='no-underline hover:underline text-airt-primary'
              >
                https://myaccount.google.com/permissions‍
              </a>
            </p>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Google API Services User Data Policy</h2>
            <h3 className='text-l font-semibold mb-2'>Google API Services Disclosure</h3>
            <p>
              FastAgency's use and transfer of information received from Google APIs adhere to{' '}
              <a
                href='https://developers.google.com/terms/api-services-user-data-policy'
                target='_blank'
                className='no-underline hover:underline text-airt-primary'
              >
                Google API Services User Data Policy
              </a>
              , including the Limited Use requirements. We recommend reviewing Google API Services User Data Policy to
              better understand their practices.
            </p>
            <br />
            <h3 className='text-l font-semibold mb-2'>Use of Google API Services Data</h3>
            <p>
              When you choose to connect various Google services to FastAgency, we require specific permissions to fetch
              and display data for your interactive queries. Below are the permissions required for each Google service:
            </p>
            <br />
            <ul className='list-disc pl-6'>
              <li>
                Google Analytics:{' '}
                <a
                  href='https://developers.google.com/analytics/devguides/config/admin/v1'
                  target='_blank'
                  className='no-underline hover:underline text-airt-primary'
                >
                  https://developers.google.com/analytics/devguides/config/admin/v1
                </a>{' '}
                - Enables you to interact with your Google Analytics data through FastAgency.
              </li>

              {/* <li>
                Google Ad:{' '}
                <a
                  href='https://developers.google.com/google-ads/api/docs/oauth/internals'
                  target='_blank'
                  className='no-underline hover:underline text-airt-primary'
                >
                  https://developers.google.com/google-ads/api/docs/oauth/internals
                </a>{' '}
                - Allows FastAgency to fetch and display your Google Ads data for interactive queries.
              </li> */}
              <li>
                Google Search Console:{' '}
                <a
                  href='https://developers.google.com/webmaster-tools/v1/sites/get'
                  target='_blank'
                  className='no-underline hover:underline text-airt-primary'
                >
                  https://developers.google.com/webmaster-tools/v1/sites/get
                </a>{' '}
                - Permits FastAgency to access and display your Google Search Console data, making it available for
                interactive chat.
              </li>
            </ul>
            <br />
            <p>You may choose to connect one, multiple, or none of these services as per your preference.</p>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Third-Party and Proprietary AI Tools</h2>
            <p>
              Our chatbot service utilizes advanced AI technology by employing privately deployed OpenAI models on
              Microsoft Azure. This approach allows us to generate contextually relevant and accurate responses based on
              your interactions and queries, ensuring a high-quality user experience.
            </p>
            <br />
            <h3 className='text-l font-semibold mb-2'>Data Sharing in Different Use Cases</h3>
            <p>
              Your chat interactions are processed using our privately deployed OpenAI models on Microsoft Azure. This
              ensures that your data, including chat history, user metrics, and dimensions from integrated services like
              Google Analytics, Google Ads, and Facebook Ads, is not shared with OpenAI directly.
            </p>
            <br />
            <p>Here's a breakdown of the specific data shared from each source:</p>
            <br />
            <p>
              <b>Google Analytics:</b> Your Google Analytics data includes website traffic information, user behavior,
              and engagement metrics from your connected websites. Metrics like page views, session duration, bounce
              rate, and user demographics. By incorporating these insights, the chatbot can tailor its responses to
              align with the user's website-related inquiries.
            </p>
            {/* <br /> */}
            {/* <p>
              <b>Google Ads:</b> Data from your Google Ads campaigns offers insights into your advertising efforts, ad
              performance, and user interactions with your advertisements. Key metrics such as ad clicks, impressions,
              click-through rates (CTR), and conversion rates are integrated into the chatbot's learning process. This
              integration enables the chatbot to provide more informed and relevant responses regarding your advertising
              strategies.
            </p> */}
            <br />
            <p>
              <b>Google Search Console:</b> Information gathered from Google Search Console sheds light on your
              website's visibility in Google search results. Details about search queries, click-through rates (CTR),
              and average position help the chatbot understand user intent and prevalent search trends. By leveraging
              this data, the chatbot can offer insights and answers that align with current search behaviors.
            </p>
            <br />
            <p>
              <b>Chat Interactions:</b> This refers to the text-based interactions you have with the chatbot within the
              FastAgency platform. The content of these conversations, including your questions and responses. This data
              aids in refining the AI's ability to comprehend inputs and generate contextually accurate responses.
            </p>
            <br />
            <p>
              All of the data sources mentioned above are crucial for enhancing the chatbot's ability to provide
              accurate and contextually relevant responses. When chatting directly on our website, certain data points
              from your interactions and connected platforms are processed using our privately deployed OpenAI models on
              Microsoft Azure. We ensure that only relevant and necessary data are shared to maintain the effectiveness
              of the chatbot's functionality.
            </p>
          </section>

          <section className='mb-8'>
            <h3 className='text-l font-semibold mb-2'>Data Storage on Azure Database</h3>
            <p>
              While we do not directly store raw data from third-party sources such as Google Ads, Google Analytics, or
              Facebook Ads, it's crucial to understand that your chat history may contain references to or summaries of
              data from these services. Retaining this chat history is not just for record-keeping; it's a fundamental
              component for the seamless functionality of our chatbot service. This chat data is securely stored in
              Azure Database service, a cloud-based database, in compliance with Azure privacy policy (
              <a
                href='https://learn.microsoft.com/en-us/azure/compliance/'
                target='_blank'
                className='no-underline hover:underline text-airt-primary'
              >
                https://learn.microsoft.com/en-us/azure/compliance/
              </a>
              ). Your chat history is retained indefinitely, but you have the option to delete it at any time through
              the settings in our application.
            </p>
          </section>

          <section className='mb-8'>
            <h3 className='text-l font-semibold mb-2'>User Consent Process</h3>
            <p>
              During your registration with FastAgency, we require your explicit consent regarding our privacy
              practices. As part of the sign-up process, you will encounter a checkbox indicating that you have read and
              agree to our Terms and Conditions and Privacy Policy. By checking this box, you acknowledge your
              understanding and agreement to how we handle your data as detailed in these documents. Only upon agreeing
              to these terms will the chatbot service proceed with using your data. You have the option to withdraw your
              consent at any point, read more below.
            </p>
          </section>

          <section className='mb-8'>
            <h3 className='text-l font-semibold mb-2'>Opt-Out Options</h3>
            <p>
              If you choose to withdraw your consent and opt-out of data sharing with third-party tools, you will no
              longer be able to use the FastAgency service. The nature of our tool requires data sharing for its basic
              functionality. Therefore, opting out effectively means discontinuing use of the service.
            </p>
          </section>

          <section className='mb-8'>
            <h3 className='text-l font-semibold mb-2'>Agreement</h3>
            <p>
              By using our chatbot service, you explicitly consent to your chat data being processed as described above.
              We ensure that your data is handled securely and in accordance with this privacy policy, as well as Azure
              privacy policy.
            </p>
            <br />
            <p>
              <b>If you do not agree with this policy, please refrain from signing up and using FastAgency.</b>
            </p>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Google Analytics</h2>
            <p>
              Google Analytics is used across fastagency.ai domain in order to collect information about the users'
              interactions with the site as well as to identify returning visits, location, device data and engagement
              signals. Collected data helps to understand the relevancy and general usage of the tool hence, to provide
              better experience and solutions towards the needs of the users, fix errors and bugs. No data is shared
              with the 3rd party organizations or individuals.
            </p>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Information Sharing and Disclosure</h2>
            <p>We may share your information with third parties in the following circumstances:</p>
            <br />
            <ul className='list-disc pl-6'>
              <li>
                Service Providers: We may share your information with third-party service providers who perform services
                on our behalf, such as hosting, analytics, and customer support.
              </li>
              <li>
                AI Data Sharing: Your chat interactions and data from connected third-party services may be shared with
                our in-house AI algorithms. This sharing is essential for the service and is detailed in the section
                above "Third-Party and Proprietary AI Tools".
              </li>
              <li>
                Compliance with Laws: We may disclose your information as required by law or in response to legal
                process, including subpoenas, court orders, and requests from law enforcement.
              </li>
              <li>
                Business Transfers: If we are involved in a merger, acquisition, or sale of all or a portion of our
                assets, your information may be transferred as part of that transaction.
              </li>
              <li>Your Consent: We may disclose your information with your consent.</li>
            </ul>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Your Choices</h2>
            <p>
              You can access and update your account information through the Service. You can also unsubscribe from our
              promotional emails by following the instructions in the email.
            </p>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Data Retention</h2>
            <p>
              We retain the information we collect for as long as necessary to provide the Service and fulfill the
              purposes described in this Privacy Policy. When we no longer need the information, we will securely delete
              it or de-identify it. Your chat history is retained indefinitely, but you have the option to delete it at
              any time through the settings in our application.
            </p>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Security</h2>
            <p>
              We take reasonable measures to protect your information from unauthorized access, use, disclosure, and
              destruction. However, no method of transmission over the internet or method of electronic storage is
              completely secure.
            </p>
          </section>

          <section className='mb-8'>
            <h2 className='text-xl font-semibold mb-2'>Changes to this Privacy Policy</h2>
            <p>
              We may update this Privacy Policy from time to time. If we make any material changes, we will notify you
              by email or by posting a notice on our website prior to the change becoming effective.
            </p>
          </section>

          <section>
            <h2 className='text-xl font-semibold mb-2'>Contact Us</h2>
            <p className='mb-4'>
              In order to receive further information regarding use of the Site, please contact us at:{' '}
              <a href='mailto:support@fastagency.ai' className='no-underline hover:underline text-airt-primary'>
                support@fastagency.ai
              </a>
              .
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
