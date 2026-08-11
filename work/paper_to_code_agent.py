import os
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import subprocess
import google.generativeai as genai

# Setup Gemini API key
# The agent will look for GEMINI_API_KEY in the environment
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    print("Warning: GEMINI_API_KEY environment variable not set. Please set it to run the LLM self-correction loop.")
else:
    genai.configure(api_key=api_key)

def search_arxiv(query: str) -> dict:
    """Searches arXiv API for the top match matching the query and returns metadata."""
    print(f"\n[Agent] Searching arXiv for: '{query}'...")
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results=1"
    
    try:
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        
        # Parse XML
        root = ET.fromstring(xml_data)
        
        # Define namespaces used by arXiv API
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'
        }
        
        entry = root.find('atom:entry', namespaces)
        if entry is None:
            return {"error": "No paper found matching query."}
            
        title = entry.find('atom:title', namespaces).text.strip().replace('\n', ' ')
        summary = entry.find('atom:summary', namespaces).text.strip().replace('\n', ' ')
        id_url = entry.find('atom:id', namespaces).text.strip()
        
        return {
            "title": title,
            "summary": summary,
            "url": id_url
        }
    except Exception as e:
        return {"error": f"Failed to query arXiv: {str(e)}"}

def run_local_script(filepath: str) -> tuple[bool, str]:
    """Runs the python script locally and captures output/errors."""
    print(f"[Agent] Executing {filepath} locally to verify...")
    try:
        result = subprocess.run(
            [sys.executable, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            return True, "Success! Script compiled and ran without errors."
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Error: Script execution timed out (potential infinite loop)."
    except Exception as e:
        return False, f"Execution failed: {str(e)}"

def run_agent_loop(query: str, output_code_path: str = "temp_scaffold.py"):
    """Core Agent Loop: Fetch -> Draft -> Execute -> Self-Correct -> Save."""
    # 1. Fetch Paper
    paper = search_arxiv(query)
    if "error" in paper:
        print(f"Error: {paper['error']}")
        return
        
    print(f"\n[Agent] Top Paper Found: {paper['title']}")
    print(f"[Agent] URL: {paper['url']}")
    print("-" * 50)
    print(f"Abstract Summary:\n{paper['summary'][:300]}...")
    print("-" * 50)
    
    if not api_key:
        print("\nStopping Agent: GEMINI_API_KEY is not set, cannot run the generation loop.")
        return
        
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # 2. Initial Draft Prompt
    prompt = f"""
    You are an expert Machine Learning Engineer. I need you to implement the core PyTorch module/block described in this paper abstract.
    
    Paper Title: {paper['title']}
    Abstract: {paper['summary']}
    
    Create a file '{output_code_path}' containing the PyTorch class. The code must be self-contained and run dummy inputs through the forward pass at the bottom of the script inside a `if __name__ == '__main__':` block to verify shape dimensions and syntax.
    
    Return ONLY clean, runnable Python code inside a markdown block. Do not include extra conversational text outside the code block.
    """
    
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        print(f"\n[Agent] [Attempt {attempt}/{max_retries}] Prompting LLM for code generation...")
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Extract code from markdown block
        code_lines = []
        in_block = False
        for line in text.splitlines():
            if line.strip().startswith("```python"):
                in_block = True
                continue
            elif line.strip().startswith("```") and in_block:
                in_block = False
                continue
            if in_block:
                code_lines.append(line)
                
        code = "\n".join(code_lines) if code_lines else text
        
        # Write to file
        with open(output_code_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[Agent] Saved draft to {output_code_path}")
        
        # 3. Execute
        success, feedback = run_local_script(output_code_path)
        
        if success:
            print(f"\n[Agent] SUCCESS! The model compiled and passed execution checks.")
            print("-" * 50)
            print(feedback)
            print("-" * 50)
            break
        else:
            print(f"\n[Agent] FAILURE on execution verification. Error Log:\n{feedback}")
            # Feed back the error log for self-correction in the next iteration
            prompt = f"""
            The previous Python code you generated for '{paper['title']}' failed execution check.
            Here is the code that failed:
            
            ```python
            {code}
            ```
            
            Here is the execution error log/stack trace:
            {feedback}
            
            Please analyze the error (such as wrong imports, syntax errors, or shape mismatches during forward pass), correct the code, and return the entire updated Python script.
            Return ONLY the updated python code inside a ```python block.
            """
    else:
        print(f"\n[Agent] Failed to compile after {max_retries} attempts.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "LoRA: Low-Rank Adaptation of Large Language Models"
        
    run_agent_loop(query)
