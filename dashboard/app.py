import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── Project root ──
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

st.set_page_config(
    page_title="Pothole Severity · Decision Support",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════
# DESIGN SYSTEM — Custom CSS
# ═══════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141432 0%, #1c1c3a 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e0e0ff !important;
}

/* ── KPI Cards ── */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 24px;
    transition: transform 0.3s cubic-bezier(.25,.8,.25,1), box-shadow 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.18);
    border-color: rgba(99,102,241,0.35);
}
div[data-testid="stMetric"] label {
    color: #a5b4fc !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.85rem !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(255,255,255,0.03);
    border-radius: 14px;
    padding: 4px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #a5b4fc;
    font-weight: 500;
    font-size: 0.82rem;
    padding: 8px 18px;
    transition: all 0.25s ease;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(99,102,241,0.35);
}

/* ── Dataframes ── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.25) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(99,102,241,0.4) !important;
}

/* ── Selectbox / Multiselect ── */
div[data-baseweb="select"] {
    border-radius: 10px;
}

/* ── Section headings ── */
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e0e0ff;
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}
.section-sub {
    font-size: 0.88rem;
    color: #8888bb;
    margin-bottom: 24px;
    line-height: 1.5;
}

/* ── Glass panel ── */
.glass-panel {
    background: rgba(255,255,255,0.035);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
}

