# README generation experiment: manuscript section and appendix

The section below is written for an OSA paper. It reports the
`readme_2026_three_models` run, completed by 22 October 2026, and a secondary
judge pass completed on 23 October 2026. We audited the retained logs on 23
October 2026. Both tables use only scores whose generated README is still
present, exclude observed upstream-reference retrievals, and use the same
repositories for all 15 conditions. The appendix records the dataset,
prompts, failures, and cost assumptions.

## Manuscript section: README generation

### Experimental design

We evaluated README generation on 48 public GitHub repositories frozen at
specific commits: 30 in the dataset's **Common** group and 18 in its
**Scientific** group. The full repository list and revisions appear in
Appendix A. We saved each repository's original root README as an evaluation
reference, removed it from a local Git snapshot, and gave every generator a
fresh isolated worktree of that snapshot. Other tracked files, including
documentation below the root, remained available. This prevented direct
reading of the local reference while preserving the same pinned source state
for all methods. Network access was not fully contained, as the audit below
shows.

We crossed three OpenRouter generator models—`openai/gpt-6-luna`,
`anthropic/claude-haiku-5.5`, and `z-ai/glm-5.3-flash`—with five methods,
for 720 planned outputs. **Base** sent one fixed README-writing prompt plus a
deterministically selected repository tree and source text to the model, capped
at 64,000 `cl100k_base` tokens. **OSA** ran its advanced local README workflow:
repository context collection, section planning, deterministic and model-written
sections, assembly, and internal review. **ReadMeReady (RR)** summarized files
and folders, built a local embedding index with
`sentence-transformers/all-mpnet-base-v2`, and generated named README sections.
**LArch** built context with its `file_names` context creator, made one
generation request, and post-processed the response. **OpenCode (OC)** used a
README-writing agent with repository read and edit access. Its configured shell,
`webfetch`, and task permissions were denied, but the agent's `execute` tool
could still fetch remote pages in three observed runs. Each method used the same generator
model within a model arm, although the workflows made different numbers of
requests and used different context-selection strategies. The pinned tool
versions and operational prompts are in Appendix D.

We used DeepEval 4.3.1 G-Eval with `openai/gpt-6-sol` as a single LLM judge.
For each output, its actual-output field contained the generated README and
JSON repository structure, while its expected-output field contained the
original README. Six fixed evaluation steps asked about consistency with the
structure, project overview, setup, examples, requirements, and readability.
The judge returned an integer from 0 to 10, which the installed G-Eval version
normalized to a score from 0 to 1. The exact benchmark-defined instructions,
the installed template, and the request wrapper are in Appendix C. The reported
score is a reference-conditioned LLM judgment; it is not a human-verified
factuality measure.

The run retained 691 nonempty generated READMEs. Generation succeeded for all
144 Base, OSA, and LArch conditions, 141/144 OC conditions, and 118/144 RR
conditions. We excluded missing outputs and malformed or stale score rows.
For the main comparison, a repository was included only when all 15 conditions
had a valid score and retained README and no run log showed retrieval of its
upstream reference. This left 34 paired repositories: 22/30 Common and 12/18
Scientific. We calculated each table entry as the
arithmetic mean of the relevant repositories' normalized scores; no missing
score was imputed.

### Results

**Table 1.** Mean G-Eval README-quality scores on the same complete
repositories for each model and group. Base is the direct LLM prompt, RR is
ReadMeReady, and OC is OpenCode. Bold marks the largest displayed value within
each model and row. The 0–1 scale is higher-is-better.

| Repo type (complete / total) | Luna Base | Luna RR | Luna LArch | Luna OSA | Luna OC | Haiku Base | Haiku RR | Haiku LArch | Haiku OSA | Haiku OC | GLM Base | GLM RR | GLM LArch | GLM OSA | GLM OC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Common (22 / 30) | 0.71 | 0.38 | 0.60 | 0.45 | **0.75** | 0.70 | 0.28 | 0.55 | 0.55 | **0.76** | **0.70** | 0.45 | 0.52 | 0.59 | 0.69 |
| Scientific (12 / 18) | **0.85** | 0.32 | 0.53 | 0.46 | 0.83 | 0.83 | 0.26 | 0.52 | 0.56 | **0.84** | 0.79 | 0.40 | 0.52 | 0.71 | **0.82** |
| All (34 / 48) | 0.76 | 0.36 | 0.57 | 0.45 | **0.78** | 0.75 | 0.27 | 0.54 | 0.56 | **0.79** | 0.73 | 0.43 | 0.52 | 0.63 | **0.74** |

