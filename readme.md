# MyWebProject

Vue 3 + FastAPI 全栈项目，前端首页提供一个后端连接测试按钮。

## 技术栈

- 前端：Vue 3、Vite、Vue Router
- 后端：FastAPI、Pydantic Settings、Uvicorn
- 包管理：前端 Yarn，后端 uv

## 目录结构

```
.
├── backend/                 # FastAPI 后端
│   ├── src/mypyproject/
│   │   ├── api/             # 路由
│   │   ├── resource/path.py # 基于 pathlib 的路径管理
│   │   ├── schema/          # Pydantic 模型
│   │   ├── config.py        # 环境配置
│   │   └── main.py          # 应用入口
│   └── pyproject.toml
├── frontend/                # Vue 3 前端
│   └── src/
│       ├── components/BackendTester.vue # 连接测试组件
│       └── views/HomeView.vue
├── .env.example             # 环境变量模板
└── readme.md
```

## 快速开始

### 1. 配置环境变量

```bash
cp .env.example .env
```

按需修改 `.env` 中的数据库地址、密码及服务端口。

### 2. 启动后端

```bash
cd backend
uv sync
uv run mypyproject
```

后端默认运行在 `http://127.0.0.1:8000`：

- 接口文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/api/health`

### 3. 启动前端

```bash
cd frontend
yarn install
yarn dev
```

打开 `http://localhost:5173`，点击“测试连接”按钮即可验证前后端连通性。开发服务器会将 `/api` 请求代理到 `http://127.0.0.1:8000`。

## 常用命令

```bash
# 前端
yarn build          # 生产构建
yarn test:unit      # 单元测试
yarn lint           # 代码检查

# 后端
uv run uvicorn mypyproject.main:app --reload  # 热重载启动
```
