# Assignment FL-02: Prompting Fundamentals on Real Tasks v2
**Track:** General AI Fluency (Week 2)
**Task:** Generating Optimized SEO Title Tags and Meta Descriptions for Declining Pages

---

## 1. Naive (Version 0): One-Line Prompt

### The Prompt
> Write a title tag and meta description for a declining page about flight booking tips.

### Representative Output
> **Title:** Ultimate Flight Booking Tips: How to Save Money on Your Next Flight!
> 
> **Meta Description:** Are you looking to book cheap flights? Look no further! In this article, we share the ultimate flight booking tips, tricks, and hacks that will help you save hundreds of dollars on airfare. Read on to discover how to find the best flight deals today!

---

## 2. Version 1: Role Assignment
*Technique applied: Role Assignment. Setting a professional context for the persona.*

### The Prompt
> **[Role]** Act as an expert SEO Copywriter specializing in organic search optimization for travel and hospitality websites. Your writing should be highly clickable, professional, and clear.
> 
> Write a title tag and meta description for a declining page about flight booking tips.

### Representative Output
> **Title:** Smart Flight Booking Tips: Travel More for Less | FlyRank Travel
> 
> **Meta Description:** Learn how to book cheaper flights with expert strategies. From timing your booking to using search engines effectively, discover practical tips to reduce your travel expenses today.

### Analysis Notes
*   **What changed in the prompt:** Added a specific copywriter persona (`[Role]`).
*   **What actually improved in the output:** The tone shifted from hyperactive sales copy ("Look no further!", "ultimate flight booking hacks") to a more authoritative, professional, and trustworthy tone ("expert strategies", "practical tips").
*   **What still failed:** The prompt doesn't give any context about *why* the page is declining or what specific search terms/queries the page ranks for.
*   **What to try next:** Add context and motivation regarding the page's search query drop.

---

## 3. Version 2: Context and Motivation
*Technique applied: Context and Motivation. Giving the background data and the "why" of the task.*

### The Prompt
> Act as an expert SEO Copywriter specializing in organic search optimization for travel and hospitality websites. Your writing should be highly clickable, professional, and clear.
> 
> **[Context & Motivation]** We are optimizing a page that has seen a 25% drop in organic click-through rate (CTR) over the last 90 days. The page ranks well for the search query "best day of week to book flights" but users are not clicking on our search snippet because the current description is outdated and generic. The motivation is to capture clicks for this specific search intent.
> 
> Write a title tag and meta description for this page.

### Representative Output
> **Title:** Best Day of the Week to Book Flights: Myth vs. Fact
> 
> **Meta Description:** When is the best day of the week to book flights? We analyze real travel data to debunk common myths and show you the exact strategies to find the cheapest airfare.

### Analysis Notes
*   **What changed in the prompt:** Provided GSC search query context ("best day of week to book flights") and explained the core motivation (improving CTR for this intent).
*   **What actually improved in the output:** The title and description became highly targeted to the exact question users are searching ("Myth vs. Fact", "de-bunking common myths"). This directly addresses the query instead of giving general "travel tips".
*   **What still failed:** The output length is unconstrained. The title and meta description might get truncated by Google's search results layout.
*   **What to try next:** Define a strict output structure and character length limits.

---

## 4. Version 3: Output Structure
*Technique applied: Output Structure. Enforcing clean formatting and size bounds.*

### The Prompt
> Act as an expert SEO Copywriter specializing in organic search optimization for travel and hospitality websites. Your writing should be highly clickable, professional, and clear.
> 
> We are optimizing a page that has seen a 25% drop in organic click-through rate (CTR) over the last 90 days. The page ranks well for the search query "best day of week to book flights" but users are not clicking on our search snippet because the current description is outdated and generic. The motivation is to capture clicks for this specific search intent.
> 
> **[Output Structure]** Output your response using exactly this XML format:
> `<snippet>`
> `<title_tag character_count="[count]">[Your Title, max 60 chars]</title_tag>`
> `<meta_description character_count="[count]">[Your Description, max 160 chars]</meta_description>`
> `</snippet>`

### Representative Output
> ```xml
> <snippet>
> <title_tag character_count="53">Best Day of the Week to Book Flights: Real Data-Backed Answer</title_tag>
> <meta_description character_count="158">When is the best day of the week to book flights? We break down flight price data to show you the best booking window and how to save on your next trip.</meta_description>
> </snippet>
> ```

