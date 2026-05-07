# mock_data.py
# All fake customers, SKUs, and order history — hardcoded, no external dependencies.

CUSTOMERS = {
    "C001": {
        "name": "Hargrove Mechanical",
        "contact": "Dave Hargrove",
        "email": "dave@hargrove-mech.com",
        "preferred_vendors": ["Parker", "Swagelok"],
        "payment_terms": "Net 30",
        "order_history": [
            {
                "order_id": "ORD-2024-0312",
                "date": "2024-03-12",
                "items": [
                    {"sku": "BF-1002", "qty": 50, "unit_price": 4.25, "description": "1/2\" Brass Compression Fitting"},
                    {"sku": "BF-1005", "qty": 25, "unit_price": 6.80, "description": "3/4\" Brass Elbow 90deg"},
                    {"sku": "SV-2001", "qty": 10, "unit_price": 18.50, "description": "1\" Steel Ball Valve"},
                ],
                "total": 529.50,
                "notes": "usual quarterly restock",
            },
            {
                "order_id": "ORD-2024-0615",
                "date": "2024-06-15",
                "items": [
                    {"sku": "BF-1002", "qty": 50, "unit_price": 4.25, "description": "1/2\" Brass Compression Fitting"},
                    {"sku": "BF-1004", "qty": 30, "unit_price": 5.10, "description": "1/2\" Brass Tee"},
                    {"sku": "PC-3002", "qty": 20, "unit_price": 3.75, "description": "1/2\" PVC Pipe Connector"},
                ],
                "total": 453.50,
                "notes": "",
            },
            {
                "order_id": "ORD-2024-1001",
                "date": "2024-10-01",
                "items": [
                    {"sku": "BF-1002", "qty": 50, "unit_price": 4.25, "description": "1/2\" Brass Compression Fitting"},
                    {"sku": "BF-1005", "qty": 25, "unit_price": 6.80, "description": "3/4\" Brass Elbow 90deg"},
                ],
                "total": 382.50,
                "notes": "same as last time, just the brass",
            },
        ],
    },
    "C002": {
        "name": "Rio Grande Plumbing Supply",
        "contact": "Maria Santos",
        "email": "m.santos@riogrande-supply.com",
        "preferred_vendors": ["Mueller", "Watts"],
        "payment_terms": "Net 15",
        "order_history": [
            {
                "order_id": "ORD-2024-0201",
                "date": "2024-02-01",
                "items": [
                    {"sku": "SV-2003", "qty": 5, "unit_price": 42.00, "description": "2\" Steel Gate Valve"},
                    {"sku": "SV-2004", "qty": 5, "unit_price": 38.00, "description": "1.5\" Steel Gate Valve"},
                    {"sku": "PC-3005", "qty": 100, "unit_price": 1.20, "description": "3/4\" Copper Pipe Connector"},
                ],
                "total": 530.00,
                "notes": "",
            },
            {
                "order_id": "ORD-2024-0820",
                "date": "2024-08-20",
                "items": [
                    {"sku": "SV-2003", "qty": 8, "unit_price": 42.00, "description": "2\" Steel Gate Valve"},
                    {"sku": "BF-1007", "qty": 60, "unit_price": 3.50, "description": "3/8\" Brass Compression Fitting"},
                ],
                "total": 546.00,
                "notes": "rush order",
            },
        ],
    },
    "C003": {
        "name": "Apex Industrial Services",
        "contact": "Tom Beckett",
        "email": "tbeckett@apex-ind.com",
        "preferred_vendors": ["Parker", "Eaton", "Swagelok"],
        "payment_terms": "Net 60",
        "order_history": [
            {
                "order_id": "ORD-2023-1105",
                "date": "2023-11-05",
                "items": [
                    {"sku": "HF-4001", "qty": 20, "unit_price": 22.00, "description": "Hydraulic Fitting 1/4\" NPT"},
                    {"sku": "HF-4002", "qty": 20, "unit_price": 28.00, "description": "Hydraulic Fitting 3/8\" NPT"},
                    {"sku": "SV-2002", "qty": 4, "unit_price": 65.00, "description": "1\" Steel Check Valve"},
                ],
                "total": 1200.00,
                "notes": "",
            },
            {
                "order_id": "ORD-2024-0410",
                "date": "2024-04-10",
                "items": [
                    {"sku": "HF-4001", "qty": 20, "unit_price": 22.00, "description": "Hydraulic Fitting 1/4\" NPT"},
                    {"sku": "HF-4003", "qty": 15, "unit_price": 35.00, "description": "Hydraulic Fitting 1/2\" NPT"},
                    {"sku": "BF-1006", "qty": 40, "unit_price": 7.20, "description": "1\" Brass Union"},
                ],
                "total": 1217.00,
                "notes": "annual maintenance stock",
            },
        ],
    },
    "C004": {
        "name": "Coastline HVAC",
        "contact": "Jenny Park",
        "email": "j.park@coastline-hvac.com",
        "preferred_vendors": ["Honeywell", "Johnson Controls"],
        "payment_terms": "Net 30",
        "order_history": [
            {
                "order_id": "ORD-2024-0305",
                "date": "2024-03-05",
                "items": [
                    {"sku": "BF-1003", "qty": 100, "unit_price": 2.10, "description": "1/4\" Brass Compression Fitting"},
                    {"sku": "PC-3001", "qty": 200, "unit_price": 0.95, "description": "1/4\" Copper Pipe Connector"},
                    {"sku": "SV-2005", "qty": 15, "unit_price": 28.00, "description": "1/2\" Steel Ball Valve"},
                ],
                "total": 820.00,
                "notes": "spring season prep",
            },
            {
                "order_id": "ORD-2024-0901",
                "date": "2024-09-01",
                "items": [
                    {"sku": "BF-1003", "qty": 150, "unit_price": 2.10, "description": "1/4\" Brass Compression Fitting"},
                    {"sku": "PC-3001", "qty": 150, "unit_price": 0.95, "description": "1/4\" Copper Pipe Connector"},
                ],
                "total": 457.50,
                "notes": "fall restock, went lighter on valves",
            },
        ],
    },
    "C005": {
        "name": "Frontier Oilfield Supply",
        "contact": "Ray Dominguez",
        "email": "ray.d@frontier-oilfield.com",
        "preferred_vendors": ["Parker", "Swagelok", "Ham-Let"],
        "payment_terms": "Net 30",
        "order_history": [
            {
                "order_id": "ORD-2024-0115",
                "date": "2024-01-15",
                "items": [
                    {"sku": "HF-4002", "qty": 50, "unit_price": 28.00, "description": "Hydraulic Fitting 3/8\" NPT"},
                    {"sku": "HF-4004", "qty": 30, "unit_price": 45.00, "description": "High-Pressure Hydraulic Fitting 1/2\""},
                    {"sku": "SV-2006", "qty": 8, "unit_price": 120.00, "description": "2\" Steel Globe Valve"},
                ],
                "total": 3310.00,
                "notes": "",
            },
            {
                "order_id": "ORD-2024-0715",
                "date": "2024-07-15",
                "items": [
                    {"sku": "HF-4002", "qty": 50, "unit_price": 28.00, "description": "Hydraulic Fitting 3/8\" NPT"},
                    {"sku": "HF-4004", "qty": 30, "unit_price": 45.00, "description": "High-Pressure Hydraulic Fitting 1/2\""},
                    {"sku": "SV-2006", "qty": 8, "unit_price": 120.00, "description": "2\" Steel Globe Valve"},
                    {"sku": "BF-1008", "qty": 25, "unit_price": 9.50, "description": "1\" Brass NPT Plug"},
                ],
                "total": 3547.50,
                "notes": "same as january, plus plugs",
            },
        ],
    },
}

