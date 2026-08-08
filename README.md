# Mini RAG Backend

> 每天 1 小时、30 天公开构建的科研文档 RAG 后端

**当前进度：Day 3/30（约 10%）**

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

截至 Day 3，仓库代码和 Git 记录能够证明已完成：

- Python 项目初始化、虚拟环境与依赖文件配置。
- FastAPI 基础项目结构，以及 `app`、`services` Python 包。
- 使用 `.env` 加载 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`，并通过 `.gitignore` 排除 `.env`。
- `LLMService` 配置封装与配置完整性检查；尚未实现真实模型调用。
- `ChatRequest` 和 `ChatResponse` 基础 Pydantic 模型。
- `GET /`、`GET /health`、`POST /chat`、`GET /request-info` 四个接口。
- `/chat` 的基础输入处理：去除首尾空格、拒绝纯空白消息，并返回模拟回复。
- GET、POST、请求头、请求体、JSON 与常见 HTTP 状态码的学习和练习记录。

当前 Git 历史共有 3 次提交：

- `16bcff2`：初始化 FastAPI 项目。
- `659df8a`：完成 Day 3 代码更新。
- `b474b81`：加入 Day 1 至 Day 3 及月计划学习文档。

## 当前接口

| 请求方法 | 路径 | 作用 | 当前状态 |
| --- | --- | --- | --- |
| GET | `/` | 返回服务运行提示 | 已实现 |
| GET | `/health` | 返回服务状态，以及三项 LLM 配置是否齐全 | 已实现；只检查配置，不调用模型 |
| POST | `/chat` | 接收 `message` 并返回 `reply` | 已实现模拟回复；尚未调用真实 LLM |
| GET | `/request-info` | 读取可选的 `X-Client-Name` 请求头 | 已实现；未提供时返回 `unknown` |

`POST /chat` 当前请求示例：

```json
{
  "message": "什么是 RAG？"
}
```

当前响应是模拟结果：

```json
{
  "reply": "模拟大模型回复：你发送了「什么是 RAG？」"
}
```

纯空白 `message` 会返回 `400`；缺少字段或字段类型不符合要求时，由 FastAPI 和 Pydantic 返回请求校验错误。

## 技术栈

### 当前已使用

- Python：后端开发语言。
- FastAPI `0.141.1`：API 路由与接口文档。
- Uvicorn `0.52.1`：本地 ASGI 服务。
- Pydantic `2.13.4`：请求和响应数据模型。
- python-dotenv `1.2.2`：加载本地环境变量。
- HTTPX `0.28.1`：已列入依赖，但尚未用于真实 LLM API 调用。
- Git：版本记录与学习进度管理。

### 计划使用

- 真实大模型 API：生成回答。
- SQLite：持久化聊天记录。
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
│   ├── main.py                  # FastAPI 应用、数据模型与当前接口
│   └── services/
│       ├── __init__.py          # 标记 services 为 Python 包
│       └── llm_service.py       # 保存 LLM 配置并检查是否完整
├── docs/
│   ├── Day1.md                  # Day 1 项目初始化学习记录
│   ├── Day2.md                  # Day 2 Python 项目结构学习记录
│   ├── Day3.md                  # Day 3 HTTP 与 REST 学习记录
│   └── 月计划.md                 # 30 天整体学习计划
├── .gitignore                   # 排除环境变量、虚拟环境与缓存等文件
├── requirements.txt             # 当前 Python 依赖及固定版本
└── README.md                    # 项目说明与进度
```

`.venv`、`.env`、`__pycache__` 等本地或缓存内容未在目录树中展示。

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

## 环境变量

如需准备模型配置，可在项目根目录创建 `.env`，只填写自己的配置：

```env
LLM_API_KEY=
LLM_BASE_URL=
LLM_MODEL=
```

`.env` 已被 `.gitignore` 忽略，不应提交到 Git。不要把真实密钥写入代码、README 或公开学习记录。

目前 `/health` 只会检查以上三项是否都有值，`/chat` 仍然不会读取这些配置去调用真实模型。

## 30 天路线

| 周次 | 学习与实现内容 | 状态 |
| --- | --- | --- |
| 第 1 周 | Python 工程、Git、HTTP、FastAPI、Pydantic、LLM API | **进行中**：仅 Day 1 至 Day 3 有完成证据，真实 LLM API 尚未接入 |
| 第 2 周 | 聊天记录、SQLite、异常处理、`async` / `await` | **未开始** |
| 第 3 周 | PDF、Chunk、Embedding、FAISS、完整 RAG | **未开始** |
| 第 4 周 | 测试问题、参数调整、引用来源、README 和模拟面试 | **未开始**：README 会随开发持续更新，不代表本周其他任务已完成 |

当前可确认的里程碑：

- **Day 1 已完成**：项目初始化、虚拟环境、依赖、Git 与基础 FastAPI 结构。
- **Day 2 已完成**：Python 包与模块、绝对导入、`.env` 配置加载。
- **Day 3 已完成**：HTTP / REST 基础练习，以及当前四个接口和基础 Pydantic 模型。
- **Day 4 至 Day 30 尚未完成**。

## 学习时间安排

每天约 1 小时，按固定节奏推进：

- 5 分钟：复习前一天内容。
- 15 分钟：学习一个新概念。
- 35 分钟：编写和验证代码。
- 5 分钟：复盘并进行 Git 提交。

## 已知限制

- `/chat` 当前只返回模拟回复，没有调用真实大模型。
- 只有基础请求模型和空白消息检查，数据校验仍需继续完善。
- 尚无 SQLite 或其他数据库，聊天记录不会持久化。
- 尚未实现 PDF 上传、文本解析、Chunk、Embedding 和 FAISS 向量检索。
- 尚未形成完整 RAG 问答，也不会返回引用来源。
- 尚未建立效果评估流程。
- 尚未进行 Docker 容器化、部署或性能优化。

## 后续计划

下一步将继续完善 `/chat` 的数据校验，再通过 HTTPX 接入真实大模型 API。之后逐步实现 SQLite 聊天记录，并按 PDF 解析、Chunk、Embedding、FAISS 检索、带来源回答和效果评估的顺序完成 RAG 链路。

## 公开学习记录

代码、README 和学习记录会随着每天的实践持续更新：

[GitHub：lv-xiaoke/260804_mini-rag-backend](https://github.com/lv-xiaoke/260804_mini-rag-backend)

如果你也在学习 AI 应用开发，欢迎交流各自的实践过程和踩坑记录。
