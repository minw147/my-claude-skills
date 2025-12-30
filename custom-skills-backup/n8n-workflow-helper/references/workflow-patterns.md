# n8n Workflow Patterns & Architectures

This document outlines proven workflow patterns based on real implementations of complex n8n automation systems.

## Core Architecture Patterns

### 1. AI Assistant Backend Pattern

**Use Case:** Building conversational AI assistants with memory, tools, and knowledge base integration.

**Workflow Structure:**
```
Webhook Trigger → Input Processing → Model Selection → AI Agent → Memory Management → Tool Integration → Response
```

**Key Nodes:**
- **Webhook** (`n8n-nodes-base.webhook`): Receives chat messages via HTTP POST
- **Switch** (`n8n-nodes-base.switch`): Routes between Flash/Pro models based on complexity
- **AI Agent** (`@n8n/n8n-nodes-langchain.agent`): LangChain-powered AI processing
- **Memory Buffer** (`@n8n/n8n-nodes-langchain.memoryBufferWindow`): Conversation context
- **Google Drive Tools**: Knowledge base search and retrieval
- **Respond to Webhook**: Sends responses back to frontend

**Configuration Details:**

**Webhook Setup:**
```json
{
  "httpMethod": "POST",
  "path": "chat",
  "responseMode": "responseNode",
  "options": {}
}
```

**Model Selection Logic:**
```javascript
// Switch based on model parameter from frontend
if ($json.body.model === "pro") {
  return "pro";
} else {
  return "flash";
}
```

**AI Agent System Prompt Structure:**
```
# Master Profile: [Personality Definition]
## Core Identity
[Role and relationship description]

## Operational Rules
[Context continuity, decision frameworks, code standards]

## Tool Usage Protocol
[API interaction guidelines, error handling]

## Knowledge Base Scope
[Available information domains and access patterns]
```

### 2. Automated Backup System Pattern

**Use Case:** Creating self-maintaining backup systems for n8n workflows and data.

**Workflow Structure:**
```
Schedule Trigger → List Workflows → Batch Processing → Export JSON → Cloud Storage → Notifications
```

**Key Nodes:**
- **Schedule Trigger** (`n8n-nodes-base.scheduleTrigger`): Cron-based automation
- **n8n API** (`n8n-nodes-base.n8n`): Workflow introspection and export
- **Split In Batches** (`n8n-nodes-base.splitInBatches`): Handle large workflow sets
- **Google Drive** (`n8n-nodes-base.googleDrive`): Cloud storage operations
- **If** (`n8n-nodes-base.if`): Conditional update vs create logic

**Implementation Details:**

**Schedule Configuration:**
```json
{
  "rule": {
    "interval": [{
      "field": "cronExpression",
      "expression": "0 4 * * 0"  // Every Sunday at 4AM
    }]
  }
}
```

**Workflow Processing Loop:**
```javascript
// Get all workflows via n8n API
const workflows = await n8nApi.listWorkflows();

// Process each workflow individually
for (const workflow of workflows) {
  const json = await n8nApi.getWorkflow(workflow.id);
  // Upload to Google Drive with naming convention
  await uploadToDrive(json, `${workflow.name}_Backup.json`);
}
```

**Cloud Storage Logic:**
```javascript
// Search for existing backup
const existing = await searchDrive(`${workflow.name}_Backup.json`);

// Update existing or create new
if (existing.files.length > 0) {
  await updateFile(existing.files[0].id, jsonData);
} else {
  await createFile(jsonData, folderId);
}
```

### 3. Memory Consolidation Pattern

**Use Case:** Automated processing of conversation data into structured knowledge.

**Workflow Structure:**
```
Schedule Trigger → Data Retrieval → AI Processing → File Generation → Cloud Upload → Cleanup
```

**Key Nodes:**
- **Schedule Trigger**: Daily execution timing
- **Google Sheets**: Read conversation buffer
- **AI Agent**: Summarize and structure conversations
- **Convert to File**: Generate Markdown output
- **Google Drive**: Store in organized folders
- **Set**: Data cleanup operations

**Data Flow:**
```javascript
// Read daily conversations from Google Sheets
const conversations = await readSheet('AI_Memory_Buffer');

// Process with AI for summarization
const summary = await aiAgent.summarize(conversations);

// Generate structured Markdown
const markdown = generateMarkdown(summary);

// Upload to dated folder
await uploadToDrive(markdown, `05_Daily_Logs/Log_${today}.md`);
```

## Advanced Integration Patterns

### Multi-Modal Input Handling

**Problem:** Handling both text and audio inputs in AI assistants.

**Solution:**
```javascript
// Check for audio in webhook payload
if ($json.body.audio) {
  // Route to audio processing
  const transcription = await groq.transcribe($json.body.audio);
  return { text: transcription, type: 'audio' };
} else {
  // Direct text processing
  return { text: $json.body.message, type: 'text' };
}
```

**Node Configuration:**
- **If Node**: Conditional routing based on `$json.body.audio`
- **HTTP Request**: Groq API for Whisper transcription
- **Set Node**: Normalize audio and text inputs to common format

### Error Handling & Resilience Patterns

