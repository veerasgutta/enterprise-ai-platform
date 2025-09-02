using Microsoft.AspNetCore.Mvc;
using EnterprisePlatformApi.Services.ContextManagement;

namespace EnterprisePlatformApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ContextController : ControllerBase
    {
        private readonly IContextService _contextService;
        private readonly ILogger<ContextController> _logger;

        public ContextController(IContextService contextService, ILogger<ContextController> logger)
        {
            _contextService = contextService;
            _logger = logger;
        }

        [HttpPost("store")]
        public async Task<ActionResult<ContextResponse>> StoreContext([FromBody] StoreContextRequest request)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(request.SessionId) || string.IsNullOrWhiteSpace(request.Context))
                {
                    return BadRequest("SessionId and Context are required");
                }

                var sessionId = await _contextService.StoreContextAsync(
                    request.SessionId, 
                    request.Context, 
                    request.ExpirationMinutes.HasValue ? TimeSpan.FromMinutes(request.ExpirationMinutes.Value) : null
                );

                return Ok(new ContextResponse
                {
                    Success = true,
                    SessionId = sessionId,
                    Message = "Context stored successfully"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error storing context for session {SessionId}", request.SessionId);
                return StatusCode(500, new ContextResponse
                {
                    Success = false,
                    Message = "Failed to store context"
                });
            }
        }

        [HttpGet("{sessionId}")]
        public async Task<ActionResult<ContextResponse>> GetContext(string sessionId)
        {
            try
            {
                var context = await _contextService.GetContextAsync(sessionId);
                
                if (context == null)
                {
                    return NotFound(new ContextResponse
                    {
                        Success = false,
                        Message = "Context not found"
                    });
                }

                return Ok(new ContextResponse
                {
                    Success = true,
                    SessionId = sessionId,
                    Context = context,
                    Message = "Context retrieved successfully"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving context for session {SessionId}", sessionId);
                return StatusCode(500, new ContextResponse
                {
                    Success = false,
                    Message = "Failed to retrieve context"
                });
            }
        }

        [HttpPut("{sessionId}")]
        public async Task<ActionResult<ContextResponse>> UpdateContext(string sessionId, [FromBody] UpdateContextRequest request)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(request.Context))
                {
                    return BadRequest("Context is required");
                }

                var success = await _contextService.UpdateContextAsync(sessionId, request.Context);
                
                if (!success)
                {
                    return NotFound(new ContextResponse
                    {
                        Success = false,
                        Message = "Failed to update context"
                    });
                }

                return Ok(new ContextResponse
                {
                    Success = true,
                    SessionId = sessionId,
                    Message = "Context updated successfully"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating context for session {SessionId}", sessionId);
                return StatusCode(500, new ContextResponse
                {
                    Success = false,
                    Message = "Failed to update context"
                });
            }
        }

        [HttpDelete("{sessionId}")]
        public async Task<ActionResult<ContextResponse>> RemoveContext(string sessionId)
        {
            try
            {
                var success = await _contextService.RemoveContextAsync(sessionId);
                
                return Ok(new ContextResponse
                {
                    Success = success,
                    SessionId = sessionId,
                    Message = success ? "Context removed successfully" : "Context not found"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error removing context for session {SessionId}", sessionId);
                return StatusCode(500, new ContextResponse
                {
                    Success = false,
                    Message = "Failed to remove context"
                });
            }
        }

        [HttpGet]
        public async Task<ActionResult<ContextListResponse>> GetAllContexts([FromQuery] string? userPrefix = null)
        {
            try
            {
                var contexts = await _contextService.GetAllContextsAsync(userPrefix ?? "");
                var count = await _contextService.GetContextCountAsync();

                return Ok(new ContextListResponse
                {
                    Success = true,
                    Contexts = contexts,
                    TotalCount = count,
                    Message = $"Retrieved {contexts.Count} contexts"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving all contexts");
                return StatusCode(500, new ContextListResponse
                {
                    Success = false,
                    Contexts = new Dictionary<string, string>(),
                    Message = "Failed to retrieve contexts"
                });
            }
        }

        [HttpPost("cleanup")]
        public async Task<ActionResult<ContextResponse>> CleanupExpiredContexts()
        {
            try
            {
                await _contextService.ClearExpiredContextsAsync();
                var remainingCount = await _contextService.GetContextCountAsync();

                return Ok(new ContextResponse
                {
                    Success = true,
                    Message = $"Cleanup completed. {remainingCount} contexts remaining."
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during context cleanup");
                return StatusCode(500, new ContextResponse
                {
                    Success = false,
                    Message = "Failed to cleanup contexts"
                });
            }
        }
    }

    // DTOs
    public class StoreContextRequest
    {
        public string SessionId { get; set; } = string.Empty;
        public string Context { get; set; } = string.Empty;
        public int? ExpirationMinutes { get; set; }
    }

    public class UpdateContextRequest
    {
        public string Context { get; set; } = string.Empty;
    }

    public class ContextResponse
    {
        public bool Success { get; set; }
        public string? SessionId { get; set; }
        public string? Context { get; set; }
        public string Message { get; set; } = string.Empty;
    }

    public class ContextListResponse
    {
        public bool Success { get; set; }
        public Dictionary<string, string> Contexts { get; set; } = new();
        public int TotalCount { get; set; }
        public string Message { get; set; } = string.Empty;
    }
}
