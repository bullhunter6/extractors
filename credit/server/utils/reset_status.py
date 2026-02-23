"""Reset all extractors to idle status"""
import asyncio
from datetime import datetime
from sqlalchemy import update
from server.core.database import AsyncSessionLocal, engine
from server.models import Extractor, ExtractorStatus


async def reset_all_extractors():
    """Reset all extractors to idle status and restart the interval countdown."""
    async with AsyncSessionLocal() as session:
        stmt = update(Extractor).values(
            status=ExtractorStatus.IDLE,
            current_task_id=None,
            last_run_at=datetime.utcnow()  # restart interval from now
        )
        await session.execute(stmt)
        await session.commit()
        print("✅ All extractors reset to IDLE status (interval countdown restarted)")


async def main():
    await reset_all_extractors()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
