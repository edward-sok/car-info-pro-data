# Car Info Pro — vehicle database

Live vehicle specs and pricing for the Car Info Pro iOS app (US, Australia, UK, Japan).
The app downloads [`vehicles.json`](vehicles.json) at launch and caches it for offline use.

- `gen_vehicles.py` — source of truth for all data; regenerates `vehicles.json`
- `validate.py` — schema and sanity checks; must pass before publishing
- `UPDATING.md` — monthly update and fact-check process
- `CHANGELOG.md` — what changed in each update, with sources

> Starter data (October 2026) is indicative and is being verified against official
> sources through the monthly updates. Confirm specs and prices with the manufacturer
> or dealer before purchase.
