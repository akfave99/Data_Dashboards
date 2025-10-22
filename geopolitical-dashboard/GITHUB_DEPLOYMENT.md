# GitHub Deployment Guide

## �� Quick Start - Push to GitHub in 3 Steps

### Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name**: `geopolitical-dashboard`
   - **Description**: `Interactive geopolitical analysis dashboard with 8 charts`
   - **Public** (so it can be deployed)
3. Click **"Create repository"**

### Step 2: Connect Local Repository to GitHub

Run these commands in your terminal:

```bash
cd /Users/ak/geopolitical-dashboard

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/geopolitical-dashboard.git

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### Step 3: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/geopolitical-dashboard`
2. You should see all your files!
3. Check that the README.md displays correctly

---

## 🌐 Deploy to Plotly Cloud from GitHub

Once your code is on GitHub:

1. Go to https://chart-studio.plotly.com/
2. Click **"Create"** → **"Deploy App"**
3. Select **"Dash App"**
4. Click **"Connect GitHub"**
5. Select your repository: `geopolitical-dashboard`
6. Select branch: `main`
7. Click **"Deploy"**

Your app will be live at:
```
https://chart-studio.plotly.com/~your-username/geopolitical-dashboard
```

---

## 📝 Making Updates

After deployment, to make updates:

1. Make changes locally
2. Test them: `python app.py`
3. Commit and push:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main
   ```
4. Plotly Cloud will automatically redeploy!

---

## 🔑 Important Notes

- **Replace `YOUR_USERNAME`** with your actual GitHub username
- **Make sure the repository is PUBLIC** for Plotly Cloud to access it
- **Keep your code clean** - the .gitignore file handles unnecessary files
- **Test locally first** before pushing to GitHub

---

## ✅ Checklist

- [ ] GitHub account created
- [ ] New repository created at github.com/new
- [ ] Local git remote added
- [ ] Code pushed to GitHub
- [ ] Repository visible on GitHub
- [ ] Connected to Plotly Cloud
- [ ] App deployed and live!

---

## 🆘 Troubleshooting

**"fatal: remote origin already exists"**
- Run: `git remote remove origin`
- Then add the new remote

**"Permission denied (publickey)"**
- Set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

**"Repository not found"**
- Make sure the repository is PUBLIC
- Check that the URL is correct

---

**Ready? Let's deploy! 🚀**
