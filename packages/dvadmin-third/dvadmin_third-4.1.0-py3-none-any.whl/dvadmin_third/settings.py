import os

from application import settings

# ================================================= #
# ***************** 插件配置区开始 *******************
# ================================================= #
# 路由配置
plugins_url_patterns = [
    {"re_path": r'api/dvadmin_third/', "include": "dvadmin_third.urls"}
]
# app 配置
apps = ['dvadmin_third']
# ================================================= #
# ******************* 插件配置区结束 *****************
# ================================================= #
if not hasattr(settings, 'REDIS_URL'):
    raise Exception("请配置redis地址，否则第三方登录无法使用！")

if not hasattr(settings, 'CACHES'):
    _DEFAULT_CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f'{settings.REDIS_URL}/1',
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }
else:
    _DEFAULT_CACHES = settings.CACHES

# ********** 赋值到 settings 中 **********
settings.CACHES = _DEFAULT_CACHES
settings.INSTALLED_APPS += [app for app in apps if app not in settings.INSTALLED_APPS]
from pathlib import Path
# 添加前端模板
settings.TEMPLATES[0]["DIRS"].append(os.path.join(Path(__file__).resolve().parent, "templates"))
settings.STATICFILES_DIRS.append(os.path.join(Path(__file__).resolve().parent, "templates",  "h5", "static"))

# ********** 注册路由 **********
settings.PLUGINS_URL_PATTERNS += plugins_url_patterns
