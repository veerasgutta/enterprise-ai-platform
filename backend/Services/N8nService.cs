using System.Text;
using System.Text.Json;
using Microsoft.Extensions.Options;
using EnterprisePlatformApi.Models;

namespace EnterprisePlatformApi.Services;

public class N8nService
{
    private readonly HttpClient _httpClient;
    private readonly N8nSettings _settings;
    private readonly ILogger<N8nService> _logger;

    public N8nService(HttpClient httpClient, IOptions<N8nSettings> settings, ILogger<N8nService> logger)
    {
        _httpClient = httpClient;
        _settings = settings.Value;
        _logger = logger;
        
        // Configure HttpClient with basic auth if needed
        if (!string.IsNullOrEmpty(_settings.BasicAuthUser) && !string.IsNullOrEmpty(_settings.BasicAuthPassword))
        {
            var authValue = Convert.ToBase64String(Encoding.UTF8.GetBytes($"{_settings.BasicAuthUser}:{_settings.BasicAuthPassword}"));
            _httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", authValue);
        }
    }

    /// <summary>
    /// Trigger a specific n8n workflow with Enterprise platform data
    /// </summary>
    public async Task<bool> TriggerWorkflowAsync(string workflowName, object data)
    {
        try
        {
            var webhookUrl = $"{_settings.BaseUrl}/webhook/{workflowName}";
            var jsonData = JsonSerializer.Serialize(data);
            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            _logger.LogInformation($"Triggering n8n workflow: {workflowName}");
            
            var response = await _httpClient.PostAsync(webhookUrl, content);
            
            if (response.IsSuccessStatusCode)
            {
                _logger.LogInformation($"Successfully triggered workflow: {workflowName}");
                return true;
            }
            else
            {
                _logger.LogError($"Failed to trigger workflow: {workflowName}. Status: {response.StatusCode}");
                return false;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Error triggering n8n workflow: {workflowName}");
            return false;
        }
    }

    /// <summary>
    /// Send Enterprise-specific notification through n8n
    /// </summary>
    public async Task<bool> SendEnterpriseNotificationAsync(EnterpriseNotificationRequest request)
    {
        var workflowData = new
        {
            notification = new
            {
                id = request.Id,
                userId = request.UserId,
                type = request.Type.ToString(),
                title = request.Title,
                message = request.Message,
                priority = request.Priority,
                scheduledFor = request.ScheduledFor,
                channels = request.Channels,
                businessContext = request.BusinessContext,
                userProfile = request.UserProfile
            },
            timestamp = DateTime.UtcNow,
            source = "enterprise-platform"
        };

        return await TriggerWorkflowAsync("enterprise-notification", workflowData);
    }

    /// <summary>
    /// Send emergency alert through multiple channels
    /// </summary>
    public async Task<bool> SendEmergencyAlertAsync(EmergencyAlertRequest request)
    {
        var workflowData = new
        {
            emergency = new
            {
                id = request.Id,
                userId = request.UserId,
                alertType = request.AlertType,
                severity = request.Severity,
                message = request.Message,
                location = request.Location,
                emergencyContacts = request.EmergencyContacts,
                userProfile = request.UserProfile
            },
            timestamp = DateTime.UtcNow,
            source = "enterprise-platform-emergency"
        };

        return await TriggerWorkflowAsync("emergency-alert", workflowData);
    }

    /// <summary>
    /// Send routine reminder with enterprise-professional formatting
    /// </summary>
    public async Task<bool> SendRoutineReminderAsync(RoutineReminderRequest request)
    {
        var workflowData = new
        {
            reminder = new
            {
                id = request.Id,
                userId = request.UserId,
                routineType = request.RoutineType,
                title = request.Title,
                description = request.Description,
                scheduledTime = request.ScheduledTime,
                visualAids = request.VisualAids,
                businessRequirements = request.BusinessRequirements,
                parentNotification = request.NotifyParents
            },
            timestamp = DateTime.UtcNow,
            source = "enterprise-platform-routine"
        };

        return await TriggerWorkflowAsync("routine-reminder", workflowData);
    }

    /// <summary>
    /// Send progress update to parents/caregivers
    /// </summary>
    public async Task<bool> SendProgressUpdateAsync(ProgressUpdateRequest request)
    {
        var workflowData = new
        {
            progress = new
            {
                id = request.Id,
                userId = request.UserId,
                reportType = request.ReportType,
                achievements = request.Achievements,
                challenges = request.Challenges,
                recommendations = request.Recommendations,
                dataVisualization = request.DataVisualization,
                parentEmails = request.ParentEmails
            },
            timestamp = DateTime.UtcNow,
            source = "enterprise-platform-progress"
        };

        return await TriggerWorkflowAsync("progress-update", workflowData);
    }

    /// <summary>
    /// Trigger social story delivery workflow
    /// </summary>
    public async Task<bool> SendSocialStoryAsync(SocialStoryRequest request)
    {
        var workflowData = new
        {
            socialStory = new
            {
                id = request.Id,
                userId = request.UserId,
                storyTitle = request.StoryTitle,
                storyContent = request.StoryContent,
                visualElements = request.VisualElements,
                audioElements = request.AudioElements,
                interactiveElements = request.InteractiveElements,
                ageAppropriate = request.AgeAppropriate
            },
            timestamp = DateTime.UtcNow,
            source = "enterprise-platform-social-story"
        };

        return await TriggerWorkflowAsync("social-story-delivery", workflowData);
    }

    /// <summary>
    /// Get workflow execution status
    /// </summary>
    public async Task<WorkflowExecutionStatus?> GetWorkflowStatusAsync(string executionId)
    {
        try
        {
            var response = await _httpClient.GetAsync($"{_settings.BaseUrl}/api/v1/executions/{executionId}");
            
            if (response.IsSuccessStatusCode)
            {
                var jsonResponse = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<WorkflowExecutionStatus>(jsonResponse);
            }
            
            return null;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Error getting workflow status: {executionId}");
            return null;
        }
    }
}

public class N8nSettings
{
    public string BaseUrl { get; set; } = "http://localhost:5678";
    public string? BasicAuthUser { get; set; }
    public string? BasicAuthPassword { get; set; }
    public int TimeoutSeconds { get; set; } = 30;
}

// Request Models for Enterprise-Specific Workflows
public class EnterpriseNotificationRequest
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public NotificationType Type { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public string Priority { get; set; } = "normal"; // low, normal, high, critical
    public DateTime? ScheduledFor { get; set; }
    public List<string> Channels { get; set; } = new(); // email, sms, push, discord, slack
    public object? BusinessContext { get; set; }
    public object? UserProfile { get; set; }
}

public class EmergencyAlertRequest
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string AlertType { get; set; } = string.Empty; // business, operational, security, missing
    public string Severity { get; set; } = "high"; // low, medium, high, critical
    public string Message { get; set; } = string.Empty;
    public object? Location { get; set; }
    public List<object> EmergencyContacts { get; set; } = new();
    public object? UserProfile { get; set; }
}

