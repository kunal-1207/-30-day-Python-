# **Kubernetes Pod Auto-Restarter**  
**Automatically detect and restart failed pods in CrashLoopBackOff or Error state.**  

---

## **📌 Overview**  
This Python script monitors a specified Kubernetes namespace and automatically restarts pods stuck in `CrashLoopBackOff` or `Error` state. It uses the official Kubernetes Python client (`kubernetes`) to interact with the cluster.  

### **Key Features**  
✅ **Monitors** pods in a given namespace  
✅ **Detects** pods in `CrashLoopBackOff` or `Error` state  
✅ **Restarts** failed pods by deleting them (Kubernetes recreates them automatically)  
✅ **Logs** all actions for auditing  
✅ **Runs** both **locally** and **inside Kubernetes** as a deployment  

---

## **🚀 Quick Start**  

### **Prerequisites**  
✔ **Kubernetes Cluster** (Minikube, EKS, AKS, GKE, etc.)  
✔ **`kubectl`** configured (`kubectl get pods` should work)  
✔ **Python 3.6+** (`python3 --version`)  
✔ **pip** (`pip --version`)  

---

## **🔧 Installation & Setup**  

### **1️⃣ Install the Kubernetes Python Client**  
```bash
pip install kubernetes
```  

### **2️⃣ Save the Script**  
Save the script as `pod_restarter.py`:  
```bash
nano pod_restarter.py
```  
Paste the script content and save (`Ctrl+O`, `Enter`, `Ctrl+X`).  

### **3️⃣ Set Up RBAC Permissions**  
The script needs permissions to **list** and **delete** pods.  

#### **Option A: Apply RBAC Manually**  
1. Create `rbac.yaml`:  
   ```bash
   nano rbac.yaml
   ```  
2. Replace `<your-namespace>` and apply:  
   ```bash
   kubectl apply -f rbac.yaml
   ```  

#### **Option B: Use Admin Permissions (Testing Only!)**  
For quick testing (not recommended in production):  
```bash
kubectl create clusterrolebinding temp-admin --clusterrole=cluster-admin --serviceaccount=default:default
```  

---

## **🏃‍♂️ Running the Script**  

### **Option 1: Run Locally (Outside Cluster)**  
```bash
python3 pod_restarter.py --namespace <your-namespace> --interval 30
```  
- `--namespace`: Namespace to monitor (e.g., `default`).  
- `--interval`: Check interval in seconds (default: `60`).  

### **Option 2: Run Inside Kubernetes as a Deployment**  
1. Create `deployment.yaml`:  
   ```bash
   nano deployment.yaml
   ```  
2. Replace `<your-namespace>` and apply:  
   ```bash
   kubectl apply -f deployment.yaml
   ```  
3. Check logs:  
   ```bash
   kubectl logs -f deployment/pod-restarter -n <your-namespace>
   ```  

---

## **🛠 Troubleshooting (Common Errors & Fixes)**  

| **Error** | **Solution** |
|-----------|-------------|
| `Permission denied` | Ensure RBAC is applied (`kubectl get clusterrolebinding pod-restarter-role-binding`). |
| `No module named 'kubernetes'` | Run `pip install kubernetes`. |
| `Error connecting to Kubernetes` | Check if `kubectl` works (`kubectl cluster-info`). |
| Script doesn’t detect failing pods | Verify pod status: `kubectl get pods -n <namespace>`. |
| `CrashLoopBackOff` still occurring | Check pod logs (`kubectl logs <pod-name> -n <namespace>`). |
| `403 Forbidden` | Ensure ServiceAccount has correct permissions (check RBAC). |

---

## **🛑 Stopping the Script**  
- **If running locally**: Press `Ctrl+C`.  
- **If running in-cluster**:  
  ```bash
  kubectl delete deployment pod-restarter -n <your-namespace>
  ```  

---

## **📜 License**  
This project is open-source under the **MIT License**.  

---

## **📢 Support & Feedback**  
If you encounter issues or have suggestions, please [open an issue](https://github.com/your-repo/issues).  

🚀 **Happy Auto-Restarting!** 🚀
