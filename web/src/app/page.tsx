import Link from 'next/link';
import { Button } from "@/components/ui/button";
import { auth } from '@clerk/nextjs/server';

export default async function Home() {
  const { userId } = await auth();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 text-center">
      <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl mb-6">
        Resurch
      </h1>
      <p className="text-xl text-gray-600 mb-8 max-w-md">
        Autonomous scholarly discovery. Stop searching, start finding.
      </p>

      <div className="flex gap-4">
        {userId ? (
          <>
            <Link href="/feed">
              <Button size="lg">My Feed</Button>
            </Link>
            <Link href="/calibration">
              <Button size="lg" variant="outline">Recalibrate</Button>
            </Link>
          </>
        ) : (
          <Link href="/calibration">
            <Button size="lg">Get Started</Button>
          </Link>
        )}
      </div>
    </main>
  );
}
