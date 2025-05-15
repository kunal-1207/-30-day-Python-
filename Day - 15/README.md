# SSL Certificate Checker CLI Tool

## Overview

This project is a Command Line Interface (CLI) tool that checks SSL certificate expiration dates for a given hostname. It provides detailed information about the SSL certificate, including its validity period, issuer, and days remaining until expiration. This tool is particularly useful for monitoring SSL certificates for websites or services to ensure they remain valid.

### Focus Areas

* Sockets
* SSL
* CLI arguments parsing

### Example Usage:

```
python ssl_checker.py example.com --port 443 --verbose
```

---

## How It Works

### Importing Necessary Modules

```python
import ssl
import socket
import argparse
from datetime import datetime
```

* `ssl`: Provides access to SSL-related functions, such as creating SSL contexts and retrieving SSL certificates.
* `socket`: Enables networking capabilities, allowing connections to be made to servers.
* `argparse`: Handles command-line argument parsing to provide a flexible CLI interface.
* `datetime`: Used to work with dates and times, allowing us to calculate the number of days until a certificate expires.

### Function: get\_ssl\_certificate\_info

This function retrieves SSL certificate information for a specified hostname and port.

#### Parameters:

* `hostname`: The server to connect to.
* `port`: The port number (default is 443 for HTTPS).
* `timeout`: The timeout duration for the socket connection.

#### Key Steps:

* Creates a default SSL context using `ssl.create_default_context()`.
* Establishes a socket connection using `socket.create_connection()`.
* Wraps the socket with SSL using `context.wrap_socket()`.
* Retrieves the certificate using `getpeercert()`.
* Extracts the `notBefore` and `notAfter` dates and converts them to datetime objects.
* Calculates the remaining days until expiration and checks if the certificate is currently valid.

### Function: print\_certificate\_info

Displays SSL certificate information in a readable format.

#### Parameters:

* `info`: Dictionary containing certificate information.
* `verbose`: If `True`, additional details about the certificate are displayed.

### Function: main

Handles argument parsing and coordinates the execution of the program.

#### Key Steps:

* Defines CLI arguments using `argparse.ArgumentParser()`.
* Retrieves certificate information by calling `get_ssl_certificate_info()`.
* Displays the information using `print_certificate_info()`.
* Handles exceptions and error messages appropriately.

### Example Command Usage:

```
python ssl_checker.py example.com --port 443 --timeout 15 --verbose
```

---

## Error Handling

* Connection timeouts, refused connections, and other exceptions are handled gracefully, providing informative error messages to the user.

---

## Future Improvements

* Add support for checking multiple hosts simultaneously.
* Implement logging to a file for record-keeping.
* Include email notifications for impending SSL certificate expirations.

---

## License

This project is open source and available under the MIT License.
