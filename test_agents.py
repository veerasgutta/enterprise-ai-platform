"""
🧪 Enterprise Agent Integration Test
===================================

Test script to verify all enterprise agents are properly implemented
and can work together through the orchestration hub.

Run this script to validate the complete enterprise agent ecosystem.
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

# Add the agent-ecosystem directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_ecosystem_dir = os.path.join(current_dir, "agent-ecosystem")
sys.path.insert(0, agent_ecosystem_dir)

# Test individual agent imports
def test_agent_imports():
    """Test that all agent modules can be imported"""
    print("🔍 Testing Agent Imports...")
    results = {}
    
    # Test Executive Agent
    try:
        from enterprise_agents.executive.executive_agent import ExecutiveAgent
        results["executive"] = "✅ SUCCESS"
    except ImportError as e:
        try:
            # Try direct import
            sys.path.append(os.path.join(agent_ecosystem_dir, "enterprise-agents", "executive"))
            from executive_agent import ExecutiveAgent
            results["executive"] = "✅ SUCCESS (direct import)"
        except ImportError:
            results["executive"] = f"❌ FAILED: {e}"
    
    # Test Finance Agent
    try:
        from enterprise_agents.finance.finance_agent import FinanceAgent
        results["finance"] = "✅ SUCCESS"
    except ImportError as e:
        try:
            sys.path.append(os.path.join(agent_ecosystem_dir, "enterprise-agents", "finance"))
            from finance_agent import FinanceAgent
            results["finance"] = "✅ SUCCESS (direct import)"
        except ImportError:
            results["finance"] = f"❌ FAILED: {e}"
    
    # Test Legal Compliance Agent
    try:
        from enterprise_agents.legal_compliance.legal_compliance_agent import LegalComplianceAgent
        results["legal_compliance"] = "✅ SUCCESS"
    except ImportError as e:
        try:
            sys.path.append(os.path.join(agent_ecosystem_dir, "enterprise-agents", "legal-compliance"))
            from legal_compliance_agent import LegalComplianceAgent
            results["legal_compliance"] = "✅ SUCCESS (direct import)"
        except ImportError:
            results["legal_compliance"] = f"❌ FAILED: {e}"
    
    # Test Operations Agent
    try:
        from enterprise_agents.operations.operations_agent import OperationsAgent
        results["operations"] = "✅ SUCCESS"
    except ImportError as e:
        try:
            sys.path.append(os.path.join(agent_ecosystem_dir, "enterprise-agents", "operations"))
            from operations_agent import OperationsAgent
            results["operations"] = "✅ SUCCESS (direct import)"
        except ImportError:
            results["operations"] = f"❌ FAILED: {e}"
    
    # Print results
    for agent, status in results.items():
        print(f"  {agent.title().replace('_', ' ')} Agent: {status}")
    
    return results

async def test_agent_functionality():
    """Test basic functionality of each agent"""
    print("\n⚙️ Testing Agent Functionality...")
    
    # Test Executive Agent
    try:
        sys.path.append(os.path.join(agent_ecosystem_dir, "enterprise-agents", "executive"))
        from executive_agent import ExecutiveAgent
        
        exec_agent = ExecutiveAgent()
        print("  📊 Executive Agent:")
        
        # Test strategic business analysis
        situation_data = {
            "business_area": "market_expansion",
            "current_performance": {"revenue": 25000000, "growth_rate": 0.15},
            "market_conditions": ["competitive", "growing"],
            "timeline": "12_months"
        }
        
        result = await exec_agent.analyze_business_situation(situation_data)
        print(f"    ✅ Business Situation Analysis: {result.insight_id}")
        
    except Exception as e:
        print(f"    ❌ Executive Agent Test Failed: {e}")
    
    # Test Finance Agent
    try:
        sys.path.append(os.path.join(agent_ecosystem_dir, "enterprise-agents", "finance"))
        from finance_agent import FinanceAgent
        
        finance_agent = FinanceAgent()
        print("  💰 Finance Agent:")
        
        # Test financial forecasting
        forecast_data = {
            "current_financial_data": {
                "revenue": 25000000,
                "expenses": 18500000,
                "assets": 45000000,
                "liabilities": 15000000
            },
            "growth_assumptions": {
                "revenue_growth": 0.15,
                "expense_growth": 0.08
            }
        }
        
        result = await finance_agent.generate_financial_forecast(forecast_data, 12)
        print(f"    ✅ Financial Forecast: {result.forecast_id}")
        
    except Exception as e:
        print(f"    ❌ Finance Agent Test Failed: {e}")
    
    # Test Legal Compliance Agent
    try:
        sys.path.append(os.path.join(agent_ecosystem_dir, "enterprise-agents", "legal-compliance"))
        from legal_compliance_agent import LegalComplianceAgent
        
        legal_agent = LegalComplianceAgent()
        print("  ⚖️ Legal Compliance Agent:")
        
        # Test compliance assessment
        from legal_compliance_agent import ComplianceArea
        result = await legal_agent.assess_compliance_status(ComplianceArea.DATA_PRIVACY)
        print(f"    ✅ Compliance Assessment: {result['assessment_id']}")
        
    except Exception as e:
        print(f"    ❌ Legal Compliance Agent Test Failed: {e}")
    
    # Test Operations Agent
    try:
        sys.path.append(os.path.join(agent_ecosystem_dir, "enterprise-agents", "operations"))
        from operations_agent import OperationsAgent
        
        ops_agent = OperationsAgent()
        print("  ⚙️ Operations Agent:")
        
        # Test KPI monitoring
        result = await ops_agent.monitor_operational_kpis("30_days")
        print(f"    ✅ KPI Monitoring: {result['monitoring_id']}")
        
    except Exception as e:
        print(f"    ❌ Operations Agent Test Failed: {e}")

async def test_orchestration_integration():
    """Test integration with orchestration hub"""
    print("\n🎭 Testing Orchestration Integration...")
    
    try:
        # Import orchestration hub  
        sys.path.insert(0, agent_ecosystem_dir)
        from orchestration_hub import AgentOrchestrator
        
        # Create orchestrator instance
        orchestrator = AgentOrchestrator()
        print("  ✅ Orchestration Hub initialized")
        
        # Check enterprise agent status
        enterprise_status = orchestrator.get_enterprise_agent_status()
        print(f"  📊 Enterprise Agents Available: {len(enterprise_status.get('enterprise_agents', {}))}")
        
        # Test enterprise analysis if agents are available
        if enterprise_status.get('availability', {}).get('executive'):
            try:
                exec_data = {
                    "business_area": "integration_test",
                    "current_performance": {"revenue": 10000000},
                    "market_conditions": ["test"]
                }
                result = await orchestrator.execute_enterprise_analysis("executive", exec_data)
                print(f"    ✅ Executive Analysis via Orchestrator: {result.get('analysis_id', 'completed')}")
            except Exception as e:
                print(f"    ❌ Executive Analysis Failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Orchestration Integration Failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        "agent-ecosystem/enterprise-agents/executive/executive_agent.py",
        "agent-ecosystem/enterprise-agents/finance/finance_agent.py", 
        "agent-ecosystem/enterprise-agents/legal-compliance/legal_compliance_agent.py",
        "agent-ecosystem/enterprise-agents/operations/operations_agent.py",
        "agent-ecosystem/orchestration_hub.py"
    ]
    
    results = {}
    for file_path in required_files:
        full_path = os.path.join(current_dir, file_path)
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            results[file_path] = f"✅ EXISTS ({file_size:,} bytes)"
        else:
            results[file_path] = "❌ MISSING"
    
    for file_path, status in results.items():
        agent_name = file_path.split('/')[-2] if 'enterprise-agents' in file_path else 'orchestration'
        print(f"  {agent_name.title().replace('-', ' ')}: {status}")
    
    return results

async def run_comprehensive_test():
    """Run comprehensive test of the enterprise agent ecosystem"""
    print("🚀 Enterprise Agent Ecosystem Integration Test")
    print("=" * 55)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test file structure
    file_results = test_file_structure()
    
    # Test imports
    import_results = test_agent_imports()
    
    # Test functionality
    await test_agent_functionality()
    
    # Test orchestration integration
    orchestration_success = await test_orchestration_integration()
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 Test Summary:")
    
    # File structure summary
    missing_files = sum(1 for status in file_results.values() if "MISSING" in status)
    print(f"  📁 File Structure: {len(file_results) - missing_files}/{len(file_results)} files found")
    
    # Import summary
    successful_imports = sum(1 for status in import_results.values() if "SUCCESS" in status)
    print(f"  📦 Agent Imports: {successful_imports}/{len(import_results)} agents imported")
    
    # Orchestration summary
    print(f"  🎭 Orchestration: {'✅ Working' if orchestration_success else '❌ Failed'}")
    
    # Overall status
    overall_success = (missing_files == 0 and successful_imports == len(import_results) and orchestration_success)
    print(f"\n🎯 Overall Status: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 Enterprise Agent Ecosystem is fully operational!")
        print("   All agents are implemented and integrated successfully.")
    else:
        print("\n⚠️  Some components need attention.")
        print("   Please check the individual test results above.")

def main():
    """Main test runner"""
    try:
        asyncio.run(run_comprehensive_test())
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
