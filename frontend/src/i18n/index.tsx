/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useMemo, useState, type ReactNode } from 'react'

const messages = {
  en: {
    overview: 'Overview',
    scenarios: 'Scenarios',
    sandbox: 'Sandbox',
    runs: 'Run log',
    prototype: 'Synthetic research prototype — not a deployed companion service',
    thesis: 'Correct recall is not the same as appropriate use.',
    run: 'Run method',
    compare: 'Compare methods',
    generator: 'Generator context',
    outside: 'Outside generator context',
    synthetic: 'Synthetic data',
    study: 'Study',
  },
  zh: {
    overview: '项目概览',
    scenarios: '场景浏览',
    sandbox: '伴侣沙盒',
    runs: '运行记录',
    prototype: '纯合成研究原型——不是已部署的陪伴服务',
    thesis: '正确记住，不等于适合在此刻提起。',
    run: '运行方法',
    compare: '比较方法',
    generator: '生成器上下文',
    outside: '生成器上下文之外',
    synthetic: '合成数据',
    study: '研究',
  },
} as const

type Language = keyof typeof messages
type Dictionary = (typeof messages)['en']
const LanguageContext = createContext<{
  language: Language
  setLanguage: (language: Language) => void
  t: Dictionary
}>({ language: 'en', setLanguage: () => undefined, t: messages.en })

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>('en')
  const value = useMemo(
    () => ({ language, setLanguage, t: messages[language] as Dictionary }),
    [language],
  )
  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>
}

export const useLanguage = () => useContext(LanguageContext)
