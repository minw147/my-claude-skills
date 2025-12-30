# n8n Workflow Troubleshooting Guide

This guide covers common issues and solutions based on real debugging sessions and implementation experiences.

## AI Agent Issues

### Tool Schema Mismatch Errors

**Error:** `"Received tool input did not match expected schema"`

**Symptoms:**
- Workflow fails intermittently
- Works on retry with same input
- More common with Flash model than Pro

**Root Causes:**
- AI model gets "distracted" by complex context
- JSON formatting inconsistencies in tool calls
- Insufficient prompt specificity for tool usage

**Solutions:**

1. **Add Tool Usage Protocol to System Prompt:**
```markdown
## Tool Usage Protocol (Critical)
When using tools, you MUST provide the exact JSON schema required. Do not include any conversational filler inside the tool call. Format tool calls precisely as specified in the tool documentation.
```

2. **Use Pro Model for Complex Interactions:**
```javascript
// Switch to Pro for tool-heavy operations
if (requiresTools($json.body.message)) {
  return "pro";
}
```

3. **Simplify Tool Attachments:**
```javascript
// Only attach necessary tools
const tools = [];
if (queryNeedsSearch(query)) {
  tools.push(searchTool);
}
if (queryNeedsDownload(query)) {
  tools.push(downloadTool);
}
```

4. **Add Validation Layer:**
```javascript
// Pre-validate tool inputs
const validatedInput = validateToolInput(rawInput);
if (!validatedInput.valid) {
  return { error: validatedInput.message };
}
```

### Memory Buffer Problems

**Error:** Context loss between conversation turns

**Symptoms:**
- AI "forgets" previous conversation
- Inconsistent responses across turns
- Memory buffer appears empty

**Solutions:**

1. **Increase Buffer Window:**
```json
{
  "sessionIdType": "customKey",
  "sessionKey": "{{ $('Webhook').item.json.body.sessionId }}",
  "contextWindowLength": 20
}
```

2. **Implement Session Persistence:**
```javascript
// Ensure consistent session IDs
const sessionId = $json.body.sessionId || generateSessionId();
return { sessionId, ...otherData };
```

3. **Add Memory Debugging:**
```javascript
// Log memory state for debugging
const memoryState = await getMemoryState(sessionId);
console.log('Memory items:', memoryState.length);
```

## Webhook Integration Issues

### Timeout Errors

**Error:** `Webhook timeout` or `Request aborted`

**Symptoms:**
- Long-running workflows fail
- Frontend receives timeout errors
- Partial execution without completion

**Solutions:**

1. **Use Async Response Mode:**
```json
{
  "responseMode": "lastNode",
  "options": {}
}
```

2. **Implement Status Polling:**
```javascript
// Return execution ID immediately
return {
  executionId: $execution.id,
  status: "processing",
  message: "Processing your request..."
};
```

3. **Add Progress Webhooks:**
```javascript
// Send progress updates to frontend
await sendWebhook({
  type: "progress",
  executionId: $execution.id,
  progress: 50,
  message: "Processing complete"
});
```

### CORS Issues

**Error:** `CORS policy blocked` or preflight errors

**Symptoms:**
- Frontend can't connect to n8n webhooks
- Browser console shows CORS errors

**Solutions:**

1. **Configure CORS in n8n:**
```bash
# n8n configuration
N8N_CORS_ORIGIN=https://your-frontend-domain.com
```

2. **Add CORS Headers in Webhook:**
```javascript
return {
  headers: {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  },
  body: responseData
};
```

## Google Drive Integration Problems

### Authentication Failures

**Error:** `Invalid credentials` or `Access denied`

**Symptoms:**
- Google Drive operations fail
- Authentication errors in logs

**Solutions:**

1. **Verify OAuth Scopes:**
```json
{
  "scopes": [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file"
  ]
}
```

2. **Refresh Token Logic:**
```javascript
if (isTokenExpired(token)) {
  const newToken = await refreshOAuthToken(token);
  updateCredentials(newToken);
}
```

3. **Test API Access:**
```bash
curl -H "Authorization: Bearer $TOKEN" \
     "https://www.googleapis.com/drive/v3/files"
```

### File Not Found Errors

**Error:** `File not found` or `Invalid file ID`

**Symptoms:**
- Search returns empty results
- Download operations fail

**Solutions:**

1. **Verify Folder Structure:**
```javascript
// Check folder exists and is accessible
const folder = await drive.files.get({
  fileId: folderId,
  fields: 'name,permissions'
});
```

2. **Use Correct MIME Types:**
```javascript
// Search with proper filters
const query = "name contains 'Strategy' and mimeType='text/markdown'";
const results = await drive.files.list({ q: query });
```

3. **Handle Permission Issues:**
```javascript
// Check file permissions
const permissions = await drive.permissions.list({
  fileId: fileId
});
```

## API Integration Issues

### Rate Limiting

**Error:** `Rate limit exceeded` or `Too many requests`

**Symptoms:**
- API calls fail intermittently
- 429 status codes in logs

**Solutions:**

1. **Implement Exponential Backoff:**
```javascript
let attempt = 0;
const maxAttempts = 5;

while (attempt < maxAttempts) {
  try {
    return await apiCall();
  } catch (error) {
    if (error.status === 429) {
      const delay = Math.pow(2, attempt) * 1000;
      await sleep(delay);
      attempt++;
    } else {
      throw error;
    }
  }
}
```

