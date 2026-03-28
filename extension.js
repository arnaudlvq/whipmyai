// @ts-check
'use strict';

const vscode = require('vscode');
const path = require('path');
const { spawn } = require('child_process');

/** @type {boolean} */
let enabled = true;

/** @type {string[]} */
let sounds;

function playWhip() {
    const sound = sounds[Math.floor(Math.random() * sounds.length)];
    spawn('afplay', [sound], { detached: true, stdio: 'ignore' }).unref();
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    sounds = ['whip.mp3', 'whip2.mp3', 'whip3.mp3'].map(
        f => path.join(context.extensionPath, f)
    );

    // Toggle command
    const toggleCmd = vscode.commands.registerCommand('whipmyai.toggle', () => {
        enabled = !enabled;
        vscode.window.setStatusBarMessage(
            enabled ? '$(unmute) WhipMyAI: ON' : '$(mute) WhipMyAI: OFF',
            3000
        );
    });

    // Fires when the user presses Enter in any VS Code chat input (panel chat, inline chat, etc.)
    // The keybinding in package.json routes Enter → this command → plays sound + submits.
    const submitChatCmd = vscode.commands.registerCommand('whipmyai.submitChat', async () => {
        if (enabled) playWhip();
        try {
            await vscode.commands.executeCommand('workbench.action.chat.submit');
        } catch {
            // chat not available, nothing to do
        }
    });

    context.subscriptions.push(toggleCmd, submitChatCmd);
}

function deactivate() {}

module.exports = { activate, deactivate };
