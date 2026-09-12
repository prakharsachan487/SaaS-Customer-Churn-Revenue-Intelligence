// ==============================================================================
// RETENTION IQ - Interactive Logic & Visualizations
// ==============================================================================

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  initSparklines();
  initHeroChart();
  initDonutChart();
  initRiskPageCharts();
  initCohortPage();
  initSimulator();
});

// 1. PAGE NAVIGATION
function initNavigation() {
  const navLinks = document.querySelectorAll(".nav-link");
  const pages = document.querySelectorAll(".tab-page");
  const pageTitle = document.getElementById("page-title");

  const titles = {
    page1: "Executive Dashboard",
    page2: "Churn Drivers & Early Warning Risk Radar",
    page3: "Cohort Retention & Lifetime Value (LTV)"
  };

  navLinks.forEach(link => {
    link.addEventListener("click", () => {
      navLinks.forEach(l => l.classList.remove("active"));
      pages.forEach(p => p.classList.remove("active-tab"));

      link.classList.add("active");
      const target = link.getAttribute("data-page");
      document.getElementById(target).classList.add("active-tab");
      pageTitle.innerText = titles[target];
    });
  });
}

// 2. MINI SPARKLINES FOR KPI CARDS (MATCHING REFERENCE IMAGE)
function createSparkline(canvasId, dataPoints, color) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: dataPoints.map((_, i) => i),
      datasets: [{
        data: dataPoints,
        borderColor: color,
        borderWidth: 2,
        pointRadius: 0,
        fill: false,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      scales: {
        x: { display: false },
        y: { display: false }
      }
    }
  });
}

function initSparklines() {
  createSparkline("spark-mrr", [1.1, 1.18, 1.25, 1.35, 1.42, 1.51, 1.58], "#3b82f6");
  createSparkline("spark-subs", [4200, 4600, 5100, 5600, 6000, 6300, 6532], "#10b981");
  createSparkline("spark-churn", [54, 52, 50, 49, 48.5, 48.0, 47.74], "#ef4444");
  createSparkline("spark-ltv", [1420, 1490, 1560, 1610, 1680, 1714], "#8b5cf6");
}

// 3. HERO REVENUE GROWTH CHART (WAVY CURVED GRADIENT)
function initHeroChart() {
  const ctx = document.getElementById("chart-hero-revenue").getContext("2d");
  
  const gradient = ctx.createLinearGradient(0, 0, 0, 240);
  gradient.addColorStop(0, "rgba(59, 130, 246, 0.28)");
  gradient.addColorStop(1, "rgba(59, 130, 246, 0.0)");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [
        {
          label: "Active MRR ($k)",
          data: [650, 740, 890, 820, 1050, 1280, 1220, 1380, 1450, 1510, 1550, 1584],
          borderColor: "#3b82f6",
          borderWidth: 2.5,
          backgroundColor: gradient,
          fill: true,
          tension: 0.45,
          pointBackgroundColor: "#ffffff",
          pointBorderColor: "#3b82f6",
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        },
        {
          label: "Lost Churn MRR ($k)",
          data: [45, 60, 80, 105, 135, 170, 195, 220, 245, 265, 280, 298],
          borderColor: "#94a3b8",
          borderWidth: 1.5,
          borderDash: [4, 4],
          pointRadius: 0,
          fill: false,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          align: "end",
          labels: { boxWidth: 10, font: { family: "Plus Jakarta Sans", size: 11 }, color: "#64748b" }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { family: "Plus Jakarta Sans", size: 11 }, color: "#94a3b8" }
        },
        y: {
          grid: { color: "#f1f5f9" },
          ticks: {
            font: { family: "Plus Jakarta Sans", size: 11 },
            color: "#94a3b8",
            callback: v => "$" + v + "k"
          }
        }
      }
    }
  });
}

// 4. DONUT CHART (PLAN TIERS)
function initDonutChart() {
  const ctx = document.getElementById("chart-plan-donut").getContext("2d");
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Starter", "Professional", "Enterprise", "Custom"],
      datasets: [{
        data: [285, 495, 520, 284],
        backgroundColor: ["#93c5fd", "#3b82f6", "#1e40af", "#64748b"],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "68%",
      plugins: {
        legend: {
          position: "bottom",
          labels: { boxWidth: 10, font: { family: "Plus Jakarta Sans", size: 10 }, color: "#64748b" }
        }
      }
    }
  });
}

