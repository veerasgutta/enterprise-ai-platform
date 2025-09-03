"""
Enterprise Marketing Agent
Advanced marketing automation and campaign management for enterprise operations
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

class CampaignType(Enum):
    """Marketing campaign types"""
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    CONTENT = "content"
    PAID_ADS = "paid_ads"
    WEBINAR = "webinar"
    EVENT = "event"

class CampaignStatus(Enum):
    """Campaign execution statuses"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class LeadSource(Enum):
    """Lead generation sources"""
    WEBSITE = "website"
    SOCIAL_MEDIA = "social_media"
    EMAIL_CAMPAIGN = "email_campaign"
    WEBINAR = "webinar"
    REFERRAL = "referral"
    PAID_ADS = "paid_ads"
    CONTENT = "content"

class ContentType(Enum):
    """Content types for marketing"""
    BLOG_POST = "blog_post"
    WHITEPAPER = "whitepaper"
    VIDEO = "video"
    INFOGRAPHIC = "infographic"
    CASE_STUDY = "case_study"
    EBOOK = "ebook"

@dataclass
class Campaign:
    """Marketing campaign data model"""
    campaign_id: str
    name: str
    type: CampaignType
    status: CampaignStatus
    budget: float
    start_date: datetime
    end_date: datetime
    target_audience: Dict[str, Any]
    channels: List[str]
    created_by: str
    metrics: Dict[str, float] = field(default_factory=dict)
    content_assets: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class Lead:
    """Marketing lead data model"""
    lead_id: str
    name: str
    email: str
    phone: Optional[str]
    company: str
    job_title: str
    source: LeadSource
    campaign_id: Optional[str]
    score: float  # 0-100
    created_at: datetime
    last_interaction: datetime
    interests: List[str] = field(default_factory=list)
    activities: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class Content:
    """Marketing content data model"""
    content_id: str
    title: str
    type: ContentType
    status: str  # draft, published, archived
    author: str
    created_at: datetime
    published_at: Optional[datetime]
    views: int = 0
    downloads: int = 0
    shares: int = 0
    conversion_rate: float = 0.0
    keywords: List[str] = field(default_factory=list)
    campaigns: List[str] = field(default_factory=list)

@dataclass
class MarketingMetrics:
    """Marketing performance metrics"""
    period: str
    total_leads: int
    qualified_leads: int
    conversion_rate: float
    cost_per_lead: float
    revenue_attributed: float
    roi: float
    website_visitors: int
    email_open_rate: float
    social_engagement: int

