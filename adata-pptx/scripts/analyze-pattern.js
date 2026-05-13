#!/usr/bin/env node

/**
 * analyze-pattern.js
 * 
 * Analyzes a user-provided pattern example PPTX file:
 * - Extracts content layout information from slides
 * - Provides coordinate data and visual structure
 * - Helps create new pattern definitions
 * 
 * Usage: node scripts/analyze-pattern.js <path-to-example.pptx> [slide-number]
 * 
 * Example:
 *   node scripts/analyze-pattern.js pattern-example.pptx
 *   node scripts/analyze-pattern.js pattern-example.pptx 1
 */

const fs = require('fs');
const path = require('path');
const AdmZip = require('adm-zip');

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('Usage: node scripts/analyze-pattern.js <path-to-example.pptx> [slide-number]');
  console.error('');
  console.error('Example:');
  console.error('  node scripts/analyze-pattern.js pattern-example.pptx');
  console.error('  node scripts/analyze-pattern.js pattern-example.pptx 1');
  console.error('');
  console.error('Output:');
  console.error('  • Lists all slides and their content');
  console.error('  • Shows text boxes, shapes, and coordinates');
  console.error('  • Analyzes layout structure for pattern creation');
  process.exit(1);
}

const pptxFile = args[0];
const slideNumber = args[1] ? parseInt(args[1]) : null;

// Verify file exists
if (!fs.existsSync(pptxFile)) {
  console.error(`Error: File not found: ${pptxFile}`);
  process.exit(1);
}

try {
  console.log(`\n📂 Analyzing Pattern Example: ${pptxFile}\n`);
  
  // Read PPTX file as ZIP
  const zip = new AdmZip(pptxFile);
  
  // Get all slide files
  const slideEntries = zip.getEntries()
    .filter(entry => entry.entryName.match(/^ppt\/slides\/slide\d+\.xml$/))
    .sort((a, b) => {
      const numA = parseInt(a.entryName.match(/\d+/)[0]);
      const numB = parseInt(b.entryName.match(/\d+/)[0]);
      return numA - numB;
    });
  
  console.log(`📋 Found ${slideEntries.length} slides\n`);
  
  if (slideNumber && (slideNumber < 1 || slideNumber > slideEntries.length)) {
    console.error(`Error: Slide ${slideNumber} not found. Available: 1-${slideEntries.length}`);
    process.exit(1);
  }
  
  const selectedSlides = slideNumber 
    ? [slideEntries[slideNumber - 1]]
    : slideEntries;
  
  // Analyze each selected slide
  selectedSlides.forEach((entry, idx) => {
    const slideNum = parseInt(entry.entryName.match(/\d+/)[0]);
    const xmlContent = entry.getData().toString('utf-8');
    
    console.log(`\n${'='.repeat(70)}`);
    console.log(`📄 Slide ${slideNum}`);
    console.log(`${'='.repeat(70)}\n`);
    
    analyzeSlideXml(xmlContent, slideNum);
  });
  
  console.log(`\n${'='.repeat(70)}`);
  console.log(`✅ Analysis Complete!\n`);
  
  console.log(`📚 Next Steps:`);
  console.log(`   1. Review the slide content structure above`);
  console.log(`   2. Note the text box coordinates and sizes`);
  console.log(`   3. Create layouts/patterns/pattern-<name>.md with:`);
  console.log(`      - Pattern name and description`);
  console.log(`      - "When to use" section (independent description)`);
  console.log(`      - Visual Structure (ASCII art or text)`);
  console.log(`      - Key Elements table (coordinates, fonts, colors)`);
  console.log(`      - pptxgenjs Code block`);
  console.log(`   4. Run: node scripts/list-patterns.js to verify`);
  
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}

/**
 * Analyze slide XML and extract text boxes and shapes
 */
function analyzeSlideXml(xmlContent, slideNum) {
  // Simple XML parsing for common slide elements
  // Extract text shapes
  
  const textPattern = /<a:t>([^<]+)<\/a:t>/g;
  const shapePattern = /<p:sp>([\s\S]*?)<\/p:sp>/g;
  
  const texts = [];
  let match;
  
  // Extract all text content
  while ((match = textPattern.exec(xmlContent)) !== null) {
    texts.push(match[1]);
  }
  
  console.log('📌 Text Content:');
  if (texts.length === 0) {
    console.log('   (no text found)');
  } else {
    texts.forEach((text, idx) => {
      console.log(`   ${idx + 1}. ${text.substring(0, 60)}${text.length > 60 ? '...' : ''}`);
    });
  }
  
  // Extract shape coordinates (EMU units: 1 inch = 914400 EMU)
  const coordPattern = /<a:off x="(\d+)" y="(\d+)"\/>\s*<a:ext cx="(\d+)" cy="(\d+)"/g;
  const coordinates = [];
  
  while ((match = coordPattern.exec(xmlContent)) !== null) {
    const x = Math.round(parseInt(match[1]) / 914400 * 100) / 100;
    const y = Math.round(parseInt(match[2]) / 914400 * 100) / 100;
    const w = Math.round(parseInt(match[3]) / 914400 * 100) / 100;
    const h = Math.round(parseInt(match[4]) / 914400 * 100) / 100;
    
    coordinates.push({ x, y, w, h });
  }
  
  console.log('\n📍 Coordinates (in inches, relative to slide 10"×5.625"):');
  if (coordinates.length === 0) {
    console.log('   (no coordinate data found)');
  } else {
    coordinates.forEach((coord, idx) => {
      console.log(`   Shape ${idx + 1}: x=${coord.x}, y=${coord.y}, w=${coord.w}, h=${coord.h}`);
    });
  }
  
  // Extract font sizes (in hundredths of a point)
  const fontPattern = /<a:rPr[^>]*sz="(\d+)"/g;
  const fontSizes = new Set();
  
  while ((match = fontPattern.exec(xmlContent)) !== null) {
    const pts = Math.round(parseInt(match[1]) / 100);
    fontSizes.add(pts);
  }
  
  console.log('\n🔤 Font Sizes Detected:');
  if (fontSizes.size === 0) {
    console.log('   (no font size data found)');
  } else {
    Array.from(fontSizes).sort((a, b) => b - a).forEach(size => {
      console.log(`   • ${size}pt`);
    });
  }
  
  // Extract colors (RGB format)
  const colorPattern = /<a:srgbClr val="([0-9A-F]{6})"/gi;
  const colors = new Set();
  
  while ((match = colorPattern.exec(xmlContent)) !== null) {
    colors.add(match[1].toUpperCase());
  }
  
  console.log('\n🎨 Colors Detected:');
  if (colors.size === 0) {
    console.log('   (no explicit color data found)');
  } else {
    Array.from(colors).forEach(color => {
      console.log(`   • #${color}`);
    });
  }
}
