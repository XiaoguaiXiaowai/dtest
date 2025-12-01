# 部署到 Ubuntu 24.04

- 部署目标：`/srv/dtest`，服务名：`dtest`，通过 `gunicorn + nginx + systemd`
- 需要具备 `python3`、`nginx`，如使用 MySQL 需安装 `mysql-server`

## 快速部署

- 将项目代码放到服务器路径 `/srv/dtest`
- 进入服务器执行：

```bash
sudo bash /srv/dtest/deploy/deploy.sh
```

## 手动部署

- 安装依赖：

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx mysql-server
```

- 创建虚拟环境并安装包：

```bash
python3 -m venv /srv/dtest/venv
/srv/dtest/venv/bin/pip install --upgrade pip
/srv/dtest/venv/bin/pip install django==5.2.7 gunicorn pymysql cryptography
```

- 迁移和收集静态：

```bash
cd /srv/dtest
/srv/dtest/venv/bin/python manage.py migrate
/srv/dtest/venv/bin/python manage.py collectstatic --noinput
```

- 配置 systemd：

将 `deploy/systemd/dtest.service` 放到 `/etc/systemd/system/dtest.service`：

```bash
sudo cp /srv/dtest/deploy/systemd/dtest.service /etc/systemd/system/dtest.service
sudo systemctl daemon-reload
sudo systemctl enable --now dtest
```

- 配置 Nginx：

将 `deploy/nginx/dtest.conf` 放到 `/etc/nginx/sites-available/dtest.conf` 并启用：

```bash
sudo cp /srv/dtest/deploy/nginx/dtest.conf /etc/nginx/sites-available/dtest.conf
sudo ln -sf /etc/nginx/sites-available/dtest.conf /etc/nginx/sites-enabled/dtest.conf
sudo nginx -t
sudo systemctl reload nginx
```

## 运行与排查

- 查看服务状态：

```bash
sudo systemctl status dtest
sudo journalctl -u dtest -f
```

- 首次启动报错常见处理：

- 数据库权限或不存在：在 MySQL 中创建 `cmdb` 数据库与 `cmdbuser` 用户，并授予权限。
- 主机名被拒绝：在 `mysite/settings.py` 中设置 `ALLOWED_HOSTS` 包含服务器域名或 IP。
- 静态文件未显示：确认已执行 `collectstatic`，且 Nginx `location /static/` 指向 `/srv/dtest/staticfiles/`。
 - MySQL 8 认证错误（需 `cryptography`）：在虚拟环境安装 `cryptography` 后重试：
   `sudo /srv/dtest/venv/bin/pip install cryptography`
   或将 MySQL 用户切换为 `mysql_native_password`：
   `ALTER USER 'cmdbuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin123';`

## 可选项

- 将 `server_name _;` 替换为实际域名或 IP
- 如需 HTTPS，使用 `certbot` 为 Nginx 配置证书
