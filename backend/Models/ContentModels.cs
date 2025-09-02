using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace EnterprisePlatformApi.Models
{
    /// <summary>
    /// Business content item
    /// </summary>
    public class ContentItem
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        
        [Required]
        public string Title { get; set; } = string.Empty;
        
        [Required]
        public string Content { get; set; } = string.Empty;
        
        public string? Summary { get; set; }
        
        public ContentType Type { get; set; } = ContentType.Article;
        
        public ExperienceLevel ExperienceLevel { get; set; } = ExperienceLevel.Entry;
        
        public string? Tags { get; set; }
        
        public string? MetaDescription { get; set; }
        
        public string? FeaturedImageUrl { get; set; }
        
        public Guid? CategoryId { get; set; }
        
        [ForeignKey("CategoryId")]
        public virtual ContentCategory? Category { get; set; }
        
        public Guid AuthorId { get; set; }
        
        [ForeignKey("AuthorId")]
        public virtual User Author { get; set; } = null!;
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
        
        public bool IsPublished { get; set; } = false;
        
        public DateTime? PublishedAt { get; set; }
        
        public int ViewCount { get; set; } = 0;
        
        public bool IsFeatured { get; set; } = false;
        
        public string? ExternalUrl { get; set; }
        
        public decimal? Price { get; set; }
        
        public bool IsArchived { get; set; } = false;
    }

    /// <summary>
    /// Content category for business organization
    /// </summary>
    public class ContentCategory
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        
        [Required]
        public string Name { get; set; } = string.Empty;
        
        public string? Description { get; set; }
        
        public ExperienceLevel ExperienceLevel { get; set; } = ExperienceLevel.Entry;
        
        public string? Icon { get; set; }
        
        public string? Color { get; set; }
        
        public int SortOrder { get; set; } = 0;
        
        public bool IsActive { get; set; } = true;
        
        public Guid? ParentCategoryId { get; set; }
        
        [ForeignKey("ParentCategoryId")]
        public virtual ContentCategory? ParentCategory { get; set; }
        
        public virtual ICollection<ContentCategory> SubCategories { get; set; } = new List<ContentCategory>();
        
        public virtual ICollection<ContentItem> ContentItems { get; set; } = new List<ContentItem>();
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }

    public enum ContentType
    {
        Article,
        Guide,
        Tutorial,
        Video,
        Webinar,
        Podcast,
        Document,
        Template,
        Tool,
        Course,
        Workshop,
        Assessment,
        Report,
        Analysis,
        Strategy,
        Policy,
        Procedure,
        Checklist
    }
}
