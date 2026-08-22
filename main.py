from fastapi import FastAPI, Request
from agent_engine import process_recovery
from database import log_audit, init_db

app = FastAPI(title="Razorpay Agentic Recovery Gateway")

@app.on_event("startup")
def startup():
    init_db()

@app.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    payload = await request.json()
    event = payload.get("event")
    
    if event == "payment.failed":
        payment_entity = payload["payload"]["payment"]["entity"]
        order_id = payment_entity.get("order_id") or payment_entity.get("id")
        amount = payment_entity.get("amount", 0) / 100.0
        error_desc = payment_entity.get("error_description", "PAYMENT_FAILED_GENERIC")
        
        result = process_recovery(
            order_id=order_id,
            amount=amount,
            failure_code=error_desc,
            attempts=1
        )
        
        log_audit(
            order_id=result["order_id"],
            original_amount=result["original_amount"],
            failure_reason=result["failure_reason"],
            ai_reasoning=result["ai_reasoning"],
            discount_pct=result["approved_discount_pct"],
            final_amount=result["final_amount"],
            payment_link=result["payment_link"],
            status=result["status"]
        )
        return {"status": "processed", "result": result}
        
    return {"status": "ignored_event"}