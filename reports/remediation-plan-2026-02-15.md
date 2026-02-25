# LAN Remediation Plan (2026-02-15)

## Scope
- Network: `192.168.0.0/24`
- Deep-focus hosts: `192.168.0.156`, `192.168.0.230`, `192.168.0.241`
- Supporting exposures from prior scan: `192.168.0.170`, `192.168.0.220`, `192.168.0.186`, `192.168.0.190`, `192.168.0.248`, `192.168.0.177`

## High Priority

### 1) `192.168.0.156` (SMB)
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

### 2) `192.168.0.230` (Tesla Powerwall)
Observed:
- `80/tcp` and `443/tcp` open
- `http-title: Tesla Powerwall`
- TLS cert is device-local/self-issued (expected for local appliance)
- HTTPS response lacks HSTS header

Risk:
- Admin interface exposed broadly on LAN can be targeted by compromised LAN clients.

Actions:
1. Restrict access to Powerwall management UI to admin devices only.
2. Confirm latest firmware/software is installed.
3. Disable unnecessary remote/local API features if not needed.
4. Segment IoT/energy devices into a dedicated VLAN with restricted east-west access.

Verification:
- From non-admin VLAN/client, confirm `80/443` are blocked.

### 3) `192.168.0.241` (`8080/tcp` WebServer)
Observed:
- `8080/tcp` open (`lighttpd` previously, `Server: WebServer` in header)
- Returns `404 Not Found` with permissive CORS header (`Access-Control-Allow-Origin: *`)

Risk:
- Unknown web service on alternate admin port may expose management or API endpoints.

Actions:
1. Identify device owner/purpose for `192.168.0.241`.
2. Restrict `8080` to admin hosts only.
3. Require authentication for management endpoints.
4. Remove wildcard CORS unless strictly required.
5. Patch/upgrade service and underlying firmware.

Verification:
- Endpoint inventory confirms service purpose.
- External/non-admin clients cannot reach `8080`.

## Lower Priority / Monitoring

### `192.168.0.170`, `192.168.0.220` (`80/tcp`)
Observed:
- HTTP service responds with `Nucleus Server Error` pages.

Action:
- Identify device/application and confirm expected exposure.
- Restrict if not intentionally user-facing on LAN.

### `192.168.0.186`, `192.168.0.190`, `192.168.0.248` (`443/tcp`)
Observed:
- HTTPS listeners present.

Action:
- Verify ownership and patch level.
- Confirm strong auth and no default credentials.

### SSH hosts `192.168.0.177` and `192.168.0.190`
Observed:
- `192.168.0.177`: OpenSSH 10.2
- `192.168.0.190`: OpenSSH 8.5

Action:
- Prefer key-based auth only.
- Disable password auth and root login if not required.
- Upgrade older SSH versions where possible (`192.168.0.190`).

## Authenticated Follow-up (next step)
To complete true authenticated auditing, provide credentials/keys for in-scope hosts and run:
1. Authenticated SMB share/permissions review on `192.168.0.156`.
2. Authenticated web/app config review on `192.168.0.230` and `192.168.0.241`.
3. Patch inventory collection from device management interfaces.

## Evidence files
- `reports/arp-targeted-services.txt`
- `reports/vuln-smb-192.168.0.156.txt`
- `reports/vuln-web-shortlist.txt`
- `reports/deep-192.168.0.156-smb.txt`
- `reports/deep-192.168.0.230-web.txt`
- `reports/deep-192.168.0.241-web8080.txt`
- `reports/ssh-hardening-check.txt`
