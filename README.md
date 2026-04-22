# Audit RAG Assistant  Business Overview & Architecture
##  Business Overview

###  What this tool does

The **Audit RAG Assistant** is an AI-powered decision support tool designed to help organizations evaluate business processes against internal controls and compliance standards.

It analyzes process descriptions, retrieves relevant policy and audit evidence, and identifies **control gaps, risks, and compliance weaknesses** — all presented in a structured, visual dashboard.

Instead of manually reviewing lengthy documents, auditors and risk teams can quickly understand:

— What controls are missing  
— What risks exist  
— What actions are required  

---

###  Target Users

This tool is designed for:

— Internal Audit Teams  
— Risk & Compliance Analysts  
— Finance and Operations Managers  
— IT Governance (ITGC) Teams  
— Audit / Advisory Consultants  

---

### Business Problem Solved

Organizations face several challenges in audit and compliance:

— Manual review of policies and audit reports is time-consuming and error-prone  
— Control validation is inconsistent across teams  
— Identifying risks requires deep domain expertise  
— Audit evidence is fragmented across multiple documents  
— Limited visibility into overall control health and risk exposure  

####  Solution

The Audit RAG Assistant addresses these challenges by:

— Automating control validation using AI  
— Retrieving relevant policy and audit evidence instantly  
— Standardizing control gap identification  
— Providing visual, data-driven insights into risk and compliance  
— Reducing audit effort while improving consistency and coverage  

---

##  Key Features

###  Hybrid Retrieval (RAG)

— Combines semantic search (embeddings) and keyword search (BM25)  
— Retrieves relevant policy statements and audit findings  
— Provides evidence-backed insights with relevance scores  

---

###  Control Gap Detection

— Identifies missing controls such as:
  - Dual Approval (Maker-Checker)  
  - Access Review  
  - Audit Evidence Retention  
  - Segregation of Duties  

— Maps process descriptions to expected control frameworks  

---

###  Interactive Dashboard

— Control coverage visualization (bar chart)  
— Present vs Missing distribution (pie chart)  
— Risk score gauge  
— KPI metrics (controls present, missing, risk level, coverage)  

---

###  Audit Intelligence Layer

— Provides structured insights aligned with audit workflows  
— Highlights key risks and compliance gaps  
— Suggests auditor focus areas and remediation steps  

---

##  Tech Details

— **Frontend:** Streamlit  
— **Retrieval Engine:** Hybrid RAG (Sentence Transformers + BM25)  
— **Embeddings Model:** all-MiniLM-L6-v2  
— **Vector Similarity:** cosine similarity (scikit-learn)  
— **Visualization:** Plotly (interactive charts)  
— **Data Layer:** Text-based policy and audit datasets  

---
## 🏗️ Architecture Diagram

![Architecture](images/architecture.png)

---
##  Business Value

— Reduces manual audit effort  
— Improves consistency in control evaluation  
— Enables faster risk identification  
— Enhances audit coverage and efficiency  
— Provides explainable, evidence-backed insights  

---