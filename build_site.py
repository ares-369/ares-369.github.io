#!/usr/bin/env python3
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "portfolio_data.json")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

def build():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    with open(INDEX_FILE, "r") as f:
        html = f.read()

    p = data.get("personal", {})
    st = data.get("stats", {})

    # Replace Hero & Personal Data
    html = re.sub(r'<span class="brand-title">[^<]+</span>', f'<span class="brand-title">{p.get("fullName", "")}</span>', html)
    html = re.sub(r'<span class="brand-sub">[^<]+</span>', f'<span class="brand-sub">{p.get("headline", "").upper()}</span>', html)
    html = re.sub(r'<span class="pill-text">[^<]+</span>', f'<span class="pill-text">{p.get("navTelemetry", "SOC OPERATIONS // THREAT HUNTING")}</span>', html)
    html = re.sub(r'<span class="status-badge"><i class="mdi mdi-shield-check"></i> [^<]+</span>', f'<span class="status-badge"><i class="mdi mdi-shield-check"></i> {p.get("statusBadge", "")}</span>', html)
    html = re.sub(r'<span class="status-location"><i class="mdi mdi-map-marker-radius"></i> [^<]+</span>', f'<span class="status-location"><i class="mdi mdi-map-marker-radius"></i> {p.get("location", "UNITED KINGDOM")}</span>', html)
    
    # Hero Name
    name_parts = p.get("fullName", "PRABHU MANIKANDAN VISWANATHAN").split()
    if len(name_parts) >= 2:
        first = " ".join(name_parts[:-1])
        last = name_parts[-1]
        name_html = f'{first} <span class="gold-gradient">{last}</span>'
    else:
        name_html = f'<span class="gold-gradient">{p.get("fullName", "")}</span>'
    html = re.sub(r'<h1 class="hero-name">\s*[\s\S]*?\s*</h1>', f'<h1 class="hero-name">\n            {name_html}\n          </h1>', html)

    # Hero Headline
    html = re.sub(r'<p class="hero-headline">\s*[\s\S]*?\s*</p>', f'<p class="hero-headline">\n            {p.get("summaryLead", "")}\n          </p>', html)

    # Summary Section
    html = re.sub(r'<p class="summary-lead">\s*[\s\S]*?\s*</p>', f'<p class="summary-lead">\n            {p.get("summaryLead", "")}\n          </p>', html)
    html = re.sub(r'<p class="summary-body">\s*[\s\S]*?\s*</p>', f'<p class="summary-body">\n            {p.get("summaryBody", "")}\n          </p>', html)

    # Build Experience Timeline HTML
    exp_html = ""
    for exp in data.get("experience", []):
        curr_cls = " current" if exp.get("isCurrent") else ""
        badge_cls = " current" if exp.get("isCurrent") else ""
        icon = "mdi-shield-star" if exp.get("isCurrent") else "mdi-briefcase-outline"
        bullets_li = "".join(f"<li>{b}</li>" for b in exp.get("bullets", []))
        tags_sp = "".join(f"<span>{t}</span>" for t in exp.get("tags", []))
        exp_html += f"""
          <div class="timeline-item{curr_cls}">
            <div class="timeline-marker"><i class="mdi {icon}"></i></div>
            <div class="timeline-content">
              <div class="timeline-header">
                <div>
                  <span class="role-badge{badge_cls}">{exp.get("badge", "")}</span>
                  <h3 class="role-title">{exp.get("role", "")}</h3>
                  <div class="company-name">{exp.get("company", "")}</div>
                </div>
                <div class="role-meta">
                  <span class="duration"><i class="mdi mdi-calendar"></i> {exp.get("duration", "")}</span>
                  <span class="location"><i class="mdi mdi-map-marker"></i> {exp.get("location", "")}</span>
                </div>
              </div>
              <ul class="role-bullets">
                {bullets_li}
              </ul>
              <div class="role-tags">
                {tags_sp}
              </div>
            </div>
          </div>"""

    html = re.sub(r'<div class="timeline">\s*[\s\S]*?\s*</div>\s*</div>\s*</section>\s*<!-- SECTION: SKILLS', f'<div class="timeline">{exp_html}\n        </div>\n      </div>\n    </section>\n\n    <!-- SECTION: SKILLS', html)

    # Build Credentials Grid HTML
    cred_html = ""
    for cred in data.get("credentials", []):
        hl_cls = " highlight" if cred.get("highlight") else ""
        cred_html += f"""
          <div class="cred-card{hl_cls}">
            <div class="cred-badge-icon"><i class="mdi {cred.get("icon", "mdi-certificate")}"></i></div>
            <div class="cred-tag">{cred.get("tag", "")}</div>
            <h3>{cred.get("title", "")}</h3>
            <div class="cred-inst">{cred.get("inst", "")}</div>
            <div class="cred-year"><i class="mdi mdi-check-decagram"></i> {cred.get("year", "")}</div>
            <p>{cred.get("desc", "")}</p>
          </div>"""

    html = re.sub(r'<div class="cred-grid">\s*[\s\S]*?\s*</div>\s*</div>\s*</section>\s*<!-- SECTION: CONTACT', f'<div class="cred-grid">{cred_html}\n        </div>\n      </div>\n    </section>\n\n    <!-- SECTION: CONTACT', html)

    # Write back
    with open(INDEX_FILE, "w") as f:
        f.write(html)

    print("Rebuilt index.html from portfolio_data.json successfully.")

if __name__ == "__main__":
    build()
