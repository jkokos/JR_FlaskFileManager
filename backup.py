
import os
import subprocess
from datetime import datetime

# Папка для резервных копий
os.makedirs("backups", exist_ok=True)

# Имя файла с датой и временем
date = datetime.now().strftime("%Y-%m-%d_%H%M%S")
filename = f"backup_{date}.sql"

backup_path = os.path.join("backups", filename)

# Команда резервного копирования
command = [
    "docker", "compose", "exec", "-T",
    "db", "pg_dump",
    "-U", os.getenv("DB_USER", "postgres"),
    os.getenv("DB_NAME", "documents_db")
]

# Сохраняем резервную копию
with open(backup_path, "wb") as file:
    subprocess.run(command, stdout=file, check=True)

print(f"Резервная копия создана: {backup_path}")
