from fastapi import FastAPI, Header, HTTPException , Response
from pydantic import BaseModel, Field

from app.services.llm_service import LLMService


app = FastAPI(
    title="Mini RAG Backend",
    description="一个用于学习 RAG 和 AI 应用开发的后端项目",
    version="0.1.0",
)

llm_service = LLMService()


class ChatRequest(BaseModel):
    """客户端发送的聊天请求。"""

    message: str = Field(
        min_length=1,
        max_length=1000,
        description="用户发送的消息",
    )


class ChatResponse(BaseModel):
    """服务器返回的聊天响应。"""

    reply: str


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "Mini RAG Backend is running"
    }


@app.get("/health")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "llm_configured": llm_service.is_configured(),
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, response: Response) -> ChatResponse:
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="message 不能只包含空格",
        )

    response.headers["Content-Type"] = "application/json; charset=utf-8"
    reply = llm_service.chat(message)

    return ChatResponse(reply=reply)


@app.get("/request-info")
async def request_info(
    x_client_name: str | None = Header(default=None),
) -> dict[str, str]:
    return {
        "client_name": x_client_name or "unknown"
    }