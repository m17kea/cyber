# LAN Remediation Plan (2026-02-15)

## Scope
- Network: `[REDACTED_PRIVATE_IP]/24`
- Deep-focus hosts: `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]`
- Supporting exposures from prior scan: `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]`

## High Priority

### 1) `[REDACTED_PRIVATE_IP]` (SMB)
Observed:
- `139/tcp`, `445/tcp` open
- Service identified as `Apple Time Capsule smbd`
- SMB2 negotiation failed (`SMB 2+ not supported`), suggesting legacy SMB behavior

Risk:
- Legacy SMB exposure is a common lateral movement path in home/SMB networks.

Actions:
1. Disable SMB sharing if not required.
2. If required, limit access to specific trusted hosts only (router ACL/VLAN).
3. Ensure guest/anonymous share access is disabled.
4. Update firmware on the storage device (or retire if no updates available).
5. Block `139/445` from non-admin VLANs.

Verification:
- Re-scan `139/445` and validate only expected admin hosts can connect.

## Medium Priority

### 2) `[REDACTED_PRIVATE_IP]` ([REDACTED_DEVICE])
Observed:
- `80/tcp` and `443/tcp` open
- `http-title: [REDACTED_DEVICE]`
- TLS cert is device-local/self-issued (expected for local appliance)
- HTTPS response lacks HSTS header

Risk:
- Admin interface exposed broadly on LAN can be targeted by compromised LAN clients.

Actions:
1. Restrict access to [REDACTED_DEVICE] management UI to admin devices only.
2. Confirm latest firmware/software is installed.
3. Disable unnecessary remote/local API features if not needed.
4. Segment IoT/energy devices into a dedicated VLAN with restricted east-west access.

Verification:
- From non-admin VLAN/client, confirm `80/443` are blocked.

### 3) `[REDACTED_PRIVATE_IP]` (`8080/tcp` WebServer)
Observed:
- `8080/tcp` open (`lighttpd` previously, `Server: WebServer` in header)
- Returns `404 Not Found` with permissive CORS header (`Access-Control-Allow-Origin: *`)

Risk:
- Unknown web service on alternate admin port may expose management or API endpoints.

Actions:
1. Identify device owner/purpose for `[REDACTED_PRIVATE_IP]`.
2. Restrict `8080` to admin hosts only.
3. Require authentication for management endpoints.
4. Remove wildcard CORS unless strictly required.
5. Patch/upgrade service and underlying firmware.

Verification:
- Endpoint inventory confirms service purpose.
- External/non-admin clients cannot reach `8080`.

## Lower Priority / Monitoring

### `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]` (`80/tcp`)
Observed:
- HTTP service responds with `Nucleus Server Error` pages.

Action:
- Identify device/application and confirm expected exposure.
- Restrict if not intentionally user-facing on LAN.

### `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]`, `[REDACTED_PRIVATE_IP]` (`443/tcp`)
Observed:
- HTTPS listeners present.

Action:
- Verify ownership and patch level.
- Confirm strong auth and no default credentials.

### SSH hosts `[REDACTED_PRIVATE_IP]` and `[REDACTED_PRIVATE_IP]`
Observed:
- `[REDACTED_PRIVATE_IP]`: OpenSSH 10.2
- `[REDACTED_PRIVATE_IP]`: OpenSSH 8.5

Action:
- Prefer key-based auth only.
- Disable password auth and root login if not required.
- Upgrade older SSH versions where possible (`[REDACTED_PRIVATE_IP]`).

## Authenticated Follow-up (next step)
To complete true authenticated auditing, provide credentials/keys for in-scope hosts and run:
1. Authenticated SMB share/permissions review on `[REDACTED_PRIVATE_IP]`.
2. Authenticated web/app config review on `[REDACTED_PRIVATE_IP]` and `[REDACTED_PRIVATE_IP]`.
3. Patch inventory collection from device management interfaces.

## Evidence files
- `reports/arp-targeted-services.txt`
- `reports/vuln-smb-[REDACTED_PRIVATE_IP].txt`
- `reports/vuln-web-shortlist.txt`
- `reports/deep-[REDACTED_PRIVATE_IP]-smb.txt`
- `reports/deep-[REDACTED_PRIVATE_IP]-web.txt`
- `reports/deep-[REDACTED_PRIVATE_IP]-web8080.txt`
- `reports/ssh-hardening-check.txt`
