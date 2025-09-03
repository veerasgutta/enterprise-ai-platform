"""
Enterprise Security Operations Agent
Advanced cybersecurity monitoring and incident response for enterprise environments
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    """Security threat levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(Enum):
    """Incident response statuses"""
    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"

class AttackType(Enum):
    """Types of security attacks"""
    MALWARE = "malware"
    PHISHING = "phishing"
    DDoS = "ddos"
    BRUTE_FORCE = "brute_force"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    INSIDER_THREAT = "insider_threat"
    DATA_BREACH = "data_breach"
    RANSOMWARE = "ransomware"

class AssetType(Enum):
    """Types of security assets"""
    SERVER = "server"
    WORKSTATION = "workstation"
    MOBILE = "mobile"
    NETWORK = "network"
    DATABASE = "database"
    APPLICATION = "application"
    CLOUD_SERVICE = "cloud_service"

class ComplianceFramework(Enum):
    """Compliance frameworks"""
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    NIST = "nist"

@dataclass
class SecurityIncident:
    """Security incident data model"""
    incident_id: str
    title: str
    description: str
    threat_level: ThreatLevel
    attack_type: AttackType
    status: IncidentStatus
    affected_assets: List[str]
    discovered_at: datetime
    reported_by: str
    assigned_to: Optional[str] = None
    resolved_at: Optional[datetime] = None
    impact_assessment: Dict[str, Any] = field(default_factory=dict)
    remediation_steps: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)

@dataclass
class SecurityAlert:
    """Security alert data model"""
    alert_id: str
    source: str
    event_type: str
    severity: ThreatLevel
    timestamp: datetime
    source_ip: Optional[str]
    destination_ip: Optional[str]
    user_account: Optional[str]
    asset_id: Optional[str]
    raw_data: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    false_positive: bool = False

@dataclass
class VulnerabilityAssessment:
    """Vulnerability assessment data model"""
    assessment_id: str
    asset_id: str
    asset_type: AssetType
    vulnerability_type: str
    cvss_score: float
    severity: ThreatLevel
    description: str
    recommendation: str
    discovered_at: datetime
    patched: bool = False
    patch_date: Optional[datetime] = None
    risk_accepted: bool = False

@dataclass
class ComplianceCheck:
    """Compliance check data model"""
    check_id: str
    framework: ComplianceFramework
    control_id: str
    description: str
    status: str  # compliant, non_compliant, not_applicable
    evidence: List[str]
    last_assessed: datetime
    next_assessment: datetime
    responsible_party: str
    remediation_required: bool = False

@dataclass
class SecurityAsset:
    """Security asset data model"""
    asset_id: str
    name: str
    type: AssetType
    ip_address: Optional[str]
    location: str
    owner: str
    criticality: str  # low, medium, high, critical
    last_scan: datetime
    vulnerabilities: int = 0
    patch_level: str = "unknown"
    security_tools: List[str] = field(default_factory=list)