**Global Error Handler:**
```javascript
// Capture all workflow errors
const error = {
  timestamp: new Date(),
  workflow: $json.workflow.name,
  executionId: $json.execution.id,
  error: $json.execution.error.message,
  stack: $json.execution.error.stack
};

// Log to Google Sheets
await logError(error);

// Send notification
await sendNotification(error);
```

**Retry Logic with Backoff:**
```javascript
let attempts = 0;
const maxAttempts = 3;

while (attempts < maxAttempts) {
  try {
    const result = await riskyOperation();
    return result;
  } catch (error) {
    attempts++;
    if (attempts < maxAttempts) {
      await sleep(Math.pow(2, attempts) * 1000); // Exponential backoff
    }
  }
}
throw new Error('Operation failed after retries');
```

### Tool Integration Best Practices

**Google Drive Tool Usage:**
```javascript
// Search with specific queries
const searchResults = await googleDrive.search({
  query: "name contains 'Strategy' and mimeType='application/vnd.google-apps.document'",
  folderId: knowledgeBaseFolderId
});

// Download specific files
const fileContent = await googleDrive.download({
  fileId: selectedFileId,
  binaryProperty: 'data'
});

// Use in AI context
const context = `Based on this document: ${fileContent}`;
```

**API Authentication Patterns:**
```javascript
// Service Account for Google APIs
const credentials = {
  type: "service_account",
  project_id: process.env.GOOGLE_PROJECT_ID,
  private_key: process.env.GOOGLE_PRIVATE_KEY,
  client_email: process.env.GOOGLE_CLIENT_EMAIL
};

// API Key for external services
const headers = {
  'Authorization': `Bearer ${process.env.API_KEY}`,
  'Content-Type': 'application/json'
};
```

## Performance Optimization

### Workflow Execution Optimization

**Batch Processing Strategies:**
```javascript
// Process items in controlled batches
const batchSize = 10;
const batches = chunkArray(items, batchSize);

for (const batch of batches) {
  await Promise.all(batch.map(item => processItem(item)));
  await sleep(1000); // Rate limiting
}
```

**Memory Management:**
```javascript
// Clear large data structures after processing
let largeData = await loadData();
const processed = await processData(largeData);
largeData = null; // Free memory

// Use streaming for large files
const stream = fs.createReadStream(largeFile);
stream.pipe(processingPipeline);
```

### AI Integration Optimization

**Context Window Management:**
```javascript
// Keep conversations focused
const recentMessages = conversation.slice(-10); // Last 10 messages
const context = recentMessages.map(msg => ({
  role: msg.sender,
  content: msg.content.substring(0, 500) // Truncate long messages
}));
```

**Tool Selection Logic:**
```javascript
// Only attach necessary tools
const tools = [];

if (query.includes('search') || query.includes('find')) {
  tools.push(googleDriveSearchTool);
}

if (query.includes('download') || query.includes('read')) {
  tools.push(googleDriveDownloadTool);
}

// Attach tools to agent
agent.tools = tools;
```

## Monitoring & Debugging

### Logging Patterns

**Structured Logging:**
```javascript
const logEntry = {
  timestamp: new Date(),
  workflow: workflowName,
  executionId: executionId,
  step: currentStep,
  dataSize: data.length,
  duration: Date.now() - startTime,
  status: success ? 'success' : 'error',
  error: error?.message
};

await appendToSheet(logEntry, 'System_Logs');
```

### Health Checks

**Workflow Self-Monitoring:**
```javascript
// Daily health check
const healthMetrics = {
  timestamp: new Date(),
  workflowsActive: await countActiveWorkflows(),
  executionsToday: await countExecutions(),
  errorsToday: await countErrors(),
  storageUsed: await checkStorageUsage()
};

await sendHealthReport(healthMetrics);
```

## Security Considerations

### API Key Management

**Environment Variables:**
```bash
# .env file
N8N_WEBHOOK_URL=https://your-n8n-instance.com
GOOGLE_SERVICE_ACCOUNT_KEY=your-key-here
GROQ_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
```

**Credential Rotation:**
```javascript
// Implement key rotation logic
if (isKeyExpired(currentKey)) {
  const newKey = await refreshKey(currentKey);
  updateEnvironment('API_KEY', newKey);
}
```

### Data Privacy

**Sensitive Data Handling:**
```javascript
// Redact sensitive information
const safeData = {
  ...originalData,
  apiKey: '[REDACTED]',
  password: '[REDACTED]',
  personalInfo: '[REDACTED]'
};
```

## Migration & Versioning

### Workflow Updates

**Backward Compatibility:**
```javascript
// Version detection
const workflowVersion = $json.version || '1.0';

// Apply version-specific logic
if (workflowVersion === '1.0') {
  // Legacy processing
} else {
  // New processing
}
```

### API Changes

**Graceful Degradation:**
```javascript
try {
  // Try new API
  const result = await newApiCall();
  return result;
} catch (error) {
  // Fallback to old API
  console.warn('New API failed, using fallback');
  return await oldApiCall();
}
```

This comprehensive guide covers the core patterns and best practices for building robust n8n automation workflows based on real-world implementations.
