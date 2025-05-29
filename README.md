### Introduction
Automated code correction has become extremely valuable in software development. It helps reduce the time and effort programmers spend hunting down and fixing bugs, thereby cutting major costs for organizations. However, automatically detecting and repairing errors, especially subtle, single-line bugs, can often prove to be difficult. Effectively fixing a bug, without changing the core algorithm and structure of the program is the main objective of automated code correction.

In this project, I built an LLM agent to tackle this exact challenge. The agent focuses on fixing single-line defects in Python programs taken from the QuixBugs benchmark. To do this, I used DSPy along with Gemini 2.0 Flash. The biggest advantage of this approach is that DSPy requires very minimal prompt engineering. The agent essentially trains itself based on simple input and output descriptions, along with a minimal docstring to give a high-level objective of its functionality, which makes the process more efficient and scalable.

After getting the fixed programs from the agent, the next step was to integrate the system with automated tests. After the agent generates a fix, the program is validated using a test harness to ensure that the bug is truly fixed and that no new errors are introduced. 

Throughout the project, I learned that the quality of the prompts play a huge role in the agent’s success. Even small changes can dramatically affect the results. A major challenge was handling the model’s tendency to output code wrapped in markdown or backticks, which breaks execution unless cleaned up. Having minimal experience with program testing, redesigning the test harness for automation and clarity was a very new experience. 

Despite the problems, the agent performed well. It was able to fully fix 28 out of 40 programs, passing all their tests. Other programs showed improvement, passing more tests than their buggy versions, though not all. 

This shows that LLMs hold significant promise for automating code debugging and repair.
