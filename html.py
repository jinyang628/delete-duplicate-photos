
INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Duplicate Photo Finder</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #1f2937;
      --muted: #687386;
      --border: #d9dee7;
      --accent: #2563eb;
      --accent-dark: #1d4ed8;
      --danger: #b42318;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    main {
      width: min(1180px, calc(100vw - 32px));
      margin: 24px auto;
    }

    h1 {
      margin: 0 0 16px;
      font-size: 28px;
      font-weight: 700;
      letter-spacing: 0;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
    }

    .folder-grid {
      display: grid;
      grid-template-columns: 180px 1fr;
      gap: 12px;
      align-items: center;
    }

    label {
      color: var(--muted);
      font-size: 14px;
      font-weight: 600;
    }

    input {
      width: 100%;
      min-width: 0;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px 11px;
      font: inherit;
    }

    .actions {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 14px 0;
      min-height: 40px;
    }

    button {
      border: 1px solid var(--border);
      border-radius: 6px;
      background: #fff;
      color: var(--text);
      cursor: pointer;
      font: inherit;
      font-weight: 600;
      padding: 9px 12px;
      white-space: nowrap;
    }

    button.primary {
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }

    button.primary:hover { background: var(--accent-dark); }
    button:disabled { cursor: not-allowed; opacity: 0.55; }

    .status {
      color: var(--muted);
      font-size: 14px;
    }

    .status.error { color: var(--danger); }

    .content {
      display: grid;
      grid-template-columns: minmax(0, 1.6fr) minmax(320px, 0.9fr);
      gap: 14px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }

    th, td {
      border-bottom: 1px solid var(--border);
      padding: 10px;
      text-align: left;
      vertical-align: top;
      overflow-wrap: anywhere;
    }

    th {
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }

    tr { cursor: pointer; }
    tr.selected { background: #eaf1ff; }

    .empty {
      color: var(--muted);
      padding: 24px 10px;
    }

    .details {
      min-height: 420px;
    }

    .details h2 {
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }

    .path-block {
      margin: 12px 0;
    }

    .path-block strong {
      display: block;
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 13px;
    }

    code {
      display: block;
      background: #f1f3f7;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 8px;
      overflow-wrap: anywhere;
      white-space: pre-wrap;
    }

    .button-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 14px;
    }

    @media (max-width: 820px) {
      .folder-grid, .content { grid-template-columns: 1fr; }
      .actions { align-items: stretch; flex-direction: column; }
      button { width: 100%; }
    }
  </style>
