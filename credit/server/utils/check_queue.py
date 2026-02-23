"""Check Celery task queue and inspect tasks"""
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Check queue length
queue_length = r.llen('celery')
print(f"📦 Tasks in queue: {queue_length}")

# List queued tasks
if queue_length > 0:
    tasks = r.lrange('celery', 0, -1)
    print(f"\n📋 Queued tasks:")
    for i, task in enumerate(tasks[:5], 1):
        print(f"  {i}. {task[:200]}...")

# Check active tasks
active_key = 'celery-task-meta-*'
active_keys = r.keys(active_key)
print(f"\n🏃 Active/completed tasks: {len(active_keys)}")

# Celery stats
print("\n📊 Redis info:")
print(f"  Connected clients: {r.info()['connected_clients']}")
print(f"  Total keys: {r.dbsize()}")
