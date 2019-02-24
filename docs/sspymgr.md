# SSPYMGR

sspymgr 现在采用 Flask（后端） + Vue（前端）的方式开发，Flask 提供基本页面和服务 API，Vue 前端负责界面渲染和数据的显示。前后端的通信完全采用 JSON 交互。

## 后端

后端程序主要基于 Flask 提供服务 API，还使用了 gevent 作为 WSGIServer 提供协程响应。保证服务端提供数据时不会由于某个路由执行时间较长导致其它路由也无法访问。

## 前端

前端是基于 Vue-cli 脚手架搭建的项目，用到了 bootstrap，vue-router，ant-design-vue，jquery 等库/框架。
