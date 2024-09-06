import aiosqlite
from datetime import datetime

DB_NAME = 'tasks.db'

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                create_time TEXT,
                                start_time TEXT,
                                exec_time INTEGER,
                                status TEXT)''')
        await db.commit()

async def add_task_to_db():
    async with aiosqlite.connect(DB_NAME) as db:
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = await db.execute("INSERT INTO tasks (create_time, status) VALUES (?, ?)", (create_time, 'In Queue'))
        await db.commit()
        task_id = cursor.lastrowid
    return task_id

async def update_task_status(task_id, status, start_time=None, exec_time=None):
    async with aiosqlite.connect(DB_NAME) as db:
        if start_time:
            await db.execute("UPDATE tasks SET status=?, start_time=? WHERE id=?", (status, start_time, task_id))
        elif exec_time is not None:
            await db.execute("UPDATE tasks SET status=?, exec_time=? WHERE id=?", (status, exec_time, task_id))
        else:
            await db.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
        await db.commit()

async def get_task_status(task_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT create_time, start_time, exec_time, status FROM tasks WHERE id=?", (task_id,))
        task = await cursor.fetchone()
    return task

async def get_active_task_count():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Run'")
        count = (await cursor.fetchone())
        count = count[0]
    return count

async def get_next_task_in_queue():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT id FROM tasks WHERE status = 'In Queue' ORDER BY id LIMIT 1")
        task = await cursor.fetchone()
    return task
