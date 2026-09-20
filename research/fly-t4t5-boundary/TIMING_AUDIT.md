# Pre-fit timing correction

The metadata audit of all 17 compact input arrays found 5 ms intervals for flash/moving-bar traces and 2.5 ms for apparent-motion/static-grating/drifting-grating traces. The initial protocol's blanket 5 ms description was incomplete. No fit or model comparison has run. Retain every supplied observation at its original time; do not relabel or discard half the samples.

B1 exponential filters use each trace's actual interval and the already registered time constants/delays. B0 remains a 5 ms operator; on 2.5 ms observations it advances at every second sample and holds its last response between updates. No interpolation is fit. This is a declared baseline discretization limitation, not new physiology. All flash fitting and selection remain on 5 ms data, so this correction does not change the registered training objective or candidate families.
