# AI Agent Coordination & Decision Engine — Frontend (M8)

This is the React + Vite frontend starter for the M8 responsibility: Frontend Dashboard, Monitoring UI & AWS Deployment.

## Features included
- Dashboard overview with workflow summary cards
- New business request form
- Agent monitoring page
- Workflow history with search
- Decision reports page
- Responsive sidebar navigation
- Demo data so frontend development can continue before the backend is ready
- API service functions prepared for backend integration

## Requirements
- Node.js 18 or later
- npm

## Run locally
```bash
npm install
npm run dev
```
Open the local URL printed by Vite (usually http://localhost:5173).

## Build check
```bash
npm run build
```
The production files will be generated in `dist/`.

## Connect to the backend
1. Copy `.env.example` to `.env`.
2. Set `VITE_API_BASE_URL` to the base URL provided by M7, for example `http://localhost:8000`.
3. Confirm the final API endpoint paths and request/response schemas with M7 before enabling live integration.

The API service currently assumes these example endpoints:
- `POST /api/workflows` with `{ "user_request": "..." }`
- `GET /api/workflows`
- `GET /api/agents/status`

These are integration placeholders, not confirmed endpoints. Update `src/services/api.js` to match the actual backend contract agreed by M1 and M7.

## Important demo-data note
The dashboard counts, workflow records, agent statuses, and recommendation reports are illustrative sample data. They are not actual results from the AI agents. Replace them with backend responses during integration.

## GitHub upload
Upload the contents of this folder into your shared repository's existing `frontend/` directory. Do not create an extra nested `frontend/frontend/` directory. Work on your team's agreed feature branch and open a Pull Request rather than pushing directly to `main`.

## M8 scope
Frontend pages and components are included. AWS deployment is not configured because the team's AWS account, permissions, selected hosting service, and backend deployment details are not yet known. Coordinate these with M7 and M1 before deployment.
