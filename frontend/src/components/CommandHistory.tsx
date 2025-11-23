import React from 'react';
import type { CommandHistoryItem } from '../types/types';
import './CommandHistory.css';

interface CommandHistoryProps {
    history: CommandHistoryItem[];
    onReplay?: (command: string) => void;
    onClear?: () => void;
}

export const CommandHistory: React.FC<CommandHistoryProps> = ({
    history,
    onReplay,
    onClear,
}) => {
    const formatTime = (timestamp: number) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    return (
        <div className="command-history glass">
            <div className="history-header">
                <h3>Command History</h3>
                {history.length > 0 && (
                    <button className="clear-button" onClick={onClear} title="Clear history">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                        </svg>
                    </button>
                )}
            </div>

            <div className="history-list">
                {history.length === 0 ? (
                    <div className="empty-history">
                        <p>No commands yet</p>
                    </div>
                ) : (
                    history.map((item) => (
                        <div
                            key={item.id}
                            className={`history-item ${item.status}`}
                            onClick={() => onReplay?.(item.command)}
                        >
                            <div className="item-header">
                                <span className="item-time">{formatTime(item.timestamp)}</span>
                                <span className={`item-status ${item.status}`}>
                                    {item.status === 'success' && '✓'}
                                    {item.status === 'error' && '✗'}
                                    {item.status === 'pending' && '⋯'}
                                </span>
                            </div>
                            <div className="item-command">{item.command}</div>
                            {item.intent && (
                                <div className="item-intent">
                                    {item.intent.intent.replace(/_/g, ' ')}
                                </div>
                            )}
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};
