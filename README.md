# Prabhu Manikandan Viswanathan — Cyber Security & Threat Hunter Portfolio

[![UK Work Authorization](https://img.shields.io/badge/UK_Right_to_Work-Unrestricted_Authorization-10b981?style=for-the-badge&logo=shield)](https://portfolio.fieldofruin.com)
[![MSc Warwick](https://img.shields.io/badge/Warwick_MSc-Distinction_(NCSC)-d4a03e?style=for-the-badge&logo=academia)](https://portfolio.fieldofruin.com)
[![ISO 27001](https://img.shields.io/badge/BSI-ISO_27001_Lead_Auditor-blue?style=for-the-badge&logo=bsi)](https://portfolio.fieldofruin.com)
[![Enterprise SOC](https://img.shields.io/badge/Enterprise_Role-L2_Threat_Hunter-red?style=for-the-badge&logo=shield)](https://portfolio.fieldofruin.com)

Interactive, high-impact cybersecurity portfolio showcasing **Prabhu Manikandan Viswanathan**: L2 Security Analyst & Primary Threat Hunter at Victoria's Secret (VS&Co), Master of Science in Cyber Security Engineering (Distinction, University of Warwick, NCSC-certified), CheriBSD memory-safety researcher, and Homelab Security Architect.

---

## 🌐 Live Deployments
- **Homelab Production**: [https://portfolio.fieldofruin.com](https://portfolio.fieldofruin.com) / [https://prabhu.fieldofruin.com](https://prabhu.fieldofruin.com)
- **GitHub Pages CDN**: [https://ares-369.github.io](https://ares-369.github.io)
- **Homelab Encyclopedia**: [https://info.fieldofruin.com](https://info.fieldofruin.com)

---

## 🛡️ Core Highlights
- **Victoria's Secret (VS&Co)**: Primary Threat Hunter managing end-to-end incident response, cloud security investigations using **Wiz**, edge perimeter blocking with **Cloudflare**, and hypothesis-driven hunts via **CrowdStrike Falcon** and **Google SecOps**.
- **University of Warwick**: Vulnerability research developing CheriBSD memory corruption and privilege escalation proof-of-concepts in **Lua** and **embedded C**; curated CTI via **MISP** and **OpenCTI**.
- **TIAA GBS India**: Automated third-party supplier risk evaluations (reducing audit cycles from 2 weeks to 20 seconds); 24/7 global SOC log analysis with **Splunk**.
- **Larsen & Toubro EAIC**: ISO 27001 internal audits and organizational training.
- **ProxC Homelab Cyber Range**: 2-Node Proxmox VE 9.2 cluster (33 hosts, 38 services) featuring virtual **OPNsense 24.7** firewall with live **Suricata 7.0.8 IDS**, **Wazuh SIEM XDR** (27 telemetry agents), and an autonomous **Cerberus AI Blue Team SOC**.

---

## 🔄 Bidirectional Continuous Sync
This portfolio is backed by single-source continuous sync:
```bash
./sync.sh "Commit message"
```
It automatically:
1. Commits local changes to Git.
2. Synchronizes to self-hosted Forgejo on CT 122 (`git.fieldofruin.com`).
3. Deploys to CT 120 production runtime (`portfolio.fieldofruin.com` & `prabhu.fieldofruin.com`).
4. Pushes upstream to GitHub (`ares-369.github.io` / `github.com/ares-369`).
