---
title: Search strategy
---

[← Back to home](index.md)

# Search strategy

## Explanation of the search

This search maps the literature on ecosystem services offshore, with the aim of informing participatory GIS worksops on 
**perceived** ecosystem services across 6 demonstration sites for the SEAMPHONI project under Horizon Grant. 
The six sites include: Iceland, Madeira, Spanish Mediterranean, Turkish Mediterranean, Wadden Sea, and La Reunion. 
The search is run in OpenAlex. For each query, a first script recovered the number of works recovered and 
and whether a set of known key papers is retrieved, so that the queries can be compared and tuned.

**How queries are built.** Search terms are organised into *term groups* (see Key terms below). Within a group, terms are joined with OR. The groups combined in a query are joined with AND, so a work has to match at least one term from every group in the query. Multi-word and hyphenated terms are quoted and so are searched as exact phrases; single words and acronyms are not quoted.

**Query design.** Each query combines an ecosystem-service and/or method component with one ocean-context group. Four ocean-context groups are used: `Ocean_generic`, `Ocean_habitats`, `Ocean_acronyms` and `Ocean_resources`. Each is run as its own set of queries rather than merged into one list, so that counts can be compared across ocean framings. For every ocean-context group, the same 13 query types are run:

| Query type | Term groups combined | Also run with Management |
|---|---|---|
| `ES_core` | `ES_core` + ocean group | No |
| `es_mapping` | `ES_core` + `Mapping_participatory` + ocean group | Yes |
| `es_perception` | `ES_core` + `Perception_social` + ocean group | Yes |
| `es_valuation` | `ES_core` + `Valuation_monetary` + ocean group | Yes |
| `mapping` | `Mapping_participatory` + ocean group | Yes |
| `perception` | `Perception_social` + ocean group | Yes |
| `valuation` | `Valuation_monetary` + ocean group | Yes |

The six variants that add the `Management` group carry the suffix `_mang`. A query's label is its type followed by the ocean group, for example `es_valuation_mang_Ocean_habitats`. In total this gives 13 query types × 4 ocean groups = 52 queries. The full strings are listed at the end of this page.

**Data and filters.** Queries use OpenAlex's `title_abstract_keywords.search` filter. No other filters are applied, so there is no restriction on publication year, language or document type. Each query is also tested against the key papers listed in `inputs/target_papers.py`, as a check on whether it retrieves papers already known to be relevant. Every run is published as a dated update page with its results table.

## Key terms

The 11 term groups below are defined in `inputs/search_terms.py` (106 terms in total). 9 of them (93 terms) are used in the current queries. Quoted terms are shown here without their quotation marks.

| Term group | Role | Terms |
|---|---|---|
| **ES_core** | Ecosystem services: core framing | ecosystem services, ecosystem service, ecosystem goods and services, natural capital, nature contributions to people |
| **ES_specific** | Ecosystem services: specific services *(not used in current queries)* | blue carbon, carbon sequestration, nutrient cycling, cultural ecosystem services, provisioning services, regulating services, CICES |
| **ES_diagnostic** | Ecosystem services: broader, noisy terms for separate testing *(not used in current queries)* | environmental services, nature services, ecosystem function, ecosystem functions, ecosystem benefits, NCP |
| **Valuation_monetary** | Method: monetary valuation | choice experiment, contingent valuation, willingness to pay, willingness to accept, stated preference, revealed preference, best-worst scaling, benefit transfer, valuation experiment, choice modelling, choice modeling, conjoint, travel cost, hedonic pricing, economic valuation, non-market valuation |
| **Perception_social** | Method: perception and socio-cultural valuation | stakeholder perception, stakeholders perception, perceptions of stakeholders, relational values, socio-cultural valuation, deliberative valuation, local ecological knowledge, traditional ecological knowledge, expert elicitation, Q methodology, Delphi, focus group, focus groups |
| **Mapping_participatory** | Method: participatory mapping | PPGIS, PGIS, participatory GIS, participatory mapping, ecosystem service mapping, ecosystem services mapping, mapping ecosystem services, mapping of ecosystem services |
| **Ocean_generic** | Ocean context: generic ocean terms | offshore, deep sea, high seas, open ocean, marine environment, marine ecosystem, coastal ecosystem, ocean ecosystem, oceanic ecosystem, submarine ecosystem, marine protected area, marine protected areas |
| **Ocean_habitats** | Ocean context: habitats | seamount, seamounts, cold-water coral, sponge ground, continental shelf, submarine canyon, pelagic, benthic, mesophotic, seagrass, estuary, estuaries, tidal flat, temperate reefs, temperate reef, coral reef, coral reefs, salt marsh, mussel bed, shellfish reef, rocky reef, fringing reef, kelp, lagoon |
| **Ocean_acronyms** | Ocean context: acronyms | ABNJ, BBNJ, MPA, MSP, OECM |
| **Ocean_resources** | Ocean context: fishery resources | fisheries, fishery, fish stock, small-scale fisheries, small-scale fishery |
| **Management** | Management and governance | marine spatial planning, conservation planning, co-management, area-based management, ecosystem-based management |

