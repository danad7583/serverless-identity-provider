# Reusable OIDC Infra Deployment Factory

This package contains only the `infra/oidc_cfn` deployment infrastructure. It does not modify the OIDC Lambda/application source code.

## Layout

```text
infra/oidc_cfn/
  templates/
    foundation.yml   # shared artifact bucket, KMS keys, logs, signing key, revocation table, secret
    network.yml      # reusable VPC exports, Lambda SG, execute-api VPCE, API endpoint SG
    app.yml          # OIDC-specific application CloudFormation template
    pipeline.yml     # reusable CodePipeline/CodeBuild/CloudFormation deployment factory
  pipeline/
    buildspec.yml    # packages Lambda zips and runs aws cloudformation package
```

## Design

The current OIDC deployment is treated as the first consumer of a reusable deployment pattern.

```text
foundation.yml
  -> creates encrypted artifact bucket and shared runtime/security resources

network.yml
  -> creates reusable network/security-group resources and exports them

pipeline.yml
  -> imports foundation/network outputs by stack name
  -> builds source through CodeBuild
  -> deploys the repo-specific application template

buildspec.yml
  -> creates Lambda zip files locally
  -> runs aws cloudformation package
  -> emits build/output/packaged-app.yml

app.yml
  -> references local Lambda zip paths
  -> aws cloudformation package rewrites those paths into S3 artifact references
```

## No hardcoded infrastructure values

The pipeline no longer expects fixed VPC IDs, subnet IDs, security group IDs, KMS ARNs, Secrets Manager ARNs, or artifact bucket names.

Instead, `pipeline.yml` accepts:

- `FoundationStackName`
- `NetworkStackName`
- app/repo injection parameters

and imports the required values from those stacks.

## Artifact bucket

The foundation stack keeps the artifact bucket. It is used for:

- CodePipeline artifact storage
- `aws cloudformation package` uploads
- review snapshots under `snapshots/`
- packaged deployment objects under `packaged/`

The old separate source/staging bucket is removed from foundation. Source comes from either:

- an existing external S3 object source, or
- CodeStar Source Connection for repo-based deployments.

## Deployment order

```text
1. Deploy templates/foundation.yml
2. Deploy templates/network.yml
3. Deploy templates/pipeline.yml
4. Start the pipeline
```

For the next repo, reuse foundation/network and deploy another pipeline stack with different source/app parameters.