PRODUCTS = {
    # Brass Fittings
    "BF-1001": {"description": "1/8\" Brass Compression Fitting", "category": "Brass Fittings", "unit_price": 2.80, "unit": "each", "vendor": "Parker", "in_stock": True},
    "BF-1002": {"description": "1/2\" Brass Compression Fitting", "category": "Brass Fittings", "unit_price": 4.25, "unit": "each", "vendor": "Parker", "in_stock": True},
    "BF-1003": {"description": "1/4\" Brass Compression Fitting", "category": "Brass Fittings", "unit_price": 2.10, "unit": "each", "vendor": "Parker", "in_stock": True},
    "BF-1004": {"description": "1/2\" Brass Tee", "category": "Brass Fittings", "unit_price": 5.10, "unit": "each", "vendor": "Swagelok", "in_stock": True},
    "BF-1005": {"description": "3/4\" Brass Elbow 90deg", "category": "Brass Fittings", "unit_price": 6.80, "unit": "each", "vendor": "Parker", "in_stock": True},
    "BF-1006": {"description": "1\" Brass Union", "category": "Brass Fittings", "unit_price": 7.20, "unit": "each", "vendor": "Swagelok", "in_stock": True},
    "BF-1007": {"description": "3/8\" Brass Compression Fitting", "category": "Brass Fittings", "unit_price": 3.50, "unit": "each", "vendor": "Parker", "in_stock": True},
    "BF-1008": {"description": "1\" Brass NPT Plug", "category": "Brass Fittings", "unit_price": 9.50, "unit": "each", "vendor": "Swagelok", "in_stock": True},
    # Steel Valves
    "SV-2001": {"description": "1\" Steel Ball Valve", "category": "Steel Valves", "unit_price": 18.50, "unit": "each", "vendor": "Mueller", "in_stock": True},
    "SV-2002": {"description": "1\" Steel Check Valve", "category": "Steel Valves", "unit_price": 65.00, "unit": "each", "vendor": "Watts", "in_stock": True},
    "SV-2003": {"description": "2\" Steel Gate Valve", "category": "Steel Valves", "unit_price": 42.00, "unit": "each", "vendor": "Mueller", "in_stock": True},
    "SV-2004": {"description": "1.5\" Steel Gate Valve", "category": "Steel Valves", "unit_price": 38.00, "unit": "each", "vendor": "Mueller", "in_stock": True},
    "SV-2005": {"description": "1/2\" Steel Ball Valve", "category": "Steel Valves", "unit_price": 28.00, "unit": "each", "vendor": "Watts", "in_stock": True},
    "SV-2006": {"description": "2\" Steel Globe Valve", "category": "Steel Valves", "unit_price": 120.00, "unit": "each", "vendor": "Parker", "in_stock": True},
    # Pipe Connectors
    "PC-3001": {"description": "1/4\" Copper Pipe Connector", "category": "Pipe Connectors", "unit_price": 0.95, "unit": "each", "vendor": "Nibco", "in_stock": True},
    "PC-3002": {"description": "1/2\" PVC Pipe Connector", "category": "Pipe Connectors", "unit_price": 3.75, "unit": "each", "vendor": "Charlotte Pipe", "in_stock": True},
    "PC-3003": {"description": "3/4\" Steel Pipe Nipple", "category": "Pipe Connectors", "unit_price": 4.50, "unit": "each", "vendor": "Anvil", "in_stock": True},
    "PC-3004": {"description": "1\" Stainless Pipe Connector", "category": "Pipe Connectors", "unit_price": 8.90, "unit": "each", "vendor": "Swagelok", "in_stock": False},
    "PC-3005": {"description": "3/4\" Copper Pipe Connector", "category": "Pipe Connectors", "unit_price": 1.20, "unit": "each", "vendor": "Nibco", "in_stock": True},
    # Hydraulic Fittings
    "HF-4001": {"description": "Hydraulic Fitting 1/4\" NPT", "category": "Hydraulic Fittings", "unit_price": 22.00, "unit": "each", "vendor": "Eaton", "in_stock": True},
    "HF-4002": {"description": "Hydraulic Fitting 3/8\" NPT", "category": "Hydraulic Fittings", "unit_price": 28.00, "unit": "each", "vendor": "Parker", "in_stock": True},
    "HF-4003": {"description": "Hydraulic Fitting 1/2\" NPT", "category": "Hydraulic Fittings", "unit_price": 35.00, "unit": "each", "vendor": "Parker", "in_stock": True},
    "HF-4004": {"description": "High-Pressure Hydraulic Fitting 1/2\"", "category": "Hydraulic Fittings", "unit_price": 45.00, "unit": "each", "vendor": "Swagelok", "in_stock": True},
}

