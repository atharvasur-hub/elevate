# ELEVATE GeoAI Frontend Dashboard

Modern AI-driven geospatial dashboard for querying Indian government welfare schemes, budgets, and fund utilization. Built with **Next.js (App Router)**, **Tailwind CSS**, and **React-Leaflet**, integrated with the FastAPI NL-to-SQL endpoint (`http://localhost:8000/api/v1/query/ask`).

---

## 🌟 Features

- 🔍 **Natural Language Search Bar**: Ask complex analytical questions in plain English with instant suggestion chips.
- 🗺️ **Center Geographic Map**: Powered by `react-leaflet` with dark-themed CartoDB tiles, custom pulsing pins, and detailed popup cards.
- 🧠 **AI Intelligence & Recommendations**: Dedicated card displaying Gemini 2.5 Flash analysis, strategic focus points, and policy takeaways.
- 💻 **SQL Query Inspector & Stats**: Inspect the generated PostgreSQL query, latency, row count, and raw execution payloads.
- 📊 **Dynamic Data Table & JSON Explorer**: Sort, search, export to CSV, or view/copy raw JSON returned by the backend.
- ⚡ **Backend Status Indicator**: Live status checking against the FastAPI backend health endpoint.

---

## 🚀 Getting Started

### 1. Prerequisites
- Node.js 18+ / 20+
- FastAPI backend running at `http://localhost:8000`

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration (Optional)
By default, the frontend connects to `http://localhost:8000`. You can configure a `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🏗️ Architecture

```
frontend/
├── src/
│   ├── app/
│   │   ├── globals.css         # Dark theme & Leaflet custom marker animations
│   │   ├── layout.tsx          # Root layout & SEO metadata
│   │   └── page.tsx            # Main Dashboard Page
│   ├── components/
│   │   ├── Navbar.tsx          # Navigation & FastAPI Health Status
│   │   ├── SearchBar.tsx       # AI Question Input & Suggestion Chips
│   │   ├── StatsOverview.tsx   # KPI Metric Cards
│   │   ├── MapComponent.tsx    # React-Leaflet Map implementation
│   │   ├── MapWrapper.tsx      # SSR-Safe Dynamic Map loader
│   │   ├── AiRecommendations.tsx # AI Insights & Policy Takeaways
│   │   ├── DataResultsTable.tsx# Interactive Table & JSON Explorer
│   │   └── SqlViewer.tsx       # SQL Code Viewer with Copy Action
│   ├── lib/
│   │   ├── api.ts              # FastAPI fetch client (/api/v1/query/ask)
│   │   └── geoData.ts          # Coordinate dictionary & Geo mapper
│   └── types/
│       └── index.ts            # TypeScript interfaces
```