class MarketingAgent:
    """
    Advanced Marketing Agent for Enterprise Campaign Management
    
    Capabilities:
    1. Campaign Management
    2. Lead Generation & Scoring
    3. Content Marketing
    4. Performance Analytics
    5. Audience Segmentation
    6. Social Media Management
    7. Email Marketing
    8. Marketing Automation
    """
    
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id or f"marketing_{uuid.uuid4().hex[:6]}"
        self.status = "active"
        self.capabilities = [
            "campaign_management",
            "lead_generation",
            "content_marketing",
            "performance_analytics",
            "audience_segmentation",
            "social_media_management",
            "email_marketing",
            "marketing_automation"
        ]
        
        # Data storage
        self.campaigns: List[Campaign] = []
        self.leads: List[Lead] = []
        self.content: List[Content] = []
        self.metrics_history: List[MarketingMetrics] = []
        
        # Performance metrics
        self.metrics = {
            "total_campaigns": 0,
            "active_campaigns": 0,
            "total_leads": 0,
            "qualified_leads": 0,
            "conversion_rate": 0.0,
            "avg_lead_score": 0.0,
            "content_pieces": 0,
            "roi": 0.0
        }
        
        # Initialize sample data
        self._initialize_sample_data()
        
        logger.info(f"Marketing Agent {self.agent_id} initialized with {len(self.capabilities)} capabilities")

    def _initialize_sample_data(self):
        """Initialize with sample campaigns, leads, and content"""
        
        # Sample campaigns
        sample_campaigns = [
            Campaign(
                campaign_id="CAMP001",
                name="Enterprise AI Platform Launch",
                type=CampaignType.EMAIL,
                status=CampaignStatus.ACTIVE,
                budget=50000.0,
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now() + timedelta(days=30),
                target_audience={
                    "industries": ["Technology", "Finance", "Healthcare"],
                    "company_size": ["Enterprise", "Mid-market"],
                    "job_titles": ["CTO", "VP Engineering", "IT Director"]
                },
                channels=["email", "linkedin", "website"],
                created_by="marketing_manager_001",
                metrics={
                    "impressions": 125000,
                    "clicks": 3750,
                    "conversions": 187,
                    "cost": 12500.0,
                    "ctr": 3.0,
                    "conversion_rate": 4.99
                },
                content_assets=["email_template_001", "landing_page_001", "demo_video"],
                tags=["product_launch", "enterprise", "ai"]
            ),
            Campaign(
                campaign_id="CAMP002",
                name="Content Marketing - AI Insights",
                type=CampaignType.CONTENT,
                status=CampaignStatus.ACTIVE,
                budget=25000.0,
                start_date=datetime.now() - timedelta(days=60),
                end_date=datetime.now() + timedelta(days=90),
                target_audience={
                    "industries": ["Technology", "Consulting"],
                    "interests": ["Artificial Intelligence", "Machine Learning", "Automation"]
                },
                channels=["blog", "social_media", "webinar"],
                created_by="content_manager_001",
                metrics={
                    "impressions": 75000,
                    "engagement": 4500,
                    "leads": 89,
                    "cost": 8750.0,
                    "engagement_rate": 6.0
                },
                content_assets=["blog_series_ai", "whitepaper_automation", "webinar_series"],
                tags=["content", "thought_leadership", "ai"]
            ),
            Campaign(
                campaign_id="CAMP003",
                name="Retargeting Campaign - Demo Requests",
                type=CampaignType.PAID_ADS,
                status=CampaignStatus.SCHEDULED,
                budget=15000.0,
                start_date=datetime.now() + timedelta(days=7),
                end_date=datetime.now() + timedelta(days=37),
                target_audience={
                    "behavior": ["visited_demo_page", "downloaded_whitepaper"],
                    "company_size": ["Mid-market", "Enterprise"]
                },
                channels=["google_ads", "linkedin_ads"],
                created_by="digital_marketing_specialist",
                tags=["retargeting", "conversion", "demo"]
            )
        ]
        
        for campaign in sample_campaigns:
            self.campaigns.append(campaign)
        
        # Sample leads
        sample_leads = [
            Lead(
                lead_id="MKT_LEAD001",
                name="Sarah Chen",
                email="s.chen@techcorp.com",
                phone="+1-555-0191",
                company="TechCorp Solutions",
                job_title="VP of Engineering",
                source=LeadSource.EMAIL_CAMPAIGN,
                campaign_id="CAMP001",
                score=85.0,
                created_at=datetime.now() - timedelta(days=5),
                last_interaction=datetime.now() - timedelta(hours=8),
                interests=["AI Platform", "Enterprise Solutions", "Automation"],
                activities=[
                    {"type": "email_open", "timestamp": datetime.now() - timedelta(days=5), "campaign": "CAMP001"},
                    {"type": "website_visit", "timestamp": datetime.now() - timedelta(days=3), "page": "/demo"},
                    {"type": "whitepaper_download", "timestamp": datetime.now() - timedelta(hours=8), "content": "AI_Enterprise_Guide"}
                ]
            ),
            Lead(
                lead_id="MKT_LEAD002",
                name="Michael Rodriguez",
                email="m.rodriguez@innovate.inc",
                phone="+1-555-0292",
                company="Innovate Inc",
                job_title="CTO",
                source=LeadSource.WEBINAR,
                campaign_id="CAMP002",
                score=92.0,
                created_at=datetime.now() - timedelta(days=12),
                last_interaction=datetime.now() - timedelta(hours=2),
                interests=["Machine Learning", "Data Analytics", "Platform Integration"],
                activities=[
                    {"type": "webinar_attendance", "timestamp": datetime.now() - timedelta(days=12), "event": "AI_Insights_Webinar"},
                    {"type": "demo_request", "timestamp": datetime.now() - timedelta(days=8), "interest": "Enterprise Package"},
                    {"type": "sales_call", "timestamp": datetime.now() - timedelta(hours=2), "outcome": "follow_up_scheduled"}
                ]
            ),
            Lead(
                lead_id="MKT_LEAD003",
                name="Jennifer Park",
                email="j.park@globalmanufacturing.com",
                phone="+1-555-0393",
                company="Global Manufacturing",
                job_title="Digital Transformation Director",
                source=LeadSource.CONTENT,
                campaign_id="CAMP002",
                score=76.0,
                created_at=datetime.now() - timedelta(days=8),
                last_interaction=datetime.now() - timedelta(days=1),
                interests=["Digital Transformation", "Process Automation", "ROI Analytics"],
                activities=[
                    {"type": "blog_read", "timestamp": datetime.now() - timedelta(days=8), "article": "AI_Manufacturing_ROI"},
                    {"type": "case_study_download", "timestamp": datetime.now() - timedelta(days=3), "content": "Manufacturing_Success_Story"},
                    {"type": "email_reply", "timestamp": datetime.now() - timedelta(days=1), "response": "interested_in_pilot"}
                ]
            )
        ]
        
        for lead in sample_leads:
            self.leads.append(lead)
        
        # Sample content
        sample_content = [
            Content(
                content_id="CONTENT001",
                title="The Future of Enterprise AI: A Complete Guide",
                type=ContentType.WHITEPAPER,
                status="published",
                author="marketing_team",
                created_at=datetime.now() - timedelta(days=45),
                published_at=datetime.now() - timedelta(days=40),
                views=2847,
                downloads=456,
                shares=89,
                conversion_rate=16.02,
                keywords=["enterprise ai", "automation", "digital transformation"],
                campaigns=["CAMP001", "CAMP002"]
            ),
            Content(
                content_id="CONTENT002",
                title="ROI Calculator: AI Platform Implementation",
                type=ContentType.CASE_STUDY,
                status="published",
                author="product_marketing",
                created_at=datetime.now() - timedelta(days=30),
                published_at=datetime.now() - timedelta(days=25),
                views=1923,
                downloads=289,
                shares=47,
                conversion_rate=15.03,
                keywords=["roi", "implementation", "business value"],
                campaigns=["CAMP001"]
            ),
            Content(
                content_id="CONTENT003",
                title="AI in Manufacturing: Success Stories and Best Practices",
                type=ContentType.VIDEO,
                status="published",
                author="industry_specialist",
                created_at=datetime.now() - timedelta(days=20),
                published_at=datetime.now() - timedelta(days=15),
                views=5432,
                downloads=0,
                shares=234,
                conversion_rate=8.76,
                keywords=["manufacturing", "case studies", "best practices"],
                campaigns=["CAMP002"]
            )
        ]
        
        for content in sample_content:
            self.content.append(content)
        
        # Update metrics
        self._update_metrics()

    async def create_campaign(self, name: str, campaign_type: CampaignType, budget: float,
                            start_date: datetime, end_date: datetime, 
                            target_audience: Dict[str, Any], channels: List[str]) -> Campaign:
        """Create a new marketing campaign"""
        try:
            campaign = Campaign(
                campaign_id=f"CAMP{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6].upper()}",
                name=name,
                type=campaign_type,
                status=CampaignStatus.DRAFT,
                budget=budget,
                start_date=start_date,
                end_date=end_date,
                target_audience=target_audience,
                channels=channels,
                created_by="marketing_agent"
            )
            
            self.campaigns.append(campaign)
            self.metrics["total_campaigns"] += 1
            
            logger.info(f"Campaign {campaign.campaign_id} created: {name}")
            return campaign
            
        except Exception as e:
            logger.error(f"Failed to create campaign: {str(e)}")
            raise

    async def generate_lead(self, name: str, email: str, company: str, 
                          source: LeadSource, campaign_id: str = None) -> Lead:
        """Generate a new marketing lead"""
        try:
            # Calculate initial lead score based on source and company info
            score = self._calculate_lead_score(source, company)
            
            lead = Lead(
                lead_id=f"MKT_LEAD{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6].upper()}",
                name=name,
                email=email,
                phone=None,
                company=company,
                job_title="Unknown",
                source=source,
                campaign_id=campaign_id,
                score=score,
                created_at=datetime.now(),
                last_interaction=datetime.now()
            )
            
            self.leads.append(lead)
            self.metrics["total_leads"] += 1
            
            if score >= 70:
                self.metrics["qualified_leads"] += 1
            
            self._update_metrics()
            
            logger.info(f"Lead {lead.lead_id} generated from {source.value} (Score: {score})")
            return lead
            
        except Exception as e:
            logger.error(f"Failed to generate lead: {str(e)}")
            raise

    def _calculate_lead_score(self, source: LeadSource, company: str) -> float:
        """Calculate lead score based on source and company information"""
        base_scores = {
            LeadSource.REFERRAL: 85.0,
            LeadSource.WEBINAR: 75.0,
            LeadSource.EMAIL_CAMPAIGN: 65.0,
            LeadSource.CONTENT: 60.0,
            LeadSource.WEBSITE: 55.0,
            LeadSource.SOCIAL_MEDIA: 45.0,
            LeadSource.PAID_ADS: 40.0
        }
        
        score = base_scores.get(source, 50.0)
        
        # Boost score for enterprise companies
        if any(keyword in company.lower() for keyword in ['corp', 'enterprise', 'global', 'international']):
            score += 15.0
        
        return min(score, 100.0)

    async def create_content(self, title: str, content_type: ContentType, 
                           author: str, keywords: List[str]) -> Content:
        """Create new marketing content"""
        try:
            content = Content(
                content_id=f"CONTENT{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6].upper()}",
                title=title,
                type=content_type,
                status="draft",
                author=author,
                created_at=datetime.now(),
                keywords=keywords
            )
            
            self.content.append(content)
            self.metrics["content_pieces"] += 1
            
            logger.info(f"Content {content.content_id} created: {title}")
            return content
            
        except Exception as e:
            logger.error(f"Failed to create content: {str(e)}")
            raise

    async def launch_campaign(self, campaign_id: str) -> bool:
        """Launch a marketing campaign"""
        try:
            campaign = next((c for c in self.campaigns if c.campaign_id == campaign_id), None)
            if not campaign:
                return False
            
            campaign.status = CampaignStatus.ACTIVE
            self.metrics["active_campaigns"] += 1
            
            logger.info(f"Campaign {campaign_id} launched: {campaign.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch campaign: {str(e)}")
            return False

    async def segment_audience(self, criteria: Dict[str, Any]) -> List[Lead]:
        """Segment leads based on specified criteria"""
        try:
            filtered_leads = []
            
            for lead in self.leads:
                matches = True
                
                # Check score range
                if 'min_score' in criteria and lead.score < criteria['min_score']:
                    matches = False
                if 'max_score' in criteria and lead.score > criteria['max_score']:
                    matches = False
                
                # Check source
                if 'source' in criteria and lead.source != criteria['source']:
                    matches = False
                
                # Check interests
                if 'interests' in criteria:
                    required_interests = criteria['interests']
                    if not any(interest in lead.interests for interest in required_interests):
                        matches = False
                
                # Check company keywords
                if 'company_keywords' in criteria:
                    keywords = criteria['company_keywords']
                    if not any(keyword.lower() in lead.company.lower() for keyword in keywords):
                        matches = False
                
                if matches:
                    filtered_leads.append(lead)
            
            logger.info(f"Audience segmentation: {len(filtered_leads)} leads match criteria")
            return filtered_leads
            
        except Exception as e:
            logger.error(f"Audience segmentation failed: {str(e)}")
            return []

    async def track_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        """Track and analyze campaign performance"""
        try:
            campaign = next((c for c in self.campaigns if c.campaign_id == campaign_id), None)
            if not campaign:
                return {}
            
            # Get campaign leads
            campaign_leads = [l for l in self.leads if l.campaign_id == campaign_id]
            qualified_leads = [l for l in campaign_leads if l.score >= 70]
            
            # Calculate metrics
            total_leads = len(campaign_leads)
            total_qualified = len(qualified_leads)
            conversion_rate = (total_qualified / total_leads * 100) if total_leads > 0 else 0
            
            cost_per_lead = campaign.budget / total_leads if total_leads > 0 else 0
            avg_lead_score = sum(l.score for l in campaign_leads) / total_leads if total_leads > 0 else 0
            
            performance = {
                "campaign_id": campaign_id,
                "campaign_name": campaign.name,
                "status": campaign.status.value,
                "budget": campaign.budget,
                "total_leads": total_leads,
                "qualified_leads": total_qualified,
                "conversion_rate": round(conversion_rate, 2),
                "cost_per_lead": round(cost_per_lead, 2),
                "avg_lead_score": round(avg_lead_score, 2),
                "roi": campaign.metrics.get("roi", 0.0)
            }
            
            return performance
            
        except Exception as e:
            logger.error(f"Performance tracking failed: {str(e)}")
            return {}

    async def analyze_content_performance(self) -> List[Dict[str, Any]]:
        """Analyze content marketing performance"""
        try:
            content_analysis = []
            
            for content in self.content:
                if content.status == "published":
                    engagement_score = (content.views * 0.1 + content.downloads * 5 + content.shares * 10)
                    
                    analysis = {
                        "content_id": content.content_id,
                        "title": content.title,
                        "type": content.type.value,
                        "views": content.views,
                        "downloads": content.downloads,
                        "shares": content.shares,
                        "conversion_rate": content.conversion_rate,
                        "engagement_score": round(engagement_score, 2),
                        "performance_rating": self._rate_content_performance(content)
                    }
                    content_analysis.append(analysis)
            
            # Sort by engagement score
            content_analysis.sort(key=lambda x: x["engagement_score"], reverse=True)
            
            return content_analysis
            
        except Exception as e:
            logger.error(f"Content analysis failed: {str(e)}")
            return []

    def _rate_content_performance(self, content: Content) -> str:
        """Rate content performance based on metrics"""
        if content.conversion_rate >= 15.0 and content.shares >= 100:
            return "Excellent"
        elif content.conversion_rate >= 10.0 and content.shares >= 50:
            return "Good"
        elif content.conversion_rate >= 5.0 and content.shares >= 20:
            return "Average"
        else:
            return "Needs Improvement"

    async def automate_lead_nurturing(self, lead_id: str) -> List[Dict[str, Any]]:
        """Automate lead nurturing based on lead behavior and score"""
        try:
            lead = next((l for l in self.leads if l.lead_id == lead_id), None)
            if not lead:
                return []
            
            nurturing_actions = []
            
            # High-score leads
            if lead.score >= 80:
                nurturing_actions.extend([
                    {"action": "schedule_sales_call", "priority": "high", "timing": "immediate"},
                    {"action": "send_personalized_demo", "priority": "high", "timing": "within_24h"},
                    {"action": "assign_account_executive", "priority": "high", "timing": "immediate"}
                ])
            
            # Medium-score leads
            elif lead.score >= 60:
                nurturing_actions.extend([
                    {"action": "send_case_study", "priority": "medium", "timing": "within_48h"},
                    {"action": "invite_to_webinar", "priority": "medium", "timing": "next_available"},
                    {"action": "follow_up_email", "priority": "medium", "timing": "weekly"}
                ])
            
            # Low-score leads
            else:
                nurturing_actions.extend([
                    {"action": "send_educational_content", "priority": "low", "timing": "weekly"},
                    {"action": "social_media_engagement", "priority": "low", "timing": "monthly"},
                    {"action": "newsletter_subscription", "priority": "low", "timing": "immediate"}
                ])
            
            # Add interest-based actions
            if "AI Platform" in lead.interests:
                nurturing_actions.append({"action": "send_ai_whitepaper", "priority": "medium", "timing": "within_48h"})
            
            if "ROI" in ' '.join(lead.interests):
                nurturing_actions.append({"action": "send_roi_calculator", "priority": "high", "timing": "within_24h"})
            
            return nurturing_actions
            
        except Exception as e:
            logger.error(f"Lead nurturing automation failed: {str(e)}")
            return []

    def _update_metrics(self):
        """Update agent performance metrics"""
        if self.leads:
            total_leads = len(self.leads)
            qualified_leads = len([l for l in self.leads if l.score >= 70])
            
            self.metrics["total_leads"] = total_leads
            self.metrics["qualified_leads"] = qualified_leads
            self.metrics["conversion_rate"] = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
            self.metrics["avg_lead_score"] = sum(l.score for l in self.leads) / total_leads if total_leads > 0 else 0
        
        self.metrics["active_campaigns"] = len([c for c in self.campaigns if c.status == CampaignStatus.ACTIVE])

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "capabilities": self.capabilities,
            "campaigns": len(self.campaigns),
            "leads": len(self.leads),
            "content_pieces": len(self.content),
            "metrics": self.metrics,
            "last_updated": datetime.now().isoformat()
        }

