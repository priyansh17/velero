"""
Simple validation tests for Velero Chatbot
Run without dependencies to check basic functionality
"""
import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    # Test individual module syntax
    tests = [
        ('src/config.py', 'Config module'),
        ('src/azure_openai_client.py', 'Azure OpenAI client'),
        ('src/document_loader.py', 'Document loader'),
        ('src/vector_db.py', 'Vector database'),
        ('src/rag_system.py', 'RAG system'),
        ('src/chatbot.py', 'Chatbot'),
        ('cli.py', 'CLI'),
    ]
    
    passed = 0
    failed = 0
    
    for file_path, name in tests:
        try:
            with open(file_path, 'r') as f:
                code = f.read()
                compile(code, file_path, 'exec')
            print(f"  ✓ {name} syntax valid")
            passed += 1
        except SyntaxError as e:
            print(f"  ✗ {name} has syntax error: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {name} error: {e}")
            failed += 1
    
    return passed, failed


def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        'cli.py',
        'setup.sh',
        'config/.env.example',
        'src/__init__.py',
        'src/config.py',
        'src/azure_openai_client.py',
        'src/document_loader.py',
        'src/vector_db.py',
        'src/rag_system.py',
        'src/chatbot.py',
        'docs/QUICKSTART.md',
        'docs/CONFIGURATION.md',
        'docs/ARCHITECTURE.md',
        'docs/DEPLOYMENT.md',
        'docs/INDEX.md',
        'examples/example_queries.md',
    ]
    
    passed = 0
    failed = 0
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path}")
            passed += 1
        else:
            print(f"  ✗ {file_path} missing")
            failed += 1
    
    return passed, failed


def test_configuration():
    """Test configuration template"""
    print("\nTesting configuration...")
    
    required_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_DEPLOYMENT_NAME',
        'PINECONE_API_KEY',
        'WEAVIATE_URL',
        'ENABLE_RAG',
        'VECTOR_DB_TYPE',
    ]
    
    passed = 0
    failed = 0
    
    try:
        with open('config/.env.example', 'r') as f:
            content = f.read()
            for var in required_vars:
                if var in content:
                    print(f"  ✓ {var} in template")
                    passed += 1
                else:
                    print(f"  ✗ {var} missing from template")
                    failed += 1
    except Exception as e:
        print(f"  ✗ Error reading config: {e}")
        failed = len(required_vars)
    
    return passed, failed


def test_documentation():
    """Test documentation completeness"""
    print("\nTesting documentation...")
    
    docs = [
        ('README.md', ['Installation', 'Usage', 'Configuration']),
        ('docs/QUICKSTART.md', ['Step 1', 'Step 2']),
        ('docs/CONFIGURATION.md', ['Azure OpenAI', 'Vector Database']),
        ('docs/ARCHITECTURE.md', ['Components', 'Architecture']),
    ]
    
    passed = 0
    failed = 0
    
    for file_path, keywords in docs:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                file_passed = True
                for keyword in keywords:
                    if keyword.lower() not in content.lower():
                        print(f"  ✗ {file_path} missing section: {keyword}")
                        failed += 1
                        file_passed = False
                if file_passed:
                    print(f"  ✓ {file_path} complete")
                    passed += 1
        except Exception as e:
            print(f"  ✗ Error reading {file_path}: {e}")
            failed += 1
    
    return passed, failed


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("Velero Chatbot Validation Tests")
    print("=" * 60)
    
    total_passed = 0
    total_failed = 0
    
    tests = [
        test_file_structure,
        test_imports,
        test_configuration,
        test_documentation,
    ]
    
    for test in tests:
        passed, failed = test()
        total_passed += passed
        total_failed += failed
    
    print("\n" + "=" * 60)
    print(f"Total: {total_passed} passed, {total_failed} failed")
    print("=" * 60)
    
    if total_failed == 0:
        print("\n✓ All validation tests passed!")
        return 0
    else:
        print(f"\n✗ {total_failed} validation test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
