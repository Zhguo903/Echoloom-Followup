import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { App } from '../App'
import { LanguageProvider } from '../i18n'

function renderApp(path = '/') {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[path]}>
        <LanguageProvider>
          <App />
        </LanguageProvider>
      </MemoryRouter>
    </QueryClientProvider>,
  )
}

test('renders claim boundary and switches language', async () => {
  renderApp()
  expect(screen.getByText('Correct recall is not the same as appropriate use.')).toBeInTheDocument()
  await userEvent.click(screen.getByRole('button', { name: 'Switch language' }))
  expect(screen.getByText('正确记住，不等于适合在此刻提起。')).toBeInTheDocument()
})

test('sandbox adds and safely renders a synthetic memory', async () => {
  renderApp('/sandbox')
  const input = screen.getByLabelText('New synthetic memory')
  await userEvent.type(input, '<script>alert(1)</script> synthetic note')
  await userEvent.click(screen.getByRole('button', { name: 'Add' }))
  expect(screen.getByDisplayValue('<script>alert(1)</script> synthetic note')).toBeInTheDocument()
  expect(document.querySelectorAll('script')).toHaveLength(0)
})

test('study page is visibly locked', () => {
  renderApp('/study')
  expect(screen.getByText('Participant collection is locked.')).toBeInTheDocument()
  expect(screen.getByText('BBI_STUDY_MODE=false')).toBeInTheDocument()
})
