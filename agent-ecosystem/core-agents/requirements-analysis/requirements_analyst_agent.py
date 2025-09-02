"""
📄 Requirements Analyst Agent - Intelligent Requirement Management
================================================================

Advanced AI agent for automated requirements analysis, validation, and management
across enterprise projects with intelligent conflict detection and resolution.

Features:
- Intelligent requirement extraction from documents
- Automated conflict detection and resolution
- Requirement completeness validation
- Traceability matrix generation
- Change impact analysis
- Requirements quality assessment
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Union, Tuple, Set
from datetime import datetime, timedelta
from enum import Enum
import logging
import uuid
from dataclasses import dataclass
from abc import ABC, abstractmethod
import statistics

class RequirementType(Enum):
    """Types of requirements"""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    USER = "user"
    SYSTEM = "system"
    INTERFACE = "interface"
    CONSTRAINT = "constraint"

class RequirementPriority(Enum):
    """Requirement priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RequirementStatus(Enum):
    """Requirement lifecycle status"""
    DRAFT = "draft"
    PROPOSED = "proposed"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    TESTED = "tested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class ConflictType(Enum):
    """Types of requirement conflicts"""
    CONTRADICTION = "contradiction"
    DUPLICATION = "duplication"
    INCONSISTENCY = "inconsistency"
    AMBIGUITY = "ambiguity"
    INCOMPLETENESS = "incompleteness"

@dataclass
class Requirement:
    """Individual requirement specification"""
    req_id: str
    title: str
    description: str
    type: RequirementType
    priority: RequirementPriority
    status: RequirementStatus
    source: str
    stakeholder: str
    acceptance_criteria: List[str]
    dependencies: List[str]
    tags: List[str]
    effort_estimate: Optional[float]
    business_value: Optional[float]
    created_at: datetime
    updated_at: datetime

@dataclass
class RequirementConflict:
    """Requirement conflict identification"""
    conflict_id: str
    type: ConflictType
    description: str
    affected_requirements: List[str]
    severity: str
    suggested_resolution: str
    impact_assessment: str
    created_at: datetime

@dataclass
class RequirementAnalysis:
    """Comprehensive requirements analysis result"""
    analysis_id: str
    project_name: str
    total_requirements: int
    requirements_by_type: Dict[str, int]
    requirements_by_priority: Dict[str, int]
    completeness_score: float
    quality_score: float
    conflicts: List[RequirementConflict]
    recommendations: List[str]
    traceability_matrix: Dict[str, List[str]]
    analysis_date: datetime

@dataclass
class ChangeImpactAnalysis:
    """Change impact analysis result"""
    change_id: str
    proposed_change: str
    affected_requirements: List[str]
    impact_scope: str
    effort_estimate: float
    risk_assessment: str
    recommendations: List[str]
    approval_required: bool

