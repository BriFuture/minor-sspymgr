# Minor-sspymgr (sspymgr): Manager Written in Python

This Project is another version that is written with Python of [shadowsocks-manager](https://github.com/shadowsocks/shadowsocks-manager) which is based on Nodejs.  

The original purpose of this project is to enable the manager to run in a machine whose memory is not so sufficient. It is based on myself needs, because I found that it takes almost 100M of memories to run [Shadowsocks](https://github.com/shadowsocks/shadowsocks-manager) on my server whose memory is only 512M. It's a little expensive when running the server. Alternatively, you can keep only the ssmgr program running in background. 

It is a python-learning project for me. I learned a lot from [shadowsocks-manager](https://github.com/shadowsocks/shadowsocks-manager) which is written in JavaScript, then i make a more suitable program named minor-sspymgr for personal usage. The advantage of this application is that it may consume 50M memory while running, much less compared with shadowsocks-manager.

## How to use

It's simple to use sspymgr to deploy a website with shadowsocks service running backend, you can install it by pip / pip3:

```bash
pip install sspymgr
```

Note: sspymgr only supports python3.x.

Or you can download the source code from github if you got git:

1. git clone https://github.com/brifuture/minor-sspymgr.git
2. cd minor-sspymgr
3. python3 ./setup.py install

After installation, simply type `sspymgr` in console will start sspymgr which would launch a website at 80 port (or 5050 port when debug is enabled). You can see more command line arguments by typing `sspymgr -h`.

You may find some useful instructions in [addition.doc](./docs/addition.md). Or if you want to know more about how I make this website application, you may have a look on [about_sspymgr.md](./docs/about_sspymgr.md) although some parts may be out of date because it changed a lot as I developed the application.

## TODO List

- database
    * database lazy loading and creation, command line arguments option add `-c` or `--config` to set config file
- admin
    * setting subsystem optimizing
    * order subsystem details for confirm
- other
    * optional: data migration and database upgrade
    * plugin system optimize, all helper instances should be attached to app instance

## Thanks To Following Projects

-  Backend: flask and some extensions for flask such as flask_sqlalchemy, shedule
-  UI(frontend): vue, bootstrap, ant-design, ext.
-  Reference: shadowsocks-manager

## License

License is under [GPLv3](./license)
