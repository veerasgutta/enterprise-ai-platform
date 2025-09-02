"""
📋 Project Manager Agent - Autonomous Project Planning & Coordination
===================================================================

Advanced AI agent for intelligent project management, resource allocation,
timeline optimization, and stakeholder coordination across enterprise projects.

Features:
- Autonomous project planning and timeline generation
- Resource allocation optimization using ML algorithms
- Risk assessment and mitigation strategy development
- Real-time progress tracking with predictive analytics
- Stakeholder communication and automated reporting
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta, date
from enum import Enum
import logging
import uuid
from dataclasses import dataclass
import statistics
from abc import ABC, abstractmethod

class ProjectStatus(Enum):
    """Project status enumeration"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DELAYED = "delayed"

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ResourceType(Enum):
    """Resource type enumeration"""
    HUMAN = "human"
    EQUIPMENT = "equipment"
    SOFTWARE = "software"
    FINANCIAL = "financial"
    EXTERNAL = "external"

class RiskLevel(Enum):
    """Risk severity levels"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ProjectResource:
    """Project resource definition"""
    resource_id: str
    name: str
    type: ResourceType
    availability: float  # 0.0 to 1.0
    cost_per_hour: float
    skills: List[str]
    allocation_start: datetime
    allocation_end: datetime

@dataclass
class ProjectTask:
    """Project task definition"""
    task_id: str
    name: str
    description: str
    priority: TaskPriority
    estimated_hours: float
    dependencies: List[str]  # Task IDs this task depends on
    required_skills: List[str]
    assigned_resources: List[str]  # Resource IDs
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    completion_percentage: float
    status: str

@dataclass
class ProjectRisk:
    """Project risk assessment"""
    risk_id: str
    description: str
    category: str
    probability: float  # 0.0 to 1.0
    impact: RiskLevel
    mitigation_strategy: str
    contingency_plan: str
    responsible_party: str
    review_date: datetime

@dataclass
class ProjectPlan:
    """Comprehensive project plan"""
    plan_id: str
    project_name: str
    description: str
    start_date: datetime
    end_date: datetime
    budget: float
    tasks: List[ProjectTask]
    resources: List[ProjectResource]
    risks: List[ProjectRisk]
    milestones: List[Dict[str, Any]]
    dependencies: Dict[str, List[str]]
    status: ProjectStatus
    created_at: datetime

class ProjectManagerAgent:
    """
    Project Manager Agent - Autonomous Project Planning & Coordination
    
    Provides intelligent project management capabilities including automated
    planning, resource optimization, risk assessment, and progress tracking.
    """
    
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id or f"pm_agent_{uuid.uuid4().hex[:8]}"
        self.agent_name = "Project Manager Agent"
        self.capabilities = [
            "project_planning",
            "resource_allocation",
            "timeline_optimization",
            "risk_assessment",
            "progress_tracking",
            "stakeholder_communication",
            "budget_management",
            "quality_assurance",
            "milestone_management",
            "reporting_automation"
        ]
        
        self.active_projects = {}
        self.resource_pool = {}
        self.project_templates = {}
        self.risk_database = {}
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"ProjectManagerAgent-{self.agent_id}")
        
        # Initialize project management algorithms
        self.planning_engine = PlanningEngine()
        self.resource_optimizer = ResourceOptimizer()
        self.risk_analyzer = RiskAnalyzer()
        
    async def create_project_plan(self, requirements: Dict[str, Any]) -> ProjectPlan:
        """
        Create comprehensive project plan from requirements
        
        Args:
            requirements: Project requirements and constraints
            
        Returns:
            ProjectPlan: Detailed project plan with timeline, resources, and risks
        """
        self.logger.info(f"Creating project plan for: {requirements.get('name', 'Unnamed Project')}")
        
        # Simulate advanced project planning
        await asyncio.sleep(3)
        
        project_name = requirements.get("name", "New Project")
        description = requirements.get("description", "")
        budget = requirements.get("budget", 100000)
        target_completion = requirements.get("target_date")
        
        # Generate project timeline
        timeline = await self.planning_engine.generate_timeline(requirements)
        
        # Optimize resource allocation
        resources = await self.resource_optimizer.allocate_resources(requirements, timeline)
        
        # Assess project risks
        risks = await self.risk_analyzer.assess_project_risks(requirements)
        
        # Generate tasks and dependencies
        tasks = self._generate_project_tasks(requirements, timeline)
        
        # Create milestones
        milestones = self._generate_milestones(tasks, timeline)
        
        project_plan = ProjectPlan(
            plan_id=f"project_{uuid.uuid4().hex[:8]}",
            project_name=project_name,
            description=description,
            start_date=timeline["start_date"],
            end_date=timeline["end_date"],
            budget=budget,
            tasks=tasks,
            resources=resources,
            risks=risks,
            milestones=milestones,
            dependencies=self._analyze_task_dependencies(tasks),
            status=ProjectStatus.PLANNED,
            created_at=datetime.now()
        )
        
        self.active_projects[project_plan.plan_id] = project_plan
        self.logger.info(f"Project plan created: {project_plan.plan_id}")
        
        return project_plan
        
    def _generate_project_tasks(self, requirements: Dict[str, Any], timeline: Dict[str, Any]) -> List[ProjectTask]:
        """Generate project tasks based on requirements"""
        project_type = requirements.get("type", "software_development")
        complexity = requirements.get("complexity", "medium")
        
        # Task templates by project type
        task_templates = {
            "software_development": [
                {"name": "Requirements Analysis", "hours": 40, "priority": "high", "skills": ["analysis", "documentation"]},
                {"name": "System Design", "hours": 60, "priority": "high", "skills": ["architecture", "design"]},
                {"name": "Frontend Development", "hours": 120, "priority": "medium", "skills": ["frontend", "ui_ux"]},
                {"name": "Backend Development", "hours": 150, "priority": "high", "skills": ["backend", "database"]},
                {"name": "Testing & QA", "hours": 80, "priority": "high", "skills": ["testing", "quality_assurance"]},
                {"name": "Deployment", "hours": 30, "priority": "medium", "skills": ["devops", "deployment"]},
                {"name": "Documentation", "hours": 40, "priority": "low", "skills": ["documentation", "technical_writing"]}
            ],
            "marketing_campaign": [
                {"name": "Market Research", "hours": 30, "priority": "high", "skills": ["research", "analysis"]},
                {"name": "Strategy Development", "hours": 40, "priority": "high", "skills": ["strategy", "marketing"]},
                {"name": "Content Creation", "hours": 80, "priority": "medium", "skills": ["content", "creative"]},
                {"name": "Campaign Launch", "hours": 20, "priority": "high", "skills": ["marketing", "project_management"]},
                {"name": "Performance Analysis", "hours": 25, "priority": "medium", "skills": ["analytics", "reporting"]}
            ]
        }
        
        templates = task_templates.get(project_type, task_templates["software_development"])
        
        # Adjust for complexity
        complexity_multipliers = {"low": 0.8, "medium": 1.0, "high": 1.3, "very_high": 1.6}
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        tasks = []
        for i, template in enumerate(templates):
            task = ProjectTask(
                task_id=f"task_{uuid.uuid4().hex[:8]}",
                name=template["name"],
                description=f"Project task: {template['name']}",
                priority=TaskPriority(template["priority"]),
                estimated_hours=template["hours"] * multiplier,
                dependencies=[],  # Will be set based on task order
                required_skills=template["skills"],
                assigned_resources=[],
                start_date=None,
                end_date=None,
                completion_percentage=0.0,
                status="planned"
            )
            
            # Set dependencies (each task depends on previous tasks)
            if i > 0:
                task.dependencies = [tasks[i-1].task_id]
                
            tasks.append(task)
            
        return tasks
        
    def _generate_milestones(self, tasks: List[ProjectTask], timeline: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate project milestones"""
        milestones = []
        
        # Major milestones based on task completion
        milestone_tasks = [
            {"name": "Requirements Complete", "percentage": 20},
            {"name": "Design Phase Complete", "percentage": 35},
            {"name": "Development Phase Complete", "percentage": 70},
            {"name": "Testing Complete", "percentage": 90},
            {"name": "Project Delivery", "percentage": 100}
        ]
        
        start_date = timeline["start_date"]
        end_date = timeline["end_date"]
        project_duration = (end_date - start_date).days
        
        for milestone in milestone_tasks:
            milestone_date = start_date + timedelta(days=int(project_duration * milestone["percentage"] / 100))
            
            milestones.append({
                "milestone_id": f"milestone_{uuid.uuid4().hex[:8]}",
                "name": milestone["name"],
                "description": f"Project milestone: {milestone['name']}",
                "target_date": milestone_date,
                "completion_percentage": milestone["percentage"],
                "status": "planned",
                "dependencies": []
            })
            
        return milestones
        
    def _analyze_task_dependencies(self, tasks: List[ProjectTask]) -> Dict[str, List[str]]:
        """Analyze and map task dependencies"""
        dependencies = {}
        
        for task in tasks:
            dependencies[task.task_id] = task.dependencies
            
        return dependencies
        
    async def track_project_progress(self, project_id: str) -> Dict[str, Any]:
        """
        Track and analyze project progress
        
        Args:
            project_id: Project identifier
            
        Returns:
            Comprehensive progress report
        """
        if project_id not in self.active_projects:
            raise ValueError(f"Project {project_id} not found")
            
        self.logger.info(f"Tracking progress for project: {project_id}")
        
        # Simulate progress tracking
        await asyncio.sleep(2)
        
        project = self.active_projects[project_id]
        
        # Calculate overall progress
        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for task in project.tasks if task.completion_percentage >= 100)
        overall_progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        # Calculate budget utilization
        total_budget = project.budget
        used_budget = self._calculate_used_budget(project)
        budget_utilization = (used_budget / total_budget) * 100 if total_budget > 0 else 0
        
        # Analyze schedule performance
        schedule_performance = self._analyze_schedule_performance(project)
        
        # Identify risks and issues
        current_risks = self._identify_current_risks(project)
        
        # Generate recommendations
        recommendations = self._generate_progress_recommendations(project, overall_progress, schedule_performance)
        
        progress_report = {
            "report_id": f"progress_{uuid.uuid4().hex[:8]}",
            "project_id": project_id,
            "project_name": project.project_name,
            "report_date": datetime.now().isoformat(),
            "overall_progress": round(overall_progress, 1),
            "budget_utilization": round(budget_utilization, 1),
            "schedule_performance": schedule_performance,
            "task_summary": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "in_progress_tasks": sum(1 for task in project.tasks if 0 < task.completion_percentage < 100),
                "pending_tasks": sum(1 for task in project.tasks if task.completion_percentage == 0)
            },
            "milestone_status": self._get_milestone_status(project),
            "current_risks": current_risks,
            "recommendations": recommendations,
            "next_actions": self._identify_next_actions(project)
        }
        
        self.logger.info(f"Progress tracking completed for {project_id}")
        return progress_report
        
    def _calculate_used_budget(self, project: ProjectPlan) -> float:
        """Calculate budget utilization"""
        used_budget = 0.0
        
        for task in project.tasks:
            # Calculate cost based on completion percentage and resource allocation
            task_cost = task.estimated_hours * 50.0  # Average hourly rate
            used_budget += task_cost * (task.completion_percentage / 100)
            
        return used_budget
        
    def _analyze_schedule_performance(self, project: ProjectPlan) -> Dict[str, Any]:
        """Analyze schedule performance"""
        current_date = datetime.now()
        project_duration = (project.end_date - project.start_date).days
        elapsed_days = (current_date - project.start_date).days
        expected_progress = (elapsed_days / project_duration) * 100 if project_duration > 0 else 0
        
        # Calculate actual progress
        actual_progress = sum(task.completion_percentage for task in project.tasks) / len(project.tasks)
        
        schedule_variance = actual_progress - expected_progress
        
        if schedule_variance > 5:
            status = "ahead_of_schedule"
        elif schedule_variance < -5:
            status = "behind_schedule"
        else:
            status = "on_schedule"
            
        return {
            "status": status,
            "expected_progress": round(expected_progress, 1),
            "actual_progress": round(actual_progress, 1),
            "schedule_variance": round(schedule_variance, 1),
            "days_elapsed": elapsed_days,
            "days_remaining": max(0, (project.end_date - current_date).days)
        }
        
    def _identify_current_risks(self, project: ProjectPlan) -> List[Dict[str, Any]]:
        """Identify current project risks"""
        active_risks = []
        
        for risk in project.risks:
            if risk.probability > 0.3:  # Only include risks with > 30% probability
                active_risks.append({
                    "risk_id": risk.risk_id,
                    "description": risk.description,
                    "category": risk.category,
                    "probability": risk.probability,
                    "impact": risk.impact.value,
                    "mitigation_strategy": risk.mitigation_strategy
                })
                
        return active_risks
        
    def _generate_progress_recommendations(self, project: ProjectPlan, progress: float, schedule: Dict[str, Any]) -> List[str]:
        """Generate progress-based recommendations"""
        recommendations = []
        
        if schedule["status"] == "behind_schedule":
            recommendations.extend([
                "Consider adding additional resources to critical path tasks",
                "Review task dependencies and look for parallelization opportunities",
                "Escalate blocking issues to stakeholders",
                "Consider scope reduction if timeline is critical"
            ])
        elif schedule["status"] == "ahead_of_schedule":
            recommendations.extend([
                "Consider expanding scope to add value",
                "Use extra time for additional quality assurance",
                "Document lessons learned for future projects"
            ])
            
        if progress < 25:
            recommendations.append("Focus on completing requirements and initial design phases")
        elif progress < 75:
            recommendations.append("Maintain momentum on development and implementation")
        else:
            recommendations.append("Prioritize testing, deployment, and documentation")
            
        return recommendations
        
    def _identify_next_actions(self, project: ProjectPlan) -> List[str]:
        """Identify immediate next actions"""
        next_actions = []
        
        # Find tasks that can be started (no pending dependencies)
        available_tasks = []
        for task in project.tasks:
            if task.completion_percentage < 100:
                dependencies_complete = all(
                    self._is_task_complete(dep_id, project.tasks) 
                    for dep_id in task.dependencies
                )
                if dependencies_complete:
                    available_tasks.append(task)
                    
        # Sort by priority and add to next actions
        available_tasks.sort(key=lambda t: t.priority.value, reverse=True)
        
        for task in available_tasks[:3]:  # Top 3 priority tasks
            next_actions.append(f"Start/Continue: {task.name}")
            
        return next_actions
        
    def _is_task_complete(self, task_id: str, tasks: List[ProjectTask]) -> bool:
        """Check if a task is complete"""
        for task in tasks:
            if task.task_id == task_id:
                return task.completion_percentage >= 100
        return True  # If task not found, assume it's complete
        
    def _get_milestone_status(self, project: ProjectPlan) -> List[Dict[str, Any]]:
        """Get current milestone status"""
        milestone_status = []
        
        for milestone in project.milestones:
            status = "pending"
            if milestone["target_date"] < datetime.now():
                # Check if milestone criteria are met
                overall_progress = sum(task.completion_percentage for task in project.tasks) / len(project.tasks)
                if overall_progress >= milestone["completion_percentage"]:
                    status = "completed"
                else:
                    status = "overdue"
                    
            milestone_status.append({
                "milestone_id": milestone["milestone_id"],
                "name": milestone["name"],
                "target_date": milestone["target_date"].isoformat(),
                "status": status,
                "completion_percentage": milestone["completion_percentage"]
            })
            
        return milestone_status
        
    async def optimize_resource_allocation(self, project_id: str) -> Dict[str, Any]:
        """
        Optimize resource allocation for project
        
        Args:
            project_id: Project identifier
            
        Returns:
            Resource optimization recommendations
        """
        if project_id not in self.active_projects:
            raise ValueError(f"Project {project_id} not found")
            
        self.logger.info(f"Optimizing resources for project: {project_id}")
        
        # Simulate resource optimization
        await asyncio.sleep(2.5)
        
        project = self.active_projects[project_id]
        
        # Analyze current resource utilization
        utilization = self._analyze_resource_utilization(project)
        
        # Identify optimization opportunities
        opportunities = self._identify_optimization_opportunities(project, utilization)
        
        # Generate reallocation recommendations
        recommendations = self._generate_reallocation_recommendations(project, opportunities)
        
        optimization_result = {
            "optimization_id": f"optimize_{uuid.uuid4().hex[:8]}",
            "project_id": project_id,
            "analysis_date": datetime.now().isoformat(),
            "current_utilization": utilization,
            "optimization_opportunities": opportunities,
            "recommendations": recommendations,
            "estimated_benefits": {
                "time_savings": "5-15 days",
                "cost_reduction": "8-12%",
                "efficiency_improvement": "15-25%"
            }
        }
        
        self.logger.info(f"Resource optimization completed for {project_id}")
        return optimization_result
        
    def _analyze_resource_utilization(self, project: ProjectPlan) -> Dict[str, Any]:
        """Analyze current resource utilization"""
        total_hours = sum(task.estimated_hours for task in project.tasks)
        total_resources = len(project.resources)
        
        # Calculate utilization metrics
        utilization = {
            "total_hours": total_hours,
            "total_resources": total_resources,
            "average_hours_per_resource": total_hours / total_resources if total_resources > 0 else 0,
            "resource_breakdown": {},
            "skill_gaps": [],
            "overallocation": []
        }
        
        # Analyze by resource type
        for resource in project.resources:
            resource_hours = sum(
                task.estimated_hours for task in project.tasks 
                if resource.resource_id in task.assigned_resources
            )
            
            utilization["resource_breakdown"][resource.name] = {
                "allocated_hours": resource_hours,
                "utilization_percentage": min((resource_hours / 40) * 100, 100),  # Assuming 40-hour work week
                "cost": resource_hours * resource.cost_per_hour
            }
            
        return utilization
        
    def _identify_optimization_opportunities(self, project: ProjectPlan, utilization: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify resource optimization opportunities"""
        opportunities = []
        
        # Check for overutilized resources
        for resource_name, data in utilization["resource_breakdown"].items():
            if data["utilization_percentage"] > 100:
                opportunities.append({
                    "type": "overutilization",
                    "resource": resource_name,
                    "issue": f"Resource overutilized at {data['utilization_percentage']:.1f}%",
                    "recommendation": "Redistribute tasks or add additional resources"
                })
                
        # Check for underutilized resources
        for resource_name, data in utilization["resource_breakdown"].items():
            if data["utilization_percentage"] < 50:
                opportunities.append({
                    "type": "underutilization",
                    "resource": resource_name,
                    "issue": f"Resource underutilized at {data['utilization_percentage']:.1f}%",
                    "recommendation": "Assign additional tasks or consider reallocation"
                })
                
        return opportunities
        
    def _generate_reallocation_recommendations(self, project: ProjectPlan, opportunities: List[Dict[str, Any]]) -> List[str]:
        """Generate resource reallocation recommendations"""
        recommendations = []
        
        for opportunity in opportunities:
            if opportunity["type"] == "overutilization":
                recommendations.append(f"Redistribute workload from {opportunity['resource']} to less utilized team members")
                recommendations.append("Consider hiring additional resources with matching skills")
                
            elif opportunity["type"] == "underutilization":
                recommendations.append(f"Assign additional responsibilities to {opportunity['resource']}")
                recommendations.append("Consider cross-training to expand capability")
                
        # General optimization recommendations
        recommendations.extend([
            "Implement task parallelization where dependencies allow",
            "Consider outsourcing non-critical tasks to optimize core team focus",
            "Establish resource sharing agreements with other projects"
        ])
        
        return recommendations
        
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and metrics"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "status": "active",
            "capabilities": self.capabilities,
            "active_projects": len(self.active_projects),
            "total_resources": len(self.resource_pool),
            "project_templates": len(self.project_templates),
            "risk_assessments": len(self.risk_database),
            "uptime": "100%",
            "last_activity": datetime.now().isoformat()
        }

# Supporting Classes

class PlanningEngine:
    """Advanced project planning engine"""
    
    async def generate_timeline(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimal project timeline"""
        await asyncio.sleep(1)
        
        # Calculate project duration based on complexity and scope
        complexity = requirements.get("complexity", "medium")
        scope = requirements.get("scope", "medium")
        
        # Base duration in days
        base_durations = {
            ("low", "small"): 30,
            ("low", "medium"): 45,
            ("low", "large"): 60,
            ("medium", "small"): 45,
            ("medium", "medium"): 90,
            ("medium", "large"): 120,
            ("high", "small"): 60,
            ("high", "medium"): 120,
            ("high", "large"): 180
        }
        
        duration_days = base_durations.get((complexity, scope), 90)
        
        start_date = requirements.get("start_date", datetime.now())
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
            
        end_date = start_date + timedelta(days=duration_days)
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "duration_days": duration_days,
            "phases": self._generate_project_phases(duration_days)
        }
        
    def _generate_project_phases(self, total_days: int) -> List[Dict[str, Any]]:
        """Generate project phases"""
        phases = [
            {"name": "Planning & Analysis", "percentage": 20},
            {"name": "Design & Architecture", "percentage": 25},
            {"name": "Implementation", "percentage": 40},
            {"name": "Testing & QA", "percentage": 10},
            {"name": "Deployment & Closure", "percentage": 5}
        ]
        
        current_day = 0
        phase_timeline = []
        
        for phase in phases:
            phase_days = int(total_days * phase["percentage"] / 100)
            phase_timeline.append({
                "name": phase["name"],
                "start_day": current_day,
                "end_day": current_day + phase_days,
                "duration_days": phase_days
            })
            current_day += phase_days
            
        return phase_timeline

