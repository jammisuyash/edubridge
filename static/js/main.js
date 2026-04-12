/**
 * EduBridge — main.js
 * ====================
 * Single JavaScript file for the entire frontend.
 * Organised into namespaced modules: App, UI, Doubt, Quiz, Flash, Progress, Particles
 *
 * Every function called from HTML (onclick="X.y()") is defined here.
 * Every element ID used here matches exactly what's in index.html.
 * Every API call hits a real Flask route in app.py.
 */

"use strict";

/* ═══════════════════════════════════════════════════════════
   SPLASH — animate loading bar then hide
═══════════════════════════════════════════════════════════ */
(function runSplash() {
  const fill   = document.getElementById("splashFill");
  const splash = document.getElementById("splash");
  let   pct    = 0;

  const timer = setInterval(() => {
    pct += Math.random() * 10 + 4;
    if (pct >= 100) {
      pct = 100;
      clearInterval(timer);
      setTimeout(() => splash.classList.add("hidden"), 350);
    }
    fill.style.width = pct + "%";
  }, 70);
})();


/* ═══════════════════════════════════════════════════════════
   PARTICLES — animated connected-dot background
═══════════════════════════════════════════════════════════ */
(function runParticles() {
  const canvas = document.getElementById("particles");
  const ctx    = canvas.getContext("2d");

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener("resize", resize);
  resize();

  // Create 55 particles with random position and velocity
  const dots = Array.from({ length: 55 }, () => ({
    x:  Math.random() * canvas.width,
    y:  Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.4,
    vy: (Math.random() - 0.5) * 0.4,
    r:  Math.random() * 1.8 + 0.5,
    a:  Math.random() * 0.35 + 0.08,
  }));

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw connecting lines between nearby dots
    for (let i = 0; i < dots.length; i++) {
      for (let j = i + 1; j < dots.length; j++) {
        const dx   = dots[i].x - dots[j].x;
        const dy   = dots[i].y - dots[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.strokeStyle = `rgba(124,58,237,${0.12 * (1 - dist / 120)})`;
          ctx.lineWidth   = 0.5;
          ctx.beginPath();
          ctx.moveTo(dots[i].x, dots[i].y);
          ctx.lineTo(dots[j].x, dots[j].y);
          ctx.stroke();
        }
      }
    }

    // Draw each dot and move it
    dots.forEach(d => {
      ctx.beginPath();
      ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(167,139,250,${d.a})`;
      ctx.fill();
      d.x += d.vx;
      d.y += d.vy;
      if (d.x < 0 || d.x > canvas.width)  d.vx *= -1;
      if (d.y < 0 || d.y > canvas.height) d.vy *= -1;
    });

    requestAnimationFrame(draw);
  }
  draw();
})();


/* ═══════════════════════════════════════════════════════════
   UI — nav scroll, mobile menu, smooth links, reveal
═══════════════════════════════════════════════════════════ */
const UI = {

  init() {
    this._navScroll();
    this._revealOnScroll();
    this._smoothLinks();
    this._counterAnimation();
    this._phoneAnimation();
    this._offlineStatus();
    this._pwaInstall();
  },

  /** Highlight nav link based on scroll position */
  _navScroll() {
    const nav      = document.getElementById("mainNav");
    const sections = document.querySelectorAll("section[id]");
    const links    = document.querySelectorAll(".nav-link");

    window.addEventListener("scroll", () => {
      nav.classList.toggle("scrolled", window.scrollY > 50);

      let current = "";
      sections.forEach(s => {
        if (window.scrollY >= s.offsetTop - 100) current = s.id;
      });
      links.forEach(l => {
        l.classList.toggle("active", l.getAttribute("href") === "#" + current);
      });
    });
  },

  /** Hamburger mobile menu */
  toggleMenu() {
    document.getElementById("hamburger").classList.toggle("open");
    document.getElementById("mobileMenu").classList.toggle("open");
  },

  closeMenu() {
    document.getElementById("hamburger").classList.remove("open");
    document.getElementById("mobileMenu").classList.remove("open");
  },

  /** Smooth scroll for all anchor links */
  _smoothLinks() {
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener("click", e => {
        e.preventDefault();
        const target = document.querySelector(a.getAttribute("href"));
        if (target) target.scrollIntoView({ behavior: "smooth" });
        this.closeMenu();
      });
    });
  },

  /** Fade-in elements as they scroll into view */
  _revealOnScroll() {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => entry.target.classList.add("in"), i * 90);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    document.querySelectorAll(".reveal, .reveal-right, .reveal-up")
            .forEach(el => obs.observe(el));
  },

  /** Animate hero stat numbers counting up */
  _counterAnimation() {
    const statsEl = document.querySelector(".hero-stats");
    if (!statsEl) return;

    const obs = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) return;
      document.querySelectorAll(".hstat-n").forEach(el => {
        const target = parseInt(el.dataset.target, 10);
        let   val    = 0;
        const step   = target / 60;
        const t = setInterval(() => {
          val = Math.min(val + step, target);
          el.textContent = Math.floor(val);
          if (val >= target) clearInterval(t);
        }, 18);
      });
      obs.disconnect();
    }, { threshold: 0.5 });

    obs.observe(statsEl);
  },

  /** Animate the hero phone chat mockup */
  _phoneAnimation() {
    const typing = document.getElementById("pcTyping");
    if (!typing) return;
    setTimeout(() => {
      typing.innerHTML = "";
      typing.className = "pc-msg bot";
      typing.textContent = "Recursion = a function calling itself! 🔁 Think Russian dolls.";
    }, 2800);
  },

  /** Show/hide offline badge */
  _offlineStatus() {
    const tag = document.getElementById("offlineTag");
    const update = () => tag.classList.toggle("show", !navigator.onLine);
    window.addEventListener("online",  update);
    window.addEventListener("offline", update);
    update();
  },

  /** PWA install prompt */
  _pwaInstall() {
    let prompt;
    window.addEventListener("beforeinstallprompt", e => {
      e.preventDefault();
      prompt = e;
      document.getElementById("installBanner").classList.add("show");
    });
    document.getElementById("installBtn").addEventListener("click", async () => {
      if (!prompt) return;
      prompt.prompt();
      const { outcome } = await prompt.userChoice;
      if (outcome === "accepted")
        document.getElementById("installBanner").classList.remove("show");
      prompt = null;
    });
    document.getElementById("bannerClose").addEventListener("click", () => {
      document.getElementById("installBanner").classList.remove("show");
    });
  },
};


/* ═══════════════════════════════════════════════════════════
   APP — student session, tab switching, streak
═══════════════════════════════════════════════════════════ */
const App = {

  init() {
    this._loadStreak();
    this._initTabs();
    this._checkStudent();

    // Hamburger click
    document.getElementById("hamburger")
            .addEventListener("click", () => UI.toggleMenu());
  },

  /** Check if student is already named; if not, show modal */
  _checkStudent() {
    const name = sessionStorage.getItem("eb_student");
    if (name) {
      this._showStudentName(name);
    } else {
      document.getElementById("nameModal").classList.remove("hidden");
      setTimeout(() => {
        document.getElementById("studentNameInput").focus();
      }, 300);
    }
    // Allow Enter key in modal
    document.getElementById("studentNameInput")
            .addEventListener("keydown", e => {
              if (e.key === "Enter") this.setStudent();
            });
  },

  /** Called by the modal button — saves student name to session */
  setStudent() {
    const input = document.getElementById("studentNameInput");
    const err   = document.getElementById("nameError");
    const name  = input.value.trim();

    err.textContent = "";
    if (!name || name.length < 2) {
      err.textContent = "Please enter at least 2 characters.";
      return;
    }

    // Tell the Flask backend about this student
    fetch("/api/set-student", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ name }),
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        sessionStorage.setItem("eb_student", name);
        document.getElementById("nameModal").classList.add("hidden");
        this._showStudentName(name);
      } else {
        err.textContent = data.error || "Something went wrong.";
      }
    })
    .catch(() => {
      // Offline fallback — still let them in
      sessionStorage.setItem("eb_student", name);
      document.getElementById("nameModal").classList.add("hidden");
      this._showStudentName(name);
    });
  },

  _showStudentName(name) {
    const pill = document.getElementById("studentDisplay");
    pill.textContent = "👤 " + name;
    pill.classList.add("show");
  },

  /** Daily streak counter stored in localStorage */
  _loadStreak() {
    const today     = new Date().toDateString();
    const stored    = JSON.parse(localStorage.getItem("eb_streak") || '{"count":0,"last":""}');
    const yesterday = new Date(Date.now() - 86400000).toDateString();

    if (stored.last === today) {
      // same day — no change
    } else if (stored.last === yesterday) {
      stored.count++;
    } else {
      stored.count = 1;
    }
    stored.last = today;
    localStorage.setItem("eb_streak", JSON.stringify(stored));

    document.getElementById("streakNum").textContent = stored.count;
  },

  /** Sidebar tab switching */
  _initTabs() {
    document.querySelectorAll(".sbtn").forEach(btn => {
      btn.addEventListener("click", () => {
        const tab = btn.dataset.tab;

        // Update sidebar button state
        document.querySelectorAll(".sbtn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        // Show the correct panel
        document.querySelectorAll(".panel").forEach(p => p.style.display = "none");
        document.getElementById("panel-" + tab).style.display = "block";

        // Load data for that panel
        if (tab === "progress") Progress.load();
        if (tab === "flash")    Flash.init();
      });
    });
  },
};


/* ═══════════════════════════════════════════════════════════
   DOUBT — chat interface + Flask API call to /api/solve
═══════════════════════════════════════════════════════════ */
const Doubt = {

  /** Ask a doubt — called from quick pills or the send button */
  ask(preset) {
    const input = document.getElementById("doubtInput");
    const query = preset || input.value.trim();
    if (!query) return;

    input.value = "";
    const win = document.getElementById("chatWindow");

    // Show what the user asked
    this._addMessage(win, "user", query);

    // Show typing indicator
    const typingEl = this._addTypingIndicator(win);

    // Disable send button while waiting
    const sendBtn = document.getElementById("sendBtn");
    sendBtn.disabled = true;

    // Call Flask backend
    fetch("/api/solve", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ question: query }),
    })
    .then(r => r.json())
    .then(data => {
      typingEl.remove();
      sendBtn.disabled = false;

      if (data.success) {
        const r      = data.result;
        const source = data.source || "local";

        // Badge showing whether answer is from local knowledge base or Gemini AI
        const badge = source === "ai"
          ? `<span style="display:inline-block;background:rgba(66,133,244,0.2);border:1px solid rgba(66,133,244,0.4);color:#93c5fd;font-size:11px;padding:2px 10px;border-radius:20px;margin-bottom:10px">✨ Answered by Gemini AI</span><br/>`
          : `<span style="display:inline-block;background:rgba(45,212,191,0.15);border:1px solid rgba(45,212,191,0.3);color:#5eead4;font-size:11px;padding:2px 10px;border-radius:20px;margin-bottom:10px">📚 Local Knowledge Base</span><br/>`;

        const stepsHtml = (r.steps || [])
          .map((s, i) => `<span style="color:rgba(255,255,255,0.45);font-size:12px">${i+1}.</span> ${s}`)
          .join("<br/>");

        const exampleHtml = r.example ? `<div class="chat-code">${r.example}</div>` : "";
        const tipHtml     = r.tip     ? `<br/><span style="color:#a78bfa;font-size:13px">💡 ${r.tip}</span>` : "";

        const html = `${badge}<strong style="font-size:15px">${r.title}</strong><br/><br/>${stepsHtml}${exampleHtml}${tipHtml}`;
        this._addMessage(win, "bot", html, true);

      } else {
        // If Gemini can't be reached, show friendly message
        const msg = data.error && data.error.includes("internet")
          ? "I couldn't reach the Gemini AI right now. Check your internet connection and try again."
          : `Sorry, something went wrong: ${data.error || "unknown error"}`;
        this._addMessage(win, "bot", msg, false);
      }
    })
    .catch(() => {
      typingEl.remove();
      sendBtn.disabled = false;
      this._addMessage(win, "bot",
        "Connection error. Make sure Flask is running on port 5000.", false);
    });
  },

  clear() {
    const win = document.getElementById("chatWindow");
    win.innerHTML = `
      <div class="chat-msg bot">
        <div class="chat-av">EB</div>
        <div class="chat-bub">Chat cleared! Ask me anything 😊</div>
      </div>`;
  },

  _addMessage(container, type, content, isHTML = false) {
    const el  = document.createElement("div");
    el.className = `chat-msg ${type === "user" ? "user-msg" : ""}`;

    const av  = document.createElement("div");
    av.className = "chat-av";
    av.textContent = type === "user" ? "👤" : "EB";

    const bub = document.createElement("div");
    bub.className = "chat-bub";
    if (isHTML) bub.innerHTML  = content;
    else        bub.textContent = content;

    el.appendChild(av);
    el.appendChild(bub);
    container.appendChild(el);
    container.scrollTop = container.scrollHeight;
    return el;
  },

  _addTypingIndicator(container) {
    const el  = document.createElement("div");
    el.className = "chat-msg";
    el.innerHTML = `
      <div class="chat-av">EB</div>
      <div class="chat-bub">
        <div class="typing-dots"><span></span><span></span><span></span></div>
      </div>`;
    container.appendChild(el);
    container.scrollTop = container.scrollHeight;
    return el;
  },
};


/* ═══════════════════════════════════════════════════════════
   QUIZ — 3-step flow: pick topic → answer questions → results
   API: POST /api/quiz/start  →  POST /api/quiz/submit
═══════════════════════════════════════════════════════════ */
const Quiz = {
  _topic:     "",
  _questions: [],   // question objects from server (no answers)
  _answers:   [],   // student's submitted answers (index of chosen option)
  _current:   0,
  _score:     0,

  /** Step 1: fetch questions from server for chosen topic */
  start(topic) {
    this._topic     = topic;
    this._questions = [];
    this._answers   = [];
    this._current   = 0;
    this._score     = 0;

    fetch("/api/quiz/start", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ topic, count: 6 }),
    })
    .then(r => r.json())
    .then(data => {
      if (!data.success) { alert(data.error); return; }
      this._questions = data.questions;
      this._show("quizActive");
      document.getElementById("quizTopicLbl").textContent = topic;
      this._renderQuestion();
    })
    .catch(() => alert("Could not load quiz. Is Flask running?"));
  },

  /** Render the current question */
  _renderQuestion() {
    const q = this._questions[this._current];
    if (!q) { this._submitAnswers(); return; }

    const total = this._questions.length;
    const pct   = Math.round((this._current / total) * 100);

    document.getElementById("quizPFill").style.width      = pct + "%";
    document.getElementById("quizQNum").textContent        = `${this._current + 1} / ${total}`;
    document.getElementById("quizLiveScore").textContent   = this._score;
    document.getElementById("quizQCard").textContent       = q.q;
    document.getElementById("quizFeedback").style.display  = "none";
    document.getElementById("quizNextBtn").style.display   = "none";

    const optsEl = document.getElementById("quizOpts");
    optsEl.innerHTML = "";
    q.options.forEach((opt, i) => {
      const btn = document.createElement("button");
      btn.className   = "quiz-opt";
      btn.textContent = opt;
      btn.onclick     = () => this._selectAnswer(i);
      optsEl.appendChild(btn);
    });
  },

  /** Student selects an answer — store it, show next button */
  _selectAnswer(index) {
    // Disable all options
    document.querySelectorAll(".quiz-opt").forEach(b => b.disabled = true);

    // Highlight selected
    document.querySelectorAll(".quiz-opt")[index].style.borderColor = "rgba(124,58,237,0.6)";

    // Store the answer (we'll submit all at end)
    this._answers[this._current] = index;

    // Optimistically update live score (rough guess, server confirms)
    document.getElementById("quizNextBtn").style.display = "block";
  },

  /** Go to next question */
  next() {
    this._current++;
    if (this._current >= this._questions.length) {
      this._submitAnswers();
    } else {
      this._renderQuestion();
    }
  },

  /** Step 2: submit all answers to Flask for scoring */
  _submitAnswers() {
    fetch("/api/quiz/submit", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ answers: this._answers }),
    })
    .then(r => r.json())
    .then(data => {
      if (!data.success) { alert(data.error); return; }
      this._showResult(data);
    })
    .catch(() => alert("Could not submit quiz. Is Flask running?"));
  },

  /** Step 3: show the result screen */
  _showResult(data) {
    this._show("quizResult");

    const pct = data.percentage;
    document.getElementById("resultPct").textContent = pct + "%";

    // Animate the SVG ring (circumference ≈ 351.9)
    const arc    = document.getElementById("resultRingArc");
    const offset = 351.9 * (1 - pct / 100);
    setTimeout(() => {
      arc.style.transition      = "stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1)";
      arc.style.strokeDashoffset = offset;
    }, 100);

    // Messages based on score
    let title, body;
    if      (pct >= 80) { title = "🏆 Excellent!";  body  = "You nailed it! Try a harder topic next."; }
    else if (pct >= 60) { title = "👍 Good Job!";   body  = "Review the explanations and aim for 80%+."; }
    else                { title = "💪 Keep Going!"; body  = "Revisit the topic in Doubt Solver, then retry!"; }

    document.getElementById("resultTitle").textContent = title;
    document.getElementById("resultBody").textContent  = body;

    // Show per-question feedback
    if (data.feedback) {
      const optsEl = document.getElementById("quizOpts");
      optsEl.innerHTML = "";
      const fb = document.getElementById("quizFeedback");
      fb.style.display = "block";
      fb.className     = "quiz-feedback ok";
      const correct = data.feedback.filter(f => f.correct).length;
      fb.innerHTML = `<strong>You got ${correct} / ${data.total} correct.</strong> ${data.weak_areas && data.weak_areas.length ? "Weak areas saved to your progress." : ""}`;
    }
  },

  retry()  { this.start(this._topic); },
  reset()  { this._show("quizTopicPicker"); },

  _show(id) {
    ["quizTopicPicker","quizActive","quizResult"].forEach(s => {
      const el = document.getElementById(s);
      if (el) el.style.display = (s === id) ? "block" : "none";
    });
  },
};


/* ═══════════════════════════════════════════════════════════
   FLASH — flashcard studio
   API: GET /api/flashcards
═══════════════════════════════════════════════════════════ */
const Flash = {
  _cards:  [],
  _index:  0,
  _known:  new Set(),   // JS Set mirrors Python set — unique card indices
  _review: new Set(),
  _loaded: false,

  init() {
    if (this._loaded) { this._render(); return; }

    fetch("/api/flashcards")
      .then(r => r.json())
      .then(data => {
        if (!data.success) return;
        this._cards  = data.flashcards;
        this._loaded = true;
        this._index  = 0;
        this._render();
      })
      .catch(() => {
        document.getElementById("fcQuestion").textContent = "Could not load cards. Is Flask running?";
      });
  },

  /** Render the current card */
  _render() {
    const card = this._cards[this._index];
    if (!card) return;

    // Reset flip
    document.getElementById("fcCard").classList.remove("flipped");

    document.getElementById("fcTag").textContent      = card.tag;
    document.getElementById("fcQuestion").textContent = card.question;
    document.getElementById("fcAnswer").textContent   = card.answer;
    document.getElementById("fcExample").textContent  = card.example;

    document.getElementById("fcCounter").textContent =
      `${this._index + 1} / ${this._cards.length}`;

    this._updateStats();
  },

  flip() {
    document.getElementById("fcCard").classList.toggle("flipped");
  },

  nav(dir) {
    // Wrap around using modulo — Python: index = (index + dir) % len(cards)
    this._index = (this._index + dir + this._cards.length) % this._cards.length;
    this._render();
  },

  mark(status) {
    if (status === "known") {
      this._known.add(this._index);
      this._review.delete(this._index);
    } else {
      this._review.add(this._index);
      this._known.delete(this._index);
    }
    this._updateStats();
    this.nav(1);  // auto-advance
  },

  _updateStats() {
    const total  = this._cards.length;
    const known  = this._known.size;
    const review = this._review.size;
    const pct    = total > 0 ? Math.round((known / total) * 100) : 0;

    document.getElementById("fcKnownCount").textContent  = `Known: ${known}`;
    document.getElementById("fcReviewCount").textContent = `Review: ${review}`;
    document.getElementById("fcTrackFill").style.width   = pct + "%";
  },
};


/* ═══════════════════════════════════════════════════════════
   PROGRESS — reads from Flask backend (which reads from files)
   API: GET /api/progress   POST /api/progress/clear
═══════════════════════════════════════════════════════════ */
const Progress = {

  load() {
    fetch("/api/progress")
      .then(r => r.json())
      .then(data => {
        if (!data.success) return;
        this._render(data.report);
      })
      .catch(() => {
        document.getElementById("sessionLog").innerHTML =
          '<div class="chip-empty">Could not load progress. Is Flask running?</div>';
      });
  },

  _render(report) {
    // Stat cards
    document.getElementById("pSessions").textContent = report.total_sessions || 0;
    document.getElementById("pDoubts").textContent   = report.total_doubts   || 0;
    document.getElementById("pAvg").textContent      = (report.avg_score || 0) + "%";

    const streak = JSON.parse(localStorage.getItem("eb_streak") || '{"count":0}').count;
    document.getElementById("pStreak").textContent   = "🔥" + streak;
    document.getElementById("streakNum").textContent = streak;

    // Score history bar chart
    const chart   = document.getElementById("scoreChart");
    const scores  = report.recent_scores || [];
    if (scores.length === 0) {
      chart.innerHTML = '<div class="chart-empty">Complete quizzes to see your score history</div>';
    } else {
      chart.style.display = "flex";
      chart.innerHTML = scores.map(s => `
        <div class="chart-bar-wrap">
          <div class="chart-bar" style="height:0%;max-height:80px" data-h="${s.score}"></div>
          <div class="chart-lbl">${s.score}%</div>
        </div>`).join("");
      // Animate bars in
      setTimeout(() => {
        chart.querySelectorAll(".chart-bar").forEach(bar => {
          bar.style.transition = "height 0.7s cubic-bezier(0.4,0,0.2,1)";
          bar.style.height     = bar.dataset.h + "%";
        });
      }, 80);
    }

    // Weak topics chips
    const weakEl = document.getElementById("weakChips");
    const weak   = report.weak_topics || [];
    weakEl.innerHTML = weak.length === 0
      ? '<span class="chip-empty">No weak topics yet — keep going!</span>'
      : weak.map(t => `<span class="weak-chip">${t}</span>`).join("");

    // Session log
    const logEl   = document.getElementById("sessionLog");
    const history = report.quiz_history || [];
    logEl.innerHTML = history.length === 0
      ? '<div class="chip-empty">No quiz sessions yet. Take your first quiz!</div>'
      : history.map(h => `
          <div class="sess-entry">
            <span class="sess-topic">${h.topic} Quiz</span>
            <span class="sess-score">${h.percentage}%</span>
            <span class="sess-time">${h.time || ""}</span>
          </div>`).join("");
  },

  clear() {
    if (!confirm("Clear all your progress? This cannot be undone.")) return;
    fetch("/api/progress/clear", { method: "POST" })
      .then(r => r.json())
      .then(() => this.load())
      .catch(() => alert("Could not clear progress."));
  },
};


/* ═══════════════════════════════════════════════════════════
   SERVICE WORKER — registers sw.js for offline PWA support
═══════════════════════════════════════════════════════════ */
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/static/sw.js")
      .catch(err => console.warn("SW registration failed:", err));
  });
}


/* ═══════════════════════════════════════════════════════════
   BOOT — initialise everything when DOM is ready
═══════════════════════════════════════════════════════════ */
document.addEventListener("DOMContentLoaded", () => {
  UI.init();
  App.init();
});
