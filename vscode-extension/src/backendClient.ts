import axios, { AxiosInstance } from 'axios';

export class BackendClient {
    private client: AxiosInstance;

    constructor(private baseUrl: string) {
        this.client = axios.create({
            baseURL: baseUrl,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    async checkConnection(): Promise<boolean> {
        try {
            const response = await this.client.get('/');
            return response.status === 200;
        } catch (error) {
            return false;
        }
    }

    async parseIntent(text: string, context?: any): Promise<any> {
        const response = await this.client.post('/intent', {
            text,
            context
        });
        return response.data;
    }

    async routeIntent(text: string, context?: any): Promise<any> {
        const response = await this.client.post('/intent/route', {
            text,
            context
        });
        return response.data;
    }

    async searchCode(query: string, lang: string = 'python'): Promise<any> {
        const response = await this.client.post('/search', {
            query,
            lang
        });
        return response.data;
    }

    async findSymbols(name: string, lang: string = 'python'): Promise<any> {
        const response = await this.client.post('/symbols', {
            name,
            lang
        });
        return response.data;
    }

    async runCommand(cmd: string, env?: any, timeout: number = 20): Promise<any> {
        const response = await this.client.post('/run', {
            cmd,
            env,
            timeout
        });
        return response.data;
    }

    async explainTrace(trace: string, snippets?: string[]): Promise<any> {
        const response = await this.client.post('/explain-trace', {
            trace,
            snippets
        });
        return response.data;
    }

    async buildIndex(force: boolean = false): Promise<any> {
        const response = await this.client.post('/index/build', null, {
            params: { force }
        });
        return response.data.stats;
    }

    async getIndexStats(): Promise<any> {
        const response = await this.client.get('/index/stats');
        return response.data;
    }

    async getFileSymbols(filePath: string): Promise<any> {
        const response = await this.client.get(`/symbols/file/${filePath}`);
        return response.data;
    }
}