class RequirementsAnalystAgent:
    """
    Requirements Analyst Agent - Intelligent Requirement Management
    
    Provides advanced capabilities for requirements analysis, validation,
    conflict detection, and traceability management.
    """
    
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id or f"req_agent_{uuid.uuid4().hex[:8]}"
        self.agent_name = "Requirements Analyst Agent"
        self.capabilities = [
            "requirement_extraction",
            "conflict_detection",
            "completeness_validation",
            "traceability_management",
            "change_impact_analysis",
            "quality_assessment",
            "stakeholder_analysis",
            "acceptance_criteria_generation",
            "requirement_prioritization",
            "documentation_generation"
        ]
        
        self.requirements_database = {}
        self.project_requirements = {}
        self.conflict_database = {}
        self.traceability_maps = {}
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"RequirementsAgent-{self.agent_id}")
        
        # Initialize analysis engines
        self.nlp_processor = NLPProcessor()
        self.conflict_detector = ConflictDetector()
        self.validator = RequirementValidator()
        
    async def extract_requirements(self, documents: List[Dict[str, Any]]) -> List[Requirement]:
        """
        Extract requirements from various document sources
        
        Args:
            documents: List of documents with text content and metadata
            
        Returns:
            List of extracted and parsed requirements
        """
        self.logger.info(f"Extracting requirements from {len(documents)} documents")
        
        # Simulate advanced NLP processing
        await asyncio.sleep(3)
        
        extracted_requirements = []
        
        for doc in documents:
            doc_requirements = await self.nlp_processor.extract_from_document(doc)
            extracted_requirements.extend(doc_requirements)
            
        # Post-process and validate extracted requirements
        validated_requirements = []
        for req_data in extracted_requirements:
            requirement = await self._create_requirement_from_extraction(req_data)
            validated_requirements.append(requirement)
            
        # Store in database
        project_name = documents[0].get("project", "Unknown Project")
        if project_name not in self.project_requirements:
            self.project_requirements[project_name] = []
            
        self.project_requirements[project_name].extend(validated_requirements)
        
        self.logger.info(f"Extracted {len(validated_requirements)} requirements")
        return validated_requirements
        
    async def _create_requirement_from_extraction(self, req_data: Dict[str, Any]) -> Requirement:
        """Create structured requirement from extracted data"""
        
        # Generate acceptance criteria
        acceptance_criteria = await self._generate_acceptance_criteria(req_data)
        
        # Determine requirement type
        req_type = self._classify_requirement_type(req_data["text"])
        
        # Calculate priority based on keywords and context
        priority = self._determine_priority(req_data)
        
        requirement = Requirement(
            req_id=f"REQ_{uuid.uuid4().hex[:8].upper()}",
            title=req_data.get("title", req_data["text"][:50] + "..."),
            description=req_data["text"],
            type=req_type,
            priority=priority,
            status=RequirementStatus.DRAFT,
            source=req_data.get("source", "Document"),
            stakeholder=req_data.get("stakeholder", "Unknown"),
            acceptance_criteria=acceptance_criteria,
            dependencies=[],
            tags=self._extract_tags(req_data["text"]),
            effort_estimate=self._estimate_effort(req_data),
            business_value=self._estimate_business_value(req_data),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return requirement
        
    def _classify_requirement_type(self, text: str) -> RequirementType:
        """Classify requirement type based on text analysis"""
        text_lower = text.lower()
        
        # Keyword patterns for different requirement types
        patterns = {
            RequirementType.FUNCTIONAL: ["shall", "must", "function", "feature", "capability", "behavior"],
            RequirementType.NON_FUNCTIONAL: ["performance", "scalability", "security", "usability", "reliability"],
            RequirementType.BUSINESS: ["business", "organization", "process", "workflow", "policy"],
            RequirementType.TECHNICAL: ["system", "architecture", "infrastructure", "platform", "technology"],
            RequirementType.USER: ["user", "customer", "actor", "persona", "end-user"],
            RequirementType.INTERFACE: ["interface", "api", "integration", "connection", "communication"],
            RequirementType.CONSTRAINT: ["constraint", "limitation", "restriction", "compliance", "regulation"]
        }
        
        # Score each type based on keyword matches
        scores = {}
        for req_type, keywords in patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[req_type] = score
            
        # Return type with highest score, default to FUNCTIONAL
        if scores and max(scores.values()) > 0:
            return max(scores.items(), key=lambda x: x[1])[0]
        else:
            return RequirementType.FUNCTIONAL
            
    def _determine_priority(self, req_data: Dict[str, Any]) -> RequirementPriority:
        """Determine requirement priority based on content analysis"""
        text = req_data["text"].lower()
        
        # Priority indicators
        critical_indicators = ["critical", "essential", "mandatory", "must have", "required"]
        high_indicators = ["important", "significant", "high priority", "should have"]
        medium_indicators = ["useful", "beneficial", "could have", "nice to have"]
        
        if any(indicator in text for indicator in critical_indicators):
            return RequirementPriority.CRITICAL
        elif any(indicator in text for indicator in high_indicators):
            return RequirementPriority.HIGH
        elif any(indicator in text for indicator in medium_indicators):
            return RequirementPriority.MEDIUM
        else:
            return RequirementPriority.MEDIUM
            
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from requirement text"""
        tags = []
        
        # Domain-specific tags
        domain_patterns = {
            "security": ["security", "authentication", "authorization", "encryption"],
            "performance": ["performance", "speed", "latency", "throughput"],
            "ui_ux": ["interface", "user experience", "usability", "design"],
            "data": ["data", "database", "storage", "information"],
            "integration": ["integration", "api", "connection", "interface"],
            "mobile": ["mobile", "smartphone", "tablet", "responsive"],
            "reporting": ["report", "analytics", "dashboard", "metrics"]
        }
        
        text_lower = text.lower()
        for tag, keywords in domain_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(tag)
                
        return tags
        
    def _estimate_effort(self, req_data: Dict[str, Any]) -> float:
        """Estimate development effort for requirement"""
        text = req_data["text"]
        
        # Simple effort estimation based on complexity indicators
        complexity_indicators = {
            "simple": ["display", "show", "list", "view"],
            "medium": ["create", "update", "manage", "process"],
            "complex": ["integrate", "calculate", "analyze", "optimize", "synchronize"]
        }
        
        text_lower = text.lower()
        
        # Count complexity indicators
        simple_count = sum(1 for indicator in complexity_indicators["simple"] if indicator in text_lower)
        medium_count = sum(1 for indicator in complexity_indicators["medium"] if indicator in text_lower)
        complex_count = sum(1 for indicator in complexity_indicators["complex"] if indicator in text_lower)
        
        # Calculate effort (story points)
        if complex_count > 0:
            return 8.0 + (complex_count * 3)
        elif medium_count > 0:
            return 5.0 + (medium_count * 2)
        else:
            return 2.0 + (simple_count * 1)
            
    def _estimate_business_value(self, req_data: Dict[str, Any]) -> float:
        """Estimate business value of requirement"""
        text = req_data["text"].lower()
        
        # Business value indicators
        high_value_keywords = ["revenue", "cost savings", "efficiency", "customer satisfaction", "competitive advantage"]
        medium_value_keywords = ["improvement", "optimization", "enhancement", "productivity"]
        
        score = 5.0  # Base value
        
        # Increase score based on value keywords
        for keyword in high_value_keywords:
            if keyword in text:
                score += 3.0
                
        for keyword in medium_value_keywords:
            if keyword in text:
                score += 1.5
                
        return min(score, 10.0)  # Cap at 10
        
    async def _generate_acceptance_criteria(self, req_data: Dict[str, Any]) -> List[str]:
        """Generate acceptance criteria for requirement"""
        await asyncio.sleep(0.5)
        
        text = req_data["text"]
        req_type = self._classify_requirement_type(text)
        
        # Template-based acceptance criteria generation
        if req_type == RequirementType.FUNCTIONAL:
            criteria = [
                "Given a valid user input",
                "When the function is executed",
                "Then the expected output is produced",
                "And the system state is updated correctly"
            ]
        elif req_type == RequirementType.NON_FUNCTIONAL:
            criteria = [
                "Given normal operating conditions",
                "When the system is under specified load",
                "Then performance metrics meet defined thresholds",
                "And system remains stable and responsive"
            ]
        else:
            criteria = [
                "Given the requirement specification",
                "When implementation is complete",
                "Then all specified conditions are met",
                "And stakeholder approval is obtained"
            ]
            
        return criteria
        
    async def analyze_requirements(self, project_name: str) -> RequirementAnalysis:
        """
        Perform comprehensive requirements analysis
        
        Args:
            project_name: Name of project to analyze
            
        Returns:
            RequirementAnalysis: Comprehensive analysis results
        """
        if project_name not in self.project_requirements:
            raise ValueError(f"Project {project_name} not found")
            
        self.logger.info(f"Analyzing requirements for project: {project_name}")
        
        # Simulate comprehensive analysis
        await asyncio.sleep(2.5)
        
        requirements = self.project_requirements[project_name]
        
        # Calculate statistics
        total_requirements = len(requirements)
        requirements_by_type = self._count_by_type(requirements)
        requirements_by_priority = self._count_by_priority(requirements)
        
        # Assess completeness and quality
        completeness_score = await self._assess_completeness(requirements)
        quality_score = await self._assess_quality(requirements)
        
        # Detect conflicts
        conflicts = await self.conflict_detector.find_conflicts(requirements)
        
        # Generate recommendations
        recommendations = self._generate_analysis_recommendations(requirements, completeness_score, quality_score)
        
        # Build traceability matrix
        traceability_matrix = self._build_traceability_matrix(requirements)
        
        analysis = RequirementAnalysis(
            analysis_id=f"analysis_{uuid.uuid4().hex[:8]}",
            project_name=project_name,
            total_requirements=total_requirements,
            requirements_by_type=requirements_by_type,
            requirements_by_priority=requirements_by_priority,
            completeness_score=completeness_score,
            quality_score=quality_score,
            conflicts=conflicts,
            recommendations=recommendations,
            traceability_matrix=traceability_matrix,
            analysis_date=datetime.now()
        )
        
        self.logger.info(f"Requirements analysis completed: {analysis.analysis_id}")
        return analysis
        
    def _count_by_type(self, requirements: List[Requirement]) -> Dict[str, int]:
        """Count requirements by type"""
        counts = {}
        for req in requirements:
            req_type = req.type.value
            counts[req_type] = counts.get(req_type, 0) + 1
        return counts
        
    def _count_by_priority(self, requirements: List[Requirement]) -> Dict[str, int]:
        """Count requirements by priority"""
        counts = {}
        for req in requirements:
            priority = req.priority.value
            counts[priority] = counts.get(priority, 0) + 1
        return counts
        
    async def _assess_completeness(self, requirements: List[Requirement]) -> float:
        """Assess requirements completeness"""
        await asyncio.sleep(1)
        
        total_score = 0
        total_checks = 0
        
        for req in requirements:
            # Check various completeness criteria
            checks = [
                len(req.description) > 20,  # Adequate description
                len(req.acceptance_criteria) > 0,  # Has acceptance criteria
                req.priority != RequirementPriority.MEDIUM,  # Priority defined
                req.stakeholder != "Unknown",  # Stakeholder identified
                req.effort_estimate is not None,  # Effort estimated
                len(req.tags) > 0  # Tagged appropriately
            ]
            
            score = sum(checks) / len(checks)
            total_score += score
            total_checks += 1
            
        return (total_score / total_checks) * 100 if total_checks > 0 else 0
        
    async def _assess_quality(self, requirements: List[Requirement]) -> float:
        """Assess requirements quality"""
        await asyncio.sleep(1)
        
        quality_metrics = []
        
        for req in requirements:
            # Quality indicators
            clarity_score = self._assess_clarity(req.description)
            specificity_score = self._assess_specificity(req.description)
            testability_score = self._assess_testability(req.acceptance_criteria)
            
            req_quality = (clarity_score + specificity_score + testability_score) / 3
            quality_metrics.append(req_quality)
            
        return statistics.mean(quality_metrics) * 100 if quality_metrics else 0
        
    def _assess_clarity(self, description: str) -> float:
        """Assess requirement clarity"""
        # Simple clarity assessment based on sentence structure
        sentences = description.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Penalize very long or very short sentences
        if 10 <= avg_sentence_length <= 25:
            return 1.0
        elif 5 <= avg_sentence_length < 10 or 25 < avg_sentence_length <= 35:
            return 0.7
        else:
            return 0.4
            
    def _assess_specificity(self, description: str) -> float:
        """Assess requirement specificity"""
        # Look for specific, measurable terms
        specific_indicators = ["exactly", "precisely", "within", "less than", "greater than", "equal to"]
        vague_indicators = ["appropriate", "reasonable", "adequate", "sufficient", "good"]
        
        description_lower = description.lower()
        
        specific_count = sum(1 for indicator in specific_indicators if indicator in description_lower)
        vague_count = sum(1 for indicator in vague_indicators if indicator in description_lower)
        
        if specific_count > vague_count:
            return 1.0
        elif specific_count == vague_count:
            return 0.6
        else:
            return 0.3
            
    def _assess_testability(self, acceptance_criteria: List[str]) -> float:
        """Assess requirement testability"""
        if not acceptance_criteria:
            return 0.0
            
        # Look for testable language patterns
        testable_patterns = ["given", "when", "then", "should", "verify", "check"]
        
        testable_count = 0
        for criterion in acceptance_criteria:
            criterion_lower = criterion.lower()
            if any(pattern in criterion_lower for pattern in testable_patterns):
                testable_count += 1
                
        return testable_count / len(acceptance_criteria)
        
    def _generate_analysis_recommendations(self, requirements: List[Requirement], 
                                         completeness: float, quality: float) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if completeness < 70:
            recommendations.extend([
                "Improve requirement completeness by adding missing acceptance criteria",
                "Identify and document stakeholders for unclear requirements",
                "Provide effort estimates for all requirements"
            ])
            
        if quality < 75:
            recommendations.extend([
                "Enhance requirement clarity by using specific, measurable language",
                "Replace vague terms with precise, quantifiable criteria",
                "Improve testability by adding detailed acceptance criteria"
            ])
            
        # Priority distribution recommendations
        priority_counts = self._count_by_priority(requirements)
        critical_ratio = priority_counts.get("critical", 0) / len(requirements)
        
        if critical_ratio > 0.3:
            recommendations.append("Review critical priority assignments - high percentage may indicate priority inflation")
        elif critical_ratio < 0.1:
            recommendations.append("Consider if more requirements should be marked as critical for project success")
            
        # Type distribution recommendations
        type_counts = self._count_by_type(requirements)
        functional_ratio = type_counts.get("functional", 0) / len(requirements)
        
        if functional_ratio > 0.8:
            recommendations.append("Consider adding non-functional requirements for system qualities")
        elif functional_ratio < 0.4:
            recommendations.append("Ensure adequate functional requirements coverage for core features")
            
        return recommendations
        
    def _build_traceability_matrix(self, requirements: List[Requirement]) -> Dict[str, List[str]]:
        """Build requirement traceability matrix"""
        traceability = {}
        
        for req in requirements:
            # Simple traceability based on tags and dependencies
            related_requirements = []
            
            # Find requirements with similar tags
            for other_req in requirements:
                if req.req_id != other_req.req_id:
                    common_tags = set(req.tags).intersection(set(other_req.tags))
                    if len(common_tags) > 0:
                        related_requirements.append(other_req.req_id)
                        
            # Add explicit dependencies
            related_requirements.extend(req.dependencies)
            
            traceability[req.req_id] = list(set(related_requirements))
            
        return traceability
        
    async def analyze_change_impact(self, project_name: str, 
                                  proposed_change: Dict[str, Any]) -> ChangeImpactAnalysis:
        """
        Analyze impact of proposed requirement changes
        
        Args:
            project_name: Project name
            proposed_change: Details of proposed change
            
        Returns:
            ChangeImpactAnalysis: Comprehensive impact analysis
        """
        if project_name not in self.project_requirements:
            raise ValueError(f"Project {project_name} not found")
            
        self.logger.info(f"Analyzing change impact for project: {project_name}")
        
        # Simulate impact analysis
        await asyncio.sleep(2)
        
        requirements = self.project_requirements[project_name]
        change_description = proposed_change.get("description", "")
        affected_req_ids = proposed_change.get("affected_requirements", [])
        
        # Find directly affected requirements
        directly_affected = [req for req in requirements if req.req_id in affected_req_ids]
        
        # Find indirectly affected requirements through dependencies
        indirectly_affected = self._find_indirect_impacts(requirements, affected_req_ids)
        
        all_affected = list(set([req.req_id for req in directly_affected] + indirectly_affected))
        
        # Assess impact scope
        impact_scope = self._assess_impact_scope(len(all_affected), len(requirements))
        
        # Estimate effort
        effort_estimate = self._estimate_change_effort(directly_affected, len(indirectly_affected))
        
        # Assess risks
        risk_assessment = self._assess_change_risks(proposed_change, all_affected)
        
        # Generate recommendations
        recommendations = self._generate_change_recommendations(impact_scope, effort_estimate, risk_assessment)
        
        # Determine if approval required
        approval_required = self._requires_approval(impact_scope, effort_estimate)
        
        analysis = ChangeImpactAnalysis(
            change_id=f"change_{uuid.uuid4().hex[:8]}",
            proposed_change=change_description,
            affected_requirements=all_affected,
            impact_scope=impact_scope,
            effort_estimate=effort_estimate,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            approval_required=approval_required
        )
        
        self.logger.info(f"Change impact analysis completed: {analysis.change_id}")
        return analysis
        
    def _find_indirect_impacts(self, requirements: List[Requirement], affected_ids: List[str]) -> List[str]:
        """Find requirements indirectly affected by changes"""
        indirect_impacts = []
        
        # Check dependencies
        for req in requirements:
            if any(dep_id in affected_ids for dep_id in req.dependencies):
                indirect_impacts.append(req.req_id)
                
        # Check tag relationships
        affected_reqs = [req for req in requirements if req.req_id in affected_ids]
        affected_tags = set()
        for req in affected_reqs:
            affected_tags.update(req.tags)
            
        for req in requirements:
            if req.req_id not in affected_ids:
                common_tags = set(req.tags).intersection(affected_tags)
                if len(common_tags) >= 2:  # Strong tag relationship
                    indirect_impacts.append(req.req_id)
                    
        return list(set(indirect_impacts))
        
    def _assess_impact_scope(self, affected_count: int, total_count: int) -> str:
        """Assess the scope of change impact"""
        percentage = (affected_count / total_count) * 100 if total_count > 0 else 0
        
        if percentage < 10:
            return "minimal"
        elif percentage < 25:
            return "limited"
        elif percentage < 50:
            return "moderate"
        elif percentage < 75:
            return "significant"
        else:
            return "extensive"
            
    def _estimate_change_effort(self, directly_affected: List[Requirement], indirect_count: int) -> float:
        """Estimate effort required for change implementation"""
        direct_effort = sum(req.effort_estimate or 5.0 for req in directly_affected)
        indirect_effort = indirect_count * 2.0  # Assume 2 story points per indirect impact
        
        return direct_effort + indirect_effort
        
    def _assess_change_risks(self, change: Dict[str, Any], affected_ids: List[str]) -> str:
        """Assess risks associated with the change"""
        change_type = change.get("type", "modification")
        affected_count = len(affected_ids)
        
        risk_factors = []
        
        if change_type == "addition":
            risk_factors.append("New functionality may introduce integration issues")
        elif change_type == "deletion":
            risk_factors.append("Removing functionality may break dependent features")
        else:  # modification
            risk_factors.append("Modifying existing functionality may cause regression")
            
        if affected_count > 10:
            risk_factors.append("Large number of affected requirements increases complexity")
            
        if affected_count > 20:
            return "high"
        elif affected_count > 5:
            return "medium"
        else:
            return "low"
            
    def _generate_change_recommendations(self, scope: str, effort: float, risk: str) -> List[str]:
        """Generate recommendations for change implementation"""
        recommendations = []
        
        if scope in ["significant", "extensive"]:
            recommendations.extend([
                "Conduct detailed impact assessment with stakeholders",
                "Consider phased implementation approach",
                "Update project timeline and resource allocation"
            ])
            
        if effort > 40:
            recommendations.extend([
                "Allocate additional development resources",
                "Extend project timeline to accommodate changes",
                "Consider alternative solutions with lower effort"
            ])
            
        if risk == "high":
            recommendations.extend([
                "Implement comprehensive testing strategy",
                "Plan rollback procedures",
                "Conduct pilot implementation first"
            ])
            
        return recommendations
        
    def _requires_approval(self, scope: str, effort: float) -> bool:
        """Determine if change requires formal approval"""
        return scope in ["moderate", "significant", "extensive"] or effort > 20
        
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and metrics"""
        total_requirements = sum(len(reqs) for reqs in self.project_requirements.values())
        
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "status": "active",
            "capabilities": self.capabilities,
            "active_projects": len(self.project_requirements),
            "total_requirements": total_requirements,
            "conflicts_detected": len(self.conflict_database),
            "traceability_maps": len(self.traceability_maps),
            "uptime": "100%",
            "last_activity": datetime.now().isoformat()
        }

