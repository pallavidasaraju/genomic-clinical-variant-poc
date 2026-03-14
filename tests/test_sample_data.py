"""
Unit tests for sample_data.py data generators
"""
import pytest
import pandas as pd
from sample_data import generate_variant_data, generate_clinical_data, generate_phenotype_genotype_links

def test_variant_data_structure():
    """Test variant data has correct structure."""
    df = generate_variant_data(50)
    assert len(df) == 50
    assert 'variant_id' in df.columns
    assert 'chromosome' in df.columns
    assert 'gene' in df.columns
    assert 'clinical_significance' in df.columns

def test_variant_quality_range():
    """Test variant quality scores are in valid range."""
    df = generate_variant_data(100)
    assert df['quality_score'].min() >= 20
    assert df['quality_score'].max() <= 99

def test_clinical_data_structure():
    """Test clinical data has correct structure."""
    df = generate_clinical_data(30)
    assert len(df) == 30
    assert 'patient_id' in df.columns
    assert 'hpo_code' in df.columns
    assert 'icd10_code' in df.columns
    assert 'snomed_code' in df.columns

def test_clinical_ontology_codes():
    """Test clinical ontology codes are non-empty."""
    df = generate_clinical_data(20)
    assert df['hpo_code'].notna().all()
    assert df['icd10_code'].notna().all()
    assert df['snomed_code'].notna().all()

def test_phenotype_genotype_links():
    """Test phenotype-genotype correlation generation."""
    variants = generate_variant_data(100)
    clinical = generate_clinical_data(50)
    links = generate_phenotype_genotype_links(variants, clinical)
    assert isinstance(links, pd.DataFrame)
    if len(links) > 0:
        assert 'patient_id' in links.columns
        assert 'variant_id' in links.columns
        assert 'hpo_code' in links.columns

def test_patient_id_format():
    """Test patient IDs follow correct format."""
    df = generate_clinical_data(100)
    assert all(df['patient_id'].str.match(r'^P\d{3}$'))

def test_age_range():
    """Test patient ages are in valid range."""
    df = generate_clinical_data(50)
    assert df['age'].min() >= 1
    assert df['age'].max() <= 80
