NODE: data-integrity

## Trigger

Run when the incident may involve a stateful write path.

## Inspect

Check write failures, invariant violations, replication lag, irreversible mutations, partial migrations, and missing integrity evidence.

## Pass

Corruption risk is excluded by relevant evidence.

## Reject

Integrity remains uncertain, an invariant is broken, or the proposed action could extend irreversible damage.

## On rejection

Block availability-first remediation. Route back to blast-radius so containment includes every affected write path before recovery proceeds.
