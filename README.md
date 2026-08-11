# Mini RAG Backend

> 每天 1 小时、30 天公开构建的科研文档 RAG 后端

**当前进度：Day 13/30（约 43%）**

**项目状态：开发学习中 / Work in Progress**

## 项目介绍

这是一个从后端工程和 AI 应用开发基础开始、持续 30 天公开构建的学习项目。项目发起者是电子科技大学数学专业硕士生，接触过算法和深度学习，希望通过约 30 小时的实践，把科研文档 RAG 后端的核心链路真正跑通。

当前阶段优先理解并实现每个关键环节，不追求堆砌多模态、Agent、LangGraph 等复杂框架。项目既用于记录公开学习过程，也用于沉淀一个能够在面试中讲清设计与取舍的实践项目。

## 最终目标

下面是计划实现的目标架构，**不是当前已经完成的架构**：

```text
用户上传 PDF
    → 文本解析
    → Chunk
    → Embedding
    → FAISS
    → 相似内容检索
    → LLM
    → 回答与引用来源
```

完成主链路后，还将使用基础测试问题进行效果评估，并调整 Chunk、检索数量等参数。

## 当前已经实现

截至 Day 13，项目已经完成基础聊天后端和第二周的工程整理：

- 完成 Python 项目初始化、虚拟环境、依赖管理和 Git 配置。
- 使用 FastAPI 实现基础路由，并通过 Pydantic 校验聊天请求、响应和历史消息。
- 从 `.env` 加载 `LLM_API_KEY`、`LLM_BASE_URL` 和 `LLM_MODEL`，敏感配置不会进入 Git。
- 使用 `httpx.AsyncClient` 异步调用 DeepSeek Chat Completions 接口。
- 使用 SQLite 创建 `messages` 表，持久化用户问题和模型回答。
- 实现 `GET /history`，按消息写入顺序返回聊天记录。
- 处理纯空白输入、配置缺失、请求超时、连接失败、上游错误状态码和异常响应结构。
- 按接口层、数据模型、数据库层和模型服务层整理代码职责。

## 当前接口

| 请求方法 | 路径 | 作用 | 当前状态 |
| --- | --- | --- | --- |
| GET | `/` | 返回服务运行提示 | 已实现 |
| GET | `/health` | 返回服务状态，以及三项 LLM 配置是否齐全 | 已实现；只检查配置，不调用模型 |
| POST | `/chat` | 调用真实模型、保存消息并返回 `reply` | 已实现异步 LLM 调用和异常处理 |
| GET | `/history` | 返回按 `id` 升序排列的聊天历史 | 已实现；只查询本地 SQLite |
| GET | `/request-info` | 读取可选的 `X-Client-Name` 请求头 | 已实现；未提供时返回 `unknown` |

`POST /chat` 当前请求示例：

```json
{
  "message": "什么是 RAG？"
}
```

成功响应示例：

```json
{
  "reply": "RAG 是一种先检索外部知识，再结合检索结果生成回答的方法。"
}
```

一次成功的 `/chat` 请求会先保存 `user` 消息，异步调用模型，再保存 `assistant` 消息。纯空白 `message` 返回 `400`；缺少字段、空字符串或字段不符合要求时，由 FastAPI 和 Pydantic 返回 `422`。

`GET /history` 响应示例：

```json
[
  {
    "id": 1,
    "role": "user",
    "content": "什么是 RAG？",
    "created_at": "2026-08-11T01:30:00"
  },
  {
    "id": 2,
    "role": "assistant",
    "content": "RAG 是一种先检索外部知识，再结合检索结果生成回答的方法。",
    "created_at": "2026-08-11T01:30:02"
  }
]
```

## 技术栈

### 当前已使用

- Python：后端开发语言。
- FastAPI `0.141.1`：API 路由与接口文档。
- Uvicorn `0.52.1`：本地 ASGI 服务。
- Pydantic `2.13.4`：请求、响应和历史消息的数据模型与校验。
- python-dotenv `1.2.2`：加载本地环境变量。
- HTTPX `0.28.1`：异步调用 DeepSeek API。
- SQLite：使用 Python 标准库 `sqlite3` 保存和查询聊天记录。
- DeepSeek API：生成真实聊天回答。
- Git：版本记录与学习进度管理。

### 计划使用

- PDF 文本解析工具：提取科研文档文本，具体库待实现时确定。
- Embedding 模型：将问题和文本块转换为向量，具体模型待确定。
- FAISS：本地向量索引与相似度检索。
- 基础评估方法：分析检索与回答效果。
- Docker：作为后续容器化与部署练习，目前尚未开始。

## 项目结构

