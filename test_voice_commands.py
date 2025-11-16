"""
Test Enhanced Voice Command Detection
Tests various natural language phrasings and command variations
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Comprehensive test cases covering different phrasings
TEST_COMMANDS = {
    "FIND_ERRORS": [
        "find all syntax errors in main.py",
        "check for bugs in this file",
        "what's wrong with my code",
        "show me errors",
        "detect any issues in app.py",
        "are there any problems in this script",
        "debug this code",
        "why isn't this working",
        "syntax check please",
        "validate my code",
        "lint this file",
    ],
    
    "FIND_SYMBOL": [
        "find where userData is defined",
        "show me all uses of counter",
        "where is this variable modified",
        "locate handleClick function",
        "where does parse_intent get called",
        "show references to myVariable",
        "track the symbol user_data",
        "find all occurrences of calculate",
        "where is total_count changed",
        "show me where config is used",
        "go to the definition of process_data",
    ],
    
    "EXPLAIN_CODE": [
        "explain what this function does",
        "what does this code do",
        "describe this class",
        "help me understand this",
        "what's this for",
        "how does this work",
        "walk me through this code",
        "summarize this function",
        "break down this logic",
        "tell me about parse_intent",
        "what is the purpose of this",
    ],
    
    "EXPLAIN_TRACE": [
        "explain this error",
        "what caused this exception",
        "why did this crash",
        "analyze this stack trace",
        "what does this error mean",
        "why am I getting this exception",
        "what went wrong here",
        "interpret this traceback",
        "root cause of this error",
    ],
    
    "RUN_TESTS": [
        "run tests",
        "execute unit tests",
        "test this file",
        "run pytest",
        "perform testing",
        "check if tests pass",
        "run the test suite",
        "verify with tests",
    ],
    
    "PROPOSE_FIX": [
        "fix this error",
        "how do I fix this",
        "suggest a solution",
        "correct this bug",
        "resolve this issue",
        "make it work",
        "repair this code",
        "fix the indentation",
        "auto fix this",
        "how can I fix the syntax error",
    ],
    
    "FORMAT_FILE": [
        "format this code",
        "prettify main.py",
        "clean up this file",
        "fix the formatting",
        "beautify my code",
        "make it prettier",
        "auto format",
        "apply code style",
    ],
    
    "RENAME_SYMBOL": [
        "rename counter to item_count",
        "change userData to user_data",
        "refactor oldName to newName",
        "call it total instead",
    ],
    
    "NAVIGATE_TO": [
        "go to line 42",
        "jump to function main",
        "open file app.py",
        "take me to the error",
        "navigate to class User",
    ],
}

def test_command(command: str, expected_intent: str = None):
    """Test a single command"""
    response = requests.post(f"{BASE_URL}/intent", json={"text": command})
    
    if response.status_code == 200:
        result = response.json()
        intent = result['intent']
        confidence = result['confidence']
        entities = result['entities']
        
        # Check if intent matches expected
        match = "✓" if not expected_intent or intent == expected_intent.lower() else "✗"
        
        return {
            "command": command,
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "match": match
        }
    else:
        return {
            "command": command,
            "error": f"HTTP {response.status_code}"
        }

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)

def main():
    print("\n" + "="*80)
    print("  Enhanced Voice Command Detection Test")
    print("  Testing various natural language phrasings")
    print("="*80)
    
    try:
        # Check server
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("\n❌ Server not running!")
            return
        
        total_tests = 0
        correct_matches = 0
        
        # Test each intent category
        for expected_intent, commands in TEST_COMMANDS.items():
            print_section(f"Testing {expected_intent}")
            
            category_correct = 0
            
            for command in commands:
                result = test_command(command, expected_intent)
                total_tests += 1
                
                if result.get('match') == '✓':
                    correct_matches += 1
                    category_correct += 1
                
                # Print result
                intent = result.get('intent', 'ERROR')
                confidence = result.get('confidence', 0)
                match = result.get('match', '?')
                
                print(f"\n{match} \"{command}\"")
                print(f"   → Intent: {intent} (confidence: {confidence:.2f})")
                
                # Show extracted entities if interesting
                entities = result.get('entities', {})
                interesting = []
                if entities.get('file'):
                    interesting.append(f"file={entities['file']}")
                if entities.get('symbol'):
                    interesting.append(f"symbol={entities['symbol']}")
                if entities.get('line'):
                    interesting.append(f"line={entities['line']}")
                if entities.get('scope') and entities['scope'] != 'all':
                    interesting.append(f"scope={entities['scope']}")
                
                if interesting:
                    print(f"   Entities: {', '.join(interesting)}")
            
            accuracy = (category_correct / len(commands)) * 100
            print(f"\n   Category Accuracy: {category_correct}/{len(commands)} ({accuracy:.1f}%)")
        
        # Overall statistics
        print_section("Overall Results")
        overall_accuracy = (correct_matches / total_tests) * 100
        print(f"\n   Total Commands Tested: {total_tests}")
        print(f"   Correctly Classified: {correct_matches}")
        print(f"   Overall Accuracy: {overall_accuracy:.1f}%")
        
        if overall_accuracy >= 90:
            print(f"\n   🎉 Excellent! Voice command detection is highly accurate!")
        elif overall_accuracy >= 75:
            print(f"\n   ✓ Good! Voice command detection is working well!")
        elif overall_accuracy >= 60:
            print(f"\n   ⚠ Fair. Some commands may be misclassified.")
        else:
            print(f"\n   ❌ Needs improvement. Many commands are misclassified.")
        
        # Test entity extraction specifically
        print_section("Entity Extraction Tests")
        
        entity_tests = [
            ("find where userData is modified", "symbol=userData, scope=writes"),
            ("check errors in main.py", "file=main.py"),
            ("go to line 42", "line=42"),
            ("explain the calculate_total function", "function=calculate_total"),
            ("find user_data in python code", "symbol=user_data, language=python"),
        ]
        
        for command, expected in entity_tests:
            result = test_command(command)
            entities = result.get('entities', {})
            
            print(f"\n\"{command}\"")
            print(f"   Expected: {expected}")
            
            extracted = []
            if entities.get('file'):
                extracted.append(f"file={entities['file']}")
            if entities.get('symbol'):
                extracted.append(f"symbol={entities['symbol']}")
            if entities.get('line'):
                extracted.append(f"line={entities['line']}")
            if entities.get('function'):
                extracted.append(f"function={entities['function']}")
            if entities.get('scope') and entities['scope'] != 'all':
                extracted.append(f"scope={entities['scope']}")
            if entities.get('language') and entities['language'] != 'python':
                extracted.append(f"language={entities['language']}")
            
            print(f"   Extracted: {', '.join(extracted) if extracted else 'none'}")
        
        print("\n" + "="*80)
        print("  ✓ Voice Command Testing Complete!")
        print("="*80 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server!")
        print("   Start the backend with: python backend/main.py")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
