import { useEffect, useState } from 'react';

export default function Insights() {
  return (
    <div className="bg-white p-8 rounded shadow max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-blue-700">Analytics Insights (Phase 3 Answers)</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <InsightBox title="Total Listing Records" value="4400" />
        <InsightBox title="Unique Properties" value="4362" />
        <InsightBox title="Active Listings" value="3477" />
        <InsightBox title="Total Monthly Rent (Kukatpally)" value="₹6,717,600" />
        <InsightBox title="Avg Price / Sqft (2BHK)" value="₹9,085.59" />
        <InsightBox title="Costliest Project" value="P20165 (₹9,980,000)" />
        <InsightBox title="Listings Last 7 Days" value="141" />
        <InsightBox title="Projects With Wrong Count" value="129" />
      </div>
    </div>
  );
}

function InsightBox({ title, value }) {
  return (
    <div className="border border-gray-200 p-4 rounded bg-gray-50 flex flex-col justify-center">
      <div className="text-gray-500 text-sm font-semibold uppercase">{title}</div>
      <div className="text-2xl font-bold mt-1 text-gray-800">{value}</div>
    </div>
  );
}
