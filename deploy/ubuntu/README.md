# Ubuntu LAN deployment

This is a deployment template for one Ubuntu host on a trusted local network. It runs Django with Gunicorn bound to loopback and puts Nginx in front for HTTPS and static files. Applicant documents stay under `/var/lib/internship-portal/media` and must never be exposed as an Nginx alias.

## Before installing

The configured host address is `192.168.0.228`, with the short LAN hostname `dvsinternship`. Confirm the address is reserved and obtain a TLS certificate whose SAN includes both names; install its certificate/key at the paths in `nginx-internship-portal.conf.example`. Clients must resolve `dvsinternship` through LAN DNS or a hosts entry and trust the issuing internal CA. Do not expose this service through router port forwarding.

Use a current checkout of `main`. Install Python 3, `python3-venv`, Nginx, and UFW using Ubuntu's package manager. Create a non-login service account named `internship-portal` and create `/opt/internship-portal` plus `/var/lib/internship-portal/media`, owned by that account. Install the app checkout and its virtual environment in `/opt/internship-portal`.

## Configure the app

1. Create `/etc/internship-portal.env` from `internship-portal.env.example`. Generate a unique secret with `python3 -c 'import secrets; print(secrets.token_urlsafe(64))'`. Confirm `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` list the exact hostname/IP users will use. Keep this file readable only by root and the service manager.
2. Install Python dependencies in the app venv: `python -m pip install -r requirements.txt`.
3. As the service account, run `python manage.py migrate` and `python manage.py collectstatic --noinput`. Create the first administrator with `python manage.py createsuperuser`.
4. Copy `internship-portal.service` to `/etc/systemd/system/`, then run `sudo systemctl daemon-reload`, `sudo systemctl enable --now internship-portal`, and inspect `sudo systemctl status internship-portal`.
5. Copy `nginx-internship-portal.conf.example` to `/etc/nginx/sites-available/internship-portal`, replace its hostname and certificate paths, enable it under `sites-enabled`, check with `sudo nginx -t`, then reload Nginx.
6. For the supplied server address `192.168.0.228/24`, allow HTTP-to-HTTPS redirect and HTTPS only from `192.168.0.0/24` with UFW:

   ```bash
   sudo ufw allow from 192.168.0.0/24 to any port 80 proto tcp
   sudo ufw allow from 192.168.0.0/24 to any port 443 proto tcp
   ```

   Preserve the existing SSH rule before enabling or changing UFW on a remotely managed server. Do not open port 8000 to the LAN; Gunicorn listens on loopback only.
7. From a second LAN device, open `https://<lan-hostname>/`. Verify the certificate, login, static styling, application upload, and owner/staff-only document download.

After HTTPS is working and clients trust the certificate, set `SECURE_HSTS_SECONDS=31536000` and restart the service. Run `python manage.py check --deploy` with the production environment and resolve the remaining warnings before relying on the system.

## Operations

Back up `/var/lib/internship-portal/db.sqlite3` and `/var/lib/internship-portal/media/` together, and test a restore. Keep the host patched, restrict administrator accounts, and monitor `journalctl -u internship-portal` and Nginx logs. SQLite is suitable only for a small, low-write single-host workload; plan PostgreSQL if concurrent application writes grow.

This template does not install packages, configure UFW, create certificates, or modify systemd/Nginx on the host. Replace all example hostnames, paths, and LAN details before applying it.
