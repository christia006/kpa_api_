from fastapi import APIRouter, HTTPException
from db import get_db_connection

router = APIRouter()

@router.post("/api/forms/bogie-checksheet")
def create_bogie_checksheet(payload: dict):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        data = payload

        cur.execute("""
            INSERT INTO bogie_checksheet 
            (form_number, inspection_by, inspection_date, 
            bmbc_adjusting_tube, bmbc_cylinder_body, bmbc_piston_trunnion, bmbc_plunger_spring,
            bogie_axle_guide, bogie_frame_condition, bogie_bolster, bogie_bolster_suspension_bracket, bogie_lower_spring_seat,
            bogie_no, date_of_ioh, deficit_components, incoming_div_and_date, maker_year_built)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            data["formNumber"],
            data["inspectionBy"],
            data["inspectionDate"],
            data["bmbcChecksheet"]["adjustingTube"],
            data["bmbcChecksheet"]["cylinderBody"],
            data["bmbcChecksheet"]["pistonTrunnion"],
            data["bmbcChecksheet"]["plungerSpring"],
            data["bogieChecksheet"]["axleGuide"],
            data["bogieChecksheet"]["bogieFrameCondition"],
            data["bogieChecksheet"]["bolster"],
            data["bogieChecksheet"]["bolsterSuspensionBracket"],
            data["bogieChecksheet"]["lowerSpringSeat"],
            data["bogieDetails"]["bogieNo"],
            data["bogieDetails"]["dateOfIOH"],
            data["bogieDetails"]["deficitComponents"],
            data["bogieDetails"]["incomingDivAndDate"],
            data["bogieDetails"]["makerYearBuilt"]
        ))

        new_id = cur.fetchone()["id"]
        conn.commit()

        return {"status": "success", "data": {"id": new_id}}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
