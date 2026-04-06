#!/usr/bin/env python3
"""Debug script to see LLM responses"""

import sys
sys.path.insert(0, '/workspaces/study_budy_AI')

from src.llm.groq_client import get_groq_client
from src.prompts.templats import mcq_prompt_template, fill_blank_prompt_template
import json

def debug_llm_response():
    try:
        llm = get_groq_client()
        
        print("🔍 Testing MCQ LLM Response...")
        mcq_prompt = mcq_prompt_template.format(topic="Python", difficulty="easy")
        print(f"\nPrompt:\n{mcq_prompt}\n")
        print("-" * 60)
        
        response = llm(mcq_prompt)
        print(f"Raw Response:\n{response.content}\n")
        print("-" * 60)
        
        # Try to parse
        try:
            parsed = json.loads(response.content)
            print(f"✓ Valid JSON:\n{json.dumps(parsed, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
        
        print("\n" + "=" * 60 + "\n")
        
        print("🔍 Testing Fill-in-the-Blank LLM Response...")
        blank_prompt = fill_blank_prompt_template.format(topic="History", difficulty="medium")
        print(f"\nPrompt:\n{blank_prompt}\n")
        print("-" * 60)
        
        response = llm(blank_prompt)
        print(f"Raw Response:\n{response.content}\n")
        print("-" * 60)
        
        # Try to parse
        try:
            parsed = json.loads(response.content)
            print(f"✓ Valid JSON:\n{json.dumps(parsed, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_llm_response()
