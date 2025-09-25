# Crop Sathi Project

Crop Sathi is a full-stack web application designed to provide hyper-local, intelligent crop advisories to farmers. It uses real-time weather data, pest prediction models, and market price trends to deliver actionable insights via a web dashboard, SMS, and WhatsApp.

## Project Structure

- **/backend**: Contains the FastAPI server, database models, business logic, and API endpoints.
- **/frontend**: Contains the `index.html` file with all the necessary HTML, CSS (Tailwind), and JavaScript for the user interface.
- **.env**: Stores secret keys and configuration variables.
- **requirements.txt**: Lists the Python dependencies for the backend.

## 1. Install Dependencies

Install the required Python packages. It's highly recommended to do this within a [virtual environment](https://docs.python.org/3/tutorial/venv.html).
```bash
pip install -r requirements.txt
```

## 2. Run with Docker (Recommended)

**Prerequisite**: Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running on your system.

From the project root directory (`CropSathiProject/`), run:

```bash
docker compose up --build
```

This will start both the FastAPI backend and the PostgreSQL database automatically.
You can then access the complete application at:

👉 http://localhost:8000

## 4. Deploy to the Cloud with Render

This project is configured for easy deployment to [Render](https://render.com/), a cloud platform that offers a free tier for web services and databases.

### Prerequisites

1.  **GitHub Account**: Your project code should be in a GitHub repository.
2.  **Render Account**: Sign up for a free account on [Render](https://render.com/).

### Deployment Steps

1.  **Create a New Blueprint Instance**:
    *   Go to the [Blueprints page](https://dashboard.render.com/blueprints) on your Render dashboard.
    *   Click **New Blueprint Instance**.
    *   Connect your GitHub account and select the repository for this project.

2.  **Configure and Deploy**:
    *   Render will automatically detect and use the `render.yaml` file in your repository.
    *   Give your service a unique name (e.g., `cropsathi-yourname`).
    *   Click **Apply**.

3.  **Set Environment Variables**:
    *   After the initial setup, go to your application's **Environment** tab in Render.
    *   Add your secret keys (like `SECRET_KEY`, `WEATHER_API_KEY`, and Twilio credentials) as environment variables. Render will automatically restart your application with the new settings.

That's it! Render will build and deploy your application. Once it's live, you can access it at the URL provided on your Render dashboard (e.g., `https://cropsathi-yourname.onrender.com`).

## 3. Running Manually (For Development Only)

If you prefer not to use Docker:

1.  **Environment Setup**:
    *   Create a `.env` file in the project root. See `backend/security.py` and `backend/services.py` for required variables (`SECRET_KEY`, `WEATHER_API_KEY`, Twilio credentials).
    *   Make sure you have a local PostgreSQL server running.
    *   Update your `.env` file with the correct database connection string:
        ```
        DATABASE_URL=postgresql://user:password@localhost/cropsathi_db
        ```
    *   💡 If you don’t have PostgreSQL locally, you can switch to SQLite. Just **omit the `DATABASE_URL`** from your `.env` file. The application will automatically fall back to using a local `cropsathi.db` file.

2.  **Run the Server**:
    From the project root directory (`CropSathiProject/`), run:
    ```bash
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```

Open your browser and go to:

👉 http://localhost:8000