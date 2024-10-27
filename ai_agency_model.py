import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def main():
    st.title("AI Automation Agency Financial Model")

    st.sidebar.header("Input Variables")

    # Top-of-Funnel Metrics
    impressions_per_week = st.sidebar.number_input(
        "Impressions per Week", value=10000, min_value=0, step=1000
    )
    ctr = (
        st.sidebar.slider(
            "Click-Through Rate (CTR) %",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.5,
        )
        / 100
    )
    conversion_to_leads = (
        st.sidebar.slider(
            "Conversion Rate to Leads %",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.5,
        )
        / 100
    )
    conversion_to_warm_leads = (
        st.sidebar.slider(
            "Conversion Rate to Warm Leads %",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=0.5,
        )
        / 100
    )
    sales_conversion_rate = (
        st.sidebar.slider(
            "Sales Conversion Rate %",
            min_value=0.0,
            max_value=100.0,
            value=25.0,
            step=0.5,
        )
        / 100
    )

    # Sales Metrics
    average_project_price = st.sidebar.number_input(
        "Average Project Price ($)", value=10000, min_value=0, step=1000
    )
    profit_margin = (
        st.sidebar.slider(
            "Profit Margin %", min_value=0.0, max_value=100.0, value=60.0, step=0.5
        )
        / 100
    )

    # Cost Metrics
    cost_per_project = average_project_price * (1 - profit_margin)
    developer_cost_per_hour = st.sidebar.number_input(
        "Developer Cost per Hour ($)", value=50, min_value=0, step=5
    )
    hours_per_project = st.sidebar.number_input(
        "Hours per Project", value=80, min_value=0, step=5
    )

    # Capacity Metrics
    project_duration_weeks = st.sidebar.number_input(
        "Project Duration (weeks)", value=2, min_value=1, step=1
    )
    developer_hours_per_week = st.sidebar.number_input(
        "Developer Work Hours per Week", value=40, min_value=0, step=5
    )

    # Calculations
    leads_per_week = impressions_per_week * ctr * conversion_to_leads
    warm_leads_per_week = leads_per_week * conversion_to_warm_leads
    clients_per_week = warm_leads_per_week * sales_conversion_rate

    weekly_revenue = clients_per_week * average_project_price
    annual_revenue = weekly_revenue * 52
    annual_profit = annual_revenue * profit_margin

    total_projects_per_year = clients_per_week * 52
    hours_needed_per_year = total_projects_per_year * hours_per_project

    # Calculate Concurrent Projects
    concurrent_projects = clients_per_week * project_duration_weeks

    # Total Hours Needed per Week considering Project Duration
    total_hours_per_week = concurrent_projects * (
        hours_per_project / project_duration_weeks
    )

    # Developers Needed based on weekly capacity
    developers_needed = total_hours_per_week / developer_hours_per_week

    # Output
    st.header("Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sales Funnel Metrics")
        st.write(f"Leads per Week: **{leads_per_week:.2f}**")
        st.write(f"Warm Leads per Week: **{warm_leads_per_week:.2f}**")
        st.write(f"Clients per Week: **{clients_per_week:.2f}**")

    with col2:
        st.subheader("Financial Metrics")
        st.write(f"Weekly Revenue: **${weekly_revenue:,.2f}**")
        st.write(f"Annual Revenue: **${annual_revenue:,.2f}**")
        st.write(f"Annual Profit: **${annual_profit:,.2f}**")

    st.subheader("Operational Metrics")
    st.write(f"Total Projects per Year: **{total_projects_per_year:.2f}**")
    st.write(f"Concurrent Projects: **{concurrent_projects:.2f}**")
    st.write(f"Total Developer Hours Needed per Week: **{total_hours_per_week:.2f}**")
    st.write(f"Developers Needed: **{developers_needed:.2f}**")
    st.write(f"Cost per Project: **${cost_per_project:,.2f}**")

    # Visualizations
    st.header("Visualizations")

    # Time to Reach $1 Million Profit
    if annual_profit > 0:
        time_to_million_years = 1_000_000 / annual_profit
        st.write(
            f"Time to Reach $1 Million Profit: **{time_to_million_years:.2f} years**"
        )
    else:
        st.write(
            "Annual profit is zero or negative; cannot reach $1 million profit with current inputs."
        )

    # Sales Funnel Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    funnel_stages = ["Impressions", "Clicks", "Leads", "Warm Leads", "Clients"]
    funnel_values = [
        impressions_per_week,
        impressions_per_week * ctr,
        leads_per_week,
        warm_leads_per_week,
        clients_per_week,
    ]
    bars = ax.bar(funnel_stages, funnel_values)
    ax.set_title("Weekly Sales Funnel")
    ax.set_ylabel("Number of People (log scale)")
    ax.set_yscale("log")  # Set y-axis to logarithmic scale
    plt.xticks(rotation=45)

    # Add numbers above the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.2f}",
            ha="center",
            va="bottom",
        )

    st.pyplot(fig)

    # Profit vs. Number of Developers
    developer_range = range(1, max(int(developers_needed * 2), 10) + 1)
    profits = []
    for devs in developer_range:
        capacity = devs * developer_hours_per_week
        possible_projects = min(capacity / hours_per_project, total_projects_per_year)
        possible_annual_revenue = possible_projects * average_project_price
        possible_annual_profit = possible_annual_revenue * profit_margin
        profits.append(possible_annual_profit)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(developer_range, profits)
    ax.set_xlabel("Number of Developers")
    ax.set_ylabel("Annual Profit ($)")
    ax.set_title("Annual Profit vs. Number of Developers")
    ax.axvline(
        x=developers_needed, color="r", linestyle="--", label="Developers Needed"
    )
    ax.axhline(
        y=annual_profit, color="g", linestyle="--", label="Current Annual Profit"
    )
    ax.legend()
    st.pyplot(fig)

    # Project Timeline
    weeks = 52
    projects_timeline = []
    ongoing_projects = 0
    projects_starting = clients_per_week
    for week in range(1, weeks + 1):
        # Projects starting this week
        starting = projects_starting
        # Projects ending this week
        if week > project_duration_weeks:
            ending = projects_starting
        else:
            ending = 0
        # Update ongoing projects
        ongoing_projects += starting - ending
        projects_timeline.append(ongoing_projects)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, weeks + 1), projects_timeline)
    ax.set_xlabel("Weeks")
    ax.set_ylabel("Cumulative Projects")
    ax.set_title("Cumulative Projects Over Time")
    st.pyplot(fig)


if __name__ == "__main__":
    main()
