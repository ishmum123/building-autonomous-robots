// ui.js — interactive controls, metrics, and plots for browser sims.
// Vanilla JS, no deps. Load after engine.js.
// All helpers return DOM nodes or objects with a small update API.

(function (root) {
  'use strict';

  // ── Injected base styles (idempotent) ────────────────────────────────────
  function injectStyles() {
    if (document.getElementById('_ui_styles')) return;
    const s = document.createElement('style');
    s.id = '_ui_styles';
    s.textContent = `
      .ui-panel {
        display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
        align-items: center; margin: 6px auto; max-width: 800px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 0.88rem; color: #333;
      }
      .ui-group { display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }
      .ui-group label { font-size: 0.82rem; color: #555; }
      .ui-row { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; align-items: center; margin: 4px auto; }
      .ui-btn {
        padding: 4px 14px; border: 1px solid #aaa; border-radius: 4px;
        background: #f5f5f5; cursor: pointer; font-size: 0.85rem;
        font-family: inherit;
      }
      .ui-btn:hover { background: #e0e0e0; }
      .ui-btn.active { background: #1976d2; color: #fff; border-color: #1976d2; }
      .ui-metrics {
        display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
        margin: 4px auto; font-size: 0.82rem; font-family: monospace;
      }
      .ui-metric { background: #f0f4ff; border-radius: 4px; padding: 2px 8px; }
      .ui-metric span { font-weight: bold; color: #1565c0; }
      .ui-ab { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin: 4px auto; }
      .ui-ab-col { display: flex; flex-direction: column; align-items: center; gap: 4px; }
      .ui-ab-label { font-size: 0.82rem; font-weight: bold; color: #555; }
      canvas.ui-plot { display: block; background: #fafafa; border: 1px solid #ddd; }
    `;
    document.head.appendChild(s);
  }

  // ── panel: generic flex container ────────────────────────────────────────
  function panel(container) {
    injectStyles();
    const div = document.createElement('div');
    div.className = 'ui-panel';
    container.appendChild(div);
    return div;
  }

  // ── row: inline flex row ──────────────────────────────────────────────────
  function row(container) {
    injectStyles();
    const div = document.createElement('div');
    div.className = 'ui-row';
    container.appendChild(div);
    return div;
  }

  // ── slider ────────────────────────────────────────────────────────────────
  // Returns the wrapper element. onChange(value) called on input.
  function slider(container, label, min, max, step, initial, onChange) {
    injectStyles();
    const g = document.createElement('div');
    g.className = 'ui-group';
    const lbl = document.createElement('label');
    lbl.textContent = `${label}: ${initial}`;
    const inp = document.createElement('input');
    inp.type = 'range';
    inp.min = min; inp.max = max; inp.step = step; inp.value = initial;
    inp.style.width = '120px';
    inp.addEventListener('input', () => {
      lbl.textContent = `${label}: ${inp.value}`;
      onChange(parseFloat(inp.value));
    });
    g.appendChild(lbl);
    g.appendChild(inp);
    container.appendChild(g);
    return g;
  }

  // ── numberInput ───────────────────────────────────────────────────────────
  function numberInput(container, label, min, max, step, initial, onChange) {
    injectStyles();
    const g = document.createElement('div');
    g.className = 'ui-group';
    const lbl = document.createElement('label');
    lbl.textContent = label;
    const inp = document.createElement('input');
    inp.type = 'number';
    inp.min = min; inp.max = max; inp.step = step; inp.value = initial;
    inp.style.width = '70px';
    inp.addEventListener('change', () => onChange(parseFloat(inp.value)));
    g.appendChild(lbl);
    g.appendChild(inp);
    container.appendChild(g);
    return g;
  }

  // ── button ────────────────────────────────────────────────────────────────
  function button(container, label, onClick) {
    injectStyles();
    const btn = document.createElement('button');
    btn.className = 'ui-btn';
    btn.textContent = label;
    btn.addEventListener('click', onClick);
    container.appendChild(btn);
    return btn;
  }

  // ── pauseResetBar ─────────────────────────────────────────────────────────
  // paused: external bool ref is kept in the returned object.
  // resetFn: called on Reset click. getRAFId: function returning current rAF id (unused; loop checked via paused flag).
  // Returns { paused, pauseBtn, resetBtn }.
  function pauseResetBar(container, resetFn) {
    injectStyles();
    const r = row(container);
    let paused = false;
    const pauseBtn = button(r, 'Pause', () => {
      paused = !paused;
      pauseBtn.textContent = paused ? 'Resume' : 'Pause';
      pauseBtn.classList.toggle('active', paused);
    });
    const resetBtn = button(r, 'Reset', () => {
      resetFn();
    });
    const state = { get paused() { return paused; } };
    return { state, pauseBtn, resetBtn };
  }

  // ── metrics ───────────────────────────────────────────────────────────────
  // labels: array of strings. Returns { update(values) } where values is array of numbers/strings.
  function metrics(container, labels) {
    injectStyles();
    const div = document.createElement('div');
    div.className = 'ui-metrics';
    const spans = labels.map(lbl => {
      const m = document.createElement('div');
      m.className = 'ui-metric';
      m.innerHTML = `${lbl}: <span>—</span>`;
      div.appendChild(m);
      return m.querySelector('span');
    });
    container.appendChild(div);
    return {
      update(values) {
        values.forEach((v, i) => {
          if (spans[i]) spans[i].textContent = typeof v === 'number' ? v.toFixed(2) : v;
        });
      }
    };
  }

  // ── stripPlot ─────────────────────────────────────────────────────────────
  // opts: { width, height, window (points), colors, labels, yLabel, title }
  // Returns { push(seriesIdx, value), clear(), canvas }
  function stripPlot(container, opts) {
    injectStyles();
    const W = opts.width || 600;
    const H = opts.height || 120;
    const WIN = opts.window || 300;
    const colors = opts.colors || ['#1976d2', '#e53935', '#4caf50', '#ff9800'];
    const seriesLabels = opts.labels || [];
    const title = opts.title || '';

    const cv = document.createElement('canvas');
    cv.className = 'ui-plot';
    cv.width = W; cv.height = H;
    container.appendChild(cv);
    const ctx = cv.getContext('2d');

    const data = [];  // data[i] = circular array of values

    function ensureSeries(i) {
      while (data.length <= i) data.push([]);
    }

    function push(seriesIdx, value) {
      ensureSeries(seriesIdx);
      data[seriesIdx].push(value);
      if (data[seriesIdx].length > WIN) data[seriesIdx].shift();
      _draw();
    }

    function clear() {
      data.forEach(d => d.length = 0);
      ctx.clearRect(0, 0, W, H);
    }

    function _draw() {
      ctx.clearRect(0, 0, W, H);
      // background
      ctx.fillStyle = '#fafafa';
      ctx.fillRect(0, 0, W, H);

      // compute global min/max across all series for autoscale
      let mn = Infinity, mx = -Infinity;
      for (const series of data) {
        for (const v of series) {
          if (v < mn) mn = v;
          if (v > mx) mx = v;
        }
      }
      if (!isFinite(mn)) { mn = -1; mx = 1; }
      if (mn === mx) { mn -= 1; mx += 1; }
      const pad = (mx - mn) * 0.1;
      mn -= pad; mx += pad;

      const PAD_L = 36, PAD_B = 18, PAD_T = title ? 18 : 6, PAD_R = 8;
      const pw = W - PAD_L - PAD_R;
      const ph = H - PAD_T - PAD_B;

      function fy(v) { return PAD_T + ph - (v - mn) / (mx - mn) * ph; }

      // zero line
      if (mn < 0 && mx > 0) {
        const zy = fy(0);
        ctx.strokeStyle = '#ddd'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(PAD_L, zy); ctx.lineTo(PAD_L + pw, zy); ctx.stroke();
      }

      // axes
      ctx.strokeStyle = '#bbb'; ctx.lineWidth = 1;
      ctx.strokeRect(PAD_L, PAD_T, pw, ph);

      // y labels
      ctx.fillStyle = '#888'; ctx.font = '9px sans-serif'; ctx.textAlign = 'right';
      ctx.fillText(mx.toFixed(1), PAD_L - 2, PAD_T + 8);
      ctx.fillText(mn.toFixed(1), PAD_L - 2, PAD_T + ph);
      ctx.fillText(((mn + mx) / 2).toFixed(1), PAD_L - 2, PAD_T + ph / 2 + 4);

      // title
      if (title) {
        ctx.fillStyle = '#555'; ctx.font = '10px sans-serif'; ctx.textAlign = 'left';
        ctx.fillText(title, PAD_L + 2, PAD_T - 4);
      }

      // series
      for (let si = 0; si < data.length; si++) {
        const series = data[si];
        if (series.length < 2) continue;
        ctx.strokeStyle = colors[si % colors.length];
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        const n = series.length;
        for (let i = 0; i < n; i++) {
          const sx = PAD_L + (i / (WIN - 1)) * pw;
          const sy = fy(series[i]);
          i === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
        }
        ctx.stroke();
      }

      // legend
      if (seriesLabels.length) {
        ctx.textAlign = 'left'; ctx.font = '9px sans-serif';
        seriesLabels.forEach((lbl, i) => {
          const lx = PAD_L + 6 + i * 80;
          ctx.fillStyle = colors[i % colors.length];
          ctx.fillRect(lx, H - PAD_B + 4, 12, 4);
          ctx.fillStyle = '#555';
          ctx.fillText(lbl, lx + 14, H - PAD_B + 9);
        });
      }
    }

    _draw();
    return { push, clear, canvas: cv };
  }

  // ── sideBySide ────────────────────────────────────────────────────────────
  // Returns { canvasA, ctxA, canvasB, ctxB, container }
  function sideBySide(container, labelA, labelB, width, height) {
    injectStyles();
    const W = width || 280;
    const H = height || 240;
    const ab = document.createElement('div');
    ab.className = 'ui-ab';

    function makeCol(label) {
      const col = document.createElement('div');
      col.className = 'ui-ab-col';
      const lbl = document.createElement('div');
      lbl.className = 'ui-ab-label';
      lbl.textContent = label;
      const cv = document.createElement('canvas');
      cv.width = W; cv.height = H;
      cv.style.border = '1px solid #ccc';
      cv.style.background = '#fafafa';
      col.appendChild(lbl);
      col.appendChild(cv);
      ab.appendChild(col);
      return cv;
    }

    const canvasA = makeCol(labelA);
    const canvasB = makeCol(labelB);
    container.appendChild(ab);
    return {
      canvasA, ctxA: canvasA.getContext('2d'),
      canvasB, ctxB: canvasB.getContext('2d'),
      container: ab
    };
  }

  // ── public API ────────────────────────────────────────────────────────────
  root.UI = { panel, row, slider, numberInput, button, pauseResetBar, metrics, stripPlot, sideBySide };

}(window));
