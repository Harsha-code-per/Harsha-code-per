<p align="center">
  <img src="assets/profile/hero.svg" width="800" alt="Harsha Systems Blueprint Hero" />
</p>

<br />

# Harshavardhan K
### Full-Stack AI Engineer

I build intelligent digital systems at the intersection of Artificial Intelligence, machine learning, and high-performance full-stack architecture. My work focuses on end-to-end execution: taking complex models from initial tensor or prompt logic and integrating them into production-ready backends, low-latency APIs, and immersive interfaces.

I don't believe AI should be treated as a detached backend script. A machine learning model only becomes useful when it is connected to a fast database, wrapped in a low-latency synchronization channel, and exposed through a fluid client interface that helps users reason about the system's decisions. I build software where intelligence and interaction operate as a single experience.

This profile is a window into my active workspace. I use it to explore complex topologies, test distributed state flows, and build systems that adapt to human behavior.

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## Interactive System Sandbox // Signal Router

Explore how data flows through my systems. Click below to route an incoming model inference request through the architecture and decrypt the message payload, keeping system latency under 20ms.

<br />

<div style="border: 1px solid rgba(255,255,255,0.06); padding: 16px; border-radius: 6px; background: #050508; font-family: monospace; font-size: 12px; color: #a1a1aa; line-height: 1.6;">

  <p style="color: #00f2fe; font-weight: bold; margin-top: 0;">&gt; SYS_ROUTING_SIMULATOR v1.0.0</p>
  <p>&gt; STATUS: INCOMING UNROUTED INFERENCE PACKET</p>
  <p>&gt; BUDGET_CONSTRAINT: LATENCY &lt; 20ms</p>
  <p style="color: #71717a;">Route the incoming signal through your architecture to resolve the execution loop.</p>
  
  <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.06); margin: 12px 0;" />

  <!-- Root Choices -->
  <details>
    <summary style="cursor: pointer; color: #ffffff; font-weight: bold;">[ ROUTE ] // Model Node Alpha (Direct Vector Store Query)</summary>
    <div style="padding-left: 16px; margin: 8px 0; border-left: 1px solid rgba(255,255,255,0.06);">
      <p style="color: #ef4444;">[WARN] Cold start query triggered.</p>
      <p style="color: #ef4444;">[ERROR] Connection Timed Out. Vector index unbuilt or query timed out (> 120ms).</p>
      <p style="color: #71717a;">&gt; Action: Close this node to return to root and try another routing path.</p>
    </div>
  </details>

  <details style="margin-top: 8px;">
    <summary style="cursor: pointer; color: #ffffff; font-weight: bold;">[ ROUTE ] // Model Node Beta (FastAPI Model Cascade)</summary>
    <div style="padding-left: 16px; margin: 8px 0; border-left: 1px solid rgba(255,255,255,0.06);">
      <p style="color: #10b981;">[OK] Model handshake verified.</p>
      <p>&gt; Processing inference weights. Local Latency: 4.8ms. Select next destination:</p>
      
      <br />
      
      <!-- Option 2A: Write-through cache -->
      <details>
        <summary style="cursor: pointer; color: #00f2fe; font-weight: bold;">[ ROUTE ] // Database Node B1 (Write-Through Redis Cache)</summary>
        <div style="padding-left: 16px; margin: 8px 0; border-left: 1px solid rgba(0,242,254,0.1);">
          <p style="color: #10b981;">[OK] Cache write success.</p>
          <p>&gt; Syncing state. Local Latency: 2.1ms (Cumulative: 6.9ms). Route to client surface:</p>
          
          <br />
          
          <!-- Option 2A1: WebGL Canvas -->
          <details>
            <summary style="cursor: pointer; color: #10b981; font-weight: bold;">[ ROUTE ] // Surface Node S1 (WebGL Canvas Client)</summary>
            <div style="padding-left: 16px; margin: 8px 0; border-left: 1px solid rgba(16,185,129,0.1);">
              <p style="color: #10b981;">[SUCCESS] Render pipeline resolved at 60 FPS.</p>
              <p style="color: #10b981;">[SUCCESS] Output delivered. Total Latency: 16.9ms (Success target: &lt; 20ms).</p>
              <p style="color: #ffffff; background: rgba(0, 242, 254, 0.05); padding: 8px; border-radius: 4px; border: 1px solid rgba(0, 242, 254, 0.1);">
                <b>&gt; DECRYPTED_SIGNAL</b><br />
                "Welcome to the workspace. Harshavardhan K engineers systems where intelligence and interaction become one seamless experience. Portfolio: https://www.harshavardhan-k.me"
              </p>
            </div>
          </details>

          <!-- Option 2A2: DOM Refresh -->
          <details style="margin-top: 8px;">
            <summary style="cursor: pointer; color: #ef4444; font-weight: bold;">[ ROUTE ] // Surface Node S2 (Standard DOM Refresh Loop)</summary>
            <div style="padding-left: 16px; margin: 8px 0; border-left: 1px solid rgba(239,68,68,0.1);">
              <p style="color: #ef4444;">[WARN] Frame dropped. Heavy layout thrashing detected.</p>
              <p style="color: #ef4444;">[ERROR] Client crash. Main thread blocked. Total Latency: 24.1ms.</p>
              <p style="color: #71717a;">&gt; Action: Close this node to return and choose a different surface.</p>
            </div>
          </details>
        </div>
      </details>

      <!-- Option 2B: Direct Disk write -->
      <details style="margin-top: 8px;">
        <summary style="cursor: pointer; color: #ef4444; font-weight: bold;">[ ROUTE ] // Database Node B2 (PostgreSQL Raw Insert)</summary>
        <div style="padding-left: 16px; margin: 8px 0; border-left: 1px solid rgba(239,68,68,0.1);">
          <p style="color: #ef4444;">[WARN] Thread lock detected on connection pool.</p>
          <p style="color: #ef4444;">[ERROR] Transaction aborted. Local Latency: 84.2ms (Exceeded budget of 20ms).</p>
          <p style="color: #71717a;">&gt; Action: Close this node to return and choose a cache strategy.</p>
        </div>
      </details>
    </div>
  </details>
</div>

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## Current Focus

My current engineering missions and active directions:

*   **Billytics** // I wanted to build a platform that doesn't just display database rows, but models real-time business intelligence and forecasting. I am exploring how AI can become the core operating system behind executive decisions instead of another static analytics page.
*   **DeV** // I am building a workspace that shifts autonomous AI coding agents from basic prompt execution to systems that reason, persist code edits, and maintain long-term working memory within local containers.
*   **Future Explorations** // Researching the engineering behind collaborative human-AI canvases, low-latency client-side vector database querying, and zero-latency local model fallbacks.

<br />

<p align="center">
  <img src="assets/profile/divider.svg" width="800" alt="divider" />
</p>

<br />

## Active Tech Matrix

Technologies and domains I enjoy building with. Hover over each panel and tech bullet to inspect domains and see active visual feedback:

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

*   **Agentic AI** // Long-term memory compression, autonomous tooling agents.
*   **Distributed Systems** // High-frequency WebSockets, state caching databases.
*   **Developer Tools** // Local container orchestrations, playground test runs.
*   **Human-AI Interaction** // Dynamic canvas surfaces, responsive feedback loops.
*   **Motion Design** // Informational micro-animations, low-overhead SVG drawings.

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
