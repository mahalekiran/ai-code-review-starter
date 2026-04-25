using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/code-review")]
public class CodeReviewController : ControllerBase
{
    private readonly IAiCodeReviewClient _aiCodeReviewClient;

    public CodeReviewController(IAiCodeReviewClient aiCodeReviewClient)
    {
        _aiCodeReviewClient = aiCodeReviewClient;
    }

    [HttpPost("analyze")]
    public async Task<ActionResult<CodeReviewResponse>> Analyze([FromBody] CodeReviewRequest request, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.Code))
        {
            return BadRequest("Code is required.");
        }

        var result = await _aiCodeReviewClient.AnalyzeAsync(request, cancellationToken);
        return Ok(result);
    }
}
