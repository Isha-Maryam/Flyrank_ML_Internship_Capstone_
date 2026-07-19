# The Prompt Ladder: Prioritizing Content Refreshes

This document tracks the iterative development of a prompt designed to prioritize content pages for review and refreshing based on performance data.

---

## Baseline (Version 0): Genuinely Weak Prompt

### The Prompt
> Help me analyze this content performance data and tell me which pages to refresh.

### Representative Output
> Sure! To analyze your content performance data and decide what to refresh, you should:
> 1. Conduct keyword research to see if search intent has changed.
> 2. Check your page load speed.
> 3. Update old statistics and add new images.
> 4. Fix broken links.
> 5. Make sure your metadata contains your target keywords.
> 
> Let me know if you can upload the data!

---

## Version 1: Clearer Goal
*Targeting the weakness: The baseline prompt was too generic, resulting in general SEO advice instead of page-level prioritization.*

### The Prompt
> **[Goal]** Analyze this content performance data. The objective is to prioritize a list of specific pages that have declined in search visibility so we can refresh them first. Tell me which pages to prioritize.

### Representative Output
> To prioritize pages that have declined in search visibility:
> 1. Look for pages where traffic has dropped by more than 20% compared to last month.
> 2. Identify pages where the average position has dropped but search volume is still high.
> 3. Find older pages that haven't been updated in over 6 months and have declining click-through rates (CTR).
> 
> Please share your data columns (like page URL, impressions, position, last update date) so I can help you prioritize them.

### Analysis Notes
1. **What changed in the prompt**: Added a specific goal (prioritizing pages that declined in search visibility for refreshing).
2. **What actually improved in the output**: The output shifted from generic SEO advice to specific criteria for finding declining pages (e.g., checking >20% drops and position shifts).
3. **What still failed**: The model still cannot analyze any actual data because it doesn't know what columns or performance signals are available.
4. **What to try next**: Provide the real context (the data schema and features of our dataset).

---

## Version 2: Real Context / Data Schema
*Targeting the weakness: The prompt does not reference the actual data columns, preventing the model from giving specific analysis instructions.*

### The Prompt
> Analyze this content performance data. The objective is to prioritize a list of specific pages that have declined in search visibility so we can refresh them first. 
> 
> **[Context]** We are working with a dataset (`content_refresh_anonymized.csv`) containing the following columns:
> - `content_id` (unique page identifier)
> - `impressions_90d` (total organic search impressions over 90 days)
> - `clicks_90d` (clicks over 90 days)
> - `ctr` (click-through rate)
> - `avg_position` (average search ranking position)
> - `days_since_last_update` (days since content was last edited)
> - `scroll_rate` (GA4 user engagement scroll rate)
> - `trend_direction` (overall trend: up, stable, or down)

### Representative Output
> Given your schema, here is how we can prioritize content:
> - **Top Priority**: Focus on pages where `trend_direction` is "down" and `impressions_90d` is high (e.g., >10,000), meaning they still have demand but are actively losing visibility.
> - **Medium Priority**: Look at pages where `days_since_last_update` is over 180 days and `avg_position` is between 4 and 10 (high potential to regain page 1 traffic).
> - **Low Priority**: Pages with high `avg_position` (e.g., >50) or very low `impressions_90d`, since refreshing them yields lower immediate returns.

### Analysis Notes
1. **What changed in the prompt**: Added the exact schema and column definitions from our dataset.
2. **What actually improved in the output**: The output became highly specific to our database, referencing actual columns like `trend_direction`, `impressions_90d`, and `days_since_last_update`.
3. **What still failed**: The output is a rambling narrative. It's difficult for a content reviewer to scan or read quickly to make a weekly decision.
4. **What to try next**: Specify a structured output format (like a Markdown table).

---

## Version 3: Specified Output Format
*Targeting the weakness: The output is too verbose and hard to read at a glance.*

### The Prompt
> Analyze this content performance data. The objective is to prioritize a list of specific pages that have declined in search visibility so we can refresh them first. 
> 
> We are working with a dataset (`content_refresh_anonymized.csv`) containing the following columns:
> - `content_id`, `impressions_90d`, `clicks_90d`, `ctr`, `avg_position`, `days_since_last_update`, `scroll_rate`, `trend_direction`
> 
> **[Output Format]** Return the prioritized recommendations in a Markdown table with the following columns:
> 1. Rank
> 2. Content ID
> 3. Priority Score (0-100)
> 4. Primary Reason (referencing specific features like impressions, avg_position, scroll_rate)

### Representative Output
> Here is a sample prioritized queue based on your criteria:
> 
> | Rank | Content ID | Priority Score | Primary Reason |
> |---|---|---|---|
> | 1 | page_9482 | 92 | `trend_direction` is down, high `impressions_90d` (15,000), and `scroll_rate` is low (30%), indicating high demand but poor engagement. |
> | 2 | page_1029 | 85 | `avg_position` is 6.5 (page 1 edge), `days_since_last_update` is 210, and `trend_direction` is down. |
> | 3 | page_4491 | 78 | `trend_direction` is down, but `impressions_90d` is moderate (4,500). High priority but lower impact than page_9482. |

### Analysis Notes
1. **What changed in the prompt**: Added a specific Markdown table layout with predefined column headers.
2. **What actually improved in the output**: The recommendations are now in a clean, structured table that is easy to read and scan immediately.
3. **What still failed**: The prompt has no constraints on length, and the reasons can still get very long and verbose, which clutters the table cells.
4. **What to try next**: Add a constraint to restrict output length.

---

## Version 4: Constraints (The "Made It Worse" Moment)
*Targeting the weakness: The reason cell descriptions are too long and clutter the table.*

### The Prompt
> Analyze this content performance data. The objective is to prioritize a list of specific pages that have declined in search visibility so we can refresh them first. 
> 
> We are working with a dataset (`content_refresh_anonymized.csv`) containing the following columns:
> - `content_id`, `impressions_90d`, `clicks_90d`, `ctr`, `avg_position`, `days_since_last_update`, `scroll_rate`, `trend_direction`
> 
> Return the prioritized recommendations in a Markdown table with the following columns:
> 1. Rank
> 2. Content ID
> 3. Priority Score (0-100)
> 4. Primary Reason
> 
> **[Constraints]** Keep the entire response under 50 words total. Do not explain your calculations.

### Representative Output
> | Rank | Content ID | Score | Reason |
> |---|---|---|---|
> | 1 | page_9482 | 92 | Down trend, high impressions. |
> | 2 | page_1029 | 85 | Stale page, position 6. |

### Analysis Notes
1. **What changed in the prompt**: Added a strict constraint to limit the entire response to 50 words.
2. **What actually improved in the output**: The output is indeed shorter and fits on a single line.
3. **What still failed (Why it made it worse)**: The strict word limit forced the model to cut out crucial details. We no longer know the actual metrics (like CTR, scroll rate, or exact impressions) or the logic behind the scores. It is too brief to serve as actual decision support.
4. **What to try next**: Replace the raw word-count constraint with quality criteria and specific detail requirements.

---

## Version 5: Quality Criteria & Clear Constraints (Final Version)
*Targeting the weakness: The previous constraint made the output too vague. We need to restore detail and accuracy while keeping the output concise.*

### The Prompt
> Analyze this content performance data. The objective is to prioritize a list of specific pages that have declined in search visibility so we can refresh them first.
> 
> **[Context]** We are working with a dataset (`content_refresh_anonymized.csv`) containing:
> - `content_id`, `impressions_90d`, `clicks_90d`, `ctr`, `avg_position`, `days_since_last_update`, `scroll_rate`, `trend_direction`
> 
> **[Constraints]** 
> - Limit the table to exactly the top 5 highest-priority pages.
> - Do not write any conversational intro or outro text; output only the table.
> 
> **[Quality Criteria]**
> - For each page, the "Primary Reason" must contain the exact values of `impressions_90d`, `avg_position`, and `scroll_rate`.
> - Do not reference internal product flags (like `health_score`) in your reasons; prioritize using search and engagement signals only.
> 
> **[Output Format]** Return a Markdown table with these columns:
> | Rank | Content ID | Priority Score (0-100) | Primary Reason |

### Representative Output
> | Rank | Content ID | Priority Score (0-100) | Primary Reason |
> |---|---|---|---|
> | 1 | page_9482 | 95 | `trend_direction` is down. High demand (`impressions_90d`: 14,800, `avg_position`: 4.2) but low user engagement (`scroll_rate`: 31.2%). High-impact refresh candidate. |
> | 2 | page_1029 | 88 | `trend_direction` is down. Page 1 edge rank (`avg_position`: 6.5) with declining traffic (`impressions_90d`: 9,200). Stale content (`days_since_last_update`: 210). |
> | 3 | page_7731 | 82 | `trend_direction` is down. Strong search presence (`impressions_90d`: 24,100, `avg_position`: 2.1) but low click-through rate (`ctr`: 1.2%, `scroll_rate`: 48.0%). Needs metadata optimize. |
> | 4 | page_4491 | 75 | `trend_direction` is down. Moderate visibility (`impressions_90d`: 4,500, `avg_position`: 12.4) and low engagement (`scroll_rate`: 25.5%). Refresh to bump back to page 1. |
> | 5 | page_0192 | 70 | `trend_direction` is down. Page is declining despite good engagement (`scroll_rate`: 65.0%) due to slipping rank (`avg_position` fell to 8.9, `impressions_90d`: 3,100). |

### Analysis Notes
1. **What changed in the prompt**: Replaced the 50-word constraint with a top-5 limit and specific quality criteria (e.g., listing exact metrics, avoiding product flags).
2. **What actually improved in the output**: The output is clean, concise, and structured. It contains the exact values needed for a human reviewer to verify the recommendation without reading long paragraphs.
3. **What still failed**: The priority score calculation is still a heuristic (mental math by the model) rather than a trained mathematical model output.
4. **What to try next**: In production, feed the output probabilities of a trained machine learning model (like our Random Forest) directly into the Priority Score column.

---

## Final Reusable Prompt

Here is the final, engineered prompt that a colleague can copy and paste into their AI workflow:

```markdown
Analyze this content performance data to prioritize a list of specific pages that have declined in search visibility for a content refresh.

[Context]
We are working with a dataset (`content_refresh_anonymized.csv`) containing the following performance metrics:
- `content_id` (unique page ID)
- `impressions_90d` (organic search impressions)
- `clicks_90d` (clicks)
- `ctr` (click-through rate)
- `avg_position` (average search ranking position)
- `days_since_last_update` (days since content was last edited)
- `scroll_rate` (GA4 engagement rate)
- `trend_direction` (overall trend: up, stable, or down)

[Constraints]
- Limit the table to exactly the top 5 highest-priority pages.
- Do not write any conversational intro or outro text; output only the table.

[Quality Criteria]
- For each page, the "Primary Reason" must contain the exact values of `impressions_90d`, `avg_position`, and `scroll_rate`.
- Do not reference internal product flags (like `health_score` or other rules) in your reasons; prioritize using search and engagement signals only to prevent circular reasoning.

[Output Format]
Return a Markdown table with these columns:
| Rank | Content ID | Priority Score (0-100) | Primary Reason |
```
