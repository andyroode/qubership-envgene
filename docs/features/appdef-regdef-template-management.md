# AppDef/RegDef Template Management

- [AppDef/RegDef Template Management](#appdefregdef-template-management)
  - [What are Application and Registry Definitions?](#what-are-application-and-registry-definitions)
  - [Purpose and Problem Solved](#purpose-and-problem-solved)
  - [Model and Structure](#model-and-structure)
    - [AppDef Schema](#appdef-schema)
    - [RegDef Schema](#regdef-schema)
  - [Repository and File Structure](#repository-and-file-structure)
    - [Instance Repository Structure](#instance-repository-structure)
    - [Template Repository Structure](#template-repository-structure)
  - [Usage and Consumers](#usage-and-consumers)
    - [Primary Consumers](#primary-consumers)
    - [Access Methods](#access-methods)
  - [Processing during Instance Generation](#processing-during-instance-generation)
  - [Template Creation](#template-creation)
    - [Manual Template Creation](#manual-template-creation)
    - [External Generation](#external-generation)
  - [Transformation Capabilities](#transformation-capabilities)
    - [Configuration for Transformation](#configuration-for-transformation)
    - [Override Patterns](#override-patterns)
    - [Why Transformation is Needed](#why-transformation-is-needed)
  - [Use Cases](#use-cases)
    - [1. Accessing AppDefs/RegDefs from File Structure](#1-accessing-appdefsregdefs-from-file-structure)
    - [2. Creating and Using AppDef/RegDef Templates](#2-creating-and-using-appdefregdef-templates)
    - [3. Transforming AppDefs/RegDefs](#3-transforming-appdefsregdefs)
    - [4. Integrating with External Systems](#4-integrating-with-external-systems)
  - [Related Documentation](#related-documentation)

## What are Application and Registry Definitions?

**Application Definitions (AppDefs)** are configuration files that define applications to be deployed in an environment. They contain:

- Application identifiers (name, artifactId, groupId)
- Registry reference for artifact retrieval
- Deployment parameters (key-value pairs)
- Technical configuration parameters (key-value pairs)
- Deployment behavior flags (e.g., parallel deployment support)

**Registry Definitions (RegDefs)** are configuration files that define artifact repositories used for application deployment. They contain:

- Registry name
- Credentials reference
- Repository configurations for different types (Docker, Maven, NPM, etc.)
- URLs and repository names for different stages (snapshot, staging, release)

Together, these definitions provide the necessary information for locating, retrieving, and configuring applications during environment deployment.

## Purpose and Problem Solved

AppDefs and RegDefs solve several critical challenges in environment configuration management:

1. **Consistent Configuration**: Ensure applications are consistently configured across environments
2. **Environment-Specific Customization**: Allow environment-specific overrides while maintaining a common base
3. **Automated Deployment**: Enable automated environment creation with proper application configurations
4. **Repository Management**: Standardize access to artifact repositories across environments
5. **Separation of Concerns**: Decouple application configuration from deployment details

Without AppDefs and RegDefs, teams would need to manually configure each application for each environment, leading to inconsistencies, errors, and maintenance overhead.

## Model and Structure

### AppDef Schema

```yaml
name: "application-name"                # Application name
registryName: "registry-name"           # Reference to a RegDef
artifactId: "app-artifact-id"           # Artifact identifier
groupId: "com.example"                  # Group identifier
supportParallelDeploy: true             # Parallel deployment flag
deployParameters:                       # Deployment parameters
  param1: "value1"
  param2: "value2"
technicalConfigurationParameters:       # Technical configuration
  tech_param1: "value1"
  tech_param2: "value2"
solutionDescriptor: false               # Optional solution descriptor flag
```

[Complete AppDef JSON Schema](/schemas/appdef.schema.json)

### RegDef Schema

```yaml
name: "registry-name"                   # Registry name
credentialsId: "credentials-id"         # Reference to credentials

# Required repository configurations
mavenConfig:
  repositoryDomainName: "maven.example.com"
  fullRepositoryUrl: "https://maven.example.com"
  targetSnapshot: "snapshots"
  targetStaging: "staging"
  targetRelease: "releases"
  snapshotGroup: "snapshot-group"
  releaseGroup: "release-group"

dockerConfig:
  snapshotUri: "docker.example.com/snapshot"
  stagingUri: "docker.example.com/staging"
  releaseUri: "docker.example.com/release"
  groupUri: "docker.example.com/group"
  snapshotRepoName: "docker-snapshot"
  stagingRepoName: "docker-staging"
  releaseRepoName: "docker-release"
  groupName: "docker-group"

# Optional repository configurations
goConfig:
  goTargetSnapshot: "go-snapshot"
  goTargetRelease: "go-release"
  goProxyRepository: "go-proxy"

# Additional optional configurations for other repository types
# (npmConfig, rawConfig, helmConfig, helmAppConfig)
```

[Complete RegDef JSON Schema](/schemas/regdef.schema.json)

## Repository and File Structure

### Instance Repository Structure

AppDefs and RegDefs are stored in the EnvGene instance repository:

```
/environments/
├── <cluster-name>/
│   └── <env-name>/
│       ├── AppDefs/                # Application Definitions
│       │   ├── app1.yml
│       │   └── app2.yml
│       └── RegDefs/                # Registry Definitions
│           ├── registry1.yml
│           └── registry2.yml
```

### Template Repository Structure

Templates for AppDefs and RegDefs are stored in the template repository:

```
/templates/
├── appdefs/                        # AppDef templates
│   ├── app1.yml.j2
│   └── app2.yml.j2
├── regdefs/                        # RegDef templates
│   ├── registry1.yml.j2
│   └── registry2.yml.j2
└── configuration/
    └── appregdef_config.yaml       # Configuration overrides
```

## Usage and Consumers

### Primary Consumers

1. **Calculator CLI**: Uses AppDefs/RegDefs to resolve application dependencies and configurations
2. **External Systems**: Access AppDefs/RegDefs for integration with deployment tools
3. **EnvGene Core**: Processes AppDefs/RegDefs during environment generation

### Access Methods

Consumers access these files directly from the instance repository file structure. The files are standard YAML and can be parsed using any YAML library.

## Processing during Instance Generation

During environment generation from a template, AppDefs and RegDefs are processed as follows:

1. **Discovery**: AppDef and RegDef templates are discovered in the template repository
2. **Configuration Loading**: Overrides are loaded from `appregdef_config.yaml`
3. **Template Rendering**: Templates are rendered using Jinja2 with:
   - Environment variables
   - Configuration overrides
   - Template-specific variables
4. **Validation**: Rendered files are validated against JSON schemas
5. **Storage**: Final files are saved to the instance repository

This process is handled by the `generate_appregdefs` Ansible role in EnvGene.

## Template Creation

### Manual Template Creation

Templates are created as Jinja2 files (`.j2`) in the template repository:

```yaml
# Example AppDef template (app1.yml.j2)
name: "{{ artifactId }}"
registryName: "{{ appdefs.overrides[app_lookup_key].registry | default('default-registry') }}"
artifactId: "{{ artifactId }}"
groupId: "{{ groupId }}"
supportParallelDeploy: {{ appdefs.overrides[app_lookup_key].supportParallelDeploy | default('true') }}
deployParameters:
  replicas: "{{ appdefs.overrides[artifactId].replicas | default('1') }}"
technicalConfigurationParameters:
  version: "{{ appdefs.overrides[app_lookup_key].version | default('1.0.0') }}"
```

Templates can use:
- Standard Jinja2 syntax
- Variables from environment configuration
- Default values from `appregdef_config.yaml`
- Conditional logic for environment-specific behavior

### External Generation

AppDefs and RegDefs can also be generated by an external job (not part of EnvGene):

1. External job generates the definitions
2. Files are packaged into a `definitions.zip` artifact
3. EnvGene imports these files during environment generation

This is configured using the `APP_REG_DEFS_JOB` pipeline parameter.

## Transformation Capabilities

AppDefs and RegDefs can be transformed during rendering to adapt to different environments or sites.

### Configuration for Transformation

Transformations are controlled by `appregdef_config.yaml`, which can be placed at:
- Global level: `/environments/configuration/appregdef_config.yaml`
- Cluster level: `/environments/<cluster-name>/configuration/appregdef_config.yaml`

### Override Patterns

```yaml
# Global defaults
default_values:
  appdef:
    supportParallelDeploy: true
    deployParameters:
      param1: "default_value1"
  regdef:
    mavenConfig:
      repositoryDomainName: "maven.example.com"

# Pattern-based overrides
override_patterns:
  environment:
    pattern: "{{ env_name }}"
    values:
      dev:
        appdef:
          deployParameters:
            param1: "dev_value1"
      prod:
        appdef:
          deployParameters:
            param1: "prod_value1"
  
  cluster:
    pattern: "{{ cluster_name }}"
    values:
      cluster-01:
        regdef:
          dockerConfig:
            snapshotUri: "docker.cluster01.example.com/snapshot"
```

### Why Transformation is Needed

Transformations enable:
1. **Site-Specific Configuration**: Different sites require different repository URLs
2. **Environment-Specific Parameters**: Production needs different settings than development
3. **Version Control**: Different environments may use different application versions
4. **Cross-Environment Consistency**: Maintain core configuration while allowing customization

## Use Cases

### 1. Accessing AppDefs/RegDefs from File Structure

**As a member of an external team integrating with EnvGene:**

To access AppDefs and RegDefs:
1. Navigate to the instance repository: `/environments/<cluster-name>/<env-name>/`
2. Access AppDefs in the `/AppDefs/` directory
3. Access RegDefs in the `/RegDefs/` directory
4. Parse the YAML files to extract configuration information

These files follow the JSON schemas defined in the EnvGene repository.

### 2. Creating and Using AppDef/RegDef Templates

**As an DevOps Engineer:**

To create and use templates:
1. Create Jinja2 templates in `/templates/appdefs/` and `/templates/regdefs/`
2. Define default values and overrides in `appregdef_config.yaml`
3. Set `app_reg_def_mode: "local"` in `config.yml` to use local templates
4. During environment generation, templates are rendered with appropriate values

This approach ensures consistent configuration across environments while allowing for customization.

### 3. Transforming AppDefs/RegDefs

**As an DevOps Engineer:**

To transform definitions for different environments:
1. Create an `appregdef_config.yaml` with override patterns
2. Define environment-specific or cluster-specific values
3. Place the config file at the appropriate level (global or cluster)
4. During rendering, templates will apply the overrides based on environment context

This enables delivery to different sites with specific configuration requirements.

### 4. Integrating with External Systems

**As an DevOps Engineer:**

To use externally generated definitions:
1. Set up an external job that generates AppDefs and RegDefs
2. Configure the `APP_REG_DEFS_JOB` pipeline parameter with the job name
3. During environment generation, EnvGene will import files from the job artifacts
4. The external files will be placed in the instance repository

This is useful when definitions need to be generated by specialized tools outside of EnvGene.

## Related Documentation

- [EnvGene Configurations](/docs/envgene-configs.md)
- [EnvGene Objects](/docs/envgene-objects.md)
- [Instance Pipeline Parameters](/docs/instance-pipeline-parameters.md)
- [Template Pipeline Parameters](/docs/template-pipeline-parameters.md)
