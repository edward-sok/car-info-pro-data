# Changelog

## 2026-10-20 — Fact-check pass 1 (US economy, AU prices)

### US — fuel economy, MPGe and EV range (54 corrections)
Source: EPA official 2025 dataset, https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip
- GR Corolla Core (Auto) mpg 21/28/24 -> 19/27/22
- Prius Plug-in Hybrid SE: city/hwy 53/51 added, EV range 44 -> 45 mi
- GR86 Base hwy 27 -> 26
- GR86 auto 21/31/25 -> 21/30/24
- GR Supra 3.0 auto 22/30/25 -> 23/31/26
- GR Supra manual comb 22 -> 21
- Corolla Cross XLE AWD hwy 32 -> 31
- RAV4 Adventure hwy 32 -> 33
- RAV4 PHEV city/hwy 40/36 added
- Grand Highlander Hybrid MAX 27/28 -> 26/27
- 4Runner TRD Off-Road hwy 24 -> 25
- 4Runner TRD Pro 20/22/21 -> 23/24/23
- Sienna XLE AWD city 35 -> 34
- Sienna Platinum AWD city 35 -> 34
- Tacoma SR city 21 -> 20
- Tacoma TRD Off-Road manual 17/21/19 -> 18/23/20
- Tundra SR hwy 24 -> 23
- Civic Sedan Sport 30/37/33 -> 31/39/34
- Civic Hatchback Sport 30/37/33 -> 30/38/34
- Civic Hatchback Sport Touring Hybrid 46/41/44 -> 50/45/48 (EPA lists one hatch hybrid config)
- CR-V EX AWD 27/32/29 -> 26/31/28
- Passport TrailSport 18/23/20 -> 19/24/21 (EPA lists one Passport AWD config)
- Prologue EX FWD MPGe 113 -> 104
- Prologue Touring AWD MPGe 103 -> 99, range 281 -> 294
- Prologue Elite AWD MPGe 100 -> 95, range 273 -> 283
- F-150 3.5 EcoBoost 4WD 17/23 -> 16/24
- F-150 Raptor city 15 -> 14
- Ranger 2.7 4WD city 18 -> 19
- Ranger Raptor city 17 -> 16
- Maverick Hybrid FWD 42/33/37 -> 42/35/38
- Maverick EcoBoost AWD hwy 29 -> 30
- Mustang EcoBoost 20/30/23 -> 22/33/26
- Mustang GT manual hwy 24 -> 23
- Mustang Dark Horse 15/24/18 -> 14/22/17
- Silverado WT 2.7 2WD 19/22/20 -> 18/21/19
- Silverado 5.3 4WD hwy 20 -> 19
- Silverado Duramax 4WD city 23 -> 22
- Ram 1500 Hurricane SO 2WD 17/23/19 -> 18/25/21
- Ram 1500 HO 4WD hwy 20 -> 21
- Ram 1500 RHO hwy 18 -> 16
- Model 3 LR RWD MPGe 131 -> 137
- Model 3 LR AWD MPGe 125 -> 128
- Model 3 Performance MPGe 113 -> 109
- Model Y LR RWD MPGe 119 -> 125, range 357 -> 337
- Model Y LR AWD MPGe 114 -> 117, range 327 -> 311
- Model Y Performance MPGe 105 -> 104, range 306 -> 277
- Tucson PHEV MPGe 80 -> 77, range 33 -> 32
- CX-5 2.5 S Select 24/30/26 -> 26/30/28 (cylinder deactivation)
- Outback XT city 23 -> 22
- Wrangler 4-door 2.0T 20/24/22 -> 20/22/21
- Wrangler 4xe EV range 21 -> 22
- Wrangler 392 hwy 17 -> 16
- BMW 330i RWD 26/34/29 -> 28/35/31
- BMW M340i xDrive 23/31/26 -> 26/33/29

### AU — prices (13 corrections)
Sources: CarExpert MY25 price lists (carexpert.com.au), 4x4 Australia, OnlineAuto, GoAuto/NRMA.
- HiLux Workmate 4x2 SC 2.7 auto $33,725 -> $28,475 (CarExpert MY25 price list, 26 Oct 2024)
- HiLux SR5 4x4 DC auto (V-Active) $64,135 -> $63,260 (CarExpert MY25)
- HiLux GR Sport $77,000 -> $74,310 (CarExpert MY25; 4x4australia)
- LandCruiser 300 GX $98,000 -> $97,990 (CarExpert / 4x4 Australia MY25 update)
- LandCruiser 300 GXL $107,000 -> $110,820
- LandCruiser 300 Sahara $141,000 -> $139,310
- RAV4 GX Hybrid 2WD $41,000 -> $42,260 (MY25 price list, OnlineAuto 13 Dec 2024)
- RAV4 GXL Hybrid AWD $49,000 -> $48,810
- RAV4 Edge Hybrid AWD $57,000 -> $58,360
- Ranger XLT V6 4x4 $63,000 -> $68,840 (OnlineAuto MY25 list)
- Ranger Wildtrak V6 $72,000 -> $74,840 (CarExpert 2025 listing; OnlineAuto)
- Ranger Wildtrak PHEV $74,000 -> $79,990 (GoAuto, NRMA, Mar 2025)
- Ranger Raptor $88,000 -> $90,440 (OnlineAuto MY25; CarExpert now $90,690)

### Unresolved / not yet verified
- Tacoma TRD Sport 2WD mpg: EPA lists two SR5/Sport/PreRunner 2WD configs (20/24/22, 21/26/23); kept existing value.
- HiLux economy figures: published as ranges by body style; existing values kept.
- Not yet verified: US prices and power, the remaining AU vehicles, all UK and Japan figures.

## 2026-10-19 — Initial publish
- Starter database: 99 vehicles / 242 trims across US (47), AU (22), GB (15), JP (15).
- All figures are indicative (written without per-figure source verification). Monthly
  updates should prioritise verifying and correcting these against official sources.