SAMPLE_RFQS = [
    {
        "label": "Vague repeat — Hargrove brass fittings",
        "customer_id": "C001",
        "email": """Hey,

Need to reorder some brass fittings like last time. Same quantities should be fine,
we're running low again. Usual delivery.

Thanks,
Dave
Hargrove Mechanical""",
    },
    {
        "label": "Ambiguous size — Coastline HVAC compression fittings",
        "customer_id": "C004",
        "email": """Hi there,

Can we get a quote on compression fittings? Need a bunch for a new job starting next week.
Probably the same ones we usually get but maybe a size up this time. Let me know on price.

- Jenny
Coastline HVAC""",
    },
    {
        "label": "New product type — Rio Grande wants hydraulics",
        "customer_id": "C002",
        "email": """Hello,

We're branching out a bit — got a client asking for hydraulic fittings now.
Looking for maybe 20-30 units of something in the 3/8 NPT range. Never ordered these before
so let us know what you carry.

Maria
Rio Grande Plumbing Supply""",
    },
    {
        "label": "Exact repeat — Frontier Oilfield semi-annual restock",
        "customer_id": "C005",
        "email": """Ray here.

Time for the semi-annual restock. Same order as July, don't change anything.
Send over the quote when ready.

Ray Dominguez
Frontier Oilfield Supply""",
    },
]
