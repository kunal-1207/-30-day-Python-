# AWS EC2 Auto-Tagger

**Identifies untagged or partially tagged EC2 instances and applies default tags (e.g., Environment, Owner) using boto3.**

---

## 📌 Problem Statement

Unmanaged AWS EC2 instances without proper tags lead to:
- **Untracked costs** across environments or teams.
- **Security and compliance gaps** due to unclear resource ownership.
- Difficulty enforcing governance policies.

This script ensures consistent tagging by automatically detecting and tagging EC2 instances that are missing required metadata.

---

## ✨ Features

- ✅ Lists EC2 instances with **no tags** or **missing required tags**.
- 🏷️ Applies **default tags** (customizable via command line).
- 🧪 **Dry-run mode** to preview changes without modifying anything.
- 🔐 Handles AWS API errors gracefully (e.g., permissions, throttling).
- ⚙️ Designed for **idempotency**—never duplicates existing tags.

---

## 🔧 Prerequisites

- Python 3.6+
- [`boto3`](https://pypi.org/project/boto3/)
- AWS credentials configured with sufficient permissions:
  - `ec2:DescribeInstances`
  - `ec2:CreateTags`

### Install boto3:

```bash
pip install boto3
````

Ensure your AWS CLI is configured:

```bash
aws configure
```

---

## 🚀 Usage

### Basic Command:

```bash
python auto_tag_ec2.py --region us-east-1 --dry-run
```

### With Custom Tags:

```bash
python auto_tag_ec2.py --region eu-west-1 --default-tags '{"Environment": "Prod", "Owner": "DevOps"}'
```

### Arguments

| Argument         | Description                                                                                               |
| ---------------- | --------------------------------------------------------------------------------------------------------- |
| `--region`       | **(Required)** AWS region to scan (e.g., `us-west-2`)                                                     |
| `--dry-run`      | Optional flag to preview tagging without applying changes                                                 |
| `--default-tags` | JSON string of tags to apply (default: `{"Environment": "Dev", "Owner": "DevOps", "AutoTagged": "True"}`) |

---

## 📋 Sample Output

### Dry-Run Mode:

```
[DRY-RUN] Would tag i-0123456789abcdef0 with: {'Owner': 'DevOps', 'AutoTagged': 'True'}
All instances are fully tagged.
```

### Actual Tagging:

```
Tagged i-0123456789abcdef0 with: {'Owner': 'DevOps', 'AutoTagged': 'True'}
Tagged i-0fedcba9876543210 with: {'Environment': 'Dev'}
```

---

## 🛠️ Troubleshooting

### Common Errors

* **`botocore.exceptions.NoCredentialsError`**
  → Ensure `aws configure` is run and credentials are valid.

* **`ClientError: UnauthorizedOperation`**
  → Check IAM permissions for `ec2:DescribeInstances` and `ec2:CreateTags`.

### Debug Tips

* Enable verbose logs with:

  ```bash
  AWS_DEBUG=1 python auto_tag_ec2.py --region us-east-1
  ```
* Use AWS CLI to verify permissions:

  ```bash
  aws ec2 describe-instances --region us-east-1
  ```

---

## ⚠️ Limitations

* Region-specific by default. Modify script to iterate over multiple regions if needed.
* Subject to AWS API rate limits; consider using exponential backoff for production scale.
* Tags are case-sensitive; ensure consistency in key naming.

---

## 🤝 Contributing & License

Contributions are welcome via pull requests or issues.

Licensed under the [MIT License](LICENSE).

---

*Built for infrastructure hygiene and tag governance at scale.* 🧹

```
