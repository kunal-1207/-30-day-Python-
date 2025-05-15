# Day 15
# Challenge: Build a CLI tool to check SSL certificate expiration dates.
# Focus: sockets, SSL
# Example Hint:ssl module

import ssl
import socket
import argparse
from datetime import datetime

def get_ssl_certificate_info(hostname, port=443, timeout=10):
    context = ssl.create_default_context()
    
    try:
        # Set a timeout for the connection
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                if not cert:
                    raise ValueError("No certificate received from the server")
                
                # Parse certificate dates
                not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                
                current_time = datetime.utcnow()
                days_remaining = (not_after - current_time).days
                
                return {
                    'subject': dict(x[0] for x in cert['subject']),
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'not_before': not_before,
                    'not_after': not_after,
                    'days_remaining': days_remaining,
                    'is_valid': current_time >= not_before and current_time <= not_after,
                    'serial_number': cert.get('serialNumber', ''),
                    'version': cert.get('version', '')
                }
                
    except socket.timeout:
        raise ConnectionError(f"Connection to {hostname}:{port} timed out after {timeout} seconds")
    except ConnectionRefusedError:
        raise ConnectionError(f"Connection to {hostname}:{port} was refused")
    except Exception as e:
        raise ConnectionError(f"Error connecting to {hostname}:{port}: {str(e)}")

def print_certificate_info(info, verbose=False):
    print(f"\nSSL Certificate Information for {info['subject'].get('commonName', 'Unknown')}")
    print("=" * 60)
    
    print(f"Valid From: {info['not_before']}")
    print(f"Expires On: {info['not_after']}")
    print(f"Days Remaining: {info['days_remaining']}")
    print(f"Currently Valid: {'Yes' if info['is_valid'] else 'No'}")
    
    if verbose:
        print("\nDetails:")
        print(f"- Subject: {info['subject']}")
        print(f"- Issuer: {info['issuer']}")
        print(f"- Serial Number: {info['serial_number']}")
        print(f"- Version: {info['version']}")

def main():
    parser = argparse.ArgumentParser(
        description="Check SSL certificate expiration dates for a given host",
        epilog="Example: python ssl_checker.py example.com --port 443 --verbose"
    )
    parser.add_argument("hostname", help="The hostname to check")
    parser.add_argument("--port", type=int, default=443, help="Port number (default: 443)")
    parser.add_argument("--timeout", type=int, default=10, help="Connection timeout in seconds (default: 10)")
    parser.add_argument("--verbose", action="store_true", help="Show detailed certificate information")
    
    args = parser.parse_args()
    
    try:
        cert_info = get_ssl_certificate_info(args.hostname, args.port, args.timeout)
        print_certificate_info(cert_info, args.verbose)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
