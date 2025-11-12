import asyncio
from mangum import Mangum  # Add to requirements.txt
from main import sio_app  # Your Socket.IO-wrapped app

handler = Mangum(sio_app, lifespan="auto")

async def main_handler(event, context):
    return await handler(event, context)

# For sync compatibility (Vercel calls sync)
def handler(event, context):
    return asyncio.run(main_handler(event, context))
