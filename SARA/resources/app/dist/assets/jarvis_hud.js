// SARA AI 2.5 Pro — JARVIS Intelligence HUD, Companion Dashboard & Telemetry
(function() {
  // =========================================================================
  // 1. COMPANION DASHBOARD (Greeting, Live Clock, Quick Actions & Telemetry)
  // Matches Baseline Reference Architecture & Aesthetic
  // =========================================================================
  function createCompanionDashboard() {
    if (document.getElementById('sara-left-panel')) return;

    // 1. Create Left Panel (Greeting, Live Clock, Quick Actions Dock)
    const leftPanel = document.createElement('div');
    leftPanel.id = 'sara-left-panel';
    leftPanel.className = 'sara-side-widget';
    leftPanel.innerHTML = `
      <!-- Greeting & Digital Clock Card -->
      <div class="sara-glass-card sara-greeting-card">
        <div class="sara-greeting-header">
          <div class="sara-lotus-badge">
            <img src="/assets/sara_logo.png" alt="SARA">
          </div>
          <div class="sara-greeting-text">
            <h4 id="sara-greeting-title">Good Evening, Pasha Jan</h4>
            <p>Let's make something amazing today! ✨</p>
          </div>
        </div>
        <div class="sara-clock-display">
          <div>
            <span class="sara-time-digits" id="sara-live-clock">08:42</span>
            <span class="sara-time-ampm" id="sara-live-ampm">PM</span>
          </div>
          <div class="sara-date-str" id="sara-live-date">Oct 29, 2026 • Thursday</div>
        </div>
      </div>

      <!-- Quick Actions Vertical Dock -->
      <div class="sara-glass-card sara-dock-card">
        <button class="sara-dock-btn" onclick="window.saraTriggerAction('chat')">
          <div class="sara-dock-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          </div>
          <div class="sara-dock-info">
            <span class="sara-dock-title">Neural Copilot</span>
            <span class="sara-dock-sub">Chat & Get Help</span>
          </div>
        </button>

        <button class="sara-dock-btn" onclick="window.saraTriggerAction('research')">
          <div class="sara-dock-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <div class="sara-dock-info">
            <span class="sara-dock-title">Research</span>
            <span class="sara-dock-sub">Live Web Search</span>
          </div>
        </button>

        <button class="sara-dock-btn" onclick="window.saraTriggerAction('code')">
          <div class="sara-dock-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          </div>
          <div class="sara-dock-info">
            <span class="sara-dock-title">Code</span>
            <span class="sara-dock-sub">Build & Create</span>
          </div>
        </button>

        <button class="sara-dock-btn" onclick="window.saraTriggerAction('files')">
          <div class="sara-dock-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/></svg>
          </div>
          <div class="sara-dock-info">
            <span class="sara-dock-title">Files</span>
            <span class="sara-dock-sub">Manage Your Files</span>
          </div>
        </button>

        <button class="sara-dock-btn" onclick="window.saraTriggerAction('whatsapp')">
          <div class="sara-dock-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          </div>
          <div class="sara-dock-info">
            <span class="sara-dock-title">WhatsApp</span>
            <span class="sara-dock-sub">Messages & Voice</span>
          </div>
        </button>

        <button class="sara-dock-btn" onclick="window.saraTriggerAction('system')">
          <div class="sara-dock-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
          </div>
          <div class="sara-dock-info">
            <span class="sara-dock-title">System</span>
            <span class="sara-dock-sub">Control & Automate</span>
          </div>
        </button>
      </div>
    `;
    document.body.appendChild(leftPanel);

    // 2. Create Right Panel (System Status & Recent Activity)
    const rightPanel = document.createElement('div');
    rightPanel.id = 'sara-right-panel';
    rightPanel.className = 'sara-side-widget';
    rightPanel.innerHTML = `
      <!-- System Status Card -->
      <div class="sara-glass-card sara-status-card">
        <div class="sara-panel-header">
          <span>System Status</span>
        </div>
        <div class="sara-status-row">
          <div class="sara-status-row-left">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>
            <span>Memory</span>
          </div>
          <span class="sara-status-val" style="color:#75D9E8;">• Active</span>
        </div>
        <div class="sara-status-row">
          <div class="sara-status-row-left">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M15 9h.01"/><path d="M9 9h.01"/><path d="M9 15h.01"/><path d="M15 15h.01"/></svg>
            <span>CPU Usage</span>
          </div>
          <span class="sara-status-val" id="sara-val-cpu">• 12%</span>
        </div>
        <div class="sara-status-row">
          <div class="sara-status-row-left">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
            <span>RAM Usage</span>
          </div>
          <span class="sara-status-val" id="sara-val-ram">• 28%</span>
        </div>
        <div class="sara-status-row">
          <div class="sara-status-row-left">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>
            <span>Disk Usage</span>
          </div>
          <span class="sara-status-val">• 42%</span>
        </div>
        <div class="sara-status-row">
          <div class="sara-status-row-left">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 13a10 10 0 0 1 14 0"/><path d="M8.5 16.5a5 5 0 0 1 7 0"/><line x1="12" x2="12.01" y1="20" y2="20"/></svg>
            <span>Network</span>
          </div>
          <span class="sara-status-val" style="color:#75D9E8;">• Connected</span>
        </div>
      </div>

      <!-- Recent Activity Card -->
      <div class="sara-glass-card sara-activity-card">
        <div class="sara-panel-header">
          <span>Recent Activity</span>
        </div>
        <div class="sara-activity-item">
          <div class="sara-activity-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <div class="sara-activity-text">
            <span class="sara-activity-title">Research completed</span>
            <span class="sara-activity-sub">AI models 2026</span>
          </div>
          <span class="sara-activity-time">2m ago</span>
        </div>

        <div class="sara-activity-item">
          <div class="sara-activity-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
          </div>
          <div class="sara-activity-text">
            <span class="sara-activity-title">Project opened</span>
            <span class="sara-activity-sub">MUBAR Horology</span>
          </div>
          <span class="sara-activity-time">4m ago</span>
        </div>

        <div class="sara-activity-item">
          <div class="sara-activity-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          </div>
          <div class="sara-activity-text">
            <span class="sara-activity-title">WhatsApp connected</span>
            <span class="sara-activity-sub">Ready to chat</span>
          </div>
          <span class="sara-activity-time">7m ago</span>
        </div>

        <div class="sara-activity-item">
          <div class="sara-activity-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4"/><path d="m16.2 7.8 2.9-2.9"/><path d="M18 12h4"/><path d="m16.2 16.2 2.9 2.9"/><path d="M12 18v4"/><path d="m4.9 19.1 2.9-2.9"/><path d="M2 12h4"/><path d="m4.9 4.9 2.9 2.9"/></svg>
          </div>
          <div class="sara-activity-text">
            <span class="sara-activity-title">Background task</span>
            <span class="sara-activity-sub">Monitoring system</span>
          </div>
          <span class="sara-activity-time">12m ago</span>
        </div>
      </div>
    `;
    document.body.appendChild(rightPanel);

    // 3. Ambient Footers
    const footerLeft = document.createElement('div');
    footerLeft.id = 'sara-footer-left';
    footerLeft.innerHTML = `
      <div class="sara-quote-serif">Always with you</div>
      <div>SARA AI 2.5 Pro 💖</div>
    `;
    document.body.appendChild(footerLeft);

    const footerRight = document.createElement('div');
    footerRight.id = 'sara-footer-right';
    footerRight.innerHTML = `
      <div class="sara-quote-serif">Better ideas<br/>Bigger dreams<br/>Together... 💙</div>
    `;
    document.body.appendChild(footerRight);

    // 4. Live Clock & Calendar Engine
    function updateClock() {
      const now = new Date();
      let hours = now.getHours();
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12 || 12;

      const clockEl = document.getElementById('sara-live-clock');
      const ampmEl = document.getElementById('sara-live-ampm');
      if (clockEl) clockEl.textContent = `${String(hours).padStart(2, '0')}:${minutes}`;
      if (ampmEl) ampmEl.textContent = ampm;

      const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
      const dateEl = document.getElementById('sara-live-date');
      if (dateEl) {
        dateEl.textContent = `${months[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()} • ${days[now.getDay()]}`;
      }

      // Dynamic Greeting
      const titleEl = document.getElementById('sara-greeting-title');
      if (titleEl) {
        const rawH = now.getHours();
        const greeting = rawH < 12 ? 'Good Morning, Pasha Jan' : rawH < 18 ? 'Good Afternoon, Pasha Jan' : 'Good Evening, Pasha Jan';
        titleEl.textContent = greeting;
      }
    }

    updateClock();
    setInterval(updateClock, 1000);

    // Simulated Telemetry Jitter for Live Feel
    setInterval(() => {
      const cpuEl = document.getElementById('sara-val-cpu');
      const ramEl = document.getElementById('sara-val-ram');
      if (cpuEl) cpuEl.textContent = `• ${Math.floor(10 + Math.random() * 8)}%`;
      if (ramEl) ramEl.textContent = `• ${Math.floor(27 + Math.random() * 4)}%`;
    }, 4000);
  }

  // Quick Action Handler - sets input value cleanly without disrupting form
  window.saraTriggerAction = function(action) {
    const input = document.querySelector('input[aria-label="Message SARA"]');
    if (!input) return;

    if (action === 'chat') {
      input.focus();
    } else if (action === 'research') {
      input.value = "Research recent developments in AI";
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.focus();
    } else if (action === 'code') {
      input.value = "Help me optimize my code architecture";
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.focus();
    } else if (action === 'files') {
      input.value = "Check my recent files on Desktop";
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.focus();
    } else if (action === 'whatsapp') {
      input.value = "Open WhatsApp and check messages";
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.focus();
    } else if (action === 'system') {
      window.toggleTaskDashboard && window.toggleTaskDashboard();
    }
  };

  // =========================================================================
  // 2. JARVIS HUD & INTELLIGENCE OVERLAY
  // =========================================================================
  function createHudElement() {
    if (document.getElementById('jarvis-hud-overlay')) return;

    const overlay = document.createElement('div');
    overlay.id = 'jarvis-hud-overlay';
    overlay.className = 'hidden';
    overlay.innerHTML = `
      <div class="jarvis-header">
        <div class="jarvis-badge">
          <div class="jarvis-beacon"></div>
          <span>JARVIS Intelligence // Live Extract</span>
        </div>
        <button id="jarvis-dismiss-btn" class="jarvis-close-btn" title="Gayab karo (Esc / Click)">✕ GAYAB KARO</button>
      </div>
      <div class="jarvis-body">
        <div id="jarvis-hud-title" class="jarvis-title">⚡ INTELLIGENCE REPORT</div>
        <ul id="jarvis-hud-list" class="jarvis-highlights-list"></ul>
        <div id="jarvis-hud-summary" class="jarvis-summary-box"></div>
      </div>
    `;

    document.body.appendChild(overlay);

    const btn = document.getElementById('jarvis-dismiss-btn');
    if (btn) {
      btn.addEventListener('click', () => {
        window.hideJarvisHud();
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        window.hideJarvisHud();
        window.hideTaskDashboard();
      }
    });
  }

  // =========================================================================
  // 3. TASK & PROJECT DASHBOARD MODAL
  // =========================================================================
  function createTaskDashboardElement() {
    if (document.getElementById('sara-task-dashboard-modal')) return;

    const modal = document.createElement('div');
    modal.id = 'sara-task-dashboard-modal';
    modal.className = 'hidden';
    modal.innerHTML = `
      <div class="dash-header">
        <div class="dash-title">📊 SARA 2.5 PRO // TASK & PROJECT DASHBOARD</div>
        <button id="sara-dash-close-btn" class="jarvis-close-btn">✕ CLOSE</button>
      </div>
      <div class="dash-body">
        <div class="dash-card">
          <div class="dash-card-header">
            <span>🚀 ACTIVE WORKSPACE: E:\\sopify</span>
            <span class="dash-score-badge" id="dash-sopify-score">95% HEALTHY</span>
          </div>
          <div class="dash-desc" id="dash-sopify-desc">
            Stack: React / Vite Web App (MUBAR Luxury Watch Store)<br/>
            Entry Points: index.html, src/main.jsx, src/App.jsx | Git: Clean
          </div>
          <div class="dash-actions">
            <button class="dash-btn" id="dash-audit-sopify-btn">🔍 Run Health Audit</button>
          </div>
        </div>

        <div class="dash-card">
          <div class="dash-card-header">
            <span>📈 QUANT WORKSPACE: E:\\Trading</span>
            <span class="dash-score-badge" style="background: rgba(16,185,129,0.25); border-color:#10b981; color:#34d399;">100% HEALTHY</span>
          </div>
          <div class="dash-desc">
            Stack: Antigravity AI Quantitative Trading System<br/>
            Skills: trend-and-structure, chart-analyzer, exness-risk-calculator
          </div>
          <div class="dash-actions">
            <button class="dash-btn" id="dash-audit-trading-btn">🔍 Audit Trading System</button>
          </div>
        </div>

        <div class="dash-card">
          <div class="dash-card-header">
            <span>⚡ ANTIGRAVITY ENGINE</span>
            <span class="dash-score-badge" style="background: rgba(0,240,255,0.2); border-color:#00f0ff; color:#38bdf8;">ACTIVE</span>
          </div>
          <div class="dash-desc">
            Task Queue: 0 Pending | Self-Improvement: Anti-Loop Guard Active
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const closeBtn = document.getElementById('sara-dash-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        window.hideTaskDashboard();
      });
    }
  }

  // Public Controllers
  window.showJarvisHud = function(data) {
    createHudElement();
    const overlay = document.getElementById('jarvis-hud-overlay');
    if (!overlay) return;

    const titleEl = document.getElementById('jarvis-hud-title');
    const listEl = document.getElementById('jarvis-hud-list');
    const sumEl = document.getElementById('jarvis-hud-summary');

    if (!data) data = {};
    const title = data.title || data.topic || data.query || 'JARVIS LIVE INTELLIGENCE';
    if (titleEl) {
      titleEl.textContent = '⚡ ' + String(title).toUpperCase();
    }

    if (listEl) {
      listEl.innerHTML = '';
      const points = Array.isArray(data.highlights) ? data.highlights : (Array.isArray(data.points) ? data.points : []);
      if (points.length === 0 && data.summary) {
        points.push(data.summary);
      }

      points.forEach((pt, idx) => {
        const li = document.createElement('li');
        li.className = 'jarvis-highlight-item';
        li.innerHTML = `<strong>#${idx + 1}</strong>: ${pt}`;
        listEl.appendChild(li);
      });
    }

    if (sumEl) {
      if (data.summary) {
        sumEl.style.display = 'block';
        sumEl.innerHTML = `<strong>Executive Summary:</strong> ${data.summary}`;
      } else {
        sumEl.style.display = 'none';
      }
    }

    overlay.classList.remove('hidden');
  };

  window.hideJarvisHud = function() {
    const overlay = document.getElementById('jarvis-hud-overlay');
    if (overlay) overlay.classList.add('hidden');
  };

  window.toggleTaskDashboard = function() {
    createTaskDashboardElement();
    const modal = document.getElementById('sara-task-dashboard-modal');
    if (modal) modal.classList.toggle('hidden');
  };

  window.hideTaskDashboard = function() {
    const modal = document.getElementById('sara-task-dashboard-modal');
    if (modal) modal.classList.add('hidden');
  };

  window.dismissJarvisHud = window.hideJarvisHud;

  // Background initialization
  // Background initialization & Ultra-Robust Modal/Settings Observer
  function setupModalObserver() {
    function checkAndToggle() {
      const rightPanel = document.getElementById('sara-right-panel');
      if (!rightPanel) return;
      const bodyHtml = document.body.innerHTML || '';
      const bodyText = document.body.textContent || '';
      const isSettingsOpen = bodyHtml.includes('SARA Configuration') || 
                             bodyHtml.includes('System settings &amp; preferences') || 
                             bodyHtml.includes('System settings & preferences') ||
                             bodyText.includes('SARA Configuration') ||
                             document.body.classList.contains('sara-settings-open') ||
                             document.body.classList.contains('sara-modal-open');
      if (isSettingsOpen) {
        if (!document.body.classList.contains('sara-settings-open')) {
          document.body.classList.add('sara-settings-open');
        }
        rightPanel.style.setProperty('display', 'none', 'important');
        rightPanel.style.setProperty('opacity', '0', 'important');
        rightPanel.style.setProperty('visibility', 'hidden', 'important');
        rightPanel.style.setProperty('pointer-events', 'none', 'important');
        rightPanel.style.setProperty('z-index', '-1', 'important');
      } else {
        if (document.body.classList.contains('sara-settings-open')) {
          document.body.classList.remove('sara-settings-open');
        }
        rightPanel.style.removeProperty('display');
        rightPanel.style.removeProperty('opacity');
        rightPanel.style.removeProperty('visibility');
        rightPanel.style.removeProperty('pointer-events');
        rightPanel.style.removeProperty('z-index');
      }
    }

    const observer = new MutationObserver(checkAndToggle);
    observer.observe(document.body, { 
      childList: true, 
      subtree: true, 
      attributes: true, 
      attributeFilter: ['class', 'style'] 
    });
    setInterval(checkAndToggle, 150);
  }

  function initAll() {
    setupModalObserver();
    createCompanionDashboard();
    createHudElement();
    createTaskDashboardElement();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
