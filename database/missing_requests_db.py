from motor.motor_asyncio import AsyncIOMotorClient
from info import OTHER_DB_URI  # Ensure correct URI import

client = AsyncIOMotorClient(OTHER_DB_URI)
db = client["your_database_name"]
missing_requests_col = db["missing_requests"]

async def add_missing_request(user_id, request_text):
    """Add a new missing request"""
    request_data = {
        "user_id": user_id,
        "request_text": request_text,
        "timestamp": datetime.datetime.utcnow()
    }
    await missing_requests_col.insert_one(request_data)

async def get_all_missing_requests():
    """Retrieve all missing requests"""
    return missing_requests_col.find()

async def delete_missing_request(user_id, request_text):
    """Delete a specific missing request"""
    await missing_requests_col.delete_one({"user_id": user_id, "request_text": request_text})
