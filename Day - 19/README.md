# YAML to JSON Converter

This project provides a simple command-line utility to convert Kubernetes YAML configuration files to JSON format. It is particularly useful for developers working with Kubernetes manifests and configurations, allowing for easy conversion and validation.

## 🛠️ Features

* Convert a single YAML document to JSON.
* Convert multiple YAML documents into a JSON array.
* Specify output file or print JSON to the console.

## 📂 Project Structure

* `yaml_to_json.py`: The main Python script containing the conversion logic.
* `sample.yaml`: Example YAML file for testing.
* `README.md`: Project documentation and instructions.

## 🚀 Requirements

* Python 3.8 or higher
* Required Libraries:

  * `pyyaml`

Install the required libraries using:

```bash
pip install pyyaml
```

---

## 🔧 How to Run the Program

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Program

**Basic Usage:**

```bash
python yaml_to_json.py <input.yaml> [output.json]
```

**Examples:**

1. Convert and print JSON to console:

```bash
python yaml_to_json.py sample.yaml
```

2. Convert and save to a file:

```bash
python yaml_to_json.py sample.yaml output.json
```

---

## 🐞 Common Issues and Solutions

### 1. Error: `FileNotFoundError: [Errno 2] No such file or directory`

* Ensure that the input file path is correct and accessible.
* Verify the file exists using `ls` or `dir` command.

### 2. Error: `yaml.YAMLError`

* This occurs if the YAML file is improperly formatted.
* Validate the YAML file using tools like `yamllint` or `online YAML validators`.

### 3. Error: `ModuleNotFoundError: No module named 'yaml'`

* Ensure that the required libraries are installed using:

```bash
pip install pyyaml
```

---

## 📝 Code Overview

### `yaml_to_json.py`

* **`yaml_to_json()` Function:**

  * Reads the input YAML file.
  * Parses the YAML content using `yaml.safe_load_all()` to handle multiple documents.
  * Converts the YAML content to JSON using `json.dumps()`.
  * Writes to the output file (if provided) or prints to the console.

* **Error Handling:**

  * Handles file not found errors, YAML parsing errors, and other unexpected exceptions.

* **Command-Line Arguments:**

  * The script expects at least one argument (YAML file path).
  * Optionally, a second argument (output JSON file path) can be provided.

---

## ✅ Example YAML Input

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: nginx
      image: nginx:1.14.2
      ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

**Command:**

```bash
python yaml_to_json.py sample.yaml output.json
```

---

## 🛠️ Improvements and Future Enhancements

* Add logging for better error tracking.
* Implement unit tests to validate the conversion logic.
* Add support for nested directories and batch processing.

---

## 📄 License

This project is licensed under the MIT License.

---

Feel free to contribute or open issues for any bugs or enhancements.