## Other notes

- `ES_specific` and `ES_diagnostic` are defined in `inputs/search_terms.py` 
but are not used in the current 52 queries. 
- Singular and plural forms and UK and US spellings are listed as separate terms (for example `ecosystem service` and `ecosystem services`, `choice modelling` and `choice modeling`).
- This page is a snapshot of the term groups and queries at the time of writing. The source is `inputs/search_terms.py`, and `git log -- inputs/search_terms.py` shows how the terms changed over time.

## Purpose and questions
The specific puporse is to have a list of what we can learn from thelitreature about the 
measurement of ES in the 6 demosites of the project and the threats they face. Below are some
questions that are of interest for the identified literature. There are some guiding questions to 
be answered with this scoping review:

- What are the ecosystem services the literature has studied in **SITE** and surrounding offshore areas? 
- What are the ecosystem services that are most at risk in **SITE** and surrounding offshore areas? What are those risks?
- What are the ecosystem services that local communties perceive they receive from offshore areas in **SITE**?

Where **SITE** can be any oocean and offshore area of (with some caveats and being general here): Iceland, Madeira, Spanish Mediterranean,
Turkish Mediterranean, Wadden Sea, and La Reunion.




## Search queries

The 52 queries run, exactly as sent to OpenAlex.

1. **ES_core_Ocean_generic**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas"))
    ```

2. **es_mapping_Ocean_generic**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas"))
    ```

3. **es_perception_Ocean_generic**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas"))
    ```

4. **es_valuation_Ocean_generic**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas"))
    ```

5. **mapping_Ocean_generic**

    ```text
    ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas"))
    ```

6. **perception_Ocean_generic**

    ```text
    (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas"))
    ```

7. **valuation_Ocean_generic**

    ```text
    (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas"))
    ```

8. **es_mapping_mang_Ocean_generic**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

9. **es_perception_mang_Ocean_generic**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

10. **es_valuation_mang_Ocean_generic**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

11. **mapping_mang_Ocean_generic**

    ```text
    ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

12. **perception_mang_Ocean_generic**

    ```text
    (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

13. **valuation_mang_Ocean_generic**

    ```text
    (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((offshore) OR ("deep sea") OR ("high seas") OR ("open ocean") OR ("marine environment") OR ("marine ecosystem") OR ("coastal ecosystem") OR ("ocean ecosystem") OR ("oceanic ecosystem") OR ("submarine ecosystem") OR ("marine protected area") OR ("marine protected areas")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

14. **ES_core_Ocean_habitats**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon))
    ```

15. **es_mapping_Ocean_habitats**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon))
    ```

16. **es_perception_Ocean_habitats**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon))
    ```

17. **es_valuation_Ocean_habitats**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon))
    ```

18. **mapping_Ocean_habitats**

    ```text
    ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon))
    ```

19. **perception_Ocean_habitats**

    ```text
    (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon))
    ```

20. **valuation_Ocean_habitats**

    ```text
    (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon))
    ```

21. **es_mapping_mang_Ocean_habitats**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

22. **es_perception_mang_Ocean_habitats**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

23. **es_valuation_mang_Ocean_habitats**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

24. **mapping_mang_Ocean_habitats**

    ```text
    ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

