from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from pydantic import BaseModel

from app.config import MailBody
from app.email_utils import send_mail
from fastapi.middleware.cors import CORSMiddleware
# Create FastAPI app with metadata
app = FastAPI(
    title="Email Service API",
    description="A simple API to send emails",
    version="1.0.0",
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify frontend URL: ["https://yourfrontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class SuccessResponse(BaseModel):
    message: str


@app.get("/", response_model=SuccessResponse)
def root() -> SuccessResponse:
    """Root endpoint to check if the API is running."""
    return SuccessResponse(message="Email Service API is running")


@app.post(
    "/send-email",
    response_model=SuccessResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {"description": "Email scheduled successfully"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Failed to schedule email"},
    },
)
async def schedule_mail(req: MailBody, tasks: BackgroundTasks) -> SuccessResponse:
    """
    Schedule an email to be sent in the background.

    Args:
        req: Email details including recipients, subject, and body
        tasks: FastAPI background tasks

    Returns:
        JSON response indicating the email has been scheduled

    Raises:
        HTTPException: If there's an error scheduling the email
    """
    try:
        # Convert Pydantic model to dict
        data = req.model_dump()

        # Add email sending task to background tasks
        tasks.add_task(send_mail, data)

        return SuccessResponse(message="Email has been scheduled")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to schedule email: {str(e)}",
        )
