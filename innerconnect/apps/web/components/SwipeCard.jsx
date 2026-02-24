export function SwipeCard() {
  return (
    <article className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-lg">
      <h2 className="text-xl font-semibold">Swipe Interface</h2>
      <div className="mt-4 rounded-xl bg-slate-800 p-5">
        <p className="font-medium">Avery, 28</p>
        <p className="text-sm text-slate-300">Product Design · Loves running, coffee, and chess.</p>
        <div className="mt-4 flex gap-3">
          <button className="flex-1 rounded-lg border border-rose-500 p-2">Pass</button>
          <button className="flex-1 rounded-lg bg-emerald-600 p-2">Like</button>
        </div>
      </div>
    </article>
  );
}
