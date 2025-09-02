using System.Text.Json.Serialization;

namespace EnterprisePlatformApi.Models.VectorDatabase
{
    /// <summary>
    /// Represents a document stored in the vector database with embeddings
    /// Used for AI context management and semantic search
    /// </summary>
    public class VectorDocument
    {
        [JsonPropertyName("id")]
        public string Id { get; set; } = Guid.NewGuid().ToString();

        [JsonPropertyName("vector")]
        public float[] Vector { get; set; } = Array.Empty<float>();

        [JsonPropertyName("payload")]
        public VectorPayload Payload { get; set; } = new();

        [JsonPropertyName("created_at")]
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }

    /// <summary>
    /// Metadata payload for vector documents
    /// Supports enterprise and fintech compliance requirements
    /// </summary>
    public class VectorPayload
    {
        [JsonPropertyName("content")]
        public string Content { get; set; } = string.Empty;

        [JsonPropertyName("content_type")]
        public string ContentType { get; set; } = "text";

        [JsonPropertyName("source")]
        public string Source { get; set; } = string.Empty;

        [JsonPropertyName("domain")]
        public string Domain { get; set; } = "general"; // enterprise, fintech, etc.

        [JsonPropertyName("classification")]
        public string Classification { get; set; } = "public"; // public, confidential, restricted

        [JsonPropertyName("tags")]
        public List<string> Tags { get; set; } = new();

        [JsonPropertyName("metadata")]
        public Dictionary<string, object> Metadata { get; set; } = new();

        [JsonPropertyName("user_id")]
        public string? UserId { get; set; }

        [JsonPropertyName("session_id")]
        public string? SessionId { get; set; }

        [JsonPropertyName("expires_at")]
        public DateTime? ExpiresAt { get; set; }
    }

    /// <summary>
    /// Search result from vector database with similarity score
    /// </summary>
    public class VectorSearchResult
    {
        [JsonPropertyName("id")]
        public string Id { get; set; } = string.Empty;

        [JsonPropertyName("score")]
        public float Score { get; set; }

        [JsonPropertyName("payload")]
        public VectorPayload Payload { get; set; } = new();

        [JsonPropertyName("vector")]
        public float[]? Vector { get; set; }
    }

    /// <summary>
    /// Search request parameters for vector similarity search
    /// </summary>
    public class VectorSearchRequest
    {
        [JsonPropertyName("vector")]
        public float[] Vector { get; set; } = Array.Empty<float>();

        [JsonPropertyName("limit")]
        public int Limit { get; set; } = 10;

        [JsonPropertyName("score_threshold")]
        public float? ScoreThreshold { get; set; }

        [JsonPropertyName("filter")]
        public Dictionary<string, object>? Filter { get; set; }

        [JsonPropertyName("with_payload")]
        public bool WithPayload { get; set; } = true;

        [JsonPropertyName("with_vector")]
        public bool WithVector { get; set; } = false;
    }

    /// <summary>
    /// Collection configuration for Qdrant
    /// </summary>
    public class CollectionConfig
    {
        [JsonPropertyName("vectors")]
        public VectorConfig Vectors { get; set; } = new();

        [JsonPropertyName("optimizers_config")]
        public OptimizersConfig? OptimizersConfig { get; set; }

        [JsonPropertyName("replication_factor")]
        public int ReplicationFactor { get; set; } = 1;

        [JsonPropertyName("write_consistency_factor")]
        public int WriteConsistencyFactor { get; set; } = 1;
    }

    /// <summary>
    /// Vector configuration for embeddings
    /// </summary>
    public class VectorConfig
    {
        [JsonPropertyName("size")]
        public int Size { get; set; } = 1536; // OpenAI ada-002 embedding size

        [JsonPropertyName("distance")]
        public string Distance { get; set; } = "Cosine"; // Cosine, Euclid, Dot

        [JsonPropertyName("hnsw_config")]
        public HnswConfig? HnswConfig { get; set; }
    }

    /// <summary>
    /// HNSW algorithm configuration for performance tuning
    /// </summary>
    public class HnswConfig
    {
        [JsonPropertyName("m")]
        public int M { get; set; } = 16;

        [JsonPropertyName("ef_construct")]
        public int EfConstruct { get; set; } = 100;

        [JsonPropertyName("full_scan_threshold")]
        public int FullScanThreshold { get; set; } = 10000;

        [JsonPropertyName("max_indexing_threads")]
        public int MaxIndexingThreads { get; set; } = 0; // Use all available cores
    }

    /// <summary>
    /// Optimizer configuration for vector search performance
    /// </summary>
    public class OptimizersConfig
    {
        [JsonPropertyName("deleted_threshold")]
        public float DeletedThreshold { get; set; } = 0.2f;

        [JsonPropertyName("vacuum_min_vector_number")]
        public int VacuumMinVectorNumber { get; set; } = 1000;

        [JsonPropertyName("default_segment_number")]
        public int DefaultSegmentNumber { get; set; } = 0;

        [JsonPropertyName("max_segment_size")]
        public int? MaxSegmentSize { get; set; }

        [JsonPropertyName("memmap_threshold")]
        public int? MemmapThreshold { get; set; }

        [JsonPropertyName("indexing_threshold")]
        public int IndexingThreshold { get; set; } = 20000;

        [JsonPropertyName("flush_interval_sec")]
        public int FlushIntervalSec { get; set; } = 5;

        [JsonPropertyName("max_optimization_threads")]
        public int MaxOptimizationThreads { get; set; } = 1;
    }
}
