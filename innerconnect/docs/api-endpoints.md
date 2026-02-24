# API Endpoints

Base path: `/api/v1`

## Auth
- `POST /auth/signup` - Sign up with company email (`@company.com`) and password.
- `POST /auth/verify-otp` - Verify email OTP.
- `POST /auth/login` - Login with rate limiting + JWT issue.
- `POST /auth/refresh` - Refresh token.
- `POST /auth/logout` - Revoke refresh token.

## Profile
- `GET /profiles/me` - Fetch self profile.
- `PUT /profiles/me` - Update profile fields.
- `PUT /profiles/me/visibility` - Toggle visibility settings.
- `DELETE /profiles/me` - Permanent deletion (anonymized).

## Discovery + Matching
- `GET /discovery/candidates` - Get swipe candidates by filters.
- `POST /likes` - Swipe action (`like` or `pass`).
- `GET /matches` - List matched users.

## Messaging
- `GET /matches/:id/messages` - Paginated message list.
- `POST /matches/:id/messages` - Send message.
- `PUT /messages/:id/seen` - Seen indicator update.

## Moderation
- `POST /reports` - Report user/content.
- `POST /blocks` - Block user.
- `DELETE /blocks/:blockedId` - Unblock user.

## Admin (RBAC: admin/moderator)
- `GET /admin/dashboard` - Analytics summary.
- `GET /admin/profiles/pending` - Profiles pending review.
- `PATCH /admin/profiles/:id` - Approve/reject profile.
- `PATCH /admin/reports/:id` - Update report status.
- `PATCH /admin/users/:id/ban` - Ban or unban user.
