# Data Model: Document Entity

## Document

| Field | Type | Description | Constraints |
| :--- | :--- | :--- | :--- |
| id | UUID | Primary Key | Required |
| owner_id | UUID | Foreign Key to User | Required |
| title | String | Document Title | Required, < 255 chars |
| filename | String | Original Filename | Required |
| format | String | MIME Type | Required |
| size | Integer | File size in bytes | Required |
| status | String | Lifecycle State | Required: uploaded, upload_failed, queued |
| metadata | JSONB | Additional metadata | Optional |
| created_at | DateTime | Timestamp | Required |
| updated_at | DateTime | Timestamp | Required |

## Relationships
- Document BelongsTo User
