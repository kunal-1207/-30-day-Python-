# Python Deployment via Ansible

## Challenge: Deploy a simple Python app via Ansible playbook.

### Focus: Understanding Ansible basics and executing a Python script via YAML playbook.

---

## 📜 Program Overview

We will deploy a simple Python application using an Ansible playbook. The program consists of:

* A Python script that prints a simple message.
* An Ansible playbook (`deploy.yml`) that automates the deployment and execution of the Python script.

---

### Python Program (`hello.py`):

```python
#!/usr/bin/env python3

def main():
    print("Hello from Day 17 Challenge!")


if __name__ == "__main__":
    main()
```

#### Line-by-Line Breakdown:

* **Line 1:** The shebang (`#!/usr/bin/env python3`) ensures that the script uses Python 3 for execution.
* **Lines 3-4:** The `main()` function prints a simple message.
* **Lines 7-8:** The script checks if it is the main module being run and then calls the `main()` function.

---

### Ansible Playbook (`deploy.yml`):

```yaml
---
- name: Deploy Python Application
  hosts: localhost
  connection: local
  vars:
    dest_path: "~/hello.py"

  tasks:
    - name: Ensure Python is installed
      apt:
        name: python3
        state: present
      become: yes

    - name: Copy Python script to destination
      copy:
        src: Day_17.py
        dest: "{{ dest_path | expanduser }}"
        mode: '0755'

    - name: Check script syntax
      command: python3 -m py_compile "{{ dest_path | expanduser }}"
      register: syntax_check
      ignore_errors: yes

    - name: Execute the Python script
      command: python3 "{{ dest_path | expanduser }}"
      register: script_output

    - name: Display script output
      debug:
        var: script_output.stdout
```

#### Line-by-Line Breakdown:

* **Line 1:** YAML file start indicator (`---`).
* **Line 2:** Playbook name (`Deploy Python Application`).
* **Lines 3-4:** Hosts and connection type (`localhost` and `local`).
* **Lines 5-6:** Variable definition (`dest_path`).
* **Lines 8-13:** Ensure Python is installed using the `apt` module and set the state to `present`.
* **Lines 15-19:** Copy the Python script to the specified destination (`~/Day_17.py`).
* **Lines 21-24:** Check the syntax of the script using `py_compile`.
* **Lines 26-28:** Execute the Python script using the `command` module and capture the output.
* **Lines 30-32:** Display the script output using the `debug` module.

---

### ✅ Pros and Cons of Running the Program:

**In WSL (Windows Subsystem for Linux):**

* **Pros:**

  * Native Linux environment for Ansible, easier package management with `apt`.
  * No compatibility issues with Ansible modules.
  * Seamless integration with the Linux file system.

* **Cons:**

  * Requires setting up WSL and enabling Linux features on Windows.
  * Potential file path differences (`~` vs `C:\Users\`).

**In Windows:**

* **Pros:**

  * Can run directly using Python installed on Windows.
  * Easy access to Windows paths and native applications.

* **Cons:**

  * Ansible installation and configuration can be more complex.
  * Windows PowerShell may require specific module adjustments (e.g., `win_command` vs `command`).

---

### 🔥 Output:

Expected output when running the playbook:

```
PLAY [Deploy Python Application] **************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************************
ok: [localhost]

TASK [Ensure Python is installed] *************************************************************************************************
ok: [localhost]

TASK [Copy Python script to destination] ******************************************************************************************
changed: [localhost]

TASK [Check script syntax] ********************************************************************************************************
changed: [localhost]

TASK [Execute the Python script] **************************************************************************************************
changed: [localhost]

TASK [Display script output] ******************************************************************************************************
ok: [localhost] => {
    "script_output.stdout": "Hello from Day 17 Challenge!"
}

PLAY RECAP *************************************************************************************************************************
localhost                  : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

### 💻 Running the Program:

1. **Ensure Python 3 and Ansible are installed:**

   * WSL: `sudo apt install python3 ansible`
   * Windows: Follow the official Ansible documentation for Windows installation.

2. **Place the Python script (`hello.py`) and the playbook (`deploy.yml`) in the same directory.**

3. **Run the Playbook:**

   * Command: `ansible-playbook deploy.yml`

4. **Verify the Output:** Ensure that the message "Hello from Day 17 Challenge!" is displayed.

---

That concludes the deployment process using Ansible for a simple Python application.
