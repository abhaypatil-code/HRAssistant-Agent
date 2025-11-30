# Deployment Guide

This guide explains how to deploy the HR Copilot AI Agent to Streamlit Community Cloud.

## Prerequisites

1.  A GitHub account
2.  A Streamlit Community Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io/))
3.  A Google Gemini API Key (get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

## Steps to Deploy

1.  **Push to GitHub**: Ensure your code is pushed to a GitHub repository.
    *   Note: Your local `.streamlit/secrets.toml` and `.env` files are **ignored** by git to protect your API keys. This is intentional.

2.  **Create App on Streamlit Cloud**:
    *   Go to [share.streamlit.io](https://share.streamlit.io/)
    *   Click "New app"
    *   Select your repository (`HRAssistant-Agent`), branch (`main`), and main file path (`app.py`).

3.  **Configure Secrets (CRITICAL)**:
    *   Before clicking "Deploy", click on **"Advanced settings"**.
    *   Find the **"Secrets"** field.
    *   Copy the contents of `.streamlit/secrets.toml.example` and paste them into the Secrets box.
    *   Replace `"your_api_key_here"` with your actual Google Gemini API Key.
    *   Example:
        ```toml
        GOOGLE_API_KEY = "AIzaSyD_..."
        ```
    *   Click "Save".

4.  **Deploy**:
    *   Click "Deploy!".
    *   Streamlit will install the dependencies from `requirements.txt` and start the app.

## Troubleshooting

*   **"API key expired" or "Key not found"**: Check your Secrets settings in the Streamlit Cloud dashboard. Ensure `GOOGLE_API_KEY` is set correctly.
*   **"FileNotFoundError"**: Ensure `data/` directory is committed to the repo.

## Local Development

For local development, create a file named `.streamlit/secrets.toml` (do not commit this file) and add your API key there:

```toml
GOOGLE_API_KEY = "your_actual_api_key"
```
