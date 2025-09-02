using Microsoft.AspNetCore.Mvc;
using EnterprisePlatformApi.Models;
using EnterprisePlatformApi.Data;
using EnterprisePlatformApi.Services;
using Microsoft.EntityFrameworkCore;
using OpenAI;
using OpenAI.Chat;
using Microsoft.Extensions.Caching.Memory;
using System.Text;
using System.Text.Json;

namespace EnterprisePlatformApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class EnterpriseAIChatController : ControllerBase
{
    private readonly EnterprisePlatformDbContext _context;
    private readonly OpenAIClient _openAIClient;
    private readonly AIContentGuardrailsService _guardrailsService;
    private readonly ILogger<EnterpriseAIChatController> _logger;
    private readonly IMemoryCache _memoryCache;
    private readonly IHttpClientFactory _httpClientFactory;

    public EnterpriseAIChatController(
        EnterprisePlatformDbContext context, 
        OpenAIClient openAIClient,
        AIContentGuardrailsService guardrailsService,
        ILogger<EnterpriseAIChatController> logger,
        IMemoryCache memoryCache,
        IHttpClientFactory httpClientFactory)
    {
        _context = context;
        _openAIClient = openAIClient;
        _guardrailsService = guardrailsService;
        _logger = logger;
        _memoryCache = memoryCache;
        _httpClientFactory = httpClientFactory;
    }

    [HttpPost("chat")]
    public async Task<IActionResult> Chat([FromBody] EnterpriseChatRequest request)
    {
        try
        {
            // First, validate the incoming user message
            var userMessageValidation = await _guardrailsService.ValidateContentAsync(new AIContentRequest
            {
                Content = request.Message,
                ContentType = AIContentType.General,
                ExperienceLevel = request.ExperienceLevel,
                UserId = request.UserId?.ToString()
            });

            if (!userMessageValidation.IsValid)
            {
                return BadRequest(new
                {
                    message = "Your message contains content that cannot be processed",
                    errors = userMessageValidation.Errors,
                    suggestions = new[]
                    {
                        "Please rephrase your question using respectful language",
                        "Focus on asking about enterprise consulting, learning, or general topics",
                        "Avoid legal advice requests - consult with legal professionals instead"
                    }
                });
            }

            // Load short-term memory
            var history = GetConversationHistory(request);

            // Get user context if userId is provided
            UserProfile? userProfile = null;
            if (request.UserId.HasValue)
            {
                userProfile = await _context.UserProfiles
                    .Include(p => p.User)
                    .FirstOrDefaultAsync(p => p.UserId == request.UserId);
            }

            var systemPrompt = CreateSystemPrompt(request.ExperienceLevel, userProfile);

            // Agent mode instructions
            if (!string.IsNullOrWhiteSpace(request.Agent))
            {
                systemPrompt += request.Agent switch
                {
                    "forecast" => "\n\nAgent Mode: Forecast\n- Focus on weather-related answers.\n- Use the provided WeatherForecast tool results when available.\n- Be concise and provide actionable advice.",
                    "recommendation" => "\n\nAgent Mode: Recommendation\n- Provide practical, step-by-step recommendations tailored to the user's context.",
                    "resources" => "\n\nAgent Mode: Resources\n- Prioritize suggesting high-quality, age-appropriate resources with short descriptions and next steps.",
                    _ => "\n\nAgent Mode: General\n- Provide supportive, concise, and practical responses."
                };
            }

            // Lightweight function-calling: enrich with tool results when relevant or forced by agent
            var toolContext = await BuildToolContextAsync(request.Message, request.Agent);
            if (!string.IsNullOrWhiteSpace(toolContext))
            {
                systemPrompt += $"\n\nTool Results (for AI use):\n{toolContext}";
            }

            var messages = new List<ChatMessage>
            {
                new SystemChatMessage(systemPrompt)
            };

            // Add conversation history (server memory first)
            if (history is { Count: > 0 })
            {
                foreach (var msg in history)
                {
                    if (msg.Role == "user") messages.Add(new UserChatMessage(msg.Content));
                    else if (msg.Role == "assistant") messages.Add(new AssistantChatMessage(msg.Content));
                }
            }

            // Add latest user message
            messages.Add(new UserChatMessage(request.Message));

            var chatCompletion = await _openAIClient.GetChatClient("gpt-4").CompleteChatAsync(messages);
            var aiResponseText = chatCompletion.Value.Content[0].Text;

            // Validate AI-generated response with guardrails
            var responseValidation = await _guardrailsService.ValidateContentAsync(new AIContentRequest
            {
                Content = aiResponseText,
                ContentType = AIContentType.General,
                ExperienceLevel = request.ExperienceLevel,
                CommunicationLevel = DetermineCommunicationLevel(userProfile),
                BusinessContext = userProfile?.BusinessContext,
                UserId = request.UserId?.ToString()
            });

            // Handle invalid AI responses
            if (!responseValidation.IsValid)
            {
                _logger.LogWarning($"AI response failed validation. Errors: {string.Join(", ", responseValidation.Errors)}");
                aiResponseText = GenerateSafeFallbackResponse(request.Message, request.ExperienceLevel);
            }

            // Log content quality metrics for monitoring
            _logger.LogInformation($"AI response validation - Score: {responseValidation.EnterpriseComplianceScore}, Quality: {responseValidation.QualityLevel}, Warnings: {responseValidation.Warnings.Count}");

            // Persist to short-term memory (last 20 turns)
            AppendToConversationHistory(request, request.Message, aiResponseText);

            var response = new EnterpriseChatResponse
            {
                Message = aiResponseText,
                Role = "assistant",
                Timestamp = DateTime.UtcNow,
                SuggestedResources = await GetSuggestedResources(request.Message, request.ExperienceLevel),
                SuggestedActions = GetSuggestedActions(request.Message, request.ExperienceLevel),
                ContentQuality = new ContentQualityInfo
                {
                    EnterpriseComplianceScore = responseValidation.EnterpriseComplianceScore,
                    QualityLevel = responseValidation.QualityLevel,
                    HasWarnings = responseValidation.Warnings.Any(),
                    ReadabilityScore = responseValidation.ContentMetrics.ReadabilityScore
                }
            };

            return Ok(response);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing enterprise chat request");
            return StatusCode(500, new EnterpriseChatResponse
            {
                Message = "I'm having trouble processing your request right now. Please try again later, or contact our support team if you need immediate assistance.",
                Role = "assistant",
                Timestamp = DateTime.UtcNow
            });
        }
    }

