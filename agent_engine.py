import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

DEFAULT_KEY_ID = "rzp_test_TSRv08TUEjVcAE"
DEFAULT_KEY_SECRET = "o0i4LBhluN3dr3KvZej8PGP4"

MAX_ALLOWED_DISCOUNT_PCT = 10.0
MIN_ORDER_VALUE_FOR_DISCOUNT = 500.0

def ai_evaluate_failure(order_id: str, amount: float, failure_code: str, attempts: int) -> dict:
    if attempts >= 3:
        return {
            "action": "ABANDON",
            "proposed_discount_pct": 0,
            "reasoning": "Maximum retry limit exceeded. Prevent customer fatigue."
        }
    
    if "TIMEOUT" in failure_code.upper() or "NETWORK" in failure_code.upper():
        return {
            "action": "RETRY_WITH_INCENTIVE",
            "proposed_discount_pct": 5.0,
            "reasoning": "Network timeout on checkout. Grant 5% recovery incentive."
        }
    elif "DECLINED" in failure_code.upper():
        return {
            "action": "RETRY_NO_INCENTIVE",
            "proposed_discount_pct": 0.0,
            "reasoning": "Payment declined by bank. Trigger alternate payment option."
        }
    else:
        return {
            "action": "RETRY_DEFAULT",
            "proposed_discount_pct": 0.0,
            "reasoning": "Standard cart drop-off. Send straightforward payment reminder link."
        }

def process_recovery(order_id: str, amount: float, failure_code: str, attempts: int = 1, key_id: str = None, key_secret: str = None):
    decision = ai_evaluate_failure(order_id, amount, failure_code, attempts)
    discount = decision.get("proposed_discount_pct", 0.0)
    
    if amount < MIN_ORDER_VALUE_FOR_DISCOUNT:
        discount = 0.0
    
    final_discount_pct = min(discount, MAX_ALLOWED_DISCOUNT_PCT)
    final_amount = amount * (1 - (final_discount_pct / 100.0))
    payment_link_url = "N/A"
    status = "REJECTED"

    # Prioritize supplied key -> OS env -> hardcoded working test key
    active_key_id = (key_id or os.getenv("RAZORPAY_KEY_ID") or DEFAULT_KEY_ID).strip()
    active_key_secret = (key_secret or os.getenv("RAZORPAY_KEY_SECRET") or DEFAULT_KEY_SECRET).strip()

    if decision["action"] != "ABANDON":
        try:
            client = razorpay.Client(auth=(active_key_id, active_key_secret))
            link_data = {
                "amount": int(final_amount * 100),
                "currency": "INR",
                "description": f"Recovery for Order #{order_id}",
                "customer": {
                    "name": "Test Customer",
                    "email": "customer@example.com",
                    "contact": "+919876543210"
                }
            }
            response = client.payment_link.create(link_data)
            payment_link_url = response.get("short_url", "http://test.link")
            status = "SUCCESS_LINK_GENERATED"
        except Exception as e:
            status = f"FAILED_API_ERROR: {str(e)}"
            payment_link_url = "FAILED"

    return {
        "order_id": order_id,
        "original_amount": amount,
        "failure_reason": failure_code,
        "ai_reasoning": decision["reasoning"],
        "approved_discount_pct": final_discount_pct,
        "final_amount": final_amount,
        "payment_link": payment_link_url,
        "status": status
    }
