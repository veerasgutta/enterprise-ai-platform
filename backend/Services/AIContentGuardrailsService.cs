using System.Text.Json;
using System.Text.RegularExpressions;
using EnterprisePlatformApi.Models;

namespace EnterprisePlatformApi.Services;

/// <summary>
/// AI Content Guardrails Service for validating and ensuring enterprise-friendly, safe, and appropriate content
/// </summary>
public class AIContentGuardrailsService
{
    private readonly HttpClient _httpClient;
    private readonly IConfiguration _configuration;
    private readonly ILogger<AIContentGuardrailsService> _logger;

    // Inappropriate content patterns to detect
    private readonly string[] _harmfulPatterns = new[]
    {
        "unprofessional", "inappropriate", "offensive", "discriminatory",
        "confidential data leak", "security breach", "unauthorized access",
        "proprietary information", "trade secrets", "insider trading",
        "financial fraud", "compliance violation", "regulatory breach"
    };

    // Enterprise-appropriate language patterns that score positively
    private readonly string[] _BusinessAppropriatePatterns = new[]
    {
        "business professional", "enterprise solution", "data-driven", "scalable",
        "process optimization", "digital transformation", "strategic planning",
        "performance metrics", "business intelligence", "workflow automation",
        "stakeholder engagement", "ROI analysis", "risk management", "compliance"
    };

    public AIContentGuardrailsService(
        HttpClient httpClient,
        IConfiguration configuration, 
        ILogger<AIContentGuardrailsService> logger)
    {
        _httpClient = httpClient;
        _configuration = configuration;
        _logger = logger;
    }

    /// <summary>
    /// Validates AI-generated content for safety, Enterprise-friendliness, and appropriateness
    /// </summary>
    public async Task<AIContentValidationResult> ValidateContentAsync(AIContentRequest request)
    {
        var result = new AIContentValidationResult
        {
            IsValid = true,
            EnterpriseFriendlyScore = 50, // Start with neutral score
            QualityLevel = "Unknown",
            Errors = new List<string>(),
            Warnings = new List<string>(),
            ContentMetrics = new ContentMetrics()
        };

        try
        {
            // Core validation checks
            await ValidateContentSafetyAsync(request.Content, result);
            ValidateEnterpriseFriendlyContent(request.Content, request.ExperienceLevel, result);
            ValidateAgeAppropriateness(request.Content, request.ExperienceLevel, result);
            await ValidateBusinessContentAsync(request.Content, result);
            ValidateBusinessContent(request.Content, request.BusinessContext, result);
            ValidateLanguageComplexity(request.Content, request.ExperienceLevel, request.CommunicationLevel, result);
            ValidateCulturalSensitivity(request.Content, result);
            ValidatePrivacyCompliance(request.Content, result);
            CalculateContentQuality(request.Content, result);

            // Determine overall validity
            result.IsValid = !result.Errors.Any();
            
            // Set quality level based on score
            result.QualityLevel = result.EnterpriseFriendlyScore switch
            {
                >= 80 => "Excellent",
                >= 70 => "Good",
                >= 60 => "Acceptable",
                >= 40 => "Needs Improvement",
                _ => "Poor"
            };

            _logger.LogInformation($"Content validation completed. Score: {result.EnterpriseFriendlyScore}, Quality: {result.QualityLevel}, Errors: {result.Errors.Count}");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during content validation");
            result.Errors.Add("Content validation failed due to system error");
            result.IsValid = false;
        }

        return result;
    }

