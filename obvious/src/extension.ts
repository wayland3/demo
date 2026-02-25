import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
	vscode.commands.registerCommand('fix.obvious', () => {
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

		let selection = editor.selection;
		let text = editor.document.getText(selection);
		if (!text) {
			return;
		}

		// 替换\\n为\n,替换\\t为\t
		text = text.replace(/\\n/g, '\n').replace(/\\t/g, '\t');

		editor.edit((editBuilder) => {
			editBuilder.replace(selection, text);
		});
	});
}

export function deactivate() { }
