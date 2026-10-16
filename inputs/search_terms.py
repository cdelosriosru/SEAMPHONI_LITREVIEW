"""
search_terms.py

The controlled vocabulary for the OpenAlex literature search, grouped by
concept. Editing search coverage should only ever mean editing this file —
the query-building logic in OpenAlex_search_new_counts.py never needs to
change just because a term was added, removed, or reworded.
"""

TERM_GROUPS = {
    # ---- ecosystem-service framing ------------------------------------
    "ES_core": [
        '"ecosystem services"',
        '"ecosystem service"',
        '"ecosystem goods and services"',
        '"natural capital"',
        '"nature contributions to people"',
    ],
    "ES_specific": [
        '"blue carbon"',
        '"carbon sequestration"',
        '"nutrient cycling"',
        '"cultural ecosystem services"',
        '"provisioning services"',
        '"regulating services"',
        'CICES',
    ],
    "ES_diagnostic": [  # noisy: test separately, never in the main tracks
        '"environmental services"',
        '"nature services"',
        '"ecosystem function"',
        '"ecosystem functions"',
        '"ecosystem benefits"',
        'NCP',
    ],
    # ---- how ES are valued / perceived / mapped -----------------------
    "Valuation_monetary": [
        '"choice experiment"',
        '"contingent valuation"',
        '"willingness to pay"',
        '"willingness to accept"',
        '"stated preference"',
        '"revealed preference"',
        '"best-worst scaling"',
        '"benefit transfer"',
        '"valuation experiment"',
        '"choice modelling"',
        '"choice modeling"',
        'conjoint',
        '"travel cost"', '"hedonic pricing"',
        '"economic valuation"',
        '"non-market valuation"',
    ],
    "Perception_social": [
        '"stakeholder perception"',
        '"stakeholders perception"',
        '"perceptions of stakeholders"',
        '"relational values"',
        '"socio-cultural valuation"',
        '"deliberative valuation"',
        '"local ecological knowledge"',
        '"traditional ecological knowledge"',
        '"expert elicitation"',
        '"Q methodology"',
        'Delphi',
        '"focus group"',
        '"focus groups"',
    ],
    "Mapping_participatory": [
        'PPGIS',
        'PGIS',
        '"participatory GIS"',
        '"participatory mapping"',
        '"ecosystem service mapping"',
        '"ecosystem services mapping"',
        '"mapping ecosystem services"',
        '"mapping of ecosystem services"',
    ],
    # ---- ocean side ---------------------------------------------------
    "Ocean_generic": [
        'offshore',
        '"deep sea"',
        '"high seas"',
        '"open ocean"',
        '"marine environment"',
        '"marine ecosystem"',
        '"coastal ecosystem"',
        '"ocean ecosystem"',
        '"oceanic ecosystem"',
        '"submarine ecosystem"',
        '"marine protected area"',
        '"marine protected areas"',
    ],
    "Ocean_habitats": [
        'seamount',
        'seamounts',
        '"cold-water coral"',
        '"sponge ground"',
        '"continental shelf"',
        '"submarine canyon"',
        'pelagic',
        'benthic',
        'mesophotic',
        'seagrass',
        'estuary',
        'estuaries',
        '"tidal flat"',
        '"temperate reefs"',
        '"temperate reef"',
        '"coral reef"',
        '"coral reefs"',
        '"salt marsh"',
        '"mussel bed"',
        '"shellfish reef"',
        '"rocky reef"',
        '"fringing reef"',
        'kelp',
        'lagoon',
    ],
    "Ocean_acronyms": [
        'ABNJ',
        'BBNJ',
        'MPA',
        'MSP',
        'OECM',
    ],
    "Ocean_resources": [
        'fisheries',
        'fishery',
        '"fish stock"',
        '"small-scale fisheries"',
        '"small-scale fishery"'
    ],
    # ---- management / governance in the oceans----------
    "Management": [
        '"marine spatial planning"',
        '"conservation planning"',
        '"co-management"',
        '"area-based management"',
        '"ecosystem-based management"',
    ]
}