</head>
<body>
  <main>
    <h1>Duplicate Photo Finder</h1>

    <section class="panel">
      <div class="folder-grid">
        <label for="folderA">Folder A (keep)</label>
        <input id="folderA" autocomplete="off">
        <label for="folderB">Folder B (review)</label>
        <input id="folderB" autocomplete="off">
      </div>
    </section>

    <div class="actions">
      <button class="primary" id="scanButton">Scan</button>
      <span class="status" id="status">Enter two folder paths, then scan.</span>
    </div>

    <section class="content">
      <div class="panel">
        <table>
          <thead>
            <tr>
              <th style="width: 28%">Filename</th>
              <th style="width: 14%">A copies</th>
              <th>Folder B candidate</th>
            </tr>
          </thead>
          <tbody id="resultsBody">
            <tr><td colspan="3" class="empty">No scan results yet.</td></tr>
          </tbody>
        </table>
      </div>

      <aside class="panel details">
        <h2>Selected duplicate</h2>
        <div id="details">Select a result to review file paths.</div>
        <div class="button-grid">
          <button id="openKeep" disabled>Open A</button>
          <button id="openDelete" disabled>Open B</button>
          <button id="openBoth" disabled>Open Both</button>
          <button id="revealDelete" disabled>Reveal B</button>
        </div>
      </aside>
    </section>
  </main>

  <script>
    const folderA = document.querySelector('#folderA');
    const folderB = document.querySelector('#folderB');
    const scanButton = document.querySelector('#scanButton');
    const statusEl = document.querySelector('#status');
    const resultsBody = document.querySelector('#resultsBody');
    const details = document.querySelector('#details');
    const actionButtons = ['openKeep', 'openDelete', 'openBoth', 'revealDelete'].map(id => document.querySelector(`#${id}`));

    let duplicates = [];
    let selectedIndex = null;

    async function api(path, body) {
      const response = await fetch(path, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body || {})
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Request failed');
      return data;
    }

    function setStatus(message, isError = false) {
      statusEl.textContent = message;
      statusEl.classList.toggle('error', isError);
    }

    function setSelected(index) {
      selectedIndex = index;
      document.querySelectorAll('tbody tr[data-index]').forEach(row => {
        row.classList.toggle('selected', Number(row.dataset.index) === index);
      });

      const duplicate = duplicates[index];
      actionButtons.forEach(button => button.disabled = !duplicate);
      if (!duplicate) {
        details.textContent = 'Select a result to review file paths.';
        return;
      }

      details.innerHTML = `
        <div class="path-block"><strong>Filename</strong><code>${escapeHtml(duplicate.filename)}</code></div>
        <div class="path-block"><strong>Folder A copies to keep</strong><code>${escapeHtml(duplicate.keep.join('\\n'))}</code></div>
        <div class="path-block"><strong>Folder B candidate</strong><code>${escapeHtml(duplicate.delete)}</code></div>
      `;
    }

    function renderResults() {
      resultsBody.innerHTML = '';
      if (!duplicates.length) {
        resultsBody.innerHTML = '<tr><td colspan="3" class="empty">No duplicate filenames found.</td></tr>';
        setSelected(null);
        return;
      }

      duplicates.forEach((duplicate, index) => {
        const row = document.createElement('tr');
        row.dataset.index = index;
        row.innerHTML = `
          <td>${escapeHtml(duplicate.filename)}</td>
          <td>${duplicate.keep.length}</td>
          <td>${escapeHtml(duplicate.delete)}</td>
        `;
        row.addEventListener('click', () => setSelected(index));
        row.addEventListener('dblclick', () => openSelected('both'));
        resultsBody.appendChild(row);
      });
      setSelected(0);
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
    }

    async function scan() {
      scanButton.disabled = true;
      setStatus('Scanning folders...');
      try {
        const data = await api('/api/scan', { folderA: folderA.value, folderB: folderB.value });
        duplicates = data.duplicates;
        renderResults();
        setStatus(`Found ${duplicates.length} duplicate file(s).`);
      } catch (error) {
        duplicates = [];
        renderResults();
        setStatus(error.message, true);
      } finally {
        scanButton.disabled = false;
      }
    }

    async function openSelected(target) {
      if (selectedIndex === null) return;
      try {
        await api('/api/open', { index: selectedIndex, target });
        setStatus('Opened selected file(s).');
      } catch (error) {
        setStatus(error.message, true);
      }
    }

    async function revealSelected() {
      if (selectedIndex === null) return;
      try {
        await api('/api/reveal', { index: selectedIndex });
        setStatus('Revealed selected Folder B file.');
      } catch (error) {
        setStatus(error.message, true);
      }
    }

    scanButton.addEventListener('click', scan);
    document.querySelector('#openKeep').addEventListener('click', () => openSelected('keep'));
    document.querySelector('#openDelete').addEventListener('click', () => openSelected('delete'));
    document.querySelector('#openBoth').addEventListener('click', () => openSelected('both'));
    document.querySelector('#revealDelete').addEventListener('click', revealSelected);

    fetch('/api/defaults')
      .then(response => response.json())
      .then(defaults => {
        folderA.value = defaults.folderA;
        folderB.value = defaults.folderB;
      });
  </script>
</body>
</html>
"""