# Supporting Classes

class NLPProcessor:
    """Natural Language Processing for requirement extraction"""
    
    async def extract_from_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract requirements from document text"""
        await asyncio.sleep(1)
        
        text = document.get("content", "")
        doc_type = document.get("type", "general")
        
        # Simple requirement extraction patterns
        requirement_patterns = [
            r"The system shall (.+)",
            r"The application must (.+)",
            r"Users should be able to (.+)",
            r"The system will (.+)",
            r"(?:REQ|Requirement)\s*\d+:?\s*(.+)"
        ]
        
        extracted = []
        for pattern in requirement_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                extracted.append({
                    "text": match.group(1).strip(),
                    "source": document.get("name", "Document"),
                    "section": "Unknown",
                    "stakeholder": document.get("author", "Unknown")
                })
                
        # If no patterns match, extract sentences that look like requirements
        if not extracted:
            sentences = text.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20 and any(word in sentence.lower() for word in ["must", "shall", "should", "will", "required"]):
                    extracted.append({
                        "text": sentence,
                        "source": document.get("name", "Document"),
                        "section": "Unknown",
                        "stakeholder": document.get("author", "Unknown")
                    })
                    
        return extracted[:20]  # Limit to avoid overwhelming

class ConflictDetector:
    """Requirement conflict detection engine"""
    
    async def find_conflicts(self, requirements: List[Requirement]) -> List[RequirementConflict]:
        """Detect conflicts between requirements"""
        await asyncio.sleep(1.5)
        
        conflicts = []
        
        # Check for duplications
        conflicts.extend(self._detect_duplications(requirements))
        
        # Check for contradictions
        conflicts.extend(self._detect_contradictions(requirements))
        
        # Check for inconsistencies
        conflicts.extend(self._detect_inconsistencies(requirements))
        
        return conflicts
        
    def _detect_duplications(self, requirements: List[Requirement]) -> List[RequirementConflict]:
        """Detect duplicate requirements"""
        duplications = []
        
        for i, req1 in enumerate(requirements):
            for j, req2 in enumerate(requirements[i+1:], i+1):
                similarity = self._calculate_similarity(req1.description, req2.description)
                if similarity > 0.8:  # High similarity threshold
                    conflict = RequirementConflict(
                        conflict_id=f"conflict_{uuid.uuid4().hex[:8]}",
                        type=ConflictType.DUPLICATION,
                        description=f"Requirements {req1.req_id} and {req2.req_id} appear to be duplicates",
                        affected_requirements=[req1.req_id, req2.req_id],
                        severity="medium",
                        suggested_resolution="Merge duplicate requirements or clarify differences",
                        impact_assessment="May cause confusion and redundant implementation",
                        created_at=datetime.now()
                    )
                    duplications.append(conflict)
                    
        return duplications
        
    def _detect_contradictions(self, requirements: List[Requirement]) -> List[RequirementConflict]:
        """Detect contradictory requirements"""
        contradictions = []
        
        # Simple contradiction detection based on opposing keywords
        opposing_patterns = [
            (["must", "shall", "required"], ["must not", "shall not", "forbidden"]),
            (["always", "all"], ["never", "none"]),
            (["mandatory", "required"], ["optional", "may"])
        ]
        
        for i, req1 in enumerate(requirements):
            for j, req2 in enumerate(requirements[i+1:], i+1):
                if self._has_contradiction(req1.description, req2.description, opposing_patterns):
                    conflict = RequirementConflict(
                        conflict_id=f"conflict_{uuid.uuid4().hex[:8]}",
                        type=ConflictType.CONTRADICTION,
                        description=f"Requirements {req1.req_id} and {req2.req_id} contain contradictory statements",
                        affected_requirements=[req1.req_id, req2.req_id],
                        severity="high",
                        suggested_resolution="Review and resolve contradictory statements",
                        impact_assessment="May lead to implementation conflicts and system inconsistencies",
                        created_at=datetime.now()
                    )
                    contradictions.append(conflict)
                    
        return contradictions
        
    def _detect_inconsistencies(self, requirements: List[Requirement]) -> List[RequirementConflict]:
        """Detect inconsistent requirements"""
        inconsistencies = []
        
        # Group requirements by domain/tags
        domain_groups = {}
        for req in requirements:
            for tag in req.tags:
                if tag not in domain_groups:
                    domain_groups[tag] = []
                domain_groups[tag].append(req)
                
        # Check for inconsistencies within domains
        for domain, reqs in domain_groups.items():
            if len(reqs) > 1:
                inconsistency = self._check_domain_consistency(reqs, domain)
                if inconsistency:
                    inconsistencies.append(inconsistency)
                    
        return inconsistencies
        
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (simplified)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
        
    def _has_contradiction(self, text1: str, text2: str, patterns: List[Tuple]) -> bool:
        """Check if two texts contain contradictory statements"""
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        for positive_words, negative_words in patterns:
            text1_has_positive = any(word in text1_lower for word in positive_words)
            text1_has_negative = any(word in text1_lower for word in negative_words)
            text2_has_positive = any(word in text2_lower for word in positive_words)
            text2_has_negative = any(word in text2_lower for word in negative_words)
            
            # Check for contradictions
            if (text1_has_positive and text2_has_negative) or (text1_has_negative and text2_has_positive):
                return True
                
        return False
        
    def _check_domain_consistency(self, requirements: List[Requirement], domain: str) -> Optional[RequirementConflict]:
        """Check consistency within a domain"""
        # Simple consistency check - if multiple requirements in same domain have very different priorities
        priorities = [req.priority for req in requirements]
        
        if RequirementPriority.CRITICAL in priorities and RequirementPriority.LOW in priorities:
            return RequirementConflict(
                conflict_id=f"conflict_{uuid.uuid4().hex[:8]}",
                type=ConflictType.INCONSISTENCY,
                description=f"Inconsistent priorities in {domain} domain requirements",
                affected_requirements=[req.req_id for req in requirements],
                severity="medium",
                suggested_resolution="Review and align priority assignments within domain",
                impact_assessment="May indicate unclear domain importance or scope",
                created_at=datetime.now()
            )
            
        return None

class RequirementValidator:
    """Requirement quality and completeness validator"""
    
    async def validate_requirement(self, requirement: Requirement) -> Dict[str, Any]:
        """Validate individual requirement quality"""
        await asyncio.sleep(0.5)
        
        validation_result = {
            "req_id": requirement.req_id,
            "is_valid": True,
            "quality_score": 0.0,
            "issues": [],
            "suggestions": []
        }
        
        # Check completeness
        if not requirement.description or len(requirement.description) < 10:
            validation_result["issues"].append("Description too short or missing")
            validation_result["is_valid"] = False
            
        if not requirement.acceptance_criteria:
            validation_result["issues"].append("Missing acceptance criteria")
            validation_result["suggestions"].append("Add specific, testable acceptance criteria")
            
        # Check clarity
        if self._has_ambiguous_language(requirement.description):
            validation_result["issues"].append("Contains ambiguous language")
            validation_result["suggestions"].append("Replace vague terms with specific, measurable criteria")
            
        # Calculate quality score
        validation_result["quality_score"] = self._calculate_quality_score(requirement)
        
        return validation_result
        
    def _has_ambiguous_language(self, text: str) -> bool:
        """Check for ambiguous language patterns"""
        ambiguous_terms = ["appropriate", "reasonable", "user-friendly", "efficient", "fast", "good", "bad", "easy"]
        return any(term in text.lower() for term in ambiguous_terms)
        
    def _calculate_quality_score(self, requirement: Requirement) -> float:
        """Calculate overall quality score for requirement"""
        score = 0.0
        max_score = 5.0
        
        # Description quality
        if len(requirement.description) >= 20:
            score += 1.0
            
        # Has acceptance criteria
        if requirement.acceptance_criteria:
            score += 1.0
            
        # Priority assigned
        if requirement.priority != RequirementPriority.MEDIUM:
            score += 0.5
            
        # Has tags
        if requirement.tags:
            score += 0.5
            
        # Effort estimated
        if requirement.effort_estimate:
            score += 1.0
            
        # Stakeholder identified
        if requirement.stakeholder != "Unknown":
            score += 1.0
            
        return (score / max_score) * 100

# Example usage and testing
async def main():
    """Test the Requirements Analyst Agent functionality"""
    req_agent = RequirementsAnalystAgent()
    
    print("📄 Requirements Analyst Agent - Intelligent Requirement Management")
    print("=" * 70)
    
    # Test requirement extraction
    documents = [
        {
            "name": "Business Requirements Document",
            "content": "The system shall allow users to login with username and password. The application must provide real-time notifications. Users should be able to generate reports.",
            "type": "business_requirements",
            "author": "Business Analyst",
            "project": "Customer Portal"
        }
    ]
    
    extracted_requirements = await req_agent.extract_requirements(documents)
    print(f"✅ Requirement Extraction: {len(extracted_requirements)} requirements extracted")
    for req in extracted_requirements:
        print(f"   {req.req_id}: {req.title[:50]}...")
    
    # Test requirements analysis
    analysis = await req_agent.analyze_requirements("Customer Portal")
    print(f"✅ Requirements Analysis: {analysis.analysis_id}")
    print(f"   Total Requirements: {analysis.total_requirements}")
    print(f"   Completeness Score: {analysis.completeness_score:.1f}%")
    print(f"   Quality Score: {analysis.quality_score:.1f}%")
    print(f"   Conflicts Detected: {len(analysis.conflicts)}")
    
    # Test change impact analysis
    change_proposal = {
        "description": "Add two-factor authentication requirement",
        "type": "addition",
        "affected_requirements": [extracted_requirements[0].req_id]
    }
    
    impact_analysis = await req_agent.analyze_change_impact("Customer Portal", change_proposal)
    print(f"✅ Change Impact Analysis: {impact_analysis.change_id}")
    print(f"   Impact Scope: {impact_analysis.impact_scope}")
    print(f"   Effort Estimate: {impact_analysis.effort_estimate} story points")
    print(f"   Approval Required: {impact_analysis.approval_required}")
    
    # Display agent status
    status = req_agent.get_agent_status()
    print(f"\n📊 Agent Status: {status['status'].upper()}")
    print(f"   Active Projects: {status['active_projects']}")
    print(f"   Total Requirements: {status['total_requirements']}")
    print(f"   Conflicts Detected: {status['conflicts_detected']}")

if __name__ == "__main__":
    asyncio.run(main())
