import { NavLink } from 'react-router-dom'
import { useLanguage } from '../i18n'

export function Layout({ children }: { children: React.ReactNode }) {
  const { language, setLanguage, t } = useLanguage()
  return (
    <div className="app-shell">
      <header className="topbar">
        <NavLink to="/" className="brand" aria-label="Before Bringing It Up home">
          <img src="/logo.svg" alt="" />
          <span>Before Bringing It Up</span>
        </NavLink>
        <nav aria-label="Primary navigation">
          <NavLink to="/">{t.overview}</NavLink>
          <NavLink to="/scenarios">{t.scenarios}</NavLink>
          <NavLink to="/sandbox">{t.sandbox}</NavLink>
          <NavLink to="/runs">{t.runs}</NavLink>
          <NavLink to="/study">{t.study}</NavLink>
        </nav>
        <button
          className="language"
          onClick={() => setLanguage(language === 'en' ? 'zh' : 'en')}
          aria-label="Switch language"
        >
          {language === 'en' ? '中文' : 'EN'}
        </button>
      </header>
      <div className="prototype-banner">{t.prototype}</div>
      <main>{children}</main>
      <footer>Reconsider-Lite · Local deterministic mock · No participant findings</footer>
    </div>
  )
}
