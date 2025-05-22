# Terraform Wrapper Script

This Python script is a wrapper for running `terraform init`, `plan`, and `apply` commands in a controlled and user-friendly way. It validates your setup, monitors execution with timeout protection, and provides useful error messages.

---

## 📁 Project Structure

```
project/
│
├── terraform_example/      # Folder with your .tf Terraform files
│   └── main.tf             # (Example Terraform config file)
│
└── terraform_wrapper.py    # This script
```

---

## ✅ Prerequisites

* Python 3.7+
* [Terraform](https://developer.hashicorp.com/terraform/downloads) installed and added to your system PATH
* A folder with valid Terraform `.tf` configuration files (`terraform_example/`)

---

## 🛠️ How to Run

1. **Install dependencies** (only standard Python libraries used — no extra install needed).
2. Place your `.tf` files inside the `terraform_example` directory.
3. Run the script:

   ```bash
   python terraform_wrapper.py
   ```
4. Follow on-screen instructions to execute `init`, `plan`, and `apply`.

---

## 🧠 What Does Each Line Do?

### Key Classes and Functions

#### `TerraformResult(NamedTuple)`

A structured way to return the results of running Terraform:

* `return_code`: Exit code from the command
* `stdout`, `stderr`: Output and errors
* `timed_out`: Whether the command timed out

#### `TerraformWrapper`

Main class to handle the Terraform operations:

* **`__init__`**: Sets working directory and timeout
* **`_validate_working_dir`**: Ensures Terraform files exist
* **`_validate_terraform_installed`**: Checks Terraform is installed
* **`_run_terraform_command`**: Executes Terraform commands with timeout protection
* **`init`, `plan`, `apply`**: Helper methods to run respective Terraform commands

#### Main Script Flow

```python
script_dir = os.path.dirname(os.path.abspath(__file__))
tf_dir = os.path.join(script_dir, "terraform_example")
```

→ Sets the Terraform directory path.

```python
tf = TerraformWrapper(tf_dir, timeout_minutes=10)
```

→ Initializes the wrapper with a 10-minute timeout.

```python
init_result = tf.init()
```

→ Runs `terraform init`.

```python
plan_result = tf.plan()
```

→ Runs `terraform plan` (skipping refresh and locking).

```python
apply_result = tf.apply()
```

→ Runs `terraform apply` if user confirms.

---

## 🚨 Common Problems & Solutions

| Problem                                | Cause                                                   | Solution                                                                                   |
| -------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| ❌ `Terraform not found in PATH`        | Terraform isn't installed or not in PATH                | Install Terraform and add it to your system environment PATH                               |
| ❌ `No Terraform files (.tf)`           | Directory has no `.tf` files                            | Add at least one `.tf` file to the `terraform_example` folder                              |
| ⏳ `Command timed out after 10 minutes` | - Network issue<br> - Large state<br> - AWS rate limits | Check internet, reduce resources in `.tf`, use smaller modules, or split into environments |
| ❌ `Permission denied`                  | IAM roles or credentials are wrong                      | Verify AWS credentials and IAM permissions for the resources you're deploying              |
| ❌ `apply` failed                       | Plan errors, missing variables                          | Recheck `.tf` logic, supply required variables with `-var-file` if needed                  |

---

## 📌 Notes

* **Timeout Feature**: Protects against stuck Terraform runs.
* **Real-time Output**: Prints logs while the process runs.
* **Safe Execution**: Only runs `apply` after successful `plan` and user confirmation.

---

## 📃 Example Terraform File (`main.tf`)

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-example-unique-bucket-name-123"
  acl    = "private"
}
```

---

## 🤝 Contributions

Feel free to fork and enhance this wrapper (e.g., add support for `destroy`, `output`, `import`, etc.).

---

## 📞 Support

For any issues, please file an issue or contact the maintainer.

