/* =============================================================================
   PRABHU MANIKANDAN VISWANATHAN — PORTFOLIO CLIENT LOGIC
   Interactive HUD, Live UTC Clock, Threat Hunting Terminal, Copy Engine
   ============================================================================= */

// 1. Live UTC Clock & Dynamic Year
function updateClock() {
  const now = new Date();
  const hrs = String(now.getUTCHours()).padStart(2, '0');
  const mins = String(now.getUTCMinutes()).padStart(2, '0');
  const secs = String(now.getUTCSeconds()).padStart(2, '0');
  const clkEl = document.getElementById('liveClock');
  if (clkEl) {
    clkEl.textContent = `${hrs}:${mins}:${secs} UTC`;
  }
}
setInterval(updateClock, 1000);
updateClock();

const fYear = document.getElementById('fYear');
if (fYear) fYear.textContent = new Date().getFullYear();

// 2. Mobile Drawer Navigation
const navToggle = document.getElementById('navToggle');
const mobileDrawer = document.getElementById('mobileDrawer');

if (navToggle && mobileDrawer) {
  navToggle.addEventListener('click', () => {
    mobileDrawer.classList.toggle('open');
  });
}

function closeDrawer() {
  if (mobileDrawer) mobileDrawer.classList.remove('open');
}

// 3. Active Nav Highlighting on Scroll
window.addEventListener('scroll', () => {
  const sections = document.querySelectorAll('section[id]');
  const scrollY = window.pageYOffset;

  sections.forEach(sec => {
    const sectionHeight = sec.offsetHeight;
    const sectionTop = sec.offsetTop - 120;
    const sectionId = sec.getAttribute('id');
    const navLink = document.querySelector(`.nav-links a[href*="${sectionId}"]`);

    if (navLink) {
      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLink.classList.add('active');
      } else {
        navLink.classList.remove('active');
      }
    }
  });
});

