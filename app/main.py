from fastapi import FastAPI

from app.services.llm_service import LLMService

app = FastAPI(
    title="Mini RAG Backend",
    description="一个用于学习RAG和AI应用开发的后端项目",
    version="0.1.0",
)
# 创建了一个 FastAPI 应用对象，并赋值给变量 `app`。这个对象是整个应用的核心，负责处理请求、路由、响应等功能。
# title、description 和 version 这些信息主要会显示在 FastAPI 自动生成的接口文档中
# 运行项目以后，可以打开：http://127.0.0.1:8000/docs ,你会看到项目名称、描述和接口列表。

llm_service = LLMService()


# 这叫作装饰器。它的意思是：当用户使用 GET 请求访问 / 时，执行下面的 root() 函数。
# 假设服务器地址是：http://127.0.0.1:8000 那么访问：http://127.0.0.1:8000/ 就会执行 root()。
@app.get("/")
async def root() -> dict[str, str]:
    # 这是定义一个异步函数。async 的详细原理后面学习异步编程时再深入。
    return {
        "message":"Mini RAG Backend is running"
    }

# 定义健康检查接口 /health 当用户访问：http://127.0.0.1:8000/health FastAPI 就会执行： health()
@app.get("/health")
async def health() -> dict[str, str | bool ]:
    return {
        "status":"ok",
        "llm_configured":llm_service.is_configured(),
    }