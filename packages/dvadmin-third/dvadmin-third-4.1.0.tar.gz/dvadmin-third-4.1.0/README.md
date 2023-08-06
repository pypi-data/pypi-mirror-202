# dvadmin_third

#### 介绍
dvadmin-third 插件是dvadmin的一个第三方用户管理插件，支持微信、企业微信、钉钉、飞书、H5页面扫码登录，支持扩展微信、企业微信、钉钉、飞书等用户信息类，以及SSO单点登录等功能(部分功能开发中)。

## 功能支持项

- [ ] 扫码登录
  - [x] H5扫码登录
  - [x] 微信扫码登录
  - [x] 微信公众号扫码登录
  - [ ] 企业微信扫码登录
  - [ ] 钉钉扫码登录
  - [ ] 飞书扫码登录
  - [ ] 
  - [ ] 
- [ ] 支持用户扩展信息类(开发中)
  - [ ] 微信用户信息
  - [ ] 企业微信信息
  - [ ] 钉钉信息
  - [ ] 飞书信息
- [ ] SSO单点登录(开发中)



## 使用说明

安装前端 dvadmin-third-web 插件进行配合使用
```shell
npm install dvadmin-third-web
```

使用pip安装软件包：

```shell
pip install dvadmin-third
```

目录结构：<br>
```javascript
dvadmin-third
|   dvdadmin_third
|   |   fixtures // 初始化文件
|   |   |   __init__.py
|   |   |   init_menu.json
|   |   |   init_systemconfig.json
|   |   |   initialize.py
|   |   migrations
|   |   templates
|   |   |   dvadmin_third // uniapp项目目录
|   |   |   h5 // 登录样式静态页面目录（编译后的，不建议修改）
|   |   views
|   |   |   __init__.py
|   |   |   third_users.py
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   settings.py
|   |   urls.py
|   setup.py
```
<br><br>
### 方式一: 一键导入注册配置
在 application / settings.py 插件配置中下导入默认配置
```python
...
from dvadmin_third.settings import *
```
<br>

### 方式二: 手动配置(推荐)
在INSTALLED_APPS 中注册app（注意先后顺序）
```python
INSTALLED_APPS = [
    ...
    'dvadmin_third'
]
```

在 application / urls.py 中注册url地址

```python
urlpatterns = [
    ...
    path(r'api/dvadmin_third/', include('dvadmin_third.urls')),
]
```

如果没有系统redis，请启动redis并添加配置 (./conf/env.example.py 及 ./conf/env.py中添加如下配置)

```python
# redis 配置
REDIS_PASSWORD = '' # 如果没密码就为空
REDIS_HOST = '127.0.0.1'
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:6379'

```

在 application / settings.py 下添加配置

```python
...
CACHES = { # 配置缓存
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'{REDIS_URL}/1', # 库名可自选1~16
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
```

### 进行迁移及初始化

```shell
python3 manage.py makemigrations 
python3 manage.py migrate 
# 注意备份初始化信息
python3 manage.py init -y 
```

### 前端登录superadmin后配置appid等参数
微信公众号扫码登录配置
![](./wechat_official.png)
飞书扫码登录配置
![](./feishu.png)
钉钉扫码登录配置
![](./dingtalk.png)

### 扫码登录时序图（auth2协议通用）
![](./wx_official_sequence_chart.jpg)

## 开发注意
先了解上面的时序图<br>
扫码跳转相关的地址尽量用域名，在电脑里做本地域名解析（域名解析可以解析为任意ip）<br>
APP跳转不支持附带端口的操作（如127.0.0.1可以但127.0.0.1:80不可以；除非用的是域名而不是ip地址）<br>
跳转的本质就是使用用户APP端内置的浏览器来进行跳转到目标地址，所以开发中的后端服务都用80端口<br>
（微信扫码登录除外，其他所有的第三方扫码登录都是80或433端口）
### 配置本地域名解析
修改域名解析比如windows系统可以修改 C:\Windows\System32\drivers\etc\hosts 文件，使用记事本打开<br>
添加的代码格式是 （127.0.0.1 aaa.bbb.com）不能加端口,意思是把 aaa.bbb.com 域名解析到本地的 127.0.0.1 上<br>
