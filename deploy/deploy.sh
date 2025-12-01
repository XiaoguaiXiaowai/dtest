#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/srv/dtest"
PORT="8001"
SERVICE_NAME="dtest"

sudo apt update
sudo apt install -y python3-venv python3-pip nginx mysql-server

sudo mkdir -p "$APP_DIR"

python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install django==5.2.7 gunicorn pymysql cryptography

cd "$APP_DIR"
"$APP_DIR/venv/bin/python" manage.py migrate
"$APP_DIR/venv/bin/python" manage.py collectstatic --noinput

sudo tee /etc/systemd/system/${SERVICE_NAME}.service >/dev/null <<'EOF'
[Unit]
Description=Django Gunicorn service for dtest
After=network.target
[Service]
Type=simple
WorkingDirectory=/srv/dtest
Environment=DJANGO_SETTINGS_MODULE=mysite.settings
ExecStart=/srv/dtest/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8001 mysite.wsgi:application
Restart=always
User=www-data
Group=www-data
[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/nginx/sites-available/${SERVICE_NAME}.conf >/dev/null <<'EOF'
server {
    listen 80;
    server_name _;
    access_log /var/log/nginx/dtest_access.log;
    error_log /var/log/nginx/dtest_error.log;
    location /static/ {
        alias /srv/dtest/staticfiles/;
        expires 7d;
        add_header Cache-Control "public, max-age=604800";
    }
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/${SERVICE_NAME}.conf /etc/nginx/sites-enabled/${SERVICE_NAME}.conf
sudo nginx -t
sudo systemctl daemon-reload
sudo systemctl enable --now ${SERVICE_NAME}
sudo systemctl reload nginx
