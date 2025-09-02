using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using System.Text.Json;

namespace EnterprisePlatformApi.Services.ContextManagement
{
    public class ContextCacheService : IContextCacheService
    {
        private readonly IMemoryCache _memoryCache;
        private readonly ILogger<ContextCacheService> _logger;
        private readonly ConcurrentDictionary<string, DateTime> _accessTimes;
        private long _totalRequests = 0;
        private long _cacheHits = 0;

        // Cache configuration
        private static readonly TimeSpan DefaultExpiration = TimeSpan.FromHours(2);
        private static readonly TimeSpan ConversationExpiration = TimeSpan.FromHours(8);
        private static readonly TimeSpan CodeContextExpiration = TimeSpan.FromMinutes(30);
        private static readonly TimeSpan UserPreferencesExpiration = TimeSpan.FromDays(7);

        public ContextCacheService(IMemoryCache memoryCache, ILogger<ContextCacheService> logger)
        {
            _memoryCache = memoryCache;
            _logger = logger;
            _accessTimes = new ConcurrentDictionary<string, DateTime>();
        }

        public async Task<T?> GetAsync<T>(string key) where T : class
        {
            Interlocked.Increment(ref _totalRequests);
            
            if (_memoryCache.TryGetValue(key, out var cached))
            {
                Interlocked.Increment(ref _cacheHits);
                _accessTimes[key] = DateTime.UtcNow;
                
                _logger.LogDebug("Cache hit for key: {Key}", key);
                return cached as T;
            }

            _logger.LogDebug("Cache miss for key: {Key}", key);
            return null;
        }

        public async Task SetAsync<T>(string key, T value, TimeSpan? expiration = null) where T : class
        {
            var options = new MemoryCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = expiration ?? DefaultExpiration,
                Priority = CacheItemPriority.Normal,
                Size = EstimateSize(value)
            };

            // Add eviction callback for cleanup
            options.RegisterPostEvictionCallback((evictedKey, evictedValue, reason, state) =>
            {
                _accessTimes.TryRemove(evictedKey.ToString()!, out _);
                _logger.LogDebug("Cache entry evicted: {Key}, Reason: {Reason}", evictedKey, reason);
            });

            _memoryCache.Set(key, value, options);
            _accessTimes[key] = DateTime.UtcNow;
            
            _logger.LogDebug("Cache entry set: {Key}", key);
        }

        public async Task RemoveAsync(string key)
        {
            _memoryCache.Remove(key);
            _accessTimes.TryRemove(key, out _);
            _logger.LogDebug("Cache entry removed: {Key}", key);
        }

        public async Task ClearAsync()
        {
            if (_memoryCache is MemoryCache mc)
            {
                mc.Clear();
            }
            _accessTimes.Clear();
            _logger.LogInformation("Cache cleared");
        }

        // AI-specific implementations
        public async Task<string?> GetConversationContextAsync(string sessionId)
        {
            var key = $"conversation:{sessionId}";
            return await GetAsync<string>(key);
        }

        public async Task SetConversationContextAsync(string sessionId, string context, TimeSpan? expiration = null)
        {
            var key = $"conversation:{sessionId}";
            await SetAsync(key, context, expiration ?? ConversationExpiration);
        }

        public async Task<Dictionary<string, object>?> GetCodeContextAsync(string fileHash)
        {
            var key = $"code:{fileHash}";
            return await GetAsync<Dictionary<string, object>>(key);
        }

        public async Task SetCodeContextAsync(string fileHash, Dictionary<string, object> context)
        {
            var key = $"code:{fileHash}";
            await SetAsync(key, context, CodeContextExpiration);
        }

        public async Task<UserAIPreferences?> GetUserPreferencesAsync(string userId)
        {
            var key = $"user:prefs:{userId}";
            return await GetAsync<UserAIPreferences>(key);
        }

        public async Task SetUserPreferencesAsync(string userId, UserAIPreferences preferences)
        {
            var key = $"user:prefs:{userId}";
            await SetAsync(key, preferences, UserPreferencesExpiration);
        }

        public async Task<CacheMetrics> GetMetricsAsync()
        {
            var totalRequests = _totalRequests;
            var cacheHits = _cacheHits;
            var hitRatio = totalRequests > 0 ? (double)cacheHits / totalRequests : 0;

            return new CacheMetrics
            {
                TotalEntries = _accessTimes.Count,
                MemoryUsage = EstimateMemoryUsage(),
                HitRatio = hitRatio,
                LastAccess = _accessTimes.Values.Count > 0 ? _accessTimes.Values.Max() : DateTime.MinValue
            };
        }

        private static int EstimateSize<T>(T value)
        {
            try
            {
                var json = JsonSerializer.Serialize(value);
                return json.Length * 2; // Rough estimate: 2 bytes per char
            }
            catch
            {
                return 1024; // Default size if serialization fails
            }
        }

        private long EstimateMemoryUsage()
        {
            // Simple estimation - in production, you might want more sophisticated tracking
            return _accessTimes.Count * 1024; // Rough estimate
        }
    }
}
