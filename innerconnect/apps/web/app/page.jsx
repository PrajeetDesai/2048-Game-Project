import { AuthCard } from '../components/AuthCard';
import { SwipeCard } from '../components/SwipeCard';
import { AdminStats } from '../components/AdminStats';
import { ThemeToggle } from '../components/ThemeToggle';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8">
      <div className="max-w-6xl mx-auto mb-4 flex justify-end"><ThemeToggle /></div>
      <section className="max-w-6xl mx-auto grid gap-6 md:grid-cols-2">
        <AuthCard />
        <SwipeCard />
      </section>
      <section className="max-w-6xl mx-auto mt-6">
        <AdminStats />
      </section>
    </main>
  );
}
