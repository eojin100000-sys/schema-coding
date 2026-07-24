NODE: rollback-safety

## Trigger

Run whenever rollback is proposed or implied as the fastest recovery action.

## Inspect

Check schema and data migrations, write compatibility, in-flight jobs, event versions, feature flags, snapshots, and whether the old binary can safely read new writes.

## Pass

Rollback is demonstrably safe, or a safer containment or roll-forward action is selected that protects integrity.

## Reject

Rollback could corrupt or strand writes, compatibility is unverified, or the plan restores availability by accepting unknown integrity risk.

## On rejection

Do not roll back. Route to change-correlation to identify a forward mitigation or narrower containment action.
