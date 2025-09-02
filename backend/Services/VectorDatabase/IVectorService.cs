using EnterprisePlatformApi.Models.VectorDatabase;

namespace EnterprisePlatformApi.Services.VectorDatabase
{
    /// <summary>
    /// Interface for vector database operations
    /// Supports context management for AI Agent Pair Programming
    /// </summary>
    public interface IVectorService
    {
        /// <summary>
        /// Create a new collection in the vector database
        /// </summary>
        Task<bool> CreateCollectionAsync(string collectionName, CollectionConfig config, CancellationToken cancellationToken = default);

        /// <summary>
        /// Check if a collection exists
        /// </summary>
        Task<bool> CollectionExistsAsync(string collectionName, CancellationToken cancellationToken = default);

        /// <summary>
        /// Store a vector document with embeddings
        /// </summary>
        Task<bool> UpsertVectorAsync(string collectionName, VectorDocument document, CancellationToken cancellationToken = default);

        /// <summary>
        /// Store multiple vector documents in batch
        /// </summary>
        Task<bool> UpsertVectorsBatchAsync(string collectionName, IEnumerable<VectorDocument> documents, CancellationToken cancellationToken = default);

        /// <summary>
        /// Search for similar vectors using semantic similarity
        /// </summary>
        Task<IEnumerable<VectorSearchResult>> SearchSimilarAsync(string collectionName, VectorSearchRequest request, CancellationToken cancellationToken = default);

        /// <summary>
        /// Get a specific vector document by ID
        /// </summary>
        Task<VectorDocument?> GetVectorAsync(string collectionName, string id, CancellationToken cancellationToken = default);

        /// <summary>
        /// Delete a vector document by ID
        /// </summary>
        Task<bool> DeleteVectorAsync(string collectionName, string id, CancellationToken cancellationToken = default);

        /// <summary>
        /// Delete multiple vectors by filter criteria
        /// </summary>
        Task<bool> DeleteVectorsByFilterAsync(string collectionName, Dictionary<string, object> filter, CancellationToken cancellationToken = default);

        /// <summary>
        /// Get collection statistics and health information
        /// </summary>
        Task<CollectionInfo?> GetCollectionInfoAsync(string collectionName, CancellationToken cancellationToken = default);

        /// <summary>
        /// Perform hybrid search combining vector similarity and filtering
        /// </summary>
        Task<IEnumerable<VectorSearchResult>> HybridSearchAsync(string collectionName, VectorSearchRequest vectorRequest, Dictionary<string, object> filter, CancellationToken cancellationToken = default);
    }

    /// <summary>
    /// Collection information and statistics
    /// </summary>
    public class CollectionInfo
    {
        public string Name { get; set; } = string.Empty;
        public long VectorCount { get; set; }
        public string Status { get; set; } = string.Empty;
        public VectorConfig Config { get; set; } = new();
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
    }
}
