import razorpay

RZP_KEY_ID = "rzp_test_TSRv08TUEjVcAE"
RZP_KEY_SECRET = "o0i4LBhluN3dr3KvZeJ8PGP4"

client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

try:
    print("Testing connection with Key ID:", RZP_KEY_ID)
    link = client.payment_link.create({
        "amount": 50000,
        "currency": "INR",
        "description": "API Test Link",
        "customer": {
            "name": "Test User",
            "email": "test@example.com",
            "contact": "+919876543210"
        }
    })
    print("\n✅ SUCCESS! Payment Link:", link.get("short_url"))
except razorpay.errors.BadRequestError as e:
    print("\n❌ BAD REQUEST (Parameters Issue):", e)
except razorpay.errors.SignatureVerificationError as e:
    print("\n❌ SIGNATURE/AUTH ERROR:", e)
except Exception as e:
    print("\n❌ RAW ERROR DETAILS:")
    print(repr(e))