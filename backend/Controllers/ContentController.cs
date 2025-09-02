using Microsoft.AspNetCore.Mvc;
using EnterprisePlatformApi.Models;
using EnterprisePlatformApi.Data;
using Microsoft.EntityFrameworkCore;
using OpenAI;
using OpenAI.Chat;
using Microsoft.Extensions.Caching.Memory;

namespace EnterprisePlatformApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ContentController : ControllerBase
{
    private readonly EnterprisePlatformDbContext _context;
    private readonly ILogger<ContentController> _logger;
    private readonly OpenAIClient _openAIClient;
    private readonly IMemoryCache _cache;

    public ContentController(EnterprisePlatformDbContext context, ILogger<ContentController> logger, OpenAIClient openAIClient, IMemoryCache cache)
    {
        _context = context;
        _logger = logger;
        _openAIClient = openAIClient;
        _cache = cache;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ContentItem>>> GetContent(
        [FromQuery] ExperienceLevel? ExperienceLevel = null,
        [FromQuery] Guid? categoryId = null,
        [FromQuery] ContentType? contentType = null,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10)
    {
        try
        {
            var query = _context.ContentItems
                .Include(c => c.Category)
                .Include(c => c.Author)
                .Where(c => c.Status == ContentStatus.Published);

            if (ExperienceLevel.HasValue)
            {
                query = query.Where(c => c.Category.ExperienceLevel == ExperienceLevel);
            }

            if (categoryId.HasValue)
            {
                query = query.Where(c => c.CategoryId == categoryId);
            }

            if (contentType.HasValue)
            {
                query = query.Where(c => c.ContentType == contentType);
            }

            var totalItems = await query.CountAsync();
            var items = await query
                .OrderByDescending(c => c.PublishedAt)
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .Select(c => new
                {
                    c.Id,
                    c.Title,
                    c.Slug,
                    c.Summary,
                    c.ContentType,
                    c.DifficultyLevel,
                    c.EstimatedReadTime,
                    c.Keywords,
                    c.PublishedAt,
                    Category = new { c.Category.Id, c.Category.Name, c.Category.ExperienceLevel },
                    Author = new { c.Author.Id, c.Author.Profile!.FirstName, c.Author.Profile.LastName }
                })
                .ToListAsync();

            return Ok(new
            {
                Items = items,
                TotalItems = totalItems,
                Page = page,
                PageSize = pageSize,
                TotalPages = (int)Math.Ceiling((double)totalItems / pageSize)
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving content");
            return StatusCode(500, "An error occurred while retrieving content");
        }
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ContentItem>> GetContentItem(Guid id)
    {
        try
        {
            var contentItem = await _context.ContentItems
                .Include(c => c.Category)
                .Include(c => c.Author)
                    .ThenInclude(a => a.Profile)
                .FirstOrDefaultAsync(c => c.Id == id && c.Status == ContentStatus.Published);

            if (contentItem == null)
            {
                return NotFound();
            }

            return Ok(new
            {
                contentItem.Id,
                contentItem.Title,
                contentItem.Slug,
                contentItem.Content,
                contentItem.Summary,
                contentItem.ContentType,
                contentItem.DifficultyLevel,
                contentItem.EstimatedReadTime,
                contentItem.Keywords,
                contentItem.PublishedAt,
                contentItem.AltTextForImages,
                contentItem.AudioTranscript,
                contentItem.HasCaptionsForVideo,
                Category = new { contentItem.Category.Id, contentItem.Category.Name, contentItem.Category.ExperienceLevel },
                Author = new { 
                    contentItem.Author.Id, 
                    Name = $"{contentItem.Author.Profile?.FirstName} {contentItem.Author.Profile?.LastName}".Trim()
                }
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving content item {ContentId}", id);
            return StatusCode(500, "An error occurred while retrieving the content item");
        }
    }

    [HttpGet("categories")]
    public async Task<ActionResult<IEnumerable<ContentCategory>>> GetCategories([FromQuery] ExperienceLevel? ExperienceLevel = null)
    {
        try
        {
            var query = _context.ContentCategories.AsQueryable();

            if (ExperienceLevel.HasValue)
            {
                query = query.Where(c => c.ExperienceLevel == ExperienceLevel);
            }

            var categories = await query
                .OrderBy(c => c.SortOrder)
                .ThenBy(c => c.Name)
                .Select(c => new
                {
                    c.Id,
                    c.Name,
                    c.ExperienceLevel,
                    c.Description,
                    c.IconUrl,
                    c.SortOrder,
                    ContentCount = c.ContentItems.Count(ci => ci.Status == ContentStatus.Published)
                })
                .ToListAsync();

            return Ok(categories);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving categories");
            return StatusCode(500, "An error occurred while retrieving categories");
        }
    }

    [HttpGet("age-groups")]
    public ActionResult<object> GetExperienceLevels()
    {
        var ExperienceLevels = Enum.GetValues<ExperienceLevel>()
            .Select(ag => new
            {
                Value = ag.ToString(),
                DisplayName = GetExperienceLevelDisplayName(ag),
                Description = GetExperienceLevelDescription(ag),
                AgeRange = GetExperienceLevelRange(ag)
            })
            .ToList();

        return Ok(ExperienceLevels);
    }

    [HttpPost("search")]
    public async Task<ActionResult<IEnumerable<ContentItem>>> SearchContent([FromBody] ContentSearchRequest request)
    {
        try
        {
            var query = _context.ContentItems
                .Include(c => c.Category)
                .Include(c => c.Author)
                    .ThenInclude(a => a.Profile)
                .Where(c => c.Status == ContentStatus.Published);

            if (!string.IsNullOrWhiteSpace(request.SearchTerm))
            {
                query = query.Where(c => 
                    c.Title.Contains(request.SearchTerm) ||
                    c.Content.Contains(request.SearchTerm) ||
                    c.Keywords.Any(k => k.Contains(request.SearchTerm)));
            }

            if (request.ExperienceLevel.HasValue)
            {
                query = query.Where(c => c.Category.ExperienceLevel == request.ExperienceLevel);
            }

            if (request.ContentType.HasValue)
            {
                query = query.Where(c => c.ContentType == request.ContentType);
            }

            if (request.DifficultyLevel.HasValue)
            {
                query = query.Where(c => c.DifficultyLevel <= request.DifficultyLevel);
            }

            var results = await query
                .OrderByDescending(c => c.PublishedAt)
                .Take(50) // Limit search results
                .Select(c => new
                {
                    c.Id,
                    c.Title,
                    c.Slug,
                    c.Summary,
                    c.ContentType,
                    c.DifficultyLevel,
                    c.EstimatedReadTime,
                    c.Keywords,
                    c.PublishedAt,
                    Category = new { c.Category.Id, c.Category.Name, c.Category.ExperienceLevel },
                    Author = new { 
                        c.Author.Id, 
                        Name = $"{c.Author.Profile!.FirstName} {c.Author.Profile.LastName}".Trim()
                    }
                })
                .ToListAsync();

            return Ok(results);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error searching content");
            return StatusCode(500, "An error occurred while searching content");
        }
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

    private static string GetExperienceLevelDescription(ExperienceLevel ExperienceLevel)
    {
        return ExperienceLevel switch
        {
            ExperienceLevel.Entry => "Onboarding Support, Training Resources, and family resources",
            ExperienceLevel.Junior => "Team Collaboration development and academic accommodations",
            ExperienceLevel.Mid => "Independence preparation and college/career planning",
            ExperienceLevel.Senior => "Post-secondary education and Job Performance preparation",
            ExperienceLevel.Principal => "Professional Development and Work-Life Balance",
            _ => "General enterprise business resources"
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

    [HttpPost("generate")]
    public async Task<ActionResult<IEnumerable<object>>> GenerateContent(
        [FromBody] ContentGenerationRequest request)
    {
        try
        {
            var ageRange = GetExperienceLevelRange(request.ExperienceLevel);
            var prompt = $@"Generate {request.Count} enterprise-professional content items for {ageRange}. 

REQUIREMENTS:
- Write in clear, simple language appropriate for {ageRange}
- Use bullet points and numbered lists for easy reading
- Focus on practical, actionable advice
- Keep paragraphs short (2-3 sentences max)
- Include specific examples when helpful
- Make content positive and empowering

FORMAT each item as:
Title: [Clear, helpful title]
Summary: [2-3 sentence overview]
Content: [Well-structured content with bullet points, numbered steps, or short paragraphs]
Tags: [3-5 relevant tags]

TOPICS should cover:
- Business process optimization
- Strategic planning methodologies  
- Performance management techniques
- Analytics tools and dashboards
- Leadership and team development
- Data-driven decision making

Make content immediately useful and business-focused. Present information in clear, structured formats.";

            var messages = new List<ChatMessage>
            {
                new SystemChatMessage("You are an expert enterprise business consultant who creates clear, practical content. Focus on actionable business advice presented in professional formats."),
                new UserChatMessage(prompt)
            };

            var chatCompletion = await _openAIClient.GetChatClient("gpt-4").CompleteChatAsync(messages);
            var responseContent = chatCompletion.Value.Content[0].Text;

            // Parse the AI response and create structured content items
            var generatedItems = ParseAIContentResponse(responseContent, request);

            // Project to a consistent shape with GetContent list items
            var projected = generatedItems.Select(i => new
            {
                i.Id,
                i.Title,
                i.Slug,
                i.Content,
                i.Summary,
                i.ContentType,
                i.DifficultyLevel,
                i.EstimatedReadTime,
                i.Keywords,
                i.PublishedAt,
                Category = new { Id = Guid.Empty, Name = "AI Generated", ExperienceLevel = request.ExperienceLevel },
                Author = new { Id = Guid.Empty, Name = "AI Content" }
            });

            return Ok(projected);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error generating content");
            return StatusCode(500, "Error generating content");
        }
    }

    private List<ContentItem> ParseAIContentResponse(string aiResponse, ContentGenerationRequest request)
    {
        var items = new List<ContentItem>();
        
        // Split the response into individual content items
        var sections = aiResponse.Split(new[] { "Title:", "\nTitle:" }, StringSplitOptions.RemoveEmptyEntries);
        
        for (int i = 0; i < Math.Min(sections.Length, request.Count); i++)
        {
            var section = sections[i].Trim();
            if (string.IsNullOrEmpty(section)) continue;

            var lines = section.Split('\n', StringSplitOptions.RemoveEmptyEntries);
            
            string title = "Generated Content";
            string summary = "AI-generated enterprise business content";
            string content = section;
            List<string> tags = new List<string> { "enterprise-business", "practical-tips" };

            // Parse title
            if (lines.Length > 0)
            {
                title = lines[0].Replace("Title:", "").Trim();
            }

            // Find summary
            var summaryIndex = Array.FindIndex(lines, l => l.StartsWith("Summary:", StringComparison.OrdinalIgnoreCase));
            if (summaryIndex >= 0 && summaryIndex + 1 < lines.Length)
            {
                summary = lines[summaryIndex].Replace("Summary:", "").Trim();
            }

            // Find content
            var contentIndex = Array.FindIndex(lines, l => l.StartsWith("Content:", StringComparison.OrdinalIgnoreCase));
            if (contentIndex >= 0)
            {
                var contentLines = lines.Skip(contentIndex + 1).TakeWhile(l => !l.StartsWith("Tags:", StringComparison.OrdinalIgnoreCase));
                content = string.Join("\n", contentLines).Trim();
            }

            // Find tags
            var tagsIndex = Array.FindIndex(lines, l => l.StartsWith("Tags:", StringComparison.OrdinalIgnoreCase));
            if (tagsIndex >= 0 && tagsIndex < lines.Length)
            {
                var tagLine = lines[tagsIndex].Replace("Tags:", "").Trim();
                tags = tagLine.Split(',').Select(t => t.Trim()).Where(t => !string.IsNullOrEmpty(t)).ToList();
            }

            items.Add(new ContentItem
            {
                Id = Guid.NewGuid(),
                Title = title,
                Summary = summary,
                Content = content,
                ContentType = request.ContentType,
                DifficultyLevel = request.DifficultyLevel,
                Status = ContentStatus.Published,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow,
                PublishedAt = DateTime.UtcNow,
                Keywords = tags,
                EstimatedReadTime = Math.Max(1, content.Length / 200), // Rough estimate
                CategoryId = Guid.NewGuid(), // You'd want to map this properly
                AuthorId = Guid.NewGuid() // System-generated content
            });
        }

        return items;
    }

    [HttpGet("tip-of-the-day")]
    public ActionResult<TipOfDayResponse> GetTipOfTheDay([FromQuery] ExperienceLevel? ExperienceLevel = null, [FromQuery] bool fresh = false)
    {
        try
        {
            var ag = ExperienceLevel ?? ExperienceLevel.Mid;
            var todayKey = $"tip:{ag}:{DateTime.UtcNow:yyyyMMdd}";

            if (!fresh)
            {
                if (_cache.TryGetValue<TipOfDayResponse>(todayKey, out var cached) && cached != null)
                {
                    return Ok(cached);
                }
            }

            var tips = GetTipsByExperienceLevel(ag);
            // Pick stable tip per day unless fresh=true, then randomize
            int index;
            if (fresh)
            {
                var rnd = new Random();
                index = rnd.Next(0, Math.Max(1, tips.Count));
            }
            else
            {
                var seed = int.Parse(DateTime.UtcNow.ToString("yyyyMMdd"));
                index = Math.Abs(seed) % tips.Count;
            }
            var tip = tips[index];

            // Attach a relevant category link if available
            var category = _context.ContentCategories
                .Where(c => c.ExperienceLevel == ag)
                .OrderBy(c => c.SortOrder)
                .FirstOrDefault();

            var response = new TipOfDayResponse
            {
                Title = tip.title,
                Text = tip.text,
                ExperienceLevel = ag.ToString(),
                LinkUrl = category != null ? $"/resources/category/{category.Id}" : null,
                LinkText = category != null ? $"Explore {category.Name}" : null,
                ExpiresAt = DateTime.UtcNow.Date.AddDays(1)
            };

            if (!fresh)
            {
                _cache.Set(todayKey, response, TimeSpan.FromHours(12));
            }
            return Ok(response);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error generating tip of the day");
            return StatusCode(500, new { message = "Unable to load tip of the day" });
        }
    }

    private List<(string title, string text)> GetTipsByExperienceLevel(ExperienceLevel ExperienceLevel)
    {
        return ExperienceLevel switch
        {
            ExperienceLevel.Entry => new()
            {
                ("Visual Project Planning", "Use simple charts to show project steps and deadlines. Keep planning clear and consistent."),
                ("Focus Break System", "Create a 5-minute break schedule with productive activities (stretch, walk, organize). Use when concentrating."),
                ("Presentation Practice", "Practice one presentation skill each day: clear voice, eye contact, or confident posture.")
            },
            ExperienceLevel.Junior => new()
            {
                ("Team Collaboration", "Keep 3 collaboration topics ready (projects, goals, ideas). Ask questions like 'What works best for our team?'"),
                ("Productivity Planning", "Use time-blocking techniques for focused work. Set clear boundaries for deep work sessions."),
                ("Learning Micro-Goals", "Break learning into 15-minute focused sessions with 5-minute reviews. Use timers to track progress.")
            },
            ExperienceLevel.Mid => new()
            {
                ("Leadership Practice", "Identify 3 achievements and 2 leadership strengths. Practice presenting them clearly and confidently."),
                ("Business Strategy", "Develop strategic planning skills with data analysis. Use frameworks like SWOT for decision making."),
                ("Professional Networking", "Send professional messages to connections: 'Hope your projects are going well.' Keep communication business-focused.")
            },
            ExperienceLevel.Senior => new()
            {
                ("Professional Development", "Choose one business skill to develop this week (analytics, presentations, project management). Create a learning plan."),
                ("Workplace Excellence", "Practice professional scripts for common situations: meetings, reporting, stakeholder communication."),
                ("Performance Optimization", "Track your productivity patterns for 3 days. Schedule important tasks during peak performance windows.")
            },
            _ => new()
            {
                ("Work Productivity", "Try a 50/10 productivity rhythm: 50 minutes focused work, 10 minutes strategic break. Use timers and minimize distractions."),
                ("Professional Communication", "Develop clear communication about your optimal work conditions (environment, tools, processes). Share with your team."),
                ("Strategic Reset", "Implement a 2-minute strategic reset: review priorities, assess progress, or take a brief planning walk.")
            }
        };
    }
}

public class ContentSearchRequest
{
    public string? SearchTerm { get; set; }
    public ExperienceLevel? ExperienceLevel { get; set; }
    public ContentType? ContentType { get; set; }
    public int? DifficultyLevel { get; set; }
}

public class ContentGenerationRequest
{
    public ExperienceLevel ExperienceLevel { get; set; }
    public ContentType ContentType { get; set; }
    public int DifficultyLevel { get; set; }
    public int Count { get; set; } = 5;
}

public class TipOfDayResponse
{
    public string Title { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public string? LinkUrl { get; set; }
    public string? LinkText { get; set; }
    public string ExperienceLevel { get; set; } = string.Empty;
    public DateTime ExpiresAt { get; set; }
}
