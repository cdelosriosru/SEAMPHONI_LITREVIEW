"""
search_terms.py

The controlled vocabulary for the OpenAlex literature search, grouped by
concept. Editing search coverage should only ever mean editing this file —
the query-building logic in OpenAlex_search_new_counts.py never needs to
change just because a term was added, removed, or reworded.
"""

TERM_GROUPS = {
    "ES_core": [
        '"ecosystem services"',
        '"environmental services"',
        '"nature services"',
        '"natural capital"'
    ],
    "ES_valuation": [
        '"choice experiment"',
        '"contingent valuation"',
        '"willingness to pay"',
        '"stated preference"',
        '"stated preferences"',
        '"revealed preference"',
        '"revealed preferences"',
        '"stakeholder perception"',
        '"stakeholder perceptions"',
        '"stakeholders perception"',
        '"stakeholders perceptions"',
        'WTP',
        'WTA',
        '"valuation experiment"',
        '"valuation experiments"',
        'PGIS'
    ],
    "Ocean_context": [
        'offshore',
        '"deep sea"',
        '"high seas"',
        '"marine environment"',
        '"marine ecosystem"',
        '"coastal environment"',
        '"coastal ecosystem"',
        '"ocean environment"',
        '"ocean ecosystem"',
        '"oceanic environment"',
        '"oceanic ecosystem"',
        '"submarine environment"',
        '"submarine ecosystem"'
    ],
    "Ocean_acronyms": [
        'ABNJ',
        'MPA',
        'MSP',
        'OMA',
        'OMAS'
    ],
    "Ocean_resources": [
        'fisheries',
        'coral',
        'fish',
        'fishery'
    ],
    "Management": [
        '"marine spatial planning"',
        '"marine protected area"',
        '"conservation planning"',
        '"participatory mapping"',
        '"co-management"',
        'management'
    ],
    "EF_core" :[
        'biodiversity',
        '"nutrient cycling"',
        '"primary production"',
        '"Ecosystem function"',
        '"Ecosystems functioning"',
        '"energy flow"',
        'regulation',
        '"biological process"',
        '"physiochemical process"'
    ],
    "EF_valuation":[
        '"species distribution"',
        '"organic loading"',
        '"carbon export"',
        '"carbon sequestration"',
        'carbon',
        '"nutrient cycling"',
        'migration',
        '"function groups"',
        '"migration patterns"',
        '"reproductive patterns"',
        'oxygen',
        'trophic',
        'sedimentation',
        'reproduction',
        'turbidity',
        'decomposition'
      ],
      "ESt_core":[
        'producers',
        'consumers',
        '"ecosystem structure"',
        '"ecosystem structures"',
        'light',
        'sunlight',
        'depth',
        'pressure',
        'temperature',
        'salinity',
        'nutrients',
        'oxygen',
        '"vertical zones"'
       ],
      "ESt_valuation":[
        'kelp',
        'seaweed',
        'seaweeds',
        'macroalgae',
        'plankton',
        'pelagic',
        'euphotic',
        'dysophotic',
        'apotic',
        'mesophotic',
        'photosynthesis',
        '"coral reef"',
        'coral',
        'corals',
        '"temperate reefs"',
        '"temperate reef"',
        'seagrass',
        '"seagrass meadows"',
        '"rocky reefs"',
        'estuaries',
        '"larval recruitment"',
        'connectivity',
        'habitats',
        'benthic',
        '"coralline algae"',
        'CCA',
    ],
    "Ecosystem_data_methods": [
        'eDNA',
        '"long-term monitoring"',
        'isotope',
        'isotopes',
        '"remote sensing"',
        'acoustics',
        'metabarcoding',
        'sedimentology',
        'image',
        'drone',
        'restoration'
    ]
}

