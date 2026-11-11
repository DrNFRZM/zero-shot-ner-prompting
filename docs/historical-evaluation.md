# Historical evaluation from the June 2025 submission

These are saved outputs from the original notebook, not corrected or independently reproduced results.

| Prompt | Saved weighted F1 on 50 test sentences |
|---|---:|
| Baseline | 0.749983 |
| Explanation | 0.761017 |
| Demonstration | 0.750525 |

The development section separately used 50 validation sentences. Both subsets were shuffled with seed 42. Development scores must not be reported as test scores, and neither subset is the full CoNLL-2003 benchmark.

The original conversion used the first three characters of entity types, including MISC -> MIS, and allowed types outside the four CoNLL categories. It also selected the first text match and could overwrite overlapping spans. API/JSON failures could become empty predictions. These defects affect how the scores should be interpreted, so this release does not rank the methods or claim an improvement based on them.

The exact dataset revision, complete evaluated sentence list and response model snapshot were not archived as a replay package. No authorized local dataset export or fresh API evaluation was available to recalculate the results during publication. The saved source notebook remains in the owner's private archive; its text responses and dataset excerpts are not redistributed.

The maintained code has offline checks only. Any later model evaluation needs a separately dated record of data version, subset selection, model identity, alignment decisions and metrics. It must not replace these 2025 outputs as if the corrected method had been used then.
