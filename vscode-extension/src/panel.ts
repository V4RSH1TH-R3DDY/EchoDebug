import * as vscode from 'vscode';

export class EchoDebugPanel {
    public static currentPanel: EchoDebugPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._panel.webview.html = this._getHtmlContent();
    }

    public static createOrShow(extensionUri: vscode.Uri) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (EchoDebugPanel.currentPanel) {
            EchoDebugPanel.currentPanel._panel.reveal(column);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'echodebugPanel',
            'EchoDebug',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        EchoDebugPanel.currentPanel = new EchoDebugPanel(panel, extensionUri);
    }

    public postMessage(message: any) {
        this._panel.webview.postMessage(message);
    }

    public dispose() {
        EchoDebugPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }

    private _getHtmlContent(): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EchoDebug</title>
    <style>
        body {
            padding: 20px;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
        }
        h1 { margin-top: 0; }
        .command-history {
            margin-top: 20px;
            border-top: 1px solid var(--vscode-panel-border);
            padding-top: 20px;
        }
        .command-item {
            padding: 10px;
            margin: 10px 0;
            background: var(--vscode-editor-background);
            border-radius: 4px;
        }
        .command-text {
            font-weight: bold;
            color: var(--vscode-textLink-foreground);
        }
        .command-result {
            margin-top: 8px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <h1>🎙️ EchoDebug</h1>
    <p>Voice-controlled AI debugger</p>
    
    <div class="command-history">
        <h2>Command History</h2>
        <div id="history"></div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        window.addEventListener('message', event => {
            const message = event.data;
            
            if (message.type === 'result') {
                addToHistory(message);
            }
        });

        function addToHistory(message) {
            const history = document.getElementById('history');
            const item = document.createElement('div');
            item.className = 'command-item';
            
            item.innerHTML = \`
                <div class="command-text">Intent: \${message.intent}</div>
                <div class="command-result">
                    <pre>\${JSON.stringify(message.data, null, 2)}</pre>
                </div>
            \`;
            
            history.insertBefore(item, history.firstChild);
        }
    </script>
</body>
</html>`;
    }
}