The direct baseline and OpenCode received the highest mean scores in all three
model arms. OSA did not lead the overall quality table: its all-repository
means were 0.45 with Luna, 0.56 with Haiku, and 0.63 with GLM. Nevertheless,
OSA exceeded ReadMeReady under every model by 0.09, 0.28, and 0.20 points,
respectively. It also exceeded LArch with Haiku by 0.01 and with GLM by 0.11;
with Luna, LArch was ahead by 0.12. These are paired descriptive comparisons
on the same 34 repositories. OSA's 144/144 successful outputs are a separate
practical advantage over RR's 118/144 and OC's 141/144 output coverage. In the
Scientific subset with GLM, OSA reached 0.71, compared with 0.52 for LArch
and 0.40 for RR, though Base and OC scored 0.79 and 0.82.

The judge's reasons give a useful, limited explanation of the pattern. Strong
OSA cases were credited for navigable sections, setup guidance, and concrete
examples (for example, Python Fire, TagGenerator, and Code Contribution
Analyzer).
Lower-scoring OSA cases were frequently missing runnable setup or usage detail,
or summarized a large repository too narrowly. Across all saved outputs,
OSA's median README was 563 words, versus 1,267 for Base and 877 for OC.
This shorter output, OSA's bounded context, and the baseline's larger
64,000-token source budget are plausible contributors to lower coverage
scores; this experiment does not isolate their causal effects. The protocol
also tested OSA's from-scratch generation path: it withheld the existing
README and supplied no research-paper attachment. OSA's ability to update
existing documentation or use paper context was therefore not measured.
The result suggests a specific improvement target: retain OSA's reliable,
structured workflow while expanding evidence selection and checking that
generated setup and examples are actionable.

### Secondary judge: GLM 5.3 Flash

We scored the same 691 retained outputs again with DeepEval G-Eval, replacing
only the judge model with `z-ai/glm-5.3-flash`. No README was regenerated. We
applied the same rubric, repository references, complete-case rule, and
reference-access exclusions as in Table 1. The paired set therefore remains
22/30 Common and 12/18 Scientific repositories. These means are a sensitivity
analysis; their absolute values should not be compared as if the two judges
shared a calibrated scoring scale.

**Table 2.** Mean G-Eval README-quality scores with GLM 5.3 Flash as judge.
Columns, bolding, and the 0–1 scale follow Table 1. The same 34 paired
repositories contribute to both tables.

| Repo type (complete / total) | Luna Base | Luna RR | Luna LArch | Luna OSA | Luna OC | Haiku Base | Haiku RR | Haiku LArch | Haiku OSA | Haiku OC | GLM Base | GLM RR | GLM LArch | GLM OSA | GLM OC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Common (22 / 30) | **0.88** | 0.44 | 0.71 | 0.62 | 0.81 | 0.85 | 0.37 | 0.75 | 0.75 | **0.86** | **0.93** | 0.56 | 0.72 | 0.83 | 0.79 |
| Scientific (12 / 18) | **0.94** | 0.33 | 0.65 | 0.48 | 0.83 | **0.92** | 0.34 | 0.67 | 0.71 | 0.88 | **0.93** | 0.49 | 0.65 | 0.78 | 0.85 |
| All (34 / 48) | **0.90** | 0.40 | 0.69 | 0.57 | 0.82 | **0.88** | 0.36 | 0.72 | 0.74 | 0.87 | **0.93** | 0.54 | 0.69 | 0.81 | 0.81 |

With this judge, the direct baseline leads every model arm on the full paired
set. OSA's full-set means are 0.57, 0.74, and 0.81 for Luna, Haiku, and GLM,
respectively; each exceeds the corresponding RR mean and the Haiku and GLM
LArch means. The order of OC and OSA changes between judges for some cells,
so the two tables support method-specific findings more strongly than an
overall ranking. GLM also judged outputs generated by GLM in one model arm;
possible same-model preference is another reason to treat this pass as a
sensitivity analysis rather than an independent ground truth.

### Cost and threats to validity