class SecurityOperationsAgent:
    """
    Advanced Security Operations Agent for Enterprise Cybersecurity
    
    Capabilities:
    1. Threat Detection & Analysis
    2. Incident Response Management
    3. Vulnerability Assessment
    4. Compliance Monitoring
    5. Security Analytics
    6. Asset Management
    7. Risk Assessment
    8. Security Automation
    """
    
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id or f"secops_{uuid.uuid4().hex[:6]}"
        self.status = "active"
        self.capabilities = [
            "threat_detection",
            "incident_response",
            "vulnerability_assessment",
            "compliance_monitoring",
            "security_analytics",
            "asset_management",
            "risk_assessment",
            "security_automation"
        ]
        
        # Data storage
        self.incidents: List[SecurityIncident] = []
        self.alerts: List[SecurityAlert] = []
        self.vulnerabilities: List[VulnerabilityAssessment] = []
        self.compliance_checks: List[ComplianceCheck] = []
        self.assets: List[SecurityAsset] = []
        
        # Security metrics
        self.metrics = {
            "total_incidents": 0,
            "open_incidents": 0,
            "critical_incidents": 0,
            "mean_time_to_detection": 0.0,
            "mean_time_to_response": 0.0,
            "alerts_processed": 0,
            "false_positive_rate": 0.0,
            "compliance_score": 0.0,
            "vulnerabilities_found": 0,
            "vulnerabilities_patched": 0
        }
        
        # Initialize sample data
        self._initialize_sample_data()
        
        logger.info(f"Security Operations Agent {self.agent_id} initialized with {len(self.capabilities)} capabilities")

    def _initialize_sample_data(self):
        """Initialize with sample security data"""
        
        # Sample incidents
        sample_incidents = [
            SecurityIncident(
                incident_id="INC001",
                title="Suspicious Login Activity",
                description="Multiple failed login attempts detected from unusual geographic location",
                threat_level=ThreatLevel.MEDIUM,
                attack_type=AttackType.BRUTE_FORCE,
                status=IncidentStatus.INVESTIGATING,
                affected_assets=["WS001", "WS002"],
                discovered_at=datetime.now() - timedelta(hours=6),
                reported_by="security_monitor_001",
                assigned_to="analyst_jones",
                impact_assessment={
                    "data_compromised": False,
                    "systems_affected": 2,
                    "business_impact": "minimal"
                },
                remediation_steps=[
                    "Reset affected user passwords",
                    "Enable additional MFA requirements",
                    "Block suspicious IP ranges"
                ]
            ),
            SecurityIncident(
                incident_id="INC002",
                title="Malware Detection on Endpoint",
                description="Antivirus software detected and quarantined potential malware on employee workstation",
                threat_level=ThreatLevel.HIGH,
                attack_type=AttackType.MALWARE,
                status=IncidentStatus.CONTAINED,
                affected_assets=["WS005"],
                discovered_at=datetime.now() - timedelta(hours=12),
                reported_by="endpoint_protection",
                assigned_to="analyst_smith",
                impact_assessment={
                    "data_compromised": False,
                    "systems_affected": 1,
                    "business_impact": "low"
                },
                remediation_steps=[
                    "Isolate affected workstation",
                    "Run full system scan",
                    "Restore from backup if necessary",
                    "Update endpoint protection signatures"
                ]
            ),
            SecurityIncident(
                incident_id="INC003",
                title="Data Exfiltration Attempt",
                description="Unusual data transfer patterns detected - potential data exfiltration",
                threat_level=ThreatLevel.CRITICAL,
                attack_type=AttackType.DATA_BREACH,
                status=IncidentStatus.RESOLVED,
                affected_assets=["DB001", "APP001"],
                discovered_at=datetime.now() - timedelta(days=2),
                reported_by="data_loss_prevention",
                assigned_to="senior_analyst_brown",
                resolved_at=datetime.now() - timedelta(hours=8),
                impact_assessment={
                    "data_compromised": True,
                    "records_affected": 1250,
                    "systems_affected": 2,
                    "business_impact": "moderate"
                },
                remediation_steps=[
                    "Block suspicious network traffic",
                    "Revoke access credentials",
                    "Conduct forensic analysis",
                    "Notify affected customers",
                    "Implement additional monitoring"
                ],
                lessons_learned=[
                    "Strengthen data access controls",
                    "Implement additional network segmentation",
                    "Enhance employee security training"
                ]
            )
        ]
        
        for incident in sample_incidents:
            self.incidents.append(incident)
        
        # Sample alerts
        sample_alerts = [
            SecurityAlert(
                alert_id="ALERT001",
                source="firewall",
                event_type="port_scan",
                severity=ThreatLevel.MEDIUM,
                timestamp=datetime.now() - timedelta(minutes=30),
                source_ip="203.0.113.45",
                destination_ip="10.0.1.100",
                user_account=None,
                asset_id=None,
                raw_data={"ports_scanned": [22, 80, 443, 3389], "duration": "15min"}
            ),
            SecurityAlert(
                alert_id="ALERT002",
                source="ids",
                event_type="sql_injection_attempt",
                severity=ThreatLevel.HIGH,
                timestamp=datetime.now() - timedelta(minutes=15),
                source_ip="198.51.100.23",
                destination_ip="10.0.2.50",
                user_account="web_app_user",
                asset_id="APP001",
                raw_data={"payload": "' OR 1=1 --", "endpoint": "/api/users"}
            ),
            SecurityAlert(
                alert_id="ALERT003",
                source="endpoint_protection",
                event_type="malware_detected",
                severity=ThreatLevel.CRITICAL,
                timestamp=datetime.now() - timedelta(hours=2),
                source_ip=None,
                destination_ip=None,
                user_account="john.doe",
                asset_id="WS007",
                raw_data={"malware_family": "trojan.banker", "file_path": "C:\\temp\\update.exe"}
            )
        ]
        
        for alert in sample_alerts:
            self.alerts.append(alert)
        
        # Sample vulnerabilities
        sample_vulnerabilities = [
            VulnerabilityAssessment(
                assessment_id="VULN001",
                asset_id="SRV001",
                asset_type=AssetType.SERVER,
                vulnerability_type="CVE-2023-4567",
                cvss_score=8.9,
                severity=ThreatLevel.HIGH,
                description="Remote code execution vulnerability in web server software",
                recommendation="Apply security patch version 2.4.51 immediately",
                discovered_at=datetime.now() - timedelta(days=5),
                patched=False
            ),
            VulnerabilityAssessment(
                assessment_id="VULN002",
                asset_id="DB001",
                asset_type=AssetType.DATABASE,
                vulnerability_type="CVE-2023-1234",
                cvss_score=6.5,
                severity=ThreatLevel.MEDIUM,
                description="SQL injection vulnerability in database interface",
                recommendation="Update database software to version 10.5.12",
                discovered_at=datetime.now() - timedelta(days=10),
                patched=True,
                patch_date=datetime.now() - timedelta(days=3)
            ),
            VulnerabilityAssessment(
                assessment_id="VULN003",
                asset_id="WS010",
                asset_type=AssetType.WORKSTATION,
                vulnerability_type="CVE-2023-8901",
                cvss_score=4.3,
                severity=ThreatLevel.LOW,
                description="Information disclosure vulnerability in office software",
                recommendation="Apply software update when convenient",
                discovered_at=datetime.now() - timedelta(days=15),
                patched=False
            )
        ]
        
        for vuln in sample_vulnerabilities:
            self.vulnerabilities.append(vuln)
        
        # Sample compliance checks
        sample_compliance = [
            ComplianceCheck(
                check_id="SOC2_001",
                framework=ComplianceFramework.SOC2,
                control_id="CC6.1",
                description="Logical and physical access controls",
                status="compliant",
                evidence=["access_control_policy.pdf", "quarterly_access_review.xlsx"],
                last_assessed=datetime.now() - timedelta(days=30),
                next_assessment=datetime.now() + timedelta(days=60),
                responsible_party="security_team"
            ),
            ComplianceCheck(
                check_id="ISO_001",
                framework=ComplianceFramework.ISO27001,
                control_id="A.12.6.1",
                description="Management of technical vulnerabilities",
                status="non_compliant",
                evidence=["vulnerability_scan_report.pdf"],
                last_assessed=datetime.now() - timedelta(days=15),
                next_assessment=datetime.now() + timedelta(days=15),
                responsible_party="it_operations",
                remediation_required=True
            ),
            ComplianceCheck(
                check_id="GDPR_001",
                framework=ComplianceFramework.GDPR,
                control_id="Art.32",
                description="Security of processing",
                status="compliant",
                evidence=["encryption_policy.pdf", "data_protection_assessment.doc"],
                last_assessed=datetime.now() - timedelta(days=45),
                next_assessment=datetime.now() + timedelta(days=45),
                responsible_party="data_protection_officer"
            )
        ]
        
        for compliance in sample_compliance:
            self.compliance_checks.append(compliance)
        
        # Sample assets
        sample_assets = [
            SecurityAsset(
                asset_id="SRV001",
                name="Web Server 1",
                type=AssetType.SERVER,
                ip_address="10.0.1.100",
                location="DataCenter-A",
                owner="it_operations",
                criticality="high",
                last_scan=datetime.now() - timedelta(days=7),
                vulnerabilities=1,
                patch_level="current-1",
                security_tools=["antivirus", "intrusion_detection", "log_monitoring"]
            ),
            SecurityAsset(
                asset_id="DB001",
                name="Primary Database",
                type=AssetType.DATABASE,
                ip_address="10.0.2.50",
                location="DataCenter-A",
                owner="database_admin",
                criticality="critical",
                last_scan=datetime.now() - timedelta(days=3),
                vulnerabilities=0,
                patch_level="current",
                security_tools=["database_firewall", "encryption", "access_monitoring"]
            ),
            SecurityAsset(
                asset_id="WS007",
                name="Executive Workstation",
                type=AssetType.WORKSTATION,
                ip_address="10.0.3.75",
                location="Executive-Floor",
                owner="john.doe",
                criticality="high",
                last_scan=datetime.now() - timedelta(hours=8),
                vulnerabilities=0,
                patch_level="current",
                security_tools=["endpoint_protection", "dlp_agent", "web_filter"]
            )
        ]
        
        for asset in sample_assets:
            self.assets.append(asset)
        
        # Update metrics
        self._update_metrics()

    async def create_incident(self, title: str, description: str, threat_level: ThreatLevel,
                            attack_type: AttackType, affected_assets: List[str]) -> SecurityIncident:
        """Create a new security incident"""
        try:
            incident = SecurityIncident(
                incident_id=f"INC{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6].upper()}",
                title=title,
                description=description,
                threat_level=threat_level,
                attack_type=attack_type,
                status=IncidentStatus.OPEN,
                affected_assets=affected_assets,
                discovered_at=datetime.now(),
                reported_by="security_agent"
            )
            
            self.incidents.append(incident)
            self.metrics["total_incidents"] += 1
            
            if threat_level == ThreatLevel.CRITICAL:
                self.metrics["critical_incidents"] += 1
            
            self._update_metrics()
            
            logger.info(f"Security incident {incident.incident_id} created: {title}")
            return incident
            
        except Exception as e:
            logger.error(f"Failed to create incident: {str(e)}")
            raise

    async def process_alert(self, source: str, event_type: str, severity: ThreatLevel,
                          source_ip: str = None, destination_ip: str = None) -> SecurityAlert:
        """Process a new security alert"""
        try:
            alert = SecurityAlert(
                alert_id=f"ALERT{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6].upper()}",
                source=source,
                event_type=event_type,
                severity=severity,
                timestamp=datetime.now(),
                source_ip=source_ip,
                destination_ip=destination_ip,
                user_account=None,
                asset_id=None
            )
            
            self.alerts.append(alert)
            self.metrics["alerts_processed"] += 1
            
            # Auto-escalate critical alerts to incidents
            if severity == ThreatLevel.CRITICAL:
                await self.create_incident(
                    title=f"Critical Alert: {event_type}",
                    description=f"Critical security alert from {source}",
                    threat_level=severity,
                    attack_type=self._map_event_to_attack_type(event_type),
                    affected_assets=[]
                )
            
            logger.info(f"Security alert {alert.alert_id} processed: {event_type}")
            return alert
            
        except Exception as e:
            logger.error(f"Failed to process alert: {str(e)}")
            raise

    def _map_event_to_attack_type(self, event_type: str) -> AttackType:
        """Map alert event type to attack type"""
        mapping = {
            "malware_detected": AttackType.MALWARE,
            "phishing_attempt": AttackType.PHISHING,
            "brute_force": AttackType.BRUTE_FORCE,
            "sql_injection_attempt": AttackType.SQL_INJECTION,
            "port_scan": AttackType.BRUTE_FORCE,
            "data_exfiltration": AttackType.DATA_BREACH
        }
        return mapping.get(event_type, AttackType.MALWARE)

    async def conduct_vulnerability_scan(self, asset_id: str) -> List[VulnerabilityAssessment]:
        """Conduct vulnerability assessment on specified asset"""
        try:
            asset = next((a for a in self.assets if a.asset_id == asset_id), None)
            if not asset:
                raise ValueError(f"Asset {asset_id} not found")
            
            # Simulate vulnerability scanning
            vulnerabilities = []
            
            # Generate random vulnerabilities based on asset type
            if asset.type == AssetType.SERVER:
                vuln_count = 2  # Servers typically have more vulnerabilities
            elif asset.type == AssetType.DATABASE:
                vuln_count = 1
            else:
                vuln_count = 1
            
            for i in range(vuln_count):
                severity = ThreatLevel.MEDIUM if i == 0 else ThreatLevel.LOW
                cvss_score = 6.5 if severity == ThreatLevel.MEDIUM else 3.2
                
                vulnerability = VulnerabilityAssessment(
                    assessment_id=f"VULN{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6].upper()}",
                    asset_id=asset_id,
                    asset_type=asset.type,
                    vulnerability_type=f"CVE-2023-{1000 + i}",
                    cvss_score=cvss_score,
                    severity=severity,
                    description=f"Vulnerability found in {asset.type.value} component",
                    recommendation="Apply security patch or implement workaround",
                    discovered_at=datetime.now()
                )
                
                vulnerabilities.append(vulnerability)
                self.vulnerabilities.append(vulnerability)
            
            asset.last_scan = datetime.now()
            asset.vulnerabilities = len(vulnerabilities)
            self.metrics["vulnerabilities_found"] += len(vulnerabilities)
            
            logger.info(f"Vulnerability scan completed for {asset_id}: {len(vulnerabilities)} vulnerabilities found")
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Vulnerability scan failed: {str(e)}")
            raise

    async def assess_compliance(self, framework: ComplianceFramework) -> Dict[str, Any]:
        """Assess compliance status for specified framework"""
        try:
            framework_checks = [c for c in self.compliance_checks if c.framework == framework]
            
            if not framework_checks:
                return {"framework": framework.value, "status": "not_assessed", "score": 0.0}
            
            total_checks = len(framework_checks)
            compliant_checks = len([c for c in framework_checks if c.status == "compliant"])
            non_compliant = len([c for c in framework_checks if c.status == "non_compliant"])
            
            compliance_score = (compliant_checks / total_checks * 100) if total_checks > 0 else 0
            
            assessment = {
                "framework": framework.value,
                "total_controls": total_checks,
                "compliant": compliant_checks,
                "non_compliant": non_compliant,
                "compliance_score": round(compliance_score, 2),
                "status": "compliant" if compliance_score >= 90 else "needs_attention",
                "last_assessed": max(c.last_assessed for c in framework_checks).isoformat()
            }
            
            return assessment
            
        except Exception as e:
            logger.error(f"Compliance assessment failed: {str(e)}")
            return {}

    async def respond_to_incident(self, incident_id: str, response_actions: List[str]) -> bool:
        """Execute incident response actions"""
        try:
            incident = next((i for i in self.incidents if i.incident_id == incident_id), None)
            if not incident:
                return False
            
            incident.status = IncidentStatus.INVESTIGATING
            incident.assigned_to = "security_agent"
            incident.remediation_steps.extend(response_actions)
            
            # Simulate response actions
            for action in response_actions:
                logger.info(f"Executing response action: {action}")
            
            # Auto-resolve low-threat incidents
            if incident.threat_level == ThreatLevel.LOW:
                incident.status = IncidentStatus.RESOLVED
                incident.resolved_at = datetime.now()
            
            self._update_metrics()
            
            logger.info(f"Incident response initiated for {incident_id}")
            return True
            
        except Exception as e:
            logger.error(f"Incident response failed: {str(e)}")
            return False

    async def analyze_security_trends(self) -> Dict[str, Any]:
        """Analyze security trends and patterns"""
        try:
            # Incident trends
            recent_incidents = [i for i in self.incidents if i.discovered_at >= datetime.now() - timedelta(days=30)]
            incident_types = {}
            for incident in recent_incidents:
                attack_type = incident.attack_type.value
                incident_types[attack_type] = incident_types.get(attack_type, 0) + 1
            
            # Alert trends
            recent_alerts = [a for a in self.alerts if a.timestamp >= datetime.now() - timedelta(days=7)]
            alert_sources = {}
            for alert in recent_alerts:
                source = alert.source
                alert_sources[source] = alert_sources.get(source, 0) + 1
            
            # Vulnerability trends
            unpatched_vulns = [v for v in self.vulnerabilities if not v.patched]
            high_risk_vulns = [v for v in unpatched_vulns if v.severity in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]]
            
            trends = {
                "incident_summary": {
                    "total_30_days": len(recent_incidents),
                    "by_attack_type": incident_types,
                    "avg_resolution_time": self._calculate_avg_resolution_time(recent_incidents)
                },
                "alert_summary": {
                    "total_7_days": len(recent_alerts),
                    "by_source": alert_sources,
                    "false_positive_rate": self.metrics["false_positive_rate"]
                },
                "vulnerability_summary": {
                    "total_unpatched": len(unpatched_vulns),
                    "high_risk": len(high_risk_vulns),
                    "patch_rate": self._calculate_patch_rate()
                }
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Security trend analysis failed: {str(e)}")
            return {}

    def _calculate_avg_resolution_time(self, incidents: List[SecurityIncident]) -> float:
        """Calculate average incident resolution time in hours"""
        resolved_incidents = [i for i in incidents if i.resolved_at]
        if not resolved_incidents:
            return 0.0
        
        total_time = sum((i.resolved_at - i.discovered_at).total_seconds() for i in resolved_incidents)
        avg_seconds = total_time / len(resolved_incidents)
        return round(avg_seconds / 3600, 2)  # Convert to hours

    def _calculate_patch_rate(self) -> float:
        """Calculate vulnerability patch rate percentage"""
        if not self.vulnerabilities:
            return 0.0
        
        patched = len([v for v in self.vulnerabilities if v.patched])
        return round((patched / len(self.vulnerabilities)) * 100, 2)

    async def automate_threat_hunting(self) -> List[Dict[str, Any]]:
        """Perform automated threat hunting"""
        try:
            hunting_results = []
            
            # Hunt for suspicious IP patterns
            ip_activity = {}
            for alert in self.alerts:
                if alert.source_ip:
                    ip_activity[alert.source_ip] = ip_activity.get(alert.source_ip, 0) + 1
            
            for ip, count in ip_activity.items():
                if count >= 5:  # Suspicious threshold
                    hunting_results.append({
                        "type": "suspicious_ip",
                        "indicator": ip,
                        "activity_count": count,
                        "risk_level": "high" if count >= 10 else "medium",
                        "recommendation": "Investigate and consider blocking"
                    })
            
            # Hunt for unusual user activity
            user_activity = {}
            for alert in self.alerts:
                if alert.user_account:
                    user_activity[alert.user_account] = user_activity.get(alert.user_account, 0) + 1
            
            for user, count in user_activity.items():
                if count >= 3:  # Suspicious threshold
                    hunting_results.append({
                        "type": "suspicious_user",
                        "indicator": user,
                        "activity_count": count,
                        "risk_level": "medium",
                        "recommendation": "Review user activity and access rights"
                    })
            
            return hunting_results
            
        except Exception as e:
            logger.error(f"Threat hunting failed: {str(e)}")
            return []

    def _update_metrics(self):
        """Update security metrics"""
        self.metrics["total_incidents"] = len(self.incidents)
        self.metrics["open_incidents"] = len([i for i in self.incidents if i.status in [IncidentStatus.OPEN, IncidentStatus.INVESTIGATING]])
        self.metrics["critical_incidents"] = len([i for i in self.incidents if i.threat_level == ThreatLevel.CRITICAL])
        
        # Calculate compliance score (average across all frameworks)
        if self.compliance_checks:
            compliant = len([c for c in self.compliance_checks if c.status == "compliant"])
            self.metrics["compliance_score"] = round((compliant / len(self.compliance_checks)) * 100, 2)
        
        self.metrics["vulnerabilities_found"] = len(self.vulnerabilities)
        self.metrics["vulnerabilities_patched"] = len([v for v in self.vulnerabilities if v.patched])

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "capabilities": self.capabilities,
            "incidents": len(self.incidents),
            "alerts": len(self.alerts),
            "vulnerabilities": len(self.vulnerabilities),
            "assets": len(self.assets),
            "metrics": self.metrics,
            "last_updated": datetime.now().isoformat()
        }

