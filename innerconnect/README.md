# InnerConnect

InnerConnect is a privacy-first dating platform for employees inside a single company campus. This repository contains a production-ready architecture blueprint with a Next.js frontend, Express backend, and PostgreSQL schema.

## Monorepo Structure

- `apps/web` – Next.js + Tailwind CSS responsive app
- `apps/api` – Node.js + Express JWT-secured API
- `db` – PostgreSQL schema and indexes
- `docs` – API, deployment, and security checklists

## Quick Start

1. Configure environment variables from `.env.example` files.
2. Create PostgreSQL database and run `db/schema.sql`.
3. Start backend API.
4. Start frontend web app.

See `docs/deployment-guide.md` for deployment details.

## Deliverables Included

- Folder structure: `docs/folder-structure.md`
- Database schema SQL: `db/schema.sql`
- API endpoint list: `docs/api-endpoints.md`
- Sample frontend components: `apps/web/components/*`
- Matching algorithm logic: `apps/api/src/utils/matching.js`
- Deployment guide: `docs/deployment-guide.md`
- Security checklist: `docs/security-checklist.md`
