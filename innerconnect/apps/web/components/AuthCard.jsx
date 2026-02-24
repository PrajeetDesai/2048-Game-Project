export function AuthCard() {
  return (
    <article className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-lg">
      <h1 className="text-2xl font-semibold">InnerConnect</h1>
      <p className="mt-2 text-sm text-slate-300">Secure employee-only dating inside your campus.</p>
      <form className="mt-6 space-y-3">
        <input className="w-full rounded-lg bg-slate-800 p-3" placeholder="name@company.com" />
        <input type="password" className="w-full rounded-lg bg-slate-800 p-3" placeholder="Password" />
        <label className="flex items-center gap-2 text-xs text-slate-300">
          <input type="checkbox" />
          I consent to terms, privacy policy, and campus-only discoverability.
        </label>
        <button className="w-full rounded-lg bg-emerald-600 p-3 font-medium">Request OTP</button>
      </form>
    </article>
  );
}
