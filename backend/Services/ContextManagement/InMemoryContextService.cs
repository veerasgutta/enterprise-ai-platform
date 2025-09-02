using Microsoft.Extensions.Caching.Memory;
using System.Collections.Concurrent;
using EnterprisePlatformApi.Services.ContextManagement;

namespace EnterprisePlatformApi.Services.ContextManagement
{
    public class InMemoryContextService : IContextService
    {
        private readonly IMemoryCache _cache;
        private readonly ILogger<InMemoryContextService> _logger;
        private readonly ConcurrentDictionary<string, DateTime> _expirations;

        public InMemoryContextService(IMemoryCache cache, ILogger<InMemoryContextService> logger)
        {
            _cache = cache;
            _logger = logger;
            _expirations = new ConcurrentDictionary<string, DateTime>();
        }

        public async Task<string> StoreContextAsync(string sessionId, string context, TimeSpan? expiration = null)
        {
            try
            {
                var cacheExpiration = expiration ?? TimeSpan.FromHours(2); // Default 2 hours
                var absoluteExpiration = DateTime.UtcNow.Add(cacheExpiration);

                var cacheOptions = new MemoryCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = cacheExpiration,
                    SlidingExpiration = TimeSpan.FromMinutes(30), // Extend if accessed
                    Priority = CacheItemPriority.Normal
                };

                _cache.Set($"context:{sessionId}", context, cacheOptions);
                _expirations[sessionId] = absoluteExpiration;

                _logger.LogInformation("Context stored for session {SessionId}, expires at {Expiration}", 
                    sessionId, absoluteExpiration);

                return sessionId;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to store context for session {SessionId}", sessionId);
                throw;
            }
        }

        public async Task<string?> GetContextAsync(string sessionId)
        {
            try
            {
                if (_cache.TryGetValue($"context:{sessionId}", out string? context))
                {
                    _logger.LogDebug("Context retrieved for session {SessionId}", sessionId);
                    return context;
                }

                _logger.LogDebug("No context found for session {SessionId}", sessionId);
                return null;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to retrieve context for session {SessionId}", sessionId);
                return null;
            }
        }

        public async Task<bool> RemoveContextAsync(string sessionId)
        {
            try
            {
                _cache.Remove($"context:{sessionId}");
                _expirations.TryRemove(sessionId, out _);
                
                _logger.LogInformation("Context removed for session {SessionId}", sessionId);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to remove context for session {SessionId}", sessionId);
                return false;
            }
        }

        public async Task<Dictionary<string, string>> GetAllContextsAsync(string userPrefix = "")
        {
            try
            {
                var contexts = new Dictionary<string, string>();
                
                // Note: MemoryCache doesn't provide enumeration, so we track keys separately
                // This is a simplified implementation for development
                foreach (var expiration in _expirations)
                {
                    if (string.IsNullOrEmpty(userPrefix) || expiration.Key.StartsWith(userPrefix))
                    {
                        var context = await GetContextAsync(expiration.Key);
                        if (context != null)
                        {
                            contexts[expiration.Key] = context;
                        }
                    }
                }

                return contexts;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to retrieve all contexts");
                return new Dictionary<string, string>();
            }
        }

        public async Task<bool> UpdateContextAsync(string sessionId, string context)
        {
            try
            {
                // For updates, we maintain the same expiration
                var existingExpiration = _expirations.GetValueOrDefault(sessionId, DateTime.UtcNow.AddHours(2));
                var remainingTime = existingExpiration - DateTime.UtcNow;
                
                if (remainingTime <= TimeSpan.Zero)
                {
                    remainingTime = TimeSpan.FromHours(2); // Reset if expired
                }

                await StoreContextAsync(sessionId, context, remainingTime);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to update context for session {SessionId}", sessionId);
                return false;
            }
        }

        public async Task<int> GetContextCountAsync()
        {
            try
            {
                await ClearExpiredContextsAsync(); // Clean up first
                return _expirations.Count;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get context count");
                return 0;
            }
        }

        public async Task ClearExpiredContextsAsync()
        {
            try
            {
                var now = DateTime.UtcNow;
                var expiredKeys = _expirations
                    .Where(kvp => kvp.Value <= now)
                    .Select(kvp => kvp.Key)
                    .ToList();

                foreach (var key in expiredKeys)
                {
                    _expirations.TryRemove(key, out _);
                    _cache.Remove($"context:{key}");
                }

                if (expiredKeys.Any())
                {
                    _logger.LogInformation("Cleared {Count} expired contexts", expiredKeys.Count);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to clear expired contexts");
            }
        }
    }
}
