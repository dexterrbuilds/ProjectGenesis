# Complete direct T4/T5 polarity extraction

The 2021 archive is complete and matches its published MD5. T4/T5 member size/CRC and SHA-256 are recorded separately. The T5 recordings are reused original recordings, not independent replications of 2019. No conditional fit was altered after their recovery.

| Type | Analyzed recordings | Mean traces | Missing explicit repeat counts |
|---|---:|---:|---:|
| T4 | 15 | 2260 | 0 |
| T5 | 17 | 2204 | 2204 |

T4 has an additional slot (ordinal 5), explicitly MATLAB-empty in the source, skipped by the authors’ plotting code. T5 ordinals 3 and 4 contain only contrast 0. Other condition-specific missing values are also preserved rather than filled. T5 `numReps` is absent from the inspected raw-condition group; this extractor leaves the repeat count null rather than inventing it or assuming equality to T4. Singleton MATLAB contrast dimensions are handled without creating missing contrasts.

## Matched author-center comparisons

Mean voltage is computed over [0, flash duration + 75 ms). These are descriptive within-recording pairs, not independent-fly significance tests. Medians of differences need not equal differences of medians.

| Type | Width (pixels) | Duration (ms) | Matched recording pairs | Dark mean (median mV) | Light mean (median mV) | Paired light − dark (median mV) |
|---|---:|---:|---:|---:|---:|---:|
| T4 | 2 | 40 | 15 | -0.772 | 4.978 | 6.266 |
| T4 | 2 | 160 | 15 | -1.416 | 12.552 | 13.539 |
| T5 | 2 | 40 | 14 | 4.396 | -0.332 | -4.299 |
| T5 | 2 | 160 | 14 | 12.122 | -0.532 | -13.396 |

No inference of spikes, calcium, transmitter sign, anatomical column occupancy, FlyWire identity or LPLC2 capability follows from these signed somatic voltages. The fits remain OFF-only conditional T5 models; this descriptive polarity extraction does not retroactively provide held-out polarity prediction. Raw mean traces and full condition metrics are saved in the type-specific NPZ/JSON artifacts.
