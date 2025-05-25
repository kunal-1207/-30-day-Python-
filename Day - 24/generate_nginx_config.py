# Challenge: Auto-generate an Nginx config file from template variables.
# Focus: string templating, Jinja2
# Example Hints: Use jinja2

from jinja2 import Environment, FileSystemLoader
import os

# Step 1: Setup Jinja2 environment
template_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("nginx_template.j2")

# Step 2: Define configuration values
config_data = {
    "server_name": "example.com",
    "root_dir": "/var/www/example",
    "proxy_pass": "127.0.0.1:5000",
    "enable_ssl": True,
    "ssl_certificate": "/etc/ssl/certs/example.crt",
    "ssl_certificate_key": "/etc/ssl/private/example.key"
}

# Step 3: Render the template with values
rendered_config = template.render(config_data)

# Step 4: Save to output file
output_path = os.path.join(template_dir, "nginx_generated.conf")
with open(output_path, "w") as f:
    f.write(rendered_config)

print(f"NGINX config successfully generated: {output_path}")
