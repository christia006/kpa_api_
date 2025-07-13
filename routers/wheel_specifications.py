from fastapi import APIRouter, HTTPException
from db import get_db_connection

router = APIRouter()

@router.get("/api/forms/wheel-specifications")
def get_wheel_specifications():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                form_number, submitted_by, submitted_date, 
                condemning_dia, last_shop_issue_size, tread_diameter_new, wheel_gauge
            FROM wheel_specifications;
        """)
        rows = cur.fetchall()

        data = []
        for row in rows:
            data.append({
                "fields": {
                    "condemningDia": row["condemning_dia"],
                    "lastShopIssueSize": row["last_shop_issue_size"],
                    "treadDiameterNew": row["tread_diameter_new"],
                    "wheelGauge": row["wheel_gauge"]
                },
                "formNumber": row["form_number"],
                "submittedBy": row["submitted_by"],
                "submittedDate": str(row["submitted_date"])
            })

        return {
            "success": True,
            "message": "Filtered wheel specification forms fetched successfully.",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
