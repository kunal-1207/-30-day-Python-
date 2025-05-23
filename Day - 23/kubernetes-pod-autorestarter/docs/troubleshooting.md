Here’s a comprehensive `troubleshooting.md` guide for your **Kubernetes Pod Auto-Restarter** project:

---

# **🔧 Troubleshooting Guide**  
Common issues and solutions for the Kubernetes Pod Auto-Restarter.  

---

## **🚨 Common Errors & Fixes**  

### **1️⃣ Permission Denied (RBAC Issues)**  
**Error:**  
```bash
ERROR - Failed to list pods: (403) Reason: Forbidden
```  
**Solution:**  
- Verify RBAC is applied:  
  ```bash
  kubectl get clusterrolebinding pod-restarter-role-binding
  ```  
- Reapply RBAC if missing:  
  ```bash
  kubectl apply -f deployments/rbac.yaml
  ```  
- For testing, grant temporary admin rights (**not for production**):  
  ```bash
  kubectl create clusterrolebinding temp-admin --clusterrole=cluster-admin --serviceaccount=default:default
  ```  

---

### **2️⃣ Python Dependency Issues**  
**Error:**  
```bash
ModuleNotFoundError: No module named 'kubernetes'
```  
**Solution:**  
- Install dependencies:  
  ```bash
  pip install -r requirements.txt
  ```  
- If using a virtual environment:  
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows
  pip install kubernetes
  ```  

---

### **3️⃣ Kubernetes Connection Failures**  
**Error:**  
```bash
ERROR - Could not configure kubernetes python client
```  
**Solution:**  
- Ensure `kubectl` works first:  
  ```bash
  kubectl cluster-info
  ```  
- If running **locally**, load kubeconfig explicitly:  
  ```python
  config.load_kube_config()  # Add this to the script for debugging
  ```  
- For **in-cluster** runs, verify the ServiceAccount exists:  
  ```bash
  kubectl get serviceaccount pod-restarter -n <namespace>
  ```  

---

### **4️⃣ Script Not Detecting Failed Pods**  
**Symptom:**  
- The script logs `No failed pods found`, but some pods are clearly failing.  
**Debug Steps:**  
1. Check pod status manually:  
   ```bash
   kubectl get pods -n <namespace> --field-selector=status.phase=Failed
   ```  
2. Verify the pod’s **exact status**:  
   ```bash
   kubectl describe pod <pod-name> -n <namespace> | grep -i "state:"
   ```  
3. Update the script to log raw pod states (temporarily for debugging):  
   ```python
   logger.info(f"Pod {pod.metadata.name} status: {pod.status.phase}, Container states: {pod.status.container_statuses}")
   ```  

---

### **5️⃣ Pods Stuck in CrashLoopBackOff After Restart**  
**Symptom:**  
- Pods are restarted but keep crashing.  
**Solution:**  
1. Check pod logs to find the root cause:  
   ```bash
   kubectl logs <pod-name> -n <namespace> --previous
   ```  
2. Fix the underlying issue (e.g., misconfigured environment variables, missing volumes).  
3. For testing, deploy a "safe" crashing pod:  
   ```bash
   kubectl apply -f scripts/test_crash_pod.yaml
   ```  

---

### **6️⃣ Deployment Fails in Kubernetes**  
**Error:**  
```bash
ERROR - ImagePullBackOff or CrashLoopBackOff in the restarter pod itself
```  
**Solution:**  
- Check the restarter pod’s logs:  
  ```bash
  kubectl logs -f deployment/pod-restarter -n <namespace>
  ```  
- Verify the `deployment.yaml` uses the correct:  
  - **Image**: `python:3.9-slim` (or update to a newer version).  
  - **Namespace**: Must match where RBAC is applied.  

---

## **🔍 Advanced Debugging**  

### **View Script Logs in Kubernetes**  
```bash
kubectl logs -f deployment/pod-restarter -n <namespace> --tail=50
```  

### **Increase Log Verbosity**  
Modify the script to enable debug logging:  
```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```  

### **Test RBAC Permissions**  
```bash
kubectl auth can-i delete pods --as=system:serviceaccount:<namespace>:pod-restarter
```  

---

## **📢 Need More Help?**  
- Open a [GitHub Issue](https://github.com/your-repo/issues) with:  
  - **Error logs**.  
  - **Steps to reproduce**.  
  - **Kubernetes version** (`kubectl version`).  

--- 

This guide covers the most common scenarios. Add more entries as users report new issues! 🛠️