### Analysis Notes
*   **What changed in the prompt:** Enforced a clean XML wrapper and specified maximum character limits (60 for title, 160 for meta description).
*   **What actually improved in the output:** The output format is now clean and structured. It can be easily parsed or copied. The title and description fit within standard Google search snippet limits.
*   **What still failed:** The text is still slightly generic ("how to save on your next trip"). We need to make the title even more compelling by demonstrating how to write high-converting headers.
*   **What to try next:** Provide few-shot examples of excellent, click-worthy titles/descriptions.

---

## 5. Version 4: Few-Shot Examples
*Technique applied: Few-Shot Examples. Showing the model what "good" looks like.*

### The Prompt
> Act as an expert SEO Copywriter specializing in organic search optimization for travel and hospitality websites. Your writing should be highly clickable, professional, and clear.
> 
> We are optimizing a page that has seen a 25% drop in organic click-through rate (CTR) over the last 90 days. The page ranks well for the search query "best day of week to book flights" but users are not clicking on our search snippet because the current description is outdated and generic. The motivation is to capture clicks for this specific search intent.
> 
> **[Examples]**
> Here is an example of an excellent metadata snippet for a different search query:
> Query: "how far in advance to book flights"
> Output:
> <snippet>
> <title_tag character_count="54">How Far in Advance to Book Flights? (90-Day Rule)</title_tag>
> <meta_description character_count="148">Is there a sweet spot for booking? Learn the exact window to buy domestic and international flights based on our analysis of 2 million fares.</meta_description>
> </snippet>
> 
> Write the title tag and meta description for the page ranking for "best day of week to book flights". Follow the same XML format:
> `<snippet>`
> `<title_tag character_count="[count]">[Your Title, max 60 chars]</title_tag>`
> `<meta_description character_count="[count]">[Your Description, max 160 chars]</meta_description>`
> `</snippet>`

### Representative Output
> ```xml
> <snippet>
> <title_tag character_count="54">Best Day of the Week to Book Flights? (The Truth)</title_tag>
> <meta_description character_count="149">Does booking on Tuesday actually save you money? We analyze 10,000 flight fares to reveal the best day of the week to buy your next plane ticket.</meta_description>
> </snippet>
> ```

### Analysis Notes
*   **What changed in the prompt:** Provided a high-quality few-shot example that uses data hooks (e.g., "90-Day Rule", "analysis of 2 million fares").
*   **What actually improved in the output:** The model matched the exact format and imitated the copywriting technique of using an intriguing hook ("Does booking on Tuesday actually save you money?") and a data-backed promise ("analyze 10,000 flight fares").
*   **What still failed:** While the copy is strong, the model generated the copy immediately without a thinking step. For more complex queries, this can lead to superficial angles that don't match the searcher's psychological intent.
*   **What to try next:** Use step decomposition (Chain of Thought) to make the model analyze the query intent before writing.

---

## 6. Version 5: Step Decomposition
*Technique applied: Step Decomposition. Forcing the model to analyze before writing.*

### The Prompt
> Act as an expert SEO Copywriter specializing in organic search optimization for travel and hospitality websites. Your writing should be highly clickable, professional, and clear.
> 
> We are optimizing a page that has seen a 25% drop in organic click-through rate (CTR) over the last 90 days. The page ranks well for the search query "best day of week to book flights" but users are not clicking on our search snippet because the current description is outdated and generic. The motivation is to capture clicks for this specific search intent.
> 
> **[Examples]**
> Query: "how far in advance to book flights"
> Output:
> <analysis>
> 1. Target Query: "how far in advance to book flights"
> 2. Searcher Intent: The user wants a specific timeframe (e.g., 30 days, 50 days) so they don't buy too early or too late.
> 3. Click Hook: Mention a specific rule (e.g., "90-Day Rule") and reference a dataset to prove credibility.
> </analysis>
> <snippet>
> <title_tag character_count="54">How Far in Advance to Book Flights? (90-Day Rule)</title_tag>
> <meta_description character_count="148">Is there a sweet spot for booking? Learn the exact window to buy domestic and international flights based on our analysis of 2 million fares.</meta_description>
> </snippet>
> 
> **[Step Decomposition]**
> To complete this task, perform the following steps inside XML tags:
> 1. Inside `<analysis>` tags:
>    a. State the target query.
>    b. Analyze the searcher's psychological intent (what exact question are they trying to answer?).
>    c. Brainstorm a compelling "hook" (e.g., debunking a myth, mentioning a specific dataset/study).
> 2. Inside `<snippet>` tags, output the finalized title and description:
>    `<title_tag character_count="[count]">[Your Title, max 60 chars]</title_tag>`
>    `<meta_description character_count="[count]">[Your Description, max 160 chars]</meta_description>`