2. **Add Request Throttling:**
```javascript
// Queue requests with delays
const queue = [];
let processing = false;

async function processQueue() {
  if (processing || queue.length === 0) return;

  processing = true;
  while (queue.length > 0) {
    const request = queue.shift();
    await request();
    await sleep(1000); // 1 second between requests
  }
  processing = false;
}
```

### API Response Parsing Errors

**Error:** `Unexpected token` or JSON parsing failures

**Symptoms:**
- API calls succeed but data processing fails
- Undefined property errors

**Solutions:**

1. **Add Response Validation:**
```javascript
function validateApiResponse(response) {
  if (!response || typeof response !== 'object') {
    throw new Error('Invalid API response format');
  }

  if (!response.hasOwnProperty('data')) {
    throw new Error('Missing required field: data');
  }

  return response;
}
```

2. **Handle Different Response Formats:**
```javascript
// Normalize different API response structures
function normalizeResponse(rawResponse) {
  // Handle various response formats
  if (rawResponse.items) return rawResponse.items;
  if (rawResponse.data) return rawResponse.data;
  if (Array.isArray(rawResponse)) return rawResponse;

  return [rawResponse]; // Single item as array
}
```

## Workflow Performance Issues

### Memory Exhaustion

**Error:** `Out of memory` or workflow crashes

**Symptoms:**
- Workflows fail on large datasets
- Memory usage spikes

**Solutions:**

1. **Implement Streaming:**
```javascript
// Process large files in chunks
const stream = fs.createReadStream(largeFile);
stream.pipe(transformStream)
       .pipe(outputStream);
```

2. **Use Batch Processing:**
```json
{
  "batchSize": 100,
  "options": {}
}
```

3. **Clean Up Resources:**
```javascript
// Explicitly free memory
let data = await loadLargeDataset();
const result = await processData(data);
data = null; // Allow garbage collection
```

### Execution Timeouts

**Error:** `Execution timeout exceeded`

**Symptoms:**
- Workflows stop mid-execution
- Long-running operations fail

**Solutions:**

1. **Break Into Sub-Workflows:**
```javascript
// Instead of one long workflow, create:
async function phase1() { /* Quick setup */ }
async function phase2() { /* Main processing */ }
async function phase3() { /* Cleanup */ }
```

2. **Add Checkpoint Logic:**
```javascript
// Save progress periodically
await saveCheckpoint(currentState, stepNumber);

// Resume from last checkpoint
const lastState = await loadLastCheckpoint();
continueFrom(lastState);
```

## Database and Storage Issues

### Connection Pool Exhaustion

**Error:** `Connection pool exhausted` or database timeouts

**Symptoms:**
- Database operations fail under load
- Connection errors in logs

**Solutions:**

1. **Implement Connection Pooling:**
```javascript
const pool = mysql.createPool({
  connectionLimit: 10,
  acquireTimeout: 60000,
  timeout: 60000
});
```

2. **Add Connection Retry Logic:**
```javascript
async function withRetry(operation, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(1000 * (i + 1));
    }
  }
}
```

### Data Consistency Issues

**Error:** Race conditions or data corruption

**Symptoms:**
- Inconsistent data states
- Duplicate records
- Missing updates

**Solutions:**

1. **Implement Transactions:**
```javascript
await db.transaction(async (trx) => {
  await trx('table1').insert(data1);
  await trx('table2').update(data2);
});
```

2. **Add Optimistic Locking:**
```javascript
const currentVersion = await getCurrentVersion(recordId);
const updateResult = await updateWithVersion(recordId, newData, currentVersion);

if (!updateResult.success) {
  throw new Error('Concurrent modification detected');
}
```

## Monitoring and Alerting

### Setting Up Health Checks

**Workflow Self-Monitoring:**
```javascript
// Daily health report
const healthStatus = {
  timestamp: new Date(),
  workflowsActive: await countActiveWorkflows(),
  executionsToday: await countExecutionsToday(),
  errorsToday: await countErrorsToday(),
  averageExecutionTime: await calculateAvgExecutionTime()
};

await sendHealthReport(healthStatus);
```

### Alert Configuration

**Error Alerting:**
```javascript
if (error.severity === 'critical') {
  await sendEmail({
    to: 'admin@company.com',
    subject: 'Critical Workflow Error',
    body: `Workflow ${workflowName} failed: ${error.message}`
  });

  await sendSlackMessage({
    channel: '#alerts',
    text: `🚨 Critical Error: ${workflowName} failed`
  });
}
```

## Best Practices Summary

1. **Always implement proper error handling**
2. **Use appropriate AI models for task complexity**
3. **Implement rate limiting and backoff strategies**
4. **Monitor memory usage and implement cleanup**
5. **Add comprehensive logging for debugging**
6. **Test workflows with realistic data volumes**
7. **Implement health checks and alerting**
8. **Use environment variables for configuration**
9. **Document workflow dependencies and requirements**
10. **Version control workflow changes**

This troubleshooting guide is based on real implementation experiences and common issues encountered during n8n workflow development and deployment.