public class RoutineReminderRequest
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string RoutineType { get; set; } = string.Empty; // meeting, workflow, monitoring, reporting
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public DateTime ScheduledTime { get; set; }
    public List<string> VisualAids { get; set; } = new();
    public object? BusinessRequirements { get; set; }
    public bool NotifyParents { get; set; }
}

public class ProgressUpdateRequest
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string ReportType { get; set; } = string.Empty; // daily, weekly, monthly, milestone
    public List<object> Achievements { get; set; } = new();
    public List<object> Challenges { get; set; } = new();
    public List<string> Recommendations { get; set; } = new();
    public object? DataVisualization { get; set; }
    public List<string> ParentEmails { get; set; } = new();
}

public class SocialStoryRequest
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string StoryTitle { get; set; } = string.Empty;
    public string StoryContent { get; set; } = string.Empty;
    public List<object> VisualElements { get; set; } = new();
    public List<object> AudioElements { get; set; } = new();
    public List<object> InteractiveElements { get; set; } = new();
    public bool AgeAppropriate { get; set; } = true;
}

public class WorkflowExecutionStatus
{
    public string Id { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty; // running, success, error, canceled
    public DateTime StartedAt { get; set; }
    public DateTime? FinishedAt { get; set; }
    public string? Error { get; set; }
    public object? Data { get; set; }
}
