using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EnterprisePlatformApi.Models
{
    /// <summary>
    /// Enterprise user account
    /// </summary>
    public class User
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        
        [Required]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;
        
        [Required]
        public string FirstName { get; set; } = string.Empty;
        
        [Required]
        public string LastName { get; set; } = string.Empty;
        
        public string? DisplayName { get; set; }
        
        public UserRole Role { get; set; } = UserRole.Employee;
        
        public ExperienceLevel ExperienceLevel { get; set; } = ExperienceLevel.Entry;
        
        public CommunicationLevel PreferredCommunicationMethod { get; set; } = CommunicationLevel.Standard;
        
        public string? Department { get; set; }
        
        public string? JobTitle { get; set; }
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        
        public DateTime? LastLoginAt { get; set; }
        
        public bool IsActive { get; set; } = true;
        
        // Supervisor/Manager relationship
        public Guid? ParentGuardianId { get; set; }
        
        [ForeignKey("ParentGuardianId")]
        public virtual User? ParentGuardian { get; set; }
        
        // Navigation properties
        public virtual UserProfile? UserProfile { get; set; }
        public virtual ICollection<Notification> Notifications { get; set; } = new List<Notification>();
    }

    /// <summary>
    /// Extended user profile with business preferences
    /// </summary>
    public class UserProfile
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        
        [Required]
        public Guid UserId { get; set; }
        
        [ForeignKey("UserId")]
        public virtual User User { get; set; } = null!;
        
        public string? Biography { get; set; }
        
        public string? ProfileImageUrl { get; set; }
        
        public string? TimeZone { get; set; }
        
        public string? Language { get; set; } = "en";
        
        public ExperienceLevel ExperienceLevel { get; set; } = ExperienceLevel.Entry;
        
        public CommunicationLevel PreferredCommunicationLevel { get; set; } = CommunicationLevel.Standard;
        
        public string? BusinessContext { get; set; }
        
        // Business preferences as JSON
        public string? Preferences { get; set; }
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    }

    public enum UserRole
    {
        Employee,
        Manager,
        Director,
        VicePresident,
        President,
        CEO,
        Administrator,
        Consultant,
        Contractor
    }
}
