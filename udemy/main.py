from fastapi import FastAPI, HTTPException, status
from typing import Optional
from scalar_fastapi import get_scalar_api_reference
from pydantic import BaseModel

app = FastAPI(title="Udemy practice")


shipments = {
    12701:{
        "weight": 1.2,
        "content": "wooden table",
        "status":"in process"
    },
    12702:{
        "weight": 2.5,
        "content": "metal chair",
        "status":"shipped"
    },
    12703:{
        "weight": 0.8,
        "content": "plastic stool",
        "status":"delivered"
    },
    12704:{
        "weight": 3.0,
        "content": "glass vase",
        "status":"in process"
    },
    12705:{
        "weight": 1.8,
        "content": "ceramic plate",
        "status":"shipped"
    },
    12706:{
        "weight": 4.2,
        "content": "wooden cabinet",
        "status":"pending"
    }
}

class Shipment(BaseModel):
    weight: Optional[float] = None
    content: Optional[str] = None
    status: Optional[str] = None

@app.get("/")
async def home():
    return {
        "content":"this is the home page",
        "status":"active"
    }


@app.get("/shipments/latest")
async def get_latest_shipments():
    id = max(shipments.keys())
    return shipments[id]


@app.get("/all-shipments")
async def get_all_shipments()-> dict[int, dict[str, object]]:
    return shipments


@app.get("/shipment")
async def get_shipment(id: int | None = None)-> dict[str, object]:
    print("Received id:", id)
    if id is None:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")   
    return shipments[id]


@app.post("/shipment/add")
async def add_shipment(shipment: Shipment)-> dict[str, object]:
    
    if shipment.weight > 25:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weight exceeds the maximum limit of 25 kgs.")

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "weight": shipment.weight,
        "content": shipment.content,
        "status": shipment.status
    }
    return {"message": "Shipment added successfully.", "id": new_id}

@app.post("/shipment/update/{id}")
async def update_shipment(id: int, shipment: Shipment)-> dict[str, object]:

    if shipment.weight > 25:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weight exceeds the maximum limit of 25 kgs.")

    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    
    if shipment.weight is not None:
        shipments[id]["weight"] = shipment.weight
    if shipment.content is not None:
        shipments[id]["content"] = shipment.content
    if shipment.status is not None:
        shipments[id]["status"] = shipment.status
    return {"message": "Shipment updated successfully.", "updated_shipment": shipments[id]}

@app.get("/scaler", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        # Point Scalar to your existing OpenAPI document
        openapi_url=app.openapi_url,
        # Optional: Avoid CORS issues in the interactive client
        scalar_proxy_url="https://proxy.scalar.com",
        title="My Awesome API Documentation"
    )
