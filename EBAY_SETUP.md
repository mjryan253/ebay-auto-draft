# Setting up eBay Sandbox Credentials

To enable your application to interact with the eBay Sandbox environment for testing purposes (e.g., listing items), you need to configure it with specific OAuth 2.0 credentials. This guide will walk you through obtaining the necessary `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, and `EBAY_REFRESH_TOKEN`, as well as understanding the `EBAY_MARKETPLACE_ID`.

## 1. Prerequisites

*   You must have an active eBay Developer Program account. If not, sign up at [https://developer.ebay.com/](https://developer.ebay.com/).
*   Familiarize yourself with the eBay Sandbox environment, which allows you to test your application without affecting live eBay listings.

## 2. Obtaining Application Keys (Client ID & Client Secret)

Your `EBAY_CLIENT_ID` (App ID) and `EBAY_CLIENT_SECRET` (Cert ID) identify your application to eBay. You will need these for the Sandbox environment.

*   Go to your eBay Developer Portal: [https://developer.ebay.com/my/keys](https://developer.ebay.com/my/keys)
*   Ensure you are working with **Sandbox** keys, not Production keys.
*   If you don't have a keyset for Sandbox, create one.
*   Note down your **App ID (Client ID)** and **Cert ID (Client Secret)**. These will be your `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET` respectively.

## 3. Generating a User Refresh Token for Sandbox

The `EBAY_REFRESH_TOKEN` allows your application to obtain new access tokens to make API calls on behalf of a sandbox test user without requiring them to log in repeatedly.

*   **Navigate to the eBay Application OAuth Tool for Sandbox:**
    *   Use this direct link: [https://developer.ebay.com/my/auth?env=sandbox&index=0](https://developer.ebay.com/my/auth?env=sandbox&index=0)
    *   This tool helps you generate User access tokens (and the associated refresh token) for the Sandbox environment.

*   **Configure Your Application's OAuth Settings:**
    *   Before generating the token, you might need to configure a "Redirect URL" for your application in the eBay Developer Portal. This URL is where eBay redirects the user after they grant consent. For local testing or if your application doesn't have a live endpoint yet, you can often use `https://localhost/` or a specific value eBay might provide like `urn:ietf:wg:oauth:2.0:oob` (Out Of Band) if available for non-web flows, though for the Authorization Code Grant, a reachable redirect URI is usually needed. The eBay token generation tool linked above might also offer an "eBay OOB" option or allow you to get the token directly.

*   **Choose Your Client ID:**
    *   In the token generation tool, select the Sandbox **Client ID (App ID)** you noted down in Step 2.

*   **Define Scopes:**
    *   You'll need to specify the permissions (scopes) your application requires. For listing items, common scopes include:
        *   `https://api.ebay.com/oauth/api_scope/sell.inventory`
        *   `https://api.ebay.com/oauth/api_scope/sell.marketing`
        *   `https://api.ebay.com/oauth/api_scope/sell.fulfillment`
        *   `https://api.ebay.com/oauth/api_scope/sell.account`
    *   Select all scopes necessary for the functionalities your application will use. Start with `https://api.ebay.com/oauth/api_scope/sell.inventory` for basic listing.

*   **Complete the Consent Flow:**
    *   Click "Get a User Token". This will redirect you to an eBay sandbox login page.
    *   Log in using one of your **Sandbox Test User** accounts (not your actual eBay developer account). You can create sandbox test users via the eBay Developer Portal under "Tools" > "Sandbox".
    *   Grant consent to your application.

*   **Receive the Authorization Code and Exchange it (or get tokens directly):**
    *   After consent, eBay will redirect you to your specified redirect URL with an `authorization_code` in the query parameters, OR the tool might directly display the access token and refresh token.
    *   **If you get an authorization code:** You need to exchange this code (along with your Client ID and Client Secret) for an access token and a refresh token. This is typically a POST request to eBay's token endpoint: `https://api.sandbox.ebay.com/identity/v1/oauth2/token`. However, the eBay developer portal tool linked above often simplifies this and directly provides you with the access token and refresh token.
    *   **Your goal is the `refresh_token`.** Make sure to copy it securely. This is your `EBAY_REFRESH_TOKEN`.

## 4. Understanding `EBAY_MARKETPLACE_ID`

The `EBAY_MARKETPLACE_ID` specifies which eBay marketplace your application will interact with (e.g., US, UK, Germany).

*   For the **US Sandbox**, the ID is `EBAY_US`.
*   For other marketplaces, refer to the official eBay documentation for the `MarketplaceIdEnum`: [eBay Marketplace ID Values](https://developer.ebay.com/api-docs/sell/account/types/ba:MarketplaceIdEnum) (This link points to the production values, but they are generally the same for Sandbox).

Common Marketplace IDs:
*   `EBAY_US`: United States
*   `EBAY_GB`: United Kingdom
*   `EBAY_DE`: Germany
*   `EBAY_AU`: Australia
*   `EBAY_CA`: Canada
*   `EBAY_FR`: France
*   `EBAY_IT`: Italy
*   `EBAY_ES`: Spain

## 5. Configuring Your Application

Once you have all the credentials, you need to make them available to your application. This project uses a `config/app.env` file for this purpose.

1.  If it doesn't exist, create a file named `app.env` in the `config/` directory. You can copy `config/example.env` to `config/app.env` to get started.
2.  Update `config/app.env` with the values you obtained:

    ```env
    # ... other configurations ...

    # eBay Sell Listing API credentials
    EBAY_CLIENT_ID=YOUR_SANDBOX_CLIENT_ID_HERE
    EBAY_CLIENT_SECRET=YOUR_SANDBOX_CLIENT_SECRET_HERE
    EBAY_REFRESH_TOKEN=YOUR_SANDBOX_REFRESH_TOKEN_HERE
    EBAY_MARKETPLACE_ID=EBAY_US # Or your desired sandbox marketplace ID
    ```

**Important Security Note:** The `EBAY_CLIENT_SECRET` and `EBAY_REFRESH_TOKEN` are sensitive. Keep them secure and **do not commit `config/app.env` to your Git repository if it contains real secrets.** The `.gitignore` file should already be configured to ignore `app.env`.

By following these steps, your application will be configured to authenticate with the eBay Sandbox and perform API operations on behalf of your test user.