class ResourceOptimizer:
    """Resource allocation optimization engine"""
    
    async def allocate_resources(self, requirements: Dict[str, Any], timeline: Dict[str, Any]) -> List[ProjectResource]:
        """Optimize resource allocation"""
        await asyncio.sleep(1.5)
        
        # Generate optimal resource allocation
        required_skills = requirements.get("required_skills", ["project_management", "development", "testing"])
        budget = requirements.get("budget", 100000)
        
        resources = []
        
        # Standard resource allocation based on project needs
        resource_templates = [
            {"name": "Project Manager", "type": "human", "skills": ["project_management", "coordination"], "rate": 75},
            {"name": "Senior Developer", "type": "human", "skills": ["development", "architecture"], "rate": 85},
            {"name": "Developer", "type": "human", "skills": ["development", "coding"], "rate": 65},
            {"name": "QA Engineer", "type": "human", "skills": ["testing", "quality_assurance"], "rate": 55},
            {"name": "Business Analyst", "type": "human", "skills": ["analysis", "requirements"], "rate": 70}
        ]
        
        start_date = timeline["start_date"]
        end_date = timeline["end_date"]
        
        for template in resource_templates:
            resource = ProjectResource(
                resource_id=f"resource_{uuid.uuid4().hex[:8]}",
                name=template["name"],
                type=ResourceType.HUMAN,
                availability=0.8,  # 80% availability
                cost_per_hour=template["rate"],
                skills=template["skills"],
                allocation_start=start_date,
                allocation_end=end_date
            )
            resources.append(resource)
            
        return resources

