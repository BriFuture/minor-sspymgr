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