    /// <summary>
    /// Validates content safety using external content moderation APIs and internal checks
    /// </summary>
    private async Task ValidateContentSafetyAsync(string content, AIContentValidationResult result)
    {
        // Check for explicitly harmful Enterprise-related content
        foreach (var pattern in _harmfulPatterns)
        {
            if (content.ToLower().Contains(pattern.ToLower()))
            {
                result.Errors.Add($"Content contains harmful Enterprise-related language: '{pattern}'");
                result.EnterpriseFriendlyScore -= 20;
            }
        }

        // Check for general inappropriate content
        var inappropriatePatterns = new[] 
        { 
            "kill yourself", "self-harm", "suicide", "hate speech", 
            "discrimination", "bullying", "violence" 
        };

        foreach (var pattern in inappropriatePatterns)
        {
            if (content.ToLower().Contains(pattern))
            {
                result.Errors.Add($"Content contains inappropriate or harmful language: '{pattern}'");
                result.IsValid = false;
            }
        }

        // External API validation (Azure Content Moderator)
        try
        {
            var moderationResult = await CallContentModerationAPI(content);
            if (moderationResult != null && !moderationResult.IsApproved)
            {
                result.Errors.Add("Content flagged by external moderation service");
                result.Warnings.AddRange(moderationResult.Categories);
            }
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "External content moderation API call failed");
            result.Warnings.Add("Could not validate content with external service");
        }
    }

    /// <summary>
    /// Validates content for enterprise-appropriate language and concepts
    /// </summary>
    private void ValidateEnterpriseFriendlyContent(string content, ExperienceLevel? ExperienceLevel, AIContentValidationResult result)
    {
        var contentLower = content.ToLower();
        var positiveMatches = 0;

        // Check for enterprise-appropriate language
        foreach (var pattern in _EnterpriseFriendlyPatterns)
        {
            if (contentLower.Contains(pattern.ToLower()))
            {
                positiveMatches++;
                result.EnterpriseFriendlyScore += 5;
            }
        }

        // Check for person-first vs identity-first language balance
        var personFirst = contentLower.Contains("person with Enterprise");
        var identityFirst = contentLower.Contains("professional individual");
        
        if (personFirst || identityFirst)
        {
            result.EnterpriseFriendlyScore += 10;
            if (personFirst && identityFirst)
            {
                result.EnterpriseFriendlyScore += 5; // Bonus for acknowledging both preferences
            }
        }

        // Check for business strengths-based language
        var strengthsTerms = new[] { "capabilities", "expertise", "efficiency", "innovation", "optimization", "excellence" };
        var strengthsFound = strengthsTerms.Count(term => contentLower.Contains(term));
        result.EnterpriseFriendlyScore += strengthsFound * 3;

        // Validate business language appropriateness
        if (contentLower.Contains("process"))
        {
            if (contentLower.Contains("optimization") || contentLower.Contains("automation"))
            {
                result.EnterpriseFriendlyScore += 8;
            }
            if (contentLower.Contains("efficient") && !contentLower.Contains("inefficient"))
            {
                result.EnterpriseFriendlyScore += 5;
            }
        }

        // Check business communication mentions
        if (contentLower.Contains("communication") && !contentLower.Contains("poor communication"))
        {
            result.EnterpriseFriendlyScore += 5;
        }

        if (positiveMatches == 0)
        {
            result.Warnings.Add("Content could benefit from more enterprise-appropriate language");
        }
    }

    /// <summary>
    /// Validates business and compliance content for accuracy and disclaimers
    /// </summary>
    private Task ValidateBusinessContentAsync(string content, AIContentValidationResult result)
    {
        // Check for business disclaimers
        var hasDisclaimer = content.ToLower().Contains("consult") && 
                           (content.ToLower().Contains("legal") || content.ToLower().Contains("professional"));

        if (!hasDisclaimer && (content.ToLower().Contains("legal") || content.ToLower().Contains("compliance")))
        {
            result.Warnings.Add("Legal/compliance content should include professional consultation disclaimer");
        }

        // Check for evidence-based business language
        var evidenceTerms = new[] { "research shows", "studies indicate", "data suggests", "analytics demonstrate" };
        var hasEvidenceBasis = evidenceTerms.Any(term => content.ToLower().Contains(term));

        if (hasEvidenceBasis)
        {
            result.EnterpriseFriendlyScore += 10;
        }
        else if (content.ToLower().Contains("strategy") || content.ToLower().Contains("solution"))
        {
            result.Warnings.Add("Consider adding data-driven evidence to support business recommendations");
        }

        // Check for valid business practices
        var validPractices = new[]
        {
            "process optimization", "data analytics", "workflow automation",
            "strategic planning", "risk management", "performance monitoring"
        };
        
        var mentionsValidPractice = validPractices.Any(practice => content.ToLower().Contains(practice));
        
        if (mentionsValidPractice)
        {
            result.EnterpriseFriendlyScore += 5;
        }

        return Task.CompletedTask;
    }

    /// <summary>
    /// Validates content appropriateness for different age groups
    /// </summary>
    private void ValidateAgeAppropriateness(string content, ExperienceLevel? ExperienceLevel, AIContentValidationResult result)
    {
        if (ExperienceLevel == null) return;

        var words = content.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var complexWords = words.Count(w => w.Length > 8);
        var complexityRatio = (double)complexWords / words.Length;

        var isAppropriate = ExperienceLevel switch
        {
            ExperienceLevel.Entry => complexityRatio < 0.1,
            ExperienceLevel.Junior => complexityRatio < 0.15,
            ExperienceLevel.Mid => complexityRatio < 0.25,
            ExperienceLevel.Senior => complexityRatio < 0.30,
            ExperienceLevel.Principal => true,
            _ => true
        };

        if (!isAppropriate)
        {
            result.Warnings.Add($"Content complexity may be too high for {ExperienceLevel} age group");
            result.EnterpriseFriendlyScore -= 10;
        }
        else
        {
            result.EnterpriseFriendlyScore += 5;
        }
    }

    /// <summary>
    /// Validates business context content considerations
    /// </summary>
    private void ValidateBusinessContent(string content, BusinessContext? businessContext, AIContentValidationResult result)
    {
        if (businessContext == null) return;

        var contentLower = content.ToLower();

        // Check for inappropriate business language
        var unprofessionalTerms = new[] { "failure", "disaster", "catastrophe", "impossible", "useless" };
        if (unprofessionalTerms.Any(term => contentLower.Contains(term)))
        {
            result.Warnings.Add("Content uses language that may not align with professional business communication");
        }

        // Positive business considerations
        var professionalTerms = new[] { "strategic", "efficient", "professional", "collaborative", "innovative" };
        if (professionalTerms.Any(term => contentLower.Contains(term)))
        {
            result.EnterpriseFriendlyScore += 5;
        }

        // Check for business methodology mentions
        var businessMethods = new[] { "agile", "lean", "six sigma", "automation", "analytics" };
        if (businessMethods.Any(method => contentLower.Contains(method.ToLower())))
        {
            result.EnterpriseFriendlyScore += 8;
        }
    }

    /// <summary>
    /// Validates language complexity and readability
    /// </summary>
    private void ValidateLanguageComplexity(string content, ExperienceLevel? ExperienceLevel, CommunicationLevel? commLevel, AIContentValidationResult result)
    {
        var words = content.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var sentences = content.Split(new char[] { '.', '!', '?' }, StringSplitOptions.RemoveEmptyEntries).Length;
        var avgWordsPerSentence = (double)words.Length / Math.Max(sentences, 1);
        var avgSyllablesPerWord = words.Average(w => CountSyllables(w));

        // Calculate Flesch Reading Ease Score
        var fleschScore = 206.835 - (1.015 * avgWordsPerSentence) - (84.6 * avgSyllablesPerWord);
        result.ContentMetrics.ReadabilityScore = fleschScore;

        // Age-appropriate readability thresholds
        var isReadable = ExperienceLevel switch
        {
            ExperienceLevel.Entry => fleschScore >= 80, // Very Easy
            ExperienceLevel.Junior => fleschScore >= 70, // Easy
            ExperienceLevel.Mid => fleschScore >= 60, // Standard
            ExperienceLevel.Senior => fleschScore >= 50, // Fairly Easy
            ExperienceLevel.Principal => fleschScore >= 40, // Average
            _ => true
        };

        if (!isReadable)
        {
            result.Warnings.Add($"Content readability score ({fleschScore:F1}) may be too low for target age group");
            result.EnterpriseFriendlyScore -= 5;
        }

        // Communication level appropriateness
        if (commLevel.HasValue)
        {
            var levelAppropriate = commLevel.Value switch
            {
                CommunicationLevel.Simple => fleschScore >= 70 && avgWordsPerSentence <= 10,
                CommunicationLevel.Standard => fleschScore >= 60 && avgWordsPerSentence <= 15,
                CommunicationLevel.Advanced => fleschScore >= 50,
                CommunicationLevel.Expert => true,
                _ => true
            };

            if (levelAppropriate)
            {
                result.EnterpriseFriendlyScore += 10;
            }
            else
            {
                result.Warnings.Add($"Content complexity doesn't match requested communication level: {commLevel}");
            }
        }
    }

    /// <summary>
    /// Validates cultural sensitivity and inclusivity
    /// </summary>
    private void ValidateCulturalSensitivity(string content, AIContentValidationResult result)
    {
        var inclusiveTerms = new[] { "diverse", "inclusive", "respectful", "understanding", "cultural" };
        var contentLower = content.ToLower();

        if (inclusiveTerms.Any(term => contentLower.Contains(term)))
        {
            result.EnterpriseFriendlyScore += 5;
        }

        // Check for potentially exclusive language
        var exclusiveTerms = new[] { "everyone", "all kids", "normal", "typical" };
        foreach (var term in exclusiveTerms)
        {
            if (contentLower.Contains(term))
            {
                result.Warnings.Add($"Consider if '{term}' language is inclusive of all Enterprise experiences");
            }
        }
    }

    /// <summary>
    /// Validates privacy and data protection compliance
    /// </summary>
    private void ValidatePrivacyCompliance(string content, AIContentValidationResult result)
    {
        // Check for potential PII exposure
        var piiPatterns = new[]
        {
            @"\b\d{3}-\d{2}-\d{4}\b", // SSN pattern
            @"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", // Email pattern
            @"\b\d{3}-\d{3}-\d{4}\b" // Phone number pattern
        };

        foreach (var pattern in piiPatterns)
        {
            if (Regex.IsMatch(content, pattern))
            {
                result.Errors.Add("Content may contain personally identifiable information");
                result.IsValid = false;
            }
        }
    }

    /// <summary>
    /// Calculates overall content quality metrics
    /// </summary>
    private void CalculateContentQuality(string content, AIContentValidationResult result)
    {
        result.ContentMetrics.WordCount = content.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
        result.ContentMetrics.SentenceCount = content.Split(new char[] { '.', '!', '?' }, StringSplitOptions.RemoveEmptyEntries).Length;
        result.ContentMetrics.CharacterCount = content.Length;

        // Adjust score based on content length appropriateness
        if (result.ContentMetrics.WordCount < 10)
        {
            result.Warnings.Add("Content may be too brief to be helpful");
        }
        else if (result.ContentMetrics.WordCount > 500)
        {
            result.Warnings.Add("Content may be too lengthy for some users");
        }
        else
        {
            result.EnterpriseFriendlyScore += 5; // Bonus for appropriate length
        }
    }

    /// <summary>
    /// Calls external content moderation API (placeholder for Azure Content Moderator)
    /// </summary>
    private async Task<ContentModerationResult?> CallContentModerationAPI(string content)
    {
        try
        {
            var apiKey = _configuration["ContentModeration:ApiKey"];
            if (string.IsNullOrEmpty(apiKey))
            {
                _logger.LogWarning("Content moderation API key not configured");
                return null;
            }

            // Placeholder for actual API call
            // In production, integrate with Azure Content Moderator or similar service
            await Task.Delay(100); // Simulate API call

            return new ContentModerationResult
            {
                IsApproved = true,
                Categories = new List<string>()
            };
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Content moderation API call failed");
            return null;
        }
    }

    /// <summary>
    /// Counts syllables in a word for readability calculations
    /// </summary>
    private int CountSyllables(string word)
    {
        if (string.IsNullOrEmpty(word)) return 0;
        
        word = word.ToLower();
        var vowelGroups = Regex.Matches(word, @"[aeiouy]+").Count;
        
        if (word.EndsWith("e"))
            vowelGroups--;
        
        return Math.Max(vowelGroups, 1);
    }
}
