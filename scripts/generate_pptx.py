#!/usr/bin/env python3
"""
SalesSlice PPTX Generator
Generates a 10-slide executive presentation in Microsoft PowerPoint (.pptx) format
using Python's standard library zipfile and XML.
"""

import os
import zipfile
import xml.sax.saxutils as saxutils

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PPTX = os.path.join(BASE_DIR, "presentation", "SalesSlice_Executive_Presentation.pptx")

# 10 Slides content
SLIDES = [
    {
        "title": "SalesSlice – Interactive Retail Analytics Dashboard",
        "subtitle": "Executive Presentation & Technical Architecture (Jun 2024 – Aug 2024)\nPresenter: Yaswanth Michanagatla\nTools: Microsoft Power BI, SQL Server Management Studio (SSMS)",
        "bullets": []
    },
    {
        "title": "Business Problem & Project Objectives",
        "subtitle": "Addressing Reporting Bottlenecks Across 8 Store Locations",
        "bullets": [
            "Manual Reporting Overhead: Regional store managers spent 15+ hours weekly assembling disconnected spreadsheets.",
            "High Query Latency: Legacy reporting queries experienced full table scans and 4+ second turnaround times.",
            "Lack of Unified Analytics: No single source of truth across 5 product lines and 8 store territories.",
            "Primary Objective: Design a centralized Kimball Star Schema data warehouse and an interactive Power BI dashboard with sub-second performance."
        ]
    },
    {
        "title": "Executive Summary & Core Business Metrics",
        "subtitle": "12-Month Consolidated Performance (July 2023 – June 2024)",
        "bullets": [
            "$10,015,154 Total Net Sales Revenue across 366 reporting calendar days.",
            "$6,100,019 Total Gross Profit realized with an overall 60.91% Gross Margin.",
            "77,033 Completed Customer Transactions generating 110,933 physical units sold.",
            "$130.01 Average Order Value (AOV) across 1,200 unique segmented shoppers.",
            "25% Reduction in manual reporting labor achieved immediately upon deployment."
        ]
    },
    {
        "title": "Kimball Star Schema Data Warehouse Design",
        "subtitle": "Engineered for VertiPaq Columnar Compression in Power BI",
        "bullets": [
            "Central Fact Table: FactSales (77,033 rows; grain = individual POS line item).",
            "Store Dimension: DimStore (8 metropolitan locations with square footage and sales targets).",
            "Product Dimension: DimProduct (40 SKUs across 5 core retail lines with margin thresholds).",
            "Calendar Dimension: DimDate (366 days with ISO attributes, seasonality, and holiday flags).",
            "Customer & Promotion Dimensions: DimCustomer (1,200 accounts) and DimPromotion (6 campaigns).",
            "Deterministic 1-to-Many single-direction relationships with zero bidirectional ambiguity."
        ]
    },
    {
        "title": "SQL Server Query Optimization Case Study",
        "subtitle": "Achieving -30% Report Turnaround and -40% Dashboard Load Time",
        "bullets": [
            "30.1% Faster Batch Turnaround: Analytical execution time reduced from 4.21s to 2.94s.",
            "40.0% Faster Dashboard Load: Power BI DirectQuery visual loading dropped from 8.52s to 5.11s.",
            "72.0% I/O Reduction: Fact table logical page reads decreased from 14,820 to 4,149 pages.",
            "SARGable Predicate Refactoring: Replaced non-SARGable YEAR() calls with integer DateKey seeks.",
            "Covering Index Strategy: IX_FactSales_Store_Date_Covering with INCLUDE eliminated 100% of bookmark lookups.",
            "Materialized Indexed Views: Pre-aggregated store metrics with SCHEMABINDING and clustered index."
        ]
    },
    {
        "title": "Power BI Semantic Model & DAX Library",
        "subtitle": "18+ Robust Business Formulations Across 4 Operational Categories",
        "bullets": [
            "Financial Core: [Total Sales], [Total Cost], [Gross Profit], [Gross Margin %], [AOV], [Discount Rate %].",
            "Time Intelligence: [Sales YTD], [Sales Prior Month], [MoM Sales Growth %], [YoY Sales Growth %], [3M Moving Avg].",
            "Spatial Productivity: [Sales per Sq Ft] ($/sq ft) measuring commercial floor space efficiency.",
            "Target Attainment: [Annual Store Target] and [Target Attainment %] tracking quota pace.",
            "Performance Ranking: Dynamic store leaderboard rank using dense rank formulations."
        ]
    },
    {
        "title": "4-Page Dashboard Visual Architecture",
        "subtitle": "Mapping 17 Interactive Visualizations to Stakeholder Decisions",
        "bullets": [
            "Page 1: Executive KPI & Revenue Overview (Visuals 1–7: Revenue, Margin, Orders, Quota, Seasonality, Line Share, Leaderboard).",
            "Page 2: Store Locations & Spatial Efficiency (Visuals 8–11: Sales vs Budget, $/SqFt, Regional Split, Traffic vs Basket Scatter).",
            "Page 3: Product Line & Category Deep Dive (Visuals 12–15: Quarterly Evolution, Margin vs Volume Quadrant, Top Subcategories, Waterfall).",
            "Page 4: Customer Trends & Time Dynamics (Visuals 16–17: Day-of-Week Sales Distribution, Loyalty Segment Share).",
            "Global Interactive Slicers: Filter by Store Location, Product Line, and Date Range across all pages."
        ]
    },
    {
        "title": "Key Retail Insights & Strategic Findings",
        "subtitle": "Data-Driven Recommendations for Retail Operations Leadership",
        "bullets": [
            "Spatial Champion: Lincoln Road Center generated highest spatial productivity ($112/sq ft) despite smaller floor plan.",
            "Category Volume Driver: Electronics & Gadgets led gross turnover ($2.49M, 24.8% share).",
            "Highest Margin Line: Beauty & Personal Care delivered peak margins (65.4%) with lowest return rate.",
            "Weekend Surge: Friday through Sunday checkouts generated 50.1% ($5.02M) of consolidated sales.",
            "Promotional Impact: Discount markdowns averaged 5.96% of gross value, preserving 60.91% realized margin."
        ]
    },
    {
        "title": "Stakeholder ROI & Business Value",
        "subtitle": "Tangible Operational Improvements Delivered by SalesSlice",
        "bullets": [
            "25% Labor Reduction: Eliminated 60+ monthly hours of manual spreadsheet compilation.",
            "Sub-Second Executive Decisions: Immediate cross-filtering across store and product dimensions.",
            "Single Source of Truth: Eradicated reporting discrepancies between store managers and corporate finance.",
            "Enterprise Scalability: Partition-ready architecture capable of ingesting multi-year retail transaction growth."
        ]
    },
    {
        "title": "Conclusion, Repository & Live Demonstration",
        "subtitle": "Explore the Codebase, Database Scripts, and Interactive Dashboard",
        "bullets": [
            "GitHub Repository: https://github.com/MICHANAGATLAYASWANTH/SalesSlice",
            "Live Interactive Web Demo: https://michanagatlayaswanth.github.io/SalesSlice/",
            "Technical Documentation: Includes Data Dictionary, KPI Catalog, and SQL Optimization Report.",
            "Tools Leveraged: Microsoft Power BI, SQL Server Management Studio (SSMS), T-SQL, Python, Tailwind CSS, Chart.js."
        ]
    }
]

