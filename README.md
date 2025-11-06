# Mom's Eye Application

This is a FastAPI application for managing user registrations and interacting with OpenAI.

## How it Works

The application provides a web interface for user login and registration. Registered users can access a dashboard with chat functionality powered by OpenAI. User credentials and additional details (parent's name, child's name, child's date of birth, phone number) are stored in a local `users.json` file.

For external integrations, the application exposes a secured API endpoint (`/api/users`) that allows authorized services (like n8n) to fetch user data. This data can then be used to trigger automated processes, such as sending reminder calls via Twilio for events like vaccine due dates or birthdays.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd mom-s-eye
    ```

2.  **Create a `.env` file:**
    Create a file named `.env` in the root directory with the following content, replacing the placeholder values with your actual keys:
    ```
    OPENAI_API_KEY=your_openai_api_key
    API_KEY=your_secret_api_key_for_n8n
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    ```

## Running the Application with Docker Compose

Make sure you have Docker and Docker Compose installed.

1.  **Build and run the services:**
    ```bash
    docker-compose up --build
    ```

    The application will be accessible at `http://localhost:8000`.

## Running the Application Locally (without Docker)

1.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    # source .venv/bin/activate  # On macOS/Linux
    pip install -r requirements.txt
    ```

2.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

    The application will be accessible at `http://localhost:8000`.

## n8n and Twilio Integration for Reminders

This application exposes an API endpoint `/api/users` that can be used by n8n to fetch user data for reminder calls.

**Endpoint:** `http://localhost:8000/api/users` (adjust host/port as necessary)
**Authentication:** Requires an `X-API-Key` header with the value set in your `.env` file (`API_KEY`).

Refer to the detailed instructions provided previously for setting up the n8n workflow with a Function node and Twilio node to send reminder calls based on user data.