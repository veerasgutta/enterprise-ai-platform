using Microsoft.AspNetCore.Mvc;
using EnterprisePlatformApi.Models;
using EnterprisePlatformApi.Data;
using EnterprisePlatformApi.Services;
using Microsoft.EntityFrameworkCore;

namespace EnterprisePlatformApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class NotificationController : ControllerBase
{
    private readonly EnterprisePlatformDbContext _context;
    private readonly N8nService _n8nService;
    private readonly ILogger<NotificationController> _logger;

    public NotificationController(
        EnterprisePlatformDbContext context,
        N8nService n8nService,
        ILogger<NotificationController> logger)
    {
        _context = context;
        _n8nService = n8nService;
        _logger = logger;
    }

    /// <summary>
    /// Get all notifications for a user
    /// </summary>
    [HttpGet("user/{userId}")]
    public async Task<ActionResult<List<Notification>>> GetUserNotifications(Guid userId)
    {
        var notifications = await _context.Notifications
            .Where(n => n.UserId == userId)
            .OrderByDescending(n => n.CreatedAt)
            .Take(50)
            .ToListAsync();

        return Ok(notifications);
    }

    /// <summary>
    /// Send a custom notification through n8n workflows
    /// </summary>
    [HttpPost("send")]
    public async Task<IActionResult> SendNotification([FromBody] SendNotificationRequest request)
    {
        try
        {
            // Get user profile for personalization
            var user = await _context.Users
                .Include(u => u.Profile)
                .FirstOrDefaultAsync(u => u.Id == request.UserId);

            if (user == null)
            {
                return NotFound("User not found");
            }

            // Create notification record
            var notification = new Notification
            {
                Id = Guid.NewGuid(),
                UserId = request.UserId,
                Type = request.Type,
                Title = request.Title,
                Message = request.Message,
                Data = request.Data,
                IsCritical = request.IsCritical,
                ScheduledFor = request.ScheduledFor,
                CreatedAt = DateTime.UtcNow
            };

            _context.Notifications.Add(notification);
            await _context.SaveChangesAsync();

            // Prepare enterprise-specific notification request
            var n8nRequest = new EnterpriseNotificationRequest
            {
                Id = notification.Id,
                UserId = request.UserId,
                Type = request.Type,
                Title = request.Title,
                Message = request.Message,
                Priority = request.IsCritical ? "critical" : "normal",
                ScheduledFor = request.ScheduledFor,
                Channels = request.Channels ?? GetDefaultChannels(user),
                BusinessContext = user.Profile?.BusinessContext,
                UserProfile = new
                {
                    ExperienceLevel = user.ExperienceLevel?.ToString(),
                    PreferredCommunication = user.PreferredCommunicationMethod.ToString(),
                    BusinessNeeds = user.Profile?.BusinessContext,
                    CommunicationPreferences = user.Profile?.CommunicationPreferences
                }
            };

            // Trigger n8n workflow
            var success = await _n8nService.SendEnterpriseNotificationAsync(n8nRequest);

            if (success)
            {
                notification.SentAt = DateTime.UtcNow;
                await _context.SaveChangesAsync();
                return Ok(new { notificationId = notification.Id, workflowTriggered = true });
            }
            else
            {
                return StatusCode(500, "Failed to trigger notification workflow");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error sending notification");
            return StatusCode(500, "Internal server error");
        }
    }

    /// <summary>
    /// Send emergency alert through n8n emergency workflow
    /// </summary>
    [HttpPost("emergency")]
    public async Task<IActionResult> SendEmergencyAlert([FromBody] EmergencyAlertRequest request)
    {
        try
        {
            // Get user with emergency contacts
            var user = await _context.Users
                .Include(u => u.Profile)
                .FirstOrDefaultAsync(u => u.Id == request.UserId);

            if (user == null)
            {
                return NotFound("User not found");
            }

            // Create critical notification record
            var notification = new Notification
            {
                Id = Guid.NewGuid(),
                UserId = request.UserId,
                Type = NotificationType.Alert,
                Title = $"EMERGENCY: {request.AlertType}",
                Message = request.Message,
                IsCritical = true,
                CreatedAt = DateTime.UtcNow
            };

            _context.Notifications.Add(notification);
            await _context.SaveChangesAsync();

            // Trigger emergency workflow in n8n
            var success = await _n8nService.SendEmergencyAlertAsync(request);

            if (success)
            {
                notification.SentAt = DateTime.UtcNow;
                await _context.SaveChangesAsync();
                
                _logger.LogWarning($"Emergency alert sent for user {request.UserId}: {request.AlertType}");
                return Ok(new { notificationId = notification.Id, emergencyAlertSent = true });
            }
            else
            {
                return StatusCode(500, "Failed to send emergency alert");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error sending emergency alert");
            return StatusCode(500, "Internal server error");
        }
    }

    /// <summary>
    /// Send routine reminder through n8n
    /// </summary>
    [HttpPost("routine-reminder")]
    public async Task<IActionResult> SendRoutineReminder([FromBody] RoutineReminderRequest request)
    {
        try
        {
            var user = await _context.Users
                .Include(u => u.Profile)
                .FirstOrDefaultAsync(u => u.Id == request.UserId);

            if (user == null)
            {
                return NotFound("User not found");
            }

            // Create notification record
            var notification = new Notification
            {
                Id = Guid.NewGuid(),
                UserId = request.UserId,
                Type = NotificationType.Information,
                Title = request.Title,
                Message = request.Description,
                ScheduledFor = request.ScheduledTime,
                CreatedAt = DateTime.UtcNow
            };

            _context.Notifications.Add(notification);
            await _context.SaveChangesAsync();

            // Trigger routine reminder workflow
            request.Id = notification.Id;
            var success = await _n8nService.SendRoutineReminderAsync(request);

            if (success)
            {
                return Ok(new { notificationId = notification.Id, reminderScheduled = true });
            }
            else
            {
                return StatusCode(500, "Failed to schedule routine reminder");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error sending routine reminder");
            return StatusCode(500, "Internal server error");
        }
    }

    /// <summary>
    /// Send progress update to parents/caregivers
    /// </summary>
    [HttpPost("progress-update")]
    public async Task<IActionResult> SendProgressUpdate([FromBody] ProgressUpdateRequest request)
    {
        try
        {
            var user = await _context.Users
                .Include(u => u.Profile)
                .Include(u => u.ParentGuardian)
                .FirstOrDefaultAsync(u => u.Id == request.UserId);

            if (user == null)
            {
                return NotFound("User not found");
            }

            // Add parent emails if not provided
            if (request.ParentEmails.Count == 0 && user.ParentGuardian != null)
            {
                request.ParentEmails.Add(user.ParentGuardian.Email);
            }

            // Create notification record
            var notification = new Notification
            {
                Id = Guid.NewGuid(),
                UserId = request.UserId,
                Type = NotificationType.Message,
                Title = $"Progress Update - {request.ReportType}",
                Message = "Progress report has been generated and sent to caregivers",
                CreatedAt = DateTime.UtcNow
            };

            _context.Notifications.Add(notification);
            await _context.SaveChangesAsync();

            // Trigger progress update workflow
            request.Id = notification.Id;
            var success = await _n8nService.SendProgressUpdateAsync(request);

            if (success)
            {
                notification.SentAt = DateTime.UtcNow;
                await _context.SaveChangesAsync();
                return Ok(new { notificationId = notification.Id, progressUpdateSent = true });
            }
            else
            {
                return StatusCode(500, "Failed to send progress update");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error sending progress update");
            return StatusCode(500, "Internal server error");
        }
    }

    /// <summary>
    /// Webhook endpoint for n8n to update notification status
    /// </summary>
    [HttpPost("webhook/status-update")]
    public async Task<IActionResult> UpdateNotificationStatus([FromBody] NotificationStatusUpdate update)
    {
        try
        {
            var notification = await _context.Notifications
                .FirstOrDefaultAsync(n => n.Id == update.NotificationId);

            if (notification == null)
            {
                return NotFound("Notification not found");
            }

            // Update notification based on n8n workflow result
            if (update.Status == "success" && notification.SentAt == null)
            {
                notification.SentAt = DateTime.UtcNow;
            }

            // Store additional data from n8n workflow
            if (!string.IsNullOrEmpty(update.WorkflowData))
            {
                notification.Data = update.WorkflowData;
            }

            await _context.SaveChangesAsync();

            return Ok(new { updated = true });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating notification status");
            return StatusCode(500, "Internal server error");
        }
    }

    /// <summary>
    /// Mark notification as read
    /// </summary>
    [HttpPut("{notificationId}/read")]
    public async Task<IActionResult> MarkAsRead(Guid notificationId)
    {
        var notification = await _context.Notifications
            .FirstOrDefaultAsync(n => n.Id == notificationId);

        if (notification == null)
        {
            return NotFound();
        }

        notification.IsRead = true;
        await _context.SaveChangesAsync();

        return Ok();
    }

    private List<string> GetDefaultChannels(User user)
    {
        var channels = new List<string>();

        switch (user.PreferredCommunicationMethod)
        {
            case CommunicationMethod.Email:
                channels.Add("email");
                break;
            case CommunicationMethod.SMS:
                channels.Add("sms");
                break;
            case CommunicationMethod.InApp:
                channels.Add("push");
                break;
            case CommunicationMethod.Push:
                channels.Add("push");
                break;
        }

        // Always include in-app notifications
        if (!channels.Contains("push"))
        {
            channels.Add("push");
        }

        return channels;
    }
}

// Request Models
public class SendNotificationRequest
{
    public Guid UserId { get; set; }
    public NotificationType Type { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public string? Data { get; set; }
    public bool IsCritical { get; set; }
    public DateTime? ScheduledFor { get; set; }
    public List<string>? Channels { get; set; }
}

public class NotificationStatusUpdate
{
    public Guid NotificationId { get; set; }
    public string Status { get; set; } = string.Empty; // success, error, pending
    public string? WorkflowData { get; set; }
    public string? Error { get; set; }
}
