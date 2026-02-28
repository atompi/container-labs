## 部署 Apache Superset

1. 拉取 git 仓库

```
git clone --depth=1  https://github.com/apache/superset.git
cd superset
git fetch --depth=1 origin tag 6.0.0
git checkout 6.0.0
```

2. 拉取 docker 镜像

```
docker pull apachesuperset.docker.scarf.sh/apache/superset:6.0.0
docker pull postgres:16
docker pull redis:7
```

3. 修改 docker-compose-image-tag.yml 文件

- 末尾 volumes 修改为：

```
volumes:
  superset_home:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: $DATA_DIR_PATH/superset_home
  db_home:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: $DATA_DIR_PATH/db_home
  redis:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: $DATA_DIR_PATH/redis
```

4. 创建 docker/.env-local 文件

```
DEV_MODE=false
SUPERSET_ENV=production
DATABASE_PASSWORD= # openssl rand -hex 8
EXAMPLES_PASSWORD= # openssl rand -hex 8
POSTGRES_PASSWORD= # openssl rand -hex 8
FLASK_DEBUG=false
SUPERSET_LOAD_EXAMPLES=no # 不加载示例数据
SUPERSET_SECRET_KEY= #openssl rand -hex 32
```

5. 修改 docker/superset-websocket/config.json 文件

```
jwtSecret 字段填写任意字符串：openssl rand -hex 32
```

6. 创建 docker/pythonpath_dev/superset_config_docker.py

```
WEBDRIVER_BASEURL_USER_FRIENDLY = (
    f"https://superset.atompi.cc/{os.environ.get('SUPERSET_APP_ROOT', '/')}/"
)
```

7. 创建数据持久化目录

```
export DATA_DIR_PATH=/data/superset
mkdir -p $DATA_DIR_PATH/superset_home $DATA_DIR_PATH/db_home $DATA_DIR_PATH/redis
```

8. 启动 superset

```
docker-compose -f docker-compose-image-tag.yml up -d
```

## Tips

### docker compose 版本要求：>=2.24.0

### 默认超级管理员

- 用户名：admin
- 密码：admin

### 公开分享 chart

授予 Public 角色以下权限：

- can read Explore
- can read Chart
- can read ExploreFormDataRestApi
- can write ExploreFormDataRestApi
- datasource access [your_datasource]
