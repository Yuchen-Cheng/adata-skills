#!/usr/bin/env node

/**
 * list-templates.js
 * 
 * Scans layouts/template/ and lists all template names + descriptions/metadata.
 * Usage: node scripts/list-templates.js
 */

const fs = require('fs');
const path = require('path');

// Skill root directory
const skillRoot = path.join(__dirname, '..');
const templateDir = path.join(skillRoot, 'layouts', 'template');

// Template file regex
const templateFileRegex = /^([a-z0-9][a-z0-9-]*)\.md$/;

try {
  // Read all files in template directory
  const files = fs.readdirSync(templateDir).sort();
  
  console.log('\n╔════════════════════════════════════════════════════════════════╗');
  console.log('║                    AVAILABLE TEMPLATES                         ║');
  console.log('╠════════════════════════════════════════════════════════════════╣');
  
  const templates = [];
  
  files.forEach(file => {
    const match = file.match(templateFileRegex);
    if (match) {
      const filePath = path.join(templateDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      
      // Extract template title (first line starting with "# Template:")
      const titleMatch = content.match(/^# Template: (.+?)$/m);
      
      // Extract template ID
      const idMatch = content.match(/\*\*Template ID:\*\*\s+`([^`]+)`/);
      
      // Extract background count
      const bgCountMatch = content.match(/\*\*Background count:\*\*\s+(\d+)/);
      
      if (titleMatch && idMatch) {
        const fullName = titleMatch[1].trim();
        const templateId = idMatch[1].trim();
        const bgCount = bgCountMatch ? bgCountMatch[1] : 'N/A';
        
        // Try to extract a brief description from first paragraph after title
        const descMatch = content.match(/^# Template:.+?\n\n(.+?)(?:\n\n|\n---)/s);
        let description = '';
        if (descMatch) {
          description = descMatch[1]
            .replace(/\*\*[^*]+:\*\*\s+`[^`]+`\s+/g, '')
            .replace(/\*\*[^*]+:\*\*\s+\d+\s*/g, '')
            .trim();
        }
        
        templates.push({
          templateId,
          fullName,
          bgCount,
          description,
          file
        });
      }
    }
  });
  
  // Print each template
  if (templates.length === 0) {
    console.log('║                    No templates found                         ║');
  } else {
    templates.forEach(t => {
      console.log(`║                                                                ║`);
      console.log(`║  [${t.templateId.toUpperCase()}] ${t.fullName}`);
      console.log(`║  ─────────────────────────────────────────────────────────────║`);
      
      // Print metadata
      console.log(`║  Background images: ${t.bgCount} slides`);
      
      if (t.description) {
        // Wrap description text to fit console width
        const maxLineLen = 60;
        const words = t.description.split(/\s+/);
        let currentLine = '';
        
        words.forEach(word => {
          if ((currentLine + ' ' + word).length > maxLineLen) {
            if (currentLine) console.log(`║  ${currentLine.padEnd(60)}║`);
            currentLine = word;
          } else {
            currentLine = currentLine ? currentLine + ' ' + word : word;
          }
        });
        
        if (currentLine) {
          console.log(`║  ${currentLine.padEnd(60)}║`);
        }
      }
    });
  }
  
  console.log(`║                                                                ║`);
  console.log('╚════════════════════════════════════════════════════════════════╝');
  console.log(`\nTotal: ${templates.length} template(s)\n`);
  
} catch (err) {
  console.error('Error reading template directory:', err.message);
  process.exit(1);
}
