const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)')

// --- Animated titles. Screen readers get the full text at once from a hidden copy.
const splitTitle = (el) => {
  const full = el.textContent.trim()
  const hidden = Object.assign(document.createElement('span'), { className: 'sr-only', textContent: full })
  const shown = document.createElement('span')
  shown.setAttribute('aria-hidden', 'true')
  el.replaceChildren(hidden, shown)
  return [full, shown]
}

const typeTitle = (el) => {
  const [full, shown] = splitTitle(el)
  const caret = Object.assign(document.createElement('span'), { className: 'type-caret' })
  caret.setAttribute('aria-hidden', 'true')
  el.append(caret)
  let i = 0
  const tick = () => {
    i += 1
    shown.textContent = full.slice(0, i)
    if (i < full.length) setTimeout(tick, 60)
    else setTimeout(() => caret.remove(), 1500)
  }
  setTimeout(tick, 250)
}

const scrambleTitle = (el) => {
  const [full, shown] = splitTitle(el)
  const glyphs = '!<>-_/[]{}=+*^?#%&@0123456789'
  const frames = 26
  let frame = 0
  const tick = () => {
    const settled = Math.floor((frame / frames) * full.length)
    shown.textContent = [...full]
      .map((c, i) => (i < settled ? c : glyphs[Math.floor(Math.random() * glyphs.length)]))
      .join('')
    frame += 1
    if (frame <= frames) setTimeout(tick, 45)
  }
  tick()
}

// --- Sections fade in as they scroll into view, and type their titles once.
// Runs first: the sections start hidden, so an error further down must not keep them that way.
const reveal = (section) => {
  section.classList.add('is-visible')
  if (!reducedMotion.matches) section.querySelectorAll('[data-type]').forEach(typeTitle)
}
const sections = document.querySelectorAll('.reveal')

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) =>
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        observer.unobserve(entry.target)
        reveal(entry.target)
      }),
    { rootMargin: '0px 0px -60px 0px', threshold: 0.1 }
  )
  sections.forEach((section) => observer.observe(section))
} else {
  sections.forEach(reveal)
}

if (!reducedMotion.matches) document.querySelectorAll('[data-scramble]').forEach(scrambleTitle)

// --- Smooth scrolling (Lenis 1.3.26, MIT licence, copy in assets/vendor/lenis)
// Only mouse-wheel and trackpad scrolling is smoothed. Touch screens keep native
// scrolling, and visitors who ask for reduced motion never get Lenis at all.
let lenis = null

const startLenis = () => {
  if (lenis || reducedMotion.matches || typeof window.Lenis !== 'function') return
  lenis = new window.Lenis({
    autoRaf: true,
    lerp: 0.1,
    stopInertiaOnNavigate: true,
  })
}

const stopLenis = () => {
  if (!lenis) return
  lenis.destroy()
  lenis = null
}

startLenis()
reducedMotion.addEventListener('change', () =>
  reducedMotion.matches ? stopLenis() : startLenis()
)

// Smooth-scroll links to a section of the current page. "/portfolio/" and
// "/portfolio/index.html" count as the same page, so "Contact" doesn't reload it.
const samePage = (url) => {
  const clean = (path) => path.replace(/index\.html$/, '')
  return url.origin === location.origin && clean(url.pathname) === clean(location.pathname)
}

document.addEventListener('click', (e) => {
  if (!lenis || e.defaultPrevented || e.button !== 0) return
  if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
  const link = e.target.closest('a[href*="#"]')
  if (!link || link.target === '_blank') return
  const url = new URL(link.href)
  if (!url.hash || !samePage(url)) return
  const target = document.getElementById(decodeURIComponent(url.hash.slice(1)))
  if (!target) return

  e.preventDefault()
  history.pushState(null, '', url.hash)
  lenis.scrollTo(target, {
    onComplete: () => {
      // Move keyboard focus to the section, as a normal jump link would.
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1')
      target.focus({ preventScroll: true })
    },
  })
})

// --- Background streaks. They move only on the home page while the hero is in view;
// everywhere else (and for reduced motion) the canvas holds one still frame.
const canvas = document.querySelector('.page-bg__streaks')

if (canvas) {
  const ctx = canvas.getContext('2d')
  const colors = ['59,130,246', '96,165,250', '147,197,253']
  const animated = document.body.classList.contains('page-home') && !reducedMotion.matches
  let w = 0
  let h = 0
  let dpr = 1
  let t = 0
  let streaks = []
  let lastWidth = 0
  let running = false

  const spawn = (s = {}) =>
    Object.assign(s, {
      x: Math.random() * w,
      y: Math.random() * h,
      trail: [],
      age: 0,
      life: 160 + Math.random() * 260,
      speed: (0.8 + Math.random() * 1.6) * dpr,
      width: (0.6 + Math.random() * 1.1) * dpr,
      alpha: 0.15 + Math.random() * 0.35,
      color: colors[Math.floor(Math.random() * colors.length)],
    })

  // Each streak follows a slowly turning flow field and keeps its last 24 points as a fading tail.
  const step = () => {
    t += 0.0025
    ctx.clearRect(0, 0, w, h)
    for (const s of streaks) {
      const angle = Math.sin((s.x / w) * 3 + t) * 1.2 + Math.cos((s.y / h) * 2.4 - t) - 0.5
      s.x += Math.cos(angle) * s.speed
      s.y += Math.sin(angle) * s.speed
      s.trail.push(s.x, s.y)
      if (s.trail.length > 48) s.trail.splice(0, 2)
      s.age += 1
      const fade = Math.max(0, Math.min(1, s.age / 40, (s.life - s.age) / 40))
      ctx.strokeStyle = `rgb(${s.color})`
      ctx.lineWidth = s.width
      for (let i = 2; i < s.trail.length; i += 2) {
        ctx.globalAlpha = s.alpha * fade * (i / s.trail.length)
        ctx.beginPath()
        ctx.moveTo(s.trail[i - 2], s.trail[i - 1])
        ctx.lineTo(s.trail[i], s.trail[i + 1])
        ctx.stroke()
      }
      if (s.age > s.life || s.x < 0 || s.x > w || s.y < 0 || s.y > h) spawn(s)
    }
    ctx.globalAlpha = 1
  }

  // Phone toolbars change only the height while scrolling; redrawing then would flicker.
  const resize = () => {
    if (window.innerWidth === lastWidth) return
    lastWidth = window.innerWidth
    dpr = Math.min(window.devicePixelRatio || 1, 2)
    w = canvas.width = Math.round(canvas.clientWidth * dpr)
    h = canvas.height = Math.round(canvas.clientHeight * dpr)
    const count = Math.round(Math.min(110, (window.innerWidth * window.innerHeight) / 11000))
    streaks = Array.from({ length: count }, () => spawn())
    // Warm up so the first (or only) frame already has tails, even if the loop never runs.
    for (let i = 0; i < 90; i++) step()
  }

  const loop = () => {
    if (!running) return
    step()
    requestAnimationFrame(loop)
  }

  const setRunning = (on) => {
    if (on === running) return
    running = on
    if (on) requestAnimationFrame(loop)
  }

  resize()
  window.addEventListener('resize', resize)

  const hero = document.querySelector('.hero')
  if (hero) {
    const onScroll = () => {
      const past = window.scrollY > hero.offsetHeight * 0.6
      document.body.classList.toggle('past-hero', past)
      setRunning(animated && !past)
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
  }
}
