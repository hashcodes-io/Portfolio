"""FastAPI wrapper exposing the IPAM operations"""
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .ipam import IPAM

app = FastAPI(title="ipnet-demo")
ipam = IPAM("ipam.db")


class PoolIn(BaseModel):
    cidr: str


class AllocationIn(BaseModel):
    cidr: Optional[str] = None
    meta: Optional[str] = None


@app.on_event("startup")
def startup_event():
    # ensure a default pool for quick demo
    ipam.add_pool("10.10.0.0/28")


@app.post("/pools", status_code=201)
def add_pool(pool: PoolIn):
    try:
        ipam.add_pool(pool.cidr)
        return {"ok": True, "cidr": pool.cidr}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/pools")
def get_pools():
    return {"pools": ipam.list_pools()}


@app.post("/allocate", status_code=201)
def allocate(req: AllocationIn):
    try:
        ip = ipam.allocate(req.cidr, req.meta)
        return {"ip": ip}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/release", status_code=200)
def release(ip: str):
    ok = ipam.release(ip)
    if not ok:
        raise HTTPException(status_code=404, detail="not found")
    return {"ok": True}


@app.get("/allocations")
def allocations():
    return {"allocations": ipam.list_allocations()}
