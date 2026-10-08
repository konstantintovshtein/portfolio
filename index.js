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

// --- Footer year
document.querySelectorAll('.js-year').forEach((el) => {
  el.textContent = new Date().getFullYear()
})
