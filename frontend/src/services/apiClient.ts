import axios from 'axios';
import type { AxiosInstance } from 'axios';
import type {
    Intent,
    Symbol,
    LintError,
    CodeFix,
    IndexStats,
    SearchResult,
    TranscriptionResult,
} from '../types/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 30000,
        });
    }

    // Speech-to-Text
    async transcribeAudio(audioBlob: Blob): Promise<TranscriptionResult> {
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.wav');

        const response = await this.client.post<TranscriptionResult>('/stt/file', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    }

    // Intent Parsing
    async parseIntent(text: string): Promise<Intent> {
        const response = await this.client.post<Intent>('/intent', { text });
        return response.data;
    }

    async parseAndRoute(text: string): Promise<any> {
        const response = await this.client.post('/intent/route', { text });
        return response.data;
    }

    // Symbol Search
    async searchSymbols(name: string, lang: string = 'python'): Promise<{ symbols: Symbol[] }> {
        const response = await this.client.post<{ symbols: Symbol[] }>('/symbols', {
            name,
            lang,
        });
        return response.data;
    }

    async getFileSymbols(filePath: string): Promise<{ symbols: Symbol[] }> {
        const response = await this.client.get<{ symbols: Symbol[] }>(
            `/symbols/file/${encodeURIComponent(filePath)}`
        );
        return response.data;
    }

    async getSymbolReferences(name: string): Promise<{ references: any[] }> {
        const response = await this.client.get<{ references: any[] }>(
            `/symbols/${encodeURIComponent(name)}/references`
        );
        return response.data;
    }

    // Code Search
    async searchCode(query: string, lang: string = 'python'): Promise<{ results: SearchResult[] }> {
        const response = await this.client.post<{ results: SearchResult[] }>('/search', {
            query,
            lang,
        });
        return response.data;
    }

    // Error Detection
    async lintFile(file: string, lang: string = 'python'): Promise<{
        errors: LintError[];
        total_errors: number;
    }> {
        const response = await this.client.post<{
            errors: LintError[];
            total_errors: number;
        }>('/lint', {
            file,
            lang,
        });
        return response.data;
    }

    // Stack Trace Analysis
    async explainTrace(trace: string, snippets?: string[]): Promise<{
        summary: string;
        suspects: any[];
    }> {
        const response = await this.client.post<{
            summary: string;
            suspects: any[];
        }>('/explain-trace', {
            trace,
            snippets,
        });
        return response.data;
    }

    // Fix Generation
    async proposeFix(file: string, goal: string): Promise<CodeFix> {
        const response = await this.client.post<CodeFix>('/propose-fix', {
            file,
            goal,
        });
        return response.data;
    }

    async applyFix(diff: string): Promise<{ ok: boolean; files_changed: string[] }> {
        const response = await this.client.post<{ ok: boolean; files_changed: string[] }>(
            '/apply-fix',
            { diff }
        );
        return response.data;
    }

    // Code Indexing
    async buildIndex(): Promise<IndexStats> {
        const response = await this.client.post<IndexStats>('/index/build');
        return response.data;
    }

    async getIndexStats(): Promise<IndexStats> {
        const response = await this.client.get<IndexStats>('/index/stats');
        return response.data;
    }

    // Command Execution
    async runCommand(cmd: string, env?: Record<string, string>, timeout?: number): Promise<{
        exit_code: number;
        stdout: string;
        stderr: string;
    }> {
        const response = await this.client.post<{
            exit_code: number;
            stdout: string;
            stderr: string;
        }>('/run', {
            cmd,
            env,
            timeout,
        });
        return response.data;
    }

    // Health Check
    async healthCheck(): Promise<boolean> {
        try {
            const response = await this.client.get('/index/stats');
            return response.status === 200;
        } catch {
            return false;
        }
    }
}

export const apiClient = new ApiClient();
export default apiClient;