# Demo function
async def demo_marketing_agent():
    """Demonstrate Marketing Agent capabilities"""
    
    print("🚀 Starting Marketing Agent Demo...")
    
    # Initialize agent
    marketing_agent = MarketingAgent()
    
    print("\n📢 Marketing Agent Demo:")
    print("=" * 50)
    
    # 1. Create campaign
    print("🎯 Campaign Creation:")
    campaign = await marketing_agent.create_campaign(
        name="Q4 Enterprise Outreach",
        campaign_type=CampaignType.EMAIL,
        budget=75000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=90),
        target_audience={"industries": ["Technology", "Finance"], "company_size": ["Enterprise"]},
        channels=["email", "linkedin", "website"]
    )
    print(f"  Campaign ID: {campaign.campaign_id}")
    print(f"  Type: {campaign.type.value}")
    print(f"  Budget: ${campaign.budget:,.2f}")
    
    # 2. Generate lead
    print("\n🎯 Lead Generation:")
    lead = await marketing_agent.generate_lead(
        name="Alex Thompson",
        email="a.thompson@techfirm.com",
        company="TechFirm Enterprise",
        source=LeadSource.EMAIL_CAMPAIGN,
        campaign_id=campaign.campaign_id
    )
    print(f"  Lead ID: {lead.lead_id}")
    print(f"  Lead Score: {lead.score}")
    print(f"  Source: {lead.source.value}")
    
    # 3. Content performance
    print("\n📊 Content Performance:")
    content_analysis = await marketing_agent.analyze_content_performance()
    for content in content_analysis[:2]:  # Show top 2
        print(f"  {content['title']}: {content['performance_rating']} (Conversion: {content['conversion_rate']}%)")
    
    # 4. Campaign performance
    print("\n📈 Campaign Performance:")
    performance = await marketing_agent.track_campaign_performance("CAMP001")
    print(f"  {performance['campaign_name']}: {performance['qualified_leads']} qualified leads")
    print(f"  Conversion Rate: {performance['conversion_rate']}%")
    print(f"  Cost per Lead: ${performance['cost_per_lead']:.2f}")
    
    # 5. Agent status
    status = await marketing_agent.get_agent_status()
    print(f"\n🤖 Agent Status: {status['status']} | Campaigns: {status['campaigns']} | Leads: {status['leads']}")

if __name__ == "__main__":
    asyncio.run(demo_marketing_agent())
