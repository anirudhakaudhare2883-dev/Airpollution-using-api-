import sys
import re
import os

target_file = r'c:\Users\Admin\Desktop\Airpollution\main\templates\prediction.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Force dark theme: replace <body data-theme="light"> with <body data-theme="dark">
content = content.replace('<body data-theme="light">', '<body data-theme="dark">')
content = content.replace(r'<div class="theme-btn" id="themeToggle" title="Toggle Dark/Light Mode"><i class="fa-solid fa-moon"'+'\n'+r'                        id="themeIcon"></i></div>', '')

# 2. Append Premium CSS before </style>
premium_css = """
        /* ===== PREMIUM DASHBOARD CSS ===== */
        :root, [data-theme="dark"] {
            --bg: #050b14;
            --bg2: #0a1120;
            --card-glass: rgba(13, 20, 36, 0.65);
            --border-glow: rgba(96, 165, 250, 0.15);
            --neon-blue: #3b82f6;
            --neon-purple: #8b5cf6;
            --t1: #f8fafc;
            --t2: #cbd5e1;
        }
        .premium-card {
            background: var(--card-glass);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            padding: 1.25rem;
            height: 100%;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .premium-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        }
        .premium-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
            border-color: rgba(96, 165, 250, 0.3);
        }
        .p-title {
            font-size: 0.8rem;
            color: var(--t2);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 700;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .p-title i {
            color: var(--neon-blue);
        }
        
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }
        .pkpi {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .pkpi .icon-box {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
            color: #fff;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .pkpi-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--t1);
            line-height: 1;
        }
        .pkpi-lbl {
            font-size: 0.65rem;
            color: var(--t3);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
            margin-top: 0.2rem;
        }
        .trend-up { color: #f97316; font-size: 0.7rem; }
        .trend-down { color: #22c55e; font-size: 0.7rem; }
        
        /* Map glow */
        #map {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.1);
        }
        .leaflet-popup-content-wrapper {
            background: var(--card-glass) !important;
            backdrop-filter: blur(8px);
            color: #fff !important;
            border: 1px solid var(--border-glow);
        }
        .leaflet-popup-tip {
            background: var(--card-glass) !important;
        }
        
        .ai-insights {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(59, 130, 246, 0.15));
            border-left: 4px solid var(--neon-purple);
            padding: 1rem;
            border-radius: 8px;
            position: relative;
        }
        .ai-badge {
            position: absolute;
            top: -10px; right: 20px;
            background: linear-gradient(90deg, var(--neon-purple), var(--neon-blue));
            color: #fff;
            font-size: 0.6rem;
            font-weight: 800;
            padding: 0.15rem 0.5rem;
            border-radius: 50px;
            box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
        }
        .ai-text {
            font-size: 0.9rem;
            color: var(--t1);
            line-height: 1.5;
            font-weight: 500;
        }
        
        .prog-bar {
            height: 6px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 0.8rem;
        }
        .prog-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease-in-out;
        }
        
        .top-action-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .btn-download {
            background: linear-gradient(90deg, #1e293b, #0f172a);
            border: 1px solid rgba(255,255,255,0.1);
            color: #fff;
            padding: 0.4rem 1rem;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.2s;
            cursor: pointer;
        }
        .btn-download:hover {
            border-color: var(--neon-blue);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
            color: var(--neon-blue);
        }
        
        canvas {
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
        }
        
        .fade-in {
            animation: fadeIn 0.8s ease-out forwards;
            opacity: 0;
            transform: translateY(15px);
        }
        @keyframes fadeIn {
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Layout overrides */
        @media(max-width:991px){
            .kpi-row { grid-template-columns: repeat(2, 1fr); }
        }
        @media(max-width:575px){
            .kpi-row { grid-template-columns: 1fr; }
        }
"""
content = content.replace('</style>', premium_css + '\n    </style>')

