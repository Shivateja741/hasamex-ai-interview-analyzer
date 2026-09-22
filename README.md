# Hasamex AI Engineer Case Study — Expert Interview Analyzer

An AI-powered application for analyzing expert interview transcripts across multiple European markets.

The application uses semantic retrieval and an LLM to answer interview-guide questions, surface supporting evidence, compare markets, and enable cross-transcript questions while keeping responses grounded in the original expert statements.

---

## 1. Problem Statement

Market research teams often need to analyze multiple expert interviews and identify:

- Answers to a predefined interview guide
- Exact supporting quotes
- Expert names, roles, and timestamps
- Common themes across interviews
- Differences between markets
- Insights that span multiple interviews
- Evidence that supports each generated conclusion

Manually performing this analysis across many transcripts is time-consuming and makes it difficult to consistently trace insights back to their sources.

This project demonstrates an AI-assisted workflow for making expert interview analysis faster, structured, and evidence-oriented.

---

## 2. Case Study

The application analyzes expert interviews about the:

**European Robotic Surgery Market**

Three expert transcripts are included:

| Market | Expert | Role |
|---|---|---|
| France | Dr. Jean Martin | Head of Urology |
| Germany | Anna Keller | Former Hospital Procurement Director |
| UK | Dr. Emily Carter | Consultant Urologist |

Each transcript contains responses to the same six interview-guide questions.

---

## 3. Interview Guide

The application supports the following questions:

### Q1. Market Adoption

How would you describe current adoption of robotic surgery in your market?

### Q2. Barriers

What are the main barriers to adoption?

### Q3. Hospital Budgets and ROI

How important are hospital budgets and ROI in purchasing decisions?

### Q4. Training and Clinical Outcomes

How important are surgeon training and clinical outcomes?

### Q5. Future Adoption

What adoption trend do you expect over the next 3–5 years?

### Q6. Purchasing Timeline

What is the typical hospital decision-making timeline for purchasing a new robotic system?

---

## 4. Key Features

### Interview Guide Analysis

Users can select one of the six predefined interview questions.

The system:

1. Retrieves relevant expert responses.
2. Restricts retrieval to the selected interview question.
3. Generates an AI synthesis.
4. Identifies common themes.
5. Identifies market differences.
6. Displays supporting evidence.
7. Shows the expert, role, country, and timestamp for each source.

### Cross-Call Analysis

The Cross-Call Analysis feature allows a question to be answered using evidence from all three interviews.

Evidence is intentionally balanced across:

- France
- Germany
- UK

This helps prevent the analysis from being dominated by a single market.

Example:

> How do the three countries balance economic and clinical considerations when purchasing robotic surgery systems?

The application retrieves relevant evidence from each market and generates a cross-market synthesis.

### Ask AI

The Ask AI tab allows users to enter their own question.

Example:

> What factors make a robotic surgery program economically sustainable?

The system provides:

- AI-generated answer
- Common themes
- Market differences
- Supporting evidence
- Expert information
- Timestamps

---

## 5. Evidence Grounding

A core design principle of the application is:

> AI-generated conclusions should be traceable back to the original interview evidence.

Each retrieved evidence item contains:

- Country
- Expert
- Role
- Question number
- Timestamp
- Original response text
- Retrieval score

The UI displays the supporting quote alongside the generated analysis.

This allows a reviewer to move from:

**AI insight → expert evidence → transcript timestamp**

rather than relying only on an unsupported LLM response.

---

## 6. Retrieval Strategy

The system uses a hybrid retrieval approach based on the structure of the interview data.

### Question-Specific Retrieval

For predefined interview-guide questions, retrieval is restricted to the corresponding question number.

For example:

```text
Q1 → only Q1 responses
Q2 → only Q2 responses
Q3 → only Q3 responses
Q4 → only Q4 responses
Q5 → only Q5 responses
Q6 → only Q6 responses