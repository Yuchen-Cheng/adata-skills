#!/usr/bin/env node

/**
 * list-patterns.js
 * 
 * Scans layouts/patterns/ and lists all pattern names + "When to use" descriptions.
 * Usage: node scripts/list-patterns.js
 */

const fs = require('fs');
const path = require('path');

// Skill root directory
const skillRoot = path.join(__dirname, '..');
const patternsDir = path.join(skillRoot, 'layouts', 'patterns');

// Pattern file regex (no letter prefix)
const patternFileRegex = /^pattern-(.+)\.md$/;

try {
  // Read all files in patterns directory
  const files = fs.readdirSync(patternsDir).sort();
  
  console.log('\n╔════════════════════════════════════════════════════════════════╗');
  console.log('║                    AVAILABLE PATTERNS                          ║');
  console.log('╠════════════════════════════════════════════════════════════════╣');
  
  const patterns = [];
  
  files.forEach(file => {
    const match = file.match(patternFileRegex);
    if (match) {
      const filePath = path.join(patternsDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      
      // Extract title (first line starting with "# Pattern")
      const titleMatch = content.match(/^# Pattern — (.+?)$/m);
      
      // Extract "When to use" text (from **When to use:** until next heading or blank line + heading)
      const whenMatch = content.match(/\*\*When to use:\*\* ([^\n]+(?:\n[^\n]+)*?)(?:\n\n## |$)/m);
      
      if (titleMatch && whenMatch) {
        const fullName = titleMatch[1];
        // Clean up: remove markdown, limit to first 2 lines max
        let whenText = whenMatch[1].trim();
        whenText = whenText.replace(/\*\*([^*]+)\*\*/g, '$1'); // remove bold
        whenText = whenText.replace(/\`([^`]+)\`/g, '$1'); // remove code blocks
        whenText = whenText.split('\n').slice(0, 2).join(' ').trim(); // take first 2 lines
        
        patterns.push({
          fullName,
          whenText,
          file
        });
      }
    }
  });
  
  // Sort by file name
  patterns.sort((a, b) => a.file.localeCompare(b.file));
  
  // Print each pattern
  patterns.forEach(p => {
    console.log(`║                                                                ║`);
    console.log(`║  ${p.fullName}`);
    console.log(`║  ─────────────────────────────────────────────────────────────║`);
    
    // Wrap "When to use" text to fit console width
    const maxLineLen = 60;
    const words = p.whenText.split(/\s+/);
    let currentLine = '';
    
    words.forEach(word => {
      if ((currentLine + ' ' + word).length > maxLineLen) {
        console.log(`║  ${currentLine.padEnd(60)}║`);
        currentLine = word;
      } else {
        currentLine = currentLine ? currentLine + ' ' + word : word;
      }
    });
    
    if (currentLine) {
      console.log(`║  ${currentLine.padEnd(60)}║`);
    }
  });
  
  console.log(`║                                                                ║`);
  console.log('╚════════════════════════════════════════════════════════════════╝');
  console.log(`\nTotal: ${patterns.length} patterns\n`);
  
} catch (err) {
  console.error('Error reading patterns directory:', err.message);
  process.exit(1);
}
