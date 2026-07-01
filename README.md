<p align="center">
  <img src="assets/profile/hero.svg" width="800" alt="Harsha Systems Blueprint Hero" />
</p>

<br />

# Harshavardhan K
### Full-Stack AI Engineer

I build systems where machine learning models, distributed backends, and user interfaces merge into a single experience. I focus on taking AI models from experimental notebooks and scaling them into production-grade applications that are fast, reliable, and built to last.

This workspace details the systems I explore, my active development pipelines, and the engineering principles I use to build low-latency software.

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## Interactive System Sandbox // Tic-Tac-Toe

Take a break and play a game of Tic-Tac-Toe directly in my workspace (Player 1 vs Player 2). Click `X` or `O` on any cell to place a mark, and use the Reset button to start over. Fully built in pure HTML/CSS with zero JavaScript.

<br />

<form style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; border: 1px solid rgba(255,255,255,0.06); padding: 24px; border-radius: 8px; background: #050508; max-width: 280px; margin: 0 auto;">
  <!-- Inputs Cell 1 -->
  <input type="radio" id="c1-e" name="c1" checked style="display:none;" />
  <input type="radio" id="c1-x" name="c1" style="display:none;" />
  <input type="radio" id="c1-o" name="c1" style="display:none;" />

  <!-- Inputs Cell 2 -->
  <input type="radio" id="c2-e" name="c2" checked style="display:none;" />
  <input type="radio" id="c2-x" name="c2" style="display:none;" />
  <input type="radio" id="c2-o" name="c2" style="display:none;" />

  <!-- Inputs Cell 3 -->
  <input type="radio" id="c3-e" name="c3" checked style="display:none;" />
  <input type="radio" id="c3-x" name="c3" style="display:none;" />
  <input type="radio" id="c3-o" name="c3" style="display:none;" />

  <!-- Inputs Cell 4 -->
  <input type="radio" id="c4-e" name="c4" checked style="display:none;" />
  <input type="radio" id="c4-x" name="c4" style="display:none;" />
  <input type="radio" id="c4-o" name="c4" style="display:none;" />

  <!-- Inputs Cell 5 -->
  <input type="radio" id="c5-e" name="c5" checked style="display:none;" />
  <input type="radio" id="c5-x" name="c5" style="display:none;" />
  <input type="radio" id="c5-o" name="c5" style="display:none;" />

  <!-- Inputs Cell 6 -->
  <input type="radio" id="c6-e" name="c6" checked style="display:none;" />
  <input type="radio" id="c6-x" name="c6" style="display:none;" />
  <input type="radio" id="c6-o" name="c6" style="display:none;" />

  <!-- Inputs Cell 7 -->
  <input type="radio" id="c7-e" name="c7" checked style="display:none;" />
  <input type="radio" id="c7-x" name="c7" style="display:none;" />
  <input type="radio" id="c7-o" name="c7" style="display:none;" />

  <!-- Inputs Cell 8 -->
  <input type="radio" id="c8-e" name="c8" checked style="display:none;" />
  <input type="radio" id="c8-x" name="c8" style="display:none;" />
  <input type="radio" id="c8-o" name="c8" style="display:none;" />

  <!-- Inputs Cell 9 -->
  <input type="radio" id="c9-e" name="c9" checked style="display:none;" />
  <input type="radio" id="c9-x" name="c9" style="display:none;" />
  <input type="radio" id="c9-o" name="c9" style="display:none;" />

  <style>
    .ttt-board {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      width: 220px;
      height: 220px;
    }
    .ttt-cell {
      background: #09090b;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      font-family: ui-monospace, SFMono-Regular, monospace;
    }
    .x-marker, .o-marker {
      display: none;
      font-size: 28px;
      font-weight: bold;
      pointer-events: none;
    }
    .x-marker { color: #00f2fe; text-shadow: 0 0 6px rgba(0, 242, 254, 0.4); }
    .o-marker { color: #6366f1; text-shadow: 0 0 6px rgba(99, 102, 241, 0.4); }
    
    .cell-controls {
      display: flex;
      gap: 4px;
    }
    .play-x, .play-o {
      cursor: pointer;
      padding: 4px 6px;
      background: rgba(255,255,255,0.02);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 4px;
      color: #52525b;
      font-size: 10px;
      font-weight: bold;
      transition: all 0.2s ease;
    }
    .play-x:hover { color: #00f2fe; border-color: #00f2fe; background: rgba(0, 242, 254, 0.05); }
    .play-o:hover { color: #6366f1; border-color: #6366f1; background: rgba(99, 102, 241, 0.05); }

    .ttt-reset {
      margin-top: 8px;
      cursor: pointer;
      padding: 6px 14px;
      background: #09090b;
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 6px;
      color: #94a3b8;
      font-family: ui-monospace, SFMono-Regular, monospace;
      font-size: 11px;
      transition: all 0.2s ease;
      font-weight: bold;
    }
    .ttt-reset:hover {
      border-color: #00f2fe;
      color: #ffffff;
      background: rgba(255,255,255,0.02);
    }

    /* Target state selections */
    #c1-x:checked ~ .ttt-board #tc-1 .x-marker { display: block; }
    #c1-x:checked ~ .ttt-board #tc-1 .cell-controls { display: none; }
    #c1-o:checked ~ .ttt-board #tc-1 .o-marker { display: block; }
    #c1-o:checked ~ .ttt-board #tc-1 .cell-controls { display: none; }

    #c2-x:checked ~ .ttt-board #tc-2 .x-marker { display: block; }
    #c2-x:checked ~ .ttt-board #tc-2 .cell-controls { display: none; }
    #c2-o:checked ~ .ttt-board #tc-2 .o-marker { display: block; }
    #c2-o:checked ~ .ttt-board #tc-2 .cell-controls { display: none; }

    #c3-x:checked ~ .ttt-board #tc-3 .x-marker { display: block; }
    #c3-x:checked ~ .ttt-board #tc-3 .cell-controls { display: none; }
    #c3-o:checked ~ .ttt-board #tc-3 .o-marker { display: block; }
    #c3-o:checked ~ .ttt-board #tc-3 .cell-controls { display: none; }

    #c4-x:checked ~ .ttt-board #tc-4 .x-marker { display: block; }
    #c4-x:checked ~ .ttt-board #tc-4 .cell-controls { display: none; }
    #c4-o:checked ~ .ttt-board #tc-4 .o-marker { display: block; }
    #c4-o:checked ~ .ttt-board #tc-4 .cell-controls { display: none; }

    #c5-x:checked ~ .ttt-board #tc-5 .x-marker { display: block; }
    #c5-x:checked ~ .ttt-board #tc-5 .cell-controls { display: none; }
    #c5-o:checked ~ .ttt-board #tc-5 .o-marker { display: block; }
    #c5-o:checked ~ .ttt-board #tc-5 .cell-controls { display: none; }

    #c6-x:checked ~ .ttt-board #tc-6 .x-marker { display: block; }
    #c6-x:checked ~ .ttt-board #tc-6 .cell-controls { display: none; }
    #c6-o:checked ~ .ttt-board #tc-6 .o-marker { display: block; }
    #c6-o:checked ~ .ttt-board #tc-6 .cell-controls { display: none; }

    #c7-x:checked ~ .ttt-board #tc-7 .x-marker { display: block; }
    #c7-x:checked ~ .ttt-board #tc-7 .cell-controls { display: none; }
    #c7-o:checked ~ .ttt-board #tc-7 .o-marker { display: block; }
    #c7-o:checked ~ .ttt-board #tc-7 .cell-controls { display: none; }

    #c8-x:checked ~ .ttt-board #tc-8 .x-marker { display: block; }
    #c8-x:checked ~ .ttt-board #tc-8 .cell-controls { display: none; }
    #c8-o:checked ~ .ttt-board #tc-8 .o-marker { display: block; }
    #c8-o:checked ~ .ttt-board #tc-8 .cell-controls { display: none; }

    #c9-x:checked ~ .ttt-board #tc-9 .x-marker { display: block; }
    #c9-x:checked ~ .ttt-board #tc-9 .cell-controls { display: none; }
    #c9-o:checked ~ .ttt-board #tc-9 .o-marker { display: block; }
    #c9-o:checked ~ .ttt-board #tc-9 .cell-controls { display: none; }
  </style>

  <div class="ttt-board">
    <div class="ttt-cell" id="tc-1">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c1-x" class="play-x">X</label>
        <label for="c1-o" class="play-o">O</label>
      </div>
    </div>
    <div class="ttt-cell" id="tc-2">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c2-x" class="play-x">X</label>
        <label for="c2-o" class="play-o">O</label>
      </div>
    </div>
    <div class="ttt-cell" id="tc-3">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c3-x" class="play-x">X</label>
        <label for="c3-o" class="play-o">O</label>
      </div>
    </div>
    <div class="ttt-cell" id="tc-4">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c4-x" class="play-x">X</label>
        <label for="c4-o" class="play-o">O</label>
      </div>
    </div>
    <div class="ttt-cell" id="tc-5">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c5-x" class="play-x">X</label>
        <label for="c5-o" class="play-o">O</label>
      </div>
    </div>
    <div class="ttt-cell" id="tc-6">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c6-x" class="play-x">X</label>
        <label for="c6-o" class="play-o">O</label>
      </div>
    </div>
    <div class="ttt-cell" id="tc-7">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c7-x" class="play-x">X</label>
        <label for="c7-o" class="play-o">O</label>
      </div>
    </div>
    <div class="ttt-cell" id="tc-8">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c8-x" class="play-x">X</label>
        <label for="c8-o" class="play-o">O</label>
      </div>
    </div>
    <div class="ttt-cell" id="tc-9">
      <div class="x-marker">X</div>
      <div class="o-marker">O</div>
      <div class="cell-controls">
        <label for="c9-x" class="play-x">X</label>
        <label for="c9-o" class="play-o">O</label>
      </div>
    </div>
  </div>

  <input type="reset" value="Reset Game" class="ttt-reset" />
</form>

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## Current Focus

*   **Billytics** // Building a telemetry engine to model real-time business intelligence forecasts. Exploring how AI can become the core operating system behind decisions instead of a static dashboard feed.
*   **DeV** // Engineering a local, sandboxed workspace that shifts autonomous coding agents from single prompt wrappers to models with long-term memory and execution access.
*   **Future Explorations** // Investigating mixed-initiative human-AI canvases, low-latency edge vector indexing, and zero-latency local model fallbacks.

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## Active Tech Matrix

Overview of core systems, frameworks, and deployment tools in my stack:

<br />

<p align="center">
  <img src="assets/profile/tech_grid.svg" width="800" alt="Harsha Interactive Tech Grid" />
</p>

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## Current Interests

*   **Agentic AI** // Long-term context memory compression and routing.
*   **Distributed Systems** // Low-latency WebSocket connections and distributed caches.
*   **Developer Tools** // Local container orchestrations and playground telemetry.
*   **Human-AI Interaction** // Fluid canvas viewports and responsive user feedback loops.
*   **Motion Design** // SVG geometry animations representing processing states.

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## GitHub Activity

<br />

<table width="100%" style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="50%" align="center" style="border: none; background: transparent;">
      <img height="150" src="https://github-readme-stats.vercel.app/api?username=Harsha-code-per&show_icons=true&hide_title=true&hide_border=true&theme=transparent&text_color=a1a1aa&icon_color=00f2fe&include_all_commits=true" alt="GitHub activity summary" />
    </td>
    <td width="50%" align="center" style="border: none; background: transparent;">
      <img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Harsha-code-per&layout=compact&hide_title=true&hide_border=true&theme=transparent&text_color=a1a1aa&title_color=5e6ad2&langs_count=6" alt="Most used languages" />
    </td>
  </tr>
</table>

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## Connect

<br />

<table width="100%" style="border-collapse: collapse; border: none; font-family: monospace;">
  <tr style="border: none;">
    <td align="center" style="border: none; padding: 10px;">
      <a href="https://www.harshavardhan-k.me/" style="color: #00f2fe; text-decoration: none; font-weight: bold; letter-spacing: 1px;">// PORTFOLIO</a>
    </td>
    <td align="center" style="border: none; padding: 10px;">
      <a href="https://www.linkedin.com/in/harshavardhan-20-k/" style="color: #5e6ad2; text-decoration: none; font-weight: bold; letter-spacing: 1px;">// LINKEDIN</a>
    </td>
    <td align="center" style="border: none; padding: 10px;">
      <a href="mailto:harshavardhan3259@gmail.com" style="color: #10b981; text-decoration: none; font-weight: bold; letter-spacing: 1px;">// EMAIL</a>
    </td>
    <td align="center" style="border: none; padding: 10px;">
      <a href="https://drive.google.com/file/d/1g_EyEwvtG9v5GpdyEqVUg9QedIlSW678/view?usp=sharing" style="color: #a1a1aa; text-decoration: none; font-weight: bold; letter-spacing: 1px;">// RESUME</a>
    </td>
  </tr>
</table>

<br />
<br />

<p align="right">
  <img src="assets/profile/signature.svg" width="200" alt="Harsha Signature" /><br />
  <font size="1" face="monospace" color="#71717a">END TRANSMISSION // HANDSHAKE_RESOLVED</font>
</p>
