# "Paper-to-Code" Research Scout Agent

An agentic AI assistant designed for Machine Learning Engineers to automate academic research discovery and boilerplate PyTorch scaffolding. Given a search query, the agent queries the arXiv API, parses relevant paper metadata, drafts a PyTorch implementation of the core block, executes tests locally inside a subprocess, and self-corrects any compilation or shape errors using a feedback loop.

---

## What It Does
* **arXiv Discovery:** Queries the public arXiv API for the top relevant machine learning paper matching a search term.
* **Math & Architecture Synthesis:** Extracts the core neural network mechanisms, dimensions, and equations from the abstract.
* **PyTorch Scaffolding:** Generates self-contained, modular PyTorch code implementing the block.
* **Local Subprocess Verification:** Executes the code in a sandbox shell to run dummy tensors through the forward pass.
* **Self-Correction Feedback Loop:** Captures tracebacks from the shell, feeds error logs back to the LLM, and refactors the script dynamically (up to 3 retries) until it compiles and runs without shape errors.

---

## Simple Architecture Sketch

```
               [ User Input Query ]
                        │
                        ▼
               ┌─────────────────┐
               │  arXiv API      │ ──► [ Title & Abstract XML ]
               └─────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │   Gemini LLM    │ ──► [ Modular PyTorch Code Draft ]
               └─────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │ Local Filesystem│ ──► [ Write temp_scaffold.py ]
               └─────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │ Subprocess Run  │ ──► [ Success? Yes: Save & Finish ]
               └─────────────────┘
                        │
                        ▼ (No: Capture stderr Error Logs)
                        │
                        ▼
               ┌─────────────────┐
               │ Self-Correction │ ──► (Re-prompt Gemini with traceback)
               └─────────────────┘
```

---

## Setup & Installation

### Prerequisites
* Python 3.8 or higher
* PyTorch installed in your active environment
* A Gemini API Key from Google AI Studio

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Isha-Maryam/Flyrank_ML_Internship_Capstone_.git
   cd Flyrank_ML_Internship_Capstone_/work
   ```

2. **Configure your API Key:**
   On Windows (PowerShell):
   ```powershell
   $env:GEMINI_API_KEY="your_api_key_here"
   ```
   On Linux/macOS:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

3. **Install the required SDK:**
   ```bash
   pip install google-generativeai pypdf
   ```

---

## Usage Example

Run the agent from your terminal by passing a research topic query:

```bash
python paper_to_code_agent.py "LoRA: Low-Rank Adaptation of Large Language Models"
```

### Observed Execution Log:
```text
[Agent] Searching arXiv for: 'LoRA: Low-Rank Adaptation of Large Language Models'...
[Agent] Top Paper Found: LoRA: Low-Rank Adaptation of Large Language Models
[Agent] URL: http://arxiv.org/abs/2106.09685
--------------------------------------------------
Abstract Summary:
We propose Low-Rank Adaptation, or LoRA, which freezes the pre-trained model weights and injects trainable rank decomposition matrices...
--------------------------------------------------

[Agent] [Attempt 1/3] Prompting LLM for code generation...
[Agent] Saved draft to temp_scaffold.py
[Agent] Executing temp_scaffold.py locally to verify...

[Agent] SUCCESS! The model compiled and passed execution checks.
--------------------------------------------------
Success! Script compiled and ran without errors.
--------------------------------------------------
```

---

## Evaluation & Performance (v2)

We evaluated the agent across 5 core research papers:
1. **LoRA (Low-Rank Adaptation):** Compiled on Attempt 1. Correctly constructed $W_0 + BA$ matrix additions.
2. **DPO (Direct Preference Optimization):** Compiled on Attempt 1. Correctly generated preference log-ratio loss.
3. **KAN (Kolmogorov-Arnold Networks):** Compiled on Attempt 2. Attempt 1 failed on spline tensor shape mismatch; self-corrected on Attempt 2.
4. **FlashAttention-2:** Compiled on Attempt 1. Note: Generates standard attention formulas rather than CUDA kernels.
5. **QLoRA:** Compiled on Attempt 2. Attempt 1 failed due to missing 4-bit quantizer libraries; self-corrected to standard simulation mock.

---

## Enforced Guardrails
* **Subprocess Sandboxing:** The agent cannot execute raw system commands (`rm`, `del`, `curl`). It only runs the generated python file using the local interpreter.
* **Environment Isolation:** The agent is blocked from running `pip install` automatically. It must operate only with libraries already present in the user's host environment.

---

## Known Limitations
* **Single Paper Search:** The agent only evaluates the top search result from arXiv. If the keyword search returns an adjacent or irrelevant paper first, the agent cannot scroll or select others.
* **Dependency Issues:** If the generated PyTorch script requires niche external libraries (like `triton` or `einops`), execution will fail unless pre-installed on the host machine.
* **API Rate Limits:** ArXiv API requests must be throttled to 3 seconds to avoid IP rate-limiting.
