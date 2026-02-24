# Security Checklist

## Authentication
- [x] Restrict signup to company domain.
- [x] OTP verification required before login access.
- [x] Hash passwords with bcrypt.
- [x] Short-lived access JWT and refresh rotation.
- [x] Login rate limiting and account lockout policy.

## Authorization
- [x] RBAC middleware for employee/moderator/admin.
- [x] Verify ownership for profile and messaging resources.
- [x] Admin actions recorded in audit logs.

## Data Privacy
- [x] Profile visibility controls.
- [x] GDPR-style consent capture.
- [x] Permanent delete with anonymization.
- [x] No public user indexing/discoverability.

## Content Safety
- [x] Report + block flows.
- [x] Moderation queue with approve/reject.
- [x] Ban users and disable abusive accounts.

## Infra Security
- [x] HTTPS everywhere.
- [x] Helmet headers and strict CORS.
- [x] Input validation/sanitization.
- [x] Secrets from vault (not in source control).
- [x] Encryption at rest + in transit.
