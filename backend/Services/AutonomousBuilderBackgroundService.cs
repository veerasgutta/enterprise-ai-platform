using EnterprisePlatformApi.Services;

namespace EnterprisePlatformApi.Services;

/// <summary>
/// Background service that can execute autonomous service building on schedules or triggers
/// </summary>
public class AutonomousBuilderBackgroundService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<AutonomousBuilderBackgroundService> _logger;
    private readonly Queue<ServiceRequirement> _buildQueue = new();
    private readonly SemaphoreSlim _queueSemaphore = new(1, 1);

    public AutonomousBuilderBackgroundService(
        IServiceProvider serviceProvider,
        ILogger<AutonomousBuilderBackgroundService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Autonomous Builder Background Service started");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcessBuildQueue(stoppingToken);
                await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken); // Check every 30 seconds
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in Autonomous Builder Background Service");
                await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken); // Wait before retrying
            }
        }

        _logger.LogInformation("Autonomous Builder Background Service stopped");
    }

    private async Task ProcessBuildQueue(CancellationToken cancellationToken)
    {
        await _queueSemaphore.WaitAsync(cancellationToken);
        
        try
        {
            while (_buildQueue.Count > 0)
            {
                var requirement = _buildQueue.Dequeue();
                _logger.LogInformation($"Processing queued service build: {requirement.ServiceName}");

                using var scope = _serviceProvider.CreateScope();
                var builderService = scope.ServiceProvider.GetRequiredService<AutonomousServiceBuilderService>();
                
                var result = await builderService.BuildServiceAsync(requirement);
                
                _logger.LogInformation($"Background build completed for {requirement.ServiceName}: {result.Status}");
            }
        }
        finally
        {
            _queueSemaphore.Release();
        }
    }

    /// <summary>
    /// Queue a service for autonomous building
    /// </summary>
    public async Task QueueServiceBuild(ServiceRequirement requirement)
    {
        await _queueSemaphore.WaitAsync();
        
        try
        {
            _buildQueue.Enqueue(requirement);
            _logger.LogInformation($"Queued service for autonomous building: {requirement.ServiceName}");
        }
        finally
        {
            _queueSemaphore.Release();
        }
    }

    /// <summary>
    /// Get current queue status
    /// </summary>
    public async Task<QueueStatus> GetQueueStatus()
    {
        await _queueSemaphore.WaitAsync();
        
        try
        {
            return new QueueStatus
            {
                PendingBuilds = _buildQueue.Count,
                QueuedServices = _buildQueue.Select(r => r.ServiceName).ToList()
            };
        }
        finally
        {
            _queueSemaphore.Release();
        }
    }
}

public class QueueStatus
{
    public int PendingBuilds { get; set; }
    public List<string> QueuedServices { get; set; } = new();
}
