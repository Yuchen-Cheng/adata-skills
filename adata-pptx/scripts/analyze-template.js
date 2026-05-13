#!/usr/bin/env node

/**
 * analyze-template.js
 * 
 * Analyzes a user-provided PPTX template file:
 * - Extracts images to assets/<template-name>_backgrounds/
 * - Extracts XML files for analysis
 * 
 * Usage: node scripts/analyze-template.js <path-to-file.pptx> <template-name>
 * 
 * Example:
 *   node scripts/analyze-template.js MyBrandedTemplate.pptx mytemplate
 *   → Extracts images to assets/mytemplate_backgrounds/
 *   → Extracts XML to pptx-analysis/<template-name>/xml/
 */

const fs = require('fs');
const path = require('path');
const AdmZip = require('adm-zip');

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length < 2) {
  console.error('Usage: node scripts/analyze-template.js <path-to-file.pptx> <template-name>');
  console.error('');
  console.error('Example:');
  console.error('  node scripts/analyze-template.js MyBrandedTemplate.pptx mytemplate');
  console.error('');
  console.error('Output:');
  console.error('  • Images → assets/mytemplate_backgrounds/');
  console.error('  • XML → pptx-analysis/mytemplate/xml/');
  process.exit(1);
}

const pptxFile = args[0];
const templateName = args[1];
const skillRoot = path.join(__dirname, '..');
const assetsDir = path.join(skillRoot, 'assets', `${templateName}_backgrounds`);
const analysisDir = path.join(skillRoot, '..', '..', 'pptx-analysis', templateName);

// Verify file exists
if (!fs.existsSync(pptxFile)) {
  console.error(`Error: File not found: ${pptxFile}`);
  process.exit(1);
}

try {
  console.log(`\n📂 Analyzing: ${pptxFile}`);
  console.log(`� Template Name: ${templateName}`);
  console.log(`📁 Assets Output: ${assetsDir}\n`);
  
  // Create output directories
  if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
    console.log(`✓ Created assets directory: assets/${templateName}_backgrounds/`);
  }
  
  const xmlDir = path.join(analysisDir, 'xml');
  if (!fs.existsSync(xmlDir)) {
    fs.mkdirSync(xmlDir, { recursive: true });
  }
  
  // Read PPTX file as ZIP
  const zip = new AdmZip(pptxFile);
  const zipEntries = zip.getEntries();
  
  // Counters
  let imageCount = 0;
  let xmlCount = 0;
  const extractedImages = [];
  
  console.log('📋 Extracting Images:\n');
  
  // Extract images and copy to assets folder
  zipEntries.forEach(entry => {
    const entryPath = entry.entryName;
    
    // Extract images
    if (entryPath.match(/^ppt\/media\//) && entry.isFile) {
      const fileName = path.basename(entryPath);
      const outputPath = path.join(assetsDir, fileName);
      
      // Extract image to assets folder
      fs.writeFileSync(outputPath, entry.getData());
      console.log(`  ✓ ${fileName}`);
      extractedImages.push(fileName);
      imageCount++;
    }
  });
  
  if (imageCount === 0) {
    console.log('  (no images found)');
  }
  
  console.log('');
  
  // Extract and save XML files
  console.log('📋 Extracting XML:\n');
  
  // Extract and save XML files
  zipEntries.forEach(entry => {
    const entryPath = entry.entryName;
    
    // Extract all XML files from ppt/ directory
    if ((entryPath.startsWith('ppt/') && entryPath.endsWith('.xml')) ||
        entryPath === '_rels/.rels' ||
        entryPath === '[Content_Types].xml' ||
        entryPath.endsWith('.rels')) {
      
      const fileName = entryPath.replace(/\//g, '--'); // Replace slashes for filename
      const outputPath = path.join(xmlDir, fileName);
      
      // Extract and format XML with indentation
      const xmlContent = entry.getData().toString('utf-8');
      const formattedXml = formatXml(xmlContent);
      
      fs.writeFileSync(outputPath, formattedXml);
      console.log(`  ✓ ${entryPath}`);
      xmlCount++;
    }
  });
  
  console.log(`\n✅ Analysis Complete!\n`);
  console.log(`📊 Summary:`);
  console.log(`   • Images extracted: ${imageCount}`);
  console.log(`   • XML files extracted: ${xmlCount}`);
  console.log(`\n📁 Output Locations:`);
  console.log(`   • Images: ${path.relative(skillRoot, assetsDir)}`);
  console.log(`   • XML: ${path.relative(skillRoot, xmlDir)}`);
  
  if (imageCount > 0) {
    console.log(`\n💾 Background Images:`);
    extractedImages.forEach(img => {
      console.log(`   • ${img}`);
    });
  }
  
  console.log(`\n📚 Next Steps:`);
  console.log(`   1. Review extracted images in assets/${templateName}_backgrounds/`);
  console.log(`   2. Review slide XML in pptx-analysis/${templateName}/xml/`);
  console.log(`   3. Create layouts/template/${templateName}.md with:`);
  console.log(`      - Background Image Library table`);
  console.log(`      - Colour Palette`);
  console.log(`      - Typography specs`);
  console.log(`      - Slide Layout definitions (01-05)`);
  console.log(`      - Design Rules`);
  console.log(`   4. Run: node scripts/list-templates.js to verify`);
  
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}

/**
 * Simple XML formatter to add indentation for readability
 */
function formatXml(xml) {
  let formatted = '';
  let indent = 0;
  const indentStr = '  ';
  
  // Split by XML tags
  const tags = xml.split(/(<[^>]+>)/);
  
  tags.forEach(tag => {
    if (tag.trim() === '') return;
    
    if (tag.startsWith('</')) {
      indent = Math.max(0, indent - 1);
      formatted += indentStr.repeat(indent) + tag + '\n';
    } else if (tag.startsWith('<') && tag.endsWith('/>')) {
      formatted += indentStr.repeat(indent) + tag + '\n';
    } else if (tag.startsWith('<')) {
      formatted += indentStr.repeat(indent) + tag + '\n';
      if (!tag.includes('/>')) {
        indent++;
      }
    } else {
      // Text content
      const text = tag.trim();
      if (text) {
        formatted += indentStr.repeat(indent) + text + '\n';
      }
    }
  });
  
  return formatted;
}