    [HttpPost("chat-stream")]
    public async Task ChatStream([FromBody] EnterpriseChatRequest request)
    {
        Response.Headers["Content-Type"] = "text/event-stream";
        Response.Headers["Cache-Control"] = "no-cache";
        Response.Headers["X-Accel-Buffering"] = "no";

        try
        {
            // Reuse Chat logic pieces but do a single completion then stream chunks to client
            var history = GetConversationHistory(request);
            UserProfile? userProfile = null;
            if (request.UserId.HasValue)
            {
                userProfile = await _context.UserProfiles
                    .Include(p => p.User)
                    .FirstOrDefaultAsync(p => p.UserId == request.UserId);
            }

            var systemPrompt = CreateSystemPrompt(request.ExperienceLevel, userProfile);

            if (!string.IsNullOrWhiteSpace(request.Agent))
            {
                systemPrompt += request.Agent switch
                {
                    "forecast" => "\n\nAgent Mode: Forecast\n- Focus on weather-related answers.\n- Use the provided WeatherForecast tool results when available.\n- Be concise and provide actionable advice.",
                    "recommendation" => "\n\nAgent Mode: Recommendation\n- Provide practical, step-by-step recommendations tailored to the user's context.",
                    "resources" => "\n\nAgent Mode: Resources\n- Prioritize suggesting high-quality, age-appropriate resources with short descriptions and next steps.",
                    _ => "\n\nAgent Mode: General\n- Provide supportive, concise, and practical responses."
                };
            }

            var toolContext = await BuildToolContextAsync(request.Message, request.Agent);
            if (!string.IsNullOrWhiteSpace(toolContext))
            {
                systemPrompt += $"\n\nTool Results (for AI use):\n{toolContext}";
            }

            var messages = new List<ChatMessage> { new SystemChatMessage(systemPrompt) };
            if (history is { Count: > 0 })
            {
                foreach (var msg in history)
                {
                    if (msg.Role == "user") messages.Add(new UserChatMessage(msg.Content));
                    else if (msg.Role == "assistant") messages.Add(new AssistantChatMessage(msg.Content));
                }
            }
            messages.Add(new UserChatMessage(request.Message));

            var chatCompletion = await _openAIClient.GetChatClient("gpt-4").CompleteChatAsync(messages);
            var aiResponseText = chatCompletion.Value.Content[0].Text;

            // Stream the response in sentence chunks
            var sentences = SplitIntoChunks(aiResponseText, 60);
            foreach (var chunk in sentences)
            {
                await WriteSseAsync("message", JsonSerializer.Serialize(new { delta = chunk }));
            }

            // Build suggestions and send as final event
            var suggestedResources = await GetSuggestedResources(request.Message, request.ExperienceLevel);
            var suggestedActions = GetSuggestedActions(request.Message, request.ExperienceLevel);
            await WriteSseAsync("suggestions", JsonSerializer.Serialize(new { suggestedResources, suggestedActions }));

            // Save to memory
            AppendToConversationHistory(request, request.Message, aiResponseText);

            await WriteSseAsync("done", "{}");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in chat-stream");
            await WriteSseAsync("error", JsonSerializer.Serialize(new { message = "Streaming error" }));
        }
    }

