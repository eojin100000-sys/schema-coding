# Sample Incident: Orders API after deployment v1842

At 14:20 UTC, deployment v1842 reached all Orders API instances.
The deployment was 40 minutes ago and changed the reservation write path.
It added a nullable `reservation_token` column and enabled a dual-write.
Six minutes later, checkout 500s rose from 0.8% to 13.7%.
Read-only order-history traffic remains normal.
The primary database reports normal CPU and connection counts.
Replica `orders-db-r3` is 11 minutes behind and logged duplicate-key apply errors.
No invariant check has run against reservations created since the deployment.
About 38,000 rows now contain a new reservation token.
The old binary cannot decode the new version of reservation events.
The latest database snapshot predates the deployment by three hours.
An on-call engineer proposes an immediate binary rollback to restore availability.
A feature flag can disable the new writer, but it has not been tested at current load.
Two customers report duplicate pending charges; neither report is confirmed yet.
The team has not established whether the lagging replica serves any checkout reads.
