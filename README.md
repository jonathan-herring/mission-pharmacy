# Mission Pharmacy

Medication inventory and dispensing for pharmacies on short-term medical missions.

## The problem

Short-term medical missions set up clinics for a few days with a pharmacy stocked from donated and purchased supplies. Prescribers usually can't see what the pharmacy has on hand, so they write prescriptions for medications that have already run out. Patients wait, volunteers hunt for substitutes, and the prescriber gets pulled back in.

## Scope (v1)

**Users:** prescribers, pharmacy volunteers, and the mission lead (admin).

1. Prescribers see live stock while prescribing.
2. Dispensing never hands out stock the pharmacy doesn't have, even under simultaneous requests.
3. It keeps working at clinics with poor or no internet and syncs when the connection returns.
4. Every stock change has an append-only audit trail: who, what, when, and why.

**Out of scope for v1:** full EHR or patient charts, billing, cross-mission analytics, native mobile apps.

## Status

Design phase. No application code yet.

## Stack

Python and PostgreSQL. Other components get added when a feature needs them, and each choice is recorded in [`docs/decisions-log.md`](docs/decisions-log.md).
