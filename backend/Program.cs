using EnterprisePlatformApi.Services;
using EnterprisePlatformApi.Data;
using Microsoft.EntityFrameworkCore;
using OpenAI;

// Load environment variables
DotNetEnv.Env.Load();

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Memory cache for short-term conversation memory
builder.Services.AddMemoryCache();

// Add Entity Framework with SQLite
builder.Services.AddDbContext<EnterprisePlatformDbContext>(options =>
    options.UseSqlite("Data Source=enterprise_platform.db"));

// Add legacy WeatherService
builder.Services.AddScoped<IWeatherService, WeatherService>();

// Add OpenAI service
builder.Services.AddSingleton(provider => 
{
    var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") 
                 ?? "dummy-key-for-development"; // Don't crash if no key
    return new OpenAIClient(apiKey);
});

// Add CORS support with updated policy
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp",
        builder => builder
            .WithOrigins("http://localhost:3000", "http://localhost:3001")
            .AllowAnyMethod()
            .AllowAnyHeader()
            .AllowCredentials());
});

// Add HttpClient for content seeding and tool calls
builder.Services.AddHttpClient();

// Add custom services  
builder.Services.AddScoped<EnterprisePlatformApi.Services.ContentSeederService>();

// Add Context Management Service
builder.Services.AddScoped<EnterprisePlatformApi.Services.ContextManagement.IContextService, EnterprisePlatformApi.Services.ContextManagement.InMemoryContextService>();

// Add AI Content Guardrails Service
builder.Services.AddHttpClient<AIContentGuardrailsService>();
builder.Services.AddScoped<AIContentGuardrailsService>();

// Add Project Status Updater Service
builder.Services.AddScoped<ProjectStatusUpdaterService>();

// Add Workspace Status Manager
builder.Services.AddScoped<WorkspaceStatusManager>();

// Add Autonomous Service Builder
builder.Services.AddScoped<AutonomousServiceBuilderService>();
builder.Services.AddHostedService<AutonomousBuilderBackgroundService>();
builder.Services.AddSingleton<AutonomousBuilderBackgroundService>();

// Add n8n service configuration
builder.Services.Configure<N8nSettings>(builder.Configuration.GetSection("N8n"));
builder.Services.AddHttpClient<N8nService>();
builder.Services.AddScoped<N8nService>();

// Add authentication and authorization (for future use)
builder.Services.AddAuthentication();
builder.Services.AddAuthorization();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Create database if it doesn't exist and seed content
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<EnterprisePlatformDbContext>();
    var contentSeeder = scope.ServiceProvider.GetRequiredService<EnterprisePlatformApi.Services.ContentSeederService>();
    
    try
    {
        context.Database.EnsureCreated();
        
        // Seed content
        await contentSeeder.SeedContentAsync();
        Console.WriteLine("Database and content initialization completed successfully.");
    }
    catch (Exception ex)
    {
        // Log the error but don't crash the app
        Console.WriteLine($"Database initialization warning: {ex.Message}");
    }
}

app.UseCors("AllowReactApp");
app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();

// Map controllers for enterprise platform APIs
app.MapControllers();

// Keep legacy weather endpoint for backward compatibility
var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapGet("/weatherforecast", () =>
{
    var forecast = Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast")
.WithOpenApi();

app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