    private async Task<string> BuildToolContextAsync(string userMessage, string? agent = null)
    {
        var lower = userMessage.ToLowerInvariant();
        var needsWeather = (agent == "forecast") || lower.Contains("weather") || lower.Contains("forecast") || lower.Contains("temperature");
        if (needsWeather)
        {
            try
            {
                var client = _httpClientFactory.CreateClient();
                var url = $"{Request.Scheme}://{Request.Host}/weatherforecast";
                var result = await client.GetStringAsync(url);
                return $"WeatherForecast: {result}";
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Failed to call weather tool");
            }
        }
        return string.Empty;
    }

    private List<string> SplitIntoChunks(string text, int maxLen)
    {
        var chunks = new List<string>();
        if (string.IsNullOrEmpty(text)) return chunks;
        var words = text.Split(' ');
        var sb = new StringBuilder();
        foreach (var w in words)
        {
            if (sb.Length + w.Length + 1 > maxLen)
            {
                chunks.Add(sb.ToString());
                sb.Clear();
            }
            if (sb.Length > 0) sb.Append(' ');
            sb.Append(w);
        }
        if (sb.Length > 0) chunks.Add(sb.ToString());
        return chunks;
    }

    private async Task WriteSseAsync(string eventName, string data)
    {
        await Response.WriteAsync($"event: {eventName}\n");
        await Response.WriteAsync($"data: {data}\n\n");
        await Response.Body.FlushAsync();
    }

    private List<ChatMessageHistory> GetConversationHistory(EnterpriseChatRequest request)
    {
        var key = GetMemoryKey(request);
        if (_memoryCache.TryGetValue(key, out List<ChatMessageHistory>? history) && history != null)
        {
            return history;
        }
        return new List<ChatMessageHistory>();
    }

    private void AppendToConversationHistory(EnterpriseChatRequest request, string userContent, string assistantContent)
    {
        var key = GetMemoryKey(request);
        var history = GetConversationHistory(request);
        history.Add(new ChatMessageHistory { Role = "user", Content = userContent });
        history.Add(new ChatMessageHistory { Role = "assistant", Content = assistantContent });
        // Keep last 20 turns (40 messages)
        if (history.Count > 40)
        {
            history = history.Skip(history.Count - 40).ToList();
        }
        _memoryCache.Set(key, history, TimeSpan.FromHours(6));
    }

    private string GetMemoryKey(EnterpriseChatRequest request)
    {
        if (!string.IsNullOrEmpty(request.SessionId))
        {
            return $"chat:{request.SessionId}";
        }
        if (request.UserId.HasValue)
        {
            return $"chat:user:{request.UserId}";
        }
        return $"chat:anonymous";
    }

