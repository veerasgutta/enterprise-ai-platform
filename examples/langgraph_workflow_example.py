"""
🎓 LEARNING PROJECT - LangGraph Workflow Example
Demonstrates state machine-based agent workflow

This shows how LangGraph enables predictable, debuggable agent workflows
using state machines. Much more controlled than pure conversation-based agents.

Author: Personal learning project
Purpose: Understanding state-based agent orchestration
"""

from typing import TypedDict, Annotated, Sequence
from enum import Enum
import operator


# State definition for the workflow
class WorkflowState(TypedDict):
    """
    Defines the state that flows through the graph.
    In real LangGraph, this would include messages, context, etc.
    """
    task: str
    analysis: str
    plan: list[str]
    results: list[str]
    current_step: int
    status: str


class AgentStep(Enum):
    """Enumeration of workflow steps"""
    ANALYZE = "analyze"
    PLAN = "plan"
    EXECUTE = "execute"
    REVIEW = "review"
    COMPLETE = "complete"


class LangGraphStyleWorkflow:
    """
    Simplified example of LangGraph-style state machine workflow.
    
    Key concepts demonstrated:
    - State flows through defined nodes
    - Conditional edges determine paths
    - Each step transforms the state
    - Predictable execution order
    
    Real LangGraph features not shown here:
    - LLM integration
    - Complex conditional logic
    - Error handling and retries
    - Parallel execution
    - Human-in-the-loop
    """
    
    def __init__(self):
        self.state = None
    
    def analyze_node(self, state: WorkflowState) -> WorkflowState:
        """
        Analysis node: Breaks down the task into components.
        
        In production: Would use LLM to analyze complexity,
        extract requirements, identify dependencies.
        """
        print(f"\n📊 ANALYZE: {state['task']}")
        
        # Simulate analysis
        state["analysis"] = f"Analysis of '{state['task']}': requires data gathering, processing, and reporting"
        state["status"] = "analyzed"
        
        print(f"   ✓ Analysis complete")
        return state
    
    def plan_node(self, state: WorkflowState) -> WorkflowState:
        """
        Planning node: Creates execution plan.
        
        In production: LLM would generate step-by-step plan
        considering dependencies, resources, timeline.
        """
        print(f"\n📋 PLAN: Creating execution strategy")
        
        # Simulate planning
        state["plan"] = [
            "Step 1: Gather required data",
            "Step 2: Process and analyze",
            "Step 3: Generate insights",
            "Step 4: Create report"
        ]
        state["current_step"] = 0
        state["status"] = "planned"
        
        print(f"   ✓ Created {len(state['plan'])}-step plan")
        return state
    
    def execute_node(self, state: WorkflowState) -> WorkflowState:
        """
        Execution node: Performs actual work.
        
        In production: Would call tools, APIs, databases,
        or delegate to specialized agents.
        """
        step_num = state["current_step"]
        if step_num < len(state["plan"]):
            current_task = state["plan"][step_num]
            print(f"\n⚡ EXECUTE: {current_task}")
            
            # Simulate execution
            result = f"Completed: {current_task}"
            state["results"].append(result)
            state["current_step"] += 1
            
            print(f"   ✓ Step {step_num + 1} complete")
        
        # Check if all steps done
        if state["current_step"] >= len(state["plan"]):
            state["status"] = "executed"
        
        return state
    
    def review_node(self, state: WorkflowState) -> WorkflowState:
        """
        Review node: Quality check results.
        
        In production: LLM would verify outputs meet requirements,
        check for errors, ensure quality standards.
        """
        print(f"\n🔍 REVIEW: Checking {len(state['results'])} results")
        
        # Simulate review
        quality_score = len(state["results"]) / len(state["plan"]) * 100
        
        if quality_score >= 100:
            state["status"] = "approved"
            print(f"   ✓ Quality check passed ({quality_score:.0f}%)")
        else:
            state["status"] = "needs_retry"
            print(f"   ⚠ Quality check failed ({quality_score:.0f}%)")
        
        return state
    
    def should_continue_execution(self, state: WorkflowState) -> str:
        """
        Conditional edge: Determines next step.
        
        This is a key LangGraph feature - routing based on state.
        """
        if state["current_step"] < len(state["plan"]):
            return "continue"  # Go back to execute
        else:
            return "done"  # Move to review
    
    def should_retry(self, state: WorkflowState) -> str:
        """
        Conditional edge: Determines if retry needed.
        """
        if state["status"] == "needs_retry":
            return "retry"
        else:
            return "complete"
    
    def run(self, initial_task: str) -> WorkflowState:
        """
        Execute the workflow graph.
        
        In real LangGraph:
        - Uses graph.compile() to create executable
        - Handles async execution
        - Provides streaming updates
        - Supports checkpointing for retries
        """
        print("="*60)
        print("🚀 LangGraph-Style Workflow Execution")
        print("="*60)
        
        # Initialize state
        state: WorkflowState = {
            "task": initial_task,
            "analysis": "",
            "plan": [],
            "results": [],
            "current_step": 0,
            "status": "pending"
        }
        
        # Execute graph: analyze -> plan -> execute (loop) -> review
        state = self.analyze_node(state)
        state = self.plan_node(state)
        
        # Execute loop (simplified - real LangGraph handles this elegantly)
        while self.should_continue_execution(state) == "continue":
            state = self.execute_node(state)
        
        state = self.review_node(state)
        
        # Final status
        print("\n" + "="*60)
        if state["status"] == "approved":
            print("✅ Workflow completed successfully!")
        else:
            print("⚠️ Workflow needs attention")
        print("="*60)
        
        return state


def demo_langgraph_workflow():
    """
    Demonstrates key LangGraph concepts through simplified example.
    
    What I learned about LangGraph:
    
    ✅ Pros:
    - Predictable execution paths
    - Easy to visualize and debug
    - Great for complex workflows
    - Built-in state management
    - Can handle retries and errors
    
    ❌ Cons:
    - More boilerplate than AutoGen
    - Steeper learning curve
    - Requires more upfront design
    - Less "magical" feel
    
    When to use LangGraph:
    - Complex workflows with many steps
    - Need to debug execution paths
    - Want predictable behavior
    - Building production systems
    - Need state persistence
    """
    
    print("\n🎓 LangGraph Workflow Learning Example")
    print("=" * 60)
    print("\n💡 Key Concepts Demonstrated:")
    print("   • State machines for agent control")
    print("   • Conditional routing between nodes")
    print("   • Predictable execution flows")
    print("   • Step-by-step progress tracking")
    print("\n" + "="*60)
    
    # Create and run workflow
    workflow = LangGraphStyleWorkflow()
    result = workflow.run("Analyze Q4 sales data and create executive report")
    
    # Show final state
    print("\n📊 Final Workflow State:")
    print(f"   Task: {result['task']}")
    print(f"   Steps Planned: {len(result['plan'])}")
    print(f"   Steps Completed: {len(result['results'])}")
    print(f"   Status: {result['status']}")
    
    print("\n💡 Key Takeaway:")
    print("   LangGraph's state machine approach gives you CONTROL")
    print("   over agent behavior - perfect for production systems!")


if __name__ == "__main__":
    demo_langgraph_workflow()
