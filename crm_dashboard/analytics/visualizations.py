"""
CRM Analytics Visualizations
Renders charts and visualizations for analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List


def render_metric_cards(metrics: Dict, title: str):
    """Render metric cards in a row"""
    st.markdown(f"#### {title}")
    
    cols = st.columns(len(metrics))
    
    for idx, (label, value) in enumerate(metrics.items()):
        with cols[idx]:
            # Determine color based on value type
            if isinstance(value, dict):
                display_value = value.get('value', 0)
                delta = value.get('delta', None)
            else:
                display_value = value
                delta = None
            
            st.metric(
                label=label,
                value=display_value,
                delta=delta
            )


def render_completion_rate_chart(data: Dict):
    """Render completion rate visualization"""
    st.markdown("#### 📈 Completion Rate")
    
    # Create data for chart
    categories = ['In Scope', 'Out of Scope', 'Data Incorrect', 'Not Started']
    values = [
        data.get('in_scope', 0),
        data.get('out_of_scope', 0),
        data.get('data_incorrect', 0),
        data.get('not_started', 0)
    ]
    colors = ['#29C46F', '#808080', '#F44336', '#FFC107']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Configuration Status Distribution",
        xaxis_title="Status",
        yaxis_title="Count",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_regional_heatmap(regional_data: Dict, status_field: str):
    """Render regional performance heatmap"""
    st.markdown("#### 🌍 Regional Performance")
    
    # Prepare data for heatmap
    regions = list(regional_data.keys())
    
    if not regions:
        st.info("No regional data available")
        return
    
    # Get all unique statuses
    all_statuses = set()
    for region_info in regional_data.values():
        all_statuses.update(region_info['status_counts'].keys())
    
    all_statuses = sorted(list(all_statuses))
    
    # Create matrix
    matrix = []
    for status in all_statuses:
        row = []
        for region in regions:
            count = regional_data[region]['status_counts'].get(status, 0)
            row.append(count)
        matrix.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=regions,
        y=all_statuses,
        colorscale='Greens',
        text=matrix,
        texttemplate='%{text}',
        textfont={"size": 12}
    ))
    
    fig.update_layout(
        title=f"{status_field} by Region",
        xaxis_title="Region",
        yaxis_title="Status",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_pie_chart(data: Dict, title: str, labels: List[str], values_keys: List[str], colors: List[str]):
    """Render pie chart"""
    st.markdown(f"#### {title}")
    
    values = [data.get(key, 0) for key in values_keys]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        hole=0.3,
        textinfo='label+percent+value',
        textposition='auto'
    )])
    
    fig.update_layout(
        title=title,
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_out_of_scope_analysis(out_of_scope_by_region: Dict):
    """Render out of scope analysis with focus areas"""
    st.markdown("#### 🔴 Out of Scope Analysis")
    
    if not out_of_scope_by_region:
        st.success("✅ No out of scope items!")
        return
    
    # Sort by percentage descending
    sorted_regions = sorted(
        out_of_scope_by_region.items(),
        key=lambda x: x[1]['percentage'],
        reverse=True
    )
    
    # Display as cards
    for region, data in sorted_regions:
        if data['count'] > 0:
            pct = data['percentage']
            
            # Determine severity
            if pct >= 50:
                color = "🔴"
                severity = "CRITICAL"
            elif pct >= 30:
                color = "🟠"
                severity = "HIGH"
            elif pct >= 10:
                color = "🟡"
                severity = "MEDIUM"
            else:
                color = "🟢"
                severity = "LOW"
            
            st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid {'#F44336' if pct >= 50 else '#FF9800' if pct >= 30 else '#FFC107' if pct >= 10 else '#4CAF50'};">
                <h4 style="margin: 0;">{color} {region}</h4>
                <p style="margin: 5px 0;"><strong>{data['count']}</strong> stores Not Configured ({pct:.1f}% of region)</p>
                <p style="margin: 5px 0; color: #888;">Severity: {severity}</p>
                <p style="margin: 5px 0; font-size: 12px;">💡 Action: Investigate why these stores are not configured and explore conversion opportunities</p>
            </div>
            """, unsafe_allow_html=True)


