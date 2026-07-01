import datetime
import subprocess
import collections
import urllib.request
import json
import re
import os

# Helper to run shell commands
def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    except Exception:
        return ""

# 1. Fetch live GitHub contributions calendar via public HTML page (no auth required)
total_contributions = 311
grid_commits = [[0]*7 for _ in range(15)]
calendar_fetched = False
token = os.environ.get("GITHUB_TOKEN")

try:
    url = 'https://github.com/users/Harsha-code-per/contributions'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        # Extract total contributions count
        match = re.search(r'(\d+[\d,]*)\s+contributions?\s+in\s+the\s+last\s+year', html, re.IGNORECASE)
        if match:
            total_contributions = int(match.group(1).replace(',', ''))
            
        # Parse all ContributionCalendar-day elements in the HTML
        tds = re.findall(r'<td[^>]*class=\"[^\"]*ContributionCalendar-day[^\"]*\"[^>]*>', html)
        day_levels = {}
        for td in tds:
            date_match = re.search(r'data-date=\"([^\"]+)\"', td)
            level_match = re.search(r'data-level=\"(\d+)\"', td)
            if date_match and level_match:
                date_str = date_match.group(1)
                level = int(level_match.group(1))
                day_levels[date_str] = level
                
        # Setup 15 weeks * 7 days = 105 days timeline
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=105 + (end_date.weekday() + 1) % 7)
        
        for c in range(15):
            for r in range(7):
                current_day = start_date + datetime.timedelta(days=c * 7 + r)
                date_str = current_day.strftime('%Y-%m-%d')
                grid_commits[c][r] = day_levels.get(date_str, 0)
                
        calendar_fetched = True
        print("HTML Calendar Fetch Success!")
except Exception as e:
    print(f"HTML Calendar Fetch Failed: {e}")

# Fallback: Query local Git dates
if not calendar_fetched:
    print("Running local Git history query fallback...")
    commit_dates = run_cmd('git log --pretty=format:"%ad" --date=short')
    date_counts = collections.Counter(commit_dates.split('\n'))
    
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=105 + (end_date.weekday() + 1) % 7)
    
    for c in range(15):
        for r in range(7):
            current_day = start_date + datetime.timedelta(days=c * 7 + r)
            date_str = current_day.strftime('%Y-%m-%d')
            commits = date_counts.get(date_str, 0)
            if commits == 0:
                grid_commits[c][r] = 0
            elif commits == 1:
                grid_commits[c][r] = 1
            elif commits == 2:
                grid_commits[c][r] = 2
            elif commits == 3:
                grid_commits[c][r] = 3
            else:
                grid_commits[c][r] = 4
                
    total_contributions = max(311, total_contributions)

# Map matrix heights and colors
grid_data = []
for c in range(15):
    col_data = []
    for r in range(7):
        level = grid_commits[c][r]
        if level == 0:
            h = 2
            color_top = "#161b22"
            color_left = "#0f131a"
            color_right = "#0b0d12"
            glow_color = "#161b22"
        elif level == 1:
            h = 6
            color_top = "#0e4429"
            color_left = "#0a301d"
            color_right = "#072214"
            glow_color = "#0e4429"
        elif level == 2:
            h = 12
            color_top = "#006d32"
            color_left = "#004d23"
            color_right = "#003317"
            glow_color = "#006d32"
        elif level == 3:
            h = 18
            color_top = "#26a641"
            color_left = "#1b752e"
            color_right = "#135220"
            glow_color = "#26a641"
        else:
            h = 24
            color_top = "#39d353"
            color_left = "#28943a"
            color_right = "#1c6829"
            glow_color = "#39d353"
            
        col_data.append({
            "h": h,
            "top": color_top,
            "left": color_left,
            "right": color_right,
            "glow": glow_color
        })
    grid_data.append(col_data)

# 2. Fetch public repository commit stats from GitHub API
repo_commits = collections.Counter()
recent_commits = []
total_repo_commits = 0

