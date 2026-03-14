"""
Translational Genomics Clinical Variant Dashboard
Interactive Streamlit app demonstrating genomic-clinical data integration
using HPO, SNOMED CT, and ICD-10 ontologies for personalised diagnostics.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sample_data import generate_variant_data, generate_clinical_data, generate_phenotype_genotype_links

st.set_page_config(page_title="Genomic Clinical Variant Dashboard", layout="wide")

# Generate data
@st.cache_data
def load_data():
    variants = generate_variant_data(100)
    clinical = generate_clinical_data(50)
    correlations = generate_phenotype_genotype_links(variants, clinical)
    return variants, clinical, correlations

variants_df, clinical_df, correlation_df = load_data()

# Header
st.title("🧬 Translational Genomics Clinical Variant Dashboard")
st.markdown("**Demonstrating NGS Variant Integration with Clinical Phenotype Data (HPO, SNOMED CT, ICD-10)**")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Variants", len(variants_df))
with col2:
    pathogenic_count = len(variants_df[variants_df['clinical_significance'].isin(['pathogenic', 'likely_pathogenic'])])
    st.metric("Pathogenic Variants", pathogenic_count)
with col3:
    st.metric("Patients with EHR Data", len(clinical_df))
with col4:
    st.metric("Phenotype-Genotype Links", len(correlation_df))

st.divider()

# Tab structure
tab1, tab2, tab3, tab4 = st.tabs(["📊 Variant Overview", "🏥 Clinical Integration", "🔗 Phenotype-Genotype", "📈 Pipeline QC"])

with tab1:
    st.header("Variant Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Variants by Clinical Significance")
        sig_counts = variants_df['clinical_significance'].value_counts().reset_index()
        sig_counts.columns = ['Significance', 'Count']
        fig_sig = px.bar(sig_counts, x='Significance', y='Count', color='Significance',
                         color_discrete_map={
                             'pathogenic': '#d62728',
                             'likely_pathogenic': '#ff7f0e',
                             'uncertain': '#bcbd22',
                             'likely_benign': '#17becf',
                             'benign': '#2ca02c'
                         })
        st.plotly_chart(fig_sig, use_container_width=True)

    with col2:
        st.subheader("Variant Types Distribution")
        type_counts = variants_df['variant_type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        fig_type = px.pie(type_counts, names='Type', values='Count', hole=0.4)
        st.plotly_chart(fig_type, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Top 10 Genes by Variant Count")
        gene_counts = variants_df['gene'].value_counts().head(10).reset_index()
        gene_counts.columns = ['Gene', 'Variant Count']
        fig_genes = px.bar(gene_counts, x='Variant Count', y='Gene', orientation='h', color='Variant Count')
        st.plotly_chart(fig_genes, use_container_width=True)

    with col4:
        st.subheader("Variant Quality Scores")
        fig_qual = px.histogram(variants_df, x='quality_score', nbins=20, marginal='box')
        fig_qual.update_layout(xaxis_title="Quality Score", yaxis_title="Count")
        st.plotly_chart(fig_qual, use_container_width=True)

with tab2:
    st.header("Clinical Data Integration (EHR + Ontologies)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("HPO Phenotype Distribution (Top 10)")
        hpo_counts = clinical_df['hpo_term'].value_counts().head(10).reset_index()
        hpo_counts.columns = ['HPO Term', 'Patient Count']
        fig_hpo = px.bar(hpo_counts, x='Patient Count', y='HPO Term', orientation='h', color='Patient Count')
        st.plotly_chart(fig_hpo, use_container_width=True)

    with col2:
        st.subheader("ICD-10 Diagnosis Distribution")
        icd10_counts = clinical_df['icd10_diagnosis'].value_counts().head(10).reset_index()
        icd10_counts.columns = ['ICD-10 Diagnosis', 'Patient Count']
        fig_icd = px.bar(icd10_counts, x='Patient Count', y='ICD-10 Diagnosis', orientation='h', color='Patient Count')
        st.plotly_chart(fig_icd, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Age Distribution by Sex")
        fig_age = px.histogram(clinical_df, x='age', color='sex', barmode='overlay', nbins=15)
        fig_age.update_layout(xaxis_title="Age (years)", yaxis_title="Count")
        st.plotly_chart(fig_age, use_container_width=True)

    with col4:
        st.subheader("Family History & Consanguinity")
        fam_hist = clinical_df['family_history'].value_counts().reset_index()
        fam_hist.columns = ['Status', 'Count']
        fig_fam = px.pie(fam_hist, names='Status', values='Count', title='Family History', hole=0.3)
        st.plotly_chart(fig_fam, use_container_width=True)

with tab3:
    st.header("Phenotype-Genotype Correlation Analysis")

    if len(correlation_df) > 0:
        st.subheader(f"Identified {len(correlation_df)} Phenotype-Genotype Links")

        # Filter for pathogenic variants only
        st.dataframe(correlation_df[['patient_id', 'gene', 'consequence', 'clinical_significance',
                                      'hpo_code', 'hpo_term', 'icd10_code', 'icd10_diagnosis']].head(20))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Genes Associated with Pathogenic Variants")
            gene_path = correlation_df['gene'].value_counts().head(10).reset_index()
            gene_path.columns = ['Gene', 'Pathogenic Variant Count']
            fig_gene_path = px.bar(gene_path, x='Pathogenic Variant Count', y='Gene', orientation='h', color='Pathogenic Variant Count')
            st.plotly_chart(fig_gene_path, use_container_width=True)

        with col2:
            st.subheader("Consequence Types in Pathogenic Variants")
            cons_counts = correlation_df['consequence'].value_counts().reset_index()
            cons_counts.columns = ['Consequence', 'Count']
            fig_cons = px.pie(cons_counts, names='Consequence', values='Count', hole=0.4)
            st.plotly_chart(fig_cons, use_container_width=True)
    else:
        st.warning("No phenotype-genotype correlations found in this dataset.")

with tab4:
    st.header("Pipeline Quality Control Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Read Depth Distribution")
        fig_depth = px.box(variants_df, y='read_depth', points='outliers')
        fig_depth.update_layout(yaxis_title="Read Depth")
        st.plotly_chart(fig_depth, use_container_width=True)

    with col2:
        st.subheader("Allele Frequency Distribution")
        fig_af = px.histogram(variants_df, x='allele_frequency', nbins=25, marginal='rug')
        fig_af.update_layout(xaxis_title="Allele Frequency", yaxis_title="Count")
        st.plotly_chart(fig_af, use_container_width=True)

    st.subheader("Variant Quality vs Read Depth")
    fig_scatter = px.scatter(variants_df, x='read_depth', y='quality_score', color='clinical_significance',
                             hover_data=['gene', 'consequence'])
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()
st.markdown("**Built with:** Python (Biopython, Pandas), Streamlit, Plotly | **Ontologies:** HPO, SNOMED CT, ICD-10 | **Pipeline:** NGS Variant Calling → Clinical Annotation → Phenotype-Genotype Correlation")
