# P2 Envelope Audit Report

This report documents the envelope shapes (request/response wrappers) for P2 domains
as extracted from the OpenAPI spec via spec inspection.

## Findings Summary

| Domain | Verdict | Reason |
|--------|---------|--------|
| services | CONFIRMED_WRAPPED | Named wrapper: "service" |
| roles | CONFIRMED_FLAT | No wrapper detected in any endpoint |
| resource_groups | CONFIRMED_WRAPPED | Named wrapper: "resourceGroup" |
| role_assignments | CONFIRMED_WRAPPED | Named wrapper: "role-assignment" |

---

## SERVICES

**Verdict:** CONFIRMED_WRAPPED

**Evidence:** Named wrapper: "service"

### Envelope Contract

| Property | Value |
|----------|-------|
| List envelope | direct_array (unwrap: None) |
| Singleton envelope | wrapped_named (unwrap: service) |
| Request body wrapper | flat (wrapper: None) — NOTE: contradicts singleton finding; verify live |
| unwrap_field (list) | None |
| unwrap_field (singleton) | service |

## ROLES

**Verdict:** CONFIRMED_FLAT

**Evidence:** No wrapper detected in any endpoint

### Envelope Contract

| Property | Value |
|----------|-------|
| List envelope | direct_array (unwrap: None) |
| Singleton envelope | flat (unwrap: None) |
| Request body wrapper | flat (wrapper: None) |
| unwrap_field (list) | None |
| unwrap_field (singleton) | None |

## RESOURCE_GROUPS

**Verdict:** CONFIRMED_WRAPPED

**Evidence:** Named wrapper: "resourceGroup"

### Envelope Contract

| Property | Value |
|----------|-------|
| List envelope | direct_array (unwrap: None) |
| Singleton envelope | flat (unwrap: None) |
| Request body wrapper | wrapped_named (wrapper: resourceGroup) |
| unwrap_field (list) | None |
| unwrap_field (singleton) | None |

## ROLE_ASSIGNMENTS

**Verdict:** CONFIRMED_WRAPPED

**Evidence:** Named wrapper: "role-assignment"

### Envelope Contract

| Property | Value |
|----------|-------|
| List envelope | direct_array (unwrap: None) |
| Singleton envelope | wrapped_named (unwrap: role-assignment) |
| Request body wrapper | flat (wrapper: None) — NOTE: contradicts singleton finding; verify live |
| unwrap_field (list) | None |
| unwrap_field (singleton) | role-assignment |