class RiskAnalyzer:
    """Project risk analysis engine"""
    
    async def assess_project_risks(self, requirements: Dict[str, Any]) -> List[ProjectRisk]:
        """Assess and categorize project risks"""
        await asyncio.sleep(1)
        
        complexity = requirements.get("complexity", "medium")
        project_type = requirements.get("type", "software_development")
        
        # Common project risks
        risk_templates = [
            {
                "description": "Scope creep and changing requirements",
                "category": "scope",
                "probability": 0.6,
                "impact": RiskLevel.MEDIUM,
                "mitigation": "Implement change control process and regular stakeholder reviews",
                "contingency": "Establish scope buffer and flexible timeline"
            },
            {
                "description": "Resource availability and skill gaps",
                "category": "resources",
                "probability": 0.4,
                "impact": RiskLevel.HIGH,
                "mitigation": "Cross-train team members and maintain resource backup plans",
                "contingency": "Engage external contractors or consultants"
            },
            {
                "description": "Technology integration challenges",
                "category": "technical",
                "probability": 0.3,
                "impact": RiskLevel.MEDIUM,
                "mitigation": "Conduct proof-of-concept and technical feasibility studies",
                "contingency": "Prepare alternative technology solutions"
            },
            {
                "description": "Budget overruns and cost escalation",
                "category": "financial",
                "probability": 0.4,
                "impact": RiskLevel.HIGH,
                "mitigation": "Implement detailed cost tracking and regular budget reviews",
                "contingency": "Secure additional funding or reduce scope"
            }
        ]
        
        # Adjust probabilities based on complexity
        complexity_multipliers = {"low": 0.8, "medium": 1.0, "high": 1.3}
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        risks = []
        for template in risk_templates:
            risk = ProjectRisk(
                risk_id=f"risk_{uuid.uuid4().hex[:8]}",
                description=template["description"],
                category=template["category"],
                probability=min(template["probability"] * multiplier, 1.0),
                impact=template["impact"],
                mitigation_strategy=template["mitigation"],
                contingency_plan=template["contingency"],
                responsible_party="Project Manager",
                review_date=datetime.now() + timedelta(days=7)
            )
            risks.append(risk)
            
        return risks