try:
    url = 'https://api.github.com/users/Harsha-code-per/events/public'
    headers = {'User-Agent': 'Mozilla/5.0'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        events = json.loads(response.read().decode('utf-8'))
        for event in events:
            if event['type'] == 'PushEvent':
                commits_count = event['payload'].get('size', 1)
                repo_name = event['repo']['name'].split('/')[-1]
                repo_commits[repo_name] += commits_count
                total_repo_commits += commits_count
                
                if 'commits' in event['payload']:
                    for commit in event['payload']['commits']:
                        sha = commit['sha'][:7]
                        msg = commit['message'].split('\n')[0]
                        if len(msg) > 35:
                            msg = msg[:32] + "..."
                        if len(recent_commits) < 3:
                            recent_commits.append((sha, msg))
except Exception as e:
    print(f"Events API Error: {e}")

# Sibling folder local fallback for commits count
if not repo_commits:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parent_dir = os.path.dirname(repo_root)
    paths = {
        "Harsha-code-per": repo_root,
        "Harshavardhan.portfolio": os.path.join(parent_dir, "Harshavardhan.portfolio"),
        "aura": os.path.join(parent_dir, "aura")
    }
    for name, path in paths.items():
        if os.path.exists(os.path.join(path, ".git")):
            try:
                commits = subprocess.check_output('git log --since="30 days ago" --oneline', shell=True, cwd=path).decode('utf-8').strip()
                count = len(commits.split('\n')) if commits else 0
                if count > 0:
                    repo_commits[name] = count
                    total_repo_commits += count
            except Exception:
                pass

if not repo_commits:
    repo_commits = {
        "Harsha-code-per": 11,
        "Harshavardhan.portfolio": 7,
        "Aura": 6
    }
    total_repo_commits = 24

# Recent commits local Git fallback
if not recent_commits:
    try:
        commit_lines = run_cmd('git log -n 3 --pretty=format:"%h|%s"').split('\n')
        for line in commit_lines:
            if "|" in line:
                sha, msg = line.split("|", 1)
                if len(msg) > 35:
                    msg = msg[:32] + "..."
                recent_commits.append((sha, msg))
    except Exception:
        pass

if not recent_commits:
    recent_commits = [
        ("fc00fe6", "Feat: Changes in profile designing"),
        ("2889aa0", "Feat:New Designs"),
        ("ad38ebf", "add gamification")
    ]

# Sort and get top 3
sorted_repos = sorted(repo_commits.items(), key=lambda x: x[1], reverse=True)[:3]
total_repos_count = len(repo_commits)

# Assemble bottom panel progress bar offsets
bar_colors = ["#10b981", "#6366f1", "#00f2fe"]

# 3. Compile SVG
svg_footer = "</svg>"
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="360" viewBox="0 0 800 360" fill="none">
  <style>
  <![CDATA[
    .bg-main {{ fill: #050508; }}
    .grid-lines {{ stroke: rgba(255, 255, 255, 0.015); stroke-width: 0.8; }}
    .blueprint-border {{ stroke: rgba(255, 255, 255, 0.12); stroke-width: 1; }}
    .sub-panel-bg {{ fill: #08080d; stroke: rgba(255, 255, 255, 0.03); stroke-width: 1; rx: 5px; }}
    
    .tech-header {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 11px;
      font-weight: bold;
      fill: #cbd5e1;
      letter-spacing: 1px;
    }}
    .tech-sub {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 8px;
      fill: #71717a;
      letter-spacing: 0.5px;
    }}
    .legend-text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 8px;
      fill: #52525b;
    }}
    
    .timeline-title {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 9px;
      font-weight: bold;
      fill: #ffffff;
      letter-spacing: 0.5px;
    }}
    .timeline-repo {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 9px;
      fill: #a1a1aa;
    }}
    .timeline-count {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 9px;
      font-weight: bold;
      fill: #ffffff;
    }}
    
    .commit-sha {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 8.5px;
      font-weight: bold;
      fill: #00f2fe;
    }}
    .commit-msg {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 8.5px;
      fill: #cbd5e1;
    }}

    .col-group {{ transition: filter 0.3s ease; }}
    @keyframes pulse-wave {{
      0%, 100% {{ filter: brightness(0.9); }}
      20% {{ filter: brightness(1.9) drop-shadow(0 0 6px var(--pulse-color, #39d353)); }}
    }}

    .c-0 {{ animation: pulse-wave 6s infinite 0.0s; }}
    .c-1 {{ animation: pulse-wave 6s infinite 0.3s; }}
    .c-2 {{ animation: pulse-wave 6s infinite 0.6s; }}
    .c-3 {{ animation: pulse-wave 6s infinite 0.9s; }}
    .c-4 {{ animation: pulse-wave 6s infinite 1.2s; }}
    .c-5 {{ animation: pulse-wave 6s infinite 1.5s; }}
    .c-6 {{ animation: pulse-wave 6s infinite 1.8s; }}
    .c-7 {{ animation: pulse-wave 6s infinite 2.1s; }}
    .c-8 {{ animation: pulse-wave 6s infinite 2.4s; }}
    .c-9 {{ animation: pulse-wave 6s infinite 2.7s; }}
    .c-10 {{ animation: pulse-wave 6s infinite 3.0s; }}
    .c-11 {{ animation: pulse-wave 6s infinite 3.3s; }}
    .c-12 {{ animation: pulse-wave 6s infinite 3.6s; }}
    .c-13 {{ animation: pulse-wave 6s infinite 3.9s; }}
    .c-14 {{ animation: pulse-wave 6s infinite 4.2s; }}
  ]]>
  </style>

  <rect width="800" height="360" class="bg-main" stroke="rgba(255, 255, 255, 0.08)" rx="6" />

  <!-- Background Grid -->
  <g>
    <line x1="100" y1="0" x2="100" y2="360" class="grid-lines" />
    <line x1="200" y1="0" x2="200" y2="360" class="grid-lines" />
    <line x1="300" y1="0" x2="300" y2="360" class="grid-lines" />
    <line x1="400" y1="0" x2="400" y2="360" class="grid-lines" />
    <line x1="500" y1="0" x2="500" y2="360" class="grid-lines" />
    <line x1="600" y1="0" x2="600" y2="360" class="grid-lines" />
    <line x1="700" y1="0" x2="700" y2="360" class="grid-lines" />
  </g>

  <!-- SECTION 1: 3D ISOMETRIC CONTRIBUTION GRID -->
  <text x="35" y="32" class="tech-header">CONTRIBUTION LANDSCAPE</text>
  <text x="35" y="44" class="tech-sub">{total_contributions} CONTRIBUTIONS IN THE LAST YEAR</text>

  <!-- Grid Legend -->
  <g transform="translate(620, 24)">
    <text x="0" y="8" class="legend-text">Less</text>
    <rect x="28" y="1" width="8" height="8" rx="1.5" fill="#161b22" />
    <rect x="40" y="1" width="8" height="8" rx="1.5" fill="#0e4429" />
    <rect x="52" y="1" width="8" height="8" rx="1.5" fill="#006d32" />
    <rect x="64" y="1" width="8" height="8" rx="1.5" fill="#26a641" />
    <rect x="76" y="1" width="8" height="8" rx="1.5" fill="#39d353" />
    <text x="90" y="8" class="legend-text">More</text>
  </g>
"""

# Render columns in isometric projection
cubes_svg = []
for c in range(15):
    cubes_svg.append(f'  <!-- Column {c} -->\n')
    for r in range(7):
        cell = grid_data[c][r]
        h = cell["h"]
        top_color = cell["top"]
        left_color = cell["left"]
        right_color = cell["right"]
        glow_color = cell["glow"]
        
        # Grid coordinates centered at x=400, y=112
        x = 400 + (c - 7.0) * 19.5 - (r - 3.0) * 9.8
        y = 112 + (c - 7.0) * 4.9 + (r - 3.0) * 9.8
        
        t1_x, t1_y = x, y - h
        t2_x, t2_y = x + 9, y + 4.5 - h
        t3_x, t3_y = x, y + 9 - h
        t4_x, t4_y = x - 9, y + 4.5 - h
        
        l1_x, l1_y = x - 9, y + 4.5 - h
        l2_x, l2_y = x, y + 9 - h
        l3_x, l3_y = x, y + 9
        l4_x, l4_y = x - 9, y + 4.5
        
        r1_x, r1_y = x, y + 9 - h
        r2_x, r2_y = x + 9, y + 4.5 - h
        r3_x, r3_y = x + 9, y + 4.5
        r4_x, r4_y = x, y + 9

        cubes_svg.append(f'  <g class="col-group c-{c}" style="--pulse-color: {glow_color};">\n')
        cubes_svg.append(f'    <polygon points="{l1_x},{l1_y} {l2_x},{l2_y} {l3_x},{l3_y} {l4_x},{l4_y}" fill="{left_color}" />\n')
        cubes_svg.append(f'    <polygon points="{r1_x},{r1_y} {r2_x},{r2_y} {r3_x},{r3_y} {r4_x},{r4_y}" fill="{right_color}" />\n')
        cubes_svg.append(f'    <polygon points="{t1_x},{t1_y} {t2_x},{t2_y} {t3_x},{t3_y} {t4_x},{t4_y}" fill="{top_color}" />\n')
        cubes_svg.append(f'  </g>\n')

# SECTION 2: CONTRIBUTION ACTIVITY
svg_divider = """
  <!-- Section Divider Line -->
  <line x1="35" y1="190" x2="765" y2="190" stroke="rgba(255,255,255,0.06)" stroke-width="1.2" stroke-dasharray="2 4" />

  <!-- Timeline Section -->
  <text x="35" y="212" class="tech-header">CONTRIBUTION ACTIVITY</text>
  <text x="35" y="222" class="tech-sub">LOGGED COMMITS &amp; REPOSITORIES // ACTIVE TIMELINE</text>
"""

# Build timeline content (repos on left, commits on right)
timeline_svg = []
# Dynamic commit statement
timeline_svg.append(f'  <!-- Timeline summary block -->\n')
timeline_svg.append(f'  <g transform="translate(35, 235)">\n')
timeline_svg.append(f'    <circle cx="8" cy="8" r="4" fill="#10b981" filter="drop-shadow(0 0 3px #10b981)" />\n')
timeline_svg.append(f'    <text x="20" y="11" class="timeline-title">Created {total_repo_commits} commits in {total_repos_count} repositories</text>\n')
timeline_svg.append(f'  </g>\n')

# Progress bars for top repos
# Repos names at x=60.
# Progress bars start at x=230.
# Progress bars width: 140px.
# Counts at x=382.
for idx, repo in enumerate(sorted_repos):
    name, count = repo
    color = bar_colors[idx % len(bar_colors)]
    ratio = count / float(total_repo_commits) if total_repo_commits > 0 else 0
    w = int(ratio * 140)
    y_offset = 258 + idx * 24
    
    timeline_svg.append(f'  <!-- Repo {idx+1} Progress -->\n')
    timeline_svg.append(f'  <text x="60" y="{y_offset+8}" class="timeline-repo">{name}</text>\n')
    # Track
    timeline_svg.append(f'  <rect x="230" y="{y_offset}" width="140" height="6" rx="3" fill="#161622" />\n')
    # Fill
    timeline_svg.append(f'  <rect x="230" y="{y_offset}" width="{w}" height="6" rx="3" fill="{color}" />\n')
    # Count
    timeline_svg.append(f'  <text x="382" y="{y_offset+8}" class="timeline-count" text-anchor="start">{count} commit{"s" if count > 1 else ""}</text>\n')

# Commit stream lists shifted further right from x=440 to x=480 to prevent conflicts
timeline_svg.append(f'  <!-- Commit List Header -->\n')
timeline_svg.append(f'  <text x="480" y="246" class="timeline-title">// LATEST LOGGED MISSIONS</text>\n')

for idx, commit in enumerate(recent_commits):
    sha, msg = commit
    y_offset = 262 + idx * 24
    
    timeline_svg.append(f'  <!-- Commit {idx+1} -->\n')
    timeline_svg.append(f'  <g transform="translate(480, {y_offset})">\n')
    timeline_svg.append(f'    <circle cx="5" cy="5" r="2.5" fill="#52525b" />\n')
    timeline_svg.append(f'    <text x="15" y="8" class="commit-sha">[{sha}]</text>\n')
    timeline_svg.append(f'    <text x="65" y="8" class="commit-msg">{msg}</text>\n')
    timeline_svg.append(f'  </g>\n')

# Technical borders
svg_borders = """
  <!-- Technical border decorations -->
  <path d="M 8 8 L 18 8 M 8 8 L 8 18" class="blueprint-border" />
  <path d="M 792 8 L 782 8 M 792 8 L 792 18" class="blueprint-border" />
  <path d="M 8 352 L 18 352 M 8 352 L 8 342" class="blueprint-border" />
  <path d="M 792 352 L 782 352 M 792 352 L 792 342" class="blueprint-border" />
"""

final_svg = svg_content + "".join(cubes_svg) + svg_divider + "".join(timeline_svg) + svg_borders + svg_footer

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_dir = os.path.join(repo_root, "assets", "profile")
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "activity.svg"), "w") as f:
    f.write(final_svg)
print("activity.svg written successfully!")
