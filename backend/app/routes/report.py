from fastapi import APIRouter
from fastapi.responses import FileResponse
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet

router = APIRouter()


@router.get("/report")
def generate_report():

    pdf_path = "outputs/GridLock_Report.pdf"

    # Load data
    hotspots = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    patrol = pd.read_csv(
        "outputs/patrol_plan.csv"
    )

    # Summary metrics
    total_violations = int(
        hotspots["violations"].sum()
    )

    total_hotspots = len(
        hotspots
    )

    high_risk = len(
        patrol[
            patrol["risk_score"] > 60
        ]
    )

    top_hotspot = (
        hotspots
        .sort_values(
            "violations",
            ascending=False
        )
        .iloc[0]
    )

    # PDF
    doc = SimpleDocTemplate(
        pdf_path
    )

    styles = (
        getSampleStyleSheet()
    )

    content = []

    # Title
    content.append(
        Paragraph(
            "GRIDLOCK AI",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "AI-Powered Parking Intelligence & Patrol Optimization Report",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # Executive Summary
    content.append(
        Paragraph(
            "Executive Summary",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"Total Violations Detected: {total_violations:,}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Total Hotspots Identified: {total_hotspots}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"High Risk Zones: {high_risk}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    # Highest Priority Hotspot
    content.append(
        Paragraph(
            "Highest Priority Hotspot",
            styles["Heading1"]
        )
    )

    hotspot_name = top_hotspot[
        "top_junction"
    ]

    if str(hotspot_name) == "No Junction":
        hotspot_name = (
            top_hotspot[
                "police_station"
            ]
            + " Area"
        )

    content.append(
        Paragraph(
            f"Location: {hotspot_name}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Police Station: {top_hotspot['police_station']}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Violations: {int(top_hotspot['violations']):,}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    # Top 5 Hotspots
    content.append(
        Paragraph(
            "Top 5 Hotspots",
            styles["Heading1"]
        )
    )

    top5 = (
        hotspots
        .sort_values(
            "violations",
            ascending=False
        )
        .head(5)
    )

    for _, row in top5.iterrows():

        name = row[
            "top_junction"
        ]

        if str(name) == "No Junction":
            name = (
                row[
                    "police_station"
                ]
                + " Area"
            )

        content.append(
            Paragraph(
                f"• {name} - {int(row['violations']):,} violations",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 15)
    )

    # Recommendations
    content.append(
        Paragraph(
            "AI Recommendations",
            styles["Heading1"]
        )
    )

    recommendations = [
        "Deploy additional officers to high-risk hotspots.",
        "Prioritize emerging hotspots before congestion spreads.",
        "Use optimized patrol routes for maximum coverage.",
        "Monitor uncovered risk zones identified by the dashboard.",
        "Increase patrol frequency during peak traffic hours."
    ]

    for rec in recommendations:
        content.append(
            Paragraph(
                f"• {rec}",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 15)
    )

    # Conclusion
    content.append(
        Paragraph(
            "Conclusion",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            "GRIDLOCK AI provides actionable intelligence for police departments by identifying parking-related congestion hotspots, recommending patrol deployment, optimizing routes, and predicting traffic impact. The system enables proactive enforcement and improved urban mobility.",
            styles["BodyText"]
        )
    )

    # Build PDF
    doc.build(content)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="GridLock_Report.pdf"
    )

