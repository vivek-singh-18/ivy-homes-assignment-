# Ivy Homes Assignment - Full Stack & Analytics

## Approach
- **Phase 1 & 2:** Identified several discrepancies between the provided `API_REFERENCE.md` and the actual API. I successfully navigated the pagination lies (`offset` vs `page`, `limit=50` max instead of 200) and the authentication lies (`X-API-Key` required in header, `refresh_token` flow required). 
- **Caching & Rate Limits:** To respect the 1200 RPM limit, I wrote a script to page through and download all raw data (`v1_listings.json`, `v1_projects.json`, `v1_rentals.json`). All data analysis was performed against this cached local dataset.
- **Phase 3 & 4:** Answered the 10 analytical questions using pandas to accurately process the data. Corrupt listings were identified by physically impossible features (e.g. negative area, villa with 300 floors). Fake listings were identified by scam phrases in descriptions. Discrepancies were documented into `submission.json`.
- **Phase 5 & 6:** Built a React frontend using Vite, React Router, TailwindCSS, and Axios. The frontend implements the authentication refresh flow seamlessly via axios interceptors and manual client-side filtering since API filters were found to be non-functional.

## Findings summary
- Pagination completely differs from documentation (uses `offset`).
- `project_id` filter on `/v1/listings` is broken (returns all listings).
- `property_type`, `min_price`, `max_price` filters on `/v1/rentals` are ignored.
- Project `price_max` is returned in Lakhs, not Rupees.
- `MAG-` listings return their `carpet_area` in Square Meters, not Square Feet.
- `posted_at` timestamps are naive (no Z suffix).
- `is_live=False` records are returned despite documentation.

## Running the Frontend
1. Navigate to the `frontend` directory.
2. `npm install`
3. Create a `.env` file containing `VITE_IVY_API_KEY=IVY26-AEC873EFB13C` and `VITE_DEMO_PASSWORD=31d4e26d65`.
4. `npm run dev` to start the local development server.

## Submission Details
- See `submission.json` for the exact calculated answers and findings array.
