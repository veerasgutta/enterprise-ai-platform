using Microsoft.AspNetCore.Mvc;
using EnterprisePlatformApi.Services;
using EnterprisePlatformApi.Models;

namespace EnterprisePlatformApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AutonomousBuilderController : ControllerBase
{
    private readonly AutonomousServiceBuilderService _builderService;
    private readonly ILogger<AutonomousBuilderController> _logger;

    public AutonomousBuilderController(
        AutonomousServiceBuilderService builderService,
        ILogger<AutonomousBuilderController> logger)
    {
        _builderService = builderService;
        _logger = logger;
    }

    [HttpPost("build-service")]
    public async Task<IActionResult> BuildService([FromBody] ServiceRequirement requirement)
    {
        try
        {
            _logger.LogInformation($"Building autonomous service: {requirement.ServiceName}");
            
            var result = await _builderService.BuildServiceAsync(requirement);
            
            return Ok(new
            {
                Status = "success",
                ServiceName = requirement.ServiceName,
                GeneratedFiles = result.GeneratedFiles,
                Message = "Service built successfully",
                Instructions = result.DeploymentInstructions
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Error building service {requirement.ServiceName}");
            return BadRequest(new
            {
                Status = "error",
                Message = ex.Message
            });
        }
    }

    [HttpGet("service-templates")]
    public IActionResult GetServiceTemplates()
    {
        var templates = new List<ServiceTemplate>
        {
            new ServiceTemplate
            {
                Name = "Data Processing Service",
                Description = "Automated data processing and analytics service",
                SuggestedFeatures = ["data processing", "analytics", "real-time"],
                Example = new ServiceRequirement
                {
                    ServiceName = "DataAnalyticsProcessor",
                    Description = "Processes and analyzes enterprise data streams",
                    Features = ["real-time", "analytics", "enterprise-grade", "scalable"]
                }
            },
            new ServiceTemplate
            {
                Name = "Notification Service",
                Description = "Enterprise notification and communication service",
                SuggestedFeatures = ["notifications", "multi-channel", "scheduling"],
                Example = new ServiceRequirement
                {
                    ServiceName = "EnterpriseNotificationHub", 
                    Description = "Manages enterprise-wide notifications and alerts",
                    Features = ["multi-channel", "scheduling", "enterprise-integration"]
                }
            },
            new ServiceTemplate
            {
                Name = "Workflow Automation Service",
                Description = "Automates business workflows and processes",
                SuggestedFeatures = ["workflow", "automation", "business-process"],
                Example = new ServiceRequirement
                {
                    ServiceName = "BusinessWorkflowEngine",
                    Description = "Automates complex business workflows",
                    Features = ["workflow", "automation", "enterprise", "scalable"]
                }
            },
            new ServiceTemplate
            {
                Name = "AI Assistant Service",
                Description = "Intelligent assistant for enterprise operations",
                SuggestedFeatures = ["ai integration", "natural language", "enterprise"],
                Example = new ServiceRequirement
                {
                    ServiceName = "EnterpriseAIAssistant",
                    Description = "AI-powered assistant for business operations",
                    Features = ["ai integration", "nlp", "enterprise", "intelligent"]
                }
            },
            new ServiceTemplate
            {
                Name = "Monitoring Service",
                Description = "System monitoring and performance tracking",
                SuggestedFeatures = ["monitoring", "performance", "alerting"],
                Example = new ServiceRequirement
                {
                    ServiceName = "SystemPerformanceMonitor",
                    Description = "Monitors system performance and health",
                    Features = ["monitoring", "performance", "alerting", "enterprise"]
                }
            }
        };

        return Ok(templates);
    }

    [HttpGet("build-status/{buildId}")]
    public async Task<IActionResult> GetBuildStatus(string buildId)
    {
        try
        {
            var status = await _builderService.GetBuildStatusAsync(buildId);
            return Ok(status);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Error getting build status for {buildId}");
            return NotFound(new { Status = "error", Message = "Build not found" });
        }
    }

    [HttpPost("deploy-service")]
    public async Task<IActionResult> DeployService([FromBody] DeploymentRequest request)
    {
        try
        {
            _logger.LogInformation($"Deploying service: {request.ServiceName}");
            
            var result = await _builderService.DeployServiceAsync(request);
            
            return Ok(new
            {
                Status = "success",
                ServiceName = request.ServiceName,
                DeploymentUrl = result.ServiceUrl,
                Message = "Service deployed successfully"
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Error deploying service {request.ServiceName}");
            return BadRequest(new
            {
                Status = "error",
                Message = ex.Message
            });
        }
    }
}

public class ServiceTemplate
{
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public List<string> SuggestedFeatures { get; set; } = new();
    public ServiceRequirement Example { get; set; } = new();
}

public class ServiceRequirement
{
    public string ServiceName { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public List<string> Features { get; set; } = new();
    public Dictionary<string, object> Configuration { get; set; } = new();
}

public class DeploymentRequest
{
    public string ServiceName { get; set; } = string.Empty;
    public string Environment { get; set; } = "development";
    public Dictionary<string, string> EnvironmentVariables { get; set; } = new();
}
