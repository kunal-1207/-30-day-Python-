# README - Deploy a Simple Python App via Ansible Playbook

## Challenge: Deploy a Simple Python App via Ansible Playbook

### Focus: Ansible Basics

---

## Objective:

The goal of this challenge is to deploy a simple Python application using an Ansible playbook. This will introduce you to the fundamentals of Ansible, including task definition, variable management, and command execution.

---

## Python Program Used:

The Python program to be deployed is a basic script that prints a message to the console.

**hello.py:**

```python
#!/usr/bin/env python3

def main():
    print("Hello from Day 17 Challenge!")


if __name__ == "__main__":
    main()
```

### Breakdown:

* `#!/usr/bin/env python3`: This line specifies the interpreter to run the script as a Python 3 program.
* `def main()`: Defines the main function that will be called.
* `print(...)`: Outputs the specified string to the console.
* `if __name__ == "__main__"`: Ensures that the `main()` function only runs when the script is executed directly, not when imported as a module.

---

## Ansible Playbook - deploy.yml:

**deploy.yml:**

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
        src: hello.py
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

### Breakdown:

* `- name: Deploy Python Application`: This defines the playbook's purpose.
* `hosts: localhost`: Specifies that the playbook will run locally.
* `connection: local`: Ensures that Ansible executes tasks locally without SSH.
* `vars`: Defines variables for use throughout the playbook.
* `tasks`: Specifies a list of tasks to be executed sequentially.
* `apt`: Ensures Python 3 is installed.
* `copy`: Copies the `hello.py` script to the specified destination path.
* `command`: Executes shell commands and registers their output.
* `debug`: Displays the registered output from the previous command.

---

## Output:

```
PLAY [Deploy Python Application] *****************************************************************************************

TASK [Gathering Facts] **************************************************************************************************
ok: [localhost]

TASK [Ensure Python is installed] ***************************************************************************************
ok: [localhost]

TASK [Copy Python script to destination] ********************************************************************************
changed: [localhost]

TASK [Check script syntax] **********************************************************************************************
changed: [localhost]

TASK [Execute the Python script] *****************************************************************************************
changed: [localhost]

TASK [Display script output] ********************************************************************************************
ok: [localhost] => {
    "script_output.stdout": "Hello from Day 17 Challenge!"
}

PLAY RECAP **************************************************************************************************************
localhost                  : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

---

## Pros and Cons of Running in WSL vs Windows:

### ✅ **Pros of Running in WSL:**

* Native Linux environment for better compatibility with Ansible.
* Easier to use Linux commands and package management (e.g., apt).
* Closer simulation to a production Linux server.

### ❌ **Cons of Running in WSL:**

* Requires setup of WSL and installation of Ubuntu or other Linux distributions.
* Potential networking issues and file path differences between Windows and WSL.

### ✅ **Pros of Running in Windows:**

* Native access to Windows paths and directories.
* No need to switch to WSL.

### ❌ **Cons of Running in Windows:**

* Ansible is primarily Linux-focused, requiring extra configuration.
* Package management with apt is not available natively in Windows.
* Compatibility issues with certain Linux commands and utilities.

---

## Steps to Execute the Program:

1. **Install Ansible:**

   * In WSL: `sudo apt update && sudo apt install ansible`

2. **Ensure Python 3 is Installed:**

   * `sudo apt install python3`

3. **Place `hello.py` in the Same Directory as `deploy.yml`**

4. **Run the Playbook:**

   * `ansible-playbook deploy.yml`

5. **Verify Output:**

   * Check the console for the output: `Hello from Day 17 Challenge!`

---

## Issues and Solutions:

* **Path Issues in WSL:**

  * The `~` path may differ in WSL; use absolute paths if necessary.

* **Permissions Issue:**

  * If permission is denied, ensure that the script is executable: `chmod +x hello.py`.

* **Ansible Not Found in Windows:**

  * Ensure that Ansible is installed and added to the PATH in both Windows and WSL.

---

Happy Coding! 🚀🚀🚀
