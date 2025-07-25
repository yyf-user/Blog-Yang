from typing import Any, List, Dict, Optional
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from openai import AsyncOpenAI, OpenAI
from app.core.deps import get_optional_user
from app.models.user import User
import logging

# 设置日志
logger = logging.getLogger("chat_api")
logger.setLevel(logging.DEBUG)

router = APIRouter()

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-7a622434f8b24406a92fed8c419d966d"  # 实际部署时应使用环境变量
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 创建客户端
async_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


# 处理根路径的POST请求，重定向到/message端点
@router.post("")
async def chat_root(
    request: Request,
    current_user: Optional[User] = Depends(get_optional_user),
) -> Any:
    """
    处理根路径的请求，将其重定向到/message端点
    """
    # 解析请求体
    try:
        body = await request.json()
        messages = body.get("messages", [])
        
        if not messages:
            raise HTTPException(status_code=400, detail="消息列表不能为空")
        
        # 直接调用message端点的处理逻辑，不是函数本身
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
        )
        
        return {
            "message": response.choices[0].message.content,
            "role": response.choices[0].message.role,
        }
    except Exception as e:
        logger.error(f"处理聊天请求时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理请求失败: {str(e)}")


# 处理OPTIONS预检请求
@router.options("")
@router.options("/stream")
@router.options("/message")
async def options_chat():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


# 流式聊天端点
@router.post("/stream")
async def chat_stream(
    request: Request,
    current_user: Optional[User] = Depends(get_optional_user),  # 使用可选用户认证
) -> StreamingResponse:
    """
    与DeepSeek大模型进行流式对话
    """
    # 解析请求体
    body = await request.json()
    messages = body.get("messages", [])
    
    if not messages:
        raise HTTPException(status_code=400, detail="消息列表不能为空")
    
    logger.info(f"开始流式聊天请求，消息数: {len(messages)}")
    
    # 创建异步迭代器，将响应流式传输到客户端
    async def event_generator():
        try:
            logger.info("创建DeepSeek流式请求")
            stream = await async_client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=messages,
                stream=True,
            )
            
            logger.info("开始接收DeepSeek流式响应")
            
            # 用于积累字符的缓冲区
            buffer = ""
            
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    
                    if content:
                        buffer += content
                        
                        # 逐个字符输出，确保前端可以实现打字机效果
                        for char in buffer:
                            yield f"data: {char}\n\n"
                            # 每个字符之间添加小延迟，便于前端处理
                            await asyncio.sleep(0.01)
                        
                        # 清空缓冲区
                        buffer = ""
                    
                    # 如果是最后一个消息，发送完成事件
                    if chunk.choices[0].finish_reason:
                        logger.info(f"收到完成标志: {chunk.choices[0].finish_reason}")
                        yield f"event: finish\ndata: {chunk.choices[0].finish_reason}\n\n"
            
            # 确保剩余的缓冲区内容也被发送
            if buffer:
                for char in buffer:
                    yield f"data: {char}\n\n"
                    await asyncio.sleep(0.01)
            
            # 确保最后有一个空行，结束SSE
            logger.info("流式响应完成")
            yield "data: [DONE]\n\n"
        except Exception as e:
            # 发送错误事件
            logger.error(f"流式响应错误: {str(e)}")
            error_message = str(e)
            yield f"event: error\ndata: {error_message}\n\n"
    
    # 返回流式响应
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用Nginx缓冲
            "Access-Control-Allow-Origin": "*",  # 允许跨域请求
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Content-Type": "text/event-stream",  # 明确设置SSE内容类型
        },
    )


# 普通聊天端点（非流式）
@router.post("/message")
async def chat_message(
    messages: List[Dict[str, str]],
    current_user: Optional[User] = Depends(get_optional_user),  # 使用可选用户认证
) -> Any:
    """
    与DeepSeek大模型进行普通对话
    """
    try:
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
        )
        
        return {
            "message": response.choices[0].message.content,
            "role": response.choices[0].message.role,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"调用DeepSeek API失败: {str(e)}") 