```text
mini-rag-backend/
├── app/
│   ├── __init__.py              # 标记 app 为 Python 包
│   ├── config.py                # 加载项目根目录下的 LLM 环境变量
│   ├── database.py              # SQLite 建表、消息保存与历史查询
│   ├── main.py                  # FastAPI 应用、路由与请求处理流程
│   ├── models.py                # ChatRequest、ChatResponse 和 Message
│   └── services/
│       ├── __init__.py          # 标记 services 为 Python 包
│       └── llm_service.py       # 异步调用 LLM 并处理上游异常
├── data/
│   └── chat.db                  # 本地 SQLite 数据，已被 Git 忽略
├── docs/
│   ├── Day1.md～Day13.md         # 每日学习计划与完成记录
│   ├── appendix/                # 学习过程中的补充笔记
│   ├── 定位自己.md               # 学习背景与能力定位
│   └── 月计划.md                 # 30 天整体学习计划
├── .gitignore                   # 排除环境变量、虚拟环境与缓存等文件
├── requirements.txt             # 当前 Python 依赖及固定版本
└── README.md                    # 项目说明与进度
```

`.venv`、`.env`、`__pycache__` 等本地或缓存内容未在目录树中展示。`data/chat.db` 只用于说明运行时位置，该文件不会提交到 Git。

## 本地运行

以下命令适用于 Windows PowerShell。代码使用了 Python 3.10 起支持的类型语法，建议使用 Python 3.10 或更高版本。

```powershell
git clone https://github.com/lv-xiaoke/260804_mini-rag-backend.git
cd 260804_mini-rag-backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

启动后访问：

- API 文档：<http://127.0.0.1:8000/docs>
- 服务根路径：<http://127.0.0.1:8000/>
- 健康检查：<http://127.0.0.1:8000/health>
- 聊天历史：<http://127.0.0.1:8000/history>

## 环境变量

如需准备模型配置，可在项目根目录创建 `.env`，只填写自己的配置：

```env
LLM_API_KEY=
LLM_BASE_URL=
LLM_MODEL=
```

`.env` 已被 `.gitignore` 忽略，不应提交到 Git。不要把真实密钥写入代码、README 或公开学习记录。

`/health` 只检查以上三项是否都有值，不会显示具体配置，也不会调用模型。`/chat` 会使用这些配置调用模型，因此启动服务前需要填写有效值。

## 30 天路线

| 周次 | 学习与实现内容 | 状态 |
| --- | --- | --- |
| 第 1 周 | Python 工程、Git、HTTP、FastAPI、Pydantic、LLM API | **已完成**：真实 `/chat` 链路已跑通 |
| 第 2 周 | 聊天记录、SQLite、异常处理、`async` / `await` | **已完成**：消息持久化、历史接口、异常处理和异步调用已实现 |
| 第 3 周 | PDF、Chunk、Embedding、FAISS、完整 RAG | **未开始** |
| 第 4 周 | 测试问题、参数调整、引用来源、README 和模拟面试 | **未开始**：README 会随开发持续更新，不代表本周其他任务已完成 |

当前可确认的里程碑：

- **第 1 周已完成**：项目初始化、HTTP、FastAPI、Pydantic 和真实 LLM API 调用。
- **第 2 周已完成**：SQLite 消息持久化、`/history`、异常处理、异步 HTTP 请求和代码职责整理。
- **下一步**：进入最小 RAG 阶段，先学习 Embedding。

## 学习时间安排

每天约 1 小时，按固定节奏推进：

- 5 分钟：复习前一天内容。
- 15 分钟：学习一个新概念。
- 35 分钟：编写和验证代码。
- 5 分钟：复盘并进行 Git 提交。

## 已知限制

- 目前只有一组全局聊天历史，还没有 `conversation_id` 和多会话管理。
- SQLite 操作仍使用同步的 `sqlite3`，尚未引入异步数据库或连接池。
- 模型调用失败时，已经保存的 `user` 消息会保留，但不会产生对应的 `assistant` 消息。
- 尚未实现 PDF 上传、文本解析、Chunk、Embedding 和 FAISS 向量检索。
- 尚未形成完整 RAG 问答，也不会返回引用来源。
- 尚未建立自动化测试和 RAG 效果评估流程。
- 尚未进行 Docker 容器化、部署或性能优化。

## 后续计划

下一步进入最小 RAG 阶段：先学习 Embedding，再按 PDF 文本解析、Chunk、FAISS、检索、连接大模型和效果评估的顺序完成整条链路。

## 公开学习记录

代码、README 和学习记录会随着每天的实践持续更新：

[GitHub：lv-xiaoke/260804_mini-rag-backend](https://github.com/lv-xiaoke/260804_mini-rag-backend)

如果你也在学习 AI 应用开发，欢迎交流各自的实践过程和踩坑记录。
