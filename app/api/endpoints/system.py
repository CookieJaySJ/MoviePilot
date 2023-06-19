import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.helper.progress import ProgressHelper

router = APIRouter()


@router.get("/progress/{process_type}", summary="实时进度")
async def get_progress(process_type: str):
    """
    实时获取处理进度，返回格式为SSE
    """
    progress = ProgressHelper()

    async def event_generator():
        while True:
            detail = progress.get(process_type)
            yield 'data: %s\n\n' % json.dumps(detail)
            await asyncio.sleep(0.2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