// 4. Skills Categorization Filter
function filterSkills(cat, btn) {
  const buttons = document.querySelectorAll('.s-filter-btn');
  buttons.forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  const cards = document.querySelectorAll('.skill-card');
  cards.forEach(card => {
    const cardCat = card.getAttribute('data-cat');
    if (cat === 'all' || cardCat === cat) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

// 5. Interactive Threat Hunting Terminal
const termOutput = document.getElementById('termOutput');
const termInput = document.getElementById('termInput');

const COMMANDS = {
  help: [
    "<span class='term-gold'>COMMAND REFERENCE:</span>",
    "  <span class='term-green'>experience</span>    - Enterprise SecOps & research trajectory",
    "  <span class='term-green'>skills</span>        - Technical toolset, frameworks & languages",
    "  <span class='term-green'>case-study</span>    - Active incident response & malware triage breakdown",
    "  <span class='term-green'>cheribsd</span>      - Warwick automotive memory-safety vulnerability research",
    "  <span class='term-green'>homelab</span>       - ProxC 2-node cluster, Suricata IDS & Wazuh SIEM details",
    "  <span class='term-green'>certifications</span>- ISO 27001 Lead Auditor, Black Hat & ISACA scholarships",
    "  <span class='term-green'>contact</span>       - Direct email, LinkedIn, and GitHub links",
    "  <span class='term-green'>clear</span>         - Clear the terminal history",
  ],
  experience: [
    "<span class='term-gold'>[1] VICTORIA'S SECRET (VS&Co)</span> — L2 Security Analyst & Primary Threat Hunter (Dec 2025 – Present)",
    "    • Primary threat hunter executing hypothesis-driven hunts across endpoint, identity, and cloud telemetry.",
    "    • Leveraged CrowdStrike Falcon and Google SecOps to unmask evasive APT TTPs and suspicious persistence.",
    "    • Managed end-to-end IR lifecycle; spearheaded rapid malware indicator triage to block malicious URIs at perimeter before EDR detections fired.",
    "    • Traced cloud attack paths and remediated toxic combinations using Wiz and Cloudflare WAF.",
    "<br><span class='term-gold'>[2] UNIVERSITY OF WARWICK</span> — Research Assistant (ResAuto & Cyber Observatory) (Sep 2024 – Mar 2025)",
    "    • Built CheriBSD memory-safety vulnerability PoCs in Lua and embedded C for automotive systems.",
    "    • Analyzed critical infrastructure exploits using MISP and OpenCTI.",
    "<br><span class='term-gold'>[3] TIAA GBS INDIA</span> — Cyber Security Intern (Feb 2023 – Apr 2023)",
    "    • Automated supplier risk assessments (slashing evaluation time from 2 weeks to 20 seconds).",
    "    • Analyzed enterprise logs using Splunk; evaluated posture with CMMI framework.",
    "<br><span class='term-gold'>[4] LARSEN & TOUBRO EAIC</span> — Project Trainee (ISMS) (Jul 2022 – Aug 2022)",
    "    • Executed ISO 27001 internal audits; remediated non-conformities; trained 100+ personnel.",
  ],
  skills: [
    "<span class='term-gold'>CORE CYBER DEFENSE COMPETENCIES:</span>",
    "  • <span class='term-cyan'>Threat Hunting & IR:</span> CrowdStrike Falcon (EDR, RTR, LogScale), Google SecOps, Splunk, Wazuh SIEM",
    "  • <span class='term-cyan'>Cloud & Perimeter:</span> Wiz Cloud Security, Cloudflare WAF, Varonis DLP, Axonius, Cequence, Wallarm",
    "  • <span class='term-cyan'>Threat Intelligence:</span> Google Threat Intelligence, MISP, OpenCTI, MITRE ATT&CK",
    "  • <span class='term-cyan'>Systems & Security Research:</span> CheriBSD (Memory Safety), Linux, Windows, Embedded C, Lua",
    "  • <span class='term-cyan'>SecOps Automation:</span> Python, Bash, PowerShell, REST API Orchestration",
    "  • <span class='term-cyan'>Governance & Frameworks:</span> ISO 27001 (Lead Auditor certified), NIST CSF, NIS Directive, CMMI",
  ],
  'case-study': [
    "<span class='term-gold'>CASE STUDY: Rapid Malware Indicator Triage & Edge Blocking</span>",
    "  <span class='term-cyan'>Scenario:</span> Emerging zero-day phishing campaign delivering a weaponized payload with unclassified C2 callbacks.",
    "  <span class='term-cyan'>Investigation:</span> Extracted memory strings and process ancestry; recovered the stage-2 payload URI from obfuscated PowerShell scripts.",
    "  <span class='term-cyan'>Immediate Containment:</span> Pushed edge DNS and perimeter proxy blocks at the Cloudflare edge gateway prior to automated CrowdStrike EDR signatures firing.",
    "  <span class='term-cyan'>Result:</span> Zero host compromises across the enterprise fleet; converted indicators into proactive telemetry hunt rules.",
  ],
  cheribsd: [
    "<span class='term-gold'>RESEARCH: CheriBSD Memory Safety for Automotive Embedded Systems</span>",
    "  <span class='term-cyan'>Institution:</span> The University of Warwick (Cyber Security Centre)",
    "  <span class='term-cyan'>Objective:</span> Evaluate hardware capability-based compartmentalization against memory corruption attacks.",
    "  <span class='term-cyan'>Methodology:</span> Developed proof-of-concept exploits in Lua and embedded C simulating stack buffer overflows and pointer corruption.",
    "  <span class='term-cyan'>Outcome:</span> Proved CheriBSD hardware capabilities successfully trap and abort out-of-bounds pointer writes without crashing whole systems.",
  ],
  homelab: [
    "<span class='term-gold'>PROXC CYBER RANGE ARCHITECTURE:</span>",
    "  • <span class='term-green'>Nodes:</span> 2 Physical Nodes (Lenovo IdeaPad + ASUS ROG Strix), 33 hosts/containers, 38 services",
    "  • <span class='term-green'>Perimeter Firewall:</span> OPNsense 24.7 VM with Suricata 7.0.8 IDS on PPPoE WAN + Gigabit LAN",
    "  • <span class='term-green'>SIEM & Telemetry:</span> Wazuh SIEM Manager (CT 106) with 27 active endpoint & network agents",
    "  • <span class='term-green'>Deception & Purple Team:</span> Cerberus AI SOC + CT 206 Honeypot (8 trap ports, Level 12 SIEM alerts)",
    "  • <span class='term-green'>Live Encyclopedia:</span> View full topology at https://info.fieldofruin.com",
  ],
  certifications: [
    "<span class='term-gold'>CREDENTIALS & HONORS:</span>",
    "  • <span class='term-cyan'>ISO/IEC 27001 ISMS Lead Auditor</span> — British Standards Institution (BSI)",
    "  • <span class='term-cyan'>MSc in Cyber Security Engineering (Distinction)</span> — The University of Warwick (NCSC Certified)",
    "  • <span class='term-cyan'>Black Hat USA 2024 Scholar</span> — Awarded competitive student conference scholarship",
    "  • <span class='term-cyan'>ISACA UK Digital Scholarship 2024</span> — International digital scholarship recipient",
    "  • <span class='term-cyan'>B.Tech (Hons.) Cyber Security & Forensics</span> — UPES",
    "  • <span class='term-cyan'>UK Graduate Visa</span> — Active and fully authorized to work in the UK through Feb 2027",
  ],
  contact: [
    "<span class='term-gold'>DIRECT COMMUNICATIONS:</span>",
    "  • <span class='term-cyan'>Email:</span> prabhumanikandan369@gmail.com",
    "  • <span class='term-cyan'>LinkedIn:</span> https://linkedin.com/in/prabhu-manikandan",
    "  • <span class='term-cyan'>GitHub:</span> https://github.com/ares-369",
    "  • <span class='term-cyan'>Official CV:</span> Download available directly via top navigation button",
  ],
};

function execTerm(cmdRaw) {
  const cmd = (cmdRaw || '').trim().toLowerCase();
  if (!cmd) return;

  if (cmd === 'clear') {
    termOutput.innerHTML = '';
    return;
  }

  const outBlock = document.createElement('div');
  outBlock.style.marginBottom = '14px';

  let html = `<div style="color:var(--accent-gold);margin-bottom:4px;">visitor@hunter-cli:~$ <span style="color:#fff">${cmd}</span></div>`;

  if (COMMANDS[cmd]) {
    html += COMMANDS[cmd].join('<br>');
  } else {
    html += `<span class='term-red'>Command not recognized: '${cmd}'. Type 'help' for available commands.</span>`;
  }

  outBlock.innerHTML = html;
  termOutput.appendChild(outBlock);
  termOutput.scrollTop = termOutput.scrollHeight;

  if (termInput) termInput.value = '';
}

if (termInput) {
  termInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      execTerm(termInput.value);
    }
  });
}

// 6. Copy to Clipboard Utility
function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const toast = document.getElementById('toastPopup');
    if (toast) {
      toast.classList.add('show');
      setTimeout(() => {
        toast.classList.remove('show');
      }, 2200);
    }
    if (btn) {
      const orig = btn.innerHTML;
      btn.innerHTML = '<i class="mdi mdi-check"></i>';
      setTimeout(() => {
        btn.innerHTML = orig;
      }, 1500);
    }
  }).catch(err => {
    console.error('Clipboard copy failed:', err);
  });
}
