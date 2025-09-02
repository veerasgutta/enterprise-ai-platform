using System.Threading.Tasks;

namespace EnterprisePlatformApi.Services.ContextManagement
{
    public interface IContextService
    {
        Task<string> StoreContextAsync(string sessionId, string context, TimeSpan? expiration = null);
        Task<string?> GetContextAsync(string sessionId);
        Task<bool> RemoveContextAsync(string sessionId);
        Task<Dictionary<string, string>> GetAllContextsAsync(string userPrefix = "");
        Task<bool> UpdateContextAsync(string sessionId, string context);
        Task<int> GetContextCountAsync();
        Task ClearExpiredContextsAsync();
    }
}