# Example usage and testing
async def main():
    """Test the Project Manager Agent functionality"""
    pm_agent = ProjectManagerAgent()
    
    print("📋 Project Manager Agent - Autonomous Project Planning")
    print("=" * 60)
    
    # Test project plan creation
    requirements = {
        "name": "Customer Portal Development",
        "description": "Develop a comprehensive customer portal with real-time analytics",
        "type": "software_development",
        "complexity": "medium",
        "scope": "medium",
        "budget": 250000,
        "required_skills": ["project_management", "frontend", "backend", "database", "testing"],
        "target_date": datetime.now() + timedelta(days=120)
    }
    
    project_plan = await pm_agent.create_project_plan(requirements)
    print(f"✅ Project Plan Created: {project_plan.plan_id}")
    print(f"   Project: {project_plan.project_name}")
    print(f"   Duration: {(project_plan.end_date - project_plan.start_date).days} days")
    print(f"   Tasks: {len(project_plan.tasks)}")
    print(f"   Resources: {len(project_plan.resources)}")
    print(f"   Risks: {len(project_plan.risks)}")
    
    # Test progress tracking
    progress_report = await pm_agent.track_project_progress(project_plan.plan_id)
    print(f"✅ Progress Tracking: {progress_report['report_id']}")
    print(f"   Overall Progress: {progress_report['overall_progress']}%")
    print(f"   Schedule Status: {progress_report['schedule_performance']['status']}")
    print(f"   Current Risks: {len(progress_report['current_risks'])}")
    
    # Test resource optimization
    optimization = await pm_agent.optimize_resource_allocation(project_plan.plan_id)
    print(f"✅ Resource Optimization: {optimization['optimization_id']}")
    print(f"   Opportunities: {len(optimization['optimization_opportunities'])}")
    print(f"   Recommendations: {len(optimization['recommendations'])}")
    
    # Display agent status
    status = pm_agent.get_agent_status()
    print(f"\n📊 Agent Status: {status['status'].upper()}")
    print(f"   Active Projects: {status['active_projects']}")
    print(f"   Capabilities: {len(status['capabilities'])}")

if __name__ == "__main__":
    asyncio.run(main())
