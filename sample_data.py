"""
Synthetic Data Generator for Translational Genomics POC
Generates:
- NGS variant data (simulated VCF-like structure)
- Clinical phenotype data from EHR (HPO, SNOMED CT, ICD-10 coded)
- Patient metadata linking genomic and clinical data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generate_variant_data(n_variants=100):
    """Generate synthetic NGS variant data (VCF-like)."""
    chromosomes = ['chr' + str(i) for i in range(1, 23)] + ['chrX', 'chrY']
    variant_types = ['SNV', 'INDEL', 'CNV']
    consequences = ['missense', 'nonsense', 'frameshift', 'splice_site', 'synonymous', 'intron', 'utr']
    genes = ['BRCA1', 'BRCA2', 'TP53', 'CFTR', 'DMD', 'HTT', 'APP', 'APOE', 'FMR1', 'HBB', 'PKU', 'GBA']

    data = {
        'variant_id': [f'var_{i:04d}' for i in range(n_variants)],
        'chromosome': np.random.choice(chromosomes, n_variants),
        'position': np.random.randint(1000, 100000000, n_variants),
        'ref_allele': np.random.choice(['A', 'T', 'C', 'G'], n_variants),
        'alt_allele': np.random.choice(['A', 'T', 'C', 'G'], n_variants),
        'variant_type': np.random.choice(variant_types, n_variants, p=[0.7, 0.2, 0.1]),
        'gene': np.random.choice(genes, n_variants),
        'consequence': np.random.choice(consequences, n_variants, p=[0.3, 0.05, 0.05, 0.05, 0.3, 0.2, 0.05]),
        'quality_score': np.random.uniform(20, 99, n_variants).round(1),
        'read_depth': np.random.randint(10, 200, n_variants),
        'allele_frequency': np.random.uniform(0.001, 0.5, n_variants).round(4),
        'clinical_significance': np.random.choice(
            ['pathogenic', 'likely_pathogenic', 'uncertain', 'likely_benign', 'benign'],
            n_variants,
            p=[0.1, 0.15, 0.3, 0.25, 0.2]
        ),
        'patient_id': [f'P{np.random.randint(1, 51):03d}' for _ in range(n_variants)]
    }

    return pd.DataFrame(data)

def generate_clinical_data(n_patients=50):
    """Generate synthetic clinical phenotype data with ontology codes."""
    phenotypes_hpo = {
        'HP:0001250': 'Seizures',
        'HP:0001263': 'Developmental delay',
        'HP:0001249': 'Intellectual disability',
        'HP:0000729': 'Autistic behavior',
        'HP:0001252': 'Muscular hypotonia',
        'HP:0001508': 'Failure to thrive',
        'HP:0000252': 'Microcephaly',
        'HP:0001629': 'Ventricular septal defect',
        'HP:0001643': 'Patent ductus arteriosus',
        'HP:0002119': 'Ventriculomegaly'
    }

    diagnoses_icd10 = {
        'E84.9': 'Cystic fibrosis, unspecified',
        'G71.0': 'Muscular dystrophy',
        'Q90.9': 'Down syndrome, unspecified',
        'E75.2': 'Gaucher disease',
        'G10': 'Huntington disease',
        'G20': 'Parkinson disease',
        'G30.9': 'Alzheimer disease, unspecified',
        'Q99.2': 'Fragile X syndrome',
        'D56.1': 'Beta thalassemia'
    }

    clinical_findings_snomed = {
        '386661006': 'Fever',
        '271807003': 'Rash',
        '62315008': 'Diarrhea',
        '422587007': 'Nausea',
        '84229001': 'Fatigue',
        '25064002': 'Headache',
        '267036007': 'Dyspnea'
    }

    data = {
        'patient_id': [f'P{i:03d}' for i in range(1, n_patients + 1)],
        'age': np.random.randint(1, 80, n_patients),
        'sex': np.random.choice(['M', 'F'], n_patients),
        'hpo_code': [np.random.choice(list(phenotypes_hpo.keys())) for _ in range(n_patients)],
        'hpo_term': [phenotypes_hpo[np.random.choice(list(phenotypes_hpo.keys()))] for _ in range(n_patients)],
        'icd10_code': [np.random.choice(list(diagnoses_icd10.keys())) for _ in range(n_patients)],
        'icd10_diagnosis': [diagnoses_icd10[np.random.choice(list(diagnoses_icd10.keys()))] for _ in range(n_patients)],
        'snomed_code': [np.random.choice(list(clinical_findings_snomed.keys())) for _ in range(n_patients)],
        'snomed_finding': [clinical_findings_snomed[np.random.choice(list(clinical_findings_snomed.keys()))] for _ in range(n_patients)],
        'consanguinity': np.random.choice(['Yes', 'No'], n_patients, p=[0.1, 0.9]),
        'family_history': np.random.choice(['Yes', 'No'], n_patients, p=[0.3, 0.7]),
        'ehr_encounter_date': [(datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime('%Y-%m-%d') for _ in range(n_patients)]
    }

    return pd.DataFrame(data)

def generate_phenotype_genotype_links(variant_df, clinical_df):
    """Create phenotype-genotype correlation table."""
    # Sample variants with pathogenic/likely_pathogenic significance
    pathogenic_vars = variant_df[variant_df['clinical_significance'].isin(['pathogenic', 'likely_pathogenic'])].copy()

    if len(pathogenic_vars) == 0:
        return pd.DataFrame()

    # Merge with clinical data on patient_id
    merged = pathogenic_vars.merge(clinical_df, on='patient_id', how='inner')

    # Select relevant columns for correlation analysis
    correlation_data = merged[[
        'patient_id', 'variant_id', 'gene', 'consequence', 'clinical_significance',
        'hpo_code', 'hpo_term', 'icd10_code', 'icd10_diagnosis', 'age', 'sex'
    ]].copy()

    return correlation_data

if __name__ == '__main__':
    # Generate datasets
    variants = generate_variant_data(100)
    clinical = generate_clinical_data(50)
    correlations = generate_phenotype_genotype_links(variants, clinical)

    print("Variant Data:", variants.shape)
    print("\nClinical Data:", clinical.shape)
    print("\nPhenotype-Genotype Correlations:", correlations.shape)
    print("\nSample Correlation:")
    print(correlations.head(3).to_string())
