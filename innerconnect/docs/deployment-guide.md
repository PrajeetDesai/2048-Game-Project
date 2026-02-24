# Deployment Guide

## 1) Infrastructure
- Frontend: Vercel or AWS Amplify
- Backend: AWS ECS/Fargate or Azure App Service
- Database: AWS RDS PostgreSQL or Azure Database for PostgreSQL
- Object storage for photos: S3 / Azure Blob
- TLS and domain via company-managed certificate

## 2) Environment Variables
- `DATABASE_URL`
- `JWT_ACCESS_SECRET`
- `JWT_REFRESH_SECRET`
- `BCRYPT_ROUNDS`
- `COMPANY_EMAIL_DOMAIN=company.com`
- `REDIS_URL` (optional for rate-limit and chat scaling)
- `SOCKET_ORIGIN`

## 3) Backend Deployment
1. Build container image.
2. Run DB migrations (`db/schema.sql` + migration tooling).
3. Attach secrets from secret manager.
4. Enable HTTPS-only and WAF rules.
5. Configure autoscaling based on CPU/req latency.

## 4) Frontend Deployment
1. Build Next.js app.
2. Set API base URL as environment variable.
3. Configure CSP and secure headers.
4. Enable PWA + service worker for mobile campus users.

## 5) Campus-only Enforcement
- Restrict ingress to corporate VPN IP ranges.
- Enforce SSO / identity provider integration when available.
- Add network ACL and private DNS resolution.

## 6) Data Protection
- PostgreSQL encryption at rest.
- Encrypted backups and key rotation.
- Audit logs sent to SIEM.
