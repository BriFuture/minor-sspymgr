## Shadowsocks Controller

For convenience, `minor-sspy-mgr` assumes that you have only one vps to run shadowsocks server and you have to run minor-sspy-mgr on the same machine. So you have no need to balance your multiple servers flow. Current version does not support multiple server running in different machine, if you do need to balance servers flow, please consider using [shadowsocks-manager](https://github.com/shadowsocks/shadowsocks-manager) instead.

I used to consider integrating shadowsocks-py into this website application. But it may be more complicated if something went wrong with the web application. I can not promise that when website occurs fatal error, the shadowsocks service is still available if it is runned in the same progress with web application. So the shadowsocks service has to be started manually by manager himself.

### Shadowsocks adapter

Shadowsocks adapter is used for communicate with shadowsocks server. It will send user addition, user deletion command to shadowsocks server and recieve statistics infomation from the server.

The statsistical thread should run with the running thread with shadowsocks server, or it may get wrong statistic data.