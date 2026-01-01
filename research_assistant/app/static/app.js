async function analyzeDataset() {
    const fileInput = document.getElementById('csv-file');
    const fileNameDisplay = document.getElementById('file-name');
    const loading = document.getElementById('loading');
    const resultsArea = document.getElementById('results-area');

    if (fileInput.files.length === 0) return;

    const file = fileInput.files[0];
    fileNameDisplay.textContent = `Selected: ${file.name}`;

    loading.classList.remove('hidden');
    resultsArea.classList.add('hidden');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }

        const data = await response.json();
        renderResults(data);
    } catch (err) {
        alert('Error: ' + err.message);
    } finally {
        loading.classList.add('hidden');
    }
}

function renderResults(data) {
    if (!data || !data.analysis) return;

    const resultsArea = document.getElementById('results-area');
    resultsArea.classList.remove('hidden');

    // Overview
    const overview = document.getElementById('dataset-overview');
    const rowCount = data.analysis.info?.rows ?? 0;
    const colCount = data.analysis.info?.columns ?? 0;
    const outlierCount = data.analysis.outlier_count ?? 0;

    overview.innerHTML = `
        <div class="stat-item"><span class="stat-label">Total Records</span><span class="stat-value">${rowCount}</span></div>
        <div class="stat-item"><span class="stat-label">Variable Count</span><span class="stat-value">${colCount}</span></div>
        <div class="stat-item"><span class="stat-label">Detected Anomalies</span><span class="stat-value">${outlierCount}</span></div>
    `;

    // Summary Lists
    updateList('observations-list', data.summary?.observations || ["No observations available."]);
    updateList('quality-list', data.summary?.quality_issues || ["No quality issues identified."]);
    updateList('steps-list', data.summary?.next_steps || ["No recommendations at this stage."]);

    // Visualizations
    const vizTitle = document.getElementById('viz-title');
    const vizContainer = document.getElementById('viz-container');
    const vizSection = document.getElementById('viz-section');
    vizContainer.innerHTML = '';

    let hasVisuals = false;
    if (data.visuals?.distributions) {
        addImage(vizContainer, data.visuals.distributions, 'Distribution Analysis');
        hasVisuals = true;
    }
    if (data.visuals?.boxplots) {
        addImage(vizContainer, data.visuals.boxplots, 'Anomaly Detection');
        hasVisuals = true;
    }
    if (data.visuals?.heatmap) {
        addImage(vizContainer, data.visuals.heatmap, 'Correlation Matrix');
        hasVisuals = true;
    }

    if (hasVisuals) {
        vizSection.classList.remove('hidden');
    } else {
        vizSection.classList.add('hidden');
    }
}

function updateList(id, items) {
    const list = document.getElementById(id);
    list.innerHTML = items.map(item => `<li>${item}</li>`).join('');
}

function addImage(container, base64, title) {
    const img = document.createElement('img');
    img.src = `data:image/png;base64,${base64}`;
    img.alt = title;
    container.appendChild(img);
}

document.getElementById('csv-file').addEventListener('change', analyzeDataset);
