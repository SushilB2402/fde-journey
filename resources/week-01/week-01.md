# Week 01 Journal

* **Goal this week:** Complete Week 1 setup—understand the Forward Deployed Engineer (FDE) role, configure the development environment (VS Code, Python 3.13, Git), complete CS50P Lectures 0–2 problem sets, and establish a learning journal habit.

## What I Did
* **Role Mapping:** Analyzed FDE job descriptions across top AI companies (Palantir, OpenAI, Anthropic, Databricks, Scale AI) and synthesized key responsibilities, skills, and differences from SWE/SE/Consultant roles.
* **Environment Setup:** Installed VS Code, Python 3.13.14, and Git/GitHub CLI. Created the `fde-journey` repository and structured folders (`week1/`, `notes/`).
* **Python Practice (CS50P):** Wrote and successfully executed 10 Python scripts covering string manipulation, conditionals, arithmetic operations, functions, and boolean logic:
  * `indoor.py` (case conversion with `.lower()`)
  * `playback.py` (string replacement with `.replace()`)
  * `faces.py` (custom function converting emoticons to emojis)
  * `einstein.py` (energy calculation $E = mc^2$)
  * `tip.py` (currency and percentage string cleaning to float)
  * `deep.py` (case-insensitive string matching)
  * `extensions.py` (MIME type matching via `.endswith()`)
  * `math_interpreter.py` (expression parsing with `.split()`)
  * `camel.py` (converting camelCase to snake_case via loop)
  * `twttr.py` (filtering vowels out of strings)
  * Checkpoint functions: `checkpoint1.py` (`is_even()`) and `checkpoint2.py` (`convert_hours_to_minutes()`).
* **Version Control:** Made incremental commits using Git in the terminal and pushed changes to GitHub.

## What Blocked Me
* **CLI Typo (`CommandNotFoundException`):** 
  * *Error:* Typed `paython playback.py` in PowerShell, yielding `paython : The term 'paython' is not recognized as the name of a cmdlet...`
  * *Fix:* Corrected spelling to `python`.
* **PowerShell Command Parsing Error:** 
  * *Error:* Typed `forty two` directly into PowerShell instead of passing it into the running `deep.py` script prompt, causing `forty : The term 'forty' is not recognized...`
  * *Fix:* Ensured `python deep.py` is actively running before typing input into the prompt.
* **Input Parsing / Unpacking Exception (`ValueError`):**
  * *Error:* Running `python math_interpreter.py` with input `1+1` threw `ValueError: not enough values to unpack (expected 3, got 1)`.
  * *Fix:* Realized `.split(" ")` strictly relies on space delimiters. Passed expressions formatted with spaces (e.g., `1 + 1`), allowing `x_str, y, z_str` to unpack cleanly into 3 variables.
* **Inline Syntax Error:**
  * *Error:* Tried running `message = input() print(message.lower())` on a single line, causing a `SyntaxError`.
  * *Fix:* Separated statements onto two distinct lines in `indoor.py` (or used a semicolon `;` for single-line inline execution).

## What I Learned
* **Core FDE Work:** FDEs sit at the intersection of production systems engineering, customer embedding, and rapid deployment. Recording exact blockers, error logs, and fixes builds the reasoning documentation essential for FDE client deliverables.
* **Python Fundamentals:** Hands-on experience with string methods (`.strip()`, `.lower()`, `.replace()`, `.split()`), type casting (`int()`, `float()`), modular function definitions (`def main()`), and control flow (`if/elif/else`, `for` loops).
* **Git Operations:** Learned to perform explicit file staging (`git add <filename>`), descriptive commit messaging (`git commit -m "..."`), and remote sync (`git push`).

## Non-Technical Role Map Summary (5 Bullet Points)
1. **Startup CTO Embedded at a Client:** An FDE is like a hands-on technical lead who temporarily moves inside a client company to solve their most high-stakes, urgent software and AI challenges.
2. **Building Production Software:** Rather than just giving advice or making presentation slides, FDEs write high-quality code and build custom software that directly integrates into the customer's live IT systems.
3. **Translating Business to Tech:** FDEs work directly with company executives to understand complex business problems, then design and build the exact technical solution needed.
4. **On-the-Frontlines Fixer:** When custom systems break or hit real-world bottlenecks, FDEs are right there on site debugging, testing, and fixing issues in real time.
5. **Improving the Core Product:** Everything an FDE learns while working with clients gets fed back to the internal product and research teams to make the main software platform better for everyone.

## Next Step
* Transition into Week 2: customer discovery (The Mom Test), technical writing, enterprise data overview, and CS50P part 2 (exceptions, libraries, file I/O).