# Replace the HTML block
html_replacement = """
            {% if data %}
            <!-- PREMIUM DASHBOARD OUTPUT SECTION -->
            <div class="col-xl-9 col-lg-8 col-md-12 col-12 ms-auto">
                
                <div class="top-action-bar fade-in" style="animation-delay: 0.1s">
                    <div>
                        <h4 style="margin:0; font-weight:700; background: -webkit-linear-gradient(45deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Intelligence Report</h4>
                        <span style="font-size:0.75rem; color:var(--t3);">Live predictive analysis based on selected data.</span>
                    </div>
                    <button class="btn-download" onclick="window.print();"><i class="fa-solid fa-cloud-arrow-down me-2"></i>Download Report</button>
                </div>

                <!-- KPI CARDS -->
                <div class="kpi-row mb-3">
                    <div class="premium-card fade-in" style="animation-delay: 0.1s; padding:1rem;">
                        <div class="pkpi">
                            <div class="icon-box" id="aqiIconBox"><i class="fa-solid fa-wind"></i></div>
                            <div>
                                <div class="pkpi-val" id="kpiAqi">{{ data.aqi }}</div>
                                <div class="pkpi-lbl">Overall AQI</div>
                            </div>
                        </div>
                        <div class="prog-bar"><div class="prog-fill" id="aqiProgBar"></div></div>
                    </div>
                    <div class="premium-card fade-in" style="animation-delay: 0.2s; padding:1rem;">
                        <div class="pkpi">
                            <div class="icon-box" style="background:rgba(234, 179, 8, 0.1); border-color:rgba(234, 179, 8, 0.2); color:#eab308;"><i class="fa-solid fa-triangle-exclamation"></i></div>
                            <div>
                                <div class="pkpi-val" id="kpiCat" style="font-size:1.1rem; padding-top:0.3rem;">{{ data.category }}</div>
                                <div class="pkpi-lbl">Risk Category</div>
                            </div>
                        </div>
                    </div>
                    <div class="premium-card fade-in" style="animation-delay: 0.3s; padding:1rem;">
                        <div class="pkpi">
                            <div class="icon-box" style="background:rgba(239, 68, 68, 0.1); border-color:rgba(239, 68, 68, 0.2); color:#ef4444;"><i class="fa-solid fa-biohazard"></i></div>
                            <div>
                                <div class="pkpi-val" id="kpiPrime">PM2.5</div>
                                <div class="pkpi-lbl">Main Pollutant <i class="fa-solid fa-arrow-trend-up trend-up ms-1"></i></div>
                            </div>
                        </div>
                    </div>
                    <div class="premium-card fade-in" style="animation-delay: 0.4s; padding:1rem;">
                        <div class="pkpi">
                            <div class="icon-box" style="background:rgba(34, 197, 94, 0.1); border-color:rgba(34, 197, 94, 0.2); color:#22c55e;"><i class="fa-solid fa-shield-heart"></i></div>
                            <div>
                                <div class="pkpi-val" id="kpiStatus" style="font-size:1.1rem; padding-top:0.3rem;">Active</div>
                                <div class="pkpi-lbl">Sensor Status <i class="fa-solid fa-arrow-trend-down trend-down ms-1"></i></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- MIDDLE SECTION -->
                <div class="row g-3 mb-3">
                    <div class="col-md-4">
                        <div class="premium-card fade-in" style="animation-delay: 0.5s;">
                            <div class="p-title"><i class="fa-solid fa-gauge-high"></i> Critical Level</div>
                            <div style="height:190px; position:relative;">
                                <canvas id="aqiGauge"></canvas>
                                <div style="position:absolute; bottom:15px; left:0; right:0; text-align:center;">
                                    <div style="font-size:2rem; font-family:'JetBrains Mono', monospace; font-weight:800; color:var(--t1);" id="gaugeN">{{ data.aqi }}</div>
                                    <div style="font-size:0.65rem; color:var(--t3); text-transform:uppercase; font-weight:700;">Index Units</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-8">
                        <div class="premium-card fade-in" style="animation-delay: 0.6s;">
                            <div class="p-title"><i class="fa-solid fa-chart-area"></i> Distribution vs Limit</div>
                            <div style="height:190px;">
                                <canvas id="pollBar"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- BOTTOM SECTION -->
                <div class="row g-3 mb-3">
                    <div class="col-md-5">
                        <div class="premium-card fade-in" style="animation-delay: 0.7s;">
                            <div class="p-title"><i class="fa-solid fa-chart-pie"></i> Pollutant Split</div>
                            <div style="height:200px;">
                                <canvas id="pollDonut"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-7">
                        <div class="premium-card fade-in" style="animation-delay: 0.8s; padding:0;">
                            <div style="height:100%; min-height:230px;" id="map"></div>
                        </div>
                    </div>
                </div>
                
                <!-- AI INSIGHTS -->
                <div class="row g-3">
                    <div class="col-12">
                        <div class="premium-card fade-in ai-insights" style="animation-delay: 0.9s;">
                            <div class="ai-badge">AI INSIGHT</div>
                            <div class="p-title" style="margin-bottom:0.5rem;"><i class="fa-solid fa-microchip"></i> Recommendation Engine</div>
                            <div class="ai-text" id="aiMsg">
                                Based on the current AQI of {{ data.aqi }}, it is classified as <span style="font-weight:700; color:var(--neon-blue);" id="txtCat">{{ data.category }}</span>. {{ data.advice }} We strongly advise monitoring the <span id="txtPrime" style="font-weight:700;">--</span> levels closely.
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            {% endif %}
"""

