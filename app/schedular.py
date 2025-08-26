from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models.otp import Otp
from datetime import datetime,timezone


def delete_expired_otps():
    db = SessionLocal()

    try:
        print(f"NOW:{datetime.now(timezone.utc)}")
        expired_count = db.query(Otp).filter(Otp.expires_at < datetime.now(timezone.utc)).count()
        print(f"Expired OTPs found: {expired_count}")  # Debug: how many expired OTPs

        deleted_count = db.query(Otp).filter (Otp.expires_at < datetime.now(timezone.utc)).delete(synchronize_session=False)
        db.commit()
        
        if deleted_count:
            print(f"Deleted {deleted_count} expired Otps")
    
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_otps,"interval",minutes=30)
    scheduler.start()
    print("Scheduler started")
    return scheduler





