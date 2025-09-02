using System.Text;
using System.Text.RegularExpressions;

namespace EnterprisePlatformApi.Services;

/// <summary>
/// Automatically updates PROJECT-STATUS.md with latest development progress
/// </summary>
public class ProjectStatusUpdaterService
{
    private readonly ILogger<ProjectStatusUpdaterService> _logger;
    private readonly string _statusFilePath;

    public ProjectStatusUpdaterService(ILogger<ProjectStatusUpdaterService> logger)
    {
        _logger = logger;
        _statusFilePath = Path.Combine(Directory.GetCurrentDirectory(), "..", "PROJECT-STATUS.md");
    }

    /// <summary>
    /// Updates project status with completed feature
    /// </summary>
    public async Task UpdateCompletedFeatureAsync(string category, string featureName, string description)
    {
        _logger.LogInformation($"Updating status: {category} - {featureName}");
        
        try
        {
            var content = await File.ReadAllTextAsync(_statusFilePath);
            var updatedContent = AddCompletedFeature(content, category, featureName, description);
            await File.WriteAllTextAsync(_statusFilePath, updatedContent);
            
            _logger.LogInformation("Project status updated successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to update project status");
        }
    }

    /// <summary>
    /// Updates project progress percentage
    /// </summary>
    public async Task UpdateProgressAsync(int progressPercentage)
    {
        try
        {
            var content = await File.ReadAllTextAsync(_statusFilePath);
            var updatedContent = UpdateProgressPercentage(content, progressPercentage);
            await File.WriteAllTextAsync(_statusFilePath, updatedContent);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to update progress percentage");
        }
    }

    /// <summary>
    /// Adds a new priority to the next steps
    /// </summary>
    public async Task AddNextPriorityAsync(string priority, string description)
    {
        try
        {
            var content = await File.ReadAllTextAsync(_statusFilePath);
            var updatedContent = AddNextPriority(content, priority, description);
            await File.WriteAllTextAsync(_statusFilePath, updatedContent);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to add next priority");
        }
    }

    /// <summary>
    /// Updates the last updated timestamp
    /// </summary>
    public async Task UpdateTimestampAsync()
    {
        try
        {
            var content = await File.ReadAllTextAsync(_statusFilePath);
            var updatedContent = UpdateLastUpdatedDate(content);
            await File.WriteAllTextAsync(_statusFilePath, updatedContent);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to update timestamp");
        }
    }

    /// <summary>
    /// Generates a comprehensive status summary for conversation context
    /// </summary>
    public async Task<string> GenerateContextSummaryAsync()
    {
        try
        {
            var content = await File.ReadAllTextAsync(_statusFilePath);
            return ExtractKeyInformation(content);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to generate context summary");
            return "Unable to load project status";
        }
    }

    /// <summary>
    /// Records autonomous service build completion
    /// </summary>
    public async Task RecordAutonomousServiceAsync(string serviceName, bool success, string details)
    {
        var status = success ? "✅" : "❌";
        var feature = $"{status} **{serviceName}Service** - {details}";
        await UpdateCompletedFeatureAsync("Autonomous Services", serviceName, feature);
    }

    #region Private Methods

    private string AddCompletedFeature(string content, string category, string featureName, string description)
    {
        // Find the completed features section
        var pattern = @"(## ✅ Completed Features.*?)(## 🚧 In Progress)";
        var match = Regex.Match(content, pattern, RegexOptions.Singleline);
        
        if (match.Success)
        {
            var completedSection = match.Groups[1].Value;
            var newFeature = $"- ✅ **{featureName}** - {description}\n";
            
            // Add under appropriate category or create new category
            if (completedSection.Contains($"### **{category}**"))
            {
                var categoryPattern = $@"(### \*\*{Regex.Escape(category)}\*\*.*?)(\n### |\n## )";
                var categoryMatch = Regex.Match(completedSection, categoryPattern, RegexOptions.Singleline);
                
                if (categoryMatch.Success)
                {
                    var updatedCategory = categoryMatch.Groups[1].Value + newFeature;
                    completedSection = completedSection.Replace(categoryMatch.Groups[1].Value, updatedCategory);
                }
            }
            else
            {
                // Add new category
                var newCategory = $"\n### **{category}**\n{newFeature}";
                completedSection += newCategory;
            }
            
            return content.Replace(match.Groups[1].Value, completedSection);
        }
        
        return content;
    }

