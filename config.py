"""
Configuration module for Albion Cost Calculator
Contains material prices, recipes, and API settings
"""

# ===== API Settings =====
BASE_URL = "https://east.albion-online-data.com"
BLACK_MARKET = "Black Market"

# Return rate for crafting
return_rate = 0.152

# API request settings
retries = 5
chunk_size = 7
timeout = 10
concurrent_requests = 7

# Wait time settings
normal_wait_min = 0.4
normal_wait_max = 0.8
throttle_wait_base = 30  # Base wait time when 429 occurs
throttle_wait_max = 60   # Max wait time when 429 occurs

# ===== Material Prices =====
material_prices = {
    # Wood (Plank)
    "T4_PLANK": 343,
    "T4_PLANK@1": 431,
    "T4_PLANK@2": 1725,
    "T5_PLANK": 1006,
    "T5_PLANK@1": 1591,
    "T5_PLANK@2": 5873,
    "T6_PLANK": 2782,
    "T6_PLANK@1": 5351,
    "T6_PLANK@2": 25326,
    "T7_PLANK": 8684,
    "T7_PLANK@1": 20111,
    "T7_PLANK@2": 85267,

    # Metal (Bar)
    "T4_BAR": 331,
    "T4_BAR@1": 557,
    "T4_BAR@2": 2090,
    "T5_BAR": 1063,
    "T5_BAR@1": 1993,
    "T5_BAR@2": 7448,
    "T6_BAR": 2821,
    "T6_BAR@1": 7914,
    "T6_BAR@2": 28361,
    "T7_BAR": 7838,
    "T7_BAR@1": 26684,
    "T7_BAR@2": 89409,

    # Leather
    "T4_LEATHER": 308,
    "T4_LEATHER@1": 443,
    "T4_LEATHER@2": 2120,
    "T5_LEATHER": 1330,
    "T5_LEATHER@1": 2159,
    "T5_LEATHER@2": 8008,
    "T6_LEATHER": 4743,
    "T6_LEATHER@1": 10009,
    "T6_LEATHER@2": 30115,
    "T7_LEATHER": 14129,
    "T7_LEATHER@1": 30536,
    "T7_LEATHER@2": 94615,

    # Cloth
    "T4_CLOTH": 337,
    "T4_CLOTH@1": 434,
    "T4_CLOTH@2": 2094,
    "T5_CLOTH": 1101,
    "T5_CLOTH@1": 1960,
    "T5_CLOTH@2": 5040,
    "T6_CLOTH": 3111,
    "T6_CLOTH@1": 6242,
    "T6_CLOTH@2": 22424,
    "T7_CLOTH": 8677,
    "T7_CLOTH@1": 23730,
    "T7_CLOTH@2": 72775,
}

