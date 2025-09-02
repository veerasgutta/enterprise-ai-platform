"""
🤖 AutoGen Multi-Agent Team Builder
Advanced conversation-based multi-agent system

This module provides sophisticated AutoGen agent teams for:
- Collaborative software development
- Multi-perspective code review
- Automated testing and QA
- Project management coordination
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

try:
    import autogen
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
    from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    print("AutoGen not available. Install with: pip install pyautogen")

@dataclass
class TeamMember:
    """AutoGen team member configuration"""
    name: str
    role: str
    system_message: str
    specializations: List[str]
    tools: List[str] = None

class AutoGenTeamBuilder:
    """
    🎭 AutoGen Multi-Agent Team Builder
    
    Creates specialized agent teams for different enterprise tasks:
    - Development teams (Senior Dev, Junior Dev, Reviewer, Tester)
    - DevOps teams (Engineer, Security Expert, Infrastructure)
    - Product teams (Manager, Designer, Analyst, Researcher)
    """
    
    def __init__(self, api_key: str = None):
        self.logger = logging.getLogger(__name__)
        self.config_list = [
            {
                "model": "gpt-4",
                "api_key": api_key or "your-openai-api-key"
            }
        ]
        self.teams: Dict[str, Dict] = {}
    
    def create_development_team(self) -> Dict[str, Any]:
        """Create a software development team"""
        if not AUTOGEN_AVAILABLE:
            raise ImportError("AutoGen not available")
        
        # Senior Software Engineer
        senior_engineer = AssistantAgent(
            name="SeniorEngineer",
            system_message="""You are a Senior Software Engineer with 10+ years of experience.
            
            Your expertise includes:
            - Full-stack development (React, Node.js, Python, .NET)
            - System architecture and design patterns
            - Performance optimization and scalability
            - Security best practices
            - Code review and mentoring
            
            You provide technical leadership and make architectural decisions.
            You write clean, efficient, and maintainable code.
            You mentor junior developers and ensure code quality.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Full-Stack Developer
        fullstack_dev = AssistantAgent(
            name="FullStackDeveloper",
            system_message="""You are a Full-Stack Developer with expertise in modern web technologies.
            
            Your skills include:
            - Frontend: React, Vue.js, Angular, TypeScript, CSS3
            - Backend: Node.js, Python, Java, REST APIs
            - Databases: PostgreSQL, MongoDB, Redis
            - DevOps: Docker, Kubernetes, CI/CD
            - Testing: Jest, Cypress, Unit testing
            
            You implement features end-to-end and ensure seamless integration.
            You write comprehensive tests and maintain high code quality.""",
            llm_config={"config_list": self.config_list}
        )
        
        # DevOps Engineer
        devops_engineer = AssistantAgent(
            name="DevOpsEngineer",
            system_message="""You are a DevOps Engineer specializing in infrastructure and automation.
            
            Your expertise includes:
            - Infrastructure as Code (Terraform, CloudFormation)
            - Container orchestration (Docker, Kubernetes)
            - CI/CD pipelines (GitHub Actions, Jenkins, GitLab)
            - Cloud platforms (AWS, Azure, GCP)
            - Monitoring and logging (Prometheus, Grafana, ELK)
            - Security and compliance
            
            You ensure reliable deployments, scalability, and system reliability.
            You automate processes and maintain infrastructure.""",
            llm_config={"config_list": self.config_list}
        )
        
        # QA Engineer
        qa_engineer = AssistantAgent(
            name="QAEngineer",
            system_message="""You are a QA Engineer focused on quality assurance and testing.
            
            Your responsibilities include:
            - Test planning and strategy
            - Automated testing (Selenium, Cypress, Playwright)
            - Performance testing and load testing
            - Security testing and vulnerability assessment
            - Bug tracking and regression testing
            - Quality metrics and reporting
            
            You ensure software quality through comprehensive testing.
            You identify issues early and maintain testing standards.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Product Manager
        product_manager = AssistantAgent(
            name="ProductManager",
            system_message="""You are a Technical Product Manager bridging business and technology.
            
            Your role includes:
            - Requirements gathering and prioritization
            - Feature specification and user stories
            - Stakeholder communication and coordination
            - Technology roadmap planning
            - Performance metrics and KPIs
            - Market analysis and competitive research
            
            You translate business needs into technical requirements.
            You ensure the product meets user needs and business goals.""",
            llm_config={"config_list": self.config_list}
        )
        
        # User Proxy for human interaction
        user_proxy = UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "work_dir": "autogen_workspace",
                "use_docker": False
            }
        )
        
        # Create group chat
        agents = [senior_engineer, fullstack_dev, devops_engineer, qa_engineer, product_manager, user_proxy]
        
        group_chat = GroupChat(
            agents=agents,
            messages=[],
            max_round=20
        )
        
        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": self.config_list}
        )
        
        team = {
            "name": "Development Team",
            "manager": manager,
            "agents": {
                "senior_engineer": senior_engineer,
                "fullstack_dev": fullstack_dev,
                "devops_engineer": devops_engineer,
                "qa_engineer": qa_engineer,
                "product_manager": product_manager,
                "user_proxy": user_proxy
            },
            "group_chat": group_chat,
            "specializations": [
                "Full-stack development",
                "System architecture",
                "DevOps and infrastructure",
                "Quality assurance",
                "Product management"
            ]
        }
        
        self.teams["development"] = team
        return team
    
    def create_ai_research_team(self) -> Dict[str, Any]:
        """Create an AI research and development team"""
        if not AUTOGEN_AVAILABLE:
            raise ImportError("AutoGen not available")
        
        # AI Research Scientist
        ai_researcher = AssistantAgent(
            name="AIResearcher",
            system_message="""You are an AI Research Scientist with deep expertise in machine learning.
            
            Your expertise includes:
            - Machine Learning algorithms and architectures
            - Deep Learning (CNNs, RNNs, Transformers)
            - Natural Language Processing
            - Computer Vision
            - Reinforcement Learning
            - MLOps and model deployment
            
            You research and implement cutting-edge AI solutions.
            You stay current with latest AI research and techniques.""",
            llm_config={"config_list": self.config_list}
        )
        
        # Data Scientist
        data_scientist = AssistantAgent(
            name="DataScientist",
            system_message="""You are a Data Scientist specializing in data analysis and insights.
            
            Your skills include:
            - Statistical analysis and modeling
            - Data preprocessing and feature engineering
            - Predictive analytics and forecasting
            - A/B testing and experimentation
            - Data visualization and storytelling
            - Python/R, SQL, Pandas, Scikit-learn
            
            You extract insights from data and build predictive models.
            You communicate findings to stakeholders effectively.""",
            llm_config={"config_list": self.config_list}
        )
        
        # ML Engineer
        ml_engineer = AssistantAgent(
            name="MLEngineer",
            system_message="""You are an ML Engineer focused on production ML systems.
            
            Your expertise includes:
            - ML model deployment and serving
            - MLOps pipelines and automation
            - Model monitoring and performance
            - Scalable ML infrastructure
            - Feature stores and data pipelines
            - TensorFlow, PyTorch, MLflow, Kubeflow
            
            You bridge research and production by deploying robust ML systems.
            You ensure models perform well in production environments.""",
            llm_config={"config_list": self.config_list}
        )
        
        # AI Ethics Specialist
        ai_ethics = AssistantAgent(
            name="AIEthicsSpecialist",
            system_message="""You are an AI Ethics Specialist ensuring responsible AI development.
            
            Your focus areas include:
            - AI fairness and bias detection
            - Explainable AI and transparency
            - Privacy and data protection
            - Ethical AI frameworks
            - Regulatory compliance
            - AI safety and robustness
            
            You ensure AI systems are fair, transparent, and beneficial.
            You identify and mitigate potential risks and biases.""",
            llm_config={"config_list": self.config_list}
        )
        
        user_proxy = UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "ai_research_workspace"}
        )
        
        agents = [ai_researcher, data_scientist, ml_engineer, ai_ethics, user_proxy]
        
        group_chat = GroupChat(agents=agents, messages=[], max_round=15)
        manager = GroupChatManager(groupchat=group_chat, llm_config={"config_list": self.config_list})
        
        team = {
            "name": "AI Research Team",
            "manager": manager,
            "agents": {
                "ai_researcher": ai_researcher,
                "data_scientist": data_scientist,
                "ml_engineer": ml_engineer,
                "ai_ethics": ai_ethics,
                "user_proxy": user_proxy
            },
            "group_chat": group_chat,
            "specializations": [
                "AI research and development",
                "Data science and analytics",
                "ML engineering and deployment",
                "AI ethics and safety"
            ]
        }
        
        self.teams["ai_research"] = team
        return team
    
    async def execute_team_task(self, team_name: str, task: str) -> Dict[str, Any]:
        """Execute a task using specified team"""
        if team_name not in self.teams:
            raise ValueError(f"Team '{team_name}' not found")
        
        team = self.teams[team_name]
        manager = team["manager"]
        user_proxy = team["agents"]["user_proxy"]
        
        try:
            # Start the conversation
            response = user_proxy.initiate_chat(
                manager,
                message=task,
                max_round=20
            )
            
            return {
                "team": team_name,
                "task": task,
                "success": True,
                "response": response,
                "agents_involved": list(team["agents"].keys())
            }
        
        except Exception as e:
            self.logger.error(f"Team task execution failed: {e}")
            return {
                "team": team_name,
                "task": task,
                "success": False,
                "error": str(e),
                "agents_involved": list(team["agents"].keys())
            }
    
    def get_team_info(self, team_name: str = None) -> Dict[str, Any]:
        """Get information about teams"""
        if team_name:
            if team_name in self.teams:
                team = self.teams[team_name]
                return {
                    "name": team["name"],
                    "agents": list(team["agents"].keys()),
                    "specializations": team["specializations"]
                }
            else:
                return {"error": f"Team '{team_name}' not found"}
        else:
            return {
                "available_teams": list(self.teams.keys()),
                "team_details": {
                    name: {
                        "name": team["name"],
                        "agents": list(team["agents"].keys()),
                        "specializations": team["specializations"]
                    }
                    for name, team in self.teams.items()
                }
            }

# Example usage
async def demo_autogen_teams():
    """Demonstrate AutoGen team capabilities"""
    if not AUTOGEN_AVAILABLE:
        print("❌ AutoGen not available. Install with: pip install pyautogen")
        return
    
    print("🤖 AutoGen Multi-Agent Teams Demo")
    print("=" * 40)
    
    # Create team builder
    team_builder = AutoGenTeamBuilder()
    
    # Create development team
    print("🔨 Creating Development Team...")
    dev_team = team_builder.create_development_team()
    print(f"✅ Created team with {len(dev_team['agents'])} agents")
    
    # Create AI research team
    print("🧠 Creating AI Research Team...")
    ai_team = team_builder.create_ai_research_team()
    print(f"✅ Created team with {len(ai_team['agents'])} agents")
    
    # Show team information
    team_info = team_builder.get_team_info()
    print(f"\n📊 Available Teams: {team_info['available_teams']}")
    
    for team_name, details in team_info['team_details'].items():
        print(f"\n{details['name']}:")
        print(f"  Agents: {', '.join(details['agents'])}")
        print(f"  Specializations: {', '.join(details['specializations'])}")
    
    # Example task (commented out to avoid API calls)
    # print("\n🎯 Executing sample task...")
    # result = await team_builder.execute_team_task(
    #     "development",
    #     "Design and implement a REST API for user authentication with JWT tokens"
    # )
    # print(f"Task result: {result['success']}")

if __name__ == "__main__":
    asyncio.run(demo_autogen_teams())
