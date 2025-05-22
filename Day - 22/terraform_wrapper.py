import subprocess
import shutil
import os
import sys
from typing import Optional, List, NamedTuple
from datetime import datetime, timedelta


class TerraformResult(NamedTuple):
    return_code: int
    stdout: str
    stderr: str
    timed_out: bool = False


class TerraformWrapper:
    def __init__(self, working_dir: str, timeout_minutes: int = 10):
        self.working_dir = os.path.abspath(working_dir)
        self.timeout = timedelta(minutes=timeout_minutes)
        self._validate_working_dir()
        self._validate_terraform_installed()
        
    def _validate_working_dir(self) -> None:
        if not os.path.isdir(self.working_dir):
            raise FileNotFoundError(f"Working directory does not exist: {self.working_dir}")
            
        tf_files = [f for f in os.listdir(self.working_dir) if f.endswith('.tf')]
        if not tf_files:
            raise ValueError(f"No Terraform files (.tf) found in directory: {self.working_dir}")

    def _validate_terraform_installed(self) -> None:
        if shutil.which("terraform") is None:
            raise EnvironmentError("Terraform not found in PATH. Please install Terraform.")

    def _run_terraform_command(
        self,
        command: str,
        args: Optional[List[str]] = None,
        var_file: Optional[str] = None
    ) -> TerraformResult:
        if args is None:
            args = []
            
        cmd = ["terraform", command] + args
        
        if var_file:
            if not os.path.isfile(var_file):
                raise FileNotFoundError(f"Var file not found: {var_file}")
            cmd.extend(["-var-file", var_file])
        
        stdout_lines = []
        stderr_lines = []
        process = None
        timed_out = False
        
        try:
            start_time = datetime.now()
            process = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Read output while process is running
            while True:
                # Check timeout
                if datetime.now() - start_time > self.timeout:
                    process.kill()
                    timed_out = True
                    raise TimeoutError(f"Command timed out after {self.timeout}")
                
                # Try to read output
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()
                
                if stdout_line:
                    print(stdout_line, end='')
                    stdout_lines.append(stdout_line)
                
                if stderr_line:
                    print(stderr_line, end='', file=sys.stderr)
                    stderr_lines.append(stderr_line)
                
                # Check if process has completed
                if process.poll() is not None:
                    break
                    
            # Get remaining output
            remaining_stdout, remaining_stderr = process.communicate()
            if remaining_stdout:
                print(remaining_stdout, end='')
                stdout_lines.append(remaining_stdout)
            if remaining_stderr:
                print(remaining_stderr, end='', file=sys.stderr)
                stderr_lines.append(remaining_stderr)
                    
        except TimeoutError as e:
            return TerraformResult(
                return_code=1,
                stdout=''.join(stdout_lines),
                stderr=''.join(stderr_lines) + f"\nERROR: {str(e)}",
                timed_out=True
            )
        except Exception as e:
            if process:
                process.kill()
            return TerraformResult(
                return_code=1,
                stdout=''.join(stdout_lines),
                stderr=''.join(stderr_lines) + f"\nError: {str(e)}",
                timed_out=timed_out
            )
        
        return TerraformResult(
            return_code=process.returncode if process else 1,
            stdout=''.join(stdout_lines),
            stderr=''.join(stderr_lines),
            timed_out=timed_out
        )

    def init(self, **kwargs) -> TerraformResult:
        return self._run_terraform_command("init", **kwargs)

    def plan(self, var_file: Optional[str] = None, extra_args: Optional[List[str]] = None) -> TerraformResult:
        args = extra_args if extra_args else []
        args.extend(["-refresh=false", "-lock=false"])  # Disable refresh and locking
        return self._run_terraform_command("plan", args=args, var_file=var_file)

    def apply(self, auto_approve: bool = True, var_file: Optional[str] = None, 
              extra_args: Optional[List[str]] = None) -> TerraformResult:
        args = extra_args if extra_args else []
        if auto_approve:
            args.append("-auto-approve")
        return self._run_terraform_command("apply", args=args, var_file=var_file)


if __name__ == "__main__":
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Set the Terraform directory
        tf_dir = os.path.join(script_dir, "terraform_example")
        
        print(f"Using Terraform directory: {tf_dir}")
        
        # Initialize with 10 minute timeout (reduced from 30)
        tf = TerraformWrapper(tf_dir, timeout_minutes=10)
        
        print("Running terraform init...")
        init_result = tf.init()
        
        if init_result.return_code != 0:
            print(f"Init failed: {init_result.stderr}", file=sys.stderr)
            sys.exit(1)
            
        print("Running terraform plan with disabled refresh...")
        plan_result = tf.plan()
        
        if plan_result.timed_out:
            print("\nERROR: Terraform plan timed out after 10 minutes!", file=sys.stderr)
            print("This indicates a serious issue. Possible causes:")
            print("1. AWS API rate limiting")
            print("2. Extremely large state file")
            print("3. Network connectivity issues")
            print("4. IAM permission problems")
            sys.exit(1)
            
        if plan_result.return_code == 0:
            print("\nPlan succeeded. Would you like to apply? (y/n)")
            if input().lower() == 'y':
                print("Running terraform apply...")
                apply_result = tf.apply()
                print(f"\nApply completed with return code: {apply_result.return_code}")
            else:
                print("Apply cancelled by user")
        else:
            print(f"\nPlan failed: {plan_result.stderr}", file=sys.stderr)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)