# ===== Recipes =====
base_recipes = {
    "OFF_SHIELD": {"PLANK": 4, "BAR": 4},
    "OFF_BOOK": {"CLOTH": 4, "LEATHER": 4},
    "OFF_TORCH": {"PLANK": 4, "CLOTH": 4},
    "CAPE": {"CLOTH": 4, "LEATHER": 4},
    "BAG": {"CLOTH": 8, "LEATHER": 8},
    "HEAD_PLATE_SET1": {"BAR": 8},
    "HEAD_PLATE_SET2": {"BAR": 8},
    "HEAD_PLATE_SET3": {"BAR": 8},
    "ARMOR_PLATE_SET1": {"BAR": 16},
    "ARMOR_PLATE_SET2": {"BAR": 16},
    "ARMOR_PLATE_SET3": {"BAR": 16},
    "SHOES_PLATE_SET1": {"BAR": 8},
    "SHOES_PLATE_SET2": {"BAR": 8},
    "SHOES_PLATE_SET3": {"BAR": 8},
    "HEAD_LEATHER_SET1": {"LEATHER": 8},
    "HEAD_LEATHER_SET2": {"LEATHER": 8},
    "HEAD_LEATHER_SET3": {"LEATHER": 8},
    "ARMOR_LEATHER_SET1": {"LEATHER": 16},
    "ARMOR_LEATHER_SET2": {"LEATHER": 16},
    "ARMOR_LEATHER_SET3": {"LEATHER": 16},
    "SHOES_LEATHER_SET1": {"LEATHER": 8},
    "SHOES_LEATHER_SET2": {"LEATHER": 8},
    "SHOES_LEATHER_SET3": {"LEATHER": 8},
    "HEAD_CLOTH_SET1": {"CLOTH": 8},
    "HEAD_CLOTH_SET2": {"CLOTH": 8},
    "HEAD_CLOTH_SET3": {"CLOTH": 8},
    "ARMOR_CLOTH_SET1": {"CLOTH": 16},
    "ARMOR_CLOTH_SET2": {"CLOTH": 16},
    "ARMOR_CLOTH_SET3": {"CLOTH": 16},
    "SHOES_CLOTH_SET1": {"CLOTH": 8},
    "SHOES_CLOTH_SET2": {"CLOTH": 8},
    "SHOES_CLOTH_SET3": {"CLOTH": 8},
    "2H_BOW": {"PLANK": 32},
    "2H_WARBOW": {"PLANK": 32},
    "2H_LONGBOW": {"PLANK": 32},
    "2H_CROSSBOW": {"PLANK": 20, "BAR": 12},
    "2H_CROSSBOWLARGE": {"PLANK": 20, "BAR": 12},
    "MAIN_1HCROSSBOW": {"PLANK": 16, "BAR": 8},
    "MAIN_CURSEDSTAFF": {"PLANK": 16, "BAR": 8},
    "2H_CURSEDSTAFF": {"PLANK": 20, "BAR": 12},
    "2H_DEMONICSTAFF": {"PLANK": 20, "BAR": 12},
    "MAIN_FIRESTAFF": {"PLANK": 16, "BAR": 8},
    "2H_FIRESTAFF": {"PLANK": 20, "BAR": 12},
    "2H_INFERNOSTAFF": {"PLANK": 20, "BAR": 12},
    "MAIN_FROSTSTAFF": {"PLANK": 16, "BAR": 8},
    "2H_FROSTSTAFF": {"PLANK": 20, "BAR": 12},
    "2H_GLACIALSTAFF": {"PLANK": 20, "BAR": 12},
    "MAIN_ARCANESTAFF": {"PLANK": 16, "BAR": 8},
    "2H_ARCANESTAFF": {"PLANK": 20, "BAR": 12},
    "2H_ENIGMATICSTAFF": {"PLANK": 20, "BAR": 12},
    "MAIN_HOLYSTAFF": {"PLANK": 16, "CLOTH": 8},
    "2H_HOLYSTAFF": {"PLANK": 20, "CLOTH": 12},
    "2H_DIVINESTAFF": {"PLANK": 20, "CLOTH": 12},
    "MAIN_NATURESTAFF": {"PLANK": 16, "CLOTH": 8},
    "2H_NATURESTAFF": {"PLANK": 20, "CLOTH": 12},
    "2H_WILDSTAFF": {"PLANK": 20, "CLOTH": 12},
    "MAIN_DAGGER": {"BAR": 12, "LEATHER": 12},
    "2H_DAGGERPAIR": {"BAR": 16, "LEATHER": 16},
    "2H_CLAWPAIR": {"BAR": 12, "LEATHER": 20},
    "MAIN_SPEAR": {"PLANK": 16, "BAR": 8},
    "2H_SPEAR": {"PLANK": 20, "BAR": 12},
    "2H_GLAIVE": {"PLANK": 12, "BAR": 20},
    "MAIN_AXE": {"PLANK": 8, "BAR": 16},
    "2H_AXE": {"PLANK": 12, "BAR": 20},
    "2H_HALBERD": {"PLANK": 20, "BAR": 12},
    "MAIN_SWORD": {"BAR": 16, "LEATHER": 8},
    "2H_CLAYMORE": {"BAR": 20, "LEATHER": 12},
    "2H_DUALSWORD": {"BAR": 20, "LEATHER": 12},
    "2H_QUARTERSTAFF": {"BAR": 12, "LEATHER": 20},
    "2H_IRONCLADEDSTAFF": {"BAR": 12, "LEATHER": 20},
    "2H_DOUBLEBLADEDSTAFF": {"BAR": 12, "LEATHER": 20},
    "MAIN_HAMMER": {"BAR": 24},
    "2H_POLEHAMMER": {"BAR": 20, "CLOTH": 12},
    "2H_HAMMER": {"BAR": 20, "CLOTH": 12},
    "MAIN_MACE": {"BAR": 16, "CLOTH": 8},
    "2H_MACE": {"BAR": 20, "CLOTH": 12},
    "2H_FLAIL": {"BAR": 20, "CLOTH": 12},
    "2H_KNUCKLES_SET1": {"BAR": 12, "LEATHER": 20},
    "2H_KNUCKLES_SET2": {"BAR": 12, "LEATHER": 20},
    "2H_KNUCKLES_SET3": {"BAR": 12, "LEATHER": 20},
}
