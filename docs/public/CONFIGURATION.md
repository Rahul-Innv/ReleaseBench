# Configuration

ReleaseBench 0.1.0 has no runtime configuration file, environment-variable contract, network daemon, or
credential store. The plugin is loaded from its directory and its skills are invoked by name.

Credentials are never ReleaseBench configuration. Any later host or registry action belongs to the
owner's authenticated tool or browser session, happens only after a separate approval, and must not
place tokens in this repository, prompts, fixtures, logs, or evidence.

If ReleaseBench later introduces a real configuration format, it must ship a schema, safe defaults,
validation fixtures, migration guidance, and explicit secret-handling rules before that format can be
called stable.