# Demo function
async def demo_security_operations_agent():
    """Demonstrate Security Operations Agent capabilities"""
    
    print("🚀 Starting Security Operations Agent Demo...")
    
    # Initialize agent
    secops_agent = SecurityOperationsAgent()
    
    print("\n🔒 Security Operations Agent Demo:")
    print("=" * 50)
    
    # 1. Create incident
    print("🚨 Incident Creation:")
    incident = await secops_agent.create_incident(
        title="Suspicious Network Activity",
        description="Unusual outbound traffic detected from internal network",
        threat_level=ThreatLevel.HIGH,
        attack_type=AttackType.DATA_BREACH,
        affected_assets=["SRV001", "WS007"]
    )
    print(f"  Incident ID: {incident.incident_id}")
    print(f"  Threat Level: {incident.threat_level.value}")
    print(f"  Attack Type: {incident.attack_type.value}")
    
    # 2. Process alert
    print("\n⚠️ Alert Processing:")
    alert = await secops_agent.process_alert(
        source="network_monitor",
        event_type="data_exfiltration",
        severity=ThreatLevel.CRITICAL,
        source_ip="10.0.1.50",
        destination_ip="203.0.113.100"
    )
    print(f"  Alert ID: {alert.alert_id}")
    print(f"  Severity: {alert.severity.value}")
    print(f"  Source: {alert.source}")
    
    # 3. Vulnerability scan
    print("\n🔍 Vulnerability Assessment:")
    vulnerabilities = await secops_agent.conduct_vulnerability_scan("SRV001")
    print(f"  Vulnerabilities Found: {len(vulnerabilities)}")
    for vuln in vulnerabilities:
        print(f"  {vuln.vulnerability_type}: {vuln.severity.value} (CVSS: {vuln.cvss_score})")
    
    # 4. Compliance assessment
    print("\n📋 Compliance Assessment:")
    compliance = await secops_agent.assess_compliance(ComplianceFramework.SOC2)
    print(f"  Framework: {compliance['framework']}")
    print(f"  Compliance Score: {compliance['compliance_score']}%")
    print(f"  Status: {compliance['status']}")
    
    # 5. Security trends
    print("\n📊 Security Trends:")
    trends = await secops_agent.analyze_security_trends()
    print(f"  Incidents (30 days): {trends['incident_summary']['total_30_days']}")
    print(f"  Alerts (7 days): {trends['alert_summary']['total_7_days']}")
    print(f"  Unpatched Vulnerabilities: {trends['vulnerability_summary']['total_unpatched']}")
    
    # 6. Agent status
    status = await secops_agent.get_agent_status()
    print(f"\n🤖 Agent Status: {status['status']} | Incidents: {status['incidents']} | Alerts: {status['alerts']}")

if __name__ == "__main__":
    asyncio.run(demo_security_operations_agent())
