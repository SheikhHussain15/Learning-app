---
name: constitution-updater
description: Update project constitution by replacing placeholders with concrete values and propagating changes to templates
source: auto-skill
extracted_at: '2026-07-01T15:55:09.525Z'
---

# Constitution Updater Skill

This skill automates the process of updating a project constitution from a template by replacing placeholder tokens with concrete values and ensuring consistency across dependent artifacts.

## Procedure

### 1. Load and Analyze Template
- Read the existing constitution template at `.specify/memory/constitution.md`
- Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`
- Note the number of principles and sections in the template

### 2. Collect/derive Values
- Extract project name and context from existing files (QWEN.md, opencode.md, etc.)
- For governance dates:
  - `RATIFICATION_DATE`: Use existing date or mark as TODO
  - `LAST_AMENDED_DATE`: Set to today's date
- For version (`CONSTITUTION_VERSION`):
  - MAJOR: Backward incompatible changes
  - MINOR: New principle/section added
  - PATCH: Clarifications, typo fixes

### 3. Draft Updated Content
- Replace all placeholder tokens with concrete text
- Organize principles into logical sections (Core Principles, Technical Standards, etc.)
- Include rationale for each principle
- Add governance, success metrics, and amendment process sections

### 4. Consistency Propagation
- Read `.specify/templates/plan-template.md` for Constitution Check alignment
- Read `.specify/templates/spec-template.md` for requirements alignment
- Read `.specify/templates/tasks-template.md` for task categorization
- Check command files in `.specify/templates/commands/` for outdated references

### 5. Create Sync Impact Report
- Prepend as HTML comment at top of constitution file
- Document version changes, modified principles, added/removed sections
- List templates requiring updates with status (✅ updated / ⚠ pending)
- Note any deferred placeholders

### 6. Validate and Write
- Ensure no remaining unexplained bracket tokens
- Verify version line matches report
- Confirm dates are ISO format (YYYY-MM-DD)
- Ensure principles are declarative and testable

### 7. Create PHR
- Write Prompt History Record to `history/prompts/constitution/`
- Include full prompt text and response summary

## When to Use

Use this skill when:
- Initializing a new project's constitution
- Updating an existing constitution with new principles
- Aligning constitution with project evolution
- Migrating from a generic template to project-specific content

## Example

```bash
# Run constitution update
/sp.constitution

# Follow prompts to:
# 1. Review template placeholders
# 2. Confirm project-specific values
# 3. Verify consistency with templates
# 4. Create PHR record
```