# 30-day-Python
This is a 30 day python challenge

### Week 1–2: Python Fundamentals (Days 1–10)

---

| **Day** | **Challenge** | **Focus** | **Example Hint** |
| --- | --- | --- | --- |
| Day 1 | Print all environment variables. | `os.environ`, basics | Use `os.environ.items()` |
| Day 2 | Write a function to find duplicates in a list. | functions, loops | Use sets |
| Day 3 | Build a simple calculator (add, subtract). | CLI input, functions | Handle invalid inputs |
| Day 4 | Rename all `.log` files to `.log.bak` in a folder. | `os`, file handling | `os.listdir()`, `os.rename()` |
| Day 5 | Parse an Apache log to count 5xx errors. | string parsing, file reading | Read line-by-line |
| Day 6 | Create a function that compresses old logs (7+ days). | `shutil`, `datetime` | Use `shutil.make_archive` |
| Day 7 | Build a script that watches CPU usage and alerts if >80%. | `psutil` | Install with pip |
| Day 8 | Write a CLI tool to tail a log file in real-time. | file I/O, loops | Use `seek()` and `readlines()` |
| Day 9 | Read a JSON config file and print formatted output. | `json`, dictionaries | `json.load()` |
| Day 10 | Build a retry decorator for unreliable functions. | decorators, error handling | `try/except`, `time.sleep()` |

---

## Week 2–3: Real DevOps Tasks (Days 11–20)

| **Day** | **Challenge** | **Focus** | **Example Hint** |
| --- | --- | --- | --- |
| Day 11 | Write a backup script for `/var/log/` rotated daily. | file automation | Combine shutil + datetime |
| Day 12 | Fetch EC2 instance statuses using Boto3. | AWS SDK (boto3), API | Install boto3 |
| Day 13 | Script to create and destroy Docker containers. | docker-py SDK | Connect to local Docker daemon |
| Day 14 | Automatically rotate Nginx logs and archive old ones. | cron, script automation | Use `logrotate` configs or pure Python |
| Day 15 | Build a CLI tool to check SSL certificate expiration dates. | sockets, SSL | `ssl` module |
| Day 16 | Script to pull top alerts from Prometheus API. | APIs, metrics | Use `requests`, Prometheus queries |
| Day 17 | Deploy a simple Python app via Ansible playbook. | Ansible basics | Call Python script in YAML |
| Day 18 | Build a Flask API that triggers Jenkins jobs via API. | `Flask`, `requests`, Jenkins API | Authentication required |
| Day 19 | Write a parser to convert Kubernetes YAML configs into JSON. | YAML parsing | Use `pyyaml` |
| Day 20 | Auto-tag untagged AWS EC2 instances with default tags. | boto3 advanced use | EC2 `create_tags()` method |

---

## Week 3–4: Advanced Automation + DevOps Tools (Days 21–30)

| **Day** | **Challenge** | **Focus** | **Example Hint** |
| --- | --- | --- | --- |
| Day 21 | Script to reboot EC2 instances based on CPU thresholds. | boto3, monitoring | Use CloudWatch metrics API |
| Day 22 | Build a Python wrapper for Terraform apply/plan. | subprocess, IaC | `subprocess.run(["terraform", "apply"])` |
| Day 23 | Write a script to monitor Kubernetes pods and restart crashed ones. | K8s Python client | Install `kubernetes` lib |
| Day 24 | Auto-generate an Nginx config file from template variables. | string templating, Jinja2 | Use `jinja2` |
| Day 25 | Poll an S3 bucket and auto-sync new files locally. | boto3, file sync | `list_objects_v2()` |
| Day 26 | Build a script to automate user creation on Linux servers. | `subprocess`, `useradd` command | `sudo` permissions required |
| Day 27 | Build an alerting system that emails on service downtime. | SMTP, retries | Use `smtplib` |
| Day 28 | Script to pull running Docker containers and log their uptime. | docker-py, logs | `.containers.list()` |
| Day 29 | Automatically clean up old, untagged EBS volumes in AWS. | boto3 | Handle pagination carefully |
| Day 30 | Final Challenge: Build a CLI Tool to Manage Cloud Resources (EC2, S3, Monitoring). | combine all skills | Modular code, logging, error handling |
