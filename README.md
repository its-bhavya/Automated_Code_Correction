### Introduction
Automated code correction has become extremely valuable in software development. It helps reduce the time and effort programmers spend hunting down and fixing bugs, thereby cutting major costs for organizations. However, automatically detecting and repairing errors, especially subtle, single-line bugs, can often prove to be difficult. Effectively fixing a bug, without changing the core algorithm and structure of the program is the main objective of automated code correction.

In this project, I built an LLM agent to tackle this exact challenge. The agent focuses on fixing single-line defects in Python programs taken from the QuixBugs benchmark. To do this, I used DSPy along with Gemini 2.0 Flash. The biggest advantage of this approach is that DSPy requires very minimal prompt engineering. The agent essentially trains itself based on simple input and output descriptions, along with a minimal docstring to give a high-level objective of its functionality, which makes the process more efficient and scalable.

After getting the fixed programs from the agent, the next step was to integrate the system with automated tests. After the agent generates a fix, the program is validated using a test harness to ensure that the bug is truly fixed and that no new errors are introduced. 

Throughout the project, I learned that the quality of the prompts play a huge role in the agent’s success. Even small changes can dramatically affect the results. A major challenge was handling the model’s tendency to output code wrapped in markdown or backticks, which breaks execution unless cleaned up. Having minimal experience with program testing, redesigning the test harness for automation and clarity was a very new experience. 

Despite the problems, the agent performed well. It was able to fully fix 28 out of 40 programs, passing all their tests. Other programs showed improvement, passing more tests than their buggy versions, though not all. 

This shows that LLMs hold significant promise for automating code debugging and repair.


### Backlogs
At the start, I had very little experience with program testing, especially using PyTest. Understanding how the test harness worked and how test cases were organized took me some time. It wasn’t straightforward at first, and I had to dig into the documentation and experiment a lot.

One tricky part was with the graph-based programs. They didn’t have proper JSON test cases in the original setup. Because of this, it was hard to tell how many test cases actually passed or failed for those. To fix this, I ended up modifying the test harness. I incorporated all the test cases, including those for graph programs, by using a more complete directory of Python test cases. This change helped make the testing consistent across all programs.

Another big challenge was that the language model sometimes output the fixed code inside markdown or with backticks around it. Even though the code itself was correct, this formatting made it impossible to run, so zero tests passed for those cases. I tried tweaking the prompts several times to fix this, but the problem never fully went away. Still, I was able to reduce the issue enough to salvage many of the fixes.

Also, PyTest produced very verbose outputs, way too much to look through every time. To handle that, I wrote some parsing code to pull out just the key numbers: how many tests passed and how many failed. This way, I could get a quick summary without sifting through pages of logs.

These hurdles did slow down the progress at times, but working through them helped me understand the testing pipeline better and made the system more reliable.

## Approach

### Basic Workflow

Sample Output
![Screenshot 2025-05-29 235256](https://github.com/user-attachments/assets/e20e2d0b-867e-4e33-bc32-ea1bb71a88af)

The method centers around a self-contained fix-and-validate pipeline that uses DSPy to connect a large language model (LLM) to a buggy Python program and return a corrected version that passes all test cases. The core principle: identify a single-line fault, repair it while preserving algorithmic logic, and verify the fix via automated testing.

The agent is built using dspy, with a signature (FixBuggyProgram) that takes buggy_code as input and outputs fixed_code. The objective is to make minimal changes, retain the core structure, and output only executable Python code, with no markdown, backticks, or explanations.

A CodeFixer module wraps the prediction logic and is used by a fix_and_test() function, which automates the entire sequence: loading buggy files, generating a fix, saving the modified version, and running it through a validation step.

The validation relies on a custom tester.py script, tailored to handle varied test structures. Initially, issues arose due to incomplete test support — especially for graph-based algorithms that lacked JSON definitions. To address this, the test harness was refactored to uniformly fetch test cases from the python_testcases/ directory. This ensured that even edge cases, including recursive graph traversals and input-driven algorithms, were handled seamlessly by the same PyTest runner.

One key issue stemmed from the formatting of LLM output. Often, the model wrapped code in triple backticks (```) or added markdown-like headers, which rendered the scripts non-executable. This behavior broke the validation loop, since even technically correct code did not execute. Stripping markdown formatting post-inference and tweaking the prompt instructions helped reduce—but not fully eliminate—this problem.

The fix-and-test loop executed programmatically, with result summaries extracted directly from PyTest’s output. Rather than dump verbose logs for every test run, the pipeline parsed lines containing "Passed: x/y" and surfaced concise pass/fail ratios. This not only sped up debugging but also provided fast feedback when running the agent across 40+ programs in batch mode.

Integration with MLflow allowed automatic logging of traces from DSPy’s compile step, aiding future evaluation or fine-tuning. While no training was involved (the model used was gemini-2.0-flash via API), tracking prompt-output pairs ensured traceability and reproducibility. MLFlow helped track the system prompt that DSPy created based on the signature and input/output field description. 
![Screenshot 2025-05-29 235609](https://github.com/user-attachments/assets/512326e1-1361-4541-9206-bf1fc179630e)


Each corrected program, if successful, was stored separately in a fixed_programs/ folder. This modular setup ensured clean separation between raw, fixed, and tested versions, making the entire system easy to debug, extend, and benchmark.

Here’s a detailed **Results** section draft based on your metrics and test outcomes:

---

### **Results**

The performance of the automated bug-fixing agent was evaluated across a benchmark suite of 40 Python programs, each containing a known one-line bug. The assessment focused on the quality of the fixes, the number of test cases passed post-repair, and the executability of the generated code.

#### **1. Overall Performance**

| Metric                                            | Count / Value   |
| ------------------------------------------------- | --------------- |
| Total buggy programs tested                       | 40              |
| Programs passing **all** test cases (fully fixed) | 28              |
| Programs with **partial improvement**             | 3               |
| Programs with **no improvement**                  | 3               |
| Programs with **non-executable output**           | 6               |
| Executable programs generated                     | 34              |
| Total repair success rate (fully fixed)           | **70%** (28/40) |
| Total executable fix rate                         | **85%** (34/40) |

#### **2. Classification of Outputs**

* **Fully Fixed**: 28 programs had all their test cases passed, indicating a complete and correct one-line repair by the LLM.
* **Partially Fixed**: 3 programs improved in performance, passing more test cases than the original buggy versions but not achieving full correctness.
* **No Change**: 3 programs performed identically to the buggy baseline — the fix did not improve or degrade results.
* **Non-Executable Outputs**: 6 generated outputs contained formatting issues like Markdown backticks or code blocks, rendering them untestable.

#### **3. Error Analysis**

* **False Positives**: None observed — programs did not falsely pass test cases they weren’t supposed to.
* **False Negatives**: Some correct-looking code snippets wrapped in Markdown syntax led to false negatives during execution due to unparseable formatting.

#### **4. Observations**

* Even minor prompt adjustments had a significant impact on output quality.
* Markdown artifacts consistently caused execution failures despite syntactically correct code inside.
* The system’s repair capability was notably strong for standard algorithmic patterns, but less consistent for graph-based logic.



