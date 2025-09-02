using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;

namespace EnterprisePlatformApi.Services;

/// <summary>
/// Multi-project workspace status management service
/// </summary>
public class WorkspaceStatusManager
{
    private readonly ILogger<WorkspaceStatusManager> _logger;
    private readonly ProjectStatusUpdaterService _projectStatusUpdater;
    private readonly string _workspaceRoot;
    private readonly Dictionary<string, ProjectInfo> _projects;

    public WorkspaceStatusManager(ILogger<WorkspaceStatusManager> logger, ProjectStatusUpdaterService projectStatusUpdater)
    {
        _logger = logger;
        _projectStatusUpdater = projectStatusUpdater;
        _workspaceRoot = Directory.GetCurrentDirectory();
        while (!Directory.Exists(Path.Combine(_workspaceRoot, ".git")) && 
               Directory.GetParent(_workspaceRoot) != null)
        {
            _workspaceRoot = Directory.GetParent(_workspaceRoot)!.FullName;
        }
        
        _projects = InitializeProjects();
    }

    /// <summary>
    /// Get status summary for all projects in workspace
    /// </summary>
    public async Task<WorkspaceStatusSummary> GetWorkspaceStatusAsync()
    {
        var summary = new WorkspaceStatusSummary
        {
            LastUpdated = DateTime.Now,
            Projects = new List<ProjectStatusSummary>()
        };

        foreach (var project in _projects.Values)
        {
            var projectSummary = await GetProjectSummaryAsync(project);
            summary.Projects.Add(projectSummary);
        }

        summary.OverallProgress = CalculateOverallProgress(summary.Projects);
        return summary;
    }



    /// <summary>
    /// Update status for specific project
    /// </summary>
    public async Task UpdateProjectStatusAsync(string projectName, string feature, string category, string description)
    {
        if (!_projects.ContainsKey(projectName))
        {
            _logger.LogWarning($"Project '{projectName}' not found in workspace");
            return;
        }

        var project = _projects[projectName];
        var statusFile = Path.Combine(project.Path, "PROJECT-STATUS.md");
        
        if (!File.Exists(statusFile))
        {
            await CreateProjectStatusFileAsync(project);
        }

        // Update individual project status
        await _projectStatusUpdater.UpdateCompletedFeatureAsync(category, feature, description);

        // Update workspace overview
        await UpdateWorkspaceOverviewAsync();
    }

    /// <summary>
    /// Create new project in workspace
    /// </summary>
    public async Task AddProjectAsync(string projectName, string path, string description, ProjectType type)
    {
        var projectInfo = new ProjectInfo
        {
            Name = projectName,
            Path = Path.Combine(_workspaceRoot, path),
            Description = description,
            Type = type,
            CreatedAt = DateTime.Now
        };

        _projects[projectName] = projectInfo;
        
        // Create project directory and initial status file
        Directory.CreateDirectory(projectInfo.Path);
        await CreateProjectStatusFileAsync(projectInfo);
        
        // Update workspace overview
        await UpdateWorkspaceOverviewAsync();
        
        _logger.LogInformation($"Added new project: {projectName}");
    }

    /// <summary>
    /// Generate conversation context for specific project
    /// </summary>
    public async Task<string> GenerateProjectContextAsync(string projectName)
    {
        if (!_projects.ContainsKey(projectName))
        {
            return $"Project '{projectName}' not found in workspace.";
        }

        var project = _projects[projectName];
        var statusFile = Path.Combine(project.Path, "PROJECT-STATUS.md");
        
        if (!File.Exists(statusFile))
        {
            return $"No status file found for project '{projectName}'.";
        }

        var content = await File.ReadAllTextAsync(statusFile);
        return ExtractProjectContext(content, project);
    }

    /// <summary>
    /// Get cross-project dependencies and blockers
    /// </summary>
    public async Task<List<ProjectDependency>> GetProjectDependenciesAsync()
    {
        var dependencies = new List<ProjectDependency>();
        
        // Analyze each project for dependencies
        foreach (var project in _projects.Values)
        {
            var projectDeps = await AnalyzeProjectDependencies(project);
            dependencies.AddRange(projectDeps);
        }

        return dependencies;
    }

    #region Private Methods

