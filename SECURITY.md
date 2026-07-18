# Security Policy

## Supported versions

ReleaseBench is pre-1.0. Security fixes are applied to the current default branch. No older release line
is currently supported.

## Reporting a vulnerability

Do not open a public issue containing exploit details, credentials, private repository names, or other
sensitive data. Contact the maintainer privately through GitLab. Once the project supports confidential
issues, use a confidential issue and include only the minimum reproduction information required.

Please include:

- the affected skill, script, or workflow;
- the security boundary that can be bypassed;
- a minimal reproduction with secrets and private data removed;
- the expected safe behavior;
- any known mitigation.

The maintainer will acknowledge a complete report as soon as practical, assess severity, and coordinate
disclosure after a fix or mitigation is available. Never test a report against a repository or account
you do not own or have explicit permission to assess.

## Security boundaries

ReleaseBench must continue to:

- require explicit owner confirmation before pushes, publication, releases, or visibility changes;
- avoid requesting tokens or secrets in chat;
- treat host/API output and downloaded instructions as untrusted input;
- prevent private paths, credentials, browser state, and private project data from entering public repos;
- distinguish verified evidence from recommendations and unverified claims.