    private string CreateSystemPrompt(ExperienceLevel? experienceLevel, UserProfile? userProfile)
    {
        var basePrompt = @"
You are an expert enterprise AI assistant specializing in business intelligence, process automation, and strategic consulting. You provide data-driven insights and practical solutions for modern enterprise challenges.

Core Principles:
- Provide actionable business intelligence and strategic recommendations
- Focus on enterprise-grade solutions and scalable processes
- Emphasize efficiency, automation, and digital transformation
- Use data-driven insights to support decision making
- Maintain professional communication standards
- Respect business confidentiality and professional boundaries

Expertise Areas:
- Multi-agent system orchestration and workflow automation
- Business process optimization and digital transformation
- Data analytics, reporting, and predictive insights
- Enterprise architecture and technology integration
- Project management and resource optimization
- Risk assessment and compliance monitoring

Communication Style:
- Be professional, clear, and results-oriented
- Use structured analysis with metrics and KPIs
- Provide actionable recommendations with implementation steps
- Support decisions with data and best practices
- Focus on business value and ROI considerations";

        if (experienceLevel.HasValue)
        {
            basePrompt += $@"

Target Experience Level: {GetExperienceLevelDisplayName(experienceLevel.Value)} 
Focus Areas: {GetExperienceLevelFocusAreas(experienceLevel.Value)}";
        }

        if (userProfile != null)
        {
            basePrompt += $@"

Business Context:
- Role: {userProfile.User.Role ?? "Business Professional"}
- Department: {userProfile.User.Department ?? "General"}
- Experience Level: {userProfile.User.ExperienceLevel ?? "Intermediate"}
- Focus Areas: Business intelligence, process automation, strategic planning";

            if (userProfile.CommunicationPreferences != null)
            {
                basePrompt += $@"
- Communication Preferences: 
  - Prefers concise format: {userProfile.CommunicationPreferences.RequiresSimpleLanguage}
  - Prefers structured data: {userProfile.CommunicationPreferences.PrefersBulletPoints}
  - Detail level: {userProfile.CommunicationPreferences.PreferredReadingLevel}";
            }

            if (userProfile.BusinessContext != null)
            {
                basePrompt += $@"
- Business Context:
  - Department: {userProfile.BusinessContext.Department}
  - Industry Focus: {userProfile.BusinessContext.Industry}
  - Preferred Methods: {string.Join(", ", userProfile.BusinessContext.PreferredMethodologies)}";
            }
        }

        basePrompt += @"

Available Resources:
- You can suggest relevant content from our enterprise resource library
- You can recommend local service providers and support groups
- You can provide information about educational accommodations and workplace supports
- You can offer practical strategies for daily living, Team Collaboration, and self-advocacy

Remember: You're here to support, inform, and empower. Every person's business experience is unique.";

        return basePrompt;
    }

    private async Task<List<SuggestedResource>> GetSuggestedResources(string message, ExperienceLevel? ExperienceLevel)
    {
        try
        {
            var query = _context.ContentItems
                .Include(c => c.Category)
                .Where(c => c.Status == ContentStatus.Published);

            if (ExperienceLevel.HasValue)
            {
                query = query.Where(c => c.Category.ExperienceLevel == ExperienceLevel);
            }

            // Simple keyword matching for now - could be enhanced with vector search
            var keywords = ExtractKeywords(message);
            var resources = await query
                .Where(c => keywords.Any(k => 
                    c.Title.Contains(k) || 
                    c.Content.Contains(k) || 
                    c.Keywords.Contains(k)))
                .OrderByDescending(c => c.PublishedAt)
                .Take(3)
                .Select(c => new SuggestedResource
                {
                    Id = c.Id,
                    Title = c.Title,
                    Type = c.ContentType.ToString(),
                    Url = $"/resources/{c.Slug}",
                    Description = c.Summary ?? ""
                })
                .ToListAsync();

            return resources;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting suggested resources");
            return new List<SuggestedResource>();
        }
    }

    private List<string> GetSuggestedActions(string message, ExperienceLevel? ExperienceLevel)
    {
        var actions = new List<string>();

        // Basic keyword-based action suggestions
        if (message.ToLower().Contains("school") || message.ToLower().Contains("education"))
        {
            actions.Add("Explore educational resources");
            actions.Add("Learn about IEP and 504 plans");
        }

        if (message.ToLower().Contains("work") || message.ToLower().Contains("job"))
        {
            actions.Add("Browse business resources");
            actions.Add("Find enterprise tools and guides");
        }

        if (message.ToLower().Contains("process") || message.ToLower().Contains("workflow"))
        {
            actions.Add("Explore automation strategies");
            actions.Add("Find process optimization tools");
        }

        if (message.ToLower().Contains("data") || message.ToLower().Contains("analytics"))
        {
            actions.Add("Learn about data intelligence");
            actions.Add("Explore reporting techniques");
        }

        // Age-specific suggestions
        if (ExperienceLevel.HasValue)
        {
            actions.AddRange(GetExperienceLevelSpecificActions(ExperienceLevel.Value));
        }

        return actions.Take(4).ToList();
    }

