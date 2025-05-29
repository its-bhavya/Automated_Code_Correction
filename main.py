from dotenv import load_dotenv
import os
import dspy
import mlflow
from utils import load_code, save_code, validate_fix_with_tester

mlflow.dspy.autolog(log_traces_from_compile=True)

mlflow.set_tracking_uri("http://127.0.0.1:8080")
mlflow.set_experiment("DSPy")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

lm = dspy.LM("gemini/gemini-2.0-flash", api_key=api_key)
dspy.configure(lm=lm)

class FixBuggyProgram(dspy.Signature):
    """Fix the one-line bug in the following program while preserving the original algorithm's logic and structure."""
    buggy_code: str = dspy.InputField(desc="Buggy source code with one-line error.")
    fixed_code: str = dspy.OutputField(desc="Fixed, valid, executable python code without any backticks, markdown, or explanation that retains the original algorithm's purpose and structure.")

class CodeFixer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.fix_program = dspy.Predict(FixBuggyProgram)

    def forward(self, buggy_code):
        result = self.fix_program(buggy_code=buggy_code)
        return result.fixed_code
    
# ========== 4. Fix-And-Test Pipeline ==========
def fix_and_test(algo_name, fixer):

    # Step 1: Load buggy code
    buggy_path = f"python_programs/{algo_name}.py"
    buggy_code = load_code(buggy_path)

    # Step 2: Generate fix using LLM
    fixed_code = fixer(buggy_code)

    # Step 3: Save fixed code
    fixed_path = f"fixed_programs/{algo_name}.py"
    save_code(fixed_path, fixed_code)

    # Step 4: Run test using tester.py
    print("----------------------------------------------------------------------------------------------------")
    print(f"Testing Result for '{algo_name}':")
    passed, pass_cases, total = validate_fix_with_tester(algo_name, flag="--fixed")

    return passed


# ========== 5. Main ==========
if __name__ == "__main__":
    fixer = CodeFixer()

    # Folder containing algorithm files
    folder = "python_programs"

    # Collect valid algorithm names (without .py)
    programs_to_fix = []

    for filename in os.listdir(folder):
        if filename.endswith(".py") and "_test" not in filename and "sqrt" not in filename:
            algo_name = filename[:-3]  
            programs_to_fix.append(algo_name)
    
    for prog in programs_to_fix[0:41]:
        fix_and_test(prog, fixer)