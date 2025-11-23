// Backend API Types

export interface Intent {
    intent: string;
    confidence: number;
    entities: {
        symbol?: string;
        file?: string;
        language?: string;
        scope?: 'reads' | 'writes' | 'declarations' | 'all';
        goal?: string;
        [key: string]: any;
    };
    follow_up_allowed: boolean;
}

export interface Symbol {
    name: string;
    kind: 'function' | 'class' | 'variable' | 'import' | 'method';
    file: string;
    line: number;
    signature?: string;
    docstring?: string;
}

export interface LintError {
    file: string;
    line: number;
    column?: number;
    message: string;
    type: 'error' | 'warning' | 'info';
    source: 'pylint' | 'mypy' | 'syntax';
    code?: string;
}

export interface CodeFix {
    diff: string;
    rationale: string;
    risk_level: 'low' | 'medium' | 'high';
    files_affected: string[];
}

export interface IndexStats {
    total_files: number;
    total_symbols: number;
    unique_symbols: number;
    index_time: number;
    last_updated: string;
}

export interface SearchResult {
    file: string;
    line: number;
    preview: string;
    match_type: string;
}

export interface TranscriptionResult {
    text: string;
    confidence?: number;
}

export interface CommandHistoryItem {
    id: string;
    timestamp: number;
    command: string;
    intent?: Intent;
    result?: any;
    status: 'success' | 'error' | 'pending';
}

export interface BackendStatus {
    connected: boolean;
    lastChecked: number;
    version?: string;
}

// UI State Types
export type ViewMode = 'voice' | 'results' | 'history';

export interface AppState {
    isRecording: boolean;
    isProcessing: boolean;
    currentView: ViewMode;
    backendStatus: BackendStatus;
    error: string | null;
}