    private List<string> GetExperienceLevelSpecificActions(ExperienceLevel ExperienceLevel)
    {
        return ExperienceLevel switch
        {
            ExperienceLevel.Entry => new List<string> { "Find onboarding and training resources", "Explore team support and mentoring" },
            ExperienceLevel.Junior => new List<string> { "Learn about career transition planning", "Find professional networking groups" },
            ExperienceLevel.Mid => new List<string> { "Explore Career Advancement", "Learn about leadership and autonomy skills" },
            ExperienceLevel.Senior => new List<string> { "Find Job Performance support", "Explore work-life balance strategies" },
            ExperienceLevel.Principal => new List<string> { "Find professional development resources", "Explore professional networking resources" },
            _ => new List<string>()
        };
    }

    private List<string> ExtractKeywords(string message)
    {
        // Simple keyword extraction - could be enhanced with NLP
        var commonWords = new HashSet<string> { "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "a", "an", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them" };
        
        return message.ToLower()
            .Split(new char[] { ' ', ',', '.', '!', '?', ';', ':' }, StringSplitOptions.RemoveEmptyEntries)
            .Where(word => word.Length > 2 && !commonWords.Contains(word))
            .Take(5)
            .ToList();
    }

    private Task<List<object>> GetLocalBusinessResources(ExperienceLevel? ExperienceLevel)
    {
        // This would typically query a database of business resources
        // For now, returning example data
        return Task.FromResult(new List<object>
        {
            new { Name = "Enterprise Consulting Center", Phone = "(555) 123-4567", Type = "Business Support" },
            new { Name = "Business Intelligence Hub", Phone = "(555) 987-6543", Type = "Analytics Support" }
        });
    }

    private List<object> GetBusinessStrategies(ExperienceLevel? ExperienceLevel)
    {
        var strategies = new List<object>
        {
            new { Strategy = "Data-driven analysis", Description = "Use metrics and KPIs to evaluate business challenges objectively" },
            new { Strategy = "Process optimization", Description = "Apply lean methodologies and automation tools to streamline operations" },
            new { Strategy = "Stakeholder alignment", Description = "Ensure clear communication and shared objectives across teams" },
            new { Strategy = "Strategic planning", Description = "Develop comprehensive roadmaps with measurable milestones and outcomes" }
        };

        return strategies;
    }

    private List<object> GetBusinessTools(ExperienceLevel? ExperienceLevel)
    {
        return new List<object>
        {
            new { Tool = "Analytics dashboards", Description = "Real-time business intelligence and performance monitoring" },
            new { Tool = "Process automation", Description = "Workflow automation and AI-driven task optimization" },
            new { Tool = "Routine maintenance", Description = "Stick to familiar routines when possible" },
            new { Tool = "Communication cards", Description = "Use visual aids to communicate needs when overwhelmed" }
        };
    }

    private static string GetExperienceLevelDisplayName(ExperienceLevel ExperienceLevel)
    {
        return ExperienceLevel switch
        {
            ExperienceLevel.Entry => "Entry Level",
            ExperienceLevel.Junior => "Junior Level", 
            ExperienceLevel.Mid => "Mid Level",
            ExperienceLevel.Senior => "Senior Level",
            ExperienceLevel.Principal => "Principal Level",
            _ => ExperienceLevel.ToString()
        };
    }

    private static string GetExperienceLevelRange(ExperienceLevel ExperienceLevel)
    {
        return ExperienceLevel switch
        {
            ExperienceLevel.Entry => "Entry Level (0-2 years)",
            ExperienceLevel.Junior => "Junior Level (2-4 years)",
            ExperienceLevel.Mid => "Mid Level (4-7 years)", 
            ExperienceLevel.Senior => "Senior Level (7-10 years)",
            ExperienceLevel.Principal => "Principal+ Level (10+ years)",
            _ => "All Experience Levels"
        };
    }

    private static string GetExperienceLevelFocusAreas(ExperienceLevel experienceLevel)
    {
        return experienceLevel switch
        {
            ExperienceLevel.Entry => "Basic business concepts, process understanding, technology skills, foundational learning",
            ExperienceLevel.Junior => "Digital literacy, problem solving, team collaboration, project management basics",
            ExperienceLevel.Mid => "Strategic thinking, technology leadership, advanced analytics, business optimization",
            ExperienceLevel.Senior => "Enterprise architecture, stakeholder management, risk assessment, complex problem solving",
            ExperienceLevel.Principal => "Advanced business strategies, organization leadership, enterprise transformation",
            ExperienceLevel.Executive => "Strategic vision, board reporting, executive decision making, enterprise governance",
            _ => "General enterprise consulting across all experience levels"
        };
    }

