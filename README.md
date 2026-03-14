# Translational Genomics Clinical Variant Dashboard

Interactive dashboard demonstrating integration of NGS variant data with clinical phenotype information using HPO, SNOMED CT, and ICD-10 ontologies for personalised diagnostics.

## Overview

This proof-of-concept showcases a translational genomics workflow that:
- Processes high-throughput sequencing variant data (simulated VCF-like structure)
- Integrates genomic data with electronic health record (EHR) clinical data
- Maps clinical terms using standardised ontologies (HPO, SNOMED CT, ICD-10)
- Performs phenotype-genotype correlation analysis
- Provides quality control metrics for genomic pipelines

## Features

### 1. Variant Overview
- Clinical significance distribution (pathogenic, likely pathogenic, uncertain, benign)
- Variant type analysis (SNV, INDEL, CNV)
- Gene-level variant frequency
- Quality score distribution

### 2. Clinical Integration (EHR + Ontologies)
- HPO (Human Phenotype Ontology) phenotype distribution
- ICD-10 diagnosis coding
- SNOMED CT clinical findings
- Demographic analysis (age, sex, family history, consanguinity)

### 3. Phenotype-Genotype Correlation
- Links between pathogenic variants and clinical phenotypes
- Gene-phenotype associations
- Consequence type analysis for pathogenic variants

### 4. Pipeline QC
- Read depth metrics
- Allele frequency distribution
- Quality vs depth scatter plots

## Technology Stack

- **Python** (Pandas, NumPy) — Data processing
- **Streamlit** — Interactive dashboard
- **Plotly** — Data visualisation
- **pytest** — Unit testing
- **Clinical Ontologies:** HPO, SNOMED CT, ICD-10

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Testing

```bash
pytest tests/
```

## Data Structure

### Variant Data (NGS)
- Variant ID, chromosome, position, ref/alt alleles
- Gene annotation, consequence prediction
- Quality metrics (QC score, read depth, allele frequency)
- Clinical significance classification

### Clinical Data (EHR)
- Patient demographics (age, sex)
- HPO codes and phenotype terms
- ICD-10 diagnosis codes
- SNOMED CT clinical findings
- Family history and consanguinity status

## Translational Genomics Workflow

1. **Variant Calling:** Simulated NGS data processing (FASTQ → VCF)
2. **Clinical Annotation:** Map variants to HPO/SNOMED/ICD-10 ontologies
3. **Phenotype Integration:** Link genomic variants with EHR-derived phenotypes
4. **Correlation Analysis:** Identify phenotype-genotype associations
5. **Reproducible Reporting:** Dashboard for clinical stakeholders

## Use Case

This POC demonstrates the workflow required for the **University of Southampton Research Fellow in Translational Genomic Informatics** role, specifically:
- Integrating high-throughput sequencing data with structured clinical data from EHRs
- Using clinical ontologies (HPO, SNOMED CT, ICD-10) for data governance and interoperability
- Developing reproducible bioinformatics pipelines for personalised diagnostics
- Supporting clinical stakeholder collaboration with interactive analytics

## Author

Pallavi Dasaraju
MSc Biotechnology with Project Management
[LinkedIn](https://www.linkedin.com/in/pallavi-dasaraju-4442a73b6/) | [GitHub](https://github.com/pallavidasaraju)
