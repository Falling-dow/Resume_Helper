# Resume Helper — 智能简历系统

基于 FastAPI + React 的智能简历平台：支持岗位爬取、AI 简历优化、用户认证，以及完整的容器化与 GitOps 部署流程。

## 快速开始

- 依赖：Docker >= 20, Docker Compose >= v2, Make
- 复制环境变量：
  - `cp backend/.env.example backend/.env`
  - `cp frontend/.env.example frontend/.env`
- 启动开发环境：`make dev`
- 查看日志：`make logs`
- 运行测试：`make test`

## 目录结构

详见 `Resume_Helper` 根目录的项目树。核心目录：
- `backend/` FastAPI 后端 + Celery 任务 + 爬虫/AI 模块
- `frontend/` React + Vite + TS 前端
- `nginx/` 反向代理与 TLS 终端
- `.github/workflows/` CI/CD 流水线

## 常用命令

- `make dev` 启动全栈（Postgres/Redis/ES/Backend/Frontend/Nginx）
- `make test` 后端/前端测试
- `make migrate` Alembic 数据库迁移
- `make build` 构建镜像
- `make deploy` 触发远端部署（需配置 GitHub Actions 与服务器）

## 环境变量

- 后端：`backend/.env.example`
- 前端：`frontend/.env.example`

## 部署

- 本地：`docker-compose up -d`
- 生产：参考 `.github/workflows/ci.yml` 及 `nginx/default.conf`，建议使用阿里云容器镜像服务与 ECS。

## 状态

当前仓库提供完整脚手架与最小可运行接口（/health、/api/v1/jobs 等）。你可以在此基础上，逐步补全业务逻辑、数据库模型、爬虫与 AI 能力。

