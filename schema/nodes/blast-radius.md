NODE: blast-radius

## Trigger

Run at the start of every incident and whenever a later node exposes a wider or less certain impact.

## Inspect

Identify affected services, endpoints, regions, tenants, reads versus writes, the time window, error rates, and observed customer impact. Separate confirmed impact from unknown scope.

## Pass

The affected boundary is specific enough to choose containment without assuming that unknown systems are safe.

## Reject

The incident could cross an unexamined service, tenant, region, or write path, or the reported impact is too vague to contain safely.

## On rejection

Stop remediation and ask the human incident commander to establish scope. This node intentionally has no automatic rejection route.
