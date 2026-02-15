#!/usr/bin/env node
// Simple CLI wrapper for discord-context skill
// Handles: poll, context, link

const args = process.argv.slice(2);
const subcommand = args[0];

// Determine base directory - try multiple approaches
function getBaseDir() {
  // 1. Try to find workspace from current working directory
  const cwd = process.cwd();
  if (cwd.includes('.openclaw/workspace')) {
    return cwd;
  }
  
  // 2. Try HOME-based path
  const home = process.env.HOME || process.env.USERPROFILE;
  if (home) {
    return `${home}/.openclaw/workspace`;
  }
  
  // 3. Default
  return '/home/deploy/.openclaw/workspace';
}

const baseDir = getBaseDir();

const scripts = {
  poll: `${baseDir}/scripts/discord-context-poll.sh`,
  context: `${baseDir}/scripts/discord-context.sh`,
  link: `${baseDir}/scripts/discord-context.sh`
};

if (!subcommand || subcommand === '--help' || subcommand === '-h') {
  console.log(`
discord-context CLI

Usage: discord-context <command> [args]

Commands:
  poll              Poll for new thread activity
  context [id]      Show cached context for thread
  link <id> <qmd>  Link QMD to thread

Examples:
  discord-context poll
  discord-context context
  discord-context context 1472595645192867983
  discord-context link 1472595645192867983 skills
`);
  process.exit(0);
}

const script = scripts[subcommand];
if (!script) {
  console.error(`Unknown command: ${subcommand}`);
  console.log('Run discord-context --help for usage');
  process.exit(1);
}

const { execSync } = require('child_process');
try {
  const result = execSync(`${script} ${subcommand} ${args.slice(1).join(' ')}`, {
    cwd: baseDir,
    encoding: 'utf8'
  });
  console.log(result);
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
