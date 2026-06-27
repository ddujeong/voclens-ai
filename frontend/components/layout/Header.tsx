import Link from "next/link";

export default function Header() {
    return (
        <header className="border-b bg-white">
            <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
                <Link
                    href="/products"
                    className="text-2xl font-bold text-blue-600"
                >
                    VOCLens
                </Link>

                <nav className="flex items-center gap-8 text-sm font-medium text-gray-700">
                    <Link
                        href="/products"
                        className="transition hover:text-blue-600"
                    >
                        Home
                    </Link>

                    <Link
                        href="/products?category=여성의류"
                        className="transition hover:text-blue-600"
                    >
                        여성의류
                    </Link>

                    <Link
                        href="/products?category=남성의류"
                        className="transition hover:text-blue-600"
                    >
                        남성의류
                    </Link>

                    <Link
                        href="/products?category=패션슈즈"
                        className="transition hover:text-blue-600"
                    >
                        패션슈즈
                    </Link>

                    <Link
                        href="/products?category=잡화"
                        className="transition hover:text-blue-600"
                    >
                        잡화
                    </Link>
                </nav>

                <Link
                    href="/admin"
                    className="rounded bg-blue-600 px-4 py-2 text-sm text-white"
                >
                    관리자
                </Link>
            </div>
        </header>
    );
}