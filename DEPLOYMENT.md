# Complete Deployment Guide

This guide walks you through deploying the SkinAI application to production.

---

## 📋 Pre-Deployment Checklist

- [ ] Model trained and saved (`model/skin_disease_model.h5`)
- [ ] Model evaluated with acceptable accuracy (≥85%)
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] CORS settings updated for production URLs
- [ ] Secret keys changed from defaults
- [ ] Database migrations applied

---

## 🚀 Deployment Overview

```
Frontend (React)          Backend (Flask)
      ↓                        ↓
   Vercel/Netlify        Render/Railway
      ↓                        ↓
   Static Files           Python Server
      ↓                        ↓
   └──────────→ User ←─────────┘
```

---

## Part 1: Backend Deployment (Render)

### Step 1: Prepare Your Repository

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - SkinAI application"
   git remote add origin https://github.com/yourusername/skin-ai.git
   git push -u origin main
   ```

2. **Verify Repository Structure**
   Ensure these files are committed:
   - `backend/` folder with all Python files
   - `model/` folder with training scripts
   - `requirements.txt`
   - `gunicorn.conf.py`

### Step 2: Deploy to Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   ```
   Name: skin-detection-api
   Environment: Python
   Region: Choose closest to your users
   Branch: main
   Root Directory: backend
   ```

4. **Build & Start Commands**
   ```bash
   Build Command:
   pip install -r requirements.txt

   Start Command:
   gunicorn -c gunicorn.conf.py app:app
   ```

5. **Set Environment Variables**
   
   Click "Environment" and add:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-a-strong-random-key>
   FRONTEND_URL=https://your-frontend-domain.vercel.app
   DATABASE_URL=sqlite:///predictions.db
   LOG_LEVEL=INFO
   ```

   **Generate a secure secret key:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for build and deployment (5-10 minutes)
   - Copy your backend URL: `https://skin-detection-api.onrender.com`

### Step 3: Verify Deployment

Test your deployed backend:

```bash
# Health check
curl https://your-backend-url.onrender.com/api/health

# Should return:
{
  "status": "healthy",
  "model_loaded": true,
  "database": "connected",
  "version": "1.0.0"
}
```

---

## Part 2: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Update Environment Variables**
   
   Create `.env.production` in `frontend/` directory:
   ```env
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

2. **Test Build Locally**
   ```bash
   cd frontend
   npm run build
   npm run preview
   ```
   
   Verify the app works and connects to the production backend.

### Step 2: Deploy to Vercel

**Option A: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
cd frontend
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name? skin-ai-frontend
# - Directory? ./
# - Override settings? N

# Production deploy
vercel --prod
```

**Option B: Using Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New..." → "Project"
3. Import from GitHub
4. Configure:
   ```
   Project Name: skin-ai-frontend
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

5. **Add Environment Variable**
   ```
   Name: VITE_API_URL
   Value: https://your-backend-url.onrender.com
   ```

6. Click "Deploy"
7. Wait for deployment (2-3 minutes)
8. Your frontend is live at: `https://skin-ai-frontend.vercel.app`

### Step 3: Update Backend CORS

After frontend deployment, update the backend:

1. Go to Render Dashboard
2. Open your backend service
3. Go to "Environment" tab
4. Update `FRONTEND_URL`:
   ```
   FRONTEND_URL=https://skin-ai-frontend.vercel.app
   ```
5. Save and wait for redeployment

---

## Part 3: Database Setup (Production)

### Option 1: SQLite (Simple - Free)

- Already configured in the app
- Database file created automatically
- Suitable for low-traffic applications
- **Limitation**: Not scalable, data lost on redeployment (Render free tier)

### Option 2: PostgreSQL (Recommended - Production)

1. **Create Database on Render**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Choose plan (Free tier available)
   - Copy the external database URL

2. **Update Backend Environment Variable**
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

3. **Redeploy Backend**
   - Render will automatically redeploy
   - Database tables created on first run

---

## Part 4: Model Deployment

### Option 1: Include in Repository (Simple)

If model file < 100MB:
```bash
git add model/skin_disease_model.h5
git commit -m "Add trained model"
git push
```

### Option 2: Download on Build (Recommended)

1. **Upload Model to Cloud Storage**
   - AWS S3, Google Cloud Storage, or GitHub Releases
   - Get public download URL

2. **Create Build Script** (`backend/download_model.sh`):
   ```bash
   #!/bin/bash
   MODEL_URL="https://your-storage.com/skin_disease_model.h5"
   MODEL_PATH="../model/skin_disease_model.h5"
   
   if [ ! -f "$MODEL_PATH" ]; then
       echo "Downloading model..."
       curl -L "$MODEL_URL" -o "$MODEL_PATH"
   else
       echo "Model already exists"
   fi
   ```

3. **Update Build Command on Render**:
   ```bash
   chmod +x download_model.sh && ./download_model.sh && pip install -r requirements.txt
   ```

---

## Part 5: Custom Domain (Optional)

### Frontend (Vercel)

