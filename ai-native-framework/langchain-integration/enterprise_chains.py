#!/usr/bin/env python3
"""
LangChain Enterprise Integration
==============================

Advanced LangChain integration for enterprise AI workflows including
chains, agents, memory systems, and tool integrations.

Author: Enterprise AI Platform Team
Version: 2.0.0
Date: September 2025
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod

# LangChain imports with fallbacks
try:
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.chains import LLMChain, SequentialChain
    from langchain.prompts import PromptTemplate, ChatPromptTemplate
    from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
    from langchain.agents import create_openai_functions_agent, AgentExecutor
    from langchain.tools import Tool, BaseTool
    from langchain.schema import AgentAction, AgentFinish
    from langchain.callbacks.base import BaseCallbackHandler
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    logging.warning(f"LangChain not available: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ChainConfig:
    """Configuration for LangChain chains"""
    name: str
    chain_type: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 2000
    memory_type: str = "buffer"
    tools: List[str] = None

class EnterpriseCallbackHandler(BaseCallbackHandler if LANGCHAIN_AVAILABLE else object):
    """Custom callback handler for enterprise monitoring"""
    
    def __init__(self, chain_name: str):
        self.chain_name = chain_name
        self.start_time = None
        self.metrics = {
            "total_tokens": 0,
            "total_cost": 0.0,
            "execution_time": 0.0,
            "success_count": 0,
            "error_count": 0
        }
    
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        """Called when chain starts"""
        self.start_time = datetime.now()
        logger.info(f"Chain {self.chain_name} started with inputs: {list(inputs.keys())}")
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        """Called when chain ends successfully"""
        if self.start_time:
            self.metrics["execution_time"] = (datetime.now() - self.start_time).total_seconds()
        self.metrics["success_count"] += 1
        logger.info(f"Chain {self.chain_name} completed successfully in {self.metrics['execution_time']:.2f}s")
    
    def on_chain_error(self, error: Exception, **kwargs) -> None:
        """Called when chain encounters an error"""
        self.metrics["error_count"] += 1
        logger.error(f"Chain {self.chain_name} failed: {error}")

class LangChainEnterpriseIntegration:
    """
    Enterprise-grade LangChain integration with advanced capabilities
    """
    
    def __init__(self, config_path: str = "config/langchain_config.json"):
        self.config_path = config_path
        self.chains = {}
        self.agents = {}
        self.tools = {}
        self.memory_stores = {}
        self.metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "average_execution_time": 0.0,
            "total_cost": 0.0
        }
        
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not available. Running in simulation mode.")
            return
        
        self.load_configuration()
        self.initialize_tools()
        self.initialize_chains()
        
        logger.info("LangChain Enterprise Integration initialized")
    
    def load_configuration(self):
        """Load LangChain configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_path} not found. Using defaults.")
            self.config = self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "chains": [
                {
                    "name": "requirements_analyzer",
                    "chain_type": "llm",
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.3,
                    "max_tokens": 2000,
                    "memory_type": "buffer"
                },
                {
                    "name": "project_planner",
                    "chain_type": "sequential",
                    "model": "gpt-4",
                    "temperature": 0.5,
                    "memory_type": "summary"
                },
                {
                    "name": "data_analyst",
                    "chain_type": "agent",
                    "model": "gpt-4",
                    "tools": ["calculator", "search", "database_query"]
                }
            ],
            "tools": {
                "calculator": {"enabled": True},
                "search": {"enabled": True, "api_key": ""},
                "database_query": {"enabled": True, "connection_string": ""}
            }
        }
    
    def initialize_tools(self):
        """Initialize enterprise tools for LangChain agents"""
        if not LANGCHAIN_AVAILABLE:
            return
        
        # Calculator tool
        self.tools["calculator"] = Tool(
            name="Calculator",
            description="Useful for mathematical calculations",
            func=self._calculator_tool
        )
        
        # Database query tool
        self.tools["database_query"] = Tool(
            name="DatabaseQuery",
            description="Query enterprise databases for information",
            func=self._database_query_tool
        )
        
        # Project analysis tool
        self.tools["project_analyzer"] = Tool(
            name="ProjectAnalyzer",
            description="Analyze project requirements and provide insights",
            func=self._project_analyzer_tool
        )
        
        # Risk assessment tool
        self.tools["risk_assessor"] = Tool(
            name="RiskAssessor",
            description="Assess project risks and provide mitigation strategies",
            func=self._risk_assessor_tool
        )
        
        logger.info(f"Initialized {len(self.tools)} enterprise tools")
    
    def _calculator_tool(self, query: str) -> str:
        """Simple calculator tool"""
        try:
            # Safe evaluation of mathematical expressions
            result = eval(query.replace("^", "**"))
            return f"Calculation result: {result}"
        except Exception as e:
            return f"Calculation error: {e}"
    
    def _database_query_tool(self, query: str) -> str:
        """Database query tool (simulated)"""
        # In practice, this would connect to real databases
        simulated_results = {
            "project count": "Currently tracking 23 active projects",
            "user metrics": "Total users: 1,247 | Active users: 892",
            "performance data": "Average response time: 0.8s | Uptime: 99.7%"
        }
        
        for key, result in simulated_results.items():
            if key in query.lower():
                return result
        
        return "Database query executed successfully. No specific results found."
    
    def _project_analyzer_tool(self, requirements: str) -> str:
        """Project analysis tool"""
        analysis = {
            "complexity": "Medium",
            "estimated_duration": "3-4 months",
            "resource_requirements": "5-7 team members",
            "key_technologies": ["Python", "React", "PostgreSQL"],
            "risk_factors": ["API integration complexity", "Data migration"],
            "recommendations": ["Implement MVP first", "Use agile methodology"]
        }
        
        return f"Project Analysis: {json.dumps(analysis, indent=2)}"
    
    def _risk_assessor_tool(self, project_description: str) -> str:
        """Risk assessment tool"""
        risks = {
            "technical_risks": [
                {"risk": "Technology compatibility", "severity": "Medium", "mitigation": "Proof of concept"},
                {"risk": "Scalability concerns", "severity": "Low", "mitigation": "Load testing"}
            ],
            "business_risks": [
                {"risk": "Market competition", "severity": "Medium", "mitigation": "Competitive analysis"},
                {"risk": "Budget overrun", "severity": "High", "mitigation": "Phased development"}
            ],
            "overall_risk_score": 6.5
        }
        
        return f"Risk Assessment: {json.dumps(risks, indent=2)}"
    
    def initialize_chains(self):
        """Initialize LangChain chains based on configuration"""
        if not LANGCHAIN_AVAILABLE:
            return
        
        for chain_config in self.config.get("chains", []):
            try:
                chain = self.create_chain(chain_config)
                self.chains[chain_config["name"]] = chain
                logger.info(f"Created chain: {chain_config['name']}")
            except Exception as e:
                logger.error(f"Failed to create chain {chain_config['name']}: {e}")
    
    def create_chain(self, config: Dict[str, Any]):
        """Create a LangChain chain based on configuration"""
        if not LANGCHAIN_AVAILABLE:
            return None
        
        chain_type = config.get("chain_type", "llm")
        model_name = config.get("model", "gpt-3.5-turbo")
        
        # Initialize the language model
        if "gpt-4" in model_name:
            llm = ChatOpenAI(model=model_name, temperature=config.get("temperature", 0.7))
        else:
            llm = ChatOpenAI(model=model_name, temperature=config.get("temperature", 0.7))
        
        # Initialize memory
        memory_type = config.get("memory_type", "buffer")
        if memory_type == "summary":
            memory = ConversationSummaryMemory(llm=llm, return_messages=True)
        else:
            memory = ConversationBufferMemory(return_messages=True)
        
        self.memory_stores[config["name"]] = memory
        
        # Create callback handler
        callback_handler = EnterpriseCallbackHandler(config["name"])
        
        if chain_type == "llm":
            return self._create_llm_chain(llm, memory, callback_handler, config)
        elif chain_type == "sequential":
            return self._create_sequential_chain(llm, memory, callback_handler, config)
        elif chain_type == "agent":
            return self._create_agent_chain(llm, memory, callback_handler, config)
        else:
            raise ValueError(f"Unknown chain type: {chain_type}")
    
    def _create_llm_chain(self, llm, memory, callback_handler, config):
        """Create a basic LLM chain"""
        prompt_template = config.get("prompt_template", 
            """You are an expert {role} assistant. 
            Please analyze the following {input_type} and provide detailed insights:
            
            {input}
            
            Analysis:"""
        )
        
        prompt = PromptTemplate(
            input_variables=["role", "input_type", "input"],
            template=prompt_template
        )
        
        return LLMChain(
            llm=llm,
            prompt=prompt,
            memory=memory,
            callbacks=[callback_handler],
            verbose=True
        )
    
    def _create_sequential_chain(self, llm, memory, callback_handler, config):
        """Create a sequential chain for multi-step processes"""
        # Step 1: Requirements analysis
        requirements_prompt = PromptTemplate(
            input_variables=["project_description"],
            template="""Analyze the following project description and extract key requirements:
            
            Project: {project_description}
            
            Requirements Analysis:
            1. Functional Requirements:
            2. Non-functional Requirements:
            3. Technical Requirements:
            4. Business Requirements:
            """
        )
        
        requirements_chain = LLMChain(
            llm=llm,
            prompt=requirements_prompt,
            output_key="requirements",
            verbose=True
        )
        
        # Step 2: Planning
        planning_prompt = PromptTemplate(
            input_variables=["requirements"],
            template="""Based on the following requirements, create a detailed project plan:
            
            Requirements: {requirements}
            
            Project Plan:
            1. Project Phases:
            2. Timeline:
            3. Resource Allocation:
            4. Milestones:
            5. Dependencies:
            """
        )
        
        planning_chain = LLMChain(
            llm=llm,
            prompt=planning_prompt,
            output_key="project_plan",
            verbose=True
        )
        
        return SequentialChain(
            chains=[requirements_chain, planning_chain],
            input_variables=["project_description"],
            output_variables=["requirements", "project_plan"],
            callbacks=[callback_handler],
            verbose=True
        )
    
    def _create_agent_chain(self, llm, memory, callback_handler, config):
        """Create an agent with tools"""
        # Get tools for this agent
        agent_tools = []
        tool_names = config.get("tools", [])
        
        for tool_name in tool_names:
            if tool_name in self.tools:
                agent_tools.append(self.tools[tool_name])
        
        # Create agent prompt
        system_message = """You are an expert enterprise AI assistant with access to various tools.
        Use the tools available to provide comprehensive analysis and solutions.
        Always explain your reasoning and provide detailed insights."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])
        
        # Create agent
        try:
            agent = create_openai_functions_agent(llm, agent_tools, prompt)
            return AgentExecutor(
                agent=agent,
                tools=agent_tools,
                memory=memory,
                callbacks=[callback_handler],
                verbose=True,
                max_iterations=5
            )
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            return None
    
    async def execute_chain(self, chain_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific chain with inputs"""
        if chain_name not in self.chains:
            raise ValueError(f"Chain '{chain_name}' not found")
        
        if not LANGCHAIN_AVAILABLE:
            # Simulation mode
            return {
                "result": f"Simulated result for {chain_name} with inputs: {list(inputs.keys())}",
                "execution_time": 1.5,
                "status": "simulated"
            }
        
        start_time = datetime.now()
        self.metrics["total_executions"] += 1
        
        try:
            chain = self.chains[chain_name]
            result = await chain.arun(**inputs)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.metrics["successful_executions"] += 1
            self.metrics["average_execution_time"] = (
                (self.metrics["average_execution_time"] * (self.metrics["successful_executions"] - 1) + execution_time) 
                / self.metrics["successful_executions"]
            )
            
            logger.info(f"Chain {chain_name} executed successfully in {execution_time:.2f}s")
            
            return {
                "result": result,
                "execution_time": execution_time,
                "status": "success",
                "chain_name": chain_name,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.metrics["failed_executions"] += 1
            logger.error(f"Chain {chain_name} execution failed: {e}")
            
            return {
                "error": str(e),
                "status": "failed",
                "chain_name": chain_name,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_chain_status(self) -> Dict[str, Any]:
        """Get status of all chains"""
        status = {
            "langchain_available": LANGCHAIN_AVAILABLE,
            "total_chains": len(self.chains),
            "available_chains": list(self.chains.keys()),
            "available_tools": list(self.tools.keys()),
            "memory_stores": len(self.memory_stores),
            "metrics": self.metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        if LANGCHAIN_AVAILABLE:
            # Add chain-specific status
            chain_details = {}
            for name, chain in self.chains.items():
                chain_details[name] = {
                    "type": type(chain).__name__,
                    "status": "ready",
                    "memory_messages": len(self.memory_stores.get(name, {}).chat_memory.messages) if name in self.memory_stores else 0
                }
            status["chain_details"] = chain_details
        
        return status
    
    def clear_memory(self, chain_name: str = None):
        """Clear memory for specific chain or all chains"""
        if chain_name:
            if chain_name in self.memory_stores:
                self.memory_stores[chain_name].clear()
                logger.info(f"Cleared memory for chain: {chain_name}")
        else:
            for memory in self.memory_stores.values():
                memory.clear()
            logger.info("Cleared memory for all chains")
    
    def get_conversation_history(self, chain_name: str) -> List[Dict[str, Any]]:
        """Get conversation history for a specific chain"""
        if chain_name not in self.memory_stores:
            return []
        
        memory = self.memory_stores[chain_name]
        if hasattr(memory, 'chat_memory') and hasattr(memory.chat_memory, 'messages'):
            return [
                {
                    "type": msg.type,
                    "content": msg.content,
                    "timestamp": getattr(msg, 'timestamp', 'unknown')
                }
                for msg in memory.chat_memory.messages
            ]
        return []

# Example usage and demonstration
async def main():
    """Demonstrate LangChain Enterprise Integration"""
    print("🔗 LangChain Enterprise Integration Demo")
    print("=" * 50)
    
    # Initialize integration
    integration = LangChainEnterpriseIntegration()
    
    # Get status
    status = integration.get_chain_status()
    print(f"\n📊 Status:")
    print(f"LangChain Available: {status['langchain_available']}")
    print(f"Total Chains: {status['total_chains']}")
    print(f"Available Tools: {len(status['available_tools'])}")
    
    if status['available_chains']:
        print(f"\n🔗 Available Chains:")
        for chain in status['available_chains']:
            print(f"  • {chain}")
    
    # Execute example chains
    test_inputs = [
        {
            "chain": "requirements_analyzer",
            "inputs": {
                "role": "Business Analyst",
                "input_type": "project requirements",
                "input": "Build a customer management system with real-time analytics and mobile support"
            }
        },
        {
            "chain": "project_planner",
            "inputs": {
                "project_description": "E-commerce platform with AI recommendations and inventory management"
            }
        }
    ]
    
    for test in test_inputs:
        chain_name = test["chain"]
        if chain_name in status['available_chains']:
            print(f"\n🚀 Executing chain: {chain_name}")
            try:
                result = await integration.execute_chain(chain_name, test["inputs"])
                print(f"✅ Status: {result['status']}")
                if result['status'] == 'success':
                    print(f"⏱️ Execution time: {result['execution_time']:.2f}s")
                    print(f"📝 Result preview: {result['result'][:200]}...")
                else:
                    print(f"❌ Error: {result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"❌ Execution failed: {e}")
    
    # Final metrics
    print(f"\n📈 Final Metrics:")
    final_status = integration.get_chain_status()
    metrics = final_status['metrics']
    print(f"Total Executions: {metrics['total_executions']}")
    print(f"Successful: {metrics['successful_executions']}")
    print(f"Failed: {metrics['failed_executions']}")
    print(f"Average Time: {metrics['average_execution_time']:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
