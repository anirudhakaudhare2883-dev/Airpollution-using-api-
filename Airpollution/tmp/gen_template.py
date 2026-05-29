import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AQI Intelligence Dashboard | Enterprise Analytics</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #0a0a0a;
            --bg-nav: rgba(10, 10, 10, 0.85);
            --bg-card: rgba(20, 20, 22, 0.65);
            --border: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(139, 92, 246, 0.4);
            --accent: #8b5cf6;
            --accent-sec: #3b82f6;
            --t-main: #ffffff;
            --t-mut: #a1a1aa;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --purple: #8b5cf6;
            --blue: #3b82f6;
            --glass-blur: blur(16px);
            --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            --glow: 0 0 20px rgba(139, 92, 246, 0.2);
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--t-main);
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.05), transparent 30%),
                radial-gradient(circle at 85% 30%, rgba(59, 130, 246, 0.05), transparent 30%);
        }

        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255,255,255,0.2);
        }

        /* NAVBAR */
        .pn {
            background: var(--bg-nav);
            backdrop-filter: var(--glass-blur);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .pn .inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.8rem 2rem;
        }
        .nb {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            text-decoration: none;
        }
        .nb-i {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--blue), var(--accent));
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 1.1rem;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        }
        .nb-t {
            font-weight: 700;
            font-size: 1.1rem;
            color: var(--t-main);
            letter-spacing: 0.5px;
        }
        .nb-s {
            font-size: 0.65rem;
            color: var(--t-mut);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .bh {
            background: rgba(255,255,255,0.05);
            color: #fff;
            border: 1px solid var(--border);
            padding: 0.4rem 1rem;
            border-radius: 8px;
            font-size: 0.8rem;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .bh:hover {
            background: rgba(255,255,255,0.1);
            color: #fff;
        }

        /* LAYOUT */
        .dw {
            padding: 2rem;
            max-width: 1600px;
            margin: 0 auto;
        }

        /* CARDS */
        .glass-card {
            background: var(--bg-card);
            backdrop-filter: var(--glass-blur);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        .glass-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            opacity: 0;
            transition: opacity 0.4s;
        }
        .glass-card:hover {
            transform: translateY(-2px);
            border-color: var(--border-highlight);
            box-shadow: var(--glow);
        }
        .glass-card:hover::before {
            opacity: 1;
        }
        
        .card-header-neo {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .card-title-neo {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--t-mut);
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0;
        }
        .card-title-neo i {
            color: var(--accent);
            font-size: 1rem;
        }
        .card-body-neo {
            padding: 1.25rem;
        }

        /* FORM STYLING (To match dark theme) */
        .form-label-neo {
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--t-mut);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
        }
        .form-control-neo, .form-select-neo {
            background: rgba(0,0,0,0.3);
            border: 1px solid var(--border);
            color: #fff;
            border-radius: 8px;
            padding: 0.6rem;
            font-size: 0.85rem;
            transition: all 0.3s;
        }
        .form-control-neo:focus, .form-select-neo:focus {
            background: rgba(0,0,0,0.5);
            border-color: var(--accent);
            color: #fff;
            box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
            outline: none;
        }
        .form-select-neo option {
            background: var(--bg);
            color: #fff;
        }
        .input-group-text-neo {
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            color: var(--t-mut);
            border-right: none;
            font-size: 0.8rem;
        }
        .input-group .form-control-neo { border-left: none; }
        
        .btn-neo-primary {
            background: linear-gradient(135deg, var(--accent), var(--blue));
            color: #fff;
            border: none;
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
        }
        .btn-neo-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
            color: #fff;
        }
        .btn-neo-sec {
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--border);
            color: var(--t-main);
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
        .btn-neo-sec:hover {
            background: rgba(255,255,255,0.1);
            border-color: var(--t-mut);
            color: #fff;
        }

        /* ------------------ DASHBOARD (OUTPUT) ------------------ */
        .dash-top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            animation: fadeIn 0.5s ease;
        }
        .dash-title {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(to right, #fff, var(--t-mut));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        .dash-actions {
            display: flex;
            gap: 1rem;
        }
        .btn-dash-action {
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.3);
            color: #d8b4fe;
            padding: 0.5rem 1.25rem;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.3s;
            cursor: pointer;
        }
        .btn-dash-action:hover {
            background: var(--accent);
            color: #fff;
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
            transform: translateY(-1px);
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
            backdrop-filter: var(--glass-blur);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        .kpi-card:hover {
            transform: translateY(-3px);
            border-color: var(--border-highlight);
            box-shadow: var(--glow);
        }
        .kpi-icon {
            width: 46px;
            height: 46px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            flex-shrink: 0;
        }
        .kpi-content {
            flex: 1;
        }
        .kpi-label {
            font-size: 0.72rem;
            color: var(--t-mut);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.2rem;
        }
        .kpi-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.4rem;
            font-weight: 700;
            color: #fff;
            line-height: 1.1;
        }

        /* MAIN VISUALS */
        .main-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        /* Map styling */
        #map {
            height: 400px;
            width: 100%;
            border-radius: 12px;
            z-index: 1;
            background: #000;
        }
        .leaflet-popup-content-wrapper {
            background: rgba(20,20,22,0.95) !important;
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-highlight);
            color: #fff !important;
            border-radius: 8px !important;
            box-shadow: 0 0 20px rgba(0,0,0,0.8) !important;
        }
        .leaflet-popup-tip {
            background: rgba(20,20,22,0.95) !important;
        }

        /* GAUGE */
        .gauge-container {
            position: relative;
            height: 160px;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            margin-bottom: 0.5rem;
        }
        .gauge-center {
            position: absolute;
            bottom: 0;
            text-align: center;
            transform: translateY(10%);
        }
        .gauge-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1;
            text-shadow: 0 0 20px currentColor;
        }
        .gauge-lbl {
            font-size: 0.75rem;
            color: var(--t-mut);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
        }

        /* AI INSIGHTS */
        .ai-panel {
            background: linear-gradient(135deg, rgba(20,20,22,0.8), rgba(139, 92, 246, 0.08));
            border-left: 4px solid var(--accent);
            padding: 1.5rem;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }
        .ai-panel::before {
            content: '\\f0e7';
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            right: -10px;
            bottom: -20px;
            font-size: 6rem;
            opacity: 0.05;
            color: var(--accent);
        }
        .ai-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(139, 92, 246, 0.2);
            color: #c4b5fd;
            padding: 0.3rem 0.8rem;
            border-radius: 30px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1rem;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }
        .ai-text {
            font-size: 0.95rem;
            line-height: 1.6;
            color: #d1d5db;
            font-weight: 300;
        }
        .ai-text strong {
            color: #fff;
            font-weight: 600;
        }

        /* ANIMATIONS */
        .anim-up {
            opacity: 0;
            transform: translateY(20px);
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @keyframes slideUp {
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .d-1 { animation-delay: 0.1s; }
        .d-2 { animation-delay: 0.15s; }
        .d-3 { animation-delay: 0.2s; }
        .d-4 { animation-delay: 0.25s; }
        .d-5 { animation-delay: 0.35s; }
        .d-6 { animation-delay: 0.45s; }
        
        /* SKELETON PRELOADER */
        .skeleton-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(10,10,10,0.85);
            z-index: 50;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 1;
            transition: opacity 0.5s;
        }
        .skeleton-overlay.hide {
            opacity: 0;
            pointer-events: none;
        }
        .loader {
            width: 40px;
            height: 40px;
            border: 3px solid rgba(139, 92, 246, 0.2);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }

        /* AQI PROGRESS BAR */
        .progress-bar-container {
            width: 100%;
            height: 6px;
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            margin-top: 0.6rem;
            overflow: hidden;
            position: relative;
        }
        .progress-bar-fill {
            height: 100%;
            border-radius: 10px;
            width: 0%;
            transition: width 1.5s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* RESPONSIVE */
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

    <!-- NAVBAR -->
    <nav class="pn">
        <div class="inner">
            <a class="nb" href="#">
                <div class="nb-i"><i class="fa-solid fa-atom"></i></div>
                <div>
                    <div class="nb-t">AQInsights</div>
                    <div class="nb-s">Enterprise Air Quality Analytics</div>
                </div>
            </a>
            <div class="d-flex align-items-center gap-3">
                <a href="/" class="bh"><i class="fa-solid fa-arrow-left me-2"></i>Exit Dashboard</a>
            </div>
        </div>
    </nav>

    <div class="dw">
        <div class="row g-4">
            
            <!-- INPUT PANEL -->
            <div class="{% if data %}col-xl-3{% else %}col-xl-5 mx-auto mt-4{% endif %}">
                <div class="glass-card anim-up">
                    <div class="card-header-neo">
                        <h6 class="card-title-neo"><i class="fa-solid fa-satellite-dish"></i> Data Ingestion</h6>
                    </div>
                    <div class="card-body-neo">
                        <form method="POST" id="aqiForm">
                            <label class="form-label-neo">Location Mapping</label>
                            <select id="country" class="form-control form-select-neo mb-2" onchange="loadStates()">
                                <option value="">Select Country</option>
                            </select>
                            <div class="row g-2 mb-2">
                                <div class="col-6"><select id="state" class="form-control form-select-neo" onchange="loadCities()" disabled><option value="">State</option></select></div>
                                <div class="col-6"><select id="city" class="form-control form-select-neo" disabled><option value="">City</option></select></div>
                            </div>
                            <button type="button" onclick="getCoords()" class="btn-neo-sec w-100 mb-3" style="font-size:0.75rem;"><i class="fa-solid fa-location-crosshairs me-1"></i> Auto-Detect Coordinates</button>
                            
                            <hr style="border-color:var(--border);">

                            <div class="row g-2 mb-3">
                                <div class="col-6"><label class="form-label-neo">Latitude</label><input type="text" id="lat" name="lat" class="form-control form-control-neo" placeholder="0.0000" required readonly></div>
                                <div class="col-6"><label class="form-label-neo">Longitude</label><input type="text" id="lon" name="lon" class="form-control form-control-neo" placeholder="0.0000" required readonly></div>
                            </div>

                            <label class="form-label-neo mt-2">Sensor Telemetry (µg/m³)</label>
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
                                <button type="button" id="btnFetch" onclick="getAirQuality()" class="btn-neo-sec"><i class="fa-solid fa-cloud-arrow-down me-1"></i> Retrieve Live API Data</button>
                                <button type="submit" class="btn-neo-primary" id="btnPredict"><i class="fa-solid fa-bolt me-1"></i> Generate Prediction</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            {% if data %}
            <!-- DASHBOARD OUTPUT -->
            <div class="col-xl-9">
                
                <div class="dash-top-bar">
                    <h1 class="dash-title">Predictive AQI Analytics</h1>
                    <div class="dash-actions">
                        <button class="btn-dash-action" onclick="window.print()"><i class="fa-solid fa-file-pdf me-1"></i> Export Report</button>
                    </div>
                </div>

                <!-- KPIs -->
                <div class="kpi-grid">
                    <div class="kpi-card anim-up d-1">
                        <div class="kpi-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
                            <i class="fa-solid fa-wind"></i>
                        </div>
                        <div class="kpi-content">
                            <div class="kpi-label">Overall AQI</div>
                            <div class="kpi-val" id="kpi-aqi">{{ data.aqi }}</div>
                            <div class="progress-bar-container"><div class="progress-bar-fill" id="aqi-bar"></div></div>
                        </div>
                    </div>
                    
                    <div class="kpi-card anim-up d-2">
                        <div class="kpi-icon" id="icon-cat">
                            <i class="fa-solid fa-shield-halved"></i>
                        </div>
                        <div class="kpi-content">
                            <div class="kpi-label">Health Category</div>
                            <div class="kpi-val" style="font-size: 1.1rem; font-family: 'Inter'; line-height: 1.2; margin-top:4px;">{{ data.category }}</div>
                        </div>
                    </div>

                    <div class="kpi-card anim-up d-3">
                        <div class="kpi-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;">
                            <i class="fa-solid fa-biohazard"></i>
                        </div>
                        <div class="kpi-content">
                            <div class="kpi-label">Critical Pollutant</div>
                            <div class="kpi-val" id="kpi-prime" style="font-size: 1.3rem;">--</div>
                        </div>
                    </div>

                    <div class="kpi-card anim-up d-4">
                        <div class="kpi-icon" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6;">
                            <i class="fa-solid fa-heart-pulse"></i>
                        </div>
                        <div class="kpi-content">
                            <div class="kpi-label">Risk Level</div>
                            <div class="kpi-val" id="kpi-risk" style="font-size: 1.1rem; font-family: 'Inter'; line-height: 1.2; margin-top:4px;">Evaluating...</div>
                        </div>
                    </div>
                </div>

                <!-- MAIN VISUALS -->
                <div class="main-grid">
                    <!-- LEFT: MAP -->
                    <div class="glass-card anim-up d-5" style="position:relative;">
                        <div class="card-header-neo">
                            <h6 class="card-title-neo"><i class="fa-solid fa-map-location-dot"></i> Geospatial Intelligence</h6>
                        </div>
                        <div class="card-body-neo p-2">
                            <div id="map"></div>
                        </div>
                        <div class="skeleton-overlay" id="map-skel"><div class="loader"></div></div>
                    </div>

                    <!-- RIGHT: GAUGE & DONUT -->
                    <div class="d-flex flex-column gap-3 h-100">
                        <div class="glass-card anim-up d-6 flex-fill">
                            <div class="card-header-neo border-0 pb-0">
                                <h6 class="card-title-neo"><i class="fa-solid fa-tachometer-alt"></i> Severity Index</h6>
                            </div>
                            <div class="card-body-neo pt-1 pb-2">
                                <div class="gauge-container">
                                    <canvas id="gaugeChart"></canvas>
                                    <div class="gauge-center">
                                        <div class="gauge-val" id="gauge-val-txt">{{ data.aqi }}</div>
                                        <div class="gauge-lbl" id="gauge-cat-txt" style="font-family:'Inter';font-weight:600;color:#fff;">{{ data.category }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="glass-card anim-up d-6 flex-fill">
                            <div class="card-header-neo border-0 pb-0">
                                <h6 class="card-title-neo"><i class="fa-solid fa-chart-pie"></i> Pollutant Distribution</h6>
                            </div>
                            <div class="card-body-neo" style="height: 180px; padding-top: 5px;">
                                <canvas id="donutChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- BOTTOM ROW: CHARTS & AI -->
                <div class="row g-4 mb-4">
                    <div class="col-lg-4">
                        <div class="glass-card anim-up d-5 h-100">
                            <div class="card-header-neo">
                                <h6 class="card-title-neo"><i class="fa-solid fa-chart-column"></i> Concentration vs WHO</h6>
                            </div>
                            <div class="card-body-neo" style="height: 250px;">
                                <canvas id="barChart"></canvas>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-lg-4">
                        <div class="glass-card anim-up d-5 h-100">
                            <div class="card-header-neo">
                                <h6 class="card-title-neo"><i class="fa-solid fa-chart-line"></i> 24H Trend Simulation</h6>
                            </div>
                            <div class="card-body-neo" style="height: 250px;">
                                <canvas id="lineChart"></canvas>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-4">
                        <div class="ai-panel anim-up d-6 h-100">
                            <div class="ai-badge"><i class="fa-solid fa-robot"></i> AI Engine Insights</div>
                            <div class="ai-text">
                                The predictive model calculates the Air Quality Index at <strong style="color:var(--t-main)" id="ai-aqi">{{ data.aqi }}</strong> based on real-time telemetry.
                                <br><br>
                                The primary driver is <strong id="ai-prime">--</strong>.<br>
                                <br>
                                <strong>Advisory:</strong> <span id="ai-advice">{{ data.advice }}</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            {% endif %}

        </div>
    </div>

    <!-- Scripts -->
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        /* ====== API LOGIC ====== */
        const countrySel = document.getElementById("country"), stateSel = document.getElementById("state"), citySel = document.getElementById("city");
        document.addEventListener("DOMContentLoaded", () => {
            fetch("https://countriesnow.space/api/v0.1/countries/positions").then(r => r.json()).then(d => {
                if (!d.error) d.data.forEach(c => { let o = document.createElement("option"); o.value = c.name; o.text = c.name; countrySel.add(o); });
            });
            
            {% if data %}
            // Remove skeleton after slightly delayed load effect
            setTimeout(() => {
                const skel = document.getElementById('map-skel');
                if(skel) skel.classList.add('hide');
            }, 800);
            {% endif %}
        });

        function loadStates() { stateSel.innerHTML = '<option value="">Loading...</option>'; stateSel.disabled = true; citySel.innerHTML = '<option value="">City</option>'; citySel.disabled = true; fetch("https://countriesnow.space/api/v0.1/countries/states", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ country: countrySel.value }) }).then(r => r.json()).then(d => { stateSel.innerHTML = '<option value="">Select State</option>'; if (!d.error) { d.data.states.forEach(s => { let o = document.createElement("option"); o.value = s.name; o.text = s.name; stateSel.add(o) }); stateSel.disabled = false } }) }
        function loadCities() { citySel.innerHTML = '<option value="">Loading...</option>'; citySel.disabled = true; fetch("https://countriesnow.space/api/v0.1/countries/state/cities", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ country: countrySel.value, state: stateSel.value }) }).then(r => r.json()).then(d => { citySel.innerHTML = '<option value="">Select City</option>'; if (!d.error) { d.data.forEach(c => { let o = document.createElement("option"); o.value = c; o.text = c; citySel.add(o) }); citySel.disabled = false } }) }
        function getCoords() { const c = citySel.value, co = countrySel.value; if (!c) { alert("Please select a city first."); return } fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + c + ',' + co).then(r => r.json()).then(d => { if (d.length > 0) { document.getElementById('lat').value = parseFloat(d[0].lat).toFixed(4); document.getElementById('lon').value = parseFloat(d[0].lon).toFixed(4) } else alert("Coordinates not found.") }) }
        function getAirQuality() { const la = document.getElementById('lat').value, lo = document.getElementById('lon').value, b = document.getElementById('btnFetch'); if (!la || !lo) { alert("Latitude and Longitude required."); return } const ot = b.innerHTML; b.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i>Fetching...'; b.disabled = true; fetch('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=' + la + '&longitude=' + lo + '&current=pm10,pm2_5,nitrogen_dioxide,ozone').then(r => r.json()).then(d => { if (d.current) { document.getElementById('pm25').value = d.current.pm2_5; document.getElementById('pm10').value = d.current.pm10; document.getElementById('no2').value = d.current.nitrogen_dioxide; document.getElementById('o3').value = d.current.ozone } }).catch(() => alert("Error fetching data")).finally(() => { b.innerHTML = ot; b.disabled = false }) }
        
        /* ====== PREDICTIVE DASHBOARD LOGIC ====== */
        {% if data %}
        
        const AQI = {{ data.aqi }}, COLOR = '{{data.color}}', LAT = {{ data.lat }}, LON = {{ data.lon }}, PM25 = {{ data.pm25 }}, PM10 = {{ data.pm10 }}, NO2 = {{ data.no2 }}, O3 = {{ data.o3 }}, CAT = '{{data.category}}';
        
        const hexMap = {
            'green': '#10b981',
            'yellow': '#f59e0b',
            'orange': '#f97316',
            'red': '#ef4444',
            'purple': '#8b5cf6',
            'maroon': '#9f1239'
        };
        const actualColor = hexMap[COLOR] || '#8b5cf6';

        // Apply dynamic colors to text and icons
        document.getElementById('kpi-aqi').style.color = actualColor;
        document.getElementById('gauge-val-txt').style.color = actualColor;
        document.getElementById('icon-cat').style.background = actualColor + '20';
        document.getElementById('icon-cat').style.color = actualColor;
        
        // AQI Progress Bar
        const bar = document.getElementById('aqi-bar');
        bar.style.background = actualColor;
        bar.style.boxShadow = '0 0 10px ' + actualColor;
        setTimeout(() => { bar.style.width = Math.min((AQI/500)*100, 100) + '%'; }, 500);

        // Risk Level mapping
        let riskLevel = "Minimal Risk";
        if(AQI > 50) riskLevel = "Moderate Risk";
        if(AQI > 100) riskLevel = "High Risk";
        if(AQI > 200) riskLevel = "Severe Risk";
        document.getElementById('kpi-risk').textContent = riskLevel;
        document.getElementById('kpi-risk').style.color = actualColor;

        // Primary Pollutant detection
        const poll = { 'PM2.5': PM25, 'PM10': PM10, 'NO₂': NO2, 'O₃': O3 };
        let mx = 0, pn = 'PM2.5';
        Object.entries(poll).forEach(([k, v]) => { if (v > mx) { mx = v; pn = k; } });
        document.getElementById('kpi-prime').textContent = pn;
        document.getElementById('ai-prime').textContent = pn;

        // Chart.js global defaults
        Chart.defaults.color = '#a1a1aa';
        Chart.defaults.font.family = "'Inter', sans-serif";
        Chart.defaults.borderColor = 'rgba(255,255,255,0.05)';
        const ttOpts = { 
            backgroundColor: 'rgba(10,10,10,0.9)', 
            titleColor: '#fff', 
            bodyColor: '#e2e8f0', 
            borderColor: 'rgba(139, 92, 246, 0.3)',
            borderWidth: 1,
            cornerRadius: 8, 
            padding: 12,
            displayColors: true 
        };

        // 1. GAUGE CHART
        (function(){
            const ctx = document.getElementById('gaugeChart').getContext('2d');
            const ratio = Math.min(AQI/500, 1);
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [ratio*100, (1-ratio)*100],
                        backgroundColor: [actualColor, 'rgba(255,255,255,0.05)'],
                        borderWidth: 0,
                        borderRadius: 20
                    }]
                },
                options: {
                    rotation: -90, circumference: 180, cutout: '82%',
                    plugins: { tooltip: { enabled: false } },
                    maintainAspectRatio: false,
                    animation: { animateRotate: true, duration: 2000, easing: 'easeOutQuart' }
                }
            });
        })();

        // 2. DONUT CHART
        (function(){
            const ctx = document.getElementById('donutChart').getContext('2d');
            const colors = ['#f59e0b', '#3b82f6', '#8b5cf6', '#10b981'];
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(poll),
                    datasets: [{
                        data: Object.values(poll),
                        backgroundColor: colors.map(c => c+'d0'),
                        borderColor: '#141416',
                        borderWidth: 2,
                        hoverOffset: 6
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { usePointStyle: true, boxWidth: 8, color: '#e2e8f0', font: {size:10} } },
                        tooltip: ttOpts
                    },
                    cutout: '65%'
                }
            });
        })();

        // 3. BAR CHART (vs WHO)
        (function(){
            const ctx = document.getElementById('barChart').getContext('2d');
            const who = [15, 45, 25, 100]; // WHO guideline limits
            const dataVals = Object.values(poll);
            
            const gradientActual = ctx.createLinearGradient(0,0,0,250);
            gradientActual.addColorStop(0, 'rgba(139, 92, 246, 0.9)');
            gradientActual.addColorStop(1, 'rgba(59, 130, 246, 0.4)');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(poll),
                    datasets: [
                        { label: 'Current Level', data: dataVals, backgroundColor: gradientActual, borderRadius: 6, barPercentage: 0.6 },
                        { label: 'WHO Limit', data: who, backgroundColor: 'rgba(16, 185, 129, 0.15)', borderColor: '#10b981', borderWidth: 1, borderRadius: 6, barPercentage: 0.6, borderDash: [4,4] }
                    ]
                },
                options: {
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false } },
                        y: { beginAtZero: true, border: {dash: [4,4]} }
                    },
                    plugins: { tooltip: ttOpts, legend: { position: 'top', labels: {usePointStyle: true, font:{size:10}} } }
                }
            });
        })();

        // 4. LINE CHART (24H Trend Simulation)
        (function(){
            const ctx = document.getElementById('lineChart').getContext('2d');
            const labels = ['-5h','-4h','-3h','-2h','-1h','Now'];
            
            // Random walk simulation based on current AQI
            let trend = [];
            for(let i=5; i>0; i--) {
                const noise = (Math.random() - 0.5) * 30;
                trend.push(Math.max(0, Math.round(AQI + noise)));
            }
            trend.push(AQI);

            const gradient = ctx.createLinearGradient(0,0,0,200);
            gradient.addColorStop(0, actualColor + '60');
            gradient.addColorStop(1, actualColor + '00');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'AQI Trend',
                        data: trend,
                        borderColor: actualColor,
                        backgroundColor: gradient,
                        borderWidth: 3,
                        pointBackgroundColor: '#0a0a0a',
                        pointBorderColor: actualColor,
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false } },
                        y: { border: {dash: [4,4]} }
                    },
                    plugins: { tooltip: ttOpts, legend: { display: false } }
                }
            });
        })();

        // 5. MAP WITH LEAFLET
        setTimeout(() => {
            const m = L.map('map', { zoomControl: false }).setView([LAT, LON], 12);
            
            // CartoDB Dark Matter tiles
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; CartoDB',
                maxZoom: 19
            }).addTo(m);
            
            // Glowing radius
            L.circle([LAT, LON], {
                color: actualColor,
                fillColor: actualColor,
                fillOpacity: 0.15,
                radius: 3500,
                weight: 1
            }).addTo(m);

            // Custom Marker
            const iconHtml = `<div style="background:${actualColor};width:16px;height:16px;border-radius:50%;box-shadow:0 0 20px ${actualColor};border:2px solid #fff;"></div>`;
            const customIcon = L.divIcon({ html: iconHtml, className: '', iconSize: [16,16], iconAnchor: [8,8] });
            
            const popupHtml = `
                <div style="text-align:center;padding:5px;">
                    <h6 style="margin:0;color:${actualColor};font-weight:700;">AQI: ${AQI}</h6>
                    <small style="color:#e2e8f0;font-weight:600;">${CAT}</small>
                </div>
            `;
            L.marker([LAT, LON], {icon: customIcon}).addTo(m).bindPopup(popupHtml).openPopup();

        }, 500);

        {% endif %}
    </script>
</body>
</html>
"""

with open(r"c:\Users\Admin\Desktop\Airpollution\main\templates\prediction.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Template written successfully!")
