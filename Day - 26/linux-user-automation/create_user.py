# Challenge: Build a script to automate user creation on Linux servers.
# Focus: subprocess, useradd command
# Example Hint: sudo permissions required
#!/usr/bin/env python3

import subprocess
import getpass
import argparse
from typing import List, Optional

def create_linux_user(
    username: str,
    password: Optional[str] = None,
    shell: str = "/bin/bash",
    home_dir: Optional[str] = None,
    groups: Optional[List[str]] = None,
    system_account: bool = False,
    comment: Optional[str] = None
) -> bool:
    """
    Creates a user on a Linux system using the useradd command.
    
    Args:
        username: Name of the user to create
        password: Password for the new user (None to skip password setting)
        shell: Default shell for the user
        home_dir: Custom home directory (None for default)
        groups: List of supplementary groups
        system_account: Whether to create a system account
        comment: GECOS comment field (usually full name)
    
    Returns:
        bool: True if user creation succeeded, False otherwise
    """
    # Build the useradd command
    cmd = ["sudo", "useradd"]
    
    if system_account:
        cmd.append("--system")
    
    if home_dir:
        cmd.extend(["--home-dir", home_dir])
    else:
        cmd.extend(["--create-home"])
    
    if comment:
        cmd.extend(["--comment", comment])
    
    if groups:
        cmd.extend(["--groups", ",".join(groups)])
    
    cmd.extend(["--shell", shell])
    cmd.append(username)
    
    try:
        # Create the user
        subprocess.run(cmd, check=True)
        
        # Set password if provided
        if password:
            set_password_cmd = f"echo '{username}:{password}' | sudo chpasswd"
            subprocess.run(set_password_cmd, shell=True, check=True)
        
        print(f"User '{username}' created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create user '{username}': {e}")
        return False

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Linux User Creation Tool")
    parser.add_argument("username", help="Username to create")
    parser.add_argument("-p", "--password", help="User password (prompt if not provided)")
    parser.add_argument("-s", "--shell", default="/bin/bash", help="User shell")
    parser.add_argument("-d", "--home-dir", help="Custom home directory")
    parser.add_argument("-g", "--groups", help="Comma-separated list of supplementary groups")
    parser.add_argument("-c", "--comment", help="Comment/Full name for the user")
    parser.add_argument("--system", action="store_true", help="Create a system account")
    
    args = parser.parse_args()
    
    # Get password if not provided
    password = args.password
    if not password:
        password = getpass.getpass(f"Enter password for {args.username}: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Error: Passwords do not match!")
            return
    
    # Process groups
    groups = args.groups.split(",") if args.groups else None
    
    # Create the user
    success = create_linux_user(
        username=args.username,
        password=password,
        shell=args.shell,
        home_dir=args.home_dir,
        groups=groups,
        system_account=args.system,
        comment=args.comment
    )
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()