    private Dictionary<string, ProjectInfo> InitializeProjects()
    {
        var projects = new Dictionary<string, ProjectInfo>();

        // Auto-detect projects based on directory structure
        var commonProjectMarkers = new[] { "package.json", "*.csproj", "requirements.txt", "Dockerfile" };
        
        foreach (var dir in Directory.GetDirectories(_workspaceRoot))
        {
            var dirName = Path.GetFileName(dir);
            if (dirName.StartsWith(".")) continue; // Skip hidden directories

            var hasProjectFiles = commonProjectMarkers.Any(pattern => 
                Directory.GetFiles(dir, pattern, SearchOption.TopDirectoryOnly).Any());

            if (hasProjectFiles)
            {
                var type = DetermineProjectType(dir);
                projects[dirName] = new ProjectInfo
                {
                    Name = dirName,
                    Path = dir,
                    Description = $"Auto-detected {type} project",
                    Type = type,
                    CreatedAt = Directory.GetCreationTime(dir)
                };
            }
        }

        return projects;
    }

    private ProjectType DetermineProjectType(string projectPath)
    {
        if (File.Exists(Path.Combine(projectPath, "package.json"))) return ProjectType.Frontend;
        if (Directory.GetFiles(projectPath, "*.csproj").Any()) return ProjectType.Backend;
        if (File.Exists(Path.Combine(projectPath, "requirements.txt"))) return ProjectType.PythonService;
        if (File.Exists(Path.Combine(projectPath, "docker-compose.yml"))) return ProjectType.Infrastructure;
        return ProjectType.Other;
    }

    private async Task<ProjectStatusSummary> GetProjectSummaryAsync(ProjectInfo project)
    {
        var statusFile = Path.Combine(project.Path, "PROJECT-STATUS.md");
        var summary = new ProjectStatusSummary
        {
            Name = project.Name,
            Type = project.Type,
            Path = project.Path,
            Progress = 0,
            Phase = "Not Started",
            LastActivity = project.CreatedAt
        };

        if (File.Exists(statusFile))
        {
            var content = await File.ReadAllTextAsync(statusFile);
            summary.Progress = ExtractProgress(content);
            summary.Phase = ExtractCurrentPhase(content);
            summary.LastActivity = File.GetLastWriteTime(statusFile);
        }

        return summary;
    }

    private async Task CreateProjectStatusFileAsync(ProjectInfo project)
    {
        var template = GenerateProjectStatusTemplate(project);
        var statusFile = Path.Combine(project.Path, "PROJECT-STATUS.md");
        await File.WriteAllTextAsync(statusFile, template);
    }

    private string GenerateProjectStatusTemplate(ProjectInfo project)
    {
        return $@"# {project.Name} - Project Status 📊

**Last Updated**: {DateTime.Now:MMMM dd, yyyy}  
**Project Type**: {project.Type}  
**Current Phase**: Planning  
**Overall Progress**: 0% Complete

## 🎯 Project Overview
{project.Description}

---

## ✅ Completed Features

### **Initial Setup**
- ✅ **Project Structure** - Basic directory structure created
- ✅ **Status Tracking** - Project status documentation initialized

---

## 🚧 In Progress

*No active development yet*

---

## 📋 Next Priorities

### **Immediate (Next 1-2 Sessions)**
1. **Define Requirements** - Establish project scope and objectives
2. **Architecture Planning** - Design system architecture
3. **Development Setup** - Configure development environment

---

## 🏗️ Architecture Status

*To be defined*

---

## 📖 Key Files

*To be documented as project develops*

---

*This document is part of the larger workspace managed by WORKSPACE-STATUS.md*
";
    }

    private int ExtractProgress(string content)
    {
        var match = Regex.Match(content, @"\*\*Overall Progress\*\*: (\d+)%");
        return match.Success ? int.Parse(match.Groups[1].Value) : 0;
    }

    private string ExtractCurrentPhase(string content)
    {
        var match = Regex.Match(content, @"\*\*Current Phase\*\*: (.+)");
        return match.Success ? match.Groups[1].Value.Trim() : "Unknown";
    }

    private int CalculateOverallProgress(List<ProjectStatusSummary> projects)
    {
        if (!projects.Any()) return 0;
        return (int)projects.Average(p => p.Progress);
    }

    private async Task UpdateWorkspaceOverviewAsync()
    {
        var workspaceFile = Path.Combine(_workspaceRoot, "WORKSPACE-STATUS.md");
        if (!File.Exists(workspaceFile)) return;

        var summary = await GetWorkspaceStatusAsync();
        // Update workspace file with current project statuses
        // Implementation would update project table and metrics
    }

    private string ExtractProjectContext(string content, ProjectInfo project)
    {
        var context = new StringBuilder();
        context.AppendLine($"📁 Project: {project.Name} ({project.Type})");
        
        // Extract key information similar to single-project version
        var phaseMatch = Regex.Match(content, @"\*\*Current Phase\*\*: (.+)");
        var progressMatch = Regex.Match(content, @"\*\*Overall Progress\*\*: (.+)");
        
        if (phaseMatch.Success && progressMatch.Success)
        {
            context.AppendLine($"🎯 Phase: {phaseMatch.Groups[1].Value}");
            context.AppendLine($"📊 Progress: {progressMatch.Groups[1].Value}");
        }

        return context.ToString();
    }