html_pattern = re.compile(r'\{\%\s*if data\s*\%\}(.*?)\{\%\s*endif\s*\%\}', re.DOTALL)
html_matches = list(html_pattern.finditer(content))
# The first match should be the HTML output section.
if len(html_matches) >= 2:
    # Replace the HTML part
    content = content[:html_matches[0].start()] + html_replacement + content[html_matches[0].end():]


# Replace the JS part
js_replacement = """        {% if data %}
        // === PREMIUM DASHBOARD SCRIPT ===
        Chart.defaults.color = '#cbd5e1'; 
        Chart.defaults.borderColor = 'rgba(255,255,255,0.05)'; 
        Chart.defaults.font.family = "'Inter',sans-serif";
        
        const AQI = {{ data.aqi }}, COLOR = '{{data.color}}', LAT = {{ data.lat }}, LON = {{ data.lon }};
        const PM25 = {{ data.pm25 }}, PM10 = {{ data.pm10 }}, NO2 = {{ data.no2 }}, O3 = {{ data.o3 }};
        const CAT = '{{data.category}}';
        
        // Setup Colors based on AQI
        document.getElementById('aqiIconBox').style.background = COLOR + '20';
        document.getElementById('aqiIconBox').style.borderColor = COLOR + '40';
        document.getElementById('aqiIconBox').style.color = COLOR;
        document.getElementById('kpiCat').style.color = COLOR;
        document.getElementById('gaugeN').style.color = COLOR;
        document.getElementById('txtCat').style.color = COLOR;
        
        const prog = Math.min((AQI / 500) * 100, 100);
        document.getElementById('aqiProgBar').style.width = prog + '%';
        document.getElementById('aqiProgBar').style.background = COLOR;
        
        const Math_max = Math.max;
        const pollVals = { 'PM2.5': PM25, 'PM10': PM10, 'NO₂': NO2, 'O₃': O3 };
        let maxV = 0, pName = 'PM2.5';
        Object.entries(pollVals).forEach(([k, v]) => { if(v > maxV) { maxV = v; pName = k; } });
        document.getElementById('kpiPrime').textContent = pName;
        document.getElementById('txtPrime').textContent = pName;
        
        const ttOpts = { 
            backgroundColor: 'rgba(15,23,42,0.9)', 
            titleColor: '#fff', 
            bodyColor: '#cbd5e1', 
            borderColor: 'rgba(96,165,250,0.3)',
            borderWidth: 1,
            cornerRadius: 12, 
            padding: 12, 
            boxPadding: 6,
            usePointStyle: true
        };

        // 1. RADIAL GAUGE
        const ctxGauge = document.getElementById('aqiGauge').getContext('2d');
        const rRatio = Math.min(AQI/300, 1);
        const gradGauge = ctxGauge.createLinearGradient(0, 0, 200, 0);
        gradGauge.addColorStop(0, '#22c55e');
        gradGauge.addColorStop(0.3, '#eab308');
        gradGauge.addColorStop(0.6, '#f97316');
        gradGauge.addColorStop(1, '#ef4444');
        new Chart(ctxGauge, {
            type: 'doughnut',
            data: { datasets: [{ data: [rRatio*100, (1-rRatio)*100], backgroundColor: [gradGauge, 'rgba(255,255,255,0.05)'], borderWidth: 0, borderRadius: [10, 10] }] },
            options: {
                rotation: -90, circumference: 180, cutout: '80%', plugins: { tooltip: { enabled: false } },
                maintainAspectRatio: false, animation: { duration: 2000, easing: 'easeOutBounce' }
            }
        });

        // 2. DONUT CHART (SPLIT)
        const ctxDonut = document.getElementById('pollDonut').getContext('2d');
        new Chart(ctxDonut, {
            type: 'doughnut',
            data: {
                labels: Object.keys(pollVals),
                datasets: [{ data: Object.values(pollVals), backgroundColor: ['#3b82f6', '#8b5cf6', '#f97316', '#22c55e'], borderWidth: 0, hoverOffset: 4 }]
            },
            options: {
                cutout: '70%', maintainAspectRatio: false,
                plugins: { legend: { position: 'right', labels: { font: { size: 10 }, usePointStyle: true, boxWidth: 8, color: '#f8fafc' } }, tooltip: ttOpts },
                animation: { duration: 1500, easing: 'easeOutQuart' }
            }
        });

        // 3. BAR CHART (GRADIENT)
        const ctxBar = document.getElementById('pollBar').getContext('2d');
        const gradBar = ctxBar.createLinearGradient(0, 200, 0, 0);
        gradBar.addColorStop(0, 'rgba(59, 130, 246, 0.2)');
        gradBar.addColorStop(1, 'rgba(139, 92, 246, 0.8)');
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: Object.keys(pollVals),
                datasets: [
                    { label: 'Current Level', data: Object.values(pollVals), backgroundColor: gradBar, borderRadius: 6, barPercentage: 0.5 },
                    { label: 'WHO Safe Limit', data: [15, 45, 25, 100], type: 'line', borderColor: '#22c55e', borderDash: [5,5], pointBackgroundColor: '#22c55e', borderWidth: 2, tension: 0.4 }
                ]
            },
            options: {
                maintainAspectRatio: false,
                scales: { x: { grid: { display: false }, ticks: { color: '#f8fafc' } }, y: { grid: { color: 'rgba(255,255,255,0.05)' }, beginAtZero: true, ticks: { color: '#cbd5e1' } } },
                plugins: { legend: { display: true, position: 'top', labels: { usePointStyle:true, font:{size:10}, color: '#f8fafc' } }, tooltip: ttOpts },
                animation: { duration: 1800, delay: 200 }
            }
        });

        // 4. PREMIUM MAP
        setTimeout(() => {
            const m = L.map('map', { zoomControl: false, attributionControl: false }).setView([LAT, LON], 12);
            // Dark map tiles (CartoDB Dark Matter equivalent)
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(m);
            // Glowing circle
            L.circle([LAT, LON], { color: COLOR, fillColor: COLOR, fillOpacity: 0.2, radius: 4000, weight: 2, className: 'map-pulse' }).addTo(m);
            L.circle([LAT, LON], { color: COLOR, fillColor: COLOR, fillOpacity: 0.5, radius: 1000, weight: 0 }).addTo(m);
            
            // Custom popup
            const popupContent = `<div style="text-align:center; padding:5px;"><h6 style="color:${COLOR}; margin:0; font-weight:800; font-size:1.2rem;">AQI ${AQI}</h6><div style="font-size:0.75rem; color:#cbd5e1; margin-top:2px;">${CAT}</div></div>`;
            L.popup({ closeButton: false, offset: [0, -10] }).setLatLng([LAT, LON]).setContent(popupContent).openOn(m);
        }, 800);
        {% endif %}"""

html_matches = list(html_pattern.finditer(content))
if len(html_matches) >= 1:
    content = content[:html_matches[-1].start()] + js_replacement + content[html_matches[-1].end():]

# Also remove theme toggle initialization inside JS
tgs_pattern = re.compile(r'/\* ====== THEME TOGGLE ====== \*/.*?\(\)\);', re.DOTALL)
content = tgs_pattern.sub('// Theme forced to dark mode', content)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)
