| Repo type | gpt-6-luna Base | gpt-6-luna RR | gpt-6-luna LArch | gpt-6-luna OSA | gpt-6-luna OC | claude-haiku-5.5 Base | claude-haiku-5.5 RR | claude-haiku-5.5 LArch | claude-haiku-5.5 OSA | claude-haiku-5.5 OC | glm-5.3-flash Base | glm-5.3-flash RR | glm-5.3-flash LArch | glm-5.3-flash OSA | glm-5.3-flash OC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Common | **0.88** | 0.44 | 0.71 | 0.62 | 0.81 | 0.85 | 0.37 | 0.75 | 0.75 | **0.86** | **0.93** | 0.56 | 0.72 | 0.83 | 0.79 |
| Scientific | **0.94** | 0.33 | 0.65 | 0.48 | 0.83 | **0.92** | 0.34 | 0.67 | 0.71 | 0.88 | **0.93** | 0.49 | 0.65 | 0.78 | 0.85 |
| All | **0.90** | 0.40 | 0.69 | 0.57 | 0.82 | **0.88** | 0.36 | 0.72 | 0.74 | 0.87 | **0.93** | 0.54 | 0.69 | 0.81 | 0.81 |

GEval judge: `z-ai/glm-5.3-flash`. Means use the same complete repositories across all 15 cells.
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
| GEval judge | 691 / 691 | $1.1904 |

Other tools do not yet expose per-call costs in their output; no cost is inferred from token counts.
