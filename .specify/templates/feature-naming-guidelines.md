# Feature Naming Guidelines

## Purpose
Provide consistent naming conventions for feature branches and spec files.

## Branch Naming
- Format: `{FEATURE_NUMBER}-{SHORT-NAME}`
- Number: Sequential starting at 1, increases by 1 for each new major feature
- Short name: 2-4 words, kebab-case, action-noun when possible

## Examples
- "Add user authentication" → "user-auth"
- "Implement OAuth2 integration for the API" → "oauth2-api-integration"
- "Create a dashboard for analytics" → "analytics-dashboard"
- "Fix payment processing timeout bug" → "fix-payment-timeout"
- "Design AI infrastructure for agent orchestration" → "ai-infrastructure"

## Required Components
- Must be descriptive enough to understand feature at a glance
- Must preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
- No spaces or special characters except hyphens

## Workflow
1. Analyze feature description to extract meaningful keywords
2. Create concise short name capturing feature essence
3. Find highest existing number for the short name
4. Use next sequential number + extracted short name for branch name