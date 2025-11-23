import { useState, useEffect, useCallback } from 'react';
import { VoiceRecorder } from './components/VoiceRecorder';
import { ResultsPanel } from './components/ResultsPanel';
import { CommandHistory } from './components/CommandHistory';
import { useBackendStatus } from './hooks/useBackendStatus';
import { apiClient } from './services/apiClient';
import type { Intent, Symbol, LintError, CodeFix, CommandHistoryItem } from './types/types';
import './App.css';

function App() {
  const { status } = useBackendStatus();
  const [currentTranscript, setCurrentTranscript] = useState('');
  const [intent, setIntent] = useState<Intent | undefined>();
  const [symbols, setSymbols] = useState<Symbol[] | undefined>();
  const [errors, setErrors] = useState<LintError[] | undefined>();
  const [fix, setFix] = useState<CodeFix | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<CommandHistoryItem[]>([]);

  // Load history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('echodebug-history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to load history:', e);
      }
    }
  }, []);

  // Save history to localStorage
  useEffect(() => {
    localStorage.setItem('echodebug-history', JSON.stringify(history));
  }, [history]);

  const addToHistory = useCallback((
    command: string,
    intent?: Intent,
    result?: any,
    status: 'success' | 'error' | 'pending' = 'success'
  ) => {
    const item: CommandHistoryItem = {
      id: Date.now().toString(),
      timestamp: Date.now(),
      command,
      intent,
      result,
      status,
    };
    setHistory((prev) => [item, ...prev].slice(0, 50)); // Keep last 50
  }, []);

  const handleTranscription = useCallback(async (text: string) => {
    setCurrentTranscript(text);
    setError(null);
    setIsLoading(true);

    // Clear previous results
    setIntent(undefined);
    setSymbols(undefined);
    setErrors(undefined);
    setFix(undefined);

    try {
      // Parse intent
      const parsedIntent = await apiClient.parseIntent(text);
      setIntent(parsedIntent);

      // Route based on intent
      switch (parsedIntent.intent) {
        case 'find_symbol':
          if (parsedIntent.entities.symbol) {
            const result = await apiClient.searchSymbols(parsedIntent.entities.symbol);
            setSymbols(result.symbols);
            addToHistory(text, parsedIntent, result, 'success');
          }
          break;

        case 'find_errors':
          if (parsedIntent.entities.file) {
            const result = await apiClient.lintFile(parsedIntent.entities.file);
            setErrors(result.errors);
            addToHistory(text, parsedIntent, result, 'success');
          }
          break;

        case 'propose_fix':
          if (parsedIntent.entities.file && parsedIntent.entities.goal) {
            const result = await apiClient.proposeFix(
              parsedIntent.entities.file,
              parsedIntent.entities.goal
            );
            setFix(result);
            addToHistory(text, parsedIntent, result, 'success');
          }
          break;

        default:
          addToHistory(text, parsedIntent, null, 'success');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Request failed';
      setError(errorMessage);
      addToHistory(text, undefined, null, 'error');
    } finally {
      setIsLoading(false);
    }
  }, [addToHistory]);

  const handleError = useCallback((errorMessage: string) => {
    setError(errorMessage);
  }, []);

  const handleReplay = useCallback((command: string) => {
    setCurrentTranscript(command);
    handleTranscription(command);
  }, [handleTranscription]);

  const handleClearHistory = useCallback(() => {
    setHistory([]);
    localStorage.removeItem('echodebug-history');
  }, []);

  return (
    <div className="app">
      <header className="app-header glass">
        <div className="header-content">
          <div className="logo">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
              <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
              <line x1="12" y1="19" x2="12" y2="23" />
              <line x1="8" y1="23" x2="16" y2="23" />
            </svg>
            <h1>
              <span className="gradient-text">Echo</span>Debug
            </h1>
          </div>
          <div className="header-status">
            <div className={`status-indicator ${status.connected ? 'connected' : 'disconnected'}`}>
              <div className="status-dot" />
              <span>{status.connected ? 'Connected' : 'Disconnected'}</span>
            </div>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="main-content">
          <div className="voice-section">
            <VoiceRecorder onTranscription={handleTranscription} onError={handleError} />
            {currentTranscript && (
              <div className="transcript-display glass fade-in">
                <div className="transcript-label">You said:</div>
                <div className="transcript-text">"{currentTranscript}"</div>
              </div>
            )}
            {error && (
              <div className="error-banner fade-in">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
                </svg>
                {error}
              </div>
            )}
          </div>

          <ResultsPanel
            intent={intent}
            symbols={symbols}
            errors={errors}
            fix={fix}
            isLoading={isLoading}
          />
        </div>

        <aside className="sidebar">
          <CommandHistory
            history={history}
            onReplay={handleReplay}
            onClear={handleClearHistory}
          />
        </aside>
      </main>
    </div>
  );
}

export default App;
