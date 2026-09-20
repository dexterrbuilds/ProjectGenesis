# One biological identity; one anatomical record

This is a research schema proposal with a deduplication audit, **not a unified neural model**.

| Record | Canonical key | Required fields / invariant |
|---|---|---|
| Dataset | specimen + materialization + source hash | FAFB adult female, v783; pin annotations independently to v3.1.0. Root changes in another version need explicit lineage, never silent identity substitution. |
| Neuron | dataset + root string | Root remains a decimal string, never IEEE-754 number. Annotation/type aliases and confidence are versioned claims. A physiological population is not an individual root. |
| Local state | neuron key + partition-version + local-label + state-kind | Owner is exactly one neuron. Regions carry anatomical/experimental justification. Voltage, calcium, release and biochemical states are distinct kinds, not automatically one variable. |
| Anatomical contact | dataset + actual upstream contact ID, if supplied | Only possible when contact-level records are available. The current proofread aggregate table does not supply these IDs. Never invent N contacts by appending indices to a count. |
| Aggregate anatomical row | hash(dataset, source hash, pre root, post root, neuropil) | Stores contact count and provenance once. A row is not an independently measured synapse. Conflicting counts fail import. Different neuropils remain different rows. |
| Physiological assignment | row key + evidence/model version | Target/receptor sign, local endpoints, release/observation mapping may be unknown. MB_VL alone does not identify alpha1/alpha2/alpha3 or alpha-prime compartments. Null is retained until crosswalk support exists. |
| Plastic state | row key + model-version + state-kind | One canonical efficacy/eligibility owner per row per alternative model. Alternative experiments may have separate snapshots, never two concurrent rules on one synapse. |
| Intracellular coupling | neuron key + local state pair + evidence/model version | Not an EM chemical edge; must not increase anatomical contact counts. Unknown coupling not inferred from calcium attenuation alone. |
| Modulatory field | compartment identity + transmitter + evidence | Distinct from DAN electrical state and from direct chemical contact. Eligible target membership requires localization evidence. No root-specific receptor map inferred from count/name. |
| Experiment view | list of neuron/row/local-state references | No anatomical duplication. Rules explicitly unresolved or single compatible operator. An incompatible rule conflict blocks composition. |

The executable audit imports only frozen Stage-1/2/3 circuit JSON and assigns no physiology. It verifies that the 4,622 shared KC→MBON07 and 1,053 KC→MBON11 aggregate rows have identical identity/counts and records their IDs. The existing conflict report remains authoritative: different normalization, dopamine projection, acute gating, learning laws and feedback signs are **not reconciled** by deduplicating records.

For a later migration, identity/partition provenance belongs in a research artifact; none of this changes Genesis BrainAdapter, organism records, money, memories or application schema.
