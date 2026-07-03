# external-cred-provision

Provisions external credentials into secret stores from a declarative YAML context file.

## Usage

```bash
external-cred-provision [OPTIONS] <context-path>
```

```bash
external-cred-provision effective-set/external-credential/external-credentials.yaml
```

Dry-run against the same context:

```bash
external-cred-provision --dry-run effective-set/external-credential/external-credentials.yaml
```
