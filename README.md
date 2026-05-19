# Internal OIDC Starter Package

This repository provides a secure, developer-focused foundation for building a serverless OpenID Connect (OIDC)-style identity service. It is designed with a platform-agnostic core and cloud-specific adapters at the edge.

## Purpose

This project is intended for internal R&D, prototyping, and controlled testing of identity and revocation patterns. It is not production-ready and is expected to evolve.

## Design Goals

- Maintain a cloud-neutral core for authentication and revocation logic  
- Require `jti` on all tokens to support deterministic revocation  
- Treat revocation as a first-class validation requirement  
- Use thin handlers and clearly defined service boundaries  
- Isolate AWS-specific implementations to adapters, providers, and stores  

## Current Scope

This package currently focuses on foundational components:

- Core contracts, interfaces, and service boundaries  
- Revocation service and storage model  
- JWT/JWKS service boundaries  
- Claim validation with enforced `jti` requirements  
- Thin, platform-neutral endpoint handlers  
- AWS adapter examples and least-privilege IAM patterns  

## Incomplete Areas

The following capabilities are planned but not yet fully implemented:

- Full OAuth/OIDC authorization flow  
- PKCE and authorization code lifecycle  
- Client registration and authentication backends  
- Token issuance workflows  
- Session management and logout behavior  

## Repository Structure

- `src/internal_oidc/core` – configuration, models, interfaces, services  
- `src/internal_oidc/security` – cryptography and claim validation  
- `src/internal_oidc/handlers` – platform-neutral endpoint logic  
- `src/internal_oidc/adapters` – serverless wrappers (e.g., Lambda)  
- `src/internal_oidc/providers` – key management integrations  
- `src/internal_oidc/stores` – revocation and supporting data stores  
- `infra/aws/iam` – sample least-privilege IAM policies  

## Implementation Roadmap

1. Complete key provider integration and signing/verification support  
2. Implement DynamoDB and Redis revocation stores  
3. Integrate request authentication (Lambda authorizer or in-handler)  
4. Implement token issuance with mandatory `jti` enforcement  
5. Add authorization flow, PKCE support, and client registry  

## Repository and Packaging Notes

- Application code resides under `src/`; infrastructure is under `infra/`  
- Lambda artifacts should include only runtime code and dependencies  
- CloudFormation (`infra/oidc_cfn/templates/app.yml`) deploys multiple Lambda functions from a shared codebase using different handlers  
- CodeBuild produces `oidc-api.zip` and `revoke.zip`, each packaging `internal_oidc/` at the root to align with handler paths  

## Important Notes

- This project is intended for internal use within a controlled environment (e.g., private VPC)  
- Revocation currently requires only an authenticated caller; fine-grained authorization is intentionally deferred during R&D  
- This repository should not be used in production without additional security controls, review, and hardening  