# external-cred-provision

Provisions external credentials into secret stores from a declarative YAML context file.

## Usage

```bash
external-cred-provision [OPTIONS] <context-path>
```

```bash
external-cred-provision path/to/context.yaml
```

Dry-run against the same context:

```bash
external-cred-provision --dry-run path/to/context.yaml
```
