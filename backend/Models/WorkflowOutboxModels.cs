using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EnterprisePlatformApi.Models;

public enum OutboxStatus
{
    Pending,
    Processing,
    Succeeded,
    Failed
}

public class WorkflowOutboxEvent
{
    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();

    [Required]
    [MaxLength(128)]
    public string Type { get; set; } = string.Empty; // e.g., "chat.reply", "notification.create"

    [Required]
    public string Payload { get; set; } = string.Empty; // JSON payload

    public Guid? UserId { get; set; }

    [MaxLength(128)]
    public string? CorrelationId { get; set; } // e.g., sessionId, requestId

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public OutboxStatus Status { get; set; } = OutboxStatus.Pending;

    public int Attempts { get; set; } = 0;

    public DateTime? ProcessedAt { get; set; }

    public string? LastError { get; set; }
}
