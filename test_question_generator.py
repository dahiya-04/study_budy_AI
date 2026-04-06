#!/usr/bin/env python3
"""Quick test script for QuestionGenerator"""

import sys
sys.path.insert(0, '/workspaces/study_budy_AI')

from src.generator.question_genrator import QuestionGenerator

def test_question_generator():
    try:
        print("🧪 Testing QuestionGenerator...")
        
        # Initialize
        print("\n✓ Initializing QuestionGenerator...")
        generator = QuestionGenerator()
        print("✓ Initialization successful")
        
        # Test MCQ generation
        print("\n📝 Testing MCQ Generation...")
        mcq = generator.generate_mcq(topic="Python", difficulty="easy")
        print(f"✓ MCQ generated successfully:")
        print(f"  Question: {mcq.question}")
        print(f"  Options: {mcq.options}")
        print(f"  Correct Answer: {mcq.correct_answer}")
        
        # Test Fill-in-the-blank generation
        print("\n📝 Testing Fill-in-the-Blank Generation...")
        blank = generator.generate_fill_in_blank(topic="History", difficulty="medium")
        print(f"✓ Fill-in-the-blank generated successfully:")
        print(f"  Question: {blank.question}")
        print(f"  Answer: {blank.correct_answer}")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_question_generator()
    sys.exit(0 if success else 1)
