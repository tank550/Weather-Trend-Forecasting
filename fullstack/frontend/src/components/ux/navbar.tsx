import Link from "next/link";
import { Button } from "../ui/button";

export default function Navbar() {
    return (
        <nav className="flex items-center justify-between bg-blue-600 px-6 py-4 text-white">
            <h1 className="text-xl font-bold">Weather-App</h1>

            <div className="flex gap-10">
                <Link href="/">Dashboard</Link>
                <Link href="/list">Saved</Link>
                <Link href="/contact">History</Link>
                <Link href="/about">About</Link>
            </div>

            <div className="flex gap-2">
                <Button variant="outline">Button</Button>
            </div>
        </nav>
    );
}