import os
import glob

for filepath in glob.glob("docs/**/*.md", recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix instances where the mermaid block starts on the same line as *(Reference Diagram:
    if "*(Reference Diagram: ```mermaid" in content:
        content = content.replace("*(Reference Diagram: ```mermaid", "*(Reference Diagram:)*\n\n```mermaid")
        # Also need to fix the closing tag which is ```)*
        content = content.replace("```)*", "```")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")
