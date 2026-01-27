# Business Context: ITFC Analysis

## Problem Statement

Sports organizations and fan database administrators need to query large fan databases containing millions of records across multiple tables (fan profiles, ticket purchases, communications, memberships, etc.). Traditional SQL querying requires technical expertise and is time-consuming for exploratory data analysis.

## Solution

ITFC Analysis provides a natural language interface powered by Claude AI that translates English questions into SQL queries, executes them against live Ipswich Town fan databases, and returns results with visualizations. The system maintains chat history and learns from successful queries to improve accuracy over time.

## Value Proposition

- **Accessibility**: Non-technical users can query complex databases without SQL knowledge
- **Speed**: Get answers in seconds instead of writing and debugging SQL manually
- **Learning**: System improves over time by learning from successful query patterns
- **Visualization**: Automatic chart generation for numeric query results
- **History**: Persistent conversation history for tracking analysis over time

## Target Users

- Sports club administrators
- Fan database analysts
- Marketing teams needing fan segmentation data
- Operations staff analyzing attendance and ticket sales

## Key Metrics

- Query success rate (first attempt)
- Average response time (currently 5-10s)
- User adoption rate
- Query complexity handled
- Learning system effectiveness (improved accuracy over time)

## Business Model

- Hosted SaaS solution
- Monthly hosting cost: $65-70 (Heroku + RDS)
- Client provides Azure SQL Server access
- Production deployment: https://www.itfcanalysis.com

**Sources**: README.md:L334-L360 (Live URL, Tech Stack), ARCHITECTURE.md:L300-L326 (Environment Variables)
