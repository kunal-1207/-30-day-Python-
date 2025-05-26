# **Linux User Creation Automation Tool**  
**A Python script to automate user creation on Linux servers using `useradd` and `subprocess`.**  

---

## **📝 Table of Contents**  
1. [Features](#-features)  
2. [Prerequisites](#-prerequisites)  
3. [Installation & Usage](#-installation--usage)  
4. [Common Problems & Solutions](#-common-problems--solutions)  
5. [Security Considerations](#-security-considerations)  
6. [Future Improvements](#-future-improvements)  
7. [License](#-license)  

---

## **✨ Features**  
✅ **Automates Linux user creation** with `useradd`  
✅ Supports:  
   - Custom home directories (`-d`)  
   - Default shell selection (`-s`)  
   - Supplementary groups (`-g`)  
   - GECOS comment (`-c`)  
   - System account creation (`--system`)  
✅ **Secure password handling** (interactive prompt or CLI argument)  
✅ **Error handling** for user conflicts, permission issues  
✅ **Logging** (basic success/failure messages)  

---

## **⚙️ Prerequisites**  
- **Linux OS** (Ubuntu, Debian, CentOS, etc.)  
- **Python 3.6+**  
- **Sudo privileges** (to run `useradd` and `chpasswd`)  

---

## **📥 Installation & Usage**  

### **1. Download the Script**  
```bash
curl -O https://gist.githubusercontent.com/yourusername/scriptid/raw/create_user.py
chmod +x create_user.py
```

### **2. Run the Script**  

#### **Basic Usage (Prompts for Password)**
```bash
sudo python3 create_user.py username
```
- You will be asked to enter & confirm the password.  

#### **Advanced Usage (All Arguments)**
```bash
sudo python3 create_user.py username \
  -p "securepassword" \
  -s "/bin/bash" \
  -d "/home/username" \
  -g "sudo,developers" \
  -c "User Full Name" \
  --system
```
**Arguments:**  
| Flag | Description | Example |
|------|-------------|---------|
| `-p` | Password (avoid in logs) | `-p "Pass123!"` |
| `-s` | Shell (default: `/bin/bash`) | `-s "/bin/zsh"` |
| `-d` | Home directory | `-d "/custom/home"` |
| `-g` | Comma-separated groups | `-g "sudo,dev"` |
| `-c` | User description | `-c "Admin User"` |
| `--system` | Create system account | `--system` |

---

## **⚠️ Common Problems & Solutions**  

### **1. `username is not in the sudoers file`**  
❌ **Error:**  
```bash
sudo usermod -aG sudo username
```
**Solution:**  
- Run the command from an **already privileged account** (not the new user).  
- Alternatively, manually edit `/etc/sudoers`:  
  ```bash
  sudo visudo
  ```
  Add:  
  ```
  username ALL=(ALL:ALL) ALL
  ```

### **2. `useradd: Permission denied`**  
❌ **Error:**  
```bash
useradd: cannot lock /etc/passwd; try again later.
```
**Solution:**  
- Ensure script is run with `sudo`.  
- Check if another process is modifying users (e.g., `killall useradd`).  

### **3. `chpasswd: (user) pam_chauthtok() failed`**  
❌ **Error:** Password too weak or policy restrictions.  
**Solution:**  
- Use a stronger password.  
- Bypass policy (not recommended):  
  ```bash
  echo "username:password" | sudo chpasswd --crypt-method=SHA512
  ```

### **4. `Home directory not created`**  
❌ **Error:** Missing `/home/username`.  
**Solution:**  
- Manually create it:  
  ```bash
  sudo mkdir /home/username
  sudo chown username:username /home/username
  ```

---

## **🔒 Security Considerations**  
- **Avoid passing passwords in CLI** (use interactive mode).  
- **Use SSH keys** instead of passwords where possible.  
- **Restrict sudo access** for new users if not needed.  
- **Enable password aging**:  
  ```bash
  sudo chage -M 90 username  # Expires in 90 days
  ```

---

## **🚀 Future Improvements**  
- [ ] **Bulk user creation** from CSV  
- [ ] **Password strength validation**  
- [ ] **Email notifications** on user creation  
- [ ] **Logging** to `/var/log/user_management.log`  

---

## **📜 License**  
MIT License - Free for personal and commercial use.  

---

### **🎯 Summary**  
This script simplifies Linux user management while handling common pitfalls. Report issues [here](#).  

**Happy automating!** 🚀
