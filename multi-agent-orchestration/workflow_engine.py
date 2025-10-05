"""
🎓 LEARNING PROJECT - Educational Example

This code is part of a personal learning project exploring enterprise AI patterns.
Created for educational purposes and portfolio demonstration.

⚠️ NOT PRODUCTION CODE - For learning and demonstration only.

Technologies: Multi-agent systems, AI orchestration, enterprise architecture
Author: Personal learning project
License: Educational use only
"""
"""
🔄 Multi-Agent Workflow Engine
Advanced workflow orchestration for enterprise AI agents

This module provides comprehensive workflow management for coordinating
multiple AI agents in complex business processes and decision-making scenarios.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable, Union
from datetime import datetime, timedelta
from enum import Enum
import logging
import uuid

class WorkflowStatus(Enum):
    """Workflow execution status"""
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentStatus(Enum):
    """Agent status within workflow"""
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowAgent:
    """Individual agent participating in workflow"""
    
    def __init__(self, agent_id: str, agent_type: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.current_task = None
        self.execution_history = []
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 100.0,
            "average_execution_time": 0.0
        }
        self.logger = logging.getLogger(__name__)
    
    async def execute_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a task assigned to this agent"""
        self.status = AgentStatus.RUNNING
        self.current_task = task
        start_time = datetime.now()
        
        self.logger.info(f"Agent {self.agent_id} executing task: {task.get('name', 'unnamed')}")
        
        try:
            # Execute based on agent type
            if self.agent_type == "project_manager":
                result = await self._execute_project_management_task(task, context or {})
            elif self.agent_type == "data_analyst":
                result = await self._execute_data_analysis_task(task, context or {})
            elif self.agent_type == "business_analyst":
                result = await self._execute_business_analysis_task(task, context or {})
            elif self.agent_type == "security_analyst":
                result = await self._execute_security_task(task, context or {})
            elif self.agent_type == "quality_assurance":
                result = await self._execute_qa_task(task, context or {})
            else:
                result = await self._execute_generic_task(task, context or {})
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update performance metrics
            self.performance_metrics["tasks_completed"] += 1
            self.performance_metrics["average_execution_time"] = (
                (self.performance_metrics["average_execution_time"] * (self.performance_metrics["tasks_completed"] - 1) + execution_time) /
                self.performance_metrics["tasks_completed"]
            )
            
            # Record execution
            execution_record = {
                "task_id": task.get("id", str(uuid.uuid4())),
                "task_name": task.get("name", "unnamed"),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "result_summary": str(result.get("summary", "Task completed"))
            }
            self.execution_history.append(execution_record)
            
            self.status = AgentStatus.COMPLETED
            self.current_task = None
            
            return {
                "agent_id": self.agent_id,
                "task_result": result,
                "execution_time": execution_time,
                "status": "success"
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Agent {self.agent_id} failed task execution: {e}")
            
            # Update failure metrics
            total_tasks = self.performance_metrics["tasks_completed"] + 1
            self.performance_metrics["success_rate"] = (
                self.performance_metrics["tasks_completed"] / total_tasks * 100
            )
            
            execution_record = {
                "task_id": task.get("id", str(uuid.uuid4())),
                "task_name": task.get("name", "unnamed"),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "error": str(e)
            }
            self.execution_history.append(execution_record)
            
            self.status = AgentStatus.FAILED
            self.current_task = None
            
            return {
                "agent_id": self.agent_id,
                "status": "failed",
                "error": str(e),
                "execution_time": execution_time
            }
    
    async def _execute_project_management_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute project management specific task"""
        task_type = task.get("type", "general")
        
        if task_type == "create_timeline":
            return {
                "summary": "Project timeline created",
                "timeline": {
                    "phase_1": "Requirements (2 weeks)",
                    "phase_2": "Development (8 weeks)", 
                    "phase_3": "Testing (3 weeks)",
                    "phase_4": "Deployment (1 week)"
                },
                "total_duration": "14 weeks",
                "critical_path": ["Requirements", "Development", "Testing"]
            }
        elif task_type == "risk_assessment":
            return {
                "summary": "Risk assessment completed",
                "risks_identified": [
                    {"risk": "Resource availability", "probability": "Medium", "impact": "High"},
                    {"risk": "Technology changes", "probability": "Low", "impact": "Medium"},
                    {"risk": "Scope creep", "probability": "High", "impact": "Medium"}
                ],
                "mitigation_strategies": [
                    "Secure backup resources",
                    "Implement change control process",
                    "Define clear scope boundaries"
                ]
            }
        else:
            return {
                "summary": f"Project management task '{task_type}' completed",
                "recommendations": ["Continue monitoring project progress", "Update stakeholders"]
            }
    
    async def _execute_data_analysis_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data analysis specific task"""
        return {
            "summary": "Data analysis completed",
            "data_processed": {
                "records_analyzed": 50000,
                "data_quality_score": 0.92,
                "processing_time": "3.4s"
            },
            "insights": [
                "Customer engagement increased by 15%",
                "Product usage peaked during weekends",
                "Support ticket volume decreased by 8%"
            ],
            "recommendations": [
                "Focus marketing on weekend campaigns",
                "Optimize support resources",
                "Enhance engagement features"
            ]
        }
    
    async def _execute_business_analysis_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute business analysis specific task"""
        return {
            "summary": "Business analysis completed",
            "business_impact": {
                "revenue_potential": "$2.4M",
                "cost_savings": "$450K",
                "roi_percentage": 35.5
            },
            "market_analysis": {
                "market_size": "$12.8B",
                "growth_rate": "12.3%",
                "competitive_position": "Strong"
            },
            "strategic_recommendations": [
                "Expand to new market segments",
                "Invest in automation technologies",
                "Strengthen customer relationships"
            ]
        }
    
    async def _execute_security_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute security analysis task"""
        return {
            "summary": "Security analysis completed",
            "security_assessment": {
                "vulnerability_scan": "Clean",
                "compliance_score": 94,
                "threat_level": "Low"
            },
            "findings": [
                "All systems up to date",
                "Access controls properly configured",
                "No critical vulnerabilities detected"
            ],
            "recommendations": [
                "Continue regular security updates",
                "Conduct quarterly penetration testing",
                "Review access permissions monthly"
            ]
        }
    
    async def _execute_qa_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute quality assurance task"""
        return {
            "summary": "Quality assurance testing completed",
            "test_results": {
                "tests_executed": 245,
                "tests_passed": 240,
                "pass_rate": 97.96,
                "critical_issues": 0
            },
            "quality_metrics": {
                "code_coverage": "89%",
                "performance_score": 92,
                "usability_score": 88
            },
            "recommendations": [
                "Address remaining test failures",
                "Improve code coverage in module X",
                "Optimize performance for mobile users"
            ]
        }
    
    async def _execute_generic_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic task"""
        return {
            "summary": f"Generic task completed by {self.agent_type}",
            "task_details": task,
            "context_processed": len(context),
            "capabilities_used": self.capabilities[:2]  # Show first 2 capabilities
        }

class WorkflowTask:
    """Individual task within a workflow"""
    
    def __init__(self, task_id: str, name: str, task_type: str, required_capabilities: List[str]):
        self.task_id = task_id
        self.name = name
        self.task_type = task_type
        self.required_capabilities = required_capabilities
        self.dependencies = []
        self.assigned_agent = None
        self.status = "created"
        self.result = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
    
    def add_dependency(self, task_id: str) -> None:
        """Add a dependency to this task"""
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
    
    def can_execute(self, completed_tasks: List[str]) -> bool:
        """Check if task can be executed based on dependencies"""
        return all(dep in completed_tasks for dep in self.dependencies)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            "id": self.task_id,
            "name": self.name,
            "type": self.task_type,
            "required_capabilities": self.required_capabilities,
            "dependencies": self.dependencies,
            "assigned_agent": self.assigned_agent,
            "status": self.status
        }

