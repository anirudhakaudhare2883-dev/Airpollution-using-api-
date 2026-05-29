import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AirQuality AI | Premium Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            /* Metallic Gray + Crimson Premium Theme */
            --bg-base: #0a0a0c;
            --bg-nav: rgba(15, 15, 18, 0.85);
            --bg-card: rgba(20, 20, 24, 0.6);
            --border: rgba(255, 255, 255, 0.04);
            --border-highlight: rgba(239, 68, 68, 0.4);
            --accent: #ef4444; /* Crimson Red */
            --accent-sec: #9f1239; /* Deep Ruby */
            --accent-light: #fda4af; /* Rose Light */
            --t-main: #f4f4f5;
            --t-mut: #a1a1aa;
            
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.6), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
            --glass-blur: blur(16px);
            --radius: 12px;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-base);
            color: var(--t-main);
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 50%, rgba(239, 68, 68, 0.04), transparent 40%),
                radial-gradient(circle at 90% 30%, rgba(159, 18, 57, 0.07), transparent 40%);
        }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-base); }
        ::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #52525b; }

        /* NAVBAR */
        .pn {
            background: var(--bg-nav);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .pn .inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.8rem 2.5rem;
            max-width: 1600px;
            margin: 0 auto;
        }
        .nb {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }
        .nb-i {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--accent), var(--accent-sec));
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 1.3rem;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
        }
        .nb-t {
            font-weight: 800;
            font-size: 1.25rem;
            color: #fff;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .bh {
            background: rgba(255,255,255,0.03);
            color: var(--t-mut);
            border: 1px solid var(--border);
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .bh:hover {
            background: rgba(239, 68, 68, 0.1);
            color: #fff;
            border-color: rgba(239, 68, 68, 0.3);
        }

        /* LAYOUT */
        .dw {
            padding: 2.5rem;
            max-width: 1600px;
            margin: 0 auto;
        }

        /* CARDS */
        .glass-card {
            background: linear-gradient(160deg, rgba(24, 24, 27, 0.6), rgba(10, 10, 12, 0.8));
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid rgba(63, 63, 70, 0.4);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        .glass-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(239,68,68,0.2), transparent);
        }
        .glass-card:hover {
            border-color: rgba(239, 68, 68, 0.3);
            transform: translateY(-4px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.7), 0 0 20px rgba(239, 68, 68, 0.1);
        }
        
        .card-header-neo {
            padding: 1.2rem 1.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.03);
            background: rgba(0,0,0,0.3);
        }
        .card-title-neo {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--t-mut);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .card-title-neo i {
            color: var(--accent);
            font-size: 0.9rem;
        }
        .card-body-neo {
            padding: 1.5rem;
        }

        /* FORM STYLING */
        .form-label-neo {
            font-size: 0.7rem;
            font-weight: 500;
            color: var(--t-mut);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.4rem;
        }
        .form-control-neo, .form-select-neo {
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(63, 63, 70, 0.6);
            color: #fff;
            border-radius: 6px;
            padding: 0.6rem 0.8rem;
            font-size: 0.9rem;
            font-family: inherit;
            transition: all 0.2s;
        }
        .form-control-neo:focus, .form-select-neo:focus {
            border-color: var(--accent);
            background: rgba(0,0,0,0.6);
            box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
            color: #fff;
            outline: none;
        }
        .form-control-neo::placeholder { color: #52525b; }
        
        .input-group-text-neo {
            background: rgba(24, 24, 27, 0.8);
            border: 1px solid rgba(63, 63, 70, 0.6);
            color: var(--accent);
            border-right: none;
            font-size: 0.8rem;
            font-weight: 700;
        }
        .input-group .form-control-neo { border-left: none; }
        
        .btn-neo-primary {
            background: linear-gradient(135deg, var(--accent), var(--accent-sec));
            color: #fff;
            border: none;
            padding: 0.8rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.9rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
        }
        .btn-neo-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.5);
            color: #fff;
        }
        .btn-neo-sec {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(63, 63, 70, 0.6);
            color: var(--t-main);
            padding: 0.8rem;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .btn-neo-sec:hover {
            background: rgba(255,255,255,0.08);
            border-color: rgba(255,255,255,0.2);
            color: #fff;
        }

        /* ------------------ DASHBOARD (OUTPUT) ------------------ */
        .dash-top-bar {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 2rem;
        }
        .dash-title {
            font-size: 2rem;
            font-weight: 300;
            color: #fff;
            margin: 0;
            letter-spacing: -0.5px;
        }
        .dash-title strong { font-weight: 800; color: var(--accent); }
        
        .dash-actions {
            display: flex;
            gap: 1rem;
        }
        .btn-dash-action {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: var(--t-mut);
            padding: 0.5rem 1.2rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        .btn-dash-action:hover {
            background: rgba(255,255,255,0.1);
            color: #fff;
        }

        /* KPI CARDS */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .kpi-card {
            background: linear-gradient(145deg, rgba(39, 39, 42, 0.3) 0%, rgba(24, 24, 27, 0.5) 100%);
            border: 1px solid rgba(63, 63, 70, 0.6);
            border-radius: var(--radius);
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
            position: relative;
            overflow: hidden;
            transition: 0.3s;
        }
        .kpi-card:hover {
            border-color: rgba(239, 68, 68, 0.3);
            transform: translateY(-4px);
        }
        .kpi-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .kpi-label {
            font-size: 0.75rem;
            color: var(--t-mut);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .kpi-icon {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            background: rgba(239, 68, 68, 0.1);
            color: var(--accent);
            border: 1px solid rgba(239, 68, 68, 0.2);
        }
        .kpi-val {
            font-size: 2.4rem;
            font-weight: 800;
            color: #fff;
            line-height: 1;
            font-feature-settings: "tnum";
            text-shadow: 0 0 20px rgba(255,255,255,0.1);
        }
        
        .kpi-glow-bar {
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
            background: var(--accent);
            opacity: 0.7;
        }

        /* MAIN VISUALS */
        .main-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        #map {
            height: 100%;
            min-height: 400px;
            width: 100%;
            border-radius: 8px;
            z-index: 1;
            filter: invert(100%) hue-rotate(180deg) brightness(85%) contrast(110%) grayscale(60%) sepia(20%) hue-rotate(-20deg);
        }

        /* GAUGE */
        .gauge-container {
            position: relative;
            height: 220px;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            padding-bottom: 10px;
        }
        .gauge-center {
            position: absolute;
            bottom: 10px;
            text-align: center;
        }
        .gauge-val {
            font-size: 3.5rem;
            font-weight: 900;
            line-height: 1;
            color: #fff;
            text-shadow: 0 0 30px rgba(239, 68, 68, 0.3);
        }
        .gauge-lbl {
            font-size: 0.9rem;
            color: var(--t-mut);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 8px;
        }

        /* AI INSIGHTS */
        .ai-panel {
            background: linear-gradient(to right, rgba(24, 24, 27, 0.7), rgba(15, 15, 18, 0.5));
            border: 1px solid rgba(239, 68, 68, 0.2);
            padding: 2.5rem;
            border-radius: var(--radius);
            position: relative;
            overflow: hidden;
        }
        .ai-panel::after {
            content: '';
            position: absolute;
            top: 0; right: 0;
            width: 150px; height: 150px;
            background: radial-gradient(circle, rgba(239, 68, 68, 0.15), transparent 70%);
            pointer-events: none;
        }
        .ai-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(239, 68, 68, 0.1);
            color: var(--accent);
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            border: 1px solid rgba(239, 68, 68, 0.3);
            margin-bottom: 1.5rem;
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
        }
        .ai-text {
            font-size: 1.05rem;
            line-height: 1.7;
            color: #e4e4e7;
            font-weight: 300;
        }
        .ai-text strong { font-weight: 600; color: #fff; }

        /* CHATBOT STYLES (Red Premium theme) */
        #chatbot-fab {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 65px;
            height: 65px;
            background: linear-gradient(135deg, var(--accent), var(--accent-sec));
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4);
            cursor: pointer;
            z-index: 9999;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 2px solid rgba(255,255,255,0.1);
        }
        #chatbot-fab:hover {
            transform: scale(1.1) translateY(-5px);
            box-shadow: 0 15px 35px rgba(239, 68, 68, 0.6);
            border-color: rgba(255,255,255,0.3);
        }
        #chatbot-window {
            position: fixed;
            bottom: 100px;
            right: 2rem;
            width: 400px;
            height: 550px;
            background: rgba(15, 15, 18, 0.95);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 16px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.7), 0 0 30px rgba(239, 68, 68, 0.1);
            display: none;
            flex-direction: column;
            z-index: 9998;
            overflow: hidden;
            transform-origin: bottom right;
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        @keyframes popIn {
            0% { opacity: 0; transform: scale(0.8) translateY(30px); }
            100% { opacity: 1; transform: scale(1) translateY(0); }
        }
        #chatbot-window.open { display: flex; }
        
        .chat-header {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(159, 18, 57, 0.2));
            border-bottom: 1px solid rgba(239, 68, 68, 0.3);
            padding: 1.2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chat-header span {
            font-weight: 700;
            color: #fff;
            letter-spacing: 1px;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
        }
        .chat-header i.fa-robot { color: var(--accent); font-size: 1.2rem; }
        .chat-header button {
            background: none; border: none; color: var(--t-mut);
            cursor: pointer; font-size: 1.3rem; transition: 0.2s;
        }
        .chat-header button:hover { color: #fff; transform: rotate(90deg); }
        
        .chat-body {
            flex: 1;
            padding: 1.5rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .chat-input-area {
            padding: 1.2rem;
            background: rgba(0,0,0,0.3);
            border-top: 1px solid rgba(255,255,255,0.05);
            display: flex;
            gap: 12px;
        }
        .chat-input-area input {
            flex: 1;
            padding: 0.8rem 1.2rem;
            background: rgba(24, 24, 27, 0.8);
            border: 1px solid rgba(63, 63, 70, 0.6);
            color: #fff;
            border-radius: 12px;
            font-size: 0.95rem;
            outline: none;
            transition: 0.2s;
        }
        .chat-input-area input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
        }
        .chat-input-area button {
            background: linear-gradient(135deg, var(--accent), var(--accent-sec));
            color: #fff;
            border: none;
            width: 48px;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.2s;
            font-size: 1.2rem;
        }
        .chat-input-area button:hover { transform: scale(1.05); box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }
        
        .msg { max-width: 85%; padding: 1rem 1.2rem; border-radius: 14px; font-size: 0.95rem; line-height: 1.5; }
        .msg.bot { 
            background: rgba(39, 39, 42, 0.5); 
            border: 1px solid rgba(63, 63, 70, 0.6); 
            color: #e4e4e7; 
            align-self: flex-start;  
            border-bottom-left-radius: 4px;
        }
        .msg.user { 
            background: linear-gradient(135deg, var(--accent), var(--accent-sec));
            color: #fff; 
            font-weight: 500;
            align-self: flex-end; 
            border-bottom-right-radius: 4px; 
            box-shadow: 0 5px 15px rgba(239, 68, 68, 0.2);
        }

        @media(max-width: 1200px) {
            .kpi-grid { grid-template-columns: repeat(2, 1fr); }
            .main-grid { grid-template-columns: 1fr; }
        }
        @media(max-width: 768px) {
            .kpi-grid { grid-template-columns: 1fr; }
            .dw { padding: 1.5rem; }
            .dash-top-bar { flex-direction: column; gap: 1rem; align-items: flex-start; }
            #chatbot-window { right: 1rem; left: 1rem; width: auto; bottom: 100px; }
            #chatbot-fab { right: 1rem; bottom: 1.5rem; }
            #map { min-height: 350px; }
        }
    </style>
</head>
<body>

    <nav class="pn">
        <div class="inner">
            <a class="nb" href="#">
                <div class="nb-i"><i class="fa-solid fa-fire-flame-simple"></i></div>
                <div>
                    <div class="nb-t">AirQuality AI</div>
                </div>
            </a>
            <div class="d-flex align-items-center gap-3">
                <a href="/" class="bh"><i class="fa-solid fa-arrow-left me-2"></i> Return to Network</a>
            </div>
        </div>
    </nav>

    <div class="dw">
        <div class="row g-4">
            
            <div class="{% if data %}col-xl-3{% else %}col-xl-4 mx-auto mt-5{% endif %}">
                <div class="glass-card h-100">
                    <div class="card-header-neo">
                        <h6 class="card-title-neo"><i class="fa-solid fa-microchip"></i> System Parameters</h6>
                    </div>
                    <div class="card-body-neo">
                        <form method="POST" id="aqiForm">
                            <label class="form-label-neo">Regional Target</label>
                            <select id="country" class="form-control form-select-neo mb-2" onchange="loadStates()">
                                <option value="">Select Country</option>
                            </select>
                            <div class="row g-2 mb-2">
                                <div class="col-6"><select id="state" class="form-control form-select-neo" onchange="loadCities()" disabled><option value="">State</option></select></div>
                                <div class="col-6"><select id="city" class="form-control form-select-neo" disabled><option value="">City</option></select></div>
                            </div>
                            <button type="button" onclick="getCoords()" class="btn-neo-sec w-100 mb-4" style="font-size:0.75rem;"><i class="fa-solid fa-location-crosshairs me-1"></i> Lock Coordinates</button>
                            
                            <div class="row g-2 mb-4">
                                <div class="col-6"><label class="form-label-neo">Lat (N/S)</label><input type="text" id="lat" name="lat" class="form-control form-control-neo" placeholder="0.00" required readonly></div>
                                <div class="col-6"><label class="form-label-neo">Lon (E/W)</label><input type="text" id="lon" name="lon" class="form-control form-control-neo" placeholder="0.00" required readonly></div>
                            </div>

                            <label class="form-label-neo mt-2">Particulate Readings</label>
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
                            
                            <div class="d-grid gap-3 mt-4">
                                <button type="button" id="btnFetch" onclick="getAirQuality()" class="btn-neo-sec"><i class="fa-solid fa-satellite-dish me-2"></i> Sync API Telemetry</button>
                                <button type="submit" class="btn-neo-primary" id="btnPredict"><i class="fa-solid fa-bolt me-2"></i> Execute Inference</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            {% if data %}
            <div class="col-xl-9">
                <div class="dash-top-bar">
                    <h1 class="dash-title">Analysis <strong>Terminal</strong></h1>
                    <div class="dash-actions">
                        <button class="btn-dash-action" onclick="window.print()"><i class="fa-solid fa-file-pdf me-2"></i> Export Report</button>
                    </div>
                </div>

                <!-- KPIs -->
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-header">
                            <div class="kpi-label">System AQI</div>
                            <div class="kpi-icon" id="icon-aqi"><i class="fa-solid fa-wind"></i></div>
                        </div>
                        <div class="kpi-val">{{ data.aqi }}</div>
                        <div class="kpi-glow-bar" id="aqi-bar"></div>
                    </div>
                    
                    <div class="kpi-card">
                        <div class="kpi-header">
                            <div class="kpi-label">Threat Level</div>
                            <div class="kpi-icon"><i class="fa-solid fa-shield-virus"></i></div>
                        </div>
                        <div class="kpi-val" style="font-size:1.6rem;" id="kpi-cat-text">{{ data.category }}</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-header">
                            <div class="kpi-label">Primary Driver</div>
                            <div class="kpi-icon"><i class="fa-solid fa-skull-crossbones"></i></div>
                        </div>
                        <div class="kpi-val" id="kpi-prime" style="font-size:2rem;">--</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-header">
                            <div class="kpi-label">Advisory Status</div>
                            <div class="kpi-icon"><i class="fa-solid fa-triangle-exclamation"></i></div>
                        </div>
                        <div class="kpi-val" id="kpi-risk" style="font-size:1.5rem;">--</div>
                    </div>
                </div>

                <div class="main-grid">
                    <!-- LEFT: MAP (OSM WITH RED-TINT CSS INVERT) -->
                    <div class="glass-card">
                        <div class="card-header-neo">
                            <h6 class="card-title-neo"><i class="fa-solid fa-radar"></i> Geospatial Node</h6>
                        </div>
                        <div class="card-body-neo p-0 h-100 min-h-100">
                            <div id="map"></div>
                        </div>
                    </div>

                    <!-- RIGHT: CHARTS -->
                    <div class="d-flex flex-column gap-4 h-100">
                        <div class="glass-card flex-fill">
                            <div class="card-header-neo">
                                <h6 class="card-title-neo"><i class="fa-solid fa-gauge-high"></i> Severity Gauge</h6>
                            </div>
                            <div class="card-body-neo p-4">
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
                                <h6 class="card-title-neo"><i class="fa-solid fa-chart-pie"></i> Particulate Matrix</h6>
                            </div>
                            <div class="card-body-neo" style="height: 200px;">
                                <canvas id="donutChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- BOTTOM ROW -->
                <div class="row g-4 mb-3">
                    <div class="col-lg-5">
                        <div class="glass-card h-100">
                            <div class="card-header-neo">
                                <h6 class="card-title-neo"><i class="fa-solid fa-chart-simple"></i> WHO Thresholds</h6>
                            </div>
                            <div class="card-body-neo" style="height: 250px;">
                                <canvas id="barChart"></canvas>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-7">
                        <div class="ai-panel h-100">
                            <div class="ai-badge"><i class="fa-solid fa-microchip"></i> Diagnostics Protocol</div>
                            <div class="ai-text mt-3">
                                Data synthesis complete. The telemetry indicates an absolute Air Quality Index of <strong>{{ data.aqi }}</strong>.
                                <br><br>
                                The dominant atmospheric element driving this alert is <strong id="ai-prime" style="color:var(--accent)">--</strong>.<br>
                                <br>
                                <span style="color:var(--t-mut); font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px; display:inline-block;">Actionable Output:</span><br>
                                <span id="ai-advice" style="font-size:1.15rem; font-weight:500;">{{ data.advice }}</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            {% endif %}

        </div>
    </div>

    <!-- CHATBOT UI -->
    <div id="chatbot-fab" onclick="toggleChat()">
        <i class="fa-brands fa-space-awesome"></i>
    </div>
    <div id="chatbot-window">
        <div class="chat-header">
            <span><i class="fa-solid fa-robot"></i> Network AI</span>
            <button onclick="toggleChat()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="chat-body" id="chat-body">
            <div class="msg bot">System online. I am processing environmental telemetry. Awaiting query.</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="chat-input" placeholder="Initiate query..." onkeypress="handleEnter(event)">
            <button onclick="sendMessage()"><i class="fa-solid fa-arrow-up"></i></button>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        /* ====== GEMINI CHATBOT LOGIC ====== */
        const apiKey = "AIzaSyD5ucNcH5ydwGnYP72JV3Z0nEllVIoMRX4";
        const chatWindow = document.getElementById("chatbot-window");
        const chatBody = document.getElementById("chat-body");
        const chatInput = document.getElementById("chat-input");

        function toggleChat() {
            chatWindow.classList.toggle("open");
            if(chatWindow.classList.contains("open")) {
                chatInput.focus();
            }
        }

        function handleEnter(e) {
            if(e.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const text = chatInput.value.trim();
            if(!text) return;

            // Add user message
            appendMessage(text, 'user');
            chatInput.value = '';

            // Loading indicator
            const loadId = 'load-' + Date.now();
            appendMessage('<i class="fa-solid fa-circle-notch fa-spin"></i> Processing data...', 'bot', loadId);

            // Context from the dashboard if data is available
            let promptContext = "You are an advanced environmental AI assistant for a dark premium metallic dashboard. You use concise, professional language.";
            {% if data %}
                promptContext += " The current air quality analysis shows an AQI of {{data.aqi}} ({{data.category}}). The main advice is: '{{data.advice}}'. Pollutant levels are PM2.5: {{data.pm25}}, PM10: {{data.pm10}}, NO2: {{data.no2}}, O3: {{data.o3}}.";
            {% endif %}
            
            const payload = {
                contents: [{
                    parts: [{ text: promptContext + " User asks: " + text }]
                }]
            };

            try {
                // FIXED: Changed endpoint to gemini-2.5-flash based on API ListModels capability
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();
                
                // Remove loading
                document.getElementById(loadId).remove();
                
                if(data.candidates && data.candidates[0].content && data.candidates[0].content.parts) {
                    const botReply = data.candidates[0].content.parts[0].text;
                    const htmlReply = botReply.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>').replace(/\*(.*?)\*/g, '<i>$1</i>').replace(/\\n/g, '<br>');
                    appendMessage(htmlReply, 'bot');
                } else if(data.error) {
                    appendMessage(`<span style='color:#ef4444'>API Connection Error: ${data.error.message}</span>`, 'bot');
                    console.error("Gemini API Error:", data.error);
                } else {
                    appendMessage("Unable to parse telemetry response. Retry query.", 'bot');
                }
            } catch (err) {
                document.getElementById(loadId).remove();
                appendMessage("Signal lost connecting to inference server.", 'bot');
                console.error(err);
            }
        }

        function appendMessage(html, sender, id="") {
            const div = document.createElement("div");
            div.className = "msg " + sender;
            div.innerHTML = html;
            if(id) div.id = id;
            chatBody.appendChild(div);
            setTimeout(() => {
                chatBody.scrollTop = chatBody.scrollHeight;
            }, 10);
        }

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
        
        // Deep Charcoal/Ruby palette mapping
        const hexMap = {
            'green': '#10b981', // Emerald
            'yellow': '#f59e0b', // Amber 
            'orange': '#f97316', // Orange
            'red': '#ef4444', // Red
            'purple': '#d946ef', // Fuchsia
            'maroon': '#e11d48' // Rose
        };
        const actualColor = hexMap[COLOR] || '#ef4444'; // Fallback to crimson

        // Apply dynamic colors
        document.getElementById('aqi-bar').style.background = `linear-gradient(90deg, #18181b, ${actualColor}, ${actualColor})`;
        document.getElementById('icon-aqi').style.color = actualColor;
        document.getElementById('icon-aqi').style.background = actualColor + '20';
        document.getElementById('icon-aqi').style.borderColor = actualColor + '40';
        document.getElementById('kpi-cat-text').style.color = actualColor;

        // Risk Level mapping
        let riskLevel = "Nominal";
        if(AQI > 50) riskLevel = "Elevated";
        if(AQI > 100) riskLevel = "Warning";
        if(AQI > 200) riskLevel = "Critical";
        document.getElementById('kpi-risk').textContent = riskLevel;

        const poll = { 'PM2.5': PM25, 'PM10': PM10, 'NO2': NO2, 'O3': O3 };
        let mx = 0, pn = 'PM2.5';
        Object.entries(poll).forEach(([k, v]) => { if (v > mx) { mx = v; pn = k; } });
        document.getElementById('kpi-prime').textContent = pn;
        document.getElementById('ai-prime').textContent = pn;

        // CHART JS FLUSH DARK GLOBALS
        Chart.defaults.color = '#a1a1aa';
        Chart.defaults.font.family = "'Outfit', sans-serif";
        Chart.defaults.borderColor = 'rgba(255,255,255,0.03)';
        const ttOpts = { 
            backgroundColor: 'rgba(24, 24, 27, 0.95)', 
            titleColor: '#fff', 
            bodyColor: '#e4e4e7', 
            borderColor: 'rgba(239, 68, 68, 0.3)',
            borderWidth: 1,
            cornerRadius: 10, 
            padding: 14,
            displayColors: true,
            boxShadow: '0 10px 20px rgba(0,0,0,0.8)'
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
                        backgroundColor: [actualColor, 'rgba(255,255,255,0.03)'],
                        borderWidth: 0,
                        borderRadius: 12
                    }]
                },
                options: {
                    rotation: -90, circumference: 180, cutout: '82%',
                    plugins: { tooltip: { enabled: false } },
                    maintainAspectRatio: false,
                    animation: { animateRotate: true, duration: 2500, easing: 'easeOutExpo' }
                }
            });
        })();

        // DONUT CHART
        (function(){
            const ctx = document.getElementById('donutChart').getContext('2d');
            const colors = ['#ef4444', '#f43f5e', '#fda4af', '#fca5a5'];  // Monochromatic Red/Rose tones
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(poll),
                    datasets: [{
                        data: Object.values(poll),
                        backgroundColor: colors,
                        borderColor: 'transparent',
                        borderWidth: 2,
                        hoverOffset: 6
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { usePointStyle: true, boxWidth: 8, color: '#f4f4f5', font: {size:11, family:'Outfit'} } },
                        tooltip: ttOpts
                    },
                    cutout: '78%',
                    animation: { duration: 1800 }
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
                        { label: 'Live Telemetry', data: dataVals, backgroundColor: '#ef4444', borderRadius: 6, barPercentage: 0.5 },
                        { label: 'WHO Limit', data: who, backgroundColor: 'rgba(255,255,255,0.08)', borderRadius: 6, barPercentage: 0.5 }
                    ]
                },
                options: {
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false } },
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.03)' } }
                    },
                    plugins: { tooltip: ttOpts, legend: { position: 'top', align: 'end', labels: {usePointStyle: true, boxWidth:8, color: '#e4e4e7'} } },
                    animation: { duration: 1500, delay: 300 }
                }
            });
        })();

        // MAP - RESTORED OSM WITH RED TINT CSS INVERT FILTER (set in CSS #map)
        setTimeout(() => {
            const m = L.map('map', { zoomControl: true }).setView([LAT, LON], 11);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" style="color:#ef4444">OSM</a>', 
                maxZoom: 19 
            }).addTo(m);
            
            L.circle([LAT, LON], { 
                color: actualColor, 
                fillColor: actualColor, 
                fillOpacity: .15, 
                radius: 5000, 
                weight: 1 
            }).addTo(m);
            
            // Custom red marker
            const markerHtml = `<div style="width:18px;height:18px;background:${actualColor};border-radius:50%;border:2px solid #fff;box-shadow:0 0 15px ${actualColor};"></div>`;
            const customIcon = L.divIcon({ html: markerHtml, className: '', iconSize: [18,18], iconAnchor: [9,9] });

            const pop = L.popup({className: 'dark-popup'}).setContent(`<div style="color:#0a0a0c;font-weight:700;font-family:'Outfit'">AQI: ${AQI}<br><span style="color:${actualColor}">${CAT}</span></div>`);

            L.marker([LAT, LON], {icon: customIcon}).addTo(m).bindPopup(pop).openPopup();
        }, 600);

        {% endif %}
    </script>
</body>
</html>
"""

with open(r"c:\Users\Admin\Desktop\Airpollution\main\templates\prediction.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Template written successfully with Premium Red Gray Theme!")
