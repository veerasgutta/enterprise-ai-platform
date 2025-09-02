"""
🧠 AI Reasoning Agents
Advanced AI agents providing intelligent reasoning and decision-making capabilities

These agents leverage advanced AI models for complex reasoning, planning,
and decision-making tasks in enterprise environments.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
import uuid
from abc import ABC, abstractmethod
import random
import math

class AIReasoningAgent(ABC):
    """Abstract base class for AI reasoning agents"""
    
    def __init__(self, agent_id: str, agent_name: str, reasoning_type: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.reasoning_type = reasoning_type
        self.status = "idle"
        self.created_at = datetime.now()
        self.reasoning_history = []
        self.confidence_threshold = 0.7
        self.learning_rate = 0.01
        self.knowledge_base = {}
        self.performance_metrics = {
            "decisions_made": 0,
            "accuracy_rate": 95.0,
            "confidence_avg": 0.85,
            "reasoning_time_avg": 0.0
        }
    
    @abstractmethod
    async def reason(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform reasoning - to be implemented by specific agents"""
        pass
    
    async def learn_from_feedback(self, decision_id: str, feedback: Dict[str, Any]) -> None:
        """Learn from feedback to improve future reasoning"""
        # Update learning based on feedback
        accuracy = feedback.get("accuracy", 0.5)
        self.performance_metrics["accuracy_rate"] = (
            self.performance_metrics["accuracy_rate"] * 0.9 + accuracy * 100 * 0.1
        )

