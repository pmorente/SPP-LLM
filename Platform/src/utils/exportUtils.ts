import { personaGroups } from '../data/personaGroups';

const getSelectedFieldsData = (selectedFields: Record<string, boolean>, formData: Record<string, string>) => {
  const data: Record<string, string> = {};
  Object.keys(selectedFields).forEach(fieldId => {
    if (selectedFields[fieldId] && formData[fieldId]) {
      data[fieldId] = formData[fieldId];
    }
  });
  return data;
};

export const exportJSON = (selectedFields: Record<string, boolean>, formData: Record<string, string>, onDownload?: () => void) => {
  const data = getSelectedFieldsData(selectedFields, formData);
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'persona-pattern.json';
  a.click();
  URL.revokeObjectURL(url);
  if (onDownload) onDownload();
};

const escapeXML = (str: string): string => {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
};

export const exportXML = (selectedFields: Record<string, boolean>, formData: Record<string, string>, onDownload?: () => void) => {
  const data = getSelectedFieldsData(selectedFields, formData);
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<persona>\n';
  Object.entries(data).forEach(([key, value]) => {
    const escapedKey = escapeXML(key);
    const escapedValue = escapeXML(value);
    xml += `  <${escapedKey}>${escapedValue}</${escapedKey}>\n`;
  });
  xml += '</persona>';

  const blob = new Blob([xml], { type: 'application/xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'persona-pattern.xml';
  a.click();
  URL.revokeObjectURL(url);
  if (onDownload) onDownload();
};

export const exportText = (selectedFields: Record<string, boolean>, formData: Record<string, string>, onDownload?: () => void) => {
  const data = getSelectedFieldsData(selectedFields, formData);
  let text = 'PERSONA PATTERN\n';
  text += '='.repeat(50) + '\n\n';

  Object.entries(data).forEach(([key, value]) => {
    const field = Object.values(personaGroups)
      .flatMap(g => g.fields)
      .find(f => f.id === key);

    if (field) {
      text += `${field.label}:\n${value}\n\n`;
    }
  });

  const blob = new Blob([text], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'persona-pattern.txt';
  a.click();
  URL.revokeObjectURL(url);
  if (onDownload) onDownload();
};

export const generatePromptCode = (selectedFields: Record<string, boolean>, formData: Record<string, string>) => {
  const data = getSelectedFieldsData(selectedFields, formData);
  let prompt = 'You are creating content for a persona with the following characteristics:\n\n';

  Object.entries(data).forEach(([key, value]) => {
    const field = Object.values(personaGroups)
      .flatMap(g => g.fields)
      .find(f => f.id === key);

    if (field) {
      prompt += `${field.label}: ${value}\n`;
    }
  });

  prompt += '\nPlease tailor your responses to match this persona\'s context, preferences, and characteristics.';
  return prompt;
};

export const generateEnhancementScripts = () => {
  return {
    python: `#!/usr/bin/env python3
"""
Persona Pattern Enhancement Script
This script helps you enhance your persona pattern with additional analysis.
"""

import json
import sys
from pathlib import Path

def load_persona(file_path):
    """Load persona pattern from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_persona(persona_data):
    """Analyze persona data and provide insights."""
    print("\\n=== PERSONA ANALYSIS ===\\n")
    print(f"Total attributes: {len(persona_data)}")
    print(f"\\nAttributes:")
    for key, value in persona_data.items():
        print(f"  - {key}: {value}")

def enhance_persona(persona_data):
    """Add computed fields to persona."""
    enhanced = persona_data.copy()
    
    # Add enhancement logic here
    # Example: Calculate age group
    if 'age' in persona_data:
        age = int(persona_data.get('age', 0))
        if age < 25:
            enhanced['ageGroup'] = 'Young Adult'
        elif age < 40:
            enhanced['ageGroup'] = 'Adult'
        elif age < 60:
            enhanced['ageGroup'] = 'Middle-aged'
        else:
            enhanced['ageGroup'] = 'Senior'
    
    return enhanced

def main():
    if len(sys.argv) < 2:
        print("Usage: python enhance_persona.py <persona-pattern.json>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File {file_path} not found")
        sys.exit(1)
    
    persona_data = load_persona(file_path)
    analyze_persona(persona_data)
    
    enhanced = enhance_persona(persona_data)
    
    output_path = file_path.parent / f"{file_path.stem}_enhanced.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced, f, indent=2, ensure_ascii=False)
    
    print(f"\\nEnhanced persona saved to: {output_path}")

if __name__ == '__main__':
    main()`,
    
    bash: `#!/bin/bash
# Persona Pattern Enhancement Script
# This script helps you enhance your persona pattern with additional analysis.

PERSONA_FILE="$1"

if [ -z "$PERSONA_FILE" ]; then
    echo "Usage: ./enhance_persona.sh <persona-pattern.json>"
    exit 1
fi

if [ ! -f "$PERSONA_FILE" ]; then
    echo "Error: File $PERSONA_FILE not found"
    exit 1
fi

echo ""
echo "=== PERSONA ANALYSIS ==="
echo ""

# Count attributes
ATTRIBUTE_COUNT=$(jq 'length' "$PERSONA_FILE" 2>/dev/null || echo "0")
echo "Total attributes: $ATTRIBUTE_COUNT"

echo ""
echo "Attributes:"
jq -r 'to_entries[] | "  - \(.key): \(.value)"' "$PERSONA_FILE" 2>/dev/null || cat "$PERSONA_FILE"

# Create enhanced version
ENHANCED_FILE="\${PERSONA_FILE%.*}_enhanced.json"
jq '. + {enhanced: true, enhancedDate: now | todateiso8601}' "$PERSONA_FILE" > "$ENHANCED_FILE" 2>/dev/null || {
    echo "Note: jq not installed. Install it for JSON processing: sudo apt-get install jq"
}

if [ -f "$ENHANCED_FILE" ]; then
    echo ""
    echo "Enhanced persona saved to: $ENHANCED_FILE"
fi`,
    
    nodejs: `#!/usr/bin/env node
/**
 * Persona Pattern Enhancement Script
 * This script helps you enhance your persona pattern with additional analysis.
 */

const fs = require('fs');
const path = require('path');

function loadPersona(filePath) {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Error loading persona:', error.message);
        process.exit(1);
    }
}

function analyzePersona(personaData) {
    console.log('\\n=== PERSONA ANALYSIS ===\\n');
    console.log(\`Total attributes: \${Object.keys(personaData).length}\`);
    console.log('\\nAttributes:');
    Object.entries(personaData).forEach(([key, value]) => {
        console.log(\`  - \${key}: \${value}\`);
    });
}

function enhancePersona(personaData) {
    const enhanced = { ...personaData };
    
    // Add enhancement logic here
    // Example: Calculate age group
    if (personaData.age) {
        const age = parseInt(personaData.age);
        if (age < 25) {
            enhanced.ageGroup = 'Young Adult';
        } else if (age < 40) {
            enhanced.ageGroup = 'Adult';
        } else if (age < 60) {
            enhanced.ageGroup = 'Middle-aged';
        } else {
            enhanced.ageGroup = 'Senior';
        }
    }
    
    enhanced.enhanced = true;
    enhanced.enhancedDate = new Date().toISOString();
    
    return enhanced;
}

function main() {
    const filePath = process.argv[2];
    
    if (!filePath) {
        console.error('Usage: node enhance_persona.js <persona-pattern.json>');
        process.exit(1);
    }
    
    if (!fs.existsSync(filePath)) {
        console.error(\`Error: File \${filePath} not found\`);
        process.exit(1);
    }
    
    const personaData = loadPersona(filePath);
    analyzePersona(personaData);
    
    const enhanced = enhancePersona(personaData);
    
    const outputPath = path.join(
        path.dirname(filePath),
        \`\${path.basename(filePath, path.extname(filePath))}_enhanced.json\`
    );
    
    fs.writeFileSync(outputPath, JSON.stringify(enhanced, null, 2), 'utf8');
    console.log(\`\\nEnhanced persona saved to: \${outputPath}\`);
}

main();`
  };
};
