using Microsoft.EntityFrameworkCore;
using EnterprisePlatformApi.Models;
using System.Text.Json;

namespace EnterprisePlatformApi.Data;

public class EnterprisePlatformDbContext : DbContext
{
    public EnterprisePlatformDbContext(DbContextOptions<EnterprisePlatformDbContext> options) : base(options)
    {
    }

    public DbSet<User> Users { get; set; }
    public DbSet<UserProfile> UserProfiles { get; set; }
    public DbSet<ContentItem> ContentItems { get; set; }
    public DbSet<ContentCategory> ContentCategories { get; set; }
    public DbSet<Notification> Notifications { get; set; }
    public DbSet<Event> Events { get; set; }
    public DbSet<WorkflowOutboxEvent> WorkflowOutbox { get; set; } // Outbox

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // User configuration
        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.Email).IsUnique();
            entity.HasIndex(e => e.ExperienceLevel);
            entity.HasIndex(e => e.Role);
            
            entity.Property(e => e.Role)
                .HasConversion<string>();
            
            entity.Property(e => e.ExperienceLevel)
                .HasConversion<string>();
            
            entity.Property(e => e.PreferredCommunicationMethod)
                .HasConversion<string>();

            // Self-referencing relationship for parent-guardian
            entity.HasOne(e => e.ParentGuardian)
                .WithMany()
                .HasForeignKey(e => e.ParentGuardianId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        // UserProfile configuration
        modelBuilder.Entity<UserProfile>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.UserId).IsUnique();

            entity.HasOne(e => e.User)
                .WithOne(e => e.Profile)
                .HasForeignKey<UserProfile>(e => e.UserId)
                .OnDelete(DeleteBehavior.Cascade);

            // JSON column configurations
            entity.Property(e => e.BusinessContext)
                .HasConversion(
                    v => JsonSerializer.Serialize(v, (JsonSerializerOptions?)null),
                    v => JsonSerializer.Deserialize<BusinessContext>(v, (JsonSerializerOptions?)null));

            entity.Property(e => e.CommunicationPreferences)
                .HasConversion(
                    v => JsonSerializer.Serialize(v, (JsonSerializerOptions?)null),
                    v => JsonSerializer.Deserialize<CommunicationPreferences>(v, (JsonSerializerOptions?)null));

            entity.Property(e => e.EmergencyContact)
                .HasConversion(
                    v => JsonSerializer.Serialize(v, (JsonSerializerOptions?)null),
                    v => JsonSerializer.Deserialize<EmergencyContact>(v, (JsonSerializerOptions?)null));

            entity.Property(e => e.PrivacySettings)
                .HasConversion(
                    v => JsonSerializer.Serialize(v, (JsonSerializerOptions?)null),
                    v => JsonSerializer.Deserialize<PrivacySettings>(v, (JsonSerializerOptions?)null));
        });

        // ContentCategory configuration
        modelBuilder.Entity<ContentCategory>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.Name);
            entity.HasIndex(e => e.ExperienceLevel);

            entity.Property(e => e.ExperienceLevel)
                .HasConversion<string>();

            // Self-referencing relationship for parent categories
            entity.HasOne(e => e.ParentCategory)
                .WithMany(e => e.SubCategories)
                .HasForeignKey(e => e.ParentCategoryId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        // ContentItem configuration
        modelBuilder.Entity<ContentItem>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.Slug).IsUnique();
            entity.HasIndex(e => new { e.CategoryId, e.Status });
            entity.HasIndex(e => e.CreatedAt);

            entity.Property(e => e.Status)
                .HasConversion<string>();

            entity.Property(e => e.ContentType)
                .HasConversion<string>();

            entity.Property(e => e.Keywords)
                .HasConversion(
                    v => JsonSerializer.Serialize(v, (JsonSerializerOptions?)null),
                    v => JsonSerializer.Deserialize<List<string>>(v, (JsonSerializerOptions?)null) ?? new List<string>());

            entity.HasOne(e => e.Category)
                .WithMany(e => e.ContentItems)
                .HasForeignKey(e => e.CategoryId)
                .OnDelete(DeleteBehavior.Restrict);

            entity.HasOne(e => e.Author)
                .WithMany(e => e.AuthoredContent)
                .HasForeignKey(e => e.AuthorId)
                .OnDelete(DeleteBehavior.Restrict);

            entity.HasOne(e => e.Approver)
                .WithMany()
                .HasForeignKey(e => e.ApprovedBy)
                .OnDelete(DeleteBehavior.SetNull);
        });

        // Notification configuration
        modelBuilder.Entity<Notification>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => new { e.UserId, e.IsRead });
            entity.HasIndex(e => e.CreatedAt);

            entity.Property(e => e.Type)
                .HasConversion<string>();

            entity.HasOne(e => e.User)
                .WithMany(e => e.Notifications)
                .HasForeignKey(e => e.UserId)
                .OnDelete(DeleteBehavior.Cascade);
        });

        // Event configuration
        modelBuilder.Entity<Event>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => new { e.ExperienceLevel, e.StartDateTime });
            entity.HasIndex(e => e.StartDateTime);

            entity.Property(e => e.EventType)
                .HasConversion<string>();

            entity.Property(e => e.ExperienceLevel)
                .HasConversion<string>();

            entity.Property(e => e.Cost)
                .HasPrecision(10, 2);

            entity.HasOne(e => e.Organizer)
                .WithMany()
                .HasForeignKey(e => e.OrganizerUserId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        // Outbox configuration
        modelBuilder.Entity<WorkflowOutboxEvent>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => new { e.Status, e.CreatedAt });
            entity.HasIndex(e => e.UserId);
            entity.Property(e => e.Status).HasConversion<string>();
        });

        // Seed data
        SeedData(modelBuilder);
    }

    private void SeedData(ModelBuilder modelBuilder)
    {
        // Seed content categories
        var categories = new List<ContentCategory>
        {
            new ContentCategory { Id = Guid.NewGuid(), Name = "Onboarding Support", ExperienceLevel = ExperienceLevel.Entry, Description = "Resources for new employee onboarding", SortOrder = 1 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Training Resources", ExperienceLevel = ExperienceLevel.Entry, Description = "Training and development resources", SortOrder = 2 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Team Collaboration", ExperienceLevel = ExperienceLevel.Junior, Description = "Building professional networks", SortOrder = 1 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Career Planning", ExperienceLevel = ExperienceLevel.Junior, Description = "Career planning and development", SortOrder = 2 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Leadership Skills", ExperienceLevel = ExperienceLevel.Mid, Description = "Developing leadership skills", SortOrder = 1 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Career Advancement", ExperienceLevel = ExperienceLevel.Mid, Description = "Planning for career advancement", SortOrder = 2 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Job Performance", ExperienceLevel = ExperienceLevel.Senior, Description = "Performance optimization and workplace skills", SortOrder = 1 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Work-Life Balance", ExperienceLevel = ExperienceLevel.Senior, Description = "Work-life balance and autonomy", SortOrder = 2 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Professional Development", ExperienceLevel = ExperienceLevel.Principal, Description = "Professional development and growth", SortOrder = 1 },
            new ContentCategory { Id = Guid.NewGuid(), Name = "Professional Networks", ExperienceLevel = ExperienceLevel.Principal, Description = "Building and maintaining Professional Networks", SortOrder = 2 }
        };

        modelBuilder.Entity<ContentCategory>().HasData(categories);
    }
}