1. Go to Vercel Dashboard
2. Select your project
3. Go to "Settings" → "Domains"
4. Add your custom domain
5. Update DNS records as instructed

### Backend (Render)

1. Go to Render Dashboard
2. Select your backend service
3. Go to "Settings" → "Custom Domain"
4. Add your domain
5. Update DNS CNAME record

---

## Part 6: Monitoring & Maintenance

### Set Up Logging

1. **Render Logs**
   - View in Dashboard → "Logs" tab
   - Filter by date/time
   - Download logs

2. **Application Logs**
   - Logs stored in `backend/logs/skin_detection.log`
   - Rotated automatically (10MB max, 5 backups)

### Monitoring

- **Render**: Built-in metrics (CPU, Memory, Response Time)
- **Vercel**: Analytics dashboard
- **Uptime Monitoring**: Use UptimeRobot or Pingdom

### Backups

1. **Database Backup** (PostgreSQL):
   ```bash
   pg_dump -h host -U user dbname > backup.sql
   ```

2. **Model Backup**:
   - Keep copy in cloud storage
   - Version control with Git LFS

---

## Part 7: Post-Deployment Testing

### 1. Test All Endpoints

```bash
# Health check
curl https://your-backend.onrender.com/api/health

# Test prediction
curl -X POST https://your-backend.onrender.com/api/predict \
  -F "image=@test-image.jpg"

# Check history
curl https://your-backend.onrender.com/api/history?limit=5
```

### 2. Test Frontend

- Open `https://your-frontend.vercel.app`
- Navigate through all pages
- Upload test image
- Verify prediction results
- Check mobile responsiveness
- Test error handling

### 3. Performance Testing

```bash
# Test response time
curl -w "@curl-format.txt" -o /dev/null -s \
  https://your-backend.onrender.com/api/health

# Load testing (optional)
npm install -g autocannon
autocannon -c 10 -d 10 https://your-backend.onrender.com/api/health
```

---

## Part 8: Security Hardening

### Backend

1. **Enable HTTPS**
   - Automatic on Render and Vercel
   - Verify SSL certificate

2. **Rate Limiting** (Optional)
   Add to `backend/requirements.txt`:
   ```
   flask-limiter==3.5.0
   ```
   
   Implement in `backend/app.py`:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=get_remote_address)
   
   @api_bp.route('/predict', methods=['POST'])
   @limiter.limit("10 per minute")
   def predict():
       # ...
   ```

3. **File Upload Security**
   - Already implemented (validation, size limits)
   - Regular cleanup of old uploads

### Frontend

1. **Environment Variables**
   - Never commit `.env` files
   - Use Vercel environment variables

2. **Content Security Policy**
   Add to `frontend/index.html`:
   ```html
   <meta http-equiv="Content-Security-Policy" 
         content="default-src 'self'; 
                  img-src 'self' data: https:; 
                  script-src 'self' 'unsafe-inline'; 
                  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
                  font-src https://fonts.gstatic.com;">
   ```

---

## Troubleshooting Deployment Issues

### Issue: Backend won't start
**Solution:**
- Check Render logs for errors
- Verify all environment variables are set
- Ensure `requirements.txt` includes all dependencies
- Check Python version compatibility

### Issue: CORS errors in production
**Solution:**
- Update `FRONTEND_URL` in backend environment variables
- Include full URL with https://
- Redeploy backend after changes

### Issue: Model not loading
**Solution:**
- Verify model file exists in repository
- Check file path in configuration
- Ensure model is compatible with TensorFlow version
- Check memory limits on hosting platform

### Issue: Frontend build fails
**Solution:**
- Check for TypeScript errors
- Verify all imports are correct
- Clear build cache: `rm -rf dist/`
- Check Node.js version compatibility

### Issue: Database connection fails
**Solution:**
- Verify DATABASE_URL format
- Check database credentials
- Ensure database is accessible from Render
- Test connection string locally

---

## Cost Estimates

### Free Tier Deployment
- **Render**: Free (750 hours/month, sleeps after 15 min inactivity)
- **Vercel**: Free (unlimited deployments, 100GB bandwidth)
- **SQLite**: Free (included)
- **Total**: $0/month

### Production Deployment
- **Render**: $7-25/month (dedicated instances)
- **Vercel**: $20/month (Pro plan)
- **PostgreSQL**: $7-49/month (depending on size)
- **Total**: $34-94/month

---

## Next Steps After Deployment

1. **Set up custom domain**
2. **Configure analytics** (Google Analytics, Plausible)
3. **Add monitoring** (Sentry, LogRocket)
4. **Set up CI/CD** (GitHub Actions)
5. **Implement user authentication** (if needed)
6. **Add email notifications**
7. **Optimize model performance**
8. **Gather user feedback**

---

## Support

If you encounter issues:
1. Check this guide thoroughly
2. Review application logs
3. Check Render/Vercel status pages
4. Create an issue on GitHub
5. Contact support

---

**Deployment Complete! 🎉**

Your SkinAI application is now live and accessible worldwide!
