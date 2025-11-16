import * as vscode from 'vscode';

export class CodeHighlighter {
    private decorationType: vscode.TextEditorDecorationType;
    private activeDecorations: Map<vscode.TextEditor, vscode.Range[]> = new Map();

    constructor() {
        const config = vscode.workspace.getConfiguration('echodebug');
        const highlightColor = config.get<string>('highlightColor', '#ffd70080');

        this.decorationType = vscode.window.createTextEditorDecorationType({
            backgroundColor: highlightColor,
            border: '1px solid #ffd700',
            borderRadius: '3px'
        });
    }

    highlightSymbols(symbols: any[]): void {
        this.clearAll();

        const editorsByFile = new Map<string, vscode.TextEditor>();
        
        // Group symbols by file
        const symbolsByFile = new Map<string, any[]>();
        for (const symbol of symbols) {
            const file = symbol.file;
            if (!symbolsByFile.has(file)) {
                symbolsByFile.set(file, []);
            }
            symbolsByFile.get(file)!.push(symbol);
        }

        // Highlight in each file
        for (const [file, fileSymbols] of symbolsByFile) {
            const editor = this.findEditorForFile(file);
            if (editor) {
                this.highlightInEditor(editor, fileSymbols);
            }
        }
    }

    highlightInEditor(editor: vscode.TextEditor, symbols: any[]): void {
        const ranges: vscode.Range[] = [];

        for (const symbol of symbols) {
            const line = Math.max(0, symbol.line - 1);
            const startPos = new vscode.Position(line, symbol.column || 0);
            
            // Try to get the actual symbol length
            const lineText = editor.document.lineAt(line).text;
            const symbolName = symbol.name || '';
            const symbolIndex = lineText.indexOf(symbolName, symbol.column || 0);
            
            let endPos: vscode.Position;
            if (symbolIndex >= 0) {
                endPos = new vscode.Position(line, symbolIndex + symbolName.length);
            } else {
                // Fallback: highlight entire line
                endPos = new vscode.Position(line, lineText.length);
            }

            ranges.push(new vscode.Range(startPos, endPos));
        }

        editor.setDecorations(this.decorationType, ranges);
        this.activeDecorations.set(editor, ranges);

        // Reveal first occurrence
        if (ranges.length > 0) {
            editor.revealRange(ranges[0], vscode.TextEditorRevealType.InCenter);
        }
    }

    highlightRange(editor: vscode.TextEditor, line: number, startCol: number, endCol: number): void {
        const range = new vscode.Range(
            new vscode.Position(line - 1, startCol),
            new vscode.Position(line - 1, endCol)
        );
        
        editor.setDecorations(this.decorationType, [range]);
        this.activeDecorations.set(editor, [range]);
    }

    clearAll(): void {
        for (const editor of this.activeDecorations.keys()) {
            editor.setDecorations(this.decorationType, []);
        }
        this.activeDecorations.clear();
    }

    clearEditor(editor: vscode.TextEditor): void {
        editor.setDecorations(this.decorationType, []);
        this.activeDecorations.delete(editor);
    }

    private findEditorForFile(file: string): vscode.TextEditor | undefined {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceFolder) {
            return undefined;
        }

        const fullPath = `${workspaceFolder}/${file}`;
        
        return vscode.window.visibleTextEditors.find(editor => 
            editor.document.uri.fsPath.endsWith(file) ||
            editor.document.uri.fsPath === fullPath
        );
    }
}
