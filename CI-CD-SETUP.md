# Jangu CI/CD Setup Guide

## Overview
This document explains the automated CI/CD pipeline for the Jangu Node.js project.

## Workflow Files Created

### 1. `.github/workflows/ci-cd.yml`
The main GitHub Actions workflow that runs on every push and pull request.

**Jobs:**
- **Lint**: ESLint checks across Node.js versions 18, 20, 22
- **Test**: Unit tests with Jest and coverage reporting
- **Build**: Creates build artifacts
- **Deploy Staging**: Deploys to staging on develop branch pushes
- **Deploy Production**: Deploys to production on main branch pushes

### 2. Configuration Files

#### `.eslintrc.json`
ESLint configuration for code quality checks.
- Enforces consistent code style
- Catches common errors
- Customizable rules

#### `jest.config.js`
Jest test framework configuration.
- Runs tests in Node.js environment
- Collects coverage metrics
- 70% minimum coverage threshold

#### `.env.example`
Template for environment variables.
- Copy to `.env` locally
- Never commit `.env` file

#### `package.json.example`
Example package.json with required scripts:
- `npm run lint` - Run ESLint
- `npm test` - Run Jest tests with coverage
- `npm run build` - Build application
- `npm start` - Start application
- `npm run dev` - Start with nodemon

## Setup Instructions

### 1. Update Package.json
Ensure your `package.json` has these scripts:
```json
{
  "scripts": {
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "test": "jest --coverage",
    "test:watch": "jest --watch",
    "build": "your-build-command",
    "start": "node src/index.js",
    "dev": "nodemon src/index.js"
  },
  "devDependencies": {
    "eslint": "^8.54.0",
    "jest": "^29.7.0",
    "nodemon": "^3.0.1"
  }
}
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Variables
```bash
# Copy example to local .env
cp .env.example .env

# Edit .env with your values
```

### 4. Test Locally
```bash
# Run linting
npm run lint

# Run tests
npm test

# Run in watch mode
npm test -- --watch
```

### 5. Configure Deployment

Edit `.github/workflows/ci-cd.yml` and uncomment your deployment method:

#### For Heroku:
```yaml
- name: Deploy to Heroku
  uses: akhileshns/heroku-deploy@v3.14.0
  with:
    heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
    heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
    heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

#### For AWS:
```yaml
- name: Deploy to AWS
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1
```

#### For DigitalOcean:
```yaml
- name: Deploy to DigitalOcean
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.DIGITALOCEAN_HOST }}
    username: ${{ secrets.DIGITALOCEAN_USER }}
    key: ${{ secrets.DIGITALOCEAN_SSH_KEY }}
    script: |
      cd /app
      git pull origin develop
      npm ci --omit=dev
      npm run build
      pm2 restart app
```

### 6. GitHub Secrets Setup

Add these secrets in GitHub repo settings (Settings → Secrets and variables → Actions):

**For Heroku:**
- `HEROKU_API_KEY` - Your Heroku API key
- `HEROKU_APP_NAME` - Your app name
- `HEROKU_EMAIL` - Your email

**For AWS:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

**For DigitalOcean:**
- `DIGITALOCEAN_HOST` - Server IP
- `DIGITALOCEAN_USER` - SSH user
- `DIGITALOCEAN_SSH_KEY` - Private SSH key

## Local Testing with Act (Nektos)

Test workflows locally before pushing:

### Install Act
```bash
# macOS
brew install act

# Ubuntu/Debian
sudo apt install act

# Or download from https://github.com/nektos/act
```

### Run Workflow Locally
```bash
# List available workflows
act -l

# Run specific workflow
act push -j lint
act push -j test
act push -j build

# Run all jobs
act push
```

### Create .env for Act
Create `.actrc` for local act execution:
```
-P ubuntu-latest=-self-hosted
--env NODE_ENV=test
```

## Branch Strategy

- **main**: Production-ready code
  - Deployment: Production only
  - Protection: Require PR reviews
  
- **develop**: Development branch
  - Deployment: Staging only
  - Where features merge in

- **feature/\***: Feature branches
  - Create from: `develop`
  - Merge to: `develop` via PR

## Monitoring

Check workflow status:
1. Go to: `https://github.com/tijuks/jangu/actions`
2. View logs for each job
3. Check deployment status

## Troubleshooting

### Workflow Not Running
- Check branch name matches trigger (main or develop)
- Verify `.github/workflows/ci-cd.yml` syntax with `act -l`

### Linting Fails
```bash
npm run lint:fix  # Auto-fix issues
npm run lint      # Check again
```

### Tests Fail
```bash
npm test -- --verbose  # See detailed output
npm test -- --watch    # Debug in watch mode
```

### Deployment Fails
- Check GitHub secrets are set
- Verify credentials are correct
- Check deployment logs in Actions tab

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [ESLint Documentation](https://eslint.org/)
- [Jest Testing Guide](https://jestjs.io/)
- [Nektos/Act](https://github.com/nektos/act)
- [Node.js Best Practices](https://nodejs.org/en/docs/guides/)
