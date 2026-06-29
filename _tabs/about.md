---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
layout: page
---

<div class="ur-about">
  <div class="ur-about-head">
    <div class="ur-eyebrow ur-mono">cat about.md</div>
    <div class="ur-about-id">
      <img class="ur-about-avatar-lg" src="{{ '/assets/img/jack-wong-profile.png' | relative_url }}" alt="Jack Wong" />
      <div>
        <h1 class="ur-h1">Jack Wong</h1>
        <div class="ur-about-role ur-mono">Enterprise Architect · tech evangelist</div>
      </div>
      <div class="ur-about-pills">
        <a class="ur-pill" href="https://github.com/uright">GitHub</a>
        <a class="ur-pill" href="https://www.linkedin.com/in/jackwong3">LinkedIn</a>
      </div>
    </div>
  </div>

  <p class="ur-lead">Building with LLMs in the open. I write about AI tooling, Claude Code, and the workflows behind shipping with large language models.</p>

  <div class="ur-eyebrow ur-about-section">SKILLS</div>
  <div class="ur-skill-chips">
    <span class="ur-pill ur-mono">AWS Bedrock</span>
    <span class="ur-pill ur-mono">Azure OpenAI</span>
    <span class="ur-pill ur-mono">PGVector</span>
    <span class="ur-pill ur-mono">Qdrant</span>
    <span class="ur-pill ur-mono">LLMs &amp; deep learning</span>
    <span class="ur-pill ur-mono">Enterprise architecture</span>
  </div>

  <div class="ur-eyebrow ur-about-section">EXPERIENCE</div>
  <div class="ur-exp">
    <div class="ur-exp-item">
      <span class="ur-exp-dot current"></span>
      <div class="ur-exp-body">
        <div class="ur-exp-role">Enterprise Architect <span class="ur-mono ur-muted">present</span></div>
        <div class="ur-exp-company current">Atos</div>
        <p class="ur-exp-desc">Technology evangelist and architect for major enterprise transformation programs.</p>
      </div>
      <div class="ur-exp-logo">
        <img src="{{ '/assets/img/logos/atos.png' | relative_url }}" alt="Atos" loading="lazy" />
      </div>
    </div>
  </div>

  <div class="ur-exp">
    <div class="ur-exp-item">
      <span class="ur-exp-dot current"></span>
      <div class="ur-exp-body">
        <div class="ur-exp-role">Partner, Director of Architecture</div>
        <div class="ur-exp-company current">AppCentrica</div>
        <p class="ur-exp-desc">Led major digital and business transformation projects for a large number of automobile, P&C insurance, and other financial and enterprise clients.</p>
      </div>
      <div class="ur-exp-logo">
        <img src="{{ '/assets/img/logos/appcentrica.jpg' | relative_url }}" alt="AppCentrica" loading="lazy" />
      </div>
    </div>
  </div>

  <div class="ur-eyebrow ur-about-section">EDUCATION</div>
  <div class="ur-edu ur-card">
    <span class="ur-edu-icon">{% include uright-icon.html name="layers" size=18 %}</span>
    <div>
      <div class="ur-edu-degree">B.Sc. Computer Science</div>
      <div class="ur-mono ur-muted">Honours Computer Science · Business Option</div>
      <div class="ur-mono ur-muted">University of Waterloo</div>
    </div>
    <div class="ur-edu-logo">
      <img src="{{ '/assets/img/logos/university-of-waterloo.png' | relative_url }}" alt="University of Waterloo" loading="lazy" />
    </div>
  </div>
</div>
