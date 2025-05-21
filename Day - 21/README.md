# EC2 CPU Monitor & Auto-Rebooter

This Python script monitors the **CPU utilization** of running EC2 instances using **Amazon CloudWatch**, and **automatically reboots** instances if the average CPU utilization exceeds a specified threshold (default is 90%) over a 5-minute period.

## 📋 Features

- Fetches all **running EC2 instances**
- Queries **CloudWatch** for average CPU usage over the last 5 minutes
- **Reboots** instances exceeding the CPU threshold
- **Dry-run mode** for safe testing
- Comprehensive **logging** and **error handling**
- Safety checks to only reboot **running** instances

---

## 🚀 Requirements

- Python 3.6+
- AWS CLI configured with appropriate credentials and permissions
- Python packages:
  - `boto3`

### IAM Permissions Required

Make sure the IAM user or role running this script has the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:RebootInstances",
        "cloudwatch:GetMetricStatistics"
      ],
      "Resource": "*"
    }
  ]
}
````

---

## 🛠 Installation

1. **Clone the repo** or download the script:

   ```bash
   git clone https://github.com/yourusername/ec2-cpu-rebooter.git
   cd ec2-cpu-rebooter
   ```

2. **Install dependencies:**

   ```bash
   pip install boto3
   ```

3. **Ensure AWS credentials are configured** using one of these methods:

   * `aws configure`
   * `~/.aws/credentials` file
   * Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)

---

## 🧠 How It Works

* The script calls `ec2:DescribeInstances` to find running instances.
* For each instance, it fetches the `CPUUtilization` metric from CloudWatch over the **last 5 minutes**.
* If the **average CPU utilization exceeds 90%**, the instance is rebooted (or simulated in dry-run mode).

---

## ⚙️ Configuration

You can modify the default values in the script:

| Variable         | Description                                     | Default     |
| ---------------- | ----------------------------------------------- | ----------- |
| `CPU_THRESHOLD`  | Max allowed average CPU usage (%) before reboot | `90.0`      |
| `PERIOD_MINUTES` | Monitoring window in minutes                    | `5`         |
| `REGION`         | AWS region                                      | `us-east-1` |

---

## 🧪 Usage

### Dry-Run Mode (Recommended First)

Simulates reboot without performing any real action:

```bash
python ec2_rebooter.py --dry-run
```

### Actual Execution (⚠️ Be Cautious)

Performs actual reboot of high-CPU instances:

```bash
python ec2_rebooter.py
```

---

## 📝 Example Log Output

```bash
2025-05-21 10:00:00 [INFO] Found 2 running instance(s).
2025-05-21 10:00:01 [INFO] Instance i-1234567890abcdef0 average CPU: 95.50%
2025-05-21 10:00:01 [WARNING] Instance i-1234567890abcdef0 exceeds CPU threshold: 95.50%
2025-05-21 10:00:01 [INFO] Dry-run confirmed. Instance i-1234567890abcdef0 can be rebooted.
2025-05-21 10:00:02 [INFO] Instance i-abcdef1234567890 average CPU: 45.30%
2025-05-21 10:00:02 [INFO] Instance i-abcdef1234567890 is within CPU limits.
```

---

## 🧼 Best Practices

* Always run in `--dry-run` mode first to ensure safe behavior.
* Use **CloudWatch Alarms** for persistent alerting alongside this script.
* Schedule the script to run periodically via **cron** or **CloudWatch Events**.

---

## 📦 Optional: Run with Cron

Edit your crontab:

```bash
crontab -e
```

Add an entry to check every 10 minutes:

```cron
*/10 * * * * /usr/bin/python3 /path/to/ec2_rebooter.py --dry-run >> /var/log/ec2_rebooter.log 2>&1
```

---

## 🧑‍💻 Contributing

Contributions are welcome! Fork the repository and submit a pull request.

---

## 🛡️ Disclaimer

This script modifies your EC2 instances. **Always test with `--dry-run`** and review logs before using in production.

---

## 📧 Contact

For questions or support, reach out via GitHub issues or email: `kunalwaghmare1207@gmail.com`

---


