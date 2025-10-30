# Deploying to Vercel

This guide provides step-by-step instructions for deploying the Cerebras Chat Interface to [Vercel](https://vercel.com).

## Prerequisites

1.  **A Vercel Account:** You can sign up for a free account on the [Vercel website](https://vercel.com/signup).
2.  **A GitHub, GitLab, or Bitbucket Account:** You'll need to connect your Vercel account to a Git provider to deploy your application.
3.  **The Project Pushed to a Git Repository:** Ensure that the latest version of the application, including the `vercel.json` file, is pushed to your repository.

## Deployment Steps

1.  **Log in to Vercel:** Open your Vercel dashboard.

2.  **Import Your Project:**
    *   Click the **"Add New..."** button and select **"Project"**.
    *   Vercel will ask to connect to your Git provider. Grant the necessary permissions.
    *   Select the repository containing your Cerebras Chat Interface application and click **"Import"**.

3.  **Configure the Project:**
    *   **Project Name:** Vercel will automatically use your repository's name, but you can change it if you wish.
    *   **Framework Preset:** Vercel should automatically detect that this is a Flask application. If not, select **"Other"** as no specific preset is needed.
    *   **Build and Output Settings:** You can leave these as their default values. The `vercel.json` file in the repository will automatically configure the build process.
    *   **Environment Variables:** This is the most important step. You need to add the following environment variables:

        *   `CEREBRAS_API_KEY`: Your API key for the Cerebras AI models.
        *   `ALLOWED_ORIGINS`: This is crucial for preventing CORS errors. See the section below for detailed instructions.

4.  **Deploy:**
    *   Click the **"Deploy"** button.
    *   Vercel will now start the build process. It will install the Python dependencies from `requirements.txt`, configure the server, and deploy the application.
    *   You can monitor the deployment progress in the build logs.

5.  **Done!**
    *   Once the deployment is complete, Vercel will provide you with a URL where your application is live (e.g., `https://your-project-name.vercel.app`).
    *   Visit the URL to start using your deployed Cerebras Chat Interface.

## Troubleshooting CORS Issues

CORS (Cross-Origin Resource Sharing) errors are common when the frontend of your application, running on a specific domain, tries to communicate with a backend API running on the same or a different domain.

To fix this, you must explicitly tell the backend which frontend URLs are allowed to make requests.

### How to Configure `ALLOWED_ORIGINS`

1.  **Get Your Vercel URLs:**
    *   After your first deployment, Vercel will assign a unique URL for your project. It will look something like this: `https://cerebras-chat-interface-your-username.vercel.app`.
    *   Vercel also creates unique URLs for each preview deployment (every time you push a new commit to a branch).

2.  **Set the Environment Variable in Vercel:**
    *   In your Vercel project dashboard, go to the **"Settings"** tab.
    *   Click on **"Environment Variables"**.
    *   Create a new environment variable with the key `ALLOWED_ORIGINS`.
    *   In the value field, add your main Vercel URL. If you want to allow multiple URLs (for example, a local development server or preview deployments), you can add them as a comma-separated list.

    **Example:**
    ```
    https://cerebras-chat-interface-your-username.vercel.app,http://localhost:5000
    ```

    **To allow all subdomains for your project (useful for preview deployments), you can use a wildcard:**
    ```
    https://*.your-username.vercel.app,https://cerebras-chat-interface-your-username.vercel.app
    ```

3.  **Redeploy:**
    *   After setting the `ALLOWED_ORIGINS` environment variable, you'll need to redeploy your application for the changes to take effect.
    *   Go to the **"Deployments"** tab in your Vercel dashboard, select the latest deployment, and choose **"Redeploy"** from the menu.

By correctly configuring `ALLOWED_ORIGINS`, you ensure that only your frontend can communicate with your backend API, preventing CORS errors and securing your application.
