import * as vscode from 'vscode';
import { EchoDebugPanel } from './panel';
import { BackendClient } from './backendClient';
import { VoiceRecorder } from './voiceRecorder';
import { CodeHighlighter } from './codeHighlighter';

let backendClient: BackendClient;
let voiceRecorder: VoiceRecorder;
let codeHighlighter: CodeHighlighter;
let statusBarItem: vscode.StatusBarItem;

export function activate(context: vscode.ExtensionContext) {
    console.log('EchoDebug extension activated');

    // Initialize components
    const config = vscode.workspace.getConfiguration('echodebug');
    const backendUrl = config.get<string>('backendUrl', 'http://localhost:8000');
    
    backendClient = new BackendClient(backendUrl);
    voiceRecorder = new VoiceRecorder();
    codeHighlighter = new CodeHighlighter();

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'echodebug.talk';
    statusBarItem.text = '$(mic) EchoDebug';
    statusBarItem.tooltip = 'Click to start voice command (Ctrl+Shift+V)';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('echodebug.talk', () => startVoiceCommand(context))
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('echodebug.stopListening', () => stopListening())
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('echodebug.explainSelection', () => explainSelection())
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('echodebug.findSymbol', () => findSymbol())
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('echodebug.buildIndex', () => buildIndex())
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('echodebug.showPanel', () => {
            EchoDebugPanel.createOrShow(context.extensionUri);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('echodebug.openSettings', () => {
            vscode.commands.executeCommand('workbench.action.openSettings', 'echodebug');
        })
    );

    // Check backend connection
    checkBackendConnection();

    // Build index on activation
    setTimeout(() => buildIndex(true), 2000);
}

async function startVoiceCommand(context: vscode.ExtensionContext) {
    try {
        statusBarItem.text = '$(mic-filled) Listening...';
        statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');

        // Show input box as placeholder for voice input
        const text = await vscode.window.showInputBox({
            prompt: 'Enter voice command (Voice recording coming soon)',
            placeHolder: 'e.g., find all errors in main.py'
        });

        statusBarItem.text = '$(mic) EchoDebug';
        statusBarItem.backgroundColor = undefined;

        if (!text) {
            return;
        }

        // Process command
        await processCommand(text, context);

    } catch (error) {
        vscode.window.showErrorMessage(`EchoDebug error: ${error}`);
        statusBarItem.text = '$(mic) EchoDebug';
        statusBarItem.backgroundColor = undefined;
    }
}

function stopListening() {
    voiceRecorder.stop();
    statusBarItem.text = '$(mic) EchoDebug';
    statusBarItem.backgroundColor = undefined;
}

async function processCommand(text: string, context: vscode.ExtensionContext) {
    try {
        // Show processing
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'EchoDebug',
            cancellable: false
        }, async (progress) => {
            progress.report({ message: 'Processing command...' });

            // Get current file context
            const editor = vscode.window.activeTextEditor;
            const currentFile = editor?.document.fileName;
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;

            // Parse intent
            const intent = await backendClient.parseIntent(text, {
                current_file: currentFile,
                workspace: workspaceFolder
            });

            progress.report({ message: `Intent: ${intent.intent}` });

            // Route and execute
            const result = await backendClient.routeIntent(text);

            // Handle result based on intent
            await handleResult(intent, result, context);

            vscode.window.showInformationMessage(`✓ ${intent.intent} completed`);
        });

    } catch (error: any) {
        vscode.window.showErrorMessage(`Command failed: ${error.message}`);
    }
}

async function handleResult(intent: any, result: any, context: vscode.ExtensionContext) {
    const intentType = intent.intent;

    switch (intentType) {
        case 'find_symbol':
            await handleFindSymbol(result);
            break;
        
        case 'find_errors':
            await handleFindErrors(result);
            break;
        
        case 'explain_code':
            await handleExplainCode(result);
            break;
        
        case 'run_tests':
            await handleRunTests(result);
            break;
        
        default:
            // Show generic result
            EchoDebugPanel.createOrShow(context.extensionUri);
            EchoDebugPanel.currentPanel?.postMessage({
                type: 'result',
                intent: intentType,
                data: result
            });
    }
}

