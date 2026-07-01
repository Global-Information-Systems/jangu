# Commit Checklist

This checklist contains the required changes to harden file uploads and update repository security/notice documentation. Add these to your next commit/PR and ensure tests and CI checks pass.

- [ ] Implement validators + safe `upload_to` (validate MIME/file signature, image verification, file size limits, filename sanitization/UUID names)
- [ ] Move `MEDIA_ROOT` outside source tree and ensure no-execute filesystem permissions
- [ ] Add Nginx config to deny script execution in media dir and configure X-Accel/X-Sendfile for secure file serving
- [ ] Add `SECURITY.md` and `NOTICE`/`THIRD_PARTY_NOTICES.md` with responsible disclosure instructions and third-party attributions
- [ ] Add unit + integration tests for uploads (validators, upload endpoint, unauthorized access, large file rejection)
- [ ] Add Bandit and dependency scanning (Dependabot/Safety/Snyk) to GitHub Actions
- [ ] Run full test suite (use `run_complete_test.sh`) and ensure all tests pass before merge

Notes:
- Default max upload size to enforce: 5 MB (adjust as needed)
- Allowed MIME types: image/png, image/jpeg, application/pdf (adjust per app requirements)
- Prefer presigned S3 URLs for public hosting or X-Accel/X-Sendfile for self-hosted production

Committed by: GitHub Copilot (assistant)
