export default function AboutPage() {
    return (
        <main className="min-h-screen bg-gray-50 px-6 py-12">
            <div className="mx-auto max-w-4xl rounded-xl bg-white p-8 shadow-md">
                <h1 className="mb-6 text-4xl font-bold text-gray-900">
                    About
                </h1>

                <section className="mb-8">
                    <h2 className="mb-2 text-2xl font-semibold text-blue-600">
                        Developer
                    </h2>
                    <p className="text-lg text-gray-700">
                        <strong>Developed by:</strong> Schalom Gandonou
                    </p>
                </section>

                <section>
                    <h2 className="mb-4 text-2xl font-semibold text-blue-600">
                        About PM Accelerator
                    </h2>

                    <p className="leading-8 text-gray-700">
                        PM Accelerator helps aspiring and experienced product managers
                        develop the skills, experience, and industry connections needed to
                        advance their careers. Through mentorship, training, and real-world
                        product experiences, the organization supports professionals in
                        building successful careers in product management.
                    </p>
                </section>
            </div>
        </main>
    );
}