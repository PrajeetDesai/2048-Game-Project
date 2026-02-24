const stats = [
  { label: 'Total Users', value: 124 },
  { label: 'Active Users', value: 89 },
  { label: 'Total Matches', value: 210 },
  { label: 'Open Reports', value: 6 }
];

export function AdminStats() {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((s) => (
        <div key={s.label} className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <p className="text-xs text-slate-400">{s.label}</p>
          <p className="text-2xl font-bold">{s.value}</p>
        </div>
      ))}
    </div>
  );
}
