# n8n Railway Deployment

Production-ready deployment of [n8n](https://n8n.io) workflow automation platform on Railway using Docker.

## Overview

This project provides a minimal configuration to deploy n8n on Railway with:

- Official n8n Docker image (`n8nio/n8n`)
- External PostgreSQL database (Railway service)
- Persistent data storage using Railway volumes
- Secure configuration with environment variables
- HTTPS support via Railway's automatic SSL

## Prerequisites

- A Railway account ([railway.app](https://railway.app))
- Railway CLI (optional, for command-line deployment)

## Project Structure

```
n8n-railway/
├── Dockerfile       # Minimal Dockerfile using official n8n image
├── env.example      # Template with all required environment variables
└── README.md        # This file
```

## Deployment Guide

### Step 1: Create a New Railway Project

1. Log in to [Railway](https://railway.app)
2. Click **"New Project"**
3. Choose **"Deploy from GitHub repo"** or **"Empty Project"**

### Step 2: Add PostgreSQL Database

1. In your Railway project, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway will automatically provision a PostgreSQL instance
3. The following environment variables will be automatically available:
   - `PGHOST`
   - `PGPORT`
   - `PGDATABASE`
   - `PGUSER`
   - `PGPASSWORD`
   - `DATABASE_URL`

### Step 3: Deploy n8n Service

#### Option A: Deploy from GitHub (Recommended)

1. Push this repository to your GitHub account
2. In Railway, click **"New"** → **"GitHub Repo"**
3. Select this repository
4. Railway will automatically detect the Dockerfile and build the image

#### Option B: Deploy using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Step 4: Configure Environment Variables

In the Railway dashboard, go to your n8n service and add these environment variables:

#### Required Variables

```bash
# n8n Host Configuration
N8N_HOST=your-app-name.up.railway.app
N8N_PROTOCOL=https
N8N_PORT=5678

# Database Configuration
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=${PGHOST}
DB_POSTGRESDB_PORT=${PGPORT}
DB_POSTGRESDB_DATABASE=${PGDATABASE}
DB_POSTGRESDB_USER=${PGUSER}
DB_POSTGRESDB_PASSWORD=${PGPASSWORD}

# Security (REQUIRED!)
N8N_ENCRYPTION_KEY=<generate-random-key>

# Basic Authentication
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=<your-secure-password>

# Webhook URL
WEBHOOK_URL=https://your-app-name.up.railway.app
```

#### Generate Encryption Key

Generate a secure encryption key using one of these methods:

```bash
# Using OpenSSL
openssl rand -hex 32

# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

**Important:** Store this key securely. If you lose it, you won't be able to decrypt stored credentials.

### Step 5: Mount Railway Volume for Data Persistence

1. In your n8n service, go to **"Settings"** → **"Volumes"**
2. Click **"Add Volume"**
3. Configure:
   - **Mount Path:** `/home/node/.n8n`
   - **Size:** 1GB (or more, depending on your needs)
4. Click **"Add"**

This ensures all n8n data (workflows, credentials, executions) persists across deployments.

### Step 6: Configure Networking

1. In your n8n service, go to **"Settings"** → **"Networking"**
2. Railway should automatically detect port 5678
3. If not, manually set the port to **5678**
4. Railway will generate a public domain (e.g., `your-app-name.up.railway.app`)

### Step 7: Update N8N_HOST Variable

1. Copy the Railway-generated domain
2. Update the `N8N_HOST` environment variable with this domain
3. Update the `WEBHOOK_URL` environment variable with `https://your-domain.up.railway.app`
4. Restart the service for changes to take effect

### Step 8: Access n8n

1. Navigate to your Railway domain (e.g., `https://your-app-name.up.railway.app`)
2. Log in using the credentials from `N8N_BASIC_AUTH_USER` and `N8N_BASIC_AUTH_PASSWORD`
3. Complete the initial setup wizard

## Environment Variables Reference

### Core Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `N8N_HOST` | Public domain where n8n is accessible | Yes | - |
| `N8N_PROTOCOL` | Protocol (http/https) | Yes | `https` |
| `N8N_PORT` | Internal port n8n listens on | Yes | `5678` |

### Database Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DB_TYPE` | Database type | Yes | `postgresdb` |
| `DB_POSTGRESDB_HOST` | PostgreSQL host | Yes | `${PGHOST}` |
| `DB_POSTGRESDB_PORT` | PostgreSQL port | Yes | `${PGPORT}` |
| `DB_POSTGRESDB_DATABASE` | Database name | Yes | `${PGDATABASE}` |
| `DB_POSTGRESDB_USER` | Database user | Yes | `${PGUSER}` |
| `DB_POSTGRESDB_PASSWORD` | Database password | Yes | `${PGPASSWORD}` |

### Security

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `N8N_ENCRYPTION_KEY` | Encryption key for credentials | Yes | - |
| `N8N_BASIC_AUTH_ACTIVE` | Enable basic authentication | Recommended | `true` |
| `N8N_BASIC_AUTH_USER` | Basic auth username | If auth enabled | - |
| `N8N_BASIC_AUTH_PASSWORD` | Basic auth password | If auth enabled | - |

### Webhooks

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `WEBHOOK_URL` | Public URL for webhooks | Yes | - |

### Optional Configuration

See `env.example` for additional optional variables:
- Execution mode and timeouts
- Timezone settings
- Logging configuration
- SMTP email settings

## Data Persistence

n8n stores all data in `/home/node/.n8n`, including:

- **Workflows:** Your automation workflows
- **Credentials:** Encrypted credentials for integrations
- **Executions:** Workflow execution history (if not using PostgreSQL)
- **Settings:** n8n configuration

Ensure the Railway volume is properly mounted to prevent data loss during redeployments.

## Security Best Practices

1. **Encryption Key:** Never commit `N8N_ENCRYPTION_KEY` to version control
2. **Strong Passwords:** Use strong passwords for basic authentication
3. **Environment Variables:** Store all secrets in Railway's environment variables
4. **HTTPS Only:** Always use HTTPS in production (`N8N_PROTOCOL=https`)
5. **User Management:** After initial setup, consider using n8n's built-in user management instead of basic auth
6. **Regular Backups:** Regularly backup your PostgreSQL database and volume data

## Monitoring and Logs

View logs in Railway:

1. Go to your n8n service
2. Click the **"Deployments"** tab
3. Click on the latest deployment
4. View real-time logs in the **"Logs"** section

## Troubleshooting

### n8n Won't Start

- Check that all required environment variables are set
- Verify PostgreSQL connection by checking database credentials
- Review logs in Railway dashboard

### Database Connection Errors

- Ensure PostgreSQL service is running
- Verify `DB_POSTGRESDB_*` variables reference Railway's PG variables correctly
- Check that both services are in the same Railway project

### Lost Data After Redeployment

- Verify Railway volume is mounted to `/home/node/.n8n`
- Check volume size hasn't been exceeded
- Ensure volume wasn't accidentally deleted

### Webhook URLs Not Working

- Confirm `WEBHOOK_URL` matches your public domain with `https://`
- Verify `N8N_HOST` is set correctly
- Check Railway networking settings

## Upgrading n8n

Railway automatically uses the `:latest` tag. To upgrade:

1. Trigger a new deployment in Railway
2. Railway will pull the latest n8n image
3. Your data persists across upgrades via the mounted volume

To use a specific version, modify the Dockerfile:

```dockerfile
FROM n8nio/n8n:1.0.0  # Replace with desired version
```

## Cost Considerations

Railway pricing (as of 2026):

- **n8n Service:** Based on resource usage (CPU, memory, network)
- **PostgreSQL:** Based on resource usage and storage
- **Volume Storage:** Based on size allocated
- **Free Tier:** $5 free credit per month

Estimate your costs using Railway's pricing calculator.

## Additional Resources

- [n8n Documentation](https://docs.n8n.io)
- [n8n Community Forum](https://community.n8n.io)
- [Railway Documentation](https://docs.railway.app)
- [n8n GitHub Repository](https://github.com/n8n-io/n8n)

## Support

For n8n-specific issues:
- [n8n Community Forum](https://community.n8n.io)
- [n8n GitHub Issues](https://github.com/n8n-io/n8n/issues)

For Railway-specific issues:
- [Railway Help Center](https://help.railway.app)
- [Railway Discord](https://discord.gg/railway)

## License

This deployment configuration is provided as-is. n8n itself is licensed under the [Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md).

---

**Note:** Remember to replace placeholder values in environment variables with your actual configuration before deployment.