// 5. TAB 2 CHARTS (CHURN & RISK RADAR)
function initRiskPageCharts() {
  // Churn Reasons
  const ctxReasons = document.getElementById("chart-churn-reasons").getContext("2d");
  new Chart(ctxReasons, {
    type: "bar",
    indexAxis: "y",
    data: {
      labels: ["Missing Features", "High Price / Budget", "Poor Support Exp", "Competitor Switch", "Difficult Onboarding", "Business Closed"],
      datasets: [{
        label: "Lost ARR ($k)",
        data: [1252, 1184, 942, 815, 620, 310],
        backgroundColor: ["#ef4444", "#f87171", "#fb923c", "#fbbf24", "#94a3b8", "#cbd5e1"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: "#f1f5f9" }, ticks: { color: "#94a3b8", callback: v => "$" + v + "k" } },
        y: { grid: { display: false }, ticks: { color: "#64748b", font: { size: 11 } } }
      }
    }
  });

  // ML Feature Weights
  const ctxML = document.getElementById("chart-ml-importance").getContext("2d");
  new Chart(ctxML, {
    type: "bar",
    data: {
      labels: ["Annual Contract", "Active Days", "CSAT Score", "Escalated Tickets", "Enterprise Plan", "Starter Plan"],
      datasets: [{
        data: [-0.47, -0.36, -0.33, 0.29, -0.23, 0.19],
        backgroundColor: [-0.47, -0.36, -0.33, 0.29, -0.23, 0.19].map(v => v < 0 ? "#10b981" : "#ef4444"),
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#64748b", font: { size: 10 } } },
        y: { grid: { color: "#f1f5f9" }, ticks: { color: "#94a3b8" } }
      }
    }
  });

  // Table population
  const riskTbody = document.getElementById("risk-tbody");
  const riskAccounts = [
    { id: "CUST-110339", seg: "Enterprise", plan: "Enterprise", cycle: "Annual", arr: "$5,089.80", score: 40.3, days: 15, tickets: 4 },
    { id: "CUST-111040", seg: "Enterprise", plan: "Enterprise", cycle: "Annual", arr: "$5,089.80", score: 44.4, days: 19, tickets: 5 },
    { id: "CUST-100022", seg: "SMB", plan: "Professional", cycle: "Monthly", arr: "$1,788.00", score: 17.7, days: 14, tickets: 4 },
    { id: "CUST-100294", seg: "Mid-Market", plan: "Professional", cycle: "Monthly", arr: "$1,788.00", score: 28.5, days: 8, tickets: 3 },
    { id: "CUST-104910", seg: "Enterprise", plan: "Custom Enterprise", cycle: "Annual", arr: "$12,229.80", score: 42.1, days: 12, tickets: 6 }
  ];

  riskTbody.innerHTML = riskAccounts.map(a => `
    <tr>
      <td><strong>${a.id}</strong></td>
      <td>${a.seg}</td>
      <td>${a.plan}</td>
      <td>${a.cycle}</td>
      <td><strong>${a.arr}</strong></td>
      <td><span class="status-pill status-critical">${a.score} / 100</span></td>
      <td>${a.days} days</td>
      <td>${a.tickets}</td>
      <td><button class="btn-table-action" onclick="alert('Priority task assigned to CSM for ${a.id}')">Dispatch CSM</button></td>
    </tr>
  `).join("");
}

// 6. TAB 3 (COHORTS & LTV)
function initCohortPage() {
  const table = document.getElementById("cohort-matrix");
  const cohorts = ["2024-01", "2024-03", "2024-05", "2024-07", "2024-09", "2024-11", "2025-01", "2025-03", "2025-05"];
  
  let html = `<thead><tr><th>Cohort</th><th>Starting</th>`;
  for (let i = 0; i <= 12; i++) {
    html += `<th>M${i}</th>`;
  }
  html += `</tr></thead><tbody>`;

  cohorts.forEach(c => {
    html += `<tr><td><strong>${c}</strong></td><td>520</td>`;
    for (let m = 0; m <= 12; m++) {
      let pct = Math.max(25, Math.round(100 - (m * 5.2) + (Math.sin(m) * 2.5)));
      let bg = pct > 75 ? "#ecfdf5" : (pct > 50 ? "#fffbeb" : "#fef2f2");
      let textCol = pct > 75 ? "#059669" : (pct > 50 ? "#d97706" : "#dc2626");
      html += `<td class="cohort-num" style="background:${bg}; color:${textCol};">${pct}%</td>`;
    }
    html += `</tr>`;
  });
  html += `</tbody>`;
  table.innerHTML = html;

  // Contract Curves Chart
  const ctxContract = document.getElementById("chart-contract-curves").getContext("2d");
  new Chart(ctxContract, {
    type: "line",
    data: {
      labels: ["M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12"],
      datasets: [
        {
          label: "Annual Contract Retention (%)",
          data: [100, 98, 96, 94, 92, 91, 89, 88, 86, 85, 84, 83, 82],
          borderColor: "#10b981",
          borderWidth: 2,
          pointRadius: 0,
          fill: false,
          tension: 0.3
        },
        {
          label: "Monthly Contract Retention (%)",
          data: [100, 78, 65, 56, 50, 46, 44, 42, 40, 39, 38, 38, 38],
          borderColor: "#ef4444",
          borderWidth: 2,
          pointRadius: 0,
          fill: false,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "top", labels: { boxWidth: 10, color: "#64748b" } } },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#94a3b8" } },
        y: { grid: { color: "#f1f5f9" }, ticks: { color: "#94a3b8", callback: v => v + "%" } }
      }
    }
  });

  // Channel LTV Chart
  const ctxLTV = document.getElementById("chart-channel-ltv").getContext("2d");
  new Chart(ctxLTV, {
    type: "bar",
    data: {
      labels: ["Referral", "Outbound", "Organic", "Direct", "Email", "Paid Ads", "Social"],
      datasets: [{
        label: "Avg LTV ($)",
        data: [2420, 2180, 1950, 1720, 1480, 1180, 980],
        backgroundColor: "#3b82f6",
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#64748b", font: { size: 10 } } },
        y: { grid: { color: "#f1f5f9" }, ticks: { color: "#94a3b8", callback: v => "$" + v } }
      }
    }
  });
}

// 7. WHAT-IF RETENTION SIMULATOR
function initSimulator() {
  const slider = document.getElementById("retention-slider");
  const label = document.getElementById("sim-slider-label");
  const display = document.getElementById("sim-recovered-arr");
  const baseLossARR = 1993215;

  slider.addEventListener("input", (e) => {
    const val = parseInt(e.target.value);
    label.innerText = val + "%";
    const recovered = Math.round(baseLossARR * (val / 100));
    display.innerText = "$" + recovered.toLocaleString();
  });
}
