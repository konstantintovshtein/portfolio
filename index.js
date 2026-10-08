// --- Mobile menu
const hamMenuBtn = document.querySelector('.header__main-ham-menu-cont')
const smallMenu = document.querySelector('.header__sm-menu')
const headerHamMenuBtn = document.querySelector('.header__main-ham-menu')
const headerHamMenuCloseBtn = document.querySelector(
  '.header__main-ham-menu-close'
)
const headerSmallMenuLinks = document.querySelectorAll('.header__sm-menu-link')

const setMenuOpen = (open) => {
  smallMenu.classList.toggle('header__sm-menu--active', open)
  headerHamMenuBtn.classList.toggle('d-none', open)
  headerHamMenuCloseBtn.classList.toggle('d-none', !open)
  hamMenuBtn.setAttribute('aria-expanded', String(open))
  hamMenuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu')
}

hamMenuBtn.addEventListener('click', () => {
  setMenuOpen(!smallMenu.classList.contains('header__sm-menu--active'))
})

headerSmallMenuLinks.forEach((link) => {
  link.addEventListener('click', () => setMenuOpen(false))
})

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && smallMenu.classList.contains('header__sm-menu--active')) {
    setMenuOpen(false)
    hamMenuBtn.focus()
  }
})

// --- Smooth scrolling (Lenis 1.3.26, MIT licence, copy in assets/vendor/lenis)
// Only mouse-wheel and trackpad scrolling is smoothed. Touch screens keep native
// scrolling, and visitors who ask for reduced motion never get Lenis at all.
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
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
