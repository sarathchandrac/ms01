from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel, get_redis_connection
from starlette.requests import Request

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# redis connection
redis = get_redis_connection(
    host="redis-12064.c264.ap-south-1-1.ec2.cloud.redislabs.com",
    port=12064,
    password="WARyaFvd5iIM4rnCDbH65WMLPuTWR876",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis


@app.post('/orders'):
async def create(request: Request):
    body = await request.json()
