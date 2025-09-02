using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace EnterprisePlatformApi.Services.ContextManagement
{
    public interface IContextCacheService
    {
        // Basic context operations
        Task<T?> GetAsync<T>(string key) where T : class;
        Task SetAsync<T>(string key, T value, TimeSpan? expiration = null) where T : class;
        Task RemoveAsync(string key);
        Task ClearAsync();

        // AI-specific context operations
        Task<string?> GetConversationContextAsync(string sessionId);
        Task SetConversationContextAsync(string sessionId, string context, TimeSpan? expiration = null);
        
        // Code context for AI pair programming
        Task<Dictionary<string, object>?> GetCodeContextAsync(string fileHash);
        Task SetCodeContextAsync(string fileHash, Dictionary<string, object> context);
        
        // User preferences and AI settings
        Task<UserAIPreferences?> GetUserPreferencesAsync(string userId);
        Task SetUserPreferencesAsync(string userId, UserAIPreferences preferences);
        
        // Performance metrics
        Task<CacheMetrics> GetMetricsAsync();
    }

    public class UserAIPreferences
    {
        public string UserId { get; set; } = string.Empty;
        public string PreferredAIModel { get; set; } = "gpt-4";
        public Dictionary<string, string> CustomPrompts { get; set; } = new();
        public bool EnableAutoComplete { get; set; } = true;
        public int ContextWindowSize { get; set; } = 4000;
    }

    public class CacheMetrics
    {
        public int TotalEntries { get; set; }
        public long MemoryUsage { get; set; }
        public double HitRatio { get; set; }
        public DateTime LastAccess { get; set; }
    }
}
