NODE: change-correlation

## Trigger

Run after scope and integrity have been assessed, especially when a recent deployment or configuration change is suspected.

## Inspect

Compare the deployment timeline with symptom onset. Inspect the changed components, feature flags, migrations, canary behavior, and plausible competing causes.

## Pass

The change is supported or ruled out strongly enough to guide the next action, with the decisive evidence stated.

## Reject

The conclusion rests only on timing, the relevant diff is unknown, or credible competing causes remain unchecked.

## On rejection

Do not guess a cause. Ask a human to inspect the deployment diff and current telemetry before remediation continues.
