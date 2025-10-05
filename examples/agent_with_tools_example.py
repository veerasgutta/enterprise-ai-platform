"""
🎓 LEARNING PROJECT - Agent with Tools Example
Demonstrates how agents use tools/functions to interact with external systems

This shows the "function calling" pattern where LLMs can decide to call
functions/APIs based on the task. Critical for practical agent applications.

Author: Personal learning project
Purpose: Understanding tool integration in agent systems
"""

from typing import Callable, Any
import json
from datetime import datetime


class Tool:
    """
    Represents a tool that an agent can use.
    
    In production frameworks (LangChain, Semantic Kernel):
    - Auto-generates function descriptions for LLM
    - Handles parameter validation
    - Manages async execution
    - Provides error handling
    """
    
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters"""
        return self.func(**kwargs)
    
    def to_llm_format(self) -> dict:
        """
        Convert tool to format LLM can understand.
        
        Real frameworks generate this automatically from
        function signatures and docstrings.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": "Dynamic based on function signature"
        }


# Define example tools (in real systems, these would be actual APIs/databases)
def search_database(query: str) -> str:
    """
    Search internal database for information.
    
    In production: Would query actual database, vector store,
    or knowledge base with semantic search.
    """
    print(f"   🔍 Tool: Searching database for '{query}'")
    
    # Simulate database results
    mock_results = {
        "sales": "Q4 sales increased 23% YoY to $4.2M",
        "customers": "Customer count grew from 1,200 to 1,450",
        "revenue": "Monthly recurring revenue at $350K",
    }
    
    # Simple keyword matching (real version uses embeddings)
    for key, value in mock_results.items():
        if key in query.lower():
            return f"Database result: {value}"
    
    return "No results found"


def send_email(to: str, subject: str, body: str) -> str:
    """
    Send email notification.
    
    In production: Would integrate with email service
    (SendGrid, AWS SES, etc.)
    """
    print(f"   📧 Tool: Sending email to {to}")
    print(f"      Subject: {subject}")
    
    # Simulate sending
    return f"Email sent successfully to {to}"


def create_report(title: str, content: str) -> str:
    """
    Generate formatted report.
    
    In production: Would create PDF, save to storage,
    or integrate with reporting tools.
    """
    print(f"   📄 Tool: Creating report '{title}'")
    
    report = f"""
╔══════════════════════════════════════════════════════╗
║  REPORT: {title:<40} ║
╠══════════════════════════════════════════════════════╣
║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}                          ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  {content:<50} ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""
    return report


def calculate_metrics(metric_type: str, value1: float, value2: float) -> str:
    """
    Perform calculations on metrics.
    
    In production: Would integrate with analytics platforms,
    use complex statistical models.
    """
    print(f"   🔢 Tool: Calculating {metric_type}")
    
    if metric_type == "growth_rate":
        growth = ((value2 - value1) / value1) * 100
        return f"Growth rate: {growth:.1f}%"
    elif metric_type == "average":
        avg = (value1 + value2) / 2
        return f"Average: {avg:.2f}"
    else:
        return f"Metric calculated: {value1 + value2}"


class AgentWithTools:
    """
    Agent that can use tools to accomplish tasks.
    
    Key concepts demonstrated:
    - Tool registration
    - Tool selection logic (simplified)
    - Tool execution
    - Result processing
    
    Real implementations (LangChain, AutoGen):
    - LLM decides which tools to use
    - Handles multi-step tool usage
    - Manages tool errors gracefully
    - Supports parallel tool execution
    """
    
    def __init__(self, name: str):
        self.name = name
        self.tools: dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool):
        """Register a tool for the agent to use"""
        self.tools[tool.name] = tool
        print(f"✅ Registered tool: {tool.name}")
    
    def list_tools(self) -> list[dict]:
        """Get list of available tools (for LLM context)"""
        return [tool.to_llm_format() for tool in self.tools.values()]
    
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a specific tool.
        
        In production: LLM chooses tool and parameters based on task.
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"
        
        tool = self.tools[tool_name]
        try:
            result = tool.execute(**kwargs)
            return result
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def solve_task(self, task: str) -> str:
        """
        Solve a task using available tools.
        
        Simplified logic - real agents use LLM to decide:
        1. Which tools to use
        2. In what order
        3. With what parameters
        4. How to combine results
        """
        print(f"\n🤖 Agent '{self.name}' solving: {task}\n")
        
        # Simplified tool selection logic
        # (Real version: LLM analyzes task and chooses tools)
        
        if "sales" in task.lower() or "revenue" in task.lower():
            # Step 1: Search for data
            data = self.use_tool("search_database", query="sales revenue")
            
            # Step 2: Create report
            report = self.use_tool(
                "create_report",
                title="Q4 Sales Analysis",
                content=data
            )
            
            # Step 3: Send notification
            email_result = self.use_tool(
                "send_email",
                to="executive@company.com",
                subject="Q4 Sales Report Ready",
                body="Please review the attached Q4 analysis."
            )
            
            return f"Task completed!\n{report}\n{email_result}"
        
        else:
            return "Task completed using available tools"


def demo_agent_with_tools():
    """
    Demonstrates agent-tool integration patterns.
    
    What I learned about tool usage:
    
    ✅ Critical for practical agents:
    - Agents need external data/actions
    - Tools extend agent capabilities
    - Function calling is core feature
    - Proper error handling crucial
    
    ⚠️ Challenges discovered:
    - Tool description quality matters
    - Parameter validation is complex
    - Chaining tools requires planning
    - Security considerations important
    
    Best practices:
    - Clear, detailed tool descriptions
    - Input validation and sanitization
    - Proper error messages
    - Rate limiting for expensive tools
    - Logging for debugging
    """
    
    print("="*60)
    print("🎓 Agent with Tools - Learning Example")
    print("="*60)
    print("\n💡 Demonstrates:")
    print("   • Tool registration and discovery")
    print("   • Agent using multiple tools")
    print("   • Multi-step task execution")
    print("   • Result processing and reporting")
    
    print("\n" + "="*60)
    print("🔧 Registering Tools...")
    print("="*60)
    
    # Create agent
    agent = AgentWithTools(name="Business Analyst")
    
    # Register tools
    agent.register_tool(Tool(
        name="search_database",
        description="Search company database for information",
        func=search_database
    ))
    
    agent.register_tool(Tool(
        name="send_email",
        description="Send email notifications",
        func=send_email
    ))
    
    agent.register_tool(Tool(
        name="create_report",
        description="Generate formatted reports",
        func=create_report
    ))
    
    agent.register_tool(Tool(
        name="calculate_metrics",
        description="Calculate business metrics",
        func=calculate_metrics
    ))
    
    # Execute task
    print("\n" + "="*60)
    print("🚀 Executing Task...")
    print("="*60)
    
    result = agent.solve_task(
        "Generate Q4 sales report and notify executives"
    )
    
    print("\n" + "="*60)
    print("📊 Task Result:")
    print("="*60)
    print(result)
    
    print("\n" + "="*60)
    print("💡 Key Takeaways:")
    print("="*60)
    print("   1. Tools are HOW agents interact with the world")
    print("   2. Good tool descriptions help LLMs choose correctly")
    print("   3. Multi-step tool usage requires orchestration")
    print("   4. Real frameworks (LangChain, etc.) automate this!")
    print("\n   🎯 Function calling is THE key to practical AI agents")


if __name__ == "__main__":
    demo_agent_with_tools()
