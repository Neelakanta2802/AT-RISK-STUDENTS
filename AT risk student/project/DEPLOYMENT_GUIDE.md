# EWS Deployment Guide: Neon, Render, and Vercel

This guide provides step-by-step instructions to deploy the Early Warning System (EWS) to production.

---

## Architecture Overview

```mermaid
graph TD
    User([Browser Client]) -->|Requests SPA| Vercel[Vercel Frontend]
    User -->|API Calls & Uploads| Render[Render Backend]
    Render -->|PostgreSQL Queries| Neon[Neon Serverless DB]
```

- **Database**: [Neon](https://neon.tech) serverless PostgreSQL.
- **Backend API**: [Render](https://render.com) FastAPI Web Service.
- **Frontend App**: [Vercel](https://vercel.com) React (Vite) single-page application.

---

## Step 1: Database Setup & Migration (Neon)

1. Sign up on [Neon.tech](https://neon.tech) and create a new database project.
2. Select your desired region and choose **PostgreSQL 16+** (default).
3. Copy your database connection string from the dashboard (under **Connection Details**). It should look similar to:
   ```
   postgresql://username:password@ep-cool-breeze-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. On your local machine, open a terminal in the backend directory (`AT risk student/project/backend`) and run the deployment script to initialize the schema:
   ```bash
   # Enforce the DATABASE_URL environment variable
   $env:DATABASE_URL="postgresql://username:password@ep-cool-breeze-123456.us-east-2.aws.neon.tech/neondb?sslmode=require"
   
   # Run the deployment script using your python environment
   python deploy_neon_db.py
   ```
   *(Note: This creates all tables, views, triggers, and mock compatibility schemas for Supabase compatibility).*

---

## Step 2: Backend API Deployment (Render)

1. Sign up/Log in to [Render.com](https://render.com).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub repository containing the project.
4. Set the following configuration details:
   - **Name**: `ews-backend` (or similar)
   - **Language**: `Python`
   - **Root Directory**: `AT risk student/project/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Advanced** and add the following **Environment Variables**:
   - `DATABASE_URL`: *Your Neon connection string*
   - `API_HOST`: `0.0.0.0`
   - `LOG_LEVEL`: `INFO`
6. Click **Create Web Service**. Render will automatically provision the container, install the python libraries, and spin up the FastAPI server.
7. Once deployed, note down the Render URL (e.g. `https://ews-backend.onrender.com`).

---

## Step 3: Frontend Deployment (Vercel)

1. Sign up/Log in to [Vercel.com](https://vercel.com).
2. Click **Add New** and select **Project**.
3. Import your GitHub repository.
4. Set the following configuration details:
   - **Root Directory**: `AT risk student/project`
   - **Framework Preset**: `Vite` (Vercel should auto-detect this)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add the following **Environment Variables** in the Project Settings:
   - `VITE_API_URL`: `https://ews-backend.onrender.com` *(Change this to your actual Render URL)*
   - `VITE_DEMO_MODE`: `true` *(Enables local demo protected auth)*
6. Click **Deploy**. Vercel will build your static bundles and deploy them to a CDN.
7. SPA routing is automatically handled via the pre-configured [vercel.json](file:///c:/Users/Windows%2011/Downloads/EWS%20project/AT%20risk%20student/project/vercel.json) file in the root.

---

## Troubleshooting & Verification

### Verify Database Connection
To check if the backend is connected to the database successfully, navigate to:
```
https://your-backend-url.onrender.com/api/health
```
It should return:
```json
{
  "status": "healthy"
}
```

### Verify API Diagnostics
To verify that database queries are running properly, go to:
```
https://your-backend-url.onrender.com/api/diagnostics
```
Ensure that the `database` section shows `"connected": true`.

### Routing 404s
If you encounter 404 errors when reloading pages like `/dashboard` on Vercel, make sure the [vercel.json](file:///c:/Users/Windows%2011/Downloads/EWS%20project/AT%20risk%20student/project/vercel.json) file is committed to your repository's root directory:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```
This tells Vercel's server to redirect all requests back to `index.html` so that React Router can handle page navigation.