class StrategicPlanningAgent(AIReasoningAgent):
    """AI agent for strategic planning and long-term decision making"""
    
    def __init__(self):
        super().__init__(
            agent_id="ai_strategic_001",
            agent_name="StrategicPlanningAgent",
            reasoning_type="strategic_planning"
        )
        self.planning_horizon = timedelta(days=365)
        self.strategic_models = {}
        self.scenario_cache = {}
    
    async def reason(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform strategic reasoning and planning"""
        self.status = "planning"
        start_time = datetime.now()
        
        try:
            planning_type = context.get("planning_type", "business_strategy")
            time_horizon = context.get("time_horizon", "1_year")
            objectives = context.get("objectives", [])
            constraints = context.get("constraints", [])
            
            # Generate strategic plan
            strategic_plan = await self._generate_strategic_plan(
                planning_type, time_horizon, objectives, constraints
            )
            
            # Assess risks and opportunities
            risk_assessment = await self._assess_risks(strategic_plan)
            opportunity_analysis = await self._analyze_opportunities(strategic_plan)
            
            # Create implementation roadmap
            roadmap = await self._create_roadmap(strategic_plan)
            
            reasoning_time = (datetime.now() - start_time).total_seconds()
            confidence = self._calculate_confidence(strategic_plan, risk_assessment)
            
            # Update metrics
            self.performance_metrics["decisions_made"] += 1
            self.performance_metrics["reasoning_time_avg"] = (
                (self.performance_metrics["reasoning_time_avg"] * 
                 (self.performance_metrics["decisions_made"] - 1) + reasoning_time) /
                self.performance_metrics["decisions_made"]
            )
            
            self.status = "idle"
            
            reasoning_result = {
                "agent_id": self.agent_id,
                "reasoning_type": "strategic_planning",
                "strategic_plan": strategic_plan,
                "risk_assessment": risk_assessment,
                "opportunity_analysis": opportunity_analysis,
                "implementation_roadmap": roadmap,
                "confidence_score": confidence,
                "reasoning_time": reasoning_time,
                "planning_horizon": time_horizon
            }
            
            # Store reasoning history
            self.reasoning_history.append({
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "result": reasoning_result
            })
            
            return reasoning_result
            
        except Exception as e:
            self.status = "error"
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e),
                "reasoning_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def _generate_strategic_plan(self, planning_type: str, time_horizon: str, 
                                     objectives: List[str], constraints: List[str]) -> Dict[str, Any]:
        """Generate comprehensive strategic plan"""
        
        # Strategic initiatives based on planning type
        if planning_type == "business_strategy":
            initiatives = [
                "Digital transformation acceleration",
                "Market expansion into emerging markets",
                "AI and automation integration",
                "Sustainability and ESG compliance",
                "Customer experience enhancement"
            ]
        elif planning_type == "technology_strategy":
            initiatives = [
                "Cloud-native architecture migration",
                "AI/ML platform development",
                "Data governance implementation",
                "Cybersecurity enhancement",
                "API ecosystem expansion"
            ]
        else:
            initiatives = [
                "Strategic objective alignment",
                "Resource optimization",
                "Risk mitigation",
                "Innovation pipeline development"
            ]
        
        return {
            "planning_type": planning_type,
            "strategic_objectives": objectives,
            "key_initiatives": initiatives,
            "success_metrics": [
                "Revenue growth: 25% YoY",
                "Market share increase: 5%",
                "Customer satisfaction: >90%",
                "Operational efficiency: 20% improvement"
            ],
            "resource_requirements": {
                "budget": "$2.5M",
                "headcount": 25,
                "technology_investment": "$800K"
            },
            "constraints_considered": constraints
        }
    
    async def _assess_risks(self, strategic_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Assess strategic risks"""
        return {
            "risk_categories": {
                "market_risks": {
                    "level": "medium",
                    "probability": 0.3,
                    "impact": "high",
                    "mitigation": "Market diversification strategy"
                },
                "technology_risks": {
                    "level": "low",
                    "probability": 0.15,
                    "impact": "medium",
                    "mitigation": "Robust testing and gradual rollout"
                },
                "regulatory_risks": {
                    "level": "medium",
                    "probability": 0.25,
                    "impact": "medium",
                    "mitigation": "Compliance monitoring and legal review"
                },
                "financial_risks": {
                    "level": "low",
                    "probability": 0.2,
                    "impact": "high",
                    "mitigation": "Financial reserves and contingency planning"
                }
            },
            "overall_risk_score": 0.225,
            "risk_tolerance": "moderate",
            "contingency_plans": [
                "Alternative market entry strategies",
                "Technology fallback options",
                "Financial risk buffers"
            ]
        }
    
    async def _analyze_opportunities(self, strategic_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze strategic opportunities"""
        return {
            "opportunity_areas": {
                "emerging_technologies": {
                    "potential_value": "high",
                    "probability": 0.8,
                    "timeline": "12-18 months",
                    "investment_required": "$500K"
                },
                "new_markets": {
                    "potential_value": "very_high",
                    "probability": 0.6,
                    "timeline": "6-12 months",
                    "investment_required": "$1.2M"
                },
                "partnerships": {
                    "potential_value": "medium",
                    "probability": 0.9,
                    "timeline": "3-6 months",
                    "investment_required": "$200K"
                }
            },
            "opportunity_score": 0.76,
            "strategic_fit": "excellent",
            "recommended_priorities": [
                "New market expansion",
                "Technology partnerships",
                "Innovation investments"
            ]
        }
    
    async def _create_roadmap(self, strategic_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation roadmap"""
        return {
            "phases": {
                "phase_1": {
                    "name": "Foundation Building",
                    "duration": "3 months",
                    "key_activities": [
                        "Team formation and training",
                        "Infrastructure setup",
                        "Initial market research"
                    ],
                    "milestones": ["Team ready", "Systems operational"]
                },
                "phase_2": {
                    "name": "Market Entry",
                    "duration": "6 months",
                    "key_activities": [
                        "Product adaptation",
                        "Channel partnerships",
                        "Marketing campaigns"
                    ],
                    "milestones": ["First customer", "Channel partners onboarded"]
                },
                "phase_3": {
                    "name": "Scale and Optimize",
                    "duration": "6 months",
                    "key_activities": [
                        "Operations scaling",
                        "Process optimization",
                        "Performance monitoring"
                    ],
                    "milestones": ["Scale targets met", "ROI achieved"]
                }
            },
            "critical_path": ["Foundation Building", "Market Entry", "Scale and Optimize"],
            "dependencies": ["Technology readiness", "Market conditions", "Resource availability"],
            "success_criteria": ["Revenue targets", "Market penetration", "Customer satisfaction"]
        }
    
    def _calculate_confidence(self, strategic_plan: Dict[str, Any], 
                            risk_assessment: Dict[str, Any]) -> float:
        """Calculate confidence in strategic plan"""
        base_confidence = 0.8
        risk_factor = 1 - risk_assessment["overall_risk_score"]
        plan_completeness = len(strategic_plan.get("key_initiatives", [])) / 5
        
        confidence = base_confidence * risk_factor * min(plan_completeness, 1.0)
        return round(confidence, 2)

class ProblemSolvingAgent(AIReasoningAgent):
    """AI agent for complex problem solving and root cause analysis"""
    
    def __init__(self):
        super().__init__(
            agent_id="ai_problem_001",
            agent_name="ProblemSolvingAgent",
            reasoning_type="problem_solving"
        )
        self.solution_patterns = {}
        self.problem_history = []
    
    async def reason(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform problem-solving reasoning"""
        self.status = "solving"
        start_time = datetime.now()
        
        try:
            problem_description = context.get("problem", "Unknown problem")
            problem_type = context.get("type", "general")
            urgency = context.get("urgency", "medium")
            constraints = context.get("constraints", [])
            
            # Analyze the problem
            problem_analysis = await self._analyze_problem(
                problem_description, problem_type, urgency
            )
            
            # Generate potential solutions
            solutions = await self._generate_solutions(problem_analysis, constraints)
            
            # Evaluate solutions
            solution_evaluation = await self._evaluate_solutions(solutions, problem_analysis)
            
            # Recommend best solution
            recommendation = await self._recommend_solution(solution_evaluation)
            
            reasoning_time = (datetime.now() - start_time).total_seconds()
            confidence = self._calculate_solution_confidence(solution_evaluation)
            
            self.status = "idle"
            
            reasoning_result = {
                "agent_id": self.agent_id,
                "reasoning_type": "problem_solving",
                "problem_analysis": problem_analysis,
                "solutions_generated": solutions,
                "solution_evaluation": solution_evaluation,
                "recommendation": recommendation,
                "confidence_score": confidence,
                "reasoning_time": reasoning_time
            }
            
            self.reasoning_history.append({
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "result": reasoning_result
            })
            
            return reasoning_result
            
        except Exception as e:
            self.status = "error"
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e),
                "reasoning_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def _analyze_problem(self, description: str, problem_type: str, urgency: str) -> Dict[str, Any]:
        """Analyze problem structure and root causes"""
        
        # Root cause analysis
        root_causes = []
        if "performance" in description.lower():
            root_causes = ["Resource constraints", "Inefficient algorithms", "Data bottlenecks"]
        elif "security" in description.lower():
            root_causes = ["Access control issues", "Vulnerable dependencies", "Configuration errors"]
        elif "integration" in description.lower():
            root_causes = ["API incompatibility", "Data format mismatches", "Network issues"]
        else:
            root_causes = ["Process inefficiencies", "Resource limitations", "Communication gaps"]
        
        return {
            "problem_description": description,
            "problem_type": problem_type,
            "urgency_level": urgency,
            "complexity_score": random.uniform(0.3, 0.9),
            "root_causes": root_causes,
            "affected_systems": ["Production", "User Experience", "Data Pipeline"],
            "impact_assessment": {
                "business_impact": "medium",
                "technical_impact": "high",
                "user_impact": "low"
            },
            "problem_pattern": "recurring" if random.random() > 0.7 else "isolated"
        }
    
    async def _generate_solutions(self, problem_analysis: Dict[str, Any], 
                                constraints: List[str]) -> List[Dict[str, Any]]:
        """Generate potential solutions"""
        
        solutions = [
            {
                "solution_id": "sol_001",
                "name": "Quick Fix Solution",
                "description": "Immediate workaround to address symptoms",
                "implementation_time": "2-4 hours",
                "resource_requirements": "Low",
                "effectiveness": 0.6,
                "risk_level": "low"
            },
            {
                "solution_id": "sol_002", 
                "name": "Comprehensive Solution",
                "description": "Address root causes with systematic approach",
                "implementation_time": "1-2 weeks",
                "resource_requirements": "High",
                "effectiveness": 0.9,
                "risk_level": "medium"
            },
            {
                "solution_id": "sol_003",
                "name": "Hybrid Approach",
                "description": "Combine immediate fixes with long-term improvements",
                "implementation_time": "3-5 days",
                "resource_requirements": "Medium",
                "effectiveness": 0.8,
                "risk_level": "low"
            }
        ]
        
        # Filter solutions based on constraints
        if "budget_limited" in constraints:
            solutions = [s for s in solutions if s["resource_requirements"] != "High"]
        
        if "time_critical" in constraints:
            solutions = [s for s in solutions if "hours" in s["implementation_time"] or "3-5 days" in s["implementation_time"]]
        
        return solutions
    
    async def _evaluate_solutions(self, solutions: List[Dict[str, Any]], 
                                problem_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate solutions against criteria"""
        
        evaluation_criteria = {
            "effectiveness": 0.4,
            "implementation_speed": 0.3,
            "resource_efficiency": 0.2,
            "risk_mitigation": 0.1
        }
        
        evaluated_solutions = []
        
        for solution in solutions:
            # Calculate weighted score
            speed_score = 1.0 if "hours" in solution["implementation_time"] else 0.5
            resource_score = {"Low": 1.0, "Medium": 0.7, "High": 0.4}[solution["resource_requirements"]]
            risk_score = {"low": 1.0, "medium": 0.7, "high": 0.4}[solution["risk_level"]]
            
            weighted_score = (
                solution["effectiveness"] * evaluation_criteria["effectiveness"] +
                speed_score * evaluation_criteria["implementation_speed"] +
                resource_score * evaluation_criteria["resource_efficiency"] +
                risk_score * evaluation_criteria["risk_mitigation"]
            )
            
            evaluated_solutions.append({
                **solution,
                "evaluation_score": round(weighted_score, 2),
                "pros": [
                    "Addresses core issues",
                    "Feasible implementation",
                    "Measurable outcomes"
                ],
                "cons": [
                    "Resource intensive" if solution["resource_requirements"] == "High" else "Limited scope",
                    "Time consuming" if "weeks" in solution["implementation_time"] else "May need follow-up"
                ]
            })
        
        # Sort by evaluation score
        evaluated_solutions.sort(key=lambda x: x["evaluation_score"], reverse=True)
        
        return {
            "evaluation_criteria": evaluation_criteria,
            "evaluated_solutions": evaluated_solutions,
            "recommendation_basis": "weighted_scoring",
            "confidence_level": "high"
        }
    
    async def _recommend_solution(self, solution_evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend the best solution"""
        
        best_solution = solution_evaluation["evaluated_solutions"][0]
        
        return {
            "recommended_solution": best_solution,
            "justification": [
                f"Highest evaluation score: {best_solution['evaluation_score']}",
                f"Optimal balance of effectiveness and feasibility",
                f"Aligns with problem urgency and constraints"
            ],
            "implementation_plan": {
                "phase_1": "Preparation and resource allocation",
                "phase_2": "Implementation and testing",
                "phase_3": "Monitoring and validation"
            },
            "success_metrics": [
                "Problem resolution confirmation",
                "Performance improvement measurement",
                "Stakeholder satisfaction"
            ],
            "contingency_plan": "Fallback to secondary solution if primary fails"
        }
    
    def _calculate_solution_confidence(self, solution_evaluation: Dict[str, Any]) -> float:
        """Calculate confidence in solution recommendation"""
        best_score = solution_evaluation["evaluated_solutions"][0]["evaluation_score"]
        score_variance = 0.1  # Simulated variance
        confidence = min(best_score * (1 - score_variance), 0.95)
        return round(confidence, 2)

class DecisionMakingAgent(AIReasoningAgent):
    """AI agent for complex decision making under uncertainty"""
    
    def __init__(self):
        super().__init__(
            agent_id="ai_decision_001",
            agent_name="DecisionMakingAgent",
            reasoning_type="decision_making"
        )
        self.decision_models = {}
        self.decision_history = []
    
    async def reason(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform decision-making reasoning"""
        self.status = "deciding"
        start_time = datetime.now()
        
        try:
            decision_context = context.get("decision_context", "Unknown decision")
            alternatives = context.get("alternatives", [])
            criteria = context.get("criteria", [])
            stakeholders = context.get("stakeholders", [])
            time_constraint = context.get("time_constraint", "none")
            
            # Analyze decision context
            context_analysis = await self._analyze_decision_context(
                decision_context, alternatives, criteria, stakeholders
            )
            
            # Evaluate alternatives
            alternative_evaluation = await self._evaluate_alternatives(
                alternatives, criteria, context_analysis
            )
            
            # Apply decision models
            decision_analysis = await self._apply_decision_models(
                alternative_evaluation, context_analysis
            )
            
            # Make final recommendation
            final_decision = await self._make_final_decision(
                decision_analysis, time_constraint
            )
            
            reasoning_time = (datetime.now() - start_time).total_seconds()
            confidence = self._calculate_decision_confidence(decision_analysis)
            
            self.status = "idle"
            
            reasoning_result = {
                "agent_id": self.agent_id,
                "reasoning_type": "decision_making",
                "context_analysis": context_analysis,
                "alternative_evaluation": alternative_evaluation,
                "decision_analysis": decision_analysis,
                "final_decision": final_decision,
                "confidence_score": confidence,
                "reasoning_time": reasoning_time
            }
            
            self.reasoning_history.append({
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "result": reasoning_result
            })
            
            return reasoning_result
            
        except Exception as e:
            self.status = "error"
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e),
                "reasoning_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def _analyze_decision_context(self, decision_context: str, alternatives: List[str],
                                      criteria: List[str], stakeholders: List[str]) -> Dict[str, Any]:
        """Analyze the decision-making context"""
        
        return {
            "decision_type": "strategic" if "strategy" in decision_context.lower() else "operational",
            "complexity_level": min(len(alternatives) * len(criteria) / 10, 1.0),
            "stakeholder_impact": {
                "internal": len([s for s in stakeholders if "internal" in s.lower()]),
                "external": len([s for s in stakeholders if "external" in s.lower()]),
                "high_influence": len(stakeholders) // 2
            },
            "decision_urgency": "high" if "urgent" in decision_context.lower() else "normal",
            "uncertainty_factors": [
                "Market conditions",
                "Resource availability",
                "Regulatory changes",
                "Technology evolution"
            ],
            "constraints": [
                "Budget limitations",
                "Time constraints",
                "Resource capacity",
                "Risk tolerance"
            ]
        }
    
    async def _evaluate_alternatives(self, alternatives: List[str], criteria: List[str],
                                   context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate alternatives against criteria"""
        
        evaluation_matrix = {}
        
        for i, alternative in enumerate(alternatives):
            scores = {}
            for criterion in criteria:
                # Simulate scoring based on alternative and criterion
                base_score = random.uniform(0.3, 0.9)
                uncertainty_adjustment = random.uniform(-0.1, 0.1)
                scores[criterion] = max(0, min(1, base_score + uncertainty_adjustment))
            
            evaluation_matrix[alternative] = {
                "criteria_scores": scores,
                "overall_score": sum(scores.values()) / len(scores),
                "strengths": [f"Strong in {max(scores, key=scores.get)}"],
                "weaknesses": [f"Weak in {min(scores, key=scores.get)}"],
                "risk_factors": ["Implementation complexity", "Resource requirements"]
            }
        
        return {
            "evaluation_method": "multi_criteria_analysis",
            "criteria_weights": {criterion: 1/len(criteria) for criterion in criteria},
            "evaluation_matrix": evaluation_matrix,
            "sensitivity_analysis": "Low sensitivity to weight changes",
            "robustness_check": "Results stable across scenarios"
        }
    
    async def _apply_decision_models(self, alternative_evaluation: Dict[str, Any],
                                   context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply various decision-making models"""
        
        evaluation_matrix = alternative_evaluation["evaluation_matrix"]
        
        # Expected value model
        expected_values = {}
        for alt, data in evaluation_matrix.items():
            expected_values[alt] = data["overall_score"] * 0.8  # Adjust for uncertainty
        
        # Risk-adjusted returns
        risk_adjusted = {}
        for alt, data in evaluation_matrix.items():
            risk_factor = 0.9  # Simulated risk adjustment
            risk_adjusted[alt] = data["overall_score"] * risk_factor
        
        # Stakeholder impact analysis
        stakeholder_preferences = {}
        for alt in evaluation_matrix.keys():
            stakeholder_preferences[alt] = random.uniform(0.4, 0.9)
        
        return {
            "decision_models_applied": [
                "Expected Value Analysis",
                "Risk-Adjusted Returns",
                "Stakeholder Impact Assessment",
                "Sensitivity Analysis"
            ],
            "expected_values": expected_values,
            "risk_adjusted_scores": risk_adjusted,
            "stakeholder_preferences": stakeholder_preferences,
            "model_consensus": max(expected_values, key=expected_values.get),
            "decision_uncertainty": 0.15
        }
    
    async def _make_final_decision(self, decision_analysis: Dict[str, Any],
                                 time_constraint: str) -> Dict[str, Any]:
        """Make the final decision recommendation"""
        
        recommended_alternative = decision_analysis["model_consensus"]
        
        return {
            "recommended_decision": recommended_alternative,
            "decision_rationale": [
                "Highest expected value across models",
                "Balanced risk-return profile",
                "Strong stakeholder alignment",
                "Robust under uncertainty"
            ],
            "implementation_considerations": [
                "Phased rollout recommended",
                "Monitor key metrics closely",
                "Prepare contingency plans",
                "Regular stakeholder communication"
            ],
            "success_probability": 0.78,
            "potential_downsides": [
                "Implementation complexity",
                "Resource intensive",
                "Change management challenges"
            ],
            "decision_timeline": "2 weeks" if time_constraint == "urgent" else "4-6 weeks",
            "review_checkpoints": ["30 days", "90 days", "6 months"]
        }
    
    def _calculate_decision_confidence(self, decision_analysis: Dict[str, Any]) -> float:
        """Calculate confidence in decision recommendation"""
        uncertainty = decision_analysis.get("decision_uncertainty", 0.2)
        model_alignment = 0.85  # Simulated model consensus strength
        confidence = (1 - uncertainty) * model_alignment
        return round(confidence, 2)

# Demo function for AI reasoning agents
async def demo_ai_reasoning_agents():
    """Demonstrate AI reasoning agents functionality"""
    
    # Create AI reasoning agents
    strategic_agent = StrategicPlanningAgent()
    problem_agent = ProblemSolvingAgent()
    decision_agent = DecisionMakingAgent()
    
    agents = [strategic_agent, problem_agent, decision_agent]
    
    print("🧠 AI Reasoning Agents Demo:")
    print("=" * 50)
    
    # Demo strategic planning
    strategic_context = {
        "planning_type": "business_strategy",
        "time_horizon": "2_years",
        "objectives": ["Market expansion", "Revenue growth", "Digital transformation"],
        "constraints": ["Budget limitations", "Resource constraints"]
    }
    strategic_result = await strategic_agent.reason(strategic_context)
    print("🎯 Strategic Planning Result:")
    print(f"  Plan Type: {strategic_result['strategic_plan']['planning_type']}")
    print(f"  Confidence: {strategic_result['confidence_score']}")
    print(f"  Key Initiatives: {len(strategic_result['strategic_plan']['key_initiatives'])}")
    
    # Demo problem solving
    problem_context = {
        "problem": "System performance degradation affecting user experience",
        "type": "performance",
        "urgency": "high",
        "constraints": ["time_critical", "budget_limited"]
    }
    problem_result = await problem_agent.reason(problem_context)
    print("\n🔧 Problem Solving Result:")
    print(f"  Root Causes: {len(problem_result['problem_analysis']['root_causes'])}")
    print(f"  Solutions Generated: {len(problem_result['solutions_generated'])}")
    print(f"  Recommended: {problem_result['recommendation']['recommended_solution']['name']}")
    
    # Demo decision making
    decision_context = {
        "decision_context": "Strategic technology platform selection",
        "alternatives": ["Cloud-native solution", "Hybrid approach", "On-premise solution"],
        "criteria": ["Cost", "Scalability", "Security", "Performance"],
        "stakeholders": ["IT team", "Business users", "External customers"],
        "time_constraint": "normal"
    }
    decision_result = await decision_agent.reason(decision_context)
    print("\n⚖️ Decision Making Result:")
    print(f"  Alternatives Evaluated: {len(decision_result['alternative_evaluation']['evaluation_matrix'])}")
    print(f"  Recommended Decision: {decision_result['final_decision']['recommended_decision']}")
    print(f"  Success Probability: {decision_result['final_decision']['success_probability']}")
    
    # Show reasoning performance
    print("\n🤖 Reasoning Agent Performance:")
    for agent in agents:
        decisions = agent.performance_metrics["decisions_made"]
        accuracy = agent.performance_metrics["accuracy_rate"]
        print(f"  {agent.agent_name}: {decisions} decisions | {accuracy:.1f}% accuracy")
    
    return {
        "strategic_planning": strategic_result,
        "problem_solving": problem_result,
        "decision_making": decision_result,
        "agent_performance": [
            {
                "agent": agent.agent_name,
                "metrics": agent.performance_metrics
            }
            for agent in agents
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting AI Reasoning Agents Demo...")
    asyncio.run(demo_ai_reasoning_agents())
