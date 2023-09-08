import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

app = FastAPI()

class Category(Enum):
    CP = 'commercial_paper'
    DPC = 'deferred_payment_check'

class Transaction(BaseModel):
    id: int
    date: date
    instrument: Category
    amount: int
    maturity: int
    rate: float
    drawer: Optional[str]

transactions = {
    0: Transaction(id = 0, date = '2023-09-04', instrument = Category.CP, amount = 100000, maturity = 120, rate = 110, drawer = 'Firm 1'),
    1: Transaction(id = 1, date = '2023-09-04', instrument = Category.CP, amount = 12000, maturity = 95, rate = 150, drawer = 'Firm 2'),
    2: Transaction(id = 2, date = '2023-09-04', instrument = Category.DPC, amount = 230000, maturity = 17, rate= 120, drawer = 'Firm 2'),
}

@app.get('/')
def index():
    return {"Database of financial instruments (currently available)": transactions}

@app.get("/transactions/{id}")
def search_by_id(id: int):
    if id not in transactions:
        raise HTTPException(status_code=404, detail=f"Transaction with Id = {id} does not exist.")
    return transactions[id]

@app.post("/")
def add_transaction(transaction: Transaction):
    if transaction.id in transactions:
        HTTPException(status_code=400, detail=f"Transaction with Id = {transactions.id=} already exists.")
    transactions[transaction.id] = transaction
    return {"added": transaction}

@app.delete("/transactions/{id}")
def delete_transaction(id: int):
    if id not in transactions:
        raise HTTPException(status_code=404, detail=f"Transaction with Id = {id=} does not exist.")
    transaction = transactions.pop(id)
    return {"deleted": transaction}

@app.put("/transactions/{id}")
def update(
    id: int,
    date: date or None = None,
    amount: int or None = None,
    maturity: int or None = None,
    rate: int or None = None,
    drawer: str or None = None
):
    if id not in transactions:
        HTTPException(status_code=404, detail=f"Transaction with Id = {id=} does not exist.")
    if all(info is None for info in (date, amount, maturity, rate, drawer)):
        raise HTTPException(status_code=400, detail="No parameters provided for update.")
    transaction = transactions[id]
    if date is not None:
        transaction.date = date
    if amount is not None:
        transaction.amount = amount
    if maturity is not None:
        transaction.maturity = maturity
    if rate is not None:
        transaction.rate = rate
    if drawer is not None:
        transaction.drawer = drawer    

    return {"updated": transaction}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)