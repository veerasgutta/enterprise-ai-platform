using Microsoft.AspNetCore.Mvc;
using EnterprisePlatformApi.Services;

namespace EnterprisePlatformApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class WorkspaceController : ControllerBase
{
    private readonly WorkspaceStatusManager _workspaceManager;
    private readonly ILogger<WorkspaceController> _logger;

    public WorkspaceController(
        WorkspaceStatusManager workspaceManager,
        ILogger<WorkspaceController> logger)
    {
        _workspaceManager = workspaceManager;
        _logger = logger;
    }

    /// <summary>
    /// Get workspace overview with all projects
    /// </summary>
    [HttpGet("overview")]
    public async Task<ActionResult<WorkspaceStatusSummary>> GetWorkspaceOverview()
    {
        _logger.LogInformation("Getting workspace overview");
        
        var summary = await _workspaceManager.GetWorkspaceStatusAsync();
        return Ok(summary);
    }

    /// <summary>
    /// Get context for specific project (optimized for conversations)
    /// </summary>
    [HttpGet("project/{projectName}/context")]
    public async Task<ActionResult<string>> GetProjectContext(string projectName)
    {
        _logger.LogInformation($"Getting context for project: {projectName}");
        
        var context = await _workspaceManager.GenerateProjectContextAsync(projectName);
        return Ok(context);
    }

    /// <summary>
    /// Get smart context based on recently modified files
    /// </summary>
    [HttpGet("smart-context")]
    public async Task<ActionResult<SmartContextResponse>> GetSmartContext()
    {
        _logger.LogInformation("Generating smart context based on recent activity");
        
        var workspaceStatus = await _workspaceManager.GetWorkspaceStatusAsync();
        var activeProject = workspaceStatus.Projects
            .OrderByDescending(p => p.LastActivity)
            .FirstOrDefault();

        if (activeProject == null)
        {
            return Ok(new SmartContextResponse 
            { 
                Message = "No active projects found",
                RecommendedFocus = "Start with project setup and planning"
            });
        }

        var projectContext = await _workspaceManager.GenerateProjectContextAsync(activeProject.Name);
        var dependencies = await _workspaceManager.GetProjectDependenciesAsync();
        
        return Ok(new SmartContextResponse
        {
            ActiveProject = activeProject.Name,
            ProjectContext = projectContext,
            CrossProjectBlockers = dependencies.Where(d => d.IsBlocking).ToList(),
            RecommendedFocus = GenerateRecommendedFocus(activeProject, dependencies),
            Message = $"Currently focused on {activeProject.Name} project"
        });
    }

    /// <summary>
    /// Update status for specific project
    /// </summary>
    [HttpPost("project/{projectName}/update")]
    public async Task<ActionResult> UpdateProjectStatus(
        string projectName, 
        [FromBody] ProjectUpdateRequest request)
    {
        _logger.LogInformation($"Updating status for project: {projectName}");
        
        await _workspaceManager.UpdateProjectStatusAsync(
            projectName, 
            request.Feature, 
            request.Category, 
            request.Description);
        
        return Ok(new { message = $"Updated {projectName} project status" });
    }

    /// <summary>
    /// Add new project to workspace
    /// </summary>
    [HttpPost("project")]
    public async Task<ActionResult> CreateProject([FromBody] CreateProjectRequest request)
    {
        _logger.LogInformation($"Creating new project: {request.Name}");
        
        await _workspaceManager.AddProjectAsync(
            request.Name,
            request.Path,
            request.Description,
            request.Type);
        
        return Ok(new { message = $"Created project {request.Name}" });
    }

    /// <summary>
    /// Get conversation-optimized summary (minimal tokens)
    /// </summary>
    [HttpGet("conversation-summary")]
    public async Task<ActionResult<ConversationSummary>> GetConversationSummary()
    {
        _logger.LogInformation("Generating conversation-optimized summary");
        
        var workspaceStatus = await _workspaceManager.GetWorkspaceStatusAsync();
        var activeProject = workspaceStatus.Projects
            .OrderByDescending(p => p.LastActivity)
            .FirstOrDefault();

        var summary = new ConversationSummary
        {
            WorkspaceProgress = workspaceStatus.OverallProgress,
            ActiveProject = activeProject?.Name ?? "No active project",
            ActiveProjectProgress = activeProject?.Progress ?? 0,
            ActiveProjectPhase = activeProject?.Phase ?? "Unknown",
            ProjectCount = workspaceStatus.Projects.Count,
            LastActivity = workspaceStatus.Projects.Max(p => p.LastActivity),
            TopPriorities = await GetTopPriorities(activeProject?.Name)
        };

        return Ok(summary);
    }

    #region Private Methods

    private string GenerateRecommendedFocus(ProjectStatusSummary activeProject, List<ProjectDependency> dependencies)
    {
        var blockers = dependencies.Where(d => d.IsBlocking && d.ToProject == activeProject.Name).ToList();
        
        if (blockers.Any())
        {
            return $"Resolve blocking dependencies: {string.Join(", ", blockers.Select(b => b.FromProject))}";
        }

        return activeProject.Progress switch
        {
            < 25 => "Focus on foundational setup and architecture",
            < 50 => "Continue core feature development",
            < 75 => "Focus on integration and testing",
            _ => "Polish and prepare for production"
        };
    }

    private async Task<List<string>> GetTopPriorities(string? projectName)
    {
        if (string.IsNullOrEmpty(projectName))
        {
            return new List<string> { "Define active project and priorities" };
        }

        // This would parse the project's status file to extract immediate priorities
        // Simplified implementation
        return new List<string>
        {
            "Continue current development sprint",
            "Address any blocking issues",
            "Maintain code quality standards"
        };
    }

    #endregion
}

// Request/Response Models
public class ProjectUpdateRequest
{
    public string Feature { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
}

public class CreateProjectRequest
{
    public string Name { get; set; } = string.Empty;
    public string Path { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public ProjectType Type { get; set; }
}

public class SmartContextResponse
{
    public string ActiveProject { get; set; } = string.Empty;
    public string ProjectContext { get; set; } = string.Empty;
    public List<ProjectDependency> CrossProjectBlockers { get; set; } = new();
    public string RecommendedFocus { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
}

public class ConversationSummary
{
    public int WorkspaceProgress { get; set; }
    public string ActiveProject { get; set; } = string.Empty;
    public int ActiveProjectProgress { get; set; }
    public string ActiveProjectPhase { get; set; } = string.Empty;
    public int ProjectCount { get; set; }
    public DateTime LastActivity { get; set; }
    public List<string> TopPriorities { get; set; } = new();
}
