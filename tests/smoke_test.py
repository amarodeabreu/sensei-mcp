import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from sensei_mcp.server import mcp, get_engineering_context, record_decision, check_consistency, analyze_changes
    from sensei_mcp.models import ContextType
    from sensei_mcp.session import SessionManager
    from sensei_mcp.engine import ContextInferenceEngine
    
    print("✅ Imports successful")
    
    # Test Context Inference
    contexts = ContextInferenceEngine.infer_contexts(file_paths=["api/users.py"])
    assert ContextType.APIS_CONTRACTS in contexts
    print("✅ Context Inference successful")
    
    # Test Session Manager (mock path)
    mgr = SessionManager(Path("/tmp/sensei_test"))
    session = mgr.get_or_create_session("test_session")
    assert session.session_id == "test_session"
    print("✅ Session Manager successful")
    
    # Test Consistency Check Logic (Directly)
    # We can't easily test the tool without running the server, but we can verify the logic if we exposed it.
    # Since we didn't expose the logic separately, we'll trust the import for now.
    
    print("✅ Smoke test passed!")
    
except Exception as e:
    print(f"❌ Smoke test failed: {e}")
    sys.exit(1)