25. **perception_mang_Ocean_habitats**

    ```text
    (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

26. **valuation_mang_Ocean_habitats**

    ```text
    (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((seamount) OR (seamounts) OR ("cold-water coral") OR ("sponge ground") OR ("continental shelf") OR ("submarine canyon") OR (pelagic) OR (benthic) OR (mesophotic) OR (seagrass) OR (estuary) OR (estuaries) OR ("tidal flat") OR ("temperate reefs") OR ("temperate reef") OR ("coral reef") OR ("coral reefs") OR ("salt marsh") OR ("mussel bed") OR ("shellfish reef") OR ("rocky reef") OR ("fringing reef") OR (kelp) OR (lagoon)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

27. **ES_core_Ocean_acronyms**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM))
    ```

28. **es_mapping_Ocean_acronyms**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM))
    ```

29. **es_perception_Ocean_acronyms**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM))
    ```

30. **es_valuation_Ocean_acronyms**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM))
    ```

31. **mapping_Ocean_acronyms**

    ```text
    ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM))
    ```

32. **perception_Ocean_acronyms**

    ```text
    (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM))
    ```

33. **valuation_Ocean_acronyms**

    ```text
    (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM))
    ```

34. **es_mapping_mang_Ocean_acronyms**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

35. **es_perception_mang_Ocean_acronyms**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

36. **es_valuation_mang_Ocean_acronyms**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

37. **mapping_mang_Ocean_acronyms**

    ```text
    ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

38. **perception_mang_Ocean_acronyms**

    ```text
    (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

39. **valuation_mang_Ocean_acronyms**

    ```text
    (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((ABNJ) OR (BBNJ) OR (MPA) OR (MSP) OR (OECM)) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

40. **ES_core_Ocean_resources**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery"))
    ```

41. **es_mapping_Ocean_resources**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery"))
    ```

42. **es_perception_Ocean_resources**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery"))
    ```

43. **es_valuation_Ocean_resources**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery"))
    ```

44. **mapping_Ocean_resources**

    ```text
    ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery"))
    ```

45. **perception_Ocean_resources**

    ```text
    (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery"))
    ```

46. **valuation_Ocean_resources**

    ```text
    (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery"))
    ```

47. **es_mapping_mang_Ocean_resources**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

48. **es_perception_mang_Ocean_resources**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

49. **es_valuation_mang_Ocean_resources**

    ```text
    (("ecosystem services") OR ("ecosystem service") OR ("ecosystem goods and services") OR ("natural capital") OR ("nature contributions to people")) AND (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

50. **mapping_mang_Ocean_resources**

    ```text
    ((PPGIS) OR (PGIS) OR ("participatory GIS") OR ("participatory mapping") OR ("ecosystem service mapping") OR ("ecosystem services mapping") OR ("mapping ecosystem services") OR ("mapping of ecosystem services")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

51. **perception_mang_Ocean_resources**

    ```text
    (("stakeholder perception") OR ("stakeholders perception") OR ("perceptions of stakeholders") OR ("relational values") OR ("socio-cultural valuation") OR ("deliberative valuation") OR ("local ecological knowledge") OR ("traditional ecological knowledge") OR ("expert elicitation") OR ("Q methodology") OR (Delphi) OR ("focus group") OR ("focus groups")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```

52. **valuation_mang_Ocean_resources**

    ```text
    (("choice experiment") OR ("contingent valuation") OR ("willingness to pay") OR ("willingness to accept") OR ("stated preference") OR ("revealed preference") OR ("best-worst scaling") OR ("benefit transfer") OR ("valuation experiment") OR ("choice modelling") OR ("choice modeling") OR (conjoint) OR ("travel cost") OR ("hedonic pricing") OR ("economic valuation") OR ("non-market valuation")) AND ((fisheries) OR (fishery) OR ("fish stock") OR ("small-scale fisheries") OR ("small-scale fishery")) AND (("marine spatial planning") OR ("conservation planning") OR ("co-management") OR ("area-based management") OR ("ecosystem-based management"))
    ```
