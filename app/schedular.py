from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models.otp import Otp
from datetime import datetime,timedelta,timezone


def delete_expired_otps():
    db = SessionLocal()

    try:
        expiry_time = datetime.now(timezone.utc) - timedelta(hours=2)
        deleted_count = db.query(Otp).filter (Otp.created_at < expiry_time).delete(synchronize_session=False)
        db.commit()
        
        if deleted_count:
            print(f"Deleted {deleted_count} expired Otps")
    
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_otps,"interval",minutes=30)
    print("Scheduler started")
    return scheduler