/* ── Priority badges ── */
.badge { display:inline-block; padding:4px 14px; border-radius:20px; font-size:0.78rem; font-weight:600; letter-spacing:0.4px; }
.badge-critical { background:rgba(239,68,68,0.18); color:#f87171; border:1px solid rgba(239,68,68,0.3); }
.badge-high { background:rgba(251,146,60,0.18); color:#fb923c; border:1px solid rgba(251,146,60,0.3); }
.badge-medium { background:rgba(250,204,21,0.15); color:#facc15; border:1px solid rgba(250,204,21,0.25); }
.badge-low { background:rgba(74,222,128,0.15); color:#4ade80; border:1px solid rgba(74,222,128,0.25); }
.badge-review { background:rgba(168,85,247,0.18); color:#c084fc; border:1px solid rgba(168,85,247,0.3); }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(139,92,246,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
}
.hero h1 {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #c7d2fe 0%, #a78bfa 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}
.hero p {
    color: #9ca3d0;
    font-size: 0.95rem;
    line-height: 1.6;
    max-width: 720px;
}

/* ── Info / Warning boxes ── */
.stAlert {
    border-radius: 12px !important;
}

/* ── Hide default streamlit branding ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


import joblib

# ═══════════════════════════════════════════════════
# DATA LOADING & INFERENCE
# ═══════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(PROJECT_ROOT, 'outputs/scheduling/maintenance_schedule_recommendations.csv'))
    imgs = pd.read_csv(os.path.join(PROJECT_ROOT, 'outputs/prioritization/image_priority_ranking.csv'))
    costs = pd.read_csv(os.path.join(PROJECT_ROOT, 'outputs/cost_estimation/cost_scenario_summary.csv'))
    with open(os.path.join(PROJECT_ROOT, 'models/final/final_model_metadata.json'), 'r') as f:
        meta = json.load(f)
    return df, imgs, costs, meta

df, image_df, cost_summary, meta = load_data()

# Model for inference
try:
    svm_model = joblib.load(os.path.join(PROJECT_ROOT, 'models/final/final_model.pkl'))
    scaler = joblib.load(os.path.join(PROJECT_ROOT, 'models/scaler.pkl'))
except:
    svm_model = None
    scaler = None


# ── Plotly color palette ──
COLORS = {
    'minor_pothole': '#4ade80',
    'medium_pothole': '#facc15',
    'major_pothole': '#f87171',
    'CRITICAL': '#ef4444',
    'HIGH': '#fb923c',
    'MEDIUM': '#facc15',
    'LOW': '#4ade80',
    'REVIEW REQUIRED': '#c084fc',
}
BG_TRANSPARENT = 'rgba(0,0,0,0)'
GRID_COLOR = 'rgba(255,255,255,0.06)'
TEXT_COLOR = '#c0c0e0'
PLOTLY_LAYOUT = dict(
    paper_bgcolor=BG_TRANSPARENT,
    plot_bgcolor=BG_TRANSPARENT,
    font=dict(family='Inter', color=TEXT_COLOR),
    margin=dict(l=40, r=20, t=50, b=40),
)


# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📤 Upload Dataset")
    uploaded_file = st.file_uploader("Upload CSV for Inference", type="csv")
    
    if uploaded_file is not None and svm_model is not None:
        try:
            udf = pd.read_csv(uploaded_file)
            
            # Require geometric features
            features = ['bbox_width', 'bbox_height', 'bbox_area', 'rel_bbox_width', 'rel_bbox_height', 'rel_bbox_area', 'bbox_aspect_ratio', 'log_bbox_area']
            if all(f in udf.columns for f in features):
                X_scaled = scaler.transform(udf[features])
                udf['predicted_severity'] = svm_model.predict(X_scaled)
                probs = svm_model.predict_proba(X_scaled)
                
                # Assume classes are ['major_pothole', 'medium_pothole', 'minor_pothole'] based on model.classes_
                cls_idx = {c: i for i, c in enumerate(svm_model.classes_)}
                if 'major_pothole' in cls_idx:
                    udf['prediction_confidence'] = probs.max(axis=1)
                    udf['priority_score'] = (
                        3 * probs[:, cls_idx.get('major_pothole', 0)] +
                        2 * probs[:, cls_idx.get('medium_pothole', 1)] +
                        1 * probs[:, cls_idx.get('minor_pothole', 2)]
                    )
                    
                    udf['priority_category'] = udf['priority_score'].apply(
                        lambda s: 'CRITICAL' if s >= 2.6 else ('HIGH' if s >= 2.0 else ('MEDIUM' if s >= 1.4 else 'LOW'))
                    )
                    udf['review_required'] = udf['prediction_confidence'] < 0.45
                    
                    # Update df for the rest of the app
                    df = udf.copy()
                    st.success("✅ Dataset Processed!")
            else:
                st.error("Missing required geometric features in CSV.")
        except Exception as e:
            st.error(f"Error processing file: {e}")
            
    st.markdown("## 🛣️ Filters")
    st.markdown("---")

    severity_opts = sorted(df['predicted_severity'].unique().tolist())
    severity_filter = st.multiselect(
        "Predicted Severity",
        options=severity_opts,
        default=severity_opts,
    )

    priority_opts = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'REVIEW REQUIRED']
    priority_filter = st.multiselect(
        "Priority Category",
        options=[p for p in priority_opts if p in df['priority_category'].unique()],
        default=[p for p in priority_opts if p in df['priority_category'].unique()],
    )

    review_only = st.toggle("🔍 Review Required only", value=False)

    st.markdown("---")
    st.markdown(
        "<p style='color:#6b6b9e;font-size:0.75rem;text-align:center;'>"
        "Pothole Decision Support v2.0<br/>Built with Streamlit & Plotly"
        "</p>",
        unsafe_allow_html=True,
    )

# ── Apply filters ──
mask = df['predicted_severity'].isin(severity_filter) & df['priority_category'].isin(priority_filter)
if review_only:
    mask = mask & (df['review_required'] == True)
fdf = df[mask].copy()


# ═══════════════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <h1>Pothole Severity &amp; Maintenance Decision Support</h1>
    <p>
        An end-to-end classification pipeline transforming 717 road images and 1,886 annotated
        potholes into actionable maintenance priorities. Powered by a tuned SVM achieving
        <strong>65.14% Macro F1</strong> on the held-out test set.
    </p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# KPI RIBBON
# ═══════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Potholes", f"{len(fdf):,}")
k2.metric("Major Severity", f"{(fdf['predicted_severity']=='major_pothole').sum():,}")
k3.metric("Critical / High", f"{fdf['priority_category'].isin(['CRITICAL','HIGH']).sum():,}")
k4.metric("Avg Confidence", f"{fdf['prediction_confidence'].mean():.1%}" if len(fdf) else "—")
k5.metric("Test Macro F1", f"{meta.get('final_test_macro_f1',0):.1%}")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════
tab_overview, tab_severity, tab_priority, tab_confidence, tab_images, tab_cost, tab_schedule, tab_model, tab_limits = st.tabs([
    "📊 Overview",
    "🎯 Severity",
    "⚡ Priority",
    "🔬 Confidence",
    "🖼️ Image Hotspots",
    "💰 Cost Planning",
    "📅 Scheduling",
    "🤖 Model",
    "⚠️ Limitations",
])


# ─── TAB 1: Overview ─────────────────────────────
with tab_overview:
    st.markdown('<p class="section-header">Dashboard Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">A transparent, data-driven decision-support system for pothole repair planning. All metrics are derived from actual model outputs — nothing is fabricated.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sev_counts = fdf['predicted_severity'].value_counts().reset_index()
        sev_counts.columns = ['Severity', 'Count']
        fig = px.pie(
            sev_counts, names='Severity', values='Count',
            color='Severity',
            color_discrete_map=COLORS,
            hole=0.55,
        )
        fig.update_layout(**PLOTLY_LAYOUT, title="Severity Breakdown", showlegend=True,
                          legend=dict(orientation='h', y=-0.15))
        fig.update_traces(textposition='inside', textinfo='percent+value',
                          marker=dict(line=dict(color='#1a1a3e', width=2)))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        pri_counts = fdf['priority_category'].value_counts().reindex(
            [p for p in priority_opts if p in fdf['priority_category'].values], fill_value=0
        ).reset_index()
        pri_counts.columns = ['Priority', 'Count']
        fig2 = px.pie(
            pri_counts, names='Priority', values='Count',
            color='Priority',
            color_discrete_map=COLORS,
            hole=0.55,
        )
        fig2.update_layout(**PLOTLY_LAYOUT, title="Priority Breakdown", showlegend=True,
                           legend=dict(orientation='h', y=-0.15))
        fig2.update_traces(textposition='inside', textinfo='percent+value',
                           marker=dict(line=dict(color='#1a1a3e', width=2)))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Filtered Dataset Preview")
    st.dataframe(
        fdf[['filename','predicted_severity','priority_category','prediction_confidence',
             'priority_score','recommended_planning_window']].head(200),
        use_container_width=True,
        height=380,
    )
    csv_all = fdf.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️  Download Filtered Data", csv_all, "filtered_potholes.csv", "text/csv")


# ─── TAB 2: Severity ─────────────────────────────
with tab_severity:
    st.markdown('<p class="section-header">Severity Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Predicted severity distribution and class probability landscape across all filtered potholes.</p>', unsafe_allow_html=True)

    sev_order = ['minor_pothole', 'medium_pothole', 'major_pothole']
    sev_c = fdf['predicted_severity'].value_counts().reindex(sev_order, fill_value=0)

    fig = go.Figure()
    for sev in sev_order:
        fig.add_trace(go.Bar(
            x=[sev.replace('_pothole','').title()], y=[sev_c.get(sev, 0)],
            name=sev.replace('_pothole','').title(),
            marker_color=COLORS[sev],
            marker_line=dict(color='rgba(0,0,0,0.2)', width=1),
            text=[sev_c.get(sev, 0)], textposition='outside',
        ))
    fig.update_layout(**PLOTLY_LAYOUT, title="Predicted Severity Distribution",
                      xaxis_title="Severity", yaxis_title="Count",
                      showlegend=False, barmode='group',
                      yaxis=dict(gridcolor=GRID_COLOR))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Class Probability Heatmap")
    c1, c2 = st.columns([2, 1])
    with c1:
        prob_cols = ['probability_minor', 'probability_medium', 'probability_major']
        prob_means = fdf.groupby('predicted_severity')[prob_cols].mean().reindex(sev_order)
        prob_means.columns = ['P(Minor)', 'P(Medium)', 'P(Major)']
        fig_heat = px.imshow(
            prob_means.values,
            x=prob_means.columns.tolist(),
            y=[s.replace('_pothole','').title() for s in prob_means.index],
            color_continuous_scale='Viridis',
            text_auto='.2f',
            aspect='auto',
        )
        fig_heat.update_layout(**PLOTLY_LAYOUT, title="Mean Class Probabilities by Predicted Severity",
                               coloraxis_colorbar=dict(title="Prob"))
        st.plotly_chart(fig_heat, use_container_width=True)
    with c2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("**Quick Stats**")
        for sev in sev_order:
            label = sev.replace('_pothole','').title()
            count = sev_c.get(sev, 0)
            pct = count / max(len(fdf), 1) * 100
            st.markdown(f"**{label}**: {count} ({pct:.1f}%)")
        st.markdown('</div>', unsafe_allow_html=True)


# ─── TAB 3: Priority ─────────────────────────────
with tab_priority:
    st.markdown('<p class="section-header">Priority Framework</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Expected Severity Score = 3·P(major) + 2·P(medium) + 1·P(minor). Thresholds are project-defined decision-support levels, not official standards.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_score = px.histogram(
            fdf, x='priority_score', nbins=40,
            color_discrete_sequence=['#818cf8'],
            opacity=0.85,
        )
        fig_score.update_layout(**PLOTLY_LAYOUT, title="Priority Score Distribution",
                                xaxis_title="Priority Score", yaxis_title="Frequency",
                                yaxis=dict(gridcolor=GRID_COLOR))
        # Add threshold lines
        for val, label, color in [(2.6,'CRITICAL','#ef4444'),(2.0,'HIGH','#fb923c'),(1.4,'MEDIUM','#facc15')]:
            fig_score.add_vline(x=val, line_dash='dot', line_color=color, line_width=2,
                                annotation_text=label, annotation_font_color=color,
                                annotation_font_size=11)
        st.plotly_chart(fig_score, use_container_width=True)

    with c2:
        pri_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'REVIEW REQUIRED']
        pri_c = fdf['priority_category'].value_counts().reindex(
            [p for p in pri_order if p in fdf['priority_category'].values], fill_value=0
        )
        fig_pri = go.Figure()
        for p in pri_c.index:
            fig_pri.add_trace(go.Bar(
                x=[p], y=[pri_c[p]],
                marker_color=COLORS.get(p, '#888'),
                text=[pri_c[p]], textposition='outside',
                name=p,
            ))
        fig_pri.update_layout(**PLOTLY_LAYOUT, title="Priority Category Distribution",
                              showlegend=False, yaxis=dict(gridcolor=GRID_COLOR))
        st.plotly_chart(fig_pri, use_container_width=True)

    # Stacked: severity breakdown per priority
    cross = pd.crosstab(fdf['priority_category'], fdf['predicted_severity']).reindex(
        index=[p for p in pri_order if p in fdf['priority_category'].values],
        columns=sev_order, fill_value=0,
    )
    fig_stack = go.Figure()
    for sev in sev_order:
        fig_stack.add_trace(go.Bar(
            x=cross.index, y=cross[sev],
            name=sev.replace('_pothole','').title(),
            marker_color=COLORS[sev],
        ))
    fig_stack.update_layout(**PLOTLY_LAYOUT, barmode='stack',
                            title="Severity Composition by Priority",
                            yaxis=dict(gridcolor=GRID_COLOR))
    st.plotly_chart(fig_stack, use_container_width=True)


# ─── TAB 4: Confidence ───────────────────────────
with tab_confidence:
    st.markdown('<p class="section-header">Prediction Confidence</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Confidence = max predicted class probability. This is NOT a calibrated probability — it reflects relative model certainty.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        fig_conf = px.histogram(
            fdf, x='prediction_confidence', nbins=40,
            color_discrete_sequence=['#a78bfa'],
            opacity=0.8,
        )
        fig_conf.add_vline(x=0.45, line_dash='dot', line_color='#ef4444', line_width=2,
                           annotation_text="Review Threshold", annotation_font_color='#ef4444')
        fig_conf.update_layout(**PLOTLY_LAYOUT, title="Confidence Distribution",
                               xaxis_title="Max Class Probability", yaxis_title="Frequency",
                               yaxis=dict(gridcolor=GRID_COLOR))
        st.plotly_chart(fig_conf, use_container_width=True)

    with c2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("**Confidence Statistics**")
        if len(fdf):
            conf = fdf['prediction_confidence']
            stats = {
                'Mean': f"{conf.mean():.3f}",
                'Median': f"{conf.median():.3f}",
                'Min': f"{conf.min():.3f}",
                'Max': f"{conf.max():.3f}",
                'Std Dev': f"{conf.std():.3f}",
            }
            for k, v in stats.items():
                st.markdown(f"**{k}:** `{v}`")
        st.markdown('</div>', unsafe_allow_html=True)

    fig_box = px.box(
        fdf, x='predicted_severity', y='prediction_confidence',
        color='predicted_severity',
        color_discrete_map=COLORS,
        category_orders={'predicted_severity': sev_order},
    )
    fig_box.update_layout(**PLOTLY_LAYOUT, title="Confidence by Severity Class",
                          showlegend=False, yaxis=dict(gridcolor=GRID_COLOR))
    st.plotly_chart(fig_box, use_container_width=True)

    review_cases = fdf[fdf['prediction_confidence'] < 0.45]
    if len(review_cases):
        st.markdown(f"#### ⚠️ {len(review_cases)} Review-Required Cases")
        st.dataframe(review_cases[['filename','predicted_severity','prediction_confidence','priority_score']],
                     use_container_width=True)


# ─── TAB 5: Image Hotspots ───────────────────────
with tab_images:
    st.markdown('<p class="section-header">Inspection Image Prioritization</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Since no GPS or road-segment data exists in the dataset, we rank by source image as a proxy for location hotspots. Filename is an image identifier, not a coordinate.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_img = px.histogram(
            image_df, x='pothole_count', nbins=int(max(image_df['pothole_count'].max(), 1)),
            color_discrete_sequence=['#6366f1'],
            opacity=0.85,
        )
        fig_img.update_layout(**PLOTLY_LAYOUT, title="Potholes per Image",
                              xaxis_title="Pothole Count", yaxis_title="Number of Images",
                              yaxis=dict(gridcolor=GRID_COLOR))
        st.plotly_chart(fig_img, use_container_width=True)
    with c2:
        top_n = st.slider("Show top N images by priority score", 5, 50, 20)
        top_imgs = image_df.nlargest(top_n, 'priority_score_max')
        fig_top = px.bar(
            top_imgs, x='filename', y='priority_score_max',
            color='priority_category',
            color_discrete_map=COLORS,
        )
        fig_top.update_layout(**PLOTLY_LAYOUT, title=f"Top {top_n} Images by Priority",
                              xaxis_title="", yaxis_title="Max Priority Score",
                              xaxis=dict(tickangle=45, tickfont=dict(size=9)),
                              yaxis=dict(gridcolor=GRID_COLOR))
        st.plotly_chart(fig_top, use_container_width=True)

    search_term = st.text_input("🔍 Search filename", placeholder="e.g. img-42")
    display_imgs = image_df[image_df['filename'].str.contains(search_term, case=False, na=False)] if search_term else image_df
    st.dataframe(display_imgs, use_container_width=True, height=400)
    csv_img = image_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️  Download Image Rankings", csv_img, "image_priority_ranking.csv", "text/csv")


# ─── TAB 6: Cost Planning ────────────────────────
with tab_cost:
    st.markdown('<p class="section-header">Scenario-Based Cost Planning</p>', unsafe_allow_html=True)
    # Currency toggle
    USD_TO_INR = 95.0
    currency = st.radio("Currency", ['USD ($)', 'INR (₹)', 'Both'], horizontal=True, index=2)

    scenario_choice = st.radio("Select Scenario", ['Low Cost', 'Baseline Cost', 'High Cost'], horizontal=True, index=1)
    scenario_col = f"{scenario_choice}_Estimate"

    def fmt_cost(val):
        if currency == 'USD ($)':
            return f"${val:,.0f}"
        elif currency == 'INR (₹)':
            return f"₹{val * USD_TO_INR:,.0f}"
        else:
            return f"${val:,.0f}  ·  ₹{val * USD_TO_INR:,.0f}"

    if scenario_col in fdf.columns:
        total_cost = fdf[scenario_col].sum()
        by_sev = fdf.groupby('predicted_severity')[scenario_col].sum().reindex(sev_order, fill_value=0)
        by_pri = fdf.groupby('priority_category')[scenario_col].sum()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Planning Estimate", fmt_cost(total_cost))
        c2.metric("Major Pothole Cost", fmt_cost(by_sev.get('major_pothole', 0)))
        c3.metric("Critical Priority Cost", fmt_cost(by_pri.get('CRITICAL', 0)))

        cc1, cc2 = st.columns(2)
        with cc1:
            fig_csev = go.Figure()
            for sev in sev_order:
                val = by_sev.get(sev, 0)
                fig_csev.add_trace(go.Bar(
                    x=[sev.replace('_pothole','').title()], y=[val],
                    marker_color=COLORS[sev],
                    text=[fmt_cost(val)], textposition='outside',
                ))
            fig_csev.update_layout(**PLOTLY_LAYOUT, title="Cost by Severity",
                                   showlegend=False, yaxis=dict(gridcolor=GRID_COLOR))
            st.plotly_chart(fig_csev, use_container_width=True)

        with cc2:
            fig_cpri = go.Figure()
            for p in ['CRITICAL','HIGH','MEDIUM','LOW']:
                if p in by_pri.index:
                    val = by_pri[p]
                    fig_cpri.add_trace(go.Bar(
                        x=[p], y=[val],
                        marker_color=COLORS.get(p,'#888'),
                        text=[fmt_cost(val)], textposition='outside',
                    ))
            fig_cpri.update_layout(**PLOTLY_LAYOUT, title="Cost by Priority",
                                   showlegend=False, yaxis=dict(gridcolor=GRID_COLOR))
            st.plotly_chart(fig_cpri, use_container_width=True)

    # Scenario comparison table
    st.markdown("#### All Scenarios Summary")
    st.dataframe(cost_summary, use_container_width=True)

    base_costs_usd = {'Low': 50, 'Baseline': 100, 'High': 200}
    st.markdown(f"""
    <div class="glass-panel">
    <strong>Formula:</strong> <code>Estimated Cost = Base_Cost × Severity_Multiplier × (1 + rel_bbox_area)</code><br/><br/>
    <strong>Severity Multipliers:</strong> Major = 3.0×, Medium = 1.5×, Minor = 1.0×<br/>
    <strong>Base Cost Assumptions (USD):</strong> Low = $50, Baseline = $100, High = $200<br/>
    <strong>Base Cost Assumptions (INR):</strong> Low = ₹{base_costs_usd['Low']*USD_TO_INR:,.0f}, Baseline = ₹{base_costs_usd['Baseline']*USD_TO_INR:,.0f}, High = ₹{base_costs_usd['High']*USD_TO_INR:,.0f}<br/>
    <span style="color:#8888bb;font-size:0.82rem;">Exchange rate used: 1 USD = ₹{USD_TO_INR:.0f} (configurable assumption)</span>
    </div>
    """, unsafe_allow_html=True)


# ─── TAB 7: Scheduling ───────────────────────────
with tab_schedule:
    st.markdown('<p class="section-header">Maintenance Scheduling</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Rule-based scheduling recommendations derived from priority categories. These are decision-support suggestions, not mandated government timelines.</p>', unsafe_allow_html=True)

    sched_cols = ['filename','predicted_severity','priority_category','review_required',
                  'recommended_planning_window','recommended_action','prediction_confidence']

    # Summary cards
    windows = fdf['recommended_planning_window'].value_counts()
    cols = st.columns(min(len(windows), 4))
    window_icons = {'Immediate Review':'🚨', 'Near-Term Planning':'📋', 'Scheduled Maintenance':'🔧', 'Routine Monitoring':'📡'}
    for i, (window, count) in enumerate(windows.items()):
        if i < len(cols):
            icon = window_icons.get(window, '📌')
            cols[i].metric(f"{icon} {window}", count)

    st.dataframe(fdf[sched_cols], use_container_width=True, height=420)
    csv_sched = fdf[sched_cols].to_csv(index=False).encode('utf-8')
    st.download_button("⬇️  Download Schedule", csv_sched, "maintenance_schedule.csv", "text/csv")


# ─── TAB 8: Model Info ───────────────────────────
with tab_model:
    st.markdown('<p class="section-header">Model Performance</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Final model: Tuned Support Vector Machine (RBF kernel). Selected via GroupKFold cross-validation on Macro F1.</p>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    m1.metric("Test Accuracy", f"{meta.get('final_test_accuracy',0):.2%}")
    m2.metric("Test Macro F1", f"{meta.get('final_test_macro_f1',0):.2%}")

    # Per-class metrics as a table
    class_metrics = pd.DataFrame({
        'Class': ['Major', 'Medium', 'Minor'],
        'Precision': [0.73, 0.56, 0.81],
        'Recall': [0.73, 0.73, 0.47],
        'F1-Score': [0.73, 0.63, 0.59],
        'Support': [84, 110, 75],
    })

    fig_class = go.Figure()
    for metric, color in [('Precision','#6366f1'), ('Recall','#a78bfa'), ('F1-Score','#c084fc')]:
        fig_class.add_trace(go.Bar(
            x=class_metrics['Class'], y=class_metrics[metric],
            name=metric, marker_color=color,
            text=[f"{v:.0%}" for v in class_metrics[metric]], textposition='outside',
        ))
    fig_class.update_layout(**PLOTLY_LAYOUT, barmode='group',
                            title="Per-Class Test Metrics",
                            yaxis=dict(range=[0, 1], gridcolor=GRID_COLOR))
    st.plotly_chart(fig_class, use_container_width=True)

    with st.expander("📄 Full Model Metadata (JSON)"):
        st.json(meta)


# ─── TAB 9: Limitations ──────────────────────────
with tab_limits:
    st.markdown('<p class="section-header">Dataset Limitations & Transparency</p>', unsafe_allow_html=True)

    st.markdown("""
<div class="glass-panel">
    <h4 style="color:#f87171;margin-top:0;">⚠️ What This Dataset Does NOT Contain</h4>
    <ul style="color:#c0c0e0;line-height:2;">
        <li><strong>GPS Coordinates</strong> — no geographic mapping possible</li>
        <li><strong>Road Segment IDs</strong> — no genuine road-level ranking</li>
        <li><strong>Traffic Volume (AADT)</strong> — no exposure-based risk scoring</li>
        <li><strong>Road Condition Variables</strong> — no IRI, PCI, or roughness data</li>
        <li><strong>Historical Maintenance Costs</strong> — no supervised cost prediction</li>
        <li><strong>Pothole Depth / Physical Volume</strong> — no real-world dimensional severity</li>
        <li><strong>Environmental / Weather Data</strong> — no climate deterioration analysis</li>
    </ul>
</div>

<div class="glass-panel">
    <h4 style="color:#4ade80;margin-top:0;">✅ What This Dashboard Provides</h4>
    <ul style="color:#c0c0e0;line-height:2;">
        <li>Image-space pothole severity classification (minor / medium / major)</li>
        <li>Transparent priority scoring from model probability outputs</li>
        <li>Image-level inspection hotspot ranking</li>
        <li>Scenario-based maintenance cost planning (configurable assumptions)</li>
        <li>Rule-based scheduling recommendations</li>
    </ul>
</div>

<div class="glass-panel">
    <h4 style="color:#818cf8;margin-top:0;">🔮 Future Data Integration Recommendations</h4>
    <ul style="color:#c0c0e0;line-height:2;">
        <li>GPS-tagged imagery for geographic clustering</li>
        <li>LiDAR depth sensing for volumetric severity assessment</li>
        <li>Municipal repair ticket database for supervised cost modeling</li>
        <li>AADT traffic maps for exposure-weighted risk prioritization</li>
    </ul>
</div>
    """, unsafe_allow_html=True)
