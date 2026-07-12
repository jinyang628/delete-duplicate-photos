
INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Duplicate File Finder</title>
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
      margin: 0;
      font-size: 28px;
      font-weight: 700;
      letter-spacing: 0;
    }

    .page-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 16px;
    }

    .language-toggle {
      display: flex;
      gap: 4px;
      padding: 3px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--panel);
    }

    .language-toggle button {
      border: 0;
      padding: 6px 10px;
      color: var(--muted);
    }

    .language-toggle button[aria-pressed="true"] {
      background: var(--accent);
      color: #fff;
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

    .file-types {
      border: 0;
      border-top: 1px solid var(--border);
      margin: 16px 0 0;
      padding: 14px 0 0;
    }

    .file-types legend {
      color: var(--muted);
      font-size: 14px;
      font-weight: 600;
      padding: 0 0 8px;
    }

    .option-list { display: flex; flex-wrap: wrap; gap: 8px; }

    .file-type-option input {
      position: absolute;
      opacity: 0;
      pointer-events: none;
    }

    .file-type-option span {
      display: block;
      border: 1px solid var(--border);
      border-radius: 999px;
      color: var(--muted);
      cursor: pointer;
      padding: 8px 12px;
    }

    .file-type-option input:checked + span {
      background: #eaf1ff;
      border-color: var(--accent);
      color: var(--accent-dark);
    }

    .file-type-option input:focus-visible + span {
      outline: 2px solid var(--accent);
      outline-offset: 2px;
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
      .language-toggle button { width: auto; }
    }
  </style>
</head>
<body>
  <main>
    <header class="page-header">
      <h1 data-i18n="title">Duplicate File Finder</h1>
      <div class="language-toggle" role="group" aria-label="Language" data-i18n-aria-label="language">
        <button type="button" data-language="en" aria-pressed="true">English</button>
        <button type="button" data-language="zh" aria-pressed="false">中文</button>
      </div>
    </header>

    <section class="panel">
      <div class="tabs" role="tablist" aria-label="Duplicate scan type" data-i18n-aria-label="scanType">
        <button class="tab" id="acrossTab" role="tab" aria-selected="true" aria-controls="acrossPanel" data-mode="across" data-i18n="acrossTab">Across two folders</button>
        <button class="tab" id="withinTab" role="tab" aria-selected="false" aria-controls="withinPanel" data-mode="within" data-i18n="withinTab">Within one folder</button>
      </div>

      <div class="tab-panel" id="acrossPanel" role="tabpanel" aria-labelledby="acrossTab">
        <div class="folder-grid">
          <label for="folderA" data-i18n="folderA">Folder A</label>
          <input id="folderA" autocomplete="off">
          <label for="folderB" data-i18n="folderB">Folder B</label>
          <input id="folderB" autocomplete="off">
        </div>
          <p class="helper" data-i18n="acrossHelp">Scans the two folders and all of their subfolders for matching filenames.</p>
      </div>

      <div class="tab-panel" id="withinPanel" role="tabpanel" aria-labelledby="withinTab" hidden>
        <div class="folder-grid">
          <label for="folderWithin" data-i18n="parentFolder">Parent folder</label>
          <input id="folderWithin" autocomplete="off">
        </div>
        <p class="helper" data-i18n="withinHelp">Scans this folder and all of its subfolders for matching filenames.</p>
      </div>

      <fieldset class="file-types">
        <legend data-i18n="fileTypes">File types to scan</legend>
        <div class="option-list">
          <label class="file-type-option"><input type="checkbox" name="fileType" value="images" checked><span data-i18n="images">Images</span></label>
          <label class="file-type-option"><input type="checkbox" name="fileType" value="videos"><span data-i18n="videos">Videos</span></label>
          <label class="file-type-option"><input type="checkbox" name="fileType" value="word"><span data-i18n="word">Word documents</span></label>
          <label class="file-type-option"><input type="checkbox" name="fileType" value="excel"><span data-i18n="excel">Excel spreadsheets</span></label>
        </div>
      </fieldset>
    </section>

    <div class="actions">
      <button class="primary" id="scanButton" data-i18n="scan">Scan</button>
      <span class="status" id="status">Enter two folder paths, then scan.</span>
    </div>

    <section class="content">
      <div class="panel">
        <table>
          <thead>
            <tr>
              <th style="width: 24%" data-i18n="filename">Filename</th>
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
        <h2 data-i18n="selectedDuplicate">Selected duplicate</h2>
        <div id="details">Select a result to review file paths.</div>
        <div class="button-grid">
          <button id="revealKeep" disabled>Reveal A</button>
          <button id="revealDelete" disabled>Reveal B</button>
          <button class="confirm-resolved" id="confirmResolved" disabled data-i18n="confirmResolved">Confirm Resolved</button>
        </div>
      </aside>
    </section>
  </main>

  <script>
    const translations = {
      en: {
        title: 'Duplicate File Finder', language: 'Language', scanType: 'Duplicate scan type',
        acrossTab: 'Across two folders', withinTab: 'Within one folder', folderA: 'Folder A', folderB: 'Folder B',
        parentFolder: 'Parent folder', acrossHelp: 'Scans the two folders and all of their subfolders for matching filenames.',
        withinHelp: 'Scans this folder and all of its subfolders for matching filenames.', fileTypes: 'File types to scan',
        images: 'Images', videos: 'Videos', word: 'Word documents', excel: 'Excel spreadsheets', scan: 'Scan',
        filename: 'Filename', folderAFile: 'Folder A File', folderBFile: 'Folder B File', matchingFiles: 'Matching Files',
        selectedDuplicate: 'Selected duplicate', selectResult: 'Select a result to review file paths.', revealA: 'Reveal A',
        revealB: 'Reveal B', reveal: 'Reveal', confirmResolved: 'Confirm Resolved', enterAcross: 'Enter two folder paths, then scan.',
        enterWithin: 'Enter one parent folder path, then scan.', noResultsYet: 'No scan results yet.', noDuplicates: 'No duplicate filenames found.',
        allResolved: 'All duplicates resolved.', copiesFound: 'Copies found', revealHelp: 'Use the Reveal button beside any file in the list to locate it.',
        selectFileType: 'Select at least one file type to scan.', scanningFolder: 'Scanning folder...', scanningFolders: 'Scanning folders...',
        opened: 'Opened selected file(s).', revealedFile: 'Revealed selected file.', revealedSelected: label => `Revealed selected ${label} file(s).`,
        folderLabel: letter => `Folder ${letter}`, foundAcross: count => `Found ${count} duplicate file(s).`,
        foundWithin: (groups, files) => `Found ${groups} duplicate filename group(s), containing ${files} file(s).`,
        resolved: (name, remaining, within) => `Resolved ${name}. ${remaining} ${within ? 'duplicate filename group(s)' : 'duplicate file(s)'} remaining.`
      },
      zh: {
        title: '重复文件查找器', language: '语言', scanType: '重复文件扫描方式', acrossTab: '对比两个文件夹', withinTab: '扫描一个文件夹',
        folderA: '文件夹 A', folderB: '文件夹 B', parentFolder: '父文件夹', acrossHelp: '扫描这两个文件夹及其所有子文件夹，查找同名文件。',
        withinHelp: '扫描此文件夹及其所有子文件夹，查找同名文件。', fileTypes: '要扫描的文件类型', images: '图片', videos: '视频',
        word: 'Word 文档', excel: 'Excel 表格', scan: '扫描', filename: '文件名', folderAFile: '文件夹 A 中的文件',
        folderBFile: '文件夹 B 中的文件', matchingFiles: '同名文件', selectedDuplicate: '选中的重复文件',
        selectResult: '请选择一条结果以查看文件路径。', revealA: '在文件夹中显示 A', revealB: '在文件夹中显示 B', reveal: '显示位置',
        confirmResolved: '确认已处理', enterAcross: '请输入两个文件夹路径，然后扫描。', enterWithin: '请输入一个父文件夹路径，然后扫描。',
        noResultsYet: '尚无扫描结果。', noDuplicates: '未找到同名文件。', allResolved: '所有重复文件均已处理。', copiesFound: '找到的副本数',
        revealHelp: '使用列表中各文件旁的“显示位置”按钮来定位文件。', selectFileType: '请至少选择一种要扫描的文件类型。',
        scanningFolder: '正在扫描文件夹…', scanningFolders: '正在扫描文件夹…', opened: '已打开选中的文件。', revealedFile: '已显示选中文件的位置。',
        revealedSelected: label => `已显示选中的${label}文件位置。`, folderLabel: letter => `文件夹 ${letter}`,
        foundAcross: count => `找到 ${count} 个重复文件。`, foundWithin: (groups, files) => `找到 ${groups} 组同名文件，共 ${files} 个文件。`,
        resolved: (name, remaining, within) => `已处理 ${name}。剩余 ${remaining} ${within ? '组同名文件' : '个重复文件'}。`
      }
    };

    let language = 'en';
    const t = key => translations[language][key];
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
    const languageButtons = [...document.querySelectorAll('[data-language]')];
    const actionButtons = ['revealKeep', 'revealDelete', 'confirmResolved'].map(id => document.querySelector(`#${id}`));

    let mode = 'across';
    let duplicates = [];
    let hasScanned = false;
    const resolvedIndices = new Set();
    let selectedIndex = null;
    let currentStatus = { key: 'enterAcross', args: [], isError: false };
    const clientId = crypto.randomUUID();

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

    function setStatusTranslation(key, ...args) {
      currentStatus = { key, args, isError: false };
      const value = t(key);
      setStatus(typeof value === 'function' ? value(...args) : value);
    }

    function setLanguage(nextLanguage) {
      language = nextLanguage;
      document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
      document.title = t('title');
      document.querySelectorAll('[data-i18n]').forEach(element => {
        element.textContent = t(element.dataset.i18n);
      });
      document.querySelectorAll('[data-i18n-aria-label]').forEach(element => {
        element.setAttribute('aria-label', t(element.dataset.i18nAriaLabel));
      });
      languageButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.language === language)));
      const isWithin = mode === 'within';
      keepHeading.textContent = isWithin ? t('matchingFiles') : t('folderAFile');
      reviewHeading.textContent = t('folderBFile');
      revealKeep.textContent = t('revealA');
      revealDelete.textContent = t('revealB');
      renderResults();
      const value = t(currentStatus.key);
      if (value) setStatus(typeof value === 'function' ? value(...currentStatus.args) : value, currentStatus.isError);
    }

    function setMode(nextMode) {
      mode = nextMode;
      tabs.forEach(tab => {
        const isActive = tab.dataset.mode === mode;
        tab.setAttribute('aria-selected', String(isActive));
        document.querySelector(`#${tab.getAttribute('aria-controls')}`).hidden = !isActive;
      });

      const isWithin = mode === 'within';
      keepHeading.textContent = isWithin ? t('matchingFiles') : t('folderAFile');
      keepHeading.colSpan = isWithin ? 2 : 1;
      reviewHeading.hidden = isWithin;
      revealKeep.hidden = isWithin;
      revealDelete.hidden = isWithin;
      revealKeep.textContent = t('revealA');
      revealDelete.textContent = t('revealB');

      duplicates = [];
      hasScanned = false;
      resolvedIndices.clear();
      renderResults();
      setStatusTranslation(isWithin ? 'enterWithin' : 'enterAcross');
    }

    function setSelected(index) {
      selectedIndex = index;
      document.querySelectorAll('tbody tr[data-index]').forEach(row => {
        row.classList.toggle('selected', Number(row.dataset.index) === index);
      });

      const duplicate = duplicates[index];
      actionButtons.forEach(button => button.disabled = !duplicate);
      if (!duplicate) {
        details.textContent = t('selectResult');
        return;
      }

      if (mode === 'within') {
        details.innerHTML = `
          <div class="path-block"><strong>${t('filename')}</strong><code>${escapeHtml(duplicate.filename)}</code></div>
          <div class="path-block"><strong>${t('copiesFound')}</strong><code>${duplicate.files.length}</code></div>
          <p class="status">${t('revealHelp')}</p>
        `;
        return;
      }

      details.innerHTML = `
        <div class="path-block"><strong>${t('filename')}</strong><code>${escapeHtml(duplicate.filename)}</code></div>
        <div class="path-block"><strong>${t('folderAFile')}</strong><code>${escapeHtml(duplicate.keep.join('\\n'))}</code></div>
        <div class="path-block"><strong>${t('folderBFile')}</strong><code>${escapeHtml(duplicate.delete)}</code></div>
      `;
    }

    function renderResults() {
      resultsBody.innerHTML = '';
      const visibleIndices = duplicates
        .map((duplicate, index) => index)
        .filter(index => !resolvedIndices.has(index));

      if (!visibleIndices.length) {
        const message = duplicates.length ? t('allResolved') : (hasScanned ? t('noDuplicates') : t('noResultsYet'));
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
              <button type="button" data-file-index="${fileIndex}">${t('reveal')}</button>
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
      const fileTypes = [...document.querySelectorAll('input[name="fileType"]:checked')]
        .map(input => input.value);
      if (!fileTypes.length) {
        currentStatus = { key: 'selectFileType', args: [], isError: true };
        setStatus(t('selectFileType'), true);
        return;
      }
      scanButton.disabled = true;
      setStatusTranslation(mode === 'within' ? 'scanningFolder' : 'scanningFolders');
      try {
        const request = mode === 'within'
          ? { mode, folder: folderWithin.value, fileTypes }
          : { mode, folderA: folderA.value, folderB: folderB.value, fileTypes };
        const data = await api('/api/scan', request);
        duplicates = data.duplicates;
        hasScanned = true;
        resolvedIndices.clear();
        renderResults();
        if (mode === 'within') {
          const fileCount = duplicates.reduce((total, duplicate) => total + duplicate.files.length, 0);
          setStatusTranslation('foundWithin', duplicates.length, fileCount);
        } else {
          setStatusTranslation('foundAcross', duplicates.length);
        }
      } catch (error) {
        duplicates = [];
        hasScanned = false;
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
        setStatusTranslation('opened');
      } catch (error) {
        setStatus(error.message, true);
      }
    }

    async function revealSelected(target) {
      if (selectedIndex === null) return;
      try {
        await api('/api/reveal', { index: selectedIndex, target });
        const label = mode === 'within'
          ? t('matchingFiles')
          : t('folderLabel')(target === 'keep' ? 'A' : 'B');
        setStatusTranslation('revealedSelected', label);
      } catch (error) {
        setStatus(error.message, true);
      }
    }

    async function revealFile(index, fileIndex) {
      setSelected(index);
      try {
        await api('/api/reveal', { index, target: 'file', fileIndex });
        setStatusTranslation('revealedFile');
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
      setStatusTranslation('resolved', filename, remaining, mode === 'within');
    }

    scanButton.addEventListener('click', scan);
    revealKeep.addEventListener('click', () => revealSelected('keep'));
    revealDelete.addEventListener('click', () => revealSelected('delete'));
    document.querySelector('#confirmResolved').addEventListener('click', confirmResolved);
    tabs.forEach(tab => tab.addEventListener('click', () => setMode(tab.dataset.mode)));
    languageButtons.forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.language)));

    // Register this tab with the local Python process. pagehide covers closing
    // the tab/window and sendBeacon can finish even while the page is unloading.
    window.addEventListener('pageshow', () => {
      api('/api/connect', { clientId }).catch(() => {});
    });
    window.addEventListener('pagehide', () => {
      navigator.sendBeacon('/api/disconnect', JSON.stringify({ clientId }));
    });

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