OpenRouter returned per-call cost metadata for all 144 baseline generations
($1.9406) and 694 recorded GPT-6 Sol judge calls ($24.4295). The secondary
GLM judge's final 691 score rows retain $1.1904 of per-call cost metadata;
an earlier progress total was $1.2413 before four retries, so the final-row
sum does not reconstruct its full billed cost. The OpenCode session
database recorded $4.0561 across its model calls, including attempted sessions.
At the 22 October 2026, 20:06 UTC account check, the key reported $56.3506
cumulative inference usage. If the key was dedicated to this experiment, the
remaining $25.9244
is attributable collectively to OSA, ReadMeReady, LArch, and any unrecorded
attempts. The runners did not save the response usage for those three tools;
therefore their individual billed costs cannot be measured from the retained
artifacts. Appendix E supplies an explicitly hypothetical call-count
allocation, not an empirical price ranking. Local embedding compute, host
resources, and credit-purchase fees are outside the inference totals.

The missingness is systematic. RR failed on 26 cells, often because a large
prompt exceeded the model context window or a job reached the 30-minute
timeout; OC failed on three GLM cells. Of the 36 mechanically complete
repositories, we excluded `ChatGLM-6B` and `system-design-primer` after the
GLM/OpenCode logs showed the agent fetching an upstream README through its
`execute` tool. A third observed case, `PyTorch-GAN`, was already incomplete.
The agent configuration denied `webfetch`, but this did not prevent network
access through `execute`. Thus the table describes 34 paired repositories,
and the logs do not prove that other sessions never accessed reference text.
The local original README was withheld from generation and used as the judge's
reference. It sometimes
contained information unavailable in the remaining repository files, such as
a project-status notice or a curated catalog; such cases can disadvantage any
source-only generator. Conversely, an original README can itself be incomplete.
The fixed repository list was not a random sample of open-source projects.
We used one primary judge model and one secondary model on the same outputs,
one generation per condition, no independent human ratings, and no controlled
study of provider routing, prompt length, or
sampling variance. Scores are coarse 0.1 increments in this implementation.
Future work should have reviewers check source-supported claims and runnable
commands, and should report quality with failure coverage and measured
per-request usage together. [DeepEval's G-Eval documentation](https://deepeval.com/docs/metrics-llm-evals)
also notes that LLM judging is not deterministic.

## Appendix A. Repositories and pinned revisions

The groups are the labels in the benchmark dataset. Every link below points
to the pinned GitHub commit. The original root README at that commit was
stored separately for judging and removed from the generator input.

| # | Group | Repository at pinned commit | Commit SHA | Commit date (UTC) |
| ---: | --- | --- | --- | --- |
| 1 | Common | [AntonOsika/gpt-engineer](https://github.com/AntonOsika/gpt-engineer/commit/a90fcd543eedcc0ff2c34561bc0785d2ba83c47e) | `a90fcd543eedcc0ff2c34561bc0785d2ba83c47e` | 2024-11-17 |
| 2 | Common | [THUDM/ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B/commit/401bf3a8a7dd8a26fba189551dccfc61a7079b4e) | `401bf3a8a7dd8a26fba189551dccfc61a7079b4e` | 2024-06-27 |
| 3 | Common | [OpenEthan/SMSBoom](https://github.com/OpenEthan/SMSBoom/commit/38ccbeccb05fab66442988b38b559062d7cf92d8) | `38ccbeccb05fab66442988b38b559062d7cf92d8` | 2024-03-20 |
| 4 | Common | [lra/mackup](https://github.com/lra/mackup/commit/45a9929f1117de2b26e7f6264453eb1546882116) | `45a9929f1117de2b26e7f6264453eb1546882116` | 2025-06-10 |
| 5 | Common | [chenfei-wu/TaskMatrix](https://github.com/chenfei-wu/TaskMatrix/commit/4b7664f8d3a23804ac1b795d75a73efd162769f0) | `4b7664f8d3a23804ac1b795d75a73efd162769f0` | 2023-06-29 |
| 6 | Common | [hacksider/Deep-Live-Cam](https://github.com/hacksider/Deep-Live-Cam/commit/f0fae811d86d05e8b94f31deec8b5456525f6b7b) | `f0fae811d86d05e8b94f31deec8b5456525f6b7b` | 2025-06-29 |
| 7 | Common | [google/python-fire](https://github.com/google/python-fire/commit/dba7e1d0da014e555d174225fdf5ab4c4574b18b) | `dba7e1d0da014e555d174225fdf5ab4c4574b18b` | 2025-06-01 |
| 8 | Common | [stitionai/devika](https://github.com/stitionai/devika/commit/3b98ed31e22cd2893563d4b375c2538c72a2e224) | `3b98ed31e22cd2893563d4b375c2538c72a2e224` | 2024-09-19 |
| 9 | Common | [Pythagora-io/gpt-pilot](https://github.com/Pythagora-io/gpt-pilot/commit/4ab9367875d9a2cfbee3aec4d3e74b4ae544fc96) | `4ab9367875d9a2cfbee3aec4d3e74b4ae544fc96` | 2025-06-30 |
| 10 | Common | [CorentinJ/Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning/commit/440322b8ff93ed1cca1d954f781bcfbe83429d23) | `440322b8ff93ed1cca1d954f781bcfbe83429d23` | 2025-05-30 |
| 11 | Common | [encode/httpx](https://github.com/encode/httpx/commit/4fb9528c2f5ac000441c3634d297e77da23067cd) | `4fb9528c2f5ac000441c3634d297e77da23067cd` | 2025-06-27 |
| 12 | Common | [lss233/kirara-ai](https://github.com/lss233/kirara-ai/commit/8295a5deda0b289a3f70d946064b6c9a3e1b0753) | `8295a5deda0b289a3f70d946064b6c9a3e1b0753` | 2025-06-28 |
| 13 | Common | [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher/commit/c368d61307e15541fd388451684b90bed4aed42d) | `c368d61307e15541fd388451684b90bed4aed42d` | 2025-06-26 |
| 14 | Common | [mkdocs/mkdocs](https://github.com/mkdocs/mkdocs/commit/4c7404485f988f409ccaf42fefe705222ff5965a) | `4c7404485f988f409ccaf42fefe705222ff5965a` | 2025-02-21 |
| 15 | Common | [ageitgey/face_recognition](https://github.com/ageitgey/face_recognition/commit/2e2dccea9dd0ce730c8d464d0f67c6eebb40c9d1) | `2e2dccea9dd0ce730c8d464d0f67c6eebb40c9d1` | 2022-06-10 |
| 16 | Common | [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer/commit/b02784ffeb2846d6b0418003b7529e68dfb69fd9) | `b02784ffeb2846d6b0418003b7529e68dfb69fd9` | 2025-05-21 |
| 17 | Common | [chatanywhere/GPT_API_free](https://github.com/chatanywhere/GPT_API_free/commit/6b755516b65c18d4b6204f6f3b79c5554e5177ca) | `6b755516b65c18d4b6204f6f3b79c5554e5177ca` | 2025-06-28 |
| 18 | Common | [Asabeneh/30-Days-Of-Python](https://github.com/Asabeneh/30-Days-Of-Python/commit/3c70b160757c0e7d1f704fbc132d246db89dcaa0) | `3c70b160757c0e7d1f704fbc132d246db89dcaa0` | 2025-06-04 |
| 19 | Common | [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper/commit/045205730c164ae6192b99538f1ca666de75d19a) | `045205730c164ae6192b99538f1ca666de75d19a` | 2024-01-05 |
| 20 | Common | [twintproject/twint](https://github.com/twintproject/twint/commit/e7c8a0c764f6879188e5c21e25fb6f1f856a7221) | `e7c8a0c764f6879188e5c21e25fb6f1f856a7221` | 2021-03-02 |
| 21 | Common | [pallets/flask](https://github.com/pallets/flask/commit/85c5d93cbd049c4bd0679c36fd1ddcae8c37b642) | `85c5d93cbd049c4bd0679c36fd1ddcae8c37b642` | 2025-06-12 |
| 22 | Common | [charlax/professional-programming](https://github.com/charlax/professional-programming/commit/9a5d23500c4e6d61ecd48ba47f9a838662736a37) | `9a5d23500c4e6d61ecd48ba47f9a838662736a37` | 2025-06-30 |
| 23 | Common | [ethereum/EIPs](https://github.com/ethereum/EIPs/commit/01fa73bba14cfaee77de3f954364f53c7180c3ac) | `01fa73bba14cfaee77de3f954364f53c7180c3ac` | 2025-06-30 |
| 24 | Common | [xai-org/grok-1](https://github.com/xai-org/grok-1/commit/7050ed204b8206bb8645c7b7bbef7252f79561b0) | `7050ed204b8206bb8645c7b7bbef7252f79561b0` | 2024-03-19 |
| 25 | Common | [eriklindernoren/PyTorch-GAN](https://github.com/eriklindernoren/PyTorch-GAN/commit/36d3c77e5ff20ebe0aeefd322326a134a279b93e) | `36d3c77e5ff20ebe0aeefd322326a134a279b93e` | 2021-01-06 |
| 26 | Common | [public-apis/public-apis](https://github.com/public-apis/public-apis/commit/675a4e63bae5cf0f6569254652fce3e2fa53b900) | `675a4e63bae5cf0f6569254652fce3e2fa53b900` | 2025-05-20 |
| 27 | Common | [Z4nzu/hackingtool](https://github.com/Z4nzu/hackingtool/commit/c43f290df520d886d87e9db212eb946a0799f61c) | `c43f290df520d886d87e9db212eb946a0799f61c` | 2025-03-03 |
| 28 | Common | [gto76/python-cheatsheet](https://github.com/gto76/python-cheatsheet/commit/8b2d95d3b229591de39fad047a318c792cde5164) | `8b2d95d3b229591de39fad047a318c792cde5164` | 2025-06-21 |
| 29 | Common | [danielgatis/rembg](https://github.com/danielgatis/rembg/commit/2cc87501606bcb07878739196ec8cc4979362c52) | `2cc87501606bcb07878739196ec8cc4979362c52` | 2025-06-10 |
| 30 | Common | [bregman-arie/devops-exercises](https://github.com/bregman-arie/devops-exercises/commit/2a9bfcb78b85bb9ead2028acb9db0fac88ed0dd3) | `2a9bfcb78b85bb9ead2028acb9db0fac88ed0dd3` | 2025-04-24 |
| 31 | Scientific | [Vision-CAIR/MiniGPT-4](https://github.com/Vision-CAIR/MiniGPT-4/commit/d94738a7626ec43eba6c2cddf3cd2043f1a9689a) | `d94738a7626ec43eba6c2cddf3cd2043f1a9689a` | 2024-09-02 |
| 32 | Scientific | [Jack-Cherish/python-spider](https://github.com/Jack-Cherish/python-spider/commit/60b7ed839713ccf00bb30fe2b203a6b45d7459aa) | `60b7ed839713ccf00bb30fe2b203a6b45d7459aa` | 2024-08-19 |
| 33 | Scientific | [openai/chatgpt-retrieval-plugin](https://github.com/openai/chatgpt-retrieval-plugin/commit/b28ddce58474441da332d4e15c6dd60ddaa953ab) | `b28ddce58474441da332d4e15c6dd60ddaa953ab` | 2024-04-24 |
| 34 | Scientific | [black-forest-labs/flux](https://github.com/black-forest-labs/flux/commit/474dc4205306cb76c46ba510e35eec7bbed5efd1) | `474dc4205306cb76c46ba510e35eec7bbed5efd1` | 2025-06-27 |
| 35 | Scientific | [sb-ai-lab/EmotiEffLib](https://github.com/sb-ai-lab/EmotiEffLib/commit/90690cda1644819d7c83b914db46a6d7e7efbd91) | `90690cda1644819d7c83b914db46a6d7e7efbd91` | 2025-06-01 |
| 36 | Scientific | [sb-ai-lab/Ride](https://github.com/sb-ai-lab/Ride/commit/97cc3a91980c21d7370144a4c05e559bc6d94438) | `97cc3a91980c21d7370144a4c05e559bc6d94438` | 2025-06-24 |
| 37 | Scientific | [hse-cs/delPezzo](https://github.com/hse-cs/delPezzo/commit/ba4736fbdab7619c7899bf8888feb422d25fcc88) | `ba4736fbdab7619c7899bf8888feb422d25fcc88` | 2025-03-25 |
| 38 | Scientific | [deeppavlov/chatsky](https://github.com/deeppavlov/chatsky/commit/cdfae50d96a2662dcf601c64455ac6c5db52c4df) | `cdfae50d96a2662dcf601c64455ac6c5db52c4df` | 2025-02-18 |
| 39 | Scientific | [deeppavlov/dialog2graph](https://github.com/deeppavlov/dialog2graph/commit/ae074dd16c3a578b3fdea94ba0a7b7132a27a199) | `ae074dd16c3a578b3fdea94ba0a7b7132a27a199` | 2025-06-26 |
| 40 | Scientific | [corl-team/verl-loras](https://github.com/corl-team/verl-loras/commit/992b9caf0123afce321b3f98252b4390216099a3) | `992b9caf0123afce321b3f98252b4390216099a3` | 2025-05-07 |
| 41 | Scientific | [sb-ai-lab/Eco2AI](https://github.com/sb-ai-lab/Eco2AI/commit/366debb262c50568abb8c5551706b08512163c7a) | `366debb262c50568abb8c5551706b08512163c7a` | 2025-03-10 |
| 42 | Scientific | [AIRI-Institute/GENA_LM](https://github.com/AIRI-Institute/GENA_LM/commit/6545a8a322be0f73d0f3a8fb480e6a28c318547e) | `6545a8a322be0f73d0f3a8fb480e6a28c318547e` | 2025-01-17 |
| 43 | Scientific | [AIRI-Institute/eco4cast](https://github.com/AIRI-Institute/eco4cast/commit/125bc1bf54b41b194a06e853848fe93b71e3a384) | `125bc1bf54b41b194a06e853848fe93b71e3a384` | 2024-06-18 |
| 44 | Scientific | [Vishnu-tppr/Camouflage-AI](https://github.com/Vishnu-tppr/Camouflage-AI/commit/1ac6cdf0f94a445c406ccb113fa0f12821a44189) | `1ac6cdf0f94a445c406ccb113fa0f12821a44189` | 2025-05-18 |
| 45 | Scientific | [tbhvishal/Python-Weather-Info-App](https://github.com/tbhvishal/Python-Weather-Info-App/commit/ca8133826796ed790d2e160f4ca0a9a2487b8d69) | `ca8133826796ed790d2e160f4ca0a9a2487b8d69` | 2025-05-10 |
| 46 | Scientific | [readytensor/rt-repo-assessment](https://github.com/readytensor/rt-repo-assessment/commit/5f8acb131b0e0243dd9b8732cdb9eb16c9139d7c) | `5f8acb131b0e0243dd9b8732cdb9eb16c9139d7c` | 2025-05-01 |
| 47 | Scientific | [DadaNanjesha/TagGenerator](https://github.com/DadaNanjesha/TagGenerator/commit/f3ea722a71cbcdfc863896e1e025c2675be912be) | `f3ea722a71cbcdfc863896e1e025c2675be912be` | 2025-03-14 |
| 48 | Scientific | [stephenombuya/Code-Contribution-Analyzer](https://github.com/stephenombuya/Code-Contribution-Analyzer/commit/0e418b3aeca0953b81a8303cef88fba6321f2805) | `0e418b3aeca0953b81a8303cef88fba6321f2805` | 2025-01-28 |

## Appendix B. Direct-baseline prompt and repository-text selection

The following shows the **exact fixed instruction text and prompt layout**
sent as the sole user message, with repository-specific parts shown as
placeholders:

```text
Create a complete README.md for this project from the repository text below. Describe only information supported by the supplied files. Include relevant overview, setup, usage, configuration, development, testing, and license sections. Return only Markdown, starting with a level-one heading. Aim for 800-1500 words.

Repository file tree:
<TRACKED_FILE_TREE>

Selected file contents:
--- <PATH> ---
<FILE_TEXT>
```

The angle-bracketed material represents per-repository substitution, not
literal prompt text. The runner listed tracked files, sorted the tree, and
selected text files by priority: manifests and requirements, entry points,
documentation, other non-test files, then tests. It skipped root README files,
symlinks, known secret filenames, binary and undecodable files. It read at most
250,000 bytes and 10,000 `cl100k_base` tokens from any file and capped the
entire message at 64,000 tokens; the tree could use at most a quarter of that
budget. Each baseline output's adjacent JSON manifest records the actual
selected files, token counts, and truncation. No explicit temperature or
random seed was supplied to OpenRouter.

## Appendix C. Judge instructions and prompt template

The benchmark configured this criterion in `evaluation.py`. With explicit
evaluation steps in DeepEval 4.3.1, the scoring request uses the six steps
below rather than asking the judge to invent steps from the criterion:

```text
Determine whether the AI-generated Readme file (ACTUAL_OUTPUT)
is better than the original one (EXPECTED_OUTPUT).
ACTUAL_OUTPUT contains two fields: 'readme', which contains the generated README itself,
and 'repo_structure' which is json with repository's structure.
Generated README's content must be consistent with the provided repository structure.
The ACTUAL_OUTPUT does not necessary have to be the same as EXPECTED_OUTPUT,
Your goal is to determine which text is better, using the provided Evaluations steps.
Readme structure does not matter much as long as it passes the evaluation steps.
```

The **exact supplied evaluation steps** were:

```text
Step 1: Does the provided structure of the repository address README content?
Step 2: Does the README provide a clear and accurate overview of the repository's purpose?
Step 3: Are installation and setup instructions included and easy to follow?
Step 4: Are usage examples provided and do they clearly demonstrate functionality?
Step 5: Are dependencies or requirements listed appropriately?
Step 6: Is the README easy to read, well-structured, and free of confusing language?
```

The wrapper sent `openai/gpt-6-sol` a system message,
`You are a strict JSON generator. Reply with one JSON object only.`, and a
user message generated by the installed DeepEval template. Below is its
**substantive user-message template**, with case-specific content replaced by
placeholders and blank-line spacing normalized. DeepEval prefixes the step
numbers, so `Step 1` appears twice.

```text
You are an evaluator. Given the following evaluation steps, assess the response below and return a JSON object with two fields:

- `"score"`: an integer between 0 and 10, with 10 indicating strong alignment with the evaluation steps and 0 indicating no alignment.
- `"reason"`: a brief explanation for why the score was given. This must mention specific strengths or shortcomings, referencing relevant details from the input. Do **not** quote the score itself in the explanation.

Your explanation should:
- Be specific and grounded in the evaluation steps.
- Mention key details from the test case parameters.
- Be concise, clear, and focused on the evaluation logic.

Only return valid JSON. Do **not** include any extra commentary or text.

---

Evaluation Steps:
1. Step 1: Does the provided structure of the repository address README content?
2. Step 2: Does the README provide a clear and accurate overview of the repository's purpose?
3. Step 3: Are installation and setup instructions included and easy to follow?
4. Step 4: Are usage examples provided and do they clearly demonstrate functionality?
5. Step 5: Are dependencies or requirements listed appropriately?
6. Step 6: Is the README easy to read, well-structured, and free of confusing language?

Test Case:
Actual Output:
{"readme": "<GENERATED_README>", "repo_structure": "<REPOSITORY_STRUCTURE_JSON>"}

Expected Output:
<ORIGINAL_README>

Parameters:
Actual Output and Expected Output

---
**Example JSON:**
{
  "reason": "your concise and informative reason here",
  "score": 0
}

JSON:
```

The placeholders were replaced per repository. `ACTUAL_OUTPUT` was
`json.dumps({"readme": generated_readme, "repo_structure": repo_structure},
ensure_ascii=False)`; `EXPECTED_OUTPUT` was the original README's full text.
The `input` field was empty and was not an evaluation parameter. The wrapper
requested JSON-object mode when supported, falling back to a plain completion
on a non-200 response; it did not set a seed or sampling temperature. No
additional rubric was configured. The raw integer was divided by 10 for the
reported score.

## Appendix D. Tool configuration, coverage, and reproducibility

The installed versions were OSA 0.3.2 (commit
`17c347e8648654aee37b741859cfc871e9b46f30`), LArch 0.0.10
(`832d36512531c4a55bc3395c7a67bc9d2c7ccdf4`), ReadMeReady 1.1.5
(`6c45438c7bce05351f4e91a06af3ab38e236aa0f`, with the local output-path
and concurrency patch), and OpenCode CLI 2.1.2. The full version manifest is
`../tool_versions.json`. The benchmark used the installed sources under
`.tools/src/`, not the older checked-in copies of the compared tools.

OSA used `--mode advanced --web-mode --readme --no-fork --no-pull-request`,
with the selected model for README and general calls. Its connector setup was
adapted for OpenRouter to omit unsupported sampling arguments; its README
workflow remained OSA's own. ReadMeReady used the selected model for
generation, local MPNet embeddings, and the headings Description,
Requirements, Installation, Usage, Contributing, and License. Its file and
folder summary prompts were, respectively, `Write a concise technical
explanation of this code file in markdown.` and `Write a concise technical
explanation of this folder in markdown.` LArch used a `file_names` context
creator and the seed `# README\n\nWrite a complete README from this
repository.\n`. OpenCode's agent prompt was: `Inspect this repository and
write a complete, accurate README.md. Create only README.md in the current
directory. Start with a level-one heading. Do not invent unsupported
claims.`

| Method | Planned cells | Retained outputs | Failed cells |
| --- | ---: | ---: | ---: |
| Base | 144 | 144 | 0 |
| OSA | 144 | 144 | 0 |
| ReadMeReady | 144 | 118 | 26 |
| LArch | 144 | 144 | 0 |
| OpenCode | 144 | 141 | 3 |
| **Total** | **720** | **691** | **29** |

Twelve repositories lacked at least one retained result and were excluded
from the paired table: `gpt-researcher`, `30-Days-Of-Python`, `flask`,
`EIPs`, `PyTorch-GAN`, `python-cheatsheet`, `EmotiEffLib`, `Ride`,
`dialog2graph`, `verl-loras`, `Eco2AI`, and `GENA_LM`. The dominant
ReadMeReady failure modes were model context overflow and the 1,800-second
runner timeout; one case also produced invalid JSON during processing.
Three GLM OpenCode attempts ended nonzero. The raw evaluation CSV contains
three scored rows for OpenCode outputs later removed by failed attempts and
one malformed row. The corrected report requires both a `done` generation
status and an existing output file; these four rows do not enter its means.
The three valid but orphaned judge calls remain in billed judge cost.

The provenance audit records three GLM/OpenCode sessions that fetched
upstream README text in `evaluation/reference_access.csv`, with the supporting
logs retained. `ChatGLM-6B` and `system-design-primer` would otherwise have
entered the paired table; `PyTorch-GAN` was already excluded for incomplete
output coverage. The audit applies the same whole-repository exclusion to all
methods and models, keeping the paired comparison aligned.

On the 34 paired repositories, OSA's wins/ties/losses against ReadMeReady
were 23/7/4 with Luna, 34/0/0 with Haiku, and 29/4/1 with GLM. Against
LArch they were 4/5/25, 14/11/9, and 19/13/2, respectively. These counts
are descriptive, with ties common because the judge uses 0.1 score steps.
The per-cell scores and reasons, original README references, retained
outputs, failure logs, and corrected summary table are in
`../results/readme_2026_three_models/`. The compact run record is included
in this repository; downloaded source trees and intermediate workspaces are
listed by pinned revision and regenerated by the preparation phase.

## Appendix E. Cost accounting and illustrative allocation

The following values are USD inference costs, not credit-purchase fees or
local compute costs. The key-level figure is **cumulative**, so it is the
experiment total only if this OpenRouter key served no unrelated traffic.
OpenRouter bills model usage by token and provider; its
[usage guidance](https://openrouter.ai/support) recommends recording usage
from responses, and its [pricing page](https://openrouter.ai/pricing)
separates inference prices from credit-purchase fees.

| Cost source | Recorded usage | USD | Attribution |
| --- | ---: | ---: | --- |
| Direct baseline | 144 priced generations | $1.9406 | Per-response OpenRouter metadata; $0.0135 per saved README |
| OpenCode | 2,039 priced model messages | $4.0561 | Local OpenCode session database; includes attempts, about $0.0288 per saved README if allocated across 141 outputs |
| GPT-6 Sol judge | 694 priced calls | $24.4295 | Per-response OpenRouter metadata; about $0.0352 per scored call |
| OSA + ReadMeReady + LArch + other unrecorded use | Not separately logged | $25.9244 | Difference from the $56.3506 cumulative key usage; cannot be assigned exactly |

For a sensitivity example only, assume the key was dedicated, that every
recorded OSA completion and LArch generation represented one priced request,
and that ReadMeReady made one request for each logged file and folder plus six
README sections. For RR attempts whose counts were lost in timeout logs,
substitute the within-model median. This produces approximately 2,077 OSA,
14,780 RR, and 144 LArch *proxy* calls. Weight each model's proxy calls by
the observed mean cost of one direct-baseline request for that model, then
allocate the $25.9244 unassigned pool in proportion to those weights:

| Method | Illustrative allocation | Approximate USD per attempted cell |
| --- | ---: | ---: |
| OSA | $3.31 | $0.023 |
| ReadMeReady | $22.40 | $0.156 |
| LArch | $0.21 | $0.0015 |

**These are assumptions, not measured instrument prices.** File/folder
counts do not prove that every processing step made a paid request, prompt
lengths differ substantially, failed jobs can incur partial charges, and
provider routing and caching affect unit price. The malformed score row may
also have lost judge usage, and the key may have served other traffic. For
example, assuming each
OSA call costs three times the proxy unit changes the allocation to about
$7.90 OSA, $17.85 RR, and $0.17 LArch. A longer-than-assumed LArch prompt
would shift money toward LArch. Thus the defensible measured comparison is
the baseline and OpenCode totals plus the combined unassigned pool. A future
replication should log `usage.cost`, input/output tokens, model, method,
repository, and attempt for every instrument request.

