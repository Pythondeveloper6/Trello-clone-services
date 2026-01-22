services/tasks/
├── app/
│   ├── api/          # Route handlers (Blueprints)
│   ├── core/         # Global config & settings
│   ├── db/           # Database session & base models
│   ├── models/       # SQLAlchemy & Pydantic models
│   ├── services/     # Complex business logic
│   └── tasks/        # Celery background tasks
├── tests/            # Pytest suite
├── migrations/       # Alembic migration scripts
├── .env.example      # Template for environment variables
├── Dockerfile        # Container definition
├── main.py           # Application entry point
└── requirements.txt  # Python dependencies