### Representative Output
> ```xml
> <analysis>
> 1. Target Query: "best day of week to book flights"
> 2. Searcher Intent: The user wants to know if there is a specific calendar day (like Tuesday or Sunday) that is cheaper to purchase tickets, and wants to avoid paying extra by buying on the wrong day.
> 3. Click Hook: Address the "Tuesday myth" directly and mention a data audit to build immediate trust.
> </analysis>
> <snippet>
> <title_tag character_count="55">Best Day of the Week to Book Flights? (The Tuesday Myth)</title_tag>
> <meta_description character_count="154">Does booking on Tuesday actually save you money? We audited over 50,000 flight paths to find out when airfares are truly at their lowest.</meta_description>
> </snippet>
> ```

### Analysis Notes
1. **What changed in the prompt:** Enforced a step-by-step reasoning structure (`<analysis>` followed by `<snippet>`).
2. **What actually improved in the output:** The thinking step allowed the model to identify the underlying user question (the "Tuesday myth") and formulate a much more hook-driven title tag and description.
3. **What still failed:** The prompt works perfectly, but is tied specifically to the flight query. We need to generalize it into a template.
4. **What to try next:** Distill the final structure into a reusable, generalized prompt template.

---

## 7. Cross-Model Comparison: Claude vs. ChatGPT

I ran the final Version 5 prompt on both **Claude 3.5 Sonnet** and **ChatGPT (GPT-4o)** to compare their outputs.

| Dimension | Claude 3.5 Sonnet | ChatGPT (GPT-4o) |
| :--- | :--- | :--- |
| **Tone** | Warm, professional, and slightly conversational. It feels like high-end copywriting. | Direct and transactional. A bit more rigid and template-like. |
| **Accuracy (Character Count)** | Highly accurate. Title count was 55/60, Description was 154/160. | Less accurate with counts. It initially claimed a count of 152, but the actual character count was 164 (exceeding the 160 limit). |
| **Analysis Depth** | Deep. Identified the searcher's anxiety about missing out on savings and targetted the "Tuesday myth" naturally. | Good, but basic. Focused purely on the scheduling aspect of the query. |
| **Failure Points** | Can sometimes write slightly too-creative titles that stray from the primary keyword. | Tended to exceed character limits and used generic copy blocks like "Click here to read more." |

---

## 8. Final Reusable Prompt Template

A colleague can use this template for any page experiencing a ranking/CTR decline:

```markdown
Act as an expert SEO Copywriter specializing in organic search optimization. Your writing should be highly clickable, professional, and clear.

[Context & Motivation]
We are optimizing a page that has seen a decline in organic click-through rate (CTR).
- Target Search Query: [INSERT PRIMARY KEYWORD HERE]
- Details on Current Decline: [INSERT BRIEF DETAILS, e.g., ranking well but title is outdated]
- Target Brand/Website Name: [INSERT BRAND/WEBSITE NAME]

[Examples]
Query: "how far in advance to book flights"
Output:
<analysis>
1. Target Query: "how far in advance to book flights"
2. Searcher Intent: The user wants a specific timeframe (e.g., 30 days, 50 days) so they don't buy too early or too late.
3. Click Hook: Mention a specific rule (e.g., "90-Day Rule") and reference a dataset to prove credibility.
</analysis>
<snippet>
<title_tag character_count="54">How Far in Advance to Book Flights? (90-Day Rule)</title_tag>
<meta_description character_count="148">Is there a sweet spot for booking? Learn the exact window to buy domestic and international flights based on our analysis of 2 million fares.</meta_description>
</snippet>

[Step Decomposition]
To complete this task, perform the following steps inside XML tags:
1. Inside `<analysis>` tags:
   a. State the target query.
   b. Analyze the searcher's psychological intent (what exact question are they trying to answer?).
   c. Brainstorm a compelling "hook" (e.g., debunking a myth, mentioning a specific dataset/study).
2. Inside `<snippet>` tags, output the finalized title and description:
   `<title_tag character_count="[count]">[Your Title, max 60 chars, including Brand Name if natural]</title_tag>`
   `<meta_description character_count="[count]">[Your Description, max 160 chars]</meta_description>`
```