def make_pptx():
    with zipfile.ZipFile(OUTPUT_PPTX, "w", zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout2.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
"""
        for i in range(1, len(SLIDES) + 1):
            content_types += f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
        content_types += "</Types>"
        z.writestr("[Content_Types].xml", content_types)

        # _rels/.rels
        z.writestr("_rels/.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>""")

        # docProps/core.xml
        z.writestr("docProps/core.xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>SalesSlice – Interactive Retail Analytics Dashboard</dc:title>
  <dc:creator>Yaswanth Michanagatla</dc:creator>
  <cp:lastModifiedBy>Yaswanth Michanagatla</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2024-08-15T10:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2024-08-15T10:00:00Z</dcterms:modified>
</cp:coreProperties>""")

        # docProps/app.xml
        z.writestr("docProps/app.xml", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <TotalTime>0</TotalTime>
  <Words>850</Words>
  <Application>Microsoft PowerPoint</Application>
  <PresentationFormat>On-screen Show (16:9)</PresentationFormat>
  <Slides>{len(SLIDES)}</Slides>
</Properties>""")

        # ppt/_rels/presentation.xml.rels
        pres_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
"""
        for i in range(1, len(SLIDES) + 1):
            pres_rels += f'  <Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
        pres_rels += "</Relationships>"
        z.writestr("ppt/_rels/presentation.xml.rels", pres_rels)

        # ppt/presentation.xml
        sldIdLst = ""
        for i in range(1, len(SLIDES) + 1):
            sldIdLst += f'    <p:sldId id="{255 + i}" r:id="rId{i+1}"/>\n'

        z.writestr("ppt/presentation.xml", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
{sldIdLst}  </p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>""")

        # ppt/theme/theme1.xml
        z.writestr("ppt/theme/theme1.xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="SalesSlice Slate">
  <a:themeElements>
    <a:clrScheme name="SalesSlice">
      <a:dk1><a:srgbClr val="0F172A"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1E293B"/></a:dk2>
      <a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="0284C7"/></a:accent1>
      <a:accent2><a:srgbClr val="10B981"/></a:accent2>
      <a:accent3><a:srgbClr val="6366F1"/></a:accent3>
      <a:accent4><a:srgbClr val="F59E0B"/></a:accent4>
      <a:accent5><a:srgbClr val="EC4899"/></a:accent5>
      <a:accent6><a:srgbClr val="0EA5E9"/></a:accent6>
      <a:hlink><a:srgbClr val="0284C7"/></a:hlink>
      <a:folHlink><a:srgbClr val="6366F1"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="SalesSliceFont">
      <a:majorFont><a:latin typeface="Segoe UI Semibold"/></a:majorFont>
      <a:minorFont><a:latin typeface="Segoe UI"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="25400"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="38100"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>""")

        # ppt/slideMasters/slideMaster1.xml
        z.writestr("ppt/slideMasters/slideMaster1.xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
    <p:sldLayoutId id="2147483650" r:id="rId2"/>
  </p:sldLayoutIdLst>
  <p:txStyles>
    <p:titleStyle><a:lvl1pPr><a:defRPr sz="4000" b="1"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill></a:defRPr></a:lvl1pPr></p:titleStyle>
    <p:bodyStyle><a:lvl1pPr><a:defRPr sz="2000"><a:solidFill><a:schemeClr val="tx2"/></a:solidFill></a:defRPr></a:lvl1pPr></p:bodyStyle>
    <p:otherStyle/>
  </p:txStyles>
</p:sldMaster>""")

        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>""")

        # slideLayout1 (Title) & slideLayout2 (Content)
        for idx, (layout_name, ltype) in enumerate([("Title", "title"), ("Content", "obj")], 1):
            z.writestr(f"ppt/slideLayouts/slideLayout{idx}.xml", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="{ltype}">
  <p:cSld name="{layout_name}"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>""")
            z.writestr(f"ppt/slideLayouts/_rels/slideLayout{idx}.xml.rels", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>""")

        # Generate individual slide XMLs
        for s_idx, slide_data in enumerate(SLIDES, 1):
            is_title = (s_idx == 1)
            title_text = saxutils.escape(slide_data["title"])
            sub_text = saxutils.escape(slide_data["subtitle"])

            # Top bar visual accent line and background
            slide_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>

      <!-- Decorative top header stripe -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="HeaderStripe"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="120000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="0284C7"/></a:solidFill>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
      </p:sp>
"""
            if is_title:
                # Title Slide Box
                slide_xml += f"""
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="TitleBox"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="1000000" y="1800000"/><a:ext cx="10192000" cy="2200000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:lstStyle/>
          <a:p>
            <a:pPr algn="l"/>
            <a:r>
              <a:rPr lang="en-US" sz="4400" b="1">
                <a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>
              </a:rPr>
              <a:t>{title_text}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Subtitle Box -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="4" name="SubtitleBox"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="1000000" y="4200000"/><a:ext cx="10192000" cy="1800000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:lstStyle/>
"""
                for sub_line in sub_text.split("\n"):
                    slide_xml += f"""
          <a:p>
            <a:pPr algn="l"/>
            <a:r>
              <a:rPr lang="en-US" sz="2000">
                <a:solidFill><a:srgbClr val="475569"/></a:solidFill>
              </a:rPr>
              <a:t>{sub_line}</a:t>
            </a:r>
          </a:p>"""
                slide_xml += """
        </p:txBody>
      </p:sp>"""
            else:
                # Content Slide: Title + Subtitle
                slide_xml += f"""
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="SlideTitle"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="800000" y="400000"/><a:ext cx="10592000" cy="1100000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="3200" b="1">
                <a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>
              </a:rPr>
              <a:t>{title_text}</a:t>
            </a:r>
          </a:p>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1600" i="1">
                <a:solidFill><a:srgbClr val="0284C7"/></a:solidFill>
              </a:rPr>
              <a:t>{sub_text}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Bullet Content Box -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="4" name="BulletList"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="800000" y="1700000"/><a:ext cx="10592000" cy="4600000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:lstStyle/>
"""
                for bullet in slide_data["bullets"]:
                    b_esc = saxutils.escape(bullet)
                    slide_xml += f"""
          <a:p>
            <a:pPr marL="285750" indent="-285750">
              <a:buFont typeface="Arial"/>
              <a:buChar char="•"/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" sz="1900">
                <a:solidFill><a:srgbClr val="334155"/></a:solidFill>
              </a:rPr>
              <a:t>{b_esc}</a:t>
            </a:r>
          </a:p>"""
                slide_xml += """
        </p:txBody>
      </p:sp>"""

            # Slide Footer
            slide_xml += f"""
      <p:sp>
        <p:nvSpPr><p:cNvPr id="5" name="Footer"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="800000" y="6400000"/><a:ext cx="10592000" cy="300000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:noFill/>
          <a:ln><a:noFill/></a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1100">
                <a:solidFill><a:srgbClr val="94A3B8"/></a:solidFill>
              </a:rPr>
              <a:t>SalesSlice Retail Analytics • Slide {s_idx} of {len(SLIDES)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""
            z.writestr(f"ppt/slides/slide{s_idx}.xml", slide_xml)

            # Slide relationships
            layout_target = "../slideLayouts/slideLayout1.xml" if is_title else "../slideLayouts/slideLayout2.xml"
            z.writestr(f"ppt/slides/_rels/slide{s_idx}.xml.rels", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="{layout_target}"/>
</Relationships>""")

    print(f"Successfully generated PowerPoint presentation: {OUTPUT_PPTX}")

if __name__ == "__main__":
    make_pptx()
