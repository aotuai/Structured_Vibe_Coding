**Repository:** https://github.com/aotuai/Structured_Vibe_Coding  
**License:** BSD. Use at your own risk; PRs welcome. Keep changes tiny, logs clear, and defaults sensible.

Author's experience:
> Using this methodology, We have generated 99% of production code with a combination of Claude, Gemini, and GPT — across both small features and large complex tasks — over the past 1.5 years, on a monthly subscription budget of $20–$60. Most of our engineer's background: decades in C/C++, Linux OS, Git, Python, and Algorithms.

- [1. Philosophy: Structured Vibe Coding](#1-philosophy-structured-vibe-coding)
  - [1.1. Who is this for?](#11-who-is-this-for)
- [2. The Structured Blueprint Method](#2-the-structured-blueprint-method)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Align Requirements Between AI and Human](#22-align-requirements-between-ai-and-human)
    - [2.2.1. Reflect the scope with change\_request\_prompt.md](#221-reflect-the-scope-with-change_request_promptmd)
  - [2.3. Co-Design with AI](#23-co-design-with-ai)
    - [2.3.1. Generate coding\_prompt.md for AI, update DESIGN.md for human](#231-generate-coding_promptmd-for-ai-update-designmd-for-human)
  - [2.4. Code and Test with Human Verification](#24-code-and-test-with-human-verification)
    - [2.4.1. Code by AI and Tests by human](#241-code-by-ai-and-tests-by-human)
- [3. Vibe Coding Tools](#3-vibe-coding-tools)
  - [3.1. Quick Start](#31-quick-start)
  - [3.2. `concatenate_text_files.py`](#32-concatenate_text_filespy)
  - [3.3. `concatenate_python_files.py`](#33-concatenate_python_filespy)
  - [3.4. `save_commits.py`](#34-save_commitspy)
  - [3.5. `analyze_folder.py`](#35-analyze_folderpy)
- [4. Workflow Examples](#4-workflow-examples)
  - [4.1. Whole-project review](#41-whole-project-review)
  - [4.2. Python bug fix in a small tool](#42-python-bug-fix-in-a-small-tool)
  - [4.3. Focused PR feedback](#43-focused-pr-feedback)
  - [4.4. The Blueprint Method](#44-the-blueprint-method)
- [5. FAQ](#5-faq)

---

# 1. Philosophy: Structured Vibe Coding

Fundamentally, Agentic IDEs (like Cursor or Copilot) introduce a middleman into your workflow. They wrap the underlying foundation models in a black box, relying on hidden system prompts and automated, unpredictable context-gathering.

Structured Vibe Coding explicitly rejects the black box. It operates on two core pillars:

* **Deterministic Tooling**: Scripts that allow humans to share exact context with the AI, and for the AI to return complete files back to the human. So the interaction with AI is transparent to the user.
  * **Concatenate scripts:** Package source code, git history, requirements and design documents for dropping into a chat interface
  * **Code retrieval tools:** Retrieve output and dropping back to the repository
* **Structured Blueprint Workflows**: A clear, phase-based framework that forces the AI to collaborate exactly how a junior and senior software engineer would interact:
  * **Requirements Clarification** 
  * **Design Constraint Confirmation** 
  * **Code & Test Verification**

| Feature | Structured Vibe Coding  | Agentic IDEs (Cursor/Copilot) | Autonomous Agents (Devin) |
| :--- | :--- | :--- | :--- |
| **Target User** | **Production Engineering.** CLI-comfortable devs and budget-conscious teams. | **Speed-Focused Devs.** Individuals rapidly prototyping. Output often requires a separate engineering pass for production. | **Task Delegators.** Teams wanting hands-off, "fire-and-forget" issue resolution. |
| **Context Control** | **Absolute.** You build the exact text file. | **Low.** The IDE guesses what matters via RAG. | **Variable.** The agent navigates the repo itself. |
| **Transparency** | **High.** Prompts are version-controlled docs. | **Zero.** Hidden system prompts and hidden RAG. | **Moderate.** You can view the agent's thought logs. |
| **Code Application** | **Atomic.** Whole-file generation downloaded directly. | **Injected.** Heuristic-based inline streaming. | **Asynchronous.** Direct git commits and branch creation. |
| **Diff & Verification** | **Strict.** Deterministic visual diffs via `meld`. | **Ephemeral.** Custom UI diffs that vanish once accepted. | **Standard PR.** Reviewed asynchronously via GitHub/GitLab. |
| **Merge Safety** | **High.** Human has pixel-perfect control over hunks. | **Variable.** "Apply" buttons often botch boilerplate and indentation. | **Moderate.** Depends entirely on the agent's test-running ability. |
| **Iteration Speed** | High Overall. Slower micro-edits due to manual diff checks, but reaches production faster by avoiding rework. | Medium Overall. Frictionless for micro-edits, but automated drafting often leads to context loss and rework. | Slowest. High latency as agents navigate and execute tasks. || **Cost** | **Predictable.** Flat-rate chat subscriptions. | **Moderate.** Monthly IDE subscription tiers. | **High.** Token-heavy, often metered per task. |
| **Vendor Lock-in** | **None.** Works with Claude, GPT, local models. | **High.** Tied to their specific interface/servers. | **High.** Tied to the specific platform. |

For small features, you don't need the Structured Blueprint Method — jump straight to [Vibe Coding Tools](#3-vibe-coding-tools). This toolkit is for software engineers comfortable with the command line.

- **Chat-only workflow:** AI is changing fast — don't lock yourself in to any one model or tool.
- **Requirements, design, and coding:** Have AI confirm each stage before moving to the next.
- **Git and diff:** Communicate with the AI through git history and diffs so it can reason over the exact context you see.

For larger features, asking an AI to design architecture and write code at the same time often leads to hallucinations and context drift. Use **The Blueprint Method**: a structured three-phase methodology that shifts AI from a guessing machine to a precise execution engine.

## 1.1. Who is this for?

- **Minimize cost.** Flat-rate chat subscriptions instead of token-metered agentic tools — predictable spend for solo developers, students, contractors, and small teams.
- **Switch models freely.** The same text bundle drops into any chat — Private AI (self-hosted Llama, DeepSeek, Qwen), Claude, GPT, Gemini — so you pick the best model per task without changing tools.
- **Production Software Engineering.** The Blueprint Method (requirements → design → code, with verification gates) outlives any specific tool or model.

---

# 2. The Structured Blueprint Method

A methodology that gets explicit confirmation at each step: requirements → design → coding. Humans and AI stay aligned without rework or context drift.

## 2.1. Prerequisites

Move your design, requirement, and test documents into Markdown format, for example, DESIGN.md in the repository.

VS Code, with a few extensions, gives you a Word/Google Docs-like editing experience for Markdown:

- Export Google Docs to HTML ZIP, then convert the HTML into Markdown with Pandoc:
  ```
  pandoc GoogleDocExport.html --wrap=none --markdown-headings=atx -f html-native_divs-native_spans -t gfm-smart --extract-media=. -o CleanedDocExport.md
  ```
- Use Mermaid `sequenceDiagram` for inline interaction sequences.
- Use Mermaid `graph TD` for inline flowcharts and architecture diagrams.
- Use drawio for diagrams, then export to SVG and embed inline in your Markdown.
- Use GitHub Flavored Markdown (GFM) for tables.
- Use the **Markdown All-in-One** extension for section numbering and the Table of Contents.

## 2.2. Align Requirements Between AI and Human

Feed the AI your change request and ask it to audit for edge cases before any code is written.

### 2.2.1. Reflect the scope with change_request_prompt.md

1. Place change_request_prompt.md in the my_app/design_docs/ folder along with design documents, e.g., DESIGN.md.

2. Package the related source code and document files with Vibe Coding Tools For example,

```bash
python3 ./Structured_Vibe_Coding/concatenate_text_files.py my_app/ --recursive
```
This will generate a file my_app_concat.txt

3. Drop the my_app_concat.txt in AI chat window along with the following prompt,

> Audit `design_docs/change_request_prompt.md` for clarity, missing edge cases, and logical gaps. Rewrite it into strict Given-When-Then acceptance criteria, divided into small steps that build incrementally and can each be verified before the next. And propose updates to `design_docs/change_request_prompt.md` reflecting the new scope. Wait for my approval before writing any code. Do not include details already implemented in the codebase.
> 
> The Ground Truth Principle: Treat the codebase as the absolute source of truth. Markdown design files are historic intent. If they clash, the code wins.
>

## 2.3. Co-Design with AI

Have the AI map out *how* the change request integrates into the codebase by updating your design docs (`DESIGN.md` or any Mermaid diagrams).

### 2.3.1. Generate coding_prompt.md for AI, update DESIGN.md for human

> Based on the approved `design_docs/change_request_prompt.md` and the codebase context, update design documents in `design_docs/`. Wait for my approval. Then generate a strict step-by-step `coding_prompt.md` for execution. Wait for my approval. Do not include in `coding_prompt.md` any details already implemented in the codebase.
>
> The Ground Truth Principle: Treat your codebase as the absolute source of truth. Design docs are historic intent. If they clash, the code wins.
>
> When updating the design documents, edit only what this change affects. Capture architecture changes, user-facing impacts, API changes, and external constraints — not low-level implementation details, which live in the code.
>
> I will provide the architecture diagrams as .drawio.svg files for you to update. Preserve the embedded draw.io XML so the diagrams stay editable.

## 2.4. Code and Test with Human Verification

Feed the AI the generated `coding_prompt.md` and force it to code incrementally.

### 2.4.1. Code by AI and Tests by human

> Execute prompt 1: `...` of the coding_prompt.md. Write complete, production-ready code with no placeholders. Stop and wait for me to verify the tests pass before moving to the next prompt.
>
> Coding Constraints:
> - Generate the whole file: Always output the complete file content so I can download and replace my local copy directly. Please provide the full file path and directory above the code block. Do not change the file name; it must exactly match the original.
> - Minimal changes only: Do the absolute minimum required to accomplish the task. Do not expand the scope. If you feel a broader architectural change is necessary, ask for my approval first.
> - Zero cosmetic changes: I manually review every line using meld via gitk diffs. Do not reformat existing code, change indentation, merge/split lines, or modify/add/remove comments. Leave the surrounding code exactly as you found it to keep the diff clean.

---

# 3. Vibe Coding Tools

Keep it simple. These small scripts package the **right** text or code so you can drop a file, folder, or file type into a chat-based AI. **No lock-in** to any model or tool.

## 3.1. Quick Start

```bash
python3 -m venv venv && source venv/bin/activate
# run any tool with: python3 <tool>.py [args]
```

1. Run a tool below to generate a **single text file**.
2. Attach or paste that file into your coding chat.
3. Prompt the AI for what you want — review, refactor, tests, bug fix, or a Blueprint Method phase.

---

## 3.2. `concatenate_text_files.py`

*Snapshot all text files in a repo.*

**What:** Recursively collects text-like files (`.py`, `.md`, `.json`, etc.), skips noisy folders (`.git/`, `node_modules/`, `dist/`, etc.), and writes one bundle with a header per file.

**Why:** Share the **whole project context** in chat without zipping.

**Usage:**
```bash
python3 concatenate_text_files.py path/to/project --recursive
# → creates ./<project>.txt containing all included files with headers
```

The script supports `--code-only` and `--py-only` options to reduce the number of files included in the package.

---

## 3.3. `concatenate_python_files.py`

*Bundle a script plus its local imports.*

**What:** Traces local Python imports starting from one or more entry scripts and concatenates those files into a single text artifact.

**Why:** Give AI the **exact Python dependency closure** it needs for reasoning, without external packages.

**Usage:**
```bash
python3 concatenate_python_files.py project_root/ path/to/main.py [another.py ...]
# → writes project_root_concatenated.txt
```

---

## 3.4. `save_commits.py`

*Package the files changed in a commit or range.*

**What:** Finds files changed in one commit (or between two commits) and writes their contents to a single text file with commit headers.

**Why:** Share **focused diffs** for targeted reviews or debugging.

**Usage:**
```bash
# Single commit
python3 save_commits.py --this f9e8d7c

# Range (base..this)
python3 save_commits.py --base a1b2c3d --this f9e8d7c
# → writes <this>.txt or base-this.txt
```

---

## 3.5. `analyze_folder.py`

*Quick repo inventory.*

**What:** Scans a directory, groups files by type, totals sizes, and shows a small table (count, total size, example largest file). No bundle output — just fast insight.

**Why:** Decide **what to package** (and what to ignore) before chatting.

**Usage:**
```bash
python3 analyze_folder.py              # analyze current folder
python3 analyze_folder.py path/to/dir  # analyze a specific directory
```

---

# 4. Workflow Examples

## 4.1. Whole-project review

1. `python3 concatenate_text_files.py ./myapp` → `myapp.txt`
2. Attach `myapp.txt` in chat.
3. Ask: *"Review for structure, add tests for X, and propose a minimal refactor."*

## 4.2. Python bug fix in a small tool

1. `python3 concatenate_python_files.py ./tools ./tools/runner.py` → `tools_concatenated.txt`
2. Attach; ask: *"There's a crash when input is empty. Fix it and add doctests."*

## 4.3. Focused PR feedback

1. `python3 save_commits.py --base abc123 --this def456` → `abc123-def456.txt`
2. Attach; ask: *"Explain risk, edge cases, and missing tests in this change."*

## 4.4. The Blueprint Method

1. `python3 concatenate_text_files.py ./myapp --code-only` → `myapp_code.txt`
2. Attach `myapp_code.txt` along with your `requirement_prompt.md`.
3. Follow the prompts in Section **The Blueprint Method** to design and execute without context drift.

---

# 5. FAQ

**Why text instead of zip?** Text is immediately visible and searchable in chat, avoids unzip friction, and keeps you and the AI tightly in sync.

**Does this include third-party dependencies?** No — these tools focus on your source and local imports. Mention external packages in your prompt or attach your `change_request_prompt.md`.

