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
    *   Before generating the token, you'll need to provide a **Redirect URI** to eBay. For server-side applications where you are manually generating an initial refresh token, the simplest approach is to use eBay's out-of-band (OOB) URI:
        *   **Recommended Redirect URI:** `urn:ietf:wg:oauth:2.0:oob`
        When you use the [eBay token generation tool](https://developer.ebay.com/my/auth?env=sandbox&index=0), look for an option to select 'OAuth redirect URI' and input this value if it's not already an option like 'eBay OOB'. This means eBay will display the authorization code or tokens to you directly in your browser, rather than redirecting to a web server you own.

*   **Choose Your Client ID:**
    *   In the token generation tool, select the Sandbox **Client ID (App ID)** you noted down in Step 2.

*   **Define Scopes:**
    *   You'll need to specify the permissions (scopes) your application requires. The scopes are space-separated. For the current functionality of creating and managing inventory items, the following scope is essential:
        *   `https://api.ebay.com/oauth/api_scope/sell.inventory`

        The application currently also requests these scopes, which are useful for managing seller account details and fulfillment, and may be used in future enhancements:
        *   `https://api.ebay.com/oauth/api_scope/sell.account`
        *   `https://api.ebay.com/oauth/api_scope/sell.fulfillment`

        When using the token generation tool, you can typically enter these scopes as a single space-separated string:
        `https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment`

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

# Configuring for eBay Production (Live) Environment

Once you have thoroughly tested your application using the eBay Sandbox environment, you can configure it to work with the live eBay Production environment.

**CRUCIAL WARNING:** All actions performed while configured for the Production environment are REAL. This includes creating live eBay listings, managing inventory that could be sold, and potentially incurring eBay fees. Proceed with caution and ensure your application logic is correct before switching to Production.

## 1. Production Credentials Required

You **MUST** obtain a separate set of credentials specifically for the Production environment. Sandbox credentials will **NOT** work for the live site, and vice-versa.

You will need:

*   **Production Application Keys:**
    *   Go to your eBay Developer Portal: [https://developer.ebay.com/my/keys](https://developer.ebay.com/my/keys)
    *   Ensure you select the **Production** keyset. If you don't have one, you'll need to create it.
    *   Note down your Production **App ID (Client ID)** and **Cert ID (Client Secret)**.
*   **Production User Refresh Token:**
    *   This token must be generated using your Production Application Keys and by logging in with your **real eBay account** that you intend to list items with.
    *   Use the eBay Application OAuth Tool: [https://developer.ebay.com/my/auth](https://developer.ebay.com/my/auth)
    *   **Critically important:** Ensure the environment selected in this tool is **Production**.
    *   Select your Production Client ID.
    *   Use the same Redirect URI method (e.g., `urn:ietf:wg:oauth:2.0:oob`) and scopes (e.g., `https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment`) as you did for Sandbox, ensuring they are appropriate for your live operations.
    *   Complete the consent flow with your live eBay account. Securely store the obtained **refresh_token**.

## 2. Updating `config/app.env` for Production

To switch your application to the Production environment, you will need to update the following variables in your `config/app.env` file:

*   `EBAY_CLIENT_ID`: Your **Production** App ID (Client ID).
*   `EBAY_CLIENT_SECRET`: Your **Production** Cert ID (Client Secret).
*   `EBAY_REFRESH_TOKEN`: Your **Production** User Refresh Token.
*   `EBAY_OAUTH_TOKEN_URL`: `https://api.ebay.com/identity/v1/oauth2/token`
*   `EBAY_API_BASE_URL`: `https://api.ebay.com`
*   `EBAY_MARKETPLACE_ID`: The `MarketplaceIdEnum` for the eBay site you are listing on (e.g., `EBAY_US` for eBay United States). Refer to the [eBay Marketplace ID Values](https://developer.ebay.com/api-docs/sell/account/types/ba:MarketplaceIdEnum) documentation if needed.

**Example `config/app.env` snippet for Production:**

```env
# ... other configurations ...

# eBay Sell Listing API credentials - PRODUCTION
EBAY_CLIENT_ID=YOUR_PRODUCTION_CLIENT_ID_HERE
EBAY_CLIENT_SECRET=YOUR_PRODUCTION_CLIENT_SECRET_HERE
EBAY_REFRESH_TOKEN=YOUR_PRODUCTION_REFRESH_TOKEN_HERE
EBAY_MARKETPLACE_ID=EBAY_US # Or your desired production marketplace ID

# eBay API Environment Configuration - PRODUCTION
EBAY_OAUTH_TOKEN_URL=https://api.ebay.com/identity/v1/oauth2/token
EBAY_API_BASE_URL=https://api.ebay.com
```

## 3. Final Checks Before Going Live

*   **Review Scopes:** Ensure the OAuth scopes associated with your production refresh token grant the necessary permissions for your application's features, but no more.
*   **Test Thoroughly:** If possible, perform a final round of testing with a limited set of non-critical items in the production environment to ensure everything works as expected.
*   **Monitor:** After going live, monitor your application's activity and eBay account closely.
