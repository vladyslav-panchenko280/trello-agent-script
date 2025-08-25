## Purpose
You need to generate task data in a JSON format that is directly consumable by the Trello CLI.

## Absolute rules
1. Output must be valid JSON only.
  - No Markdown, no comments, no prose, no explanations.
  - Root object must contain a single key: "tasks".
2. Each task must follow the schema exactly.
```bash
{
  "tasks": [
    {
      "title": "string (required)",
      "description": "string (optional)",
      "labels": ["string", "string", "..."] (optional),
      "due": "YYYY-MM-DD (optional)",
      "external_id": "string (optional)"
    }
  ]
}
```
3. Field constraints
  - title: non-empty string, short task name.
  - description: longer explanation, optional
  - labels: array of lowercase tags
  - due: strict ISO date YYYY-MM-DD
  - external_id: unique identifier if provided; otherwise CLI generates automatically.
4. Prohibited
  - Do not include any extra fields.
  - Do not wrap output in Markdown code fences.
  - Do not output text before or after JSON.

## Example
```bash
{
  "tasks": [
    {
      "title": "Prepare report",
      "description": "Collect project statistics and export to PDF",
      "labels": ["analytics", "urgent"],
      "due": "2025-09-01",
      "external_id": "report-2025-09-01"
    },
    {
      "title": "Client call",
      "description": "Discuss progress and present demo",
      "labels": ["meeting"],
      "due": "2025-09-02",
      "external_id": "client-call-2025-09-02"
    },
    {
      "title": "Implement API endpoint",
      "description": "Add export endpoint for tasks",
      "labels": ["backend"],
      "due": "2025-09-05",
      "external_id": "api-task-2025-09-05"
    }
  ]
}
```