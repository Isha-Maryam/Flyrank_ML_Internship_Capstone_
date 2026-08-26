# Capstone Report — Predictive SEO Content Decay

- **Author:** Isha Maryam
- **Lane:** Predictive Modeling / SEO Content Decay (Applied AI Track)
- **Repo:** https://github.com/Isha-Maryam/Flyrank_ML_Internship_Capstone_
- **Date:** August 26, 2026

## 1. Problem framing

* **Decision Supported:** The model supports editorial refresh allocation decisions. Instead of manually reviewing thousands of URLs or using arbitrary calendar timelines, SEO teams use this prioritization queue to determine which pages should be refreshed to arrest decay.
* **Unit of Analysis:** A single active content record (URL level) over a rolling 90-day window.
* **Output:** A predicted probability of decline (0.0 to 1.0) mapped into actionable, prioritized task tiers.
* **Human Action:** An editor reviews the high-risk priority queue, updates outdated statistics or examples, adds relevant subtopics, and submits the URL for Google recrawling.
* **Cost of a Wrong Call:** 
  - *False Positive (type I error):* Flagging a stable evergreen page as decaying leads to wasted editorial time and money (unnecessary edits).
  - *False Negative (type II error):* Failing to flag a decaying page leads to continued traffic loss, compounding search position decay and lost revenue.
* **Why Data/ML helps:** Content decay is a non-linear combination of age, traffic volume, positioning, and user engagement. Simple heuristics (like "update pages every 6 months") waste resources on stable pages while missing rapidly declining search assets. A machine learning model learns non-linear combinations of signals to accurately isolate true decay.

## 2. Data safety

* **Data Scope:** FlyRank Starter Dataset (`data/raw/content_refresh_anonymized.csv`) containing 30,000 active content records across 32 clients.
* **Excluded Columns & Rationale:**
  - `trend_direction` and `trend_pct` were strictly excluded. Since the target label (`is_declining_label`) is derived from `trend_direction`, including them would cause instant target leakage.
  - Client identifiers (`client_id`) and content identifiers (`content_id`) were excluded from the feature set to prevent the model from memorizing site-specific domain layouts rather than generalizable SEO features.
* **Leakage Safeguards:** Feature values are computed strictly from historical, trailing 90-day metrics, ensuring no future overlap with the 30-day target observation window. We confirmed the leakage checker sensitivity by injecting a target-derived variable, which resulted in a 1.0000 ROC-AUC, validating our audit harness.

## 3. Baseline

* **Baseline Rule:** The transparent baseline is a decay score heuristic defined as: `baseline_score = content_age_days * avg_position`. The assumption is that older content positioned further down in search is most vulnerable to decay.
* **Rationale:** This represents a standard industry SEO practice—refreshing content based on age and basic ranking position.
* **Baseline Metrics (on validation set):**
  - **Precision@50:** `0.3200`
  - **ROC-AUC:** `0.5298` (little better than a random guess)

## 4. Model / analysis

* **Model Choice:** Random Forest Classifier (n_estimators=100, max_depth=10). A tree ensemble handles missing feature structures, scales well, and models non-linear interactions without requiring normalization.
* **Features Used:**
  - `impressions_90d`, `clicks_90d`, `sessions_90d`
  - `avg_position`, `ctr`
  - `engagement_rate`, `scroll_rate`
  - `content_age_days`, `days_since_last_update`, `word_count`
  - `word_count_missing` (imputing missing word counts with the median)
* **Target Definition:** `is_declining_label = 1` if `trend_direction` is 'down' (representing a >10% organic search impression decline in the last 30 days vs the preceding 30 days), and `0` otherwise.

## 5. Evaluation

* **Split Design:** An honest **Grouped Client Split** (75% train / 25% test, grouped by `client_id` using `GroupShuffleSplit`). Grouping by client prevents the model from memorizing client characteristics (like a site's baseline traffic sizes) that leak during random splits.
* **Split Verification Metrics (Model vs. Baseline):**
  - **Test Base Rate (Majority Class):** `0.5165` (representing the background decay rate of the test set).
  - **Heuristic Baseline Precision@50:** `0.3200` (falls below the base rate, as oldest pages on new clients are often stable evergreen assets).
  - **Random Forest Precision@50:** **`0.5600`** (achieving a **+24% lift** over the baseline).
  - **Heuristic Baseline ROC-AUC:** `0.5298`
  - **Random Forest ROC-AUC:** **`0.6083`**
* **Error Analysis:**
  - *False Positives:* Occur on old, high-impression evergreen pages that the model flags as stale but which have highly stable rankings. We corrected this by ensuring engagement metrics (`scroll_rate`, `engagement_rate`) are factored in to help the model identify that these pages are still highly active.

## 6. Interpretation

* **Feature Importances:**
  1. `impressions_90d`: 23.7% (High-traffic pages have higher absolute momentum decay risk).
  2. `avg_position`: 21.0% (Positions further down have higher volatility).
  3. `content_age_days`: 16.5% (Age is a steady multiplier of decay).
* **Negative/Surprising Results:** We expected word count to have a positive correlation with stability. However, the data audits showed that longer content decays slightly faster in this portfolio if left unrefreshed, likely because comprehensive articles contain more time-sensitive facts that go stale.

## 7. Recommendation

* **Ranked Actions (Action Playbook):**
  1. **`Refresh Content` (`RC_HIGH_RISK_STALE`):** High decay probability (>60%) and untouched for >90 days. Priorities: Update facts and statistics. (5,498 pages).
  2. **`Optimize CTR` (`RC_PAGE1_WEAK_CTR`):** Positions 1-10 on page 1 but CTR < 0.5%. Priorities: Rewrite titles and descriptions. (8,343 pages).
  3. **`Audit Content Value` (`RC_ZOMBIE_CANDIDATE`):** High decay risk on low-visibility pages (<500 impressions). Priorities: Prune or consolidate. (3,594 pages).
* **Limits:** The recommendations are invalid for new pages (<30 days old) that have not been indexed by search engines. The playbook should serve as decision-support for human editors rather than automated publishing.

## 8. Reproducibility

* **Fresh Clone Command:**
  ```bash
  git clone https://github.com/Isha-Maryam/Flyrank_ML_Internship_Capstone_.git
  cd Flyrank_ML_Internship_Capstone_
  pip install -r requirements.txt
  python scripts/run_pipeline.py
  ```
* **Seeds & Parameters:** All train-test splits and classifiers are locked using `random_state=42`.
* **Environment Deltas:** Added `scikit-learn==1.9.0`, `pandas==2.3.3`, `numpy==2.3.5`, `matplotlib`, and `seaborn` to python environment.
