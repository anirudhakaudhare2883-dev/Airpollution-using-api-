import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Urban Air Analyzer | Environmental Data</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #f0f4f8; /* Soft corporate blue/grey */
            --bg-nav: #ffffff;
            --bg-card: #ffffff;
            --border: #e2e8f0;
            --border-highlight: #2563eb;
            --accent: #2563eb; /* Royal blue */
            --accent-sec: #f97316; /* Coral */
            --t-main: #1e293b;
            --t-mut: #64748b;
            --success: #059669;
            --warning: #d97706;
            --danger: #dc2626;
            --shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03);
            --glow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(37, 99, 235, 0.06);
            --radius: 6px;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg);
            color: var(--t-main);
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
            background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23cbd5e1' fill-opacity='0.15'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

        /* NAVBAR */
        .pn {
            background: var(--bg-nav);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: var(--shadow);
        }
        .pn .inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.7rem 2rem;
        }
        .nb {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            text-decoration: none;
        }
        .nb-i {
            width: 32px;
            height: 32px;
            border-radius: 4px;
            background: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 1rem;
        }
        .nb-t {
            font-weight: 700;
            font-size: 1.05rem;
            color: var(--t-main);
            letter-spacing: -0.2px;
        }
        .bh {
            background: #f1f5f9;
            color: var(--t-mut);
            border: 1px solid var(--border);
            padding: 0.4rem 1rem;
            border-radius: var(--radius);
            font-size: 0.8rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
        }
        .bh:hover {
            background: #e2e8f0;
            color: var(--t-main);
        }

        /* LAYOUT */
        .dw {
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }

        /* CARDS */
        .glass-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            transition: all 0.2s ease;
            position: relative;
        }
        .glass-card:hover {
            border-color: #cbd5e1;
            box-shadow: var(--glow);
        }
        
        .card-header-neo {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border);
            background: #f8fafc;
            border-top-left-radius: var(--radius);
            border-top-right-radius: var(--radius);
        }
        .card-title-neo {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--t-main);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        .card-title-neo i {
            color: var(--accent);
        }
        .card-body-neo {
            padding: 1.25rem;
        }

        /* FORM STYLING */
        .form-label-neo {
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--t-mut);
            text-transform: uppercase;
            letter-spacing: 0.2px;
            margin-bottom: 0.3rem;
        }
        .form-control-neo, .form-select-neo {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            color: var(--t-main);
            border-radius: 4px;
            padding: 0.5rem 0.6rem;
            font-size: 0.85rem;
            font-family: inherit;
        }
        .form-control-neo:focus, .form-select-neo:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
            outline: none;
        }
        .input-group-text-neo {
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            color: var(--t-mut);
            border-right: none;
            font-size: 0.8rem;
            font-weight: 600;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
        }
        .input-group .form-control-neo { border-left: none; }
        
        .btn-neo-primary {
            background: var(--accent);
            color: #fff;
            border: none;
            padding: 0.65rem;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .btn-neo-primary:hover {
            background: #1d4ed8;
            color: #fff;
            transform: translateY(-1px);
        }
        .btn-neo-sec {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            color: var(--t-main);
            padding: 0.65rem;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .btn-neo-sec:hover {
            background: #f8fafc;
            border-color: #94a3b8;
        }

        /* ------------------ DASHBOARD (OUTPUT) ------------------ */
        .dash-top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .dash-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--t-main);
            margin: 0;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--accent);
            display: inline-block;
        }
        .dash-actions {
            display: flex;
            gap: 0.8rem;
        }
        .btn-dash-action {
            background: #fff;
            border: 1px solid #cbd5e1;
            color: var(--t-mut);
            padding: 0.4rem 1rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            transition: all 0.2s;
            cursor: pointer;
        }
        .btn-dash-action:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        /* KPI CARDS */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.2rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            box-shadow: var(--shadow);
            border-left: 4px solid var(--border); /* dynamic border */
        }
        .kpi-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            flex-shrink: 0;
            background: #f1f5f9;
            color: var(--t-mut);
        }
        .kpi-content { flex: 1; }
        .kpi-label {
            font-size: 0.7rem;
            color: var(--t-mut);
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 0.1rem;
        }
        .kpi-val {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--t-main);
            line-height: 1.1;
        }

        /* MAIN VISUALS */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        #map {
            height: 380px;
            width: 100%;
            border-radius: 4px;
            z-index: 1;
            border: 1px solid #e2e8f0;
        }

        /* GAUGE */
        .gauge-container {
            position: relative;
            height: 150px;
            display: flex;
            justify-content: center;
            align-items: flex-end;
        }
        .gauge-center {
            position: absolute;
            bottom: 0;
            text-align: center;
            transform: translateY(10%);
        }
        .gauge-val {
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
            color: var(--t-main);
        }
        .gauge-lbl {
            font-size: 0.75rem;
            color: var(--t-mut);
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 5px;
        }

        /* AI INSIGHTS */
        .ai-panel {
            background: #f8fafc;
            border: 1px solid var(--border);
            padding: 1.25rem;
            border-radius: var(--radius);
        }
        .ai-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: #eff6ff;
            color: #2563eb;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            border: 1px solid #bfdbfe;
            margin-bottom: 0.8rem;
        }
        .ai-text {
            font-size: 0.85rem;
            line-height: 1.5;
            color: var(--t-main);
            font-weight: 500;
        }

        /* SKELETON PRELOADER */
        .skeleton-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(255,255,255,0.95);
            z-index: 50;
            border-radius: var(--radius);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 1;
            transition: opacity 0.4s;
        }
        .skeleton-overlay.hide { opacity: 0; pointer-events: none; }
        .spinner-border { color: var(--accent); }

        .progress-bar-container {
            width: 100%;
            height: 4px;
            background: #e2e8f0;
            border-radius: 4px;
            margin-top: 0.5rem;
        }
        .progress-bar-fill {
            height: 100%;
            border-radius: 4px;
            width: 0%;
            transition: width 1s;
        }

        @media(max-width: 1200px) {
            .kpi-grid { grid-template-columns: repeat(2, 1fr); }
            .main-grid { grid-template-columns: 1fr; }
        }
        @media(max-width: 768px) {
            .kpi-grid { grid-template-columns: 1fr; }
            .dw { padding: 1rem; }
            .dash-top-bar { flex-direction: column; gap: 1rem; align-items: flex-start; }
            #map { height: 300px; }
        }
    </style>
