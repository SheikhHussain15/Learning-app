# Research: Document Management

**Decision**: Use Supabase Storage for binary files.
**Rationale**: Integrated solution with existing auth, scales well, provides secure private/public access controls via policies.
**Alternatives considered**: 
- Local filesystem (insufficient for production scaling).
- AWS S3 (higher complexity in setup and credential management for this project).

**Decision**: Use PostgreSQL for Document Metadata.
**Rationale**: Consistent with the existing foundation; allows robust transactional integrity for metadata and document lifecycle states.
**Alternatives considered**: 
- NoSQL (unnecessary for relational metadata needs).
