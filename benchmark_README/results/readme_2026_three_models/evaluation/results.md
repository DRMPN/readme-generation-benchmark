| Repo type | gpt-6-luna Base | gpt-6-luna RR | gpt-6-luna LArch | gpt-6-luna OSA | gpt-6-luna OC | claude-haiku-5.5 Base | claude-haiku-5.5 RR | claude-haiku-5.5 LArch | claude-haiku-5.5 OSA | claude-haiku-5.5 OC | glm-5.3-flash Base | glm-5.3-flash RR | glm-5.3-flash LArch | glm-5.3-flash OSA | glm-5.3-flash OC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Common | 0.71 | 0.38 | 0.60 | 0.45 | **0.75** | 0.70 | 0.28 | 0.55 | 0.55 | **0.76** | **0.70** | 0.45 | 0.52 | 0.59 | 0.69 |
| Scientific | **0.85** | 0.32 | 0.53 | 0.46 | 0.83 | 0.83 | 0.26 | 0.52 | 0.56 | **0.84** | 0.79 | 0.40 | 0.52 | 0.71 | **0.82** |
| All | 0.76 | 0.36 | 0.57 | 0.45 | **0.78** | 0.75 | 0.27 | 0.54 | 0.56 | **0.79** | 0.73 | 0.43 | 0.52 | 0.63 | **0.74** |

GEval judge: `openai/gpt-6-sol`. Means use the same complete repositories across all 15 cells.
Repositories with observed upstream-reference access are excluded from the paired means (3 flagged; see `reference_access.csv`).

| Repo type | Complete / total |
| --- | --- |
| Common | 22 / 30 |
| Scientific | 12 / 18 |
| All | 34 / 48 |

Raw per-cell valid-score coverage, before provenance exclusions, is saved in `cell_coverage.csv`.

| Cost source | Priced calls / recorded calls | Recorded USD |
| --- | --- | ---: |
| Baseline generation | 144 / 144 | $1.9406 |
| GEval judge | 694 / 694 | $24.4295 |

Other tools do not yet expose per-call costs in their output; no cost is inferred from token counts.
