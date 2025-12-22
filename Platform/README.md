# Persona Pattern Builder

A comprehensive React application for building detailed user personas with customizable attributes. This tool allows you to select relevant persona variables and fill in data to create structured persona profiles that can be exported as JSON or XML.

## Features

- **13 Persona Groups**: Covering demographics, lifestyle, employment, health, digital identity, and more
- **Customizable Selection**: Choose which variables to include in your persona
- **Interactive Forms**: Fill in selected attributes with various input types
- **Export Options**: Download personas as JSON or XML files
- **Prompt Generation**: Generate AI prompt code for persona-based content creation
- **Modern UI**: Beautiful, responsive interface built with Tailwind CSS

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 18 or higher) - **Note:** Vite 5.4.x supports Node.js 18+, while Vite 7+ requires Node.js 20.19+ or 22.12+
- **npm** or **yarn** package manager

### For WSL (Windows Subsystem for Linux)

If you're using WSL, you'll need to install Node.js in your WSL environment:

**For Node.js 18 (current setup):**
```bash
# Update package list
sudo apt update

# Install Node.js 18 and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

**To upgrade to Node.js 20 (optional, for Vite 7+):**
```bash
# Update package list
sudo apt update

# Install Node.js 20 and npm
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /path/to/I2R
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

   This will install all required packages including:
   - React 18
   - TypeScript
   - Vite (build tool)
   - Tailwind CSS
   - Lucide React (icons)

## Development

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or another port if 5173 is in use).

## Building for Production

To create a production build:

```bash
npm run build
```

The optimized files will be in the `dist` directory.

To preview the production build:

```bash
npm run preview
```

## Project Structure

```
I2R/
├── src/
│   ├── components/          # React components
│   │   ├── Header.tsx
│   │   ├── PromptCodeModal.tsx
│   │   ├── Tabs.tsx
│   │   ├── FieldSelector.tsx
│   │   ├── FieldGroup.tsx
│   │   ├── FormField.tsx
│   │   └── PersonaForm.tsx
│   ├── data/
│   │   └── personaGroups.ts  # Persona data definitions
│   ├── utils/
│   │   └── exportUtils.ts    # Export and prompt generation utilities
│   ├── App.tsx               # Main application component
│   ├── main.tsx              # Application entry point
│   └── index.css             # Tailwind CSS imports
├── index.html                # HTML template
├── package.json              # Dependencies and scripts
├── tsconfig.json             # TypeScript configuration
├── vite.config.ts            # Vite configuration
├── tailwind.config.js        # Tailwind CSS configuration
└── postcss.config.js         # PostCSS configuration
```

## Usage

1. **Select Variables**: In the first tab, choose which persona attributes you want to include. All variables are selected by default.

2. **Fill Persona Data**: Switch to the second tab and fill in the selected attributes with relevant information.

3. **Export**: Use the export buttons to download your persona as JSON or XML.

4. **Generate Prompts**: Click "Show Prompt Code" to generate AI prompt code based on your persona data.

## Technologies Used

- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icon library

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Browser Support

This application works in all modern browsers that support ES6+ features.

## License

This project is for educational/research purposes.

