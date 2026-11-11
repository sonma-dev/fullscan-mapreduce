import uvicorn
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

load_dotenv(CURRENT_DIR / ".env")

from server.application import create_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=int(os.getenv("PORT", "8001")),
        reload=False,
    )
