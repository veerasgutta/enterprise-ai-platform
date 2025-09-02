using Microsoft.AspNetCore.Mvc;
using EnterprisePlatformApi.Services;

namespace EnterprisePlatformApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProjectStatusController : ControllerBase
{
    private readonly ProjectStatusUpdaterService _statusUpdater;
    private readonly ILogger<ProjectStatusController> _logger;

    public ProjectStatusController(
        ProjectStatusUpdaterService statusUpdater,
        ILogger<ProjectStatusController> logger)
    {
        _statusUpdater = statusUpdater;
        _logger = logger;
    }

    /// <summary>
    /// Get current project status summary for conversation context
    /// </summary>
    [HttpGet("summary")]
    public async Task<ActionResult<string>> GetProjectSummary()
    {
        _logger.LogInformation("Generating project status summary");
        
        var summary = await _statusUpdater.GenerateContextSummaryAsync();
        return Ok(summary);
    }

    /// <summary>
    /// Record completion of a new feature
    /// </summary>
    [HttpPost("feature-completed")]
    public async Task<ActionResult> RecordFeatureCompletion([FromBody] FeatureCompletionRequest request)
    {
        _logger.LogInformation($"Recording feature completion: {request.FeatureName}");
        
        await _statusUpdater.RecordFeatureCompletion(
            request.FeatureName, 
            request.Category, 
            request.Description);
        
        return Ok(new { message = "Feature completion recorded successfully" });
    }

    /// <summary>
    /// Update overall project progress
    /// </summary>
    [HttpPost("update-progress")]
    public async Task<ActionResult> UpdateProgress([FromBody] ProjectProgressUpdateRequest request)
    {
        _logger.LogInformation($"Updating project progress to {request.ProgressPercentage}%");
        
        await _statusUpdater.RecordProgressMilestone(
            request.ProgressPercentage, 
            request.Milestone);
        
        return Ok(new { message = "Progress updated successfully" });
    }

    /// <summary>
    /// Record autonomous service creation
    /// </summary>
    [HttpPost("autonomous-service")]
    public async Task<ActionResult> RecordAutonomousService([FromBody] AutonomousServiceRequest request)
    {
        _logger.LogInformation($"Recording autonomous service: {request.ServiceName}");
        
        await _statusUpdater.RecordAutonomousServiceAsync(
            request.ServiceName,
            request.Success,
            request.Details);
        
        return Ok(new { message = "Autonomous service recorded successfully" });
    }

    /// <summary>
    /// Add a new priority to the project roadmap
    /// </summary>
    [HttpPost("add-priority")]
    public async Task<ActionResult> AddPriority([FromBody] PriorityRequest request)
    {
        _logger.LogInformation($"Adding new priority: {request.Priority}");
        
        await _statusUpdater.AddNextPriorityAsync(request.Priority, request.Description);
        await _statusUpdater.UpdateTimestampAsync();
        
        return Ok(new { message = "Priority added successfully" });
    }

    /// <summary>
    /// Automatically update status after autonomous service building
    /// </summary>
    [HttpPost("auto-update")]
    public async Task<ActionResult> AutoUpdateStatus([FromBody] AutoUpdateRequest request)
    {
        _logger.LogInformation("Performing automatic status update");
        
        // Update multiple aspects based on the request
        if (!string.IsNullOrEmpty(request.CompletedFeature))
        {
            await _statusUpdater.UpdateCompletedFeatureAsync(
                request.Category ?? "Development",
                request.CompletedFeature,
                request.FeatureDescription ?? "Feature completed successfully");
        }

        if (request.NewProgress.HasValue)
        {
            await _statusUpdater.UpdateProgressAsync(request.NewProgress.Value);
        }

        if (!string.IsNullOrEmpty(request.NextPriority))
        {
            await _statusUpdater.AddNextPriorityAsync(
                request.NextPriority,
                request.PriorityDescription ?? "Continue development");
        }

        // Always update timestamp
        await _statusUpdater.UpdateTimestampAsync();

        // Return updated summary
        var summary = await _statusUpdater.GenerateContextSummaryAsync();
        
        return Ok(new 
        { 
            message = "Status updated successfully",
            updatedSummary = summary
        });
    }
}

// Request Models
public class FeatureCompletionRequest
{
    public string FeatureName { get; set; } = string.Empty;
    public string Category { get; set; } = "Development";
    public string Description { get; set; } = string.Empty;
}

public class ProjectProgressUpdateRequest
{
    public int ProgressPercentage { get; set; }
    public string Milestone { get; set; } = string.Empty;
}

public class AutonomousServiceRequest
{
    public string ServiceName { get; set; } = string.Empty;
    public bool Success { get; set; }
    public string Details { get; set; } = string.Empty;
}

public class PriorityRequest
{
    public string Priority { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
}

public class AutoUpdateRequest
{
    public string? CompletedFeature { get; set; }
    public string? Category { get; set; }
    public string? FeatureDescription { get; set; }
    public int? NewProgress { get; set; }
    public string? NextPriority { get; set; }
    public string? PriorityDescription { get; set; }
}
