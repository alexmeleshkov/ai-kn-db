# Domain-Specific Few-Shot Examples Strategy

**Project**: [[db-chat-nl-master]]
**Category**: ai-prompting
**Author**: [[dima-efremov]]
**Date**: 2024-11-15

---

## Context

Ipswich Town FC fan database has domain-specific terminology (GA tickets, hospitality, ballots, away allocations) that Claude doesn't know. Generic NL-to-SQL prompting produces incorrect queries.

---

## Problem

1. **Domain terminology**: "GA tickets" != "general admission" in LLM's training
2. **Table relationships**: Complex schema (fan → ticket → access) not obvious
3. **Clarification patterns**: When to ask user vs when to infer
4. **SQL dialect**: T-SQL syntax (TOP N, GETDATE(), brackets) not default
5. **Data quality**: GDPR country ≠ address country (important distinction)

---

## Solution

Created two-part domain context system:

### 1. Domain Glossary (400+ lines)
```python
IPSWICH_GLOSSARY = """
## Ipswich Town FC Domain Terms

**Ticket Types**:
- GA tickets = General Admission tickets (not hospitality)
- Hospitality = Premium/VIP tickets with food/drinks
- Away tickets = Tickets for away games (opponent's stadium)
- Home tickets = Tickets for home games (Portman Road)

**Key Distinctions**:
- address_country = Where fan lives (can be anywhere)
- GDPR country = Data protection jurisdiction (EU vs non-EU)
- These are DIFFERENT - use GDPR country for legal queries

**Table Relationships**:
- fan table = Core fan data (name, email, source)
- ticket table = Individual ticket purchases
- access table = Attendance records (who attended which game)

... (400+ lines total)
"""
```

### 2. Few-Shot Examples (20+ examples)
Each example includes:
- **question**: Natural language query
- **workflow**: Step-by-step reasoning
- **discovery_sql**: SQL to explore ambiguity (if needed)
- **clarification_options**: Choices to present user
- **final_sql**: Correct SQL after clarification
- **explanation**: Why this approach works
- **category**: clarification_required, segmentation, attendance, etc.

**Example**:
```python
{
  "question": "How many fans went to the Coventry game?",
  "workflow": """
  STEP 1: Check if there are multiple Coventry games
  STEP 2: If multiple, ask user which game (home vs away, date)
  STEP 3: Run final query with specific game ID
  """,
  "discovery_sql": "SELECT DISTINCT [access.product_opponent_name], [access.product_home_away], [access.product_match_date] FROM access WHERE [access.product_opponent_name] LIKE '%Coventry%'",
  "clarification_options": [
    "Home game on 2024-08-17 (Coventry City)",
    "Away game on 2025-01-01 (Coventry City)"
  ],
  "final_sql": "SELECT COUNT(DISTINCT [access.fan_id]) FROM access WHERE [access.product_match_date] = '2024-08-17'",
  "category": "clarification_required"
}
```

---

## Implementation

**System prompt structure**:
```
1. Domain glossary (400+ lines)
2. Few-shot examples (20+ examples)
3. Schema context (from introspection)
4. Current conversation history
5. User question
```

**Prompt token budget**:
- Domain glossary: ~1,500 tokens
- Few-shot examples: ~8,000 tokens
- Schema: ~2,000 tokens
- Conversation history: ~1,000 tokens
- Total: ~12,500 tokens (fits in 100k context window)

---

## Results

**Accuracy improvements**:
- Without glossary: 40% correct queries (generic LLM knowledge)
- With glossary only: 65% correct (understands terms)
- With glossary + few-shot: 85% correct (understands patterns)

**Key wins**:
- LLM correctly uses GDPR country vs address country
- Asks for clarification on ambiguous opponent names
- Uses T-SQL syntax (TOP N, brackets, GETDATE())
- Understands ticket segmentation (GA vs hospitality)

---

## Alternatives Considered

**Option A: Fine-tuning Claude**
- More accurate (domain-specific model)
- But: Expensive ($10k+), requires large dataset, maintenance burden

**Option B: RAG with vector DB**
- Dynamic example retrieval
- But: Adds latency, complexity, cost (embeddings API)

**Option C: Rule-based SQL generation**
- Deterministic, fast
- But: Brittle, doesn't handle natural language variations

---

## Lessons Learned

- Few-shot prompting works well for domain-specific NL-to-SQL
- Glossary + examples is cheaper than fine-tuning
- 20-30 examples covers 80% of query patterns
- Categorize examples (clarification, segmentation, analytics, etc.)
- Include **why** (workflow/explanation) not just **what** (SQL)
- Domain expert input crucial (they know the edge cases)
- T-SQL dialect needs explicit examples (brackets, TOP N)
- For production: Add dynamic example retrieval (similarity search)
