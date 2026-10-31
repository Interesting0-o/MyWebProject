# mywebproject

Vue 3 + FastAPI 全栈个人博客。后端提供文章、标签与归档 API，启动时会自动建表并写入示例文章；前端目前仍使用本地模拟数据，后续可切换为 API 数据源。

## 技术栈

- 前端：Vue 3、Vite、Vue Router、Pinia
- 后端：FastAPI、SQLAlchemy、Pydantic Settings、Uvicorn
- 数据库：MySQL 8.4（Docker Compose 默认）
- 包管理：前端 Yarn，后端 uv

## 目录结构

```
.
├── backend/                 # FastAPI 后端
│   ├── src/mywebproject/
│   │   ├── api/             # 文章、标签、归档路由
│   │   ├── schema/          # Pydantic 请求/响应模型
│   │   ├── models.py        # SQLAlchemy 模型
│   │   ├── seed.py          # 示例数据播种逻辑
│   │   ├── seed_data.py     # 示例文章内容
│   │   ├── db.py            # 数据库引擎、会话与初始化
│   │   ├── config.py        # 环境配置
│   │   └── main.py          # 应用入口
│   ├── tests/               # 后端 API 测试
│   └── pyproject.toml
├── frontend/                # Vue 3 前端
│   └── src/
│       ├── components/      # 页头、页脚、文章列表等内容组件
│       ├── config/site.js   # 站点信息与作者资料
│       ├── data/posts.js    # 本地模拟文章数据
│       ├── views/           # 首页、文章、归档、标签、关于等页面
│       └── router/          # 前端路由
├── docker-compose.yaml
├── init.sql                 # MySQL 数据库初始化
├── .env.example             # 环境变量模板
└── readme.md
```

## 快速开始

### 方式一：Docker Compose（推荐）

```bash
cp .env.example .env
docker compose up --build
```

启动后：

- 前端：`http://localhost`
- 后端接口文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/api/health`

MySQL 首次初始化时会执行 `init.sql`，创建并使用 `mywebproject` 数据库，建立 `posts`、`tags`、`post_tags` 并写入示例文章。后端会等待数据库健康检查通过后再启动；如果文章表为空且 `SEED_DATA=true`，后端也会从 `seed_data.py` 补种。

需要重新播种数据时，删除数据库卷后重启：

```bash
docker compose down -v
docker compose up --build
```

### 方式二：本地运行

1. 准备 MySQL 数据库。可以直接使用 Docker 只启动数据库容器：

```bash
docker compose up -d db
```

`docker-compose.yaml` 已将 MySQL 暴露到本机 `3306` 端口。`.env.example` 中的 `DATABASE_URL` 默认指向 `127.0.0.1:3306`，复制后按需修改密码。

2. 启动后端：

```bash
cd backend
uv sync
uv run mywebproject
```

3. 启动前端：

```bash
cd frontend
yarn install
yarn dev
```

打开 `http://localhost:5173` 即可浏览博客。访问 `http://localhost:5173/health` 可以测试前后端连通性。开发服务器会将 `/api` 请求代理到 `http://127.0.0.1:8000`。

## 后端接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/posts` | 文章列表，支持 `tag`、`q`、`limit`、`offset` |
| GET | `/api/posts/{slug}` | 文章详情，包含结构化正文区块 |
| GET | `/api/tags` | 标签列表及每个标签的文章数 |
| GET | `/api/archive` | 按年份分组的文章归档 |
| GET | `/api/health` | 健康检查 |

示例：

```bash
curl 'http://127.0.0.1:8000/api/posts?tag=Vue'
curl 'http://127.0.0.1:8000/api/posts/vue-3-composition-refactor'
```

## 数据播种

- Docker 首次初始化时，MySQL 执行 `init.sql`，创建表结构并写入示例文章和标签。
- 应用启动时执行 `Base.metadata.create_all`，作为本地开发时的建表兜底。
- `SEED_DATA=true` 且文章表为空时，后端会从 `seed_data.py` 写入示例文章。
- 文章正文以 JSON 区块存储，标签通过多对多关系关联。
- `init.sql` 默认创建并使用 `mywebproject` 数据库，需要与 `.env` 的 `DATABASE_NAME` 保持一致；如改用其他库名，请同时修改 `init.sql` 顶部的 `CREATE DATABASE` 和 `USE`。
- 修改 `init.sql` 后，已有数据卷不会重新执行初始化脚本，需要执行 `docker compose down -v` 后重新启动。
- 生产环境建议设置 `SEED_DATA=false`，并在后续引入 Alembic 管理数据库迁移。

## 前端路由

| 路径 | 页面 |
| --- | --- |
| `/` | 首页与最新文章 |
| `/posts/:slug` | 文章详情 |
| `/archive` | 按年份归档 |
| `/tags` | 标签列表 |
| `/tags/:tag` | 标签下的文章 |
| `/about` | 关于 |
| `/health` | 后端连接测试（不在导航中显示） |

## 常用命令

```bash
# 前端
yarn build          # 生产构建
yarn test:unit      # 单元测试
yarn lint           # 代码检查

# 后端
uv run pytest -q                               # 后端测试
uv run uvicorn mywebproject.main:app --reload  # 热重载启动
```
