# 🦌 DeerFlow Web UI (Vite + React + TypeScript)

> Originated from Open Source, give back to Open Source.

This is the Vite + React + TypeScript web UI for [`DeerFlow`](https://github.com/bytedance/deer-flow).

## Quick Start

### Prerequisites

- [`DeerFlow`](https://github.com/bytedance/deer-flow)
- Node.js (v22.14.0+)
- pnpm (v10.6.2+) as package manager

### Configuration

Create a `.env` file in the project root and configure the following environment variables:

- `VITE_API_URL`: The URL of the deer-flow API.

It's always a good idea to start with the given example file, and edit the `.env` file with your own values:

```bash
cp .env.example .env
```

## How to Install

DeerFlow Web UI uses `pnpm` as its package manager.
To install the dependencies, run:

```bash
cd web-vite
pnpm install
```

## How to Run in Development Mode

> [!NOTE]
> Ensure the Python API service is running before starting the web UI.

Start the web UI development server:

```bash
cd web-vite
pnpm dev
```

By default, the web UI will be available at `http://localhost:5173`.

You can set the `VITE_API_URL` environment variable if you're using a different host or location.

```ini
# .env
VITE_API_URL=http://localhost:8000/api
```

## Build for Production

To build the project for production:

```bash
pnpm build
```

The output will be in the `dist/` directory.

## Directory Structure

```
web-vite/
├── public/
├── src/
│   ├── app/
│   ├── assets/
│   ├── components/
│   ├── core/
│   ├── hooks/
│   ├── lib/
│   ├── pages/
│   ├── styles/
│   └── typings/
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── pnpm-lock.yaml
├── postcss.config.js
├── prettier.config.js
├── README.md
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
└── ...
```

## License

This project is open source and available under the [MIT License](../LICENSE).

## Acknowledgments

We extend our heartfelt gratitude to the open source community for their invaluable contributions.
DeerFlow is built upon the foundation of these outstanding projects:

- [Vite](https://vitejs.dev/) for their exceptional build tool
- [React](https://react.dev/) for their powerful UI library
- [shadcn/ui](https://ui.shadcn.com/) for their minimalistic components
- [Zustand](https://zustand.docs.pmnd.rs/) for their stunning state management
- [Framer Motion](https://www.framer.com/motion/) for their amazing animation library
- [React Markdown](https://www.npmjs.com/package/react-markdown) for their exceptional markdown rendering and customizability

These outstanding projects form the backbone of DeerFlow and exemplify the transformative power of open source collaboration.