    private Task<List<ProjectDependency>> AnalyzeProjectDependencies(ProjectInfo project)
    {
        // Analyze project files to detect dependencies
        // This is a simplified version - real implementation would parse config files
        return Task.FromResult(new List<ProjectDependency>());
    }

    #endregion
}

// Supporting Models
public class ProjectInfo
{
    public string Name { get; set; } = string.Empty;
    public string Path { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public ProjectType Type { get; set; }
    public DateTime CreatedAt { get; set; }
}

public class WorkspaceStatusSummary
{
    public DateTime LastUpdated { get; set; }
    public int OverallProgress { get; set; }
    public List<ProjectStatusSummary> Projects { get; set; } = new();
}

public class ProjectStatusSummary
{
    public string Name { get; set; } = string.Empty;
    public ProjectType Type { get; set; }
    public string Path { get; set; } = string.Empty;
    public int Progress { get; set; }
    public string Phase { get; set; } = string.Empty;
    public DateTime LastActivity { get; set; }
}

public class ProjectDependency
{
    public string FromProject { get; set; } = string.Empty;
    public string ToProject { get; set; } = string.Empty;
    public string DependencyType { get; set; } = string.Empty;
    public bool IsBlocking { get; set; }
}

public enum ProjectType
{
    Frontend,
    Backend,
    PythonService,
    Infrastructure,
    Documentation,
    Other
}

// Additional extension methods for WorkspaceStatusManager
public static class WorkspaceStatusManagerExtensions
{
    /// <summary>
    /// Gets project priorities from status files
    /// </summary>
    public static async Task<List<string>> GetProjectPrioritiesAsync(
        this WorkspaceStatusManager manager, string projectName)
    {
        try
        {
            var projects = typeof(WorkspaceStatusManager)
                .GetField("_projects", BindingFlags.NonPublic | BindingFlags.Instance)?
                .GetValue(manager) as Dictionary<string, ProjectInfo>;
            
            if (projects?.ContainsKey(projectName) == true)
            {
                var project = projects[projectName];
                var statusFile = Path.Combine(project.Path, "PROJECT-STATUS.md");
                
                if (File.Exists(statusFile))
                {
                    var content = await File.ReadAllTextAsync(statusFile);
                    var lines = content.Split('\n');
                    var priorities = new List<string>();
                    
                    // Find priorities section
                    bool inPrioritiesSection = false;
                    foreach (var line in lines)
                    {
                        if (line.Trim().StartsWith("## Next Priorities") || 
                            line.Trim().StartsWith("### Immediate"))
                        {
                            inPrioritiesSection = true;
                            continue;
                        }
                        
                        if (inPrioritiesSection && line.StartsWith("##"))
                        {
                            break; // End of section
                        }
                        
                        if (inPrioritiesSection && (line.Trim().StartsWith("- ") || 
                            line.Trim().StartsWith("1. ")))
                        {
                            var priority = line.Trim();
                            if (priority.StartsWith("- ")) priority = priority.Substring(2);
                            if (priority.StartsWith("1. ")) priority = priority.Substring(3);
                            priorities.Add(priority);
                        }
                    }
                    
                    return priorities;
                }
            }
        }
        catch (Exception)
        {
            // Ignore parsing errors
        }
        
        // Fallback priorities
        return new List<string>
        {
            "Continue current development milestone",
            "Address any technical debt",
            "Maintain test coverage"
        };
    }

    /// <summary>
    /// Gets recently modified files for a project
    /// </summary>
    public static Task<List<string>> GetRecentlyModifiedFilesAsync(string projectPath)
    {
        var files = new List<string>();
        
        try
        {
            if (Directory.Exists(projectPath))
            {
                var allFiles = Directory.GetFiles(projectPath, "*", SearchOption.AllDirectories)
                    .Where(f => !f.Contains("\\bin\\") && 
                               !f.Contains("\\obj\\") && 
                               !f.Contains("\\node_modules\\") &&
                               !f.Contains("\\.git\\"))
                    .Select(f => new FileInfo(f))
                    .OrderByDescending(f => f.LastWriteTime)
                    .Take(5)
                    .Select(f => f.FullName);
                
                files.AddRange(allFiles);
            }
        }
        catch (Exception)
        {
            // Ignore file system errors
        }

        return Task.FromResult(files);
    }
}