</head>
<body>

    <nav class="pn">
        <div class="inner">
            <a class="nb" href="#">
                <div class="nb-i"><i class="fa-solid fa-leaf"></i></div>
                <div>
                    <div class="nb-t">Urban Air Analyzer</div>
                </div>
            </a>
            <div class="d-flex align-items-center gap-2">
                <a href="/" class="bh"><i class="fa-solid fa-house me-1"></i> Return Home</a>
            </div>
        </div>
    </nav>

    <div class="dw">
        <div class="row g-4">
            
            <div class="{% if data %}col-xl-3{% else %}col-xl-4 mx-auto mt-5{% endif %}">
                <div class="glass-card">
                    <div class="card-header-neo">
                        <h6 class="card-title-neo"><i class="fa-solid fa-sliders"></i> Coordinates & Data</h6>
                    </div>
                    <div class="card-body-neo">
                        <form method="POST" id="aqiForm">
                            <label class="form-label-neo">Region Selection</label>
                            <select id="country" class="form-control form-select-neo mb-2" onchange="loadStates()">
                                <option value="">Select Country</option>
                            </select>
                            <div class="row g-2 mb-2">
                                <div class="col-6"><select id="state" class="form-control form-select-neo" onchange="loadCities()" disabled><option value="">State</option></select></div>
                                <div class="col-6"><select id="city" class="form-control form-select-neo" disabled><option value="">City</option></select></div>
                            </div>
                            <button type="button" onclick="getCoords()" class="btn-neo-sec w-100 mb-3" style="font-size:0.75rem;"><i class="fa-solid fa-crosshairs me-1"></i> Acquire Location</button>
                            
                            <div class="row g-2 mb-3">
                                <div class="col-6"><label class="form-label-neo">Latitude</label><input type="text" id="lat" name="lat" class="form-control form-control-neo" placeholder="0.00" required readonly></div>
                                <div class="col-6"><label class="form-label-neo">Longitude</label><input type="text" id="lon" name="lon" class="form-control form-control-neo" placeholder="0.00" required readonly></div>
                            </div>

                            <label class="form-label-neo mt-2">Particulate & Gas Variables</label>
                            <div class="row g-2 mb-4">
                                <div class="col-6">
                                    <div class="input-group">
                                        <span class="input-group-text input-group-text-neo">PM2.5</span>
                                        <input type="number" step="any" id="pm25" name="pm25" class="form-control form-control-neo" required>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="input-group">
                                        <span class="input-group-text input-group-text-neo">PM10</span>
                                        <input type="number" step="any" id="pm10" name="pm10" class="form-control form-control-neo" required>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="input-group">
                                        <span class="input-group-text input-group-text-neo">NO₂</span>
                                        <input type="number" step="any" id="no2" name="no2" class="form-control form-control-neo" required>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="input-group">
                                        <span class="input-group-text input-group-text-neo">O₃</span>
                                        <input type="number" step="any" id="o3" name="o3" class="form-control form-control-neo" required>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button type="button" id="btnFetch" onclick="getAirQuality()" class="btn-neo-sec"><i class="fa-solid fa-cloud-download-alt me-1"></i> Poll External API</button>
                                <button type="submit" class="btn-neo-primary" id="btnPredict"><i class="fa-solid fa-microchip me-1"></i> Compute Index</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            {% if data %}
            <div class="col-xl-9">
                <div class="dash-top-bar">
                    <h1 class="dash-title">Environmental Report</h1>
                    <div class="dash-actions">
                        <button class="btn-dash-action" onclick="window.print()"><i class="fa-solid fa-print me-1"></i> Print / Save</button>
                    </div>
                </div>

                <!-- KPIs -->
                <div class="kpi-grid">
                    <div class="kpi-card" id="card-aqi">
                        <div class="kpi-icon" id="icon-aqi"><i class="fa-solid fa-wind"></i></div>
                        <div class="kpi-content">
                            <div class="kpi-label">Current AQI</div>
                            <div class="kpi-val">{{ data.aqi }}</div>
                            <div class="progress-bar-container"><div class="progress-bar-fill" id="aqi-bar"></div></div>
                        </div>
                    </div>
                    <div class="kpi-card border-left-0">
                        <div class="kpi-icon" id="icon-cat"><i class="fa-solid fa-circle-check"></i></div>
                        <div class="kpi-content">
                            <div class="kpi-label">Classification</div>
                            <div class="kpi-val" style="font-size:1.1rem;margin-top:4px;" id="kpi-cat-text">{{ data.category }}</div>
                        </div>
                    </div>
                    <div class="kpi-card border-left-0">
                        <div class="kpi-icon"><i class="fa-solid fa-smog"></i></div>
                        <div class="kpi-content">
                            <div class="kpi-label">Dominant Vector</div>
                            <div class="kpi-val" id="kpi-prime" style="font-size:1.3rem;">--</div>
                        </div>
                    </div>
                    <div class="kpi-card border-left-0">
                        <div class="kpi-icon"><i class="fa-solid fa-notes-medical"></i></div>
                        <div class="kpi-content">
                            <div class="kpi-label">Alert Status</div>
                            <div class="kpi-val" id="kpi-risk" style="font-size:1rem;margin-top:4px;">Evaluating...</div>
                        </div>
                    </div>
                </div>

                <div class="main-grid">
                    <!-- LEFT: MAP -->
                    <div class="glass-card">
                        <div class="card-header-neo">
                            <h6 class="card-title-neo"><i class="fa-solid fa-location-arrow"></i> Zone Map</h6>
                        </div>
                        <div class="card-body-neo p-0">
                            <div id="map"></div>
                        </div>
                    </div>

                    <!-- RIGHT: CHARTS -->
                    <div class="d-flex flex-column gap-3 h-100">
                        <div class="glass-card flex-fill">
                            <div class="card-header-neo">
                                <h6 class="card-title-neo"><i class="fa-solid fa-gauge"></i> Index Scale</h6>
                            </div>
                            <div class="card-body-neo">
                                <div class="gauge-container">
                                    <canvas id="gaugeChart"></canvas>
                                    <div class="gauge-center">
                                        <div class="gauge-val" id="gauge-val-txt">{{ data.aqi }}</div>
                                        <div class="gauge-lbl" id="gauge-cat-txt">{{ data.category }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="glass-card flex-fill">
                            <div class="card-header-neo">
                                <h6 class="card-title-neo"><i class="fa-solid fa-chart-pie"></i> Metrics Composition</h6>
                            </div>
                            <div class="card-body-neo" style="height: 170px;">
                                <canvas id="donutChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- BOTTOM ROW -->
                <div class="row g-4 mb-4">
                    <div class="col-lg-5">
                        <div class="glass-card h-100">
                            <div class="card-header-neo">
                                <h6 class="card-title-neo"><i class="fa-solid fa-chart-bar"></i> Limits Analysis</h6>
                            </div>
                            <div class="card-body-neo" style="height: 240px;">
                                <canvas id="barChart"></canvas>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-7">
                        <div class="ai-panel h-100" style="border-left: 4px solid var(--accent);">
                            <div class="ai-badge"><i class="fa-solid fa-bolt"></i> System Analysis</div>
                            <div class="ai-text">
                                The system processed the coordinates and metrics resulting in a computed AQI of <strong>{{ data.aqi }}</strong>.
                                <br><br>
                                Triggering alert for primary element: <strong id="ai-prime">--</strong>.<br>
                                <br>
                                <strong>Safety Directive:</strong> <span id="ai-advice">{{ data.advice }}</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            {% endif %}

        </div>
    </div>

    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        /* ====== API LOGIC ====== */
        const countrySel = document.getElementById("country"), stateSel = document.getElementById("state"), citySel = document.getElementById("city");
        document.addEventListener("DOMContentLoaded", () => {
            fetch("https://countriesnow.space/api/v0.1/countries/positions").then(r => r.json()).then(d => {
                if (!d.error) d.data.forEach(c => { let o = document.createElement("option"); o.value = c.name; o.text = c.name; countrySel.add(o); });
            });
        });

        function loadStates() { stateSel.innerHTML = '<option value="">... </option>'; stateSel.disabled = true; citySel.innerHTML = '<option value="">City</option>'; citySel.disabled = true; fetch("https://countriesnow.space/api/v0.1/countries/states", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ country: countrySel.value }) }).then(r => r.json()).then(d => { stateSel.innerHTML = '<option value="">Select</option>'; if (!d.error) { d.data.states.forEach(s => { let o = document.createElement("option"); o.value = s.name; o.text = s.name; stateSel.add(o) }); stateSel.disabled = false } }) }
        function loadCities() { citySel.innerHTML = '<option value="">...</option>'; citySel.disabled = true; fetch("https://countriesnow.space/api/v0.1/countries/state/cities", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ country: countrySel.value, state: stateSel.value }) }).then(r => r.json()).then(d => { citySel.innerHTML = '<option value="">Select</option>'; if (!d.error) { d.data.forEach(c => { let o = document.createElement("option"); o.value = c; o.text = c; citySel.add(o) }); citySel.disabled = false } }) }
        function getCoords() { const c = citySel.value, co = countrySel.value; if (!c) { alert("Please select a city."); return } fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + c + ',' + co).then(r => r.json()).then(d => { if (d.length > 0) { document.getElementById('lat').value = parseFloat(d[0].lat).toFixed(4); document.getElementById('lon').value = parseFloat(d[0].lon).toFixed(4) } else alert("Coordinates not found.") }) }
        function getAirQuality() { const la = document.getElementById('lat').value, lo = document.getElementById('lon').value, b = document.getElementById('btnFetch'); if (!la || !lo) { alert("Latitude and Longitude required"); return } const ot = b.innerHTML; b.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i>'; b.disabled = true; fetch('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=' + la + '&longitude=' + lo + '&current=pm10,pm2_5,nitrogen_dioxide,ozone').then(r => r.json()).then(d => { if (d.current) { document.getElementById('pm25').value = d.current.pm2_5; document.getElementById('pm10').value = d.current.pm10; document.getElementById('no2').value = d.current.nitrogen_dioxide; document.getElementById('o3').value = d.current.ozone } }).catch(() => alert("Error")).finally(() => { b.innerHTML = ot; b.disabled = false }) }
        
        /* ====== PREDICTIVE LOGIC ====== */
        {% if data %}
        const AQI = {{ data.aqi }}, COLOR = '{{data.color}}', LAT = {{ data.lat }}, LON = {{ data.lon }}, PM25 = {{ data.pm25 }}, PM10 = {{ data.pm10 }}, NO2 = {{ data.no2 }}, O3 = {{ data.o3 }}, CAT = '{{data.category}}';
        
        // Clean corporate colors instead of the previous aggressive neons
        const hexMap = {
            'green': '#059669', // Emerald
            'yellow': '#d97706', // Amber 
            'orange': '#ea580c', // Orange
            'red': '#dc2626', // Red
            'purple': '#7c3aed', // Violet
            'maroon': '#881337' // Rose
        };
        const actualColor = hexMap[COLOR] || '#0f172a';

        // Apply dynamic colors
        document.getElementById('card-aqi').style.borderLeftColor = actualColor;
        document.getElementById('icon-aqi').style.color = actualColor;
        document.getElementById('icon-aqi').style.background = actualColor + '15';
        document.getElementById('kpi-cat-text').style.color = actualColor;
        
        // Progress Bar
        const bar = document.getElementById('aqi-bar');
        bar.style.background = actualColor;
        setTimeout(() => { bar.style.width = Math.min((AQI/500)*100, 100) + '%'; }, 300);

        // Risk Level mapping
        let riskLevel = "Normal";
        if(AQI > 50) riskLevel = "Notice";
        if(AQI > 100) riskLevel = "Warning";
        if(AQI > 200) riskLevel = "Critical";
        document.getElementById('kpi-risk').textContent = riskLevel;

        const poll = { 'PM2.5': PM25, 'PM10': PM10, 'NO2': NO2, 'O3': O3 };
        let mx = 0, pn = 'PM2.5';
        Object.entries(poll).forEach(([k, v]) => { if (v > mx) { mx = v; pn = k; } });
        document.getElementById('kpi-prime').textContent = pn;
        document.getElementById('ai-prime').textContent = pn;

        Chart.defaults.color = '#64748b';
        Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
        Chart.defaults.borderColor = '#e2e8f0';
        const ttOpts = { 
            backgroundColor: '#ffffff', 
            titleColor: '#0f172a', 
            bodyColor: '#475569', 
            borderColor: '#e2e8f0',
            borderWidth: 1,
            cornerRadius: 4, 
            padding: 10,
            displayColors: true,
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        };

        // GAUGE CHART
        (function(){
            const ctx = document.getElementById('gaugeChart').getContext('2d');
            const ratio = Math.min(AQI/500, 1);
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [ratio*100, (1-ratio)*100],
                        backgroundColor: [actualColor, '#f1f5f9'],
                        borderWidth: 0,
                        borderRadius: 4
                    }]
                },
                options: {
                    rotation: -90, circumference: 180, cutout: '76%',
                    plugins: { tooltip: { enabled: false } },
                    maintainAspectRatio: false,
                    animation: { animateRotate: true }
                }
            });
        })();

        // DONUT CHART
        (function(){
            const ctx = document.getElementById('donutChart').getContext('2d');
            const colors = ['#2563eb', '#38bdf8', '#8b5cf6', '#cbd5e1']; // Clean business colors
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(poll),
                    datasets: [{
                        data: Object.values(poll),
                        backgroundColor: colors,
                        borderColor: '#ffffff',
                        borderWidth: 2
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { usePointStyle: true, boxWidth: 6, color: '#334155', font: {size:10} } },
                        tooltip: ttOpts
                    },
                    cutout: '70%'
                }
            });
        })();

        // BAR CHART
        (function(){
            const ctx = document.getElementById('barChart').getContext('2d');
            const who = [15, 45, 25, 100];
            const dataVals = Object.values(poll);
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(poll),
                    datasets: [
                        { label: 'Reading', data: dataVals, backgroundColor: '#2563eb', borderRadius: 4, barPercentage: 0.5 },
                        { label: 'Reference Limit', data: who, backgroundColor: '#94a3b8', borderRadius: 4, barPercentage: 0.5 }
                    ]
                },
                options: {
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false } },
                        y: { beginAtZero: true }
                    },
                    plugins: { tooltip: ttOpts, legend: { position: 'top', labels: {usePointStyle: true, boxWidth:6, font:{size:10}} } }
                }
            });
        })();

        // MAP - Clean Light POSITRON Theme
        setTimeout(() => {
            const m = L.map('map', { zoomControl: false }).setView([LAT, LON], 12);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; CartoDB',
                maxZoom: 19
            }).addTo(m);
            
            L.circle([LAT, LON], {
                color: actualColor,
                fillColor: actualColor,
                fillOpacity: 0.2,
                radius: 3000,
                weight: 2
            }).addTo(m);

            const iconHtml = `<div style="background:#fff;width:14px;height:14px;border-radius:50%;border:3px solid ${actualColor};box-shadow:0 1px 3px rgba(0,0,0,0.3)"></div>`;
            const customIcon = L.divIcon({ html: iconHtml, className: '', iconSize: [14,14], iconAnchor: [7,7] });
            
            L.marker([LAT, LON], {icon: customIcon}).addTo(m);
        }, 300);

        {% endif %}
    </script>
</body>
</html>
"""

with open(r"c:\Users\Admin\Desktop\Airpollution\main\templates\prediction.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Template written successfully!")
