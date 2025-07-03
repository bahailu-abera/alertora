import sys
from app.consumers import email_worker, sms_worker,\
    push_android_worker, push_ios_worker
from sqlalchemy.exc import IntegrityError, ProgrammingError

from app.extensions import Base, engine


WORKER_MAP = {
    "email": email_worker.run,
    "sms": sms_worker.run,
    "push_android": push_android_worker.run,
    "push_ios": push_ios_worker.run
}


def safe_create_all():
    try:
        Base.metadata.create_all(bind=engine)
        print("[INFO] Tables created or already exist.")
    except (IntegrityError, ProgrammingError) as e:
        print(f"[WARN] Skipping table creation due to error: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [worker_type]")
        print("Available workers: email, sms, push_android, push_ios")
        sys.exit(1)

    worker_type = sys.argv[1]

    if worker_type not in WORKER_MAP:
        print(f"Unknown worker type '{worker_type}'")
        sys.exit(1)

    print(f"Starting {worker_type} worker...")
    WORKER_MAP[worker_type]()


if __name__ == "__main__":
    safe_create_all()
    main()
