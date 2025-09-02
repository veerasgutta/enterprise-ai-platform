using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EnterprisePlatformApi.Models
{
    /// <summary>
    /// Enterprise notification system
    /// </summary>
    public class Notification
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        
        [Required]
        public string Title { get; set; } = string.Empty;
        
        [Required]
        public string Message { get; set; } = string.Empty;
        
        public NotificationType Type { get; set; } = NotificationType.Information;
        
        public NotificationPriority Priority { get; set; } = NotificationPriority.Normal;
        
        public Guid UserId { get; set; }
        
        [ForeignKey("UserId")]
        public virtual User User { get; set; } = null!;
        
        public ExperienceLevel? ExperienceLevel { get; set; }
        
        public string? ActionUrl { get; set; }
        
        public string? ActionText { get; set; }
        
        public bool IsRead { get; set; } = false;
        
        public DateTime? ReadAt { get; set; }
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        
        public DateTime? ExpiresAt { get; set; }
        
        public string? RelatedEntityType { get; set; }
        
        public Guid? RelatedEntityId { get; set; }
        
        public string? Metadata { get; set; }
        
        public bool IsArchived { get; set; } = false;
    }

    /// <summary>
    /// Business event for tracking and analytics
    /// </summary>
    public class Event
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        
        [Required]
        public string Title { get; set; } = string.Empty;
        
        public string? Description { get; set; }
        
        public EventType Type { get; set; } = EventType.Meeting;
        
        public ExperienceLevel ExperienceLevel { get; set; } = ExperienceLevel.Entry;
        
        public DateTime StartDateTime { get; set; }
        
        public DateTime EndDateTime { get; set; }
        
        public string? Location { get; set; }
        
        public bool IsVirtual { get; set; } = false;
        
        public string? VirtualMeetingUrl { get; set; }
        
        public Guid? OrganizerId { get; set; }
        
        [ForeignKey("OrganizerId")]
        public virtual User? Organizer { get; set; }
        
        public int MaxAttendees { get; set; } = 0; // 0 = unlimited
        
        public int RegisteredCount { get; set; } = 0;
        
        public bool RequiresRegistration { get; set; } = false;
        
        public decimal? Cost { get; set; }
        
        public string? Tags { get; set; }
        
        public bool IsPublic { get; set; } = true;
        
        public bool IsCancelled { get; set; } = false;
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    }

    public enum NotificationType
    {
        Information,
        Success,
        Warning,
        Error,
        Alert,
        Reminder,
        Task,
        Message,
        System,
        Security,
        Performance,
        Update,
        Approval,
        Escalation
    }

    public enum NotificationPriority
    {
        Low,
        Normal,
        High,
        Critical,
        Urgent
    }

    public enum EventType
    {
        Meeting,
        Training,
        Workshop,
        Conference,
        Webinar,
        TeamBuilding,
        Review,
        Planning,
        Strategy,
        Presentation,
        Interview,
        Onboarding,
        Networking,
        Social,
        Milestone,
        Deadline,
        Launch,
        Demo
    }
}