def render_test_pass_rates(test_pass_rates: Dict):
    """Render test-specific pass rates"""
    st.markdown("#### 🧪 Test-Specific Pass Rates")
    
    if not test_pass_rates:
        st.info("No test data available")
        return
    
    # Create bar chart
    tests = list(test_pass_rates.keys())
    pass_rates = [test_pass_rates[test]['pass_rate'] for test in tests]
    passed = [test_pass_rates[test]['passed'] for test in tests]
    total = [test_pass_rates[test]['total'] for test in tests]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tests,
        y=pass_rates,
        text=[f"{p}/{t}<br>({pr:.1f}%)" for p, t, pr in zip(passed, total, pass_rates)],
        textposition='auto',
        marker_color=['#29C46F' if pr >= 80 else '#FFC107' if pr >= 60 else '#F44336' for pr in pass_rates]
    ))
    
    fig.update_layout(
        title="Test Pass Rates",
        xaxis_title="Test",
        yaxis_title="Pass Rate (%)",
        height=400,
        yaxis_range=[0, 100]
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_score_distribution(score_dist: Dict):
    """Render weighted score distribution"""
    st.markdown("#### 📊 Weighted Score Distribution")
    
    categories = ['Excellent\n(90-100%)', 'Good\n(75-89%)', 'Needs Improvement\n(60-74%)', 'Critical\n(<60%)']
    values = [
        score_dist.get('excellent', 0),
        score_dist.get('good', 0),
        score_dist.get('needs_improvement', 0),
        score_dist.get('critical', 0)
    ]
    colors = ['#29C46F', '#3874F2', '#FFC107', '#F44336']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title=f"Score Distribution (Avg: {score_dist.get('average_score', 0):.1f}%)",
        xaxis_title="Score Range",
        yaxis_title="Count",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_at_risk_stores(at_risk_stores: List[Dict]):
    """Render at-risk stores table"""
    st.markdown("#### ⚠️ At-Risk Stores (<7 Days to Go Live, Not GTG)")

    if not at_risk_stores:
        st.success("✅ No at-risk stores!")
        return

    df = pd.DataFrame(at_risk_stores)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.warning(f"🚨 {len(at_risk_stores)} stores require immediate attention!")


def render_assignee_performance(assignee_data: Dict, category: str):
    """Render assignee performance analysis"""
    st.markdown(f"#### 👤 Assignee Performance - {category}")

    if not assignee_data:
        st.info("No assignee data available")
        return

    # Create DataFrame for display
    rows = []
    for assignee, metrics in assignee_data.items():
        row = {'Assignee': assignee}
        row.update(metrics)
        rows.append(row)

    df = pd.DataFrame(rows)

    if category == "Configuration":
        # Sort by completion rate
        df = df.sort_values('completion_rate', ascending=False)

        # Bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['Assignee'],
            y=df['completion_rate'],
            text=df['completion_rate'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
            marker_color=['#29C46F' if x >= 80 else '#FFC107' if x >= 60 else '#F44336' for x in df['completion_rate']],
            name='Completion Rate'
        ))

        fig.update_layout(
            title="Configuration Completion Rate by Assignee",
            xaxis_title="Assignee",
            yaxis_title="Completion Rate (%)",
            height=400,
            yaxis_range=[0, 100]
        )

        st.plotly_chart(fig, use_container_width=True)

        # Table - format completion rate
        display_df = df[['Assignee', 'total', 'in_scope', 'out_of_scope', 'completion_rate']].copy()
        display_df['completion_rate'] = display_df['completion_rate'].apply(lambda x: f"{x:.2f}")

        st.dataframe(
            display_df.rename(columns={
                'total': 'Total',
                'in_scope': 'In Scope',
                'out_of_scope': 'Out of Scope',
                'completion_rate': 'Completion Rate (%)'
            }),
            use_container_width=True,
            hide_index=True
        )

    elif category == "Pre Go Live":
        # Sort by GTG rate
        df = df.sort_values('gtg_rate', ascending=False)

        # Bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['Assignee'],
            y=df['gtg_rate'],
            text=df['gtg_rate'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
            marker_color=['#29C46F' if x >= 80 else '#FFC107' if x >= 60 else '#F44336' for x in df['gtg_rate']],
            name='GTG Rate'
        ))

        fig.update_layout(
            title="Pre Go Live GTG Rate by Assignee",
            xaxis_title="Assignee",
            yaxis_title="GTG Rate (%)",
            height=400,
            yaxis_range=[0, 100]
        )

        st.plotly_chart(fig, use_container_width=True)

        # Table - format GTG rate
        display_df = df[['Assignee', 'total', 'gtg', 'gtg_rate']].copy()
        display_df['gtg_rate'] = display_df['gtg_rate'].apply(lambda x: f"{x:.2f}")

        st.dataframe(
            display_df.rename(columns={
                'total': 'Total',
                'gtg': 'GTG',
                'gtg_rate': 'GTG Rate (%)'
            }),
            use_container_width=True,
            hide_index=True
        )

    elif category == "Go Live Testing":
        # Sort by GTG rate
        df = df.sort_values('gtg_rate', ascending=False)

        # Bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['Assignee'],
            y=df['gtg_rate'],
            text=df['gtg_rate'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
            marker_color=['#29C46F' if x >= 80 else '#FFC107' if x >= 60 else '#F44336' for x in df['gtg_rate']],
            name='GTG Rate'
        ))

        fig.update_layout(
            title="Go Live Testing GTG Rate by Assignee",
            xaxis_title="Assignee",
            yaxis_title="GTG Rate (%)",
            height=400,
            yaxis_range=[0, 100]
        )

        st.plotly_chart(fig, use_container_width=True)

        # Table - format GTG rate
        display_df = df[['Assignee', 'total', 'gtg', 'blockers', 'gtg_rate']].copy()
        display_df['gtg_rate'] = display_df['gtg_rate'].apply(lambda x: f"{x:.2f}")

        st.dataframe(
            display_df.rename(columns={
                'total': 'Total',
                'gtg': 'GTG',
                'blockers': 'Blockers',
                'gtg_rate': 'GTG Rate (%)'
            }),
            use_container_width=True,
            hide_index=True
        )
