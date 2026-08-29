import { Route, Routes } from 'react-router-dom'
import { OverviewPage } from './app/OverviewPage'
import { Layout } from './components/Layout'
import { CompanionSandbox } from './features/companion-sandbox/CompanionSandbox'
import { DecisionLab } from './features/decision-lab/DecisionLab'
import { MethodCompare } from './features/method-compare/MethodCompare'
import { RunLog } from './features/run-log/RunLog'
import { ScenarioExplorer } from './features/scenario-explorer/ScenarioExplorer'
import { StudyPage } from './features/study/StudyPage'

export function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<OverviewPage />} />
        <Route path="/scenarios" element={<ScenarioExplorer />} />
        <Route path="/lab/:scenarioId" element={<DecisionLab />} />
        <Route path="/compare/:scenarioId" element={<MethodCompare />} />
        <Route path="/sandbox" element={<CompanionSandbox />} />
        <Route path="/study" element={<StudyPage />} />
        <Route path="/runs" element={<RunLog />} />
        <Route path="*" element={<OverviewPage />} />
      </Routes>
    </Layout>
  )
}
