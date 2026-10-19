# Monthly data update runbook

This repo is the live database for the **Car Info Pro** iOS app. The app downloads
`vehicles.json` from `main` at launch, so **anything pushed to `main` reaches every user**.
Updates are published automatically, so the fact check below is the only thing standing
between a mistake and the public. Take it seriously.

## Goal of each run

1. Find what changed since the last run in each market (US, AU, GB, JP):
   - New models or new model years on sale
   - Discontinued models (remove only when officially discontinued *and* no longer sold new)
   - Price changes (MSRP / RRP / OTR / Japanese list price)
   - Spec changes (power, torque, economy/range, dimensions, towing)
2. Fix any existing figure that turns out to be wrong. Much of the starter data was written
   from memory and has never been verified; correcting it is as valuable as adding new cars.
3. Publish only figures that pass the fact check.

Keep each run focused: verify and update the most important changes first. It's fine to leave
lower-priority items for the next run (note them in the changelog).

## Fact-check standard (required for every new or changed figure)

- **Primary source required.** Each figure must come from the manufacturer's official site,
  press release or spec sheet for that market, or the official government source:
  - US fuel economy: fueleconomy.gov (EPA)
  - AU fuel economy: greenvehicleguide.gov.au
  - UK: manufacturer UK price list / spec sheet (WLTP)
  - JP: manufacturer Japanese site (WLTC km/L, prices incl. tax)
- **Cross-check with a second independent source** (another official page, or a reputable
  outlet such as Car and Driver, Edmunds, CarExpert, Drive.com.au, Autocar, What Car?,
  Carsensor/Response). If the two disagree, use the official figure; if you can't resolve
  it, **don't change the existing value**. Note it as unresolved in the changelog.
- **Market-specific.** Never copy a US figure into AU/GB/JP or vice versa: power, economy,
  trims and prices differ by market.
- **Units.** Store US units in the data (the generator's `TM`/`DM` helpers convert from
  metric). Prices stay in the market's own currency. US = MSRP excl. destination;
  AU = RRP excl. on-road costs (set `drive_away=True` for brands with national drive-away
  pricing, e.g. Honda); GB = OTR incl. VAT; JP = list price incl. 10% tax.
- **0–60 vs 0–100.** US trims use `zero=` (0–60 mph); other markets use `zero100=`
  (0–100 km/h). Only include acceleration if officially published or consistently tested.
- **No guessing.** If a figure isn't published (e.g. Tesla torque), leave it `None`.
- **Tax rules.** Only change a state's tax rule from the official revenue office page
  (e.g. Revenue NSW, State Revenue Office Victoria, state DMV/department of revenue).

## Steps

1. `git pull`, then keep a copy of the currently published file:
   `cp vehicles.json /tmp/previous.json`
2. Research changes per market (see above), fact-checking each figure.
3. Edit `gen_vehicles.py` (the source of truth; never hand-edit `vehicles.json`).
   - New vehicle ids are generated from make/model/year/market. Keep existing ids stable;
     when a new model year arrives, update that vehicle's `year` and figures in place
     rather than adding a duplicate.
4. Regenerate and validate:
   ```
   python3 gen_vehicles.py vehicles.json
   python3 validate.py vehicles.json --previous /tmp/previous.json
   ```
   Fix every failure. **Never push if validation fails.**
5. Add an entry to the top of `CHANGELOG.md`: date, what changed per market, and the
   source URL(s) for every changed figure, plus anything left unresolved.
6. Commit with a message like `Data update 2026-11-01: 3 new models, 12 price changes`
   and push to `main`.
7. If nothing verifiable changed, don't push a new `vehicles.json`. Just add a short
   "no changes" changelog entry.

## Schema rules (the app breaks silently if these change)

- Don't rename, remove or retype fields. Don't change `schemaVersion`.
- Allowed values: bodyStyle `sedan hatchback wagon coupe suv minivan truck`;
  powertrain `gas diesel hybrid plugInHybrid electric`.
- `validate.py` enforces all of this. If something genuinely needs a schema change, don't
  publish it; describe it in the changelog for the app developer instead.
