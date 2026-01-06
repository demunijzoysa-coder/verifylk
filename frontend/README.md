# Frontend — VerifyLK

Vite + React + TypeScript client for the verification platform. The current UI showcases candidate, verifier, and employer flows plus a shareable report panel.

## Quickstart
```bash
cd frontend
npm install
npm run dev
```

## Structure
- `src/App.tsx` — role-based dashboard mock and report view.
- `src/App.css` — themed styles (trust-first, bright accents).
- `src/index.css` — global tokens and font.

## Next steps
- Wire API client to FastAPI backend.
- Add forms for claim creation and verification decisions.
- Add auth state and role-based routing.
- Render live score breakdown from API.
