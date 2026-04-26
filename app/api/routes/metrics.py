from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.metrics_service import get_metrics
from app.core.dependencies import get_current_admin_user

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get(
    "/",
    summary="Get system metrics",
    description="Admin-only endpoint for retrieving aggregated ticket and technician metrics.",
)
def fetch_metrics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user),
):
    """
    Retrieve system-wide ticket metrics (Admin Only).

    This endpoint provides aggregated insights into the ticketing system,
    such as ticket volume, technician workload, and overall system activity.

    Access Control:
    - Requires a valid authenticated user
    - User must have admin privileges

    Dependencies:
    - get_db: Provides a database session for querying metrics
    - get_current_admin_user: Ensures only admins can access this endpoint

    Returns:
        dict: A structured response containing system metrics data
    """

    return get_metrics(db)
