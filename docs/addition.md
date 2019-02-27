## configuration

if you did not set a file named `~/config.yaml`, the `config.py` will initiate default config file with following content:

```yaml
email:
  account: 'your@account.xx'
  password: 'your password'
  host: 'smtp host'
sspymgr:
  debugConfig: 
    enabled: false # true to override following config
    host: '127.0.0.1'
    port: 5050
    shadowsocks: false
  config:
    host: '0.0.0.0'
    port: 80
    shadowsocks: true
```

You should place your own smtp account, password and host in coressponding field.

If you want shadowsocks server listen over ipv4, keep everything under `sspymgr` unchanged, if ipv6 is enabled on your server machine, you can place the `sspymgr.config.host` with '::' to listen both ipv4 and ipv6 address.

```yaml
... # same before
sspymgr:
  config:
    host: '::'
    port: 80
    shadowsocks: true
```

If you want to start shadowsocks manually, set `sspymgr.config.shadowsocks` to false.

## Open port with firewall

Before you provide shadowsocks service, you should open port for clients to connect to shadowsocks server. If your vps uses firewall to prevent connections from other computer, you can use firewall-cmd to open port. For example:

```bash
firewall-cmd --permanent --zone=public --add-port=45000-45010/tcp
firewall-cmd --permanent --zone=public --add-port=45000-45010/udp

# reload firewall
firewall-cmd --realod
# list all port enabled
firewall-cmd --list-all
```

These commands are enough for me. You'd better to have a look at firewall command options if you want any other configurations

## Using PM2

For: Run sspymgr background on the server and start it whenever the server starts/restarts.

If you download the source code from the github, you could make it by PM2 which is developed by Node.js:

```
cd /path/to/sspymgr-src
pm2 start main.py --name=sspymgr --interpreter=python3
```

Or if you download the program from pip, then you can directly use sspymgr to start it, but we still need pm2 to start that script for better managerment, command is a little different but it's easy to typo:

```
pm2 start sspymgr
```

Then the scripts will run background with the server. Our target is to make it starts as the server if the server has ever been restarted. Use following command to save the running tasks in PM2 and execute them when server starts up:

```
pm2 save
pm2 startup
```
