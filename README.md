# 🚀 Cobox AI Backend - Production

Production URL:

https://ai.cobox.co

---

# 🏗 Architecture Overview

Tech Stack:

- FastAPI
- Uvicorn
- Ubuntu EC2
- Nginx (reverse proxy)
- Systemd service (`cobox`)
- GitHub Actions (Auto Deploy)

Deployment Flow:

GitHub Push → GitHub Actions → SSH → EC2 → git pull → install deps → restart service → LIVE

Every push to `main` branch deploys automatically to production.

---

# ⚠️ IMPORTANT RULES (MUST READ)

Before pushing code:

❌ DO NOT push secrets  
❌ DO NOT modify `.github/workflows/deploy.yml`  
❌ DO NOT SSH into production server  
❌ DO NOT change nginx or systemd configs  
❌ DO NOT commit `.env`  
❌ DO NOT delete `requirements.txt`

Only edit:

- main.py
- new API modules
- requirements.txt

---

# 👨‍💻 First Time Setup (Local Development)

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Cobox-no-code/Cobox-Ai.git
cd Cobox-Ai
