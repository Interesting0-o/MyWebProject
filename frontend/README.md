# frontend

个人博客前端，基于 Vue 3、Vite 与 Vue Router。

## 页面

- `/` 首页与最新文章
- `/posts/:slug` 文章详情
- `/archive` 按年份归档
- `/tags` 标签列表
- `/tags/:tag` 标签下的文章
- `/about` 关于
- `/health` 后端连接测试（不在导航中显示）

## 数据

文章目前来自 `src/data/posts.js`，站点与作者信息在 `src/config/site.js` 中维护。接入后端后，可以将数据读取替换为 API 请求。

## 常用命令

```sh
yarn dev        # 开发服务器
yarn build      # 生产构建
yarn test:unit  # 单元测试
yarn test:e2e   # 端到端测试（首次需 npx playwright install）
yarn lint       # 代码检查
yarn format     # 格式化 src/
```
