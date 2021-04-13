from fastapi import APIRouter

index = APIRouter()


@index.get('/')
async def status():
    return "Live", 200