    private string UpdateProgressPercentage(string content, int percentage)
    {
        var pattern = @"(\*\*Overall Progress\*\*: )\d+(%.*?)";
        return Regex.Replace(content, pattern, $"$1{percentage}$2");
    }

    private string UpdateLastUpdatedDate(string content)
    {
        var currentDate = DateTime.Now.ToString("MMMM dd, yyyy");
        var pattern = @"(\*\*Last Updated\*\*: ).*?(\n)";
        return Regex.Replace(content, pattern, $"$1{currentDate}$2");
    }

    private string AddNextPriority(string content, string priority, string description)
    {
        var pattern = @"(### \*\*Immediate \(Next 1-2 Sessions\)\*\*\n)(.*?)(\n### )";
        var match = Regex.Match(content, pattern, RegexOptions.Singleline);
        
        if (match.Success)
        {
            var newPriority = $"1. **{priority}** - {description}\n";
            var updatedSection = match.Groups[1].Value + newPriority + match.Groups[2].Value;
            return content.Replace(match.Groups[1].Value + match.Groups[2].Value, updatedSection);
        }
        
        return content;
    }

    private string ExtractKeyInformation(string content)
    {
        var summary = new StringBuilder();
        
        // Extract current phase and progress
        var phaseMatch = Regex.Match(content, @"\*\*Current Phase\*\*: (.*?)\n");
        var progressMatch = Regex.Match(content, @"\*\*Overall Progress\*\*: (.*?)\n");
        
        if (phaseMatch.Success && progressMatch.Success)
        {
            summary.AppendLine($"🎯 Current Focus: {phaseMatch.Groups[1].Value}");
            summary.AppendLine($"📊 Progress: {progressMatch.Groups[1].Value}");
            summary.AppendLine();
        }

        // Extract recent completed features (last 5)
        var completedPattern = @"- ✅ \*\*(.*?)\*\* - (.*?)(?:\n|$)";
        var completedMatches = Regex.Matches(content, completedPattern);
        
        if (completedMatches.Count > 0)
        {
            summary.AppendLine("🎉 Recent Completions:");
            foreach (Match match in completedMatches.Cast<Match>().TakeLast(5))
            {
                summary.AppendLine($"  ✅ {match.Groups[1].Value}");
            }
            summary.AppendLine();
        }

        // Extract immediate priorities
        var priorityPattern = @"### \*\*Immediate \(Next 1-2 Sessions\)\*\*\n(.*?)(?:\n### |$)";
        var priorityMatch = Regex.Match(content, priorityPattern, RegexOptions.Singleline);
        
        if (priorityMatch.Success)
        {
            summary.AppendLine("🎯 Next Priorities:");
            var priorities = Regex.Matches(priorityMatch.Groups[1].Value, @"\d+\. \*\*(.*?)\*\* - (.*?)(?:\n|$)");
            foreach (Match priority in priorities.Cast<Match>().Take(3))
            {
                summary.AppendLine($"  • {priority.Groups[1].Value}");
            }
        }

        return summary.ToString();
    }

    #endregion
}

/// <summary>
/// Extension methods for easy status updates
/// </summary>
public static class ProjectStatusExtensions
{
    public static async Task RecordFeatureCompletion(this ProjectStatusUpdaterService statusUpdater, 
        string featureName, string category = "Development", string description = "Implementation completed")
    {
        await statusUpdater.UpdateCompletedFeatureAsync(category, featureName, description);
        await statusUpdater.UpdateTimestampAsync();
    }

    public static async Task RecordProgressMilestone(this ProjectStatusUpdaterService statusUpdater, 
        int newProgress, string milestone)
    {
        await statusUpdater.UpdateProgressAsync(newProgress);
        await statusUpdater.AddNextPriorityAsync(milestone, "Continue development momentum");
        await statusUpdater.UpdateTimestampAsync();
    }
}