    private CommunicationLevel DetermineCommunicationLevel(UserProfile? userProfile)
    {
        // Determine communication level based on user profile and preferences
        if (userProfile?.CommunicationPreferences != null)
        {
            var prefs = userProfile.CommunicationPreferences;
            
            // If they require simple language, use Simple level
            if (prefs.RequiresSimpleLanguage)
                return CommunicationLevel.Simple;
            
            // Base on preferred reading level
            return prefs.PreferredReadingLevel switch
            {
                <= 3 => CommunicationLevel.Simple,
                <= 6 => CommunicationLevel.Standard,
                <= 10 => CommunicationLevel.Advanced,
                _ => CommunicationLevel.Expert
            };
        }

        // Default based on user's age group from the User entity
        return userProfile?.User?.ExperienceLevel switch
        {
            ExperienceLevel.Entry => CommunicationLevel.Simple,
            ExperienceLevel.Junior => CommunicationLevel.Simple,
            ExperienceLevel.Mid => CommunicationLevel.Standard,
            ExperienceLevel.Senior => CommunicationLevel.Advanced,
            ExperienceLevel.Principal => CommunicationLevel.Advanced,
            _ => CommunicationLevel.Standard
        };
    }

    private string GenerateSafeFallbackResponse(string originalMessage, ExperienceLevel? ExperienceLevel)
    {
        // Generate age-appropriate safe fallback responses
        var responses = ExperienceLevel switch
        {
            ExperienceLevel.Entry or ExperienceLevel.Junior => new[]
            {
                "I want to help you feel better. Can you tell me what's happening in a different way?",
                "Let's try talking about this together. What would make you feel more comfortable?",
                "I'm here to listen. Can you share what's on your mind using different words?"
            },
            ExperienceLevel.Mid or ExperienceLevel.Senior => new[]
            {
                "I understand you're looking for support. Let me help you in a way that feels right for you.",
                "I want to give you the best response possible. Could you help me understand what you need?",
                "I'm here to support you. What would be most helpful right now?"
            },
            _ => new[]
            {
                "I want to provide you with helpful and appropriate support. Could you rephrase your question?",
                "I'm committed to giving you safe and useful guidance. Let's approach this differently.",
                "I'd like to help you in the most supportive way possible. Can you share more context?"
            }
        };

        var random = new Random();
        var baseResponse = responses[random.Next(responses.Length)];

        // Add enterprise-professional closing
        return baseResponse + "\n\nRemember, it's okay to take your time, and you're doing great by reaching out. 💙";
    }

    [HttpPost("feedback")]
    public IActionResult SubmitFeedback([FromBody] ChatFeedback feedback)
    {
        try
        {
            if (feedback == null || string.IsNullOrWhiteSpace(feedback.MessageId))
            {
                return BadRequest(new { message = "Invalid feedback payload" });
            }

            _logger.LogInformation("Chat feedback received. MessageId={MessageId}, Upvote={Upvote}, Comment={Comment}",
                feedback.MessageId, feedback.Upvote, feedback.Comment);

            // TODO: Persist to DB table for feedback analytics; enqueue to outbox for n8n if needed
            return Ok(new { message = "Thank you for your feedback" });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error recording chat feedback");
            return StatusCode(500, new { message = "Unable to record feedback" });
        }
    }
}

public class EnterpriseChatRequest
{
    public string Message { get; set; } = string.Empty;
    public Guid? UserId { get; set; }
    public ExperienceLevel? ExperienceLevel { get; set; }
    public List<ChatMessageHistory>? ConversationHistory { get; set; }
    public string? SessionId { get; set; }
    public string? Agent { get; set; }
}

public class ChatMessageHistory
{
    public string Role { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
}

public class EnterpriseChatResponse
{
    public string Message { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
    public DateTime Timestamp { get; set; }
    public List<SuggestedResource> SuggestedResources { get; set; } = new();
    public List<string> SuggestedActions { get; set; } = new();
    public ContentQualityInfo? ContentQuality { get; set; }
}

public class ContentQualityInfo
{
    public int EnterpriseComplianceScore { get; set; }
    public string QualityLevel { get; set; } = string.Empty;
    public bool HasWarnings { get; set; }
    public double ReadabilityScore { get; set; }
}

public class SuggestedResource
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Type { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
}

public class ChatFeedback
{
    public string MessageId { get; set; } = string.Empty;
    public bool Upvote { get; set; }
    public string? Comment { get; set; }
    public string? SessionId { get; set; }
}
