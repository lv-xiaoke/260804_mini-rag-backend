from fastapi import FastAPI, Header, HTTPException, Response

from app.database import get_messages, init_database, save_message
from app.models import ChatRequest, ChatResponse, Message
from app.services.llm_service import LLMService


app = FastAPI(
    title="Mini RAG Backend",
    description="一个用于学习 RAG 和 AI 应用开发的后端项目",
    version="0.1.0",
)

# print("开始创建 LLMService")
llm_service = LLMService()

# print("开始初始化数据库")
init_database()  # 启动时初始化数据库

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

    save_message(role="user", content=message)

    try:
        reply = await llm_service.chat(message)
    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    save_message(role="assistant", content=reply)

    return ChatResponse(reply=reply)

@app.get("/history", response_model=list[Message])
async def history(response: Response) -> list[Message]:
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return get_messages()


@app.get("/request-info")
async def request_info(
    x_client_name: str | None = Header(default=None),
) -> dict[str, str]:
    return {
        "client_name": x_client_name or "unknown"
    }

# print("main.py 加载完成")