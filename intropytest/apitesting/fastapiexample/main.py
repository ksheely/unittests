from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Student Demo API")

# -------------------------
# Fake in-memory "database"
# -------------------------
items_db = [
    {"id": 1, "name": "Laptop", "price": 1200.0},
    {"id": 2, "name": "Mouse", "price": 25.5},
]


# -------------------------
# Pydantic Models
# Pydantic models are used to build easy-to-understand, 
# predictable data structures, with incorporated 
# type-checking and validation.
# -------------------------
class Item(BaseModel):
    id: int
    name: str
    price: float


class ItemCreate(BaseModel):
    name: str
    price: float


# -------------------------
# Root Endpoint
# -------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Demo!"}


# -------------------------
# GET with Query Parameters
# -------------------------
@app.get("/items")
def get_items(min_price: Optional[float] = Query(None)):
    if min_price:
        return [item for item in items_db if item["price"] >= min_price]
    return items_db


# -------------------------
# GET with Path Parameter
# -------------------------
@app.get("/items/{item_id}")
def get_item(item_id: int = Path(..., description="The ID of the item")):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# -------------------------
# POST - Create Item
# -------------------------
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    new_id = max(i["id"] for i in items_db) + 1 if items_db else 1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    return new_item


# -------------------------
# PUT - Update Item
# -------------------------
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: ItemCreate):
    for item in items_db:
        if item["id"] == item_id:
            item["name"] = updated_item.name
            item["price"] = updated_item.price
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# -------------------------
# DELETE - Remove Item
# -------------------------
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(i)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")