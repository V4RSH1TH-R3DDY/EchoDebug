import React from 'react';
import type { Intent, Symbol, LintError, CodeFix } from '../types/types';
import './ResultsPanel.css';

interface ResultsPanelProps {
    intent?: Intent;
    symbols?: Symbol[];
    errors?: LintError[];
    fix?: CodeFix;
    isLoading?: boolean;
}

export const ResultsPanel: React.FC<ResultsPanelProps> = ({
    intent,
    symbols,
    errors,
    fix,
    isLoading,
}) => {
    if (isLoading) {
        return (
            <div className="results-panel">
                <div className="loading-state">
                    <div className="spinner-large" />
                    <p>Processing your request...</p>
                </div>
            </div>
        );
    }

    if (!intent && !symbols && !errors && !fix) {
        return (
            <div className="results-panel">
                <div className="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z" />
                        <path d="M12 6v6l4 2" />
                    </svg>
                    <h3>Ready to Debug</h3>
                    <p>Press and hold the microphone to start voice debugging</p>
                </div>
            </div>
        );
    }

    return (
        <div className="results-panel fade-in">
            {intent && (
                <div className="result-card glass">
                    <div className="card-header">
                        <h3>Intent Detected</h3>
                        <span className={`confidence-badge ${getConfidenceClass(intent.confidence)}`}>
                            {Math.round(intent.confidence * 100)}% confident
                        </span>
                    </div>
                    <div className="card-content">
                        <div className="intent-type">{intent.intent.replace(/_/g, ' ')}</div>
                        {Object.keys(intent.entities).length > 0 && (
                            <div className="entities">
                                {Object.entries(intent.entities).map(([key, value]) => (
                                    value && (
                                        <div key={key} className="entity">
                                            <span className="entity-key">{key}:</span>
                                            <span className="entity-value">{value}</span>
                                        </div>
                                    )
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {symbols && symbols.length > 0 && (
                <div className="result-card glass">
                    <div className="card-header">
                        <h3>Symbols Found</h3>
                        <span className="count-badge">{symbols.length} results</span>
                    </div>
                    <div className="card-content">
                        <div className="symbols-list">
                            {symbols.map((symbol, index) => (
                                <div key={index} className="symbol-item">
                                    <div className="symbol-header">
                                        <span className={`symbol-kind ${symbol.kind}`}>{symbol.kind}</span>
                                        <code className="symbol-name">{symbol.name}</code>
                                    </div>
                                    <div className="symbol-location">
                                        {symbol.file}:{symbol.line}
                                    </div>
                                    {symbol.signature && (
                                        <code className="symbol-signature">{symbol.signature}</code>
                                    )}
                                    {symbol.docstring && (
                                        <p className="symbol-doc">{symbol.docstring}</p>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {errors && errors.length > 0 && (
                <div className="result-card glass">
                    <div className="card-header">
                        <h3>Errors Detected</h3>
                        <span className="count-badge error">{errors.length} issues</span>
                    </div>
                    <div className="card-content">
                        <div className="errors-list">
                            {errors.map((error, index) => (
                                <div key={index} className={`error-item ${error.type}`}>
                                    <div className="error-header">
                                        <span className={`error-type ${error.type}`}>{error.type}</span>
                                        <span className="error-source">{error.source}</span>
                                    </div>
                                    <div className="error-location">
                                        {error.file}:{error.line}
                                        {error.column && `:${error.column}`}
                                    </div>
                                    <p className="error-message">{error.message}</p>
                                    {error.code && <code className="error-code">{error.code}</code>}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {fix && (
                <div className="result-card glass">
                    <div className="card-header">
                        <h3>Proposed Fix</h3>
                        <span className={`risk-badge ${fix.risk_level}`}>{fix.risk_level} risk</span>
                    </div>
                    <div className="card-content">
                        <p className="fix-rationale">{fix.rationale}</p>
                        <div className="fix-diff">
                            <pre><code>{fix.diff}</code></pre>
                        </div>
                        {fix.files_affected.length > 0 && (
                            <div className="affected-files">
                                <strong>Files affected:</strong>
                                <ul>
                                    {fix.files_affected.map((file, index) => (
                                        <li key={index}>{file}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

function getConfidenceClass(confidence: number): string {
    if (confidence >= 0.8) return 'high';
    if (confidence >= 0.5) return 'medium';
    return 'low';
}
