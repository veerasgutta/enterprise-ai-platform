using System.ComponentModel.DataAnnotations;

namespace EnterprisePlatformApi.Models
{
    /// <summary>
    /// AI content validation result for enterprise content
    /// </summary>
    public class AIContentValidationResult
    {
        public bool IsValid { get; set; } = true;
        
        public List<string> Errors { get; set; } = new();
        
        public List<string> Warnings { get; set; } = new();
        
        public List<string> Suggestions { get; set; } = new();
        
        public ContentValidationScore ValidationScore { get; set; } = new();
        
        public DateTime ValidationTimestamp { get; set; } = DateTime.UtcNow;
        
        public string? ValidatedContent { get; set; }
        
        public string? ValidationRules { get; set; }
        
        public ExperienceLevel? TargetExperienceLevel { get; set; }
        
        public BusinessContext? BusinessContext { get; set; }
        
        public Dictionary<string, object> Metadata { get; set; } = new();
    }

    /// <summary>
    /// Content validation scoring metrics
    /// </summary>
    public class ContentValidationScore
    {
        public double OverallScore { get; set; } = 0.0;
        
        public double ProfessionalismScore { get; set; } = 0.0;
        
        public double ClarityScore { get; set; } = 0.0;
        
        public double AccuracyScore { get; set; } = 0.0;
        
        public double ComplianceScore { get; set; } = 0.0;
        
        public double ReadabilityScore { get; set; } = 0.0;
        
        public double RelevanceScore { get; set; } = 0.0;
        
        public double EngagementScore { get; set; } = 0.0;
    }

    /// <summary>
    /// Content moderation result for enterprise safety
    /// </summary>
    public class ContentModerationResult
    {
        public bool IsAppropriate { get; set; } = true;
        
        public List<string> FlaggedContent { get; set; } = new();
        
        public List<string> Reasons { get; set; } = new();
        
        public ModerationSeverity Severity { get; set; } = ModerationSeverity.None;
        
        public List<string> RecommendedActions { get; set; } = new();
        
        public double ConfidenceScore { get; set; } = 0.0;
        
        public DateTime ModerationTimestamp { get; set; } = DateTime.UtcNow;
        
        public string? ModeratorNotes { get; set; }
        
        public Dictionary<string, double> CategoryScores { get; set; } = new();
    }

    /// <summary>
    /// Suggested resource for business users
    /// </summary>
    public class SuggestedResource
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        
        [Required]
        public string Title { get; set; } = string.Empty;
        
        public string? Description { get; set; }
        
        [Required]
        public string Url { get; set; } = string.Empty;
        
        public string? ThumbnailUrl { get; set; }
        
        public ResourceType Type { get; set; } = ResourceType.Article;
        
        public ExperienceLevel ExperienceLevel { get; set; } = ExperienceLevel.Entry;
        
        public string? Category { get; set; }
        
        public int EstimatedReadingTimeMinutes { get; set; } = 0;
        
        public double RelevanceScore { get; set; } = 0.0;
        
        public string? Author { get; set; }
        
        public DateTime? PublishedDate { get; set; }
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        
        public bool IsActive { get; set; } = true;
        
        public string? Tags { get; set; }
        
        public Dictionary<string, object> Metadata { get; set; } = new();
    }

    public enum ModerationSeverity
    {
        None,
        Low,
        Medium,
        High,
        Critical
    }

    public enum ResourceType
    {
        Article,
        Video,
        Document,
        Tool,
        Template,
        Guide,
        Tutorial,
        Course,
        Webinar,
        Podcast,
        Report,
        Analysis,
        Strategy,
        Policy,
        Procedure,
        Best_Practice
    }
}
