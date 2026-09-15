# Connectivity provenance and reuse

Source: [OpenWorm ConnectomeToolbox](https://github.com/openworm/ConnectomeToolbox), commit `b9c0b4a7bc2ccf47d3ce7aac624e1b3e2ea86254`, `cect/cache/Cook2019HermReader.json` and `cect/Cells.py`.

The source is OpenWorm's processed export of Cook et al., **Whole-animal connectomes of both Caenorhabditis elegans sexes**, Nature 571, 63–71 (2019), DOI https://doi.org/10.1038/s41586-019-1352-7. Its reader selects the WormWiring adjacency matrices corrected July 2020. We preserve all 302 named hermaphrodite neurons and extract only neuron-to-neuron connections; non-neuronal cells are excluded. Electrical pairs are stored once after verifying exact matrix symmetry. Chemical direction and raw weights are retained. Weights measure EM serial sections of connectivity, not physiological strength or number of distinct synapses.

## License verification, 2026-09-14

The pinned repository distributes its processed files under MIT; the exact notice is retained at `source/LICENSE`. OpenWorm explicitly states that its code, data and models are MIT licensed at https://openworm.org/ ("Open Science at its best"). This is the reuse basis for **this OpenWorm distribution**. We do not claim that the Nature article, original micrographs, or every third-party source are MIT licensed; they are not redistributed here. Attribute both the original authors and OpenWorm. This is a documented provenance assessment, not a legal opinion about every upstream artifact.

Run `python3 scripts/import-connectome.py` to regenerate the runtime JSON without network access. Original downloaded files are retained under `source/`; SHA-256 values are embedded in the generated provenance. No random graph, inferred missing edges, or anonymous replacement neurons are introduced.