async function handleFindSymbol(result: any) {
    if (result.status === 'success' && result.result) {
        const symbols = Array.isArray(result.result) ? result.result : result.result.symbols || [];
        
        if (symbols.length === 0) {
            vscode.window.showInformationMessage('No symbols found');
            return;
        }

        // Show quick pick
        const items = symbols.map((sym: any) => ({
            label: sym.name || 'Unknown',
            description: `${sym.kind} in ${sym.file}`,
            detail: `Line ${sym.line}${sym.signature ? ': ' + sym.signature : ''}`,
            symbol: sym
        }));

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: `Found ${symbols.length} symbol(s)`
        });

        if (selected) {
            // Navigate to symbol
            await navigateToLocation(selected.symbol.file, selected.symbol.line);
        }

        // Highlight all occurrences
        codeHighlighter.highlightSymbols(symbols);
    }
}

async function handleFindErrors(result: any) {
    vscode.window.showInformationMessage('Error detection: ' + (result.message || 'Not yet implemented'));
}

async function handleExplainCode(result: any) {
    const explanation = result.message || result.explanation || 'No explanation available';
    
    const panel = vscode.window.createWebviewPanel(
        'echodebugExplanation',
        'Code Explanation',
        vscode.ViewColumn.Beside,
        {}
    );

    panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { padding: 20px; font-family: var(--vscode-font-family); }
                h2 { color: var(--vscode-foreground); }
                p { line-height: 1.6; }
            </style>
        </head>
        <body>
            <h2>Code Explanation</h2>
            <p>${explanation}</p>
        </body>
        </html>
    `;
}

async function handleRunTests(result: any) {
    const output = result.stdout || result.stderr || 'No output';
    const exitCode = result.exit || 0;
    
    const channel = vscode.window.createOutputChannel('EchoDebug Tests');
    channel.clear();
    channel.appendLine('=== Test Results ===');
    channel.appendLine(output);
    channel.appendLine(`\nExit code: ${exitCode}`);
    channel.show();
}

async function navigateToLocation(file: string, line: number) {
    try {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceFolder) {
            return;
        }

        const filePath = vscode.Uri.file(`${workspaceFolder}/${file}`);
        const document = await vscode.workspace.openTextDocument(filePath);
        const editor = await vscode.window.showTextDocument(document);
        
        const position = new vscode.Position(Math.max(0, line - 1), 0);
        editor.selection = new vscode.Selection(position, position);
        editor.revealRange(new vscode.Range(position, position), vscode.TextEditorRevealType.InCenter);
        
    } catch (error) {
        vscode.window.showErrorMessage(`Cannot open file: ${file}`);
    }
}

async function explainSelection() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No active editor');
        return;
    }

    const selection = editor.selection;
    const text = editor.document.getText(selection);
    
    if (!text) {
        vscode.window.showWarningMessage('No code selected');
        return;
    }

    await processCommand(`explain this code: ${text}`, {} as any);
}

async function findSymbol() {
    const symbol = await vscode.window.showInputBox({
        prompt: 'Enter symbol name to find',
        placeHolder: 'e.g., userData, handleClick'
    });

    if (symbol) {
        await processCommand(`find symbol ${symbol}`, {} as any);
    }
}

async function buildIndex(silent: boolean = false) {
    try {
        if (!silent) {
            vscode.window.showInformationMessage('Building code index...');
        }

        const stats = await backendClient.buildIndex();
        
        if (!silent) {
            vscode.window.showInformationMessage(
                `Index built: ${stats.files_indexed} files, ${stats.symbols_found} symbols`
            );
        }
    } catch (error: any) {
        if (!silent) {
            vscode.window.showErrorMessage(`Index build failed: ${error.message}`);
        }
    }
}

async function checkBackendConnection() {
    try {
        const isConnected = await backendClient.checkConnection();
        if (isConnected) {
            statusBarItem.tooltip = 'EchoDebug: Connected';
        } else {
            statusBarItem.tooltip = 'EchoDebug: Backend not running';
            statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
        }
    } catch (error) {
        statusBarItem.tooltip = 'EchoDebug: Backend not running';
        statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
    }
}

export function deactivate() {
    codeHighlighter.clearAll();
}
