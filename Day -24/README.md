# 🛠️ NGINX Config Generator using Python and Jinja2

This project helps you **auto-generate an NGINX configuration file** using Python and [Jinja2](https://jinja.palletsprojects.com/) templating.

Even if you're new to Python, this guide will help you:
- Understand the code.
- Set up and run it successfully.
- Troubleshoot common issues.

---

## 📌 Why This Project?

Managing NGINX configs manually can be error-prone, especially when dealing with multiple servers or environments. This project makes it easy to **generate dynamic, reusable configurations** using variables.

---

## 📁 Files Included

```bash
.
├── nginx_template.j2        # Jinja2 template with placeholders
├── generate_nginx_config.py # Python script that renders the config
└── nginx_generated.conf     # Output file generated after running the script
````

---

## ✅ Prerequisites

Make sure Python is installed. You can check it with:

```bash
python --version
```

Install the required library:

```bash
pip install Jinja2
```

---

## 🚀 How to Run

1. **Download** the files.
2. Make sure `nginx_template.j2` and `generate_nginx_config.py` are in the same folder.
3. Run the Python script:

```bash
python generate_nginx_config.py
```

4. The script will generate `nginx_generated.conf` with the final config.

---

## 🔍 Template Overview (`nginx_template.j2`)

```jinja2
server {
    listen 80;
    server_name {{ server_name }};
    root {{ root_dir }};
    
    location / {
        proxy_pass http://{{ proxy_pass }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    {% if enable_ssl %}
    listen 443 ssl;
    ssl_certificate {{ ssl_certificate }};
    ssl_certificate_key {{ ssl_certificate_key }};
    {% endif %}
}
```

### 🔁 Explanation

* `{{ variable }}`: Jinja2 syntax to insert values.
* `{% if %}`: Conditional block to include SSL only if enabled.

---

## 🧠 Code Explanation (`generate_nginx_config.py`)

```python
from jinja2 import Environment, FileSystemLoader
```

* **Imports Jinja2's tools** to load and render templates.

```python
import os
```

* Built-in Python module to interact with the file system.

```python
template_dir = os.path.dirname(os.path.abspath(__file__))
```

* Gets the current directory where the script is located.

```python
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("nginx_template.j2")
```

* Sets up Jinja2 to load the `nginx_template.j2` file.

```python
config_data = {
    "server_name": "example.com",
    "root_dir": "/var/www/example",
    "proxy_pass": "127.0.0.1:5000",
    "enable_ssl": True,
    "ssl_certificate": "/etc/ssl/certs/example.crt",
    "ssl_certificate_key": "/etc/ssl/private/example.key"
}
```

* These values will replace placeholders in the template.

```python
rendered_config = template.render(config_data)
```

* Jinja2 renders the template with actual values.

```python
output_path = os.path.join(template_dir, "nginx_generated.conf")
with open(output_path, "w") as f:
    f.write(rendered_config)
```

* Writes the rendered text into `nginx_generated.conf`.

```python
print(f"NGINX config successfully generated: {output_path}")
```

* Shows confirmation with output file path.

---

## 🧩 Common Problems & Solutions

| Problem                                         | Cause                                 | Solution                                       |
| ----------------------------------------------- | ------------------------------------- | ---------------------------------------------- |
| `ModuleNotFoundError: No module named 'jinja2'` | Jinja2 not installed                  | Run `pip install Jinja2`                       |
| `TemplateNotFound: nginx_template.j2`           | Template file is missing or misplaced | Ensure the `.j2` file is in the same directory |
| No output file is created                       | Write permissions or logic error      | Run as administrator / check for script errors |
| SSL section missing in output                   | `enable_ssl` is False                 | Set `"enable_ssl": True` in `config_data`      |

---

## 🔧 Customization Tips

* You can load the `config_data` from a JSON/YAML file.
* Create multiple templates for different environments (e.g., dev, staging, prod).
* Add more Jinja2 blocks for complex logic.

---

## 📬 Want More?

Need help customizing this for your app or integrating with Docker/Ansible? Feel free to ask!

---

## 🧾 License

MIT License – feel free to use and modify.

```

