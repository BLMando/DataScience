/**
 * Site.js - Shared utilities for dashboard rendering
 */

const Utils = {
  /**
   * Format number with thousands separator
   */
  formatNumber(num) {
    return num.toLocaleString('it-IT');
  },

  /**
   * Format percentage
   */
  formatPercent(value, decimals = 1) {
    return value.toFixed(decimals) + '%';
  },

  /**
   * Format time in mm:ss
   */
  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  },

  /**
   * Format date as dd/mm/yyyy
   */
  formatDate(dateStr) {
    const d = new Date(dateStr);
    return d.toLocaleDateString('it-IT');
  },

  /**
   * Calculate average of array
   */
  average(arr) {
    if (arr.length === 0) return 0;
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  },

  /**
   * Group array by key
   */
  groupBy(arr, key) {
    return arr.reduce((acc, item) => {
      const k = typeof key === 'function' ? key(item) : item[key];
      (acc[k] = acc[k] || []).push(item);
      return acc;
    }, {});
  },

  /**
   * Count occurrences
   */
  countBy(arr, key) {
    const groups = Utils.groupBy(arr, key);
    return Object.fromEntries(
      Object.entries(groups).map(([k, v]) => [k, v.length])
    );
  },

  /**
   * Get max value with percentage for bar charts
   */
  calcBarPercent(value, max) {
    return Math.round((value / max) * 100);
  }
};

/**
 * Render functions
 */
const Render = {
  /**
   * Render KPI card
   */
  kpi(containerId, kpis) {
    const container = document.getElementById(containerId);
    container.innerHTML = kpis.map(kpi => `
      <div class="kpi-card">
        <div class="kpi-label">${kpi.label}</div>
        <div class="kpi-value ${kpi.color || ''}">${kpi.value}</div>
        ${kpi.change ? `
          <div class="kpi-change ${kpi.changeDir || ''}">
            ${kpi.changeDir === 'up' ? '↑' : kpi.changeDir === 'down' ? '↓' : ''}
            ${kpi.change}
          </div>
        ` : ''}
      </div>
    `).join('');
  },

  /**
   * Render horizontal bar chart
   */
  barChart(containerId, data, colorClass = 'primary') {
    const container = document.getElementById(containerId);
    const max = Math.max(...data.map(d => d.value));

    container.innerHTML = data.map(item => `
      <div class="bar-item">
        <span class="bar-label">${item.label}</span>
        <div class="bar-track">
          <div class="bar-fill ${item.color || colorClass}" style="width: ${Utils.calcBarPercent(item.value, max)}%"></div>
        </div>
        <span class="bar-value">${item.display || item.value}</span>
      </div>
    `).join('');
  },

  /**
 * Render vertical bar chart
 */
  verticalBars(containerId, data, colorClass = 'primary') {
    const container = document.getElementById(containerId);
    const max = Math.max(...data.map(d => d.value));

    container.innerHTML = data.map(item => {
      const heightPercent = Math.max(5, Utils.calcBarPercent(item.value, max));
      return `
      <div class="h-bar">
        <span class="h-bar-value">${item.value}</span>
        <div class="h-bar-fill" style="height: ${heightPercent}%; background: var(--color-${item.color || colorClass});"></div>
        <span class="h-bar-label">${item.label}</span>
      </div>
    `;
    }).join('');
  },

  /**
   * Render data table
   */
  table(containerId, columns, rows) {
    const container = document.getElementById(containerId);

    container.innerHTML = `
      <table class="data-table">
        <thead>
          <tr>
            ${columns.map(col => `<th>${col.label}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
          ${rows.map(row => `
            <tr>
              ${columns.map(col => `<td>${col.render ? col.render(row[col.key], row) : row[col.key]}</td>`).join('')}
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  },

  /**
   * Render insights
   */
  insights(containerId, items) {
    const container = document.getElementById(containerId);

    container.innerHTML = items.map(item => `
      <div class="insight-item ${item.type || ''}">
        <span class="insight-icon">${item.icon}</span>
        <span class="insight-text">${item.text}</span>
      </div>
    `).join('');
  }
};
