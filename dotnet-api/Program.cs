using System.Net.Http.Json;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient("AiService", client =>
{
    var aiServiceUrl = builder.Configuration["AI_SERVICE_URL"] ?? "http://localhost:8000";
    client.BaseAddress = new Uri(aiServiceUrl);
});
builder.Services.AddScoped<IAiCodeReviewClient, AiCodeReviewClient>();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();
app.MapControllers();
app.Run();

public record CodeReviewRequest(string FileName, string Language, string Code);
public record CodeReviewFinding(string Severity, string Category, string Description, string SuggestedFix, int? LineNumber);
public record CodeReviewResponse(string Summary, List<CodeReviewFinding> Findings);

public interface IAiCodeReviewClient
{
    Task<CodeReviewResponse> AnalyzeAsync(CodeReviewRequest request, CancellationToken cancellationToken);
}

public sealed class AiCodeReviewClient : IAiCodeReviewClient
{
    private readonly IHttpClientFactory _httpClientFactory;

    public AiCodeReviewClient(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    public async Task<CodeReviewResponse> AnalyzeAsync(CodeReviewRequest request, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.Code))
        {
            throw new ArgumentException("Code cannot be empty.");
        }

        var client = _httpClientFactory.CreateClient("AiService");
        var response = await client.PostAsJsonAsync("/analyze", request, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<CodeReviewResponse>(cancellationToken: cancellationToken);
        return result ?? new CodeReviewResponse("No response returned from AI service.", new List<CodeReviewFinding>());
    }
}
