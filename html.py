
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

    .tabs {
      display: flex;
      gap: 4px;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }

    .tab {
      margin-bottom: -1px;
      border: 0;
      border-bottom: 3px solid transparent;
      border-radius: 6px 6px 0 0;
      color: var(--muted);
      padding: 10px 14px;
    }

    .tab[aria-selected="true"] {
      border-bottom-color: var(--accent);
      color: var(--accent);
    }

    .tab-panel[hidden] { display: none; }

    .helper {
      margin: 10px 0 0 180px;
      color: var(--muted);
      font-size: 13px;
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

    .confirm-resolved { grid-column: 1 / -1; }

    .file-list {
      display: grid;
      gap: 8px;
      max-height: 220px;
      overflow-y: auto;
      padding-right: 4px;
    }

    .file-list-item {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      align-items: center;
    }

    .file-list-item code { margin: 0; }

    .file-list-item button {
      padding: 7px 10px;
    }

    @media (max-width: 820px) {
      .folder-grid, .content { grid-template-columns: 1fr; }
      .helper { margin-left: 0; }
      .actions { align-items: stretch; flex-direction: column; }
      button { width: 100%; }
      .tabs { align-items: stretch; flex-direction: column; }
      .file-list-item { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <main>
    <h1>Duplicate Photo Finder</h1>

    <section class="panel">
      <div class="tabs" role="tablist" aria-label="Duplicate scan type">
        <button class="tab" id="acrossTab" role="tab" aria-selected="true" aria-controls="acrossPanel" data-mode="across">Across two folders</button>
        <button class="tab" id="withinTab" role="tab" aria-selected="false" aria-controls="withinPanel" data-mode="within">Within one folder</button>
      </div>

      <div class="tab-panel" id="acrossPanel" role="tabpanel" aria-labelledby="acrossTab">
        <div class="folder-grid">
          <label for="folderA">Folder A</label>
          <input id="folderA" autocomplete="off">
          <label for="folderB">Folder B</label>
          <input id="folderB" autocomplete="off">
        </div>
          <p class="helper">Scans the two folders and all of their subfolders for matching filenames.</p>
      </div>

      <div class="tab-panel" id="withinPanel" role="tabpanel" aria-labelledby="withinTab" hidden>
        <div class="folder-grid">
          <label for="folderWithin">Parent folder</label>
          <input id="folderWithin" autocomplete="off">
        </div>
        <p class="helper">Scans this folder and all of its subfolders for matching filenames.</p>
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
              <th style="width: 24%">Filename</th>
              <th id="keepHeading" style="width: 38%">Folder A File</th>
              <th id="reviewHeading">Folder B File</th>
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
          <button id="revealKeep" disabled>Reveal A</button>
          <button id="revealDelete" disabled>Reveal B</button>
          <button class="confirm-resolved" id="confirmResolved" disabled>Confirm Resolved</button>
        </div>
      </aside>
    </section>
  </main>

  <script>
    const folderA = document.querySelector('#folderA');
    const folderB = document.querySelector('#folderB');
    const folderWithin = document.querySelector('#folderWithin');
    const scanButton = document.querySelector('#scanButton');
    const statusEl = document.querySelector('#status');
    const resultsBody = document.querySelector('#resultsBody');
    const details = document.querySelector('#details');
    const keepHeading = document.querySelector('#keepHeading');
    const reviewHeading = document.querySelector('#reviewHeading');
    const revealKeep = document.querySelector('#revealKeep');
    const revealDelete = document.querySelector('#revealDelete');
    const tabs = [...document.querySelectorAll('[role="tab"]')];
    const actionButtons = ['revealKeep', 'revealDelete', 'confirmResolved'].map(id => document.querySelector(`#${id}`));

    let mode = 'across';
    let duplicates = [];
    const resolvedIndices = new Set();
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

    function setMode(nextMode) {
      mode = nextMode;
      tabs.forEach(tab => {
        const isActive = tab.dataset.mode === mode;
        tab.setAttribute('aria-selected', String(isActive));
        document.querySelector(`#${tab.getAttribute('aria-controls')}`).hidden = !isActive;
      });

      const isWithin = mode === 'within';
      keepHeading.textContent = isWithin ? 'Matching Files' : 'Folder A File';
      keepHeading.colSpan = isWithin ? 2 : 1;
      reviewHeading.hidden = isWithin;
      revealKeep.hidden = isWithin;
      revealDelete.hidden = isWithin;
      revealKeep.textContent = 'Reveal A';
      revealDelete.textContent = 'Reveal B';

      duplicates = [];
      resolvedIndices.clear();
      renderResults();
      setStatus(isWithin
        ? 'Enter one parent folder path, then scan.'
        : 'Enter two folder paths, then scan.');
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

      if (mode === 'within') {
        details.innerHTML = `
          <div class="path-block"><strong>Filename</strong><code>${escapeHtml(duplicate.filename)}</code></div>
          <div class="path-block"><strong>Copies found</strong><code>${duplicate.files.length}</code></div>
          <p class="status">Use the Reveal button beside any file in the list to locate it.</p>
        `;
        return;
      }

      details.innerHTML = `
        <div class="path-block"><strong>Filename</strong><code>${escapeHtml(duplicate.filename)}</code></div>
        <div class="path-block"><strong>Folder A File</strong><code>${escapeHtml(duplicate.keep.join('\\n'))}</code></div>
        <div class="path-block"><strong>Folder B File</strong><code>${escapeHtml(duplicate.delete)}</code></div>
      `;
    }

    function renderResults() {
      resultsBody.innerHTML = '';
      const visibleIndices = duplicates
        .map((duplicate, index) => index)
        .filter(index => !resolvedIndices.has(index));

      if (!visibleIndices.length) {
        const message = duplicates.length ? 'All duplicates resolved.' : 'No duplicate filenames found.';
        resultsBody.innerHTML = `<tr><td colspan="3" class="empty">${message}</td></tr>`;
        setSelected(null);
        return;
      }

      visibleIndices.forEach(index => {
        const duplicate = duplicates[index];
        const row = document.createElement('tr');
        row.dataset.index = index;
        if (mode === 'within') {
          const fileList = duplicate.files.map((path, fileIndex) => `
            <div class="file-list-item">
              <code>${escapeHtml(path)}</code>
              <button type="button" data-file-index="${fileIndex}">Reveal</button>
            </div>
          `).join('');
          row.innerHTML = `
            <td>${escapeHtml(duplicate.filename)}</td>
            <td colspan="2"><div class="file-list">${fileList}</div></td>
          `;
          row.querySelectorAll('button[data-file-index]').forEach(button => {
            button.addEventListener('click', event => {
              event.stopPropagation();
              revealFile(index, Number(button.dataset.fileIndex));
            });
          });
        } else {
          row.innerHTML = `
            <td>${escapeHtml(duplicate.filename)}</td>
            <td>${escapeHtml(duplicate.keep.join('\\n'))}</td>
            <td>${escapeHtml(duplicate.delete)}</td>
          `;
          row.addEventListener('dblclick', () => openSelected('both'));
        }
        row.addEventListener('click', () => setSelected(index));
        resultsBody.appendChild(row);
      });
      setSelected(visibleIndices[0]);
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
      setStatus(mode === 'within' ? 'Scanning folder...' : 'Scanning folders...');
      try {
        const request = mode === 'within'
          ? { mode, folder: folderWithin.value }
          : { mode, folderA: folderA.value, folderB: folderB.value };
        const data = await api('/api/scan', request);
        duplicates = data.duplicates;
        resolvedIndices.clear();
        renderResults();
        if (mode === 'within') {
          const fileCount = duplicates.reduce((total, duplicate) => total + duplicate.files.length, 0);
          setStatus(`Found ${duplicates.length} duplicate filename group(s), containing ${fileCount} file(s).`);
        } else {
          setStatus(`Found ${duplicates.length} duplicate file(s).`);
        }
      } catch (error) {
        duplicates = [];
        resolvedIndices.clear();
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

    async function revealSelected(target) {
      if (selectedIndex === null) return;
      try {
        await api('/api/reveal', { index: selectedIndex, target });
        const label = mode === 'within'
          ? (target === 'keep' ? 'keep' : 'matching')
          : `Folder ${target === 'keep' ? 'A' : 'B'}`;
        setStatus(`Revealed selected ${label} file(s).`);
      } catch (error) {
        setStatus(error.message, true);
      }
    }

    async function revealFile(index, fileIndex) {
      setSelected(index);
      try {
        await api('/api/reveal', { index, target: 'file', fileIndex });
        setStatus('Revealed selected file.');
      } catch (error) {
        setStatus(error.message, true);
      }
    }

    function confirmResolved() {
      if (selectedIndex === null) return;

      const filename = duplicates[selectedIndex].filename;
      resolvedIndices.add(selectedIndex);
      renderResults();
      const remaining = duplicates.length - resolvedIndices.size;
      const unit = mode === 'within' ? 'duplicate filename group(s)' : 'duplicate file(s)';
      setStatus(`Resolved ${filename}. ${remaining} ${unit} remaining.`);
    }

    scanButton.addEventListener('click', scan);
    revealKeep.addEventListener('click', () => revealSelected('keep'));
    revealDelete.addEventListener('click', () => revealSelected('delete'));
    document.querySelector('#confirmResolved').addEventListener('click', confirmResolved);
    tabs.forEach(tab => tab.addEventListener('click', () => setMode(tab.dataset.mode)));

    fetch('/api/defaults')
      .then(response => response.json())
      .then(defaults => {
        folderA.value = defaults.folderA;
        folderB.value = defaults.folderB;
        folderWithin.value = defaults.folderA;
      });
  </script>
</body>
</html>
"""
