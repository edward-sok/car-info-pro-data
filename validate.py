#!/usr/bin/env python3
"""Validates vehicles.json before it is published to the app.

Usage:
    python3 validate.py vehicles.json [--previous old_vehicles.json]

Checks that the file matches the schema the iOS app decodes (an invalid file is ignored by the
app, so a broken publish silently stops updates), that every figure is physically plausible, and,
with --previous, that an update doesn't accidentally delete large parts of the database.
Exits non-zero and lists every problem if anything fails.
"""
import json
import re
import sys

SCHEMA_VERSION = 2
UNITS = {"imperial", "metric", "uk", "japan"}
BODY_STYLES = {"sedan", "hatchback", "wagon", "coupe", "suv", "minivan", "truck"}
POWERTRAINS = {"gas", "diesel", "hybrid", "plugInHybrid", "electric"}
RULE_KINDS = {"flat", "marginal", "tiered", "interpolated", "engineClass"}
ENGINE_CLASSES = {"electric", "hybrid", "upTo4", "upTo6", "over6"}
# Plausible new-vehicle base price ranges per currency.
PRICE_RANGES = {"USD": (10_000, 500_000), "AUD": (15_000, 700_000), "GBP": (10_000, 400_000),
                "JPY": (1_000_000, 60_000_000), "EUR": (10_000, 500_000), "CAD": (15_000, 600_000),
                "NZD": (15_000, 700_000)}

TRIM_KEYS = {"name", "msrp", "powertrain", "engine", "horsepower", "torque", "transmission", "drivetrain",
             "mpgCity", "mpgHighway", "mpgCombined", "mpge", "electricRange", "batteryKWh",
             "zeroToSixty", "zeroTo100"}
DIM_KEYS = {"length", "width", "height", "wheelbase", "groundClearance", "curbWeight", "seating", "cargo",
            "cargoMax", "fuelCapacity", "towing", "payload", "bedLength"}
VEHICLE_KEYS = {"id", "market", "make", "model", "year", "bodyStyle", "segment", "generation", "summary",
                "trims", "dimensions", "driveAwayPricing"}
MARKET_KEYS = {"code", "name", "flag", "currency", "locale", "units", "priceLabel", "regionLabel", "taxNote",
               "regions"}

errors = []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def num(where, obj, key, lo, hi, required=True, integer=False):
    v = obj.get(key)
    if v is None:
        if required:
            err(where, f"{key} is required")
        return
    if isinstance(v, bool) or not isinstance(v, (int, float)) or (integer and not isinstance(v, int)):
        err(where, f"{key} must be {'an integer' if integer else 'a number'}, got {v!r}")
        return
    if not lo <= v <= hi:
        err(where, f"{key}={v} outside plausible range {lo}–{hi}")


def text(where, obj, key, required=True):
    v = obj.get(key)
    if v is None and not required:
        return
    if not isinstance(v, str) or not v.strip():
        err(where, f"{key} must be a non-empty string")


def unknown_keys(where, obj, allowed):
    extra = set(obj) - allowed
    if extra:
        err(where, f"unknown keys {sorted(extra)} (the app ignores them; check for typos)")


def validate_rule(where, rule):
    kind = rule.get("kind")
    if kind not in RULE_KINDS:
        err(where, f"rule kind {kind!r} not one of {sorted(RULE_KINDS)}")
        return
    if kind == "flat":
        num(where, rule, "rate", 0, 0.25)
    elif kind in ("marginal", "tiered"):
        brackets = rule.get("brackets") or []
        if not brackets or brackets[-1].get("upTo") is not None:
            err(where, "brackets must be non-empty and end with upTo: null")
        for b in brackets:
            num(where, b, "rate", 0, 0.25)
    elif kind == "interpolated":
        for end in ("low", "high"):
            if not isinstance(rule.get(end), dict):
                err(where, f"interpolated rule needs {end}")
            else:
                num(where, rule[end], "price", 0, 10_000_000)
                num(where, rule[end], "rate", 0, 0.25)
    elif kind == "engineClass":
        rates = rule.get("classRates") or {}
        if set(rates) != ENGINE_CLASSES:
            err(where, f"classRates must have exactly {sorted(ENGINE_CLASSES)}")


def validate_trim(where, t, currency):
    unknown_keys(where, t, TRIM_KEYS)
    text(where, t, "name")
    text(where, t, "engine")
    text(where, t, "transmission")
    text(where, t, "drivetrain")
    pt = t.get("powertrain")
    if pt not in POWERTRAINS:
        err(where, f"powertrain {pt!r} not one of {sorted(POWERTRAINS)}")
    lo, hi = PRICE_RANGES.get(currency, (1, 10**9))
    num(where, t, "msrp", lo, hi, integer=True)
    num(where, t, "horsepower", 30, 1300, integer=True)
    num(where, t, "torque", 30, 1500, required=False, integer=True)
    for k in ("mpgCity", "mpgHighway"):
        num(where, t, k, 5, 150, required=False, integer=True)
    num(where, t, "mpgCombined", 5, 300, required=False, integer=True)
    num(where, t, "mpge", 20, 160, required=False, integer=True)
    num(where, t, "electricRange", 5, 600, required=False, integer=True)
    num(where, t, "batteryKWh", 0.5, 250, required=False)
    num(where, t, "zeroToSixty", 1.5, 25, required=False)
    num(where, t, "zeroTo100", 1.5, 25, required=False)
    if pt == "electric":
        if t.get("electricRange") is None:
            err(where, "electric trims need electricRange")
        if t.get("mpgCombined") is not None:
            err(where, "electric trims should not have mpgCombined")
    elif pt in ("gas", "diesel", "hybrid") and t.get("mpgCombined") is None:
        err(where, "combustion/hybrid trims need mpgCombined")
    if pt == "plugInHybrid" and t.get("electricRange") is None:
        err(where, "plug-in hybrid trims need electricRange")


def validate_dimensions(where, d, body):
    unknown_keys(where, d, DIM_KEYS)
    num(where, d, "length", 100, 260)
    num(where, d, "width", 55, 90)
    num(where, d, "height", 40, 90)
    num(where, d, "wheelbase", 70, 170)
    num(where, d, "groundClearance", 2, 16, required=False)
    num(where, d, "curbWeight", 1200, 9000, integer=True)
    num(where, d, "seating", 1, 9, integer=True)
    num(where, d, "cargo", 1, 200, required=False)
    num(where, d, "cargoMax", 1, 200, required=False)
    num(where, d, "fuelCapacity", 3, 60, required=False)
    num(where, d, "towing", 0, 40_000, required=False, integer=True)
    num(where, d, "payload", 100, 8000, required=False, integer=True)
    num(where, d, "bedLength", 30, 120, required=False)
    if body == "truck" and d.get("bedLength") is None:
        err(where, "trucks need bedLength")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    path = args[0]
    previous = args[args.index("--previous") + 1] if "--previous" in args else None

    try:
        db = json.load(open(path))
    except Exception as e:  # noqa: BLE001
        sys.exit(f"FAIL: {path} is not valid JSON: {e}")

    if db.get("schemaVersion") != SCHEMA_VERSION:
        err("root", f"schemaVersion must be {SCHEMA_VERSION} (the app rejects newer schemas)")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(db.get("updated", ""))):
        err("root", "updated must be an ISO date yyyy-MM-dd")

    markets = db.get("markets") or []
    if not markets:
        err("root", "markets must be non-empty")
    market_currency = {}
    for m in markets:
        where = f"market {m.get('code')}"
        unknown_keys(where, m, MARKET_KEYS)
        for k in ("code", "name", "flag", "currency", "locale", "priceLabel"):
            text(where, m, k)
        if m.get("units") not in UNITS:
            err(where, f"units must be one of {sorted(UNITS)}")
        if m.get("code") in market_currency:
            err(where, "duplicate market code")
        market_currency[m.get("code")] = m.get("currency")
        regions = m.get("regions")
        if not isinstance(regions, list):
            err(where, "regions must be a list (use [] if none)")
            regions = []
        if regions and not m.get("regionLabel"):
            err(where, "markets with regions need a regionLabel")
        for r in regions:
            rw = f"{where} region {r.get('code')}"
            for k in ("code", "name", "taxName"):
                text(rw, r, k)
            validate_rule(rw, r.get("rule") or {})

    vehicles = db.get("vehicles") or []
    seen = set()
    for v in vehicles:
        where = v.get("id", "<no id>")
        unknown_keys(where, v, VEHICLE_KEYS)
        for k in ("id", "make", "model", "segment", "generation", "summary"):
            text(where, v, k)
        if where in seen:
            err(where, "duplicate id")
        seen.add(where)
        if not re.fullmatch(r"[a-z0-9-]+", str(v.get("id", ""))):
            err(where, "id must be lowercase letters, digits and hyphens")
        if v.get("market") not in market_currency:
            err(where, f"market {v.get('market')!r} is not defined in markets")
        if v.get("bodyStyle") not in BODY_STYLES:
            err(where, f"bodyStyle {v.get('bodyStyle')!r} not one of {sorted(BODY_STYLES)}")
        num(where, v, "year", 1990, 2035, integer=True)
        trims = v.get("trims") or []
        if not trims:
            err(where, "needs at least one trim")
        names = [t.get("name") for t in trims]
        if len(names) != len(set(names)):
            err(where, "trim names must be unique within a vehicle")
        for t in trims:
            validate_trim(f"{where} / {t.get('name')}", t, market_currency.get(v.get("market")))
        validate_dimensions(f"{where} dimensions", v.get("dimensions") or {}, v.get("bodyStyle"))

    if previous:
        old = json.load(open(previous))
        old_ids = {v["id"] for v in old.get("vehicles", [])}
        removed = old_ids - seen
        if len(removed) > max(3, len(old_ids) // 10):
            err("diff", f"{len(removed)} vehicles removed (more than 10%): {sorted(removed)[:20]}")
        old_markets = {m["code"] for m in old.get("markets", [])}
        if old_markets - set(market_currency):
            err("diff", f"markets removed: {sorted(old_markets - set(market_currency))}")
        if db.get("updated", "") < old.get("updated", ""):
            err("diff", "updated date is older than the published version; the app would ignore it")

    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    per_market = {c: sum(1 for v in vehicles if v.get("market") == c) for c in market_currency}
    print(f"OK: {len(vehicles)} vehicles, {sum(len(v['trims']) for v in vehicles)} trims, markets {per_market}")


if __name__ == "__main__":
    main()