class MultiAgentWorkflowEngine:
    """Main workflow engine for coordinating multiple agents"""
    
    def __init__(self, workflow_name: str):
        self.workflow_name = workflow_name
        self.workflow_id = str(uuid.uuid4())
        self.agents = {}
        self.tasks = {}
        self.status = WorkflowStatus.CREATED
        self.execution_plan = []
        self.completed_tasks = []
        self.failed_tasks = []
        self.start_time = None
        self.end_time = None
        self.logger = logging.getLogger(__name__)
        
    def register_agent(self, agent: WorkflowAgent) -> None:
        """Register an agent with the workflow engine"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent {agent.agent_id} ({agent.agent_type})")
    
    def add_task(self, task: WorkflowTask) -> None:
        """Add a task to the workflow"""
        self.tasks[task.task_id] = task
        self.logger.info(f"Added task {task.task_id}: {task.name}")
    
    def _find_suitable_agent(self, task: WorkflowTask) -> Optional[WorkflowAgent]:
        """Find the most suitable agent for a task"""
        suitable_agents = []
        
        for agent in self.agents.values():
            if agent.status in [AgentStatus.IDLE, AgentStatus.COMPLETED]:
                # Check if agent has required capabilities
                if any(cap in agent.capabilities for cap in task.required_capabilities):
                    suitable_agents.append(agent)
        
        if not suitable_agents:
            return None
        
        # Select agent with best performance metrics
        return max(suitable_agents, key=lambda a: a.performance_metrics["success_rate"])
    
    async def execute_workflow(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the complete workflow"""
        self.status = WorkflowStatus.RUNNING
        self.start_time = datetime.now()
        context = context or {}
        
        self.logger.info(f"Starting workflow execution: {self.workflow_name}")
        
        execution_results = []
        
        try:
            while len(self.completed_tasks) < len(self.tasks):
                # Find tasks that can be executed
                executable_tasks = [
                    task for task in self.tasks.values()
                    if (task.status == "created" and 
                        task.can_execute(self.completed_tasks))
                ]
                
                if not executable_tasks:
                    # Check if there are any running tasks
                    running_tasks = [task for task in self.tasks.values() if task.status == "running"]
                    if not running_tasks:
                        self.logger.warning("No executable tasks found and no tasks running. Workflow may be stuck.")
                        break
                    
                    # Wait a bit for running tasks to complete
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute tasks in parallel where possible
                task_executions = []
                for task in executable_tasks:
                    agent = self._find_suitable_agent(task)
                    if agent:
                        task.assigned_agent = agent.agent_id
                        task.status = "running"
                        task.started_at = datetime.now()
                        
                        task_execution = self._execute_task_with_agent(task, agent, context)
                        task_executions.append(task_execution)
                
                # Wait for all parallel executions to complete
                if task_executions:
                    results = await asyncio.gather(*task_executions, return_exceptions=True)
                    
                    for i, result in enumerate(results):
                        task = executable_tasks[i]
                        if isinstance(result, Exception):
                            task.status = "failed"
                            self.failed_tasks.append(task.task_id)
                            self.logger.error(f"Task {task.task_id} failed: {result}")
                        else:
                            task.status = "completed"
                            task.completed_at = datetime.now()
                            task.result = result
                            self.completed_tasks.append(task.task_id)
                            execution_results.append(result)
                            self.logger.info(f"Task {task.task_id} completed successfully")
            
            self.status = WorkflowStatus.COMPLETED
            self.end_time = datetime.now()
            
            return {
                "workflow_id": self.workflow_id,
                "workflow_name": self.workflow_name,
                "status": self.status.value,
                "execution_results": execution_results,
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "total_tasks": len(self.tasks),
                "execution_time": (self.end_time - self.start_time).total_seconds(),
                "agent_performance": {
                    agent_id: agent.performance_metrics 
                    for agent_id, agent in self.agents.items()
                }
            }
            
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            self.end_time = datetime.now()
            self.logger.error(f"Workflow execution failed: {e}")
            
            return {
                "workflow_id": self.workflow_id,
                "workflow_name": self.workflow_name,
                "status": self.status.value,
                "error": str(e),
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "execution_time": (self.end_time - self.start_time).total_seconds() if self.end_time else 0
            }
    
    async def _execute_task_with_agent(self, task: WorkflowTask, agent: WorkflowAgent, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task with an assigned agent"""
        task_dict = task.to_dict()
        result = await agent.execute_task(task_dict, context)
        
        return {
            "task_id": task.task_id,
            "task_name": task.name,
            "agent_id": agent.agent_id,
            "result": result
        }

# Demo function
async def demo_workflow_engine():
    """Demonstrate the multi-agent workflow engine"""
    
    # Create workflow engine
    engine = MultiAgentWorkflowEngine("Enterprise Project Analysis")
    
    # Create and register agents
    agents = [
        WorkflowAgent("pm_001", "project_manager", ["planning", "coordination", "risk_management"]),
        WorkflowAgent("da_001", "data_analyst", ["data_processing", "analytics", "reporting"]),
        WorkflowAgent("ba_001", "business_analyst", ["business_analysis", "strategy", "market_research"]),
        WorkflowAgent("sa_001", "security_analyst", ["security_assessment", "compliance", "risk_analysis"]),
        WorkflowAgent("qa_001", "quality_assurance", ["testing", "quality_control", "validation"])
    ]
    
    for agent in agents:
        engine.register_agent(agent)
    
    # Create workflow tasks
    tasks = [
        WorkflowTask("task_1", "Initial Data Collection", "data_analysis", ["data_processing"]),
        WorkflowTask("task_2", "Project Planning", "project_management", ["planning"]),
        WorkflowTask("task_3", "Business Impact Analysis", "business_analysis", ["business_analysis"]),
        WorkflowTask("task_4", "Security Assessment", "security_analysis", ["security_assessment"]),
        WorkflowTask("task_5", "Quality Review", "quality_assurance", ["testing"])
    ]
    
    # Set up task dependencies
    tasks[1].add_dependency("task_1")  # Planning depends on data collection
    tasks[2].add_dependency("task_1")  # Business analysis depends on data collection
    tasks[4].add_dependency("task_2")  # Quality review depends on planning
    tasks[4].add_dependency("task_3")  # Quality review depends on business analysis
    
    # Add tasks to engine
    for task in tasks:
        engine.add_task(task)
    
    # Execute workflow
    context = {
        "project_name": "Enterprise AI Platform v2.0",
        "budget": 500000,
        "timeline": "6 months",
        "stakeholders": ["CTO", "VP Engineering", "Product Manager"]
    }
    
    result = await engine.execute_workflow(context)
    
    print("🔄 Multi-Agent Workflow Engine Results:")
    print(json.dumps(result, indent=2, default=str))
    
    return result

if __name__ == "__main__":
    print("🚀 Starting Multi-Agent Workflow Engine Demo...")
    asyncio.run(demo_workflow_engine())
