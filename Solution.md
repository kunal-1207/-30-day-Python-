## 🔰 Week 1: Python & DevOps Basics

### **Day 1** – Print all environment variables

```python
import os

for key, value in os.environ.items():
    print(f"{key} = {value}")

```

### **Day 2** – Find duplicates in a list

```python
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

```

### **Day 3** – Simple calculator

```python
def calculator():
    try:
        a = float(input("Enter first number: "))
        op = input("Enter operator (+ or -): ")
        b = float(input("Enter second number: "))
        if op == '+':
            print(f"Result: {a + b}")
        elif op == '-':
            print(f"Result: {a - b}")
        else:
            print("Invalid operator")
    except ValueError:
        print("Invalid input")

calculator()

```

### **Day 4** – Rename `.log` files

```python
import os

for file in os.listdir("."):
    if file.endswith(".log"):
        os.rename(file, file + ".bak")

```

### **Day 5** – Count 5xx Apache errors

```python
count = 0
with open("access.log") as f:
    for line in f:
        parts = line.split()
        if len(parts) > 8 and parts[8].startswith("5"):
            count += 1
print(f"5xx errors: {count}")

```

### **Day 6** – Compress old logs

```python
import os
import shutil
import datetime

cutoff = datetime.datetime.now() - datetime.timedelta(days=7)

for file in os.listdir("logs"):
    path = os.path.join("logs", file)
    if os.path.isfile(path):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        if mtime < cutoff:
            shutil.make_archive(path, 'zip', root_dir="logs", base_dir=file)
            os.remove(path)

```

### **Day 7** – CPU usage alert

```python
import psutil

cpu = psutil.cpu_percent(interval=1)
if cpu > 80:
    print(f"ALERT! High CPU usage: {cpu}%")
else:
    print(f"CPU OK: {cpu}%")

```

### **Day 8** – Tail a log file

```python
import time

with open("logfile.log", "r") as f:
    f.seek(0, os.SEEK_END)
    while True:
        line = f.readline()
        if line:
            print(line, end="")
        else:
            time.sleep(0.5)

```

### **Day 9** – Read JSON config

```python
import json

with open("config.json") as f:
    data = json.load(f)
    print(json.dumps(data, indent=4))

```

### **Day 10** – Retry decorator

```python
import time
import random

def retry(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Retry {i+1}: {e}")
                time.sleep(2)
        raise Exception("Failed after 3 retries")
    return wrapper

@retry
def flaky():
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return "Success"

print(flaky())

```
