using System.ComponentModel.DataAnnotations;
using System.Xml.Serialization;

namespace EnterprisePlatformApi.Models
{
    /// <summary>
    /// SEC N-CEN Form C.22 Liquidity Classification Services models
    /// Based on SEC XML Technical Specifications Version 3.1
    /// </summary>
    public class NCenC22LiquidityClassification
    {
        [XmlElement("liquidityClassificationService")]
        public List<LiquidityClassificationService> LiquidityClassificationServices { get; set; } = new();
    }

    public class LiquidityClassificationService
    {
        [XmlElement("liquidityName")]
        [StringLength(150, ErrorMessage = "Liquidity name cannot exceed 150 characters")]
        public string LiquidityName { get; set; } = string.Empty;

        [XmlElement("liquidityLei")]
        [RegularExpression(@"^[A-Z0-9]{20}$|^N/A$", ErrorMessage = "LEI must be exactly 20 alphanumeric characters or 'N/A'")]
        public string? LiquidityLei { get; set; }

        [XmlElement("liquidityRssdId")]
        [RegularExpression(@"^\d{1,10}$", ErrorMessage = "RSSD ID must be 1-10 numeric characters")]
        public string? LiquidityRssdId { get; set; }

        [XmlElement("liquidityOther")]
        [StringLength(100, ErrorMessage = "Liquidity other cannot exceed 100 characters")]
        public string? LiquidityOther { get; set; }

        [XmlElement("otherDesc")]
        [StringLength(500, ErrorMessage = "Other description cannot exceed 500 characters")]
        public string? OtherDescription { get; set; }

        [XmlElement("liquidityStateCountry")]
        [Required(ErrorMessage = "State/Country information is required")]
        public LiquidityStateCountry StateCountry { get; set; } = new();

        [XmlElement("isAffiliatedPerson")]
        [Required(ErrorMessage = "Affiliated person status is required")]
        [RegularExpression(@"^[YN]$", ErrorMessage = "Must be 'Y' or 'N'")]
        public string IsAffiliatedPerson { get; set; } = string.Empty;

        [XmlElement("assetClassType")]
        [Required(ErrorMessage = "Asset class type is required")]
        public AssetClassType AssetClassType { get; set; }

        [XmlElement("otherAssetDesc")]
        [StringLength(500, ErrorMessage = "Other asset description cannot exceed 500 characters")]
        public string? OtherAssetDescription { get; set; }

        [XmlElement("isLiquidityHiredTerminated")]
        [RegularExpression(@"^[YN]$", ErrorMessage = "Must be 'Y' or 'N'")]
        public string? IsLiquidityHiredTerminated { get; set; }
    }

    public class LiquidityStateCountry
    {
        [XmlAttribute("liquidityState")]
        [RegularExpression(@"^[A-Z]{2}$", ErrorMessage = "State must be 2-character ISO code")]
        public string? LiquidityState { get; set; }

        [XmlAttribute("liquidityCountry")]
        [RegularExpression(@"^[A-Z]{2}$", ErrorMessage = "Country must be 2-character ISO code")]
        public string? LiquidityCountry { get; set; }

        [XmlText]
        [RegularExpression(@"^[A-Z]{2}$", ErrorMessage = "Foreign country must be 2-character ISO code")]
        public string? ForeignCountry { get; set; }
    }

    public enum AssetClassType
    {
        [XmlEnum("Cash")]
        Cash,
        
        [XmlEnum("CashEquivalents")]
        CashEquivalents,
        
        [XmlEnum("USGovernment")]
        USGovernment,
        
        [XmlEnum("USAgency")]
        USAgency,
        
        [XmlEnum("Municipal")]
        Municipal,
        
        [XmlEnum("Foreign")]
        Foreign,
        
        [XmlEnum("FixedIncome")]
        FixedIncome,
        
        [XmlEnum("Equity")]
        Equity,
        
        [XmlEnum("Derivatives")]
        Derivatives,
        
        [XmlEnum("Other")]
        Other
    }

    /// <summary>
    /// Validation result for SEC compliance
    /// </summary>
    public class SecValidationResult
    {
        public bool IsValid { get; set; }
        public List<string> Errors { get; set; } = new();
        public List<string> Warnings { get; set; } = new();
        public string? ValidatedXml { get; set; }
        public DateTime ValidationTimestamp { get; set; } = DateTime.UtcNow;
    }

    /// <summary>
    /// SEC Filing Context for AI-powered compliance
    /// </summary>
    public class SecFilingContext
    {
        public string FilingType { get; set; } = string.Empty;
        public string FormVersion { get; set; } = string.Empty;
        public DateTime FilingDate { get; set; }
        public string FilerCik { get; set; } = string.Empty;
        public string SubmissionType { get; set; } = string.Empty;
        public Dictionary<string, object> FormData { get; set; } = new();
        public List<string> ValidationErrors { get; set; } = new();
        public string AiAnalysisNotes { get; set; } = string.Empty;
    }

    /// <summary>
    /// Business context information for enterprise AI content validation
    /// </summary>
    public class BusinessContext
    {
        public string? Department { get; set; }
        public string? Industry { get; set; }
        public string? BusinessFunction { get; set; }
        public List<string> PreferredMethodologies { get; set; } = new();
        public string? ComplianceLevel { get; set; }
        public Dictionary<string, string> CustomSettings { get; set; } = new();
    }

    /// <summary>
    /// AI content validation request with business context
    /// </summary>
    public class AIContentRequest
    {
        public string Content { get; set; } = string.Empty;
        public AIContentType ContentType { get; set; }
        public ExperienceLevel? ExperienceLevel { get; set; }
        public CommunicationLevel? CommunicationLevel { get; set; }
        public BusinessContext? BusinessContext { get; set; }
        public string? UserId { get; set; }
    }

    public enum AIContentType
    {
        General,
        Educational,
        Business,
        Technical,
        Strategic
    }

    public enum CommunicationLevel
    {
        Simple,
        Standard,
        Advanced,
        Expert
    }

    public enum ExperienceLevel
    {
        Entry,
        Junior,
        Mid,
        Senior,
        Principal,
        Executive
    }
}
