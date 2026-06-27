import Link from "next/link";

import { getProducts } from "@/services/product";
import { Product } from "@/types/product";

const CATEGORY_ICON: Record<string, string> = {
    여성의류: "👗",
    남성의류: "👔",
    패션슈즈: "👟",
    잡화: "👜",
};

const CATEGORIES = [
    { name: "전체", icon: "🛍️" },
    { name: "여성의류", icon: "👗" },
    { name: "남성의류", icon: "👔" },
    { name: "패션슈즈", icon: "👟" },
    { name: "잡화", icon: "👜" },
];

type ProductsPageProps = {
    searchParams: Promise<{
        category?: string;
    }>;
};

export default async function ProductsPage({
    searchParams,
}: ProductsPageProps) {
    const params = await searchParams;
    const selectedCategory = params.category;

    const products: Product[] = await getProducts();

    const filteredProducts = selectedCategory
        ? products.filter(
            (product) => product.category === selectedCategory
        )
        : products;

    return (
        <main className="mx-auto max-w-7xl px-6 py-10">
            <section className="mb-10 overflow-hidden rounded-3xl bg-gradient-to-r from-blue-600 to-indigo-700 px-10 py-12 text-white">
                <p className="text-sm font-semibold uppercase tracking-wide text-blue-100">
                    AI Review Commerce
                </p>

                <h1 className="mt-3 text-4xl font-extrabold leading-tight">
                    리뷰 데이터로 검증된
                    <br />
                    패션 상품을 만나보세요
                </h1>

                <p className="mt-4 max-w-2xl text-blue-100">
                    VOCLens는 고객 리뷰를 분석하여 상품의 만족 포인트와
                    불만 요소를 함께 보여주는 AI 기반 쇼핑몰 데모입니다.
                </p>

                <div className="mt-8 flex flex-wrap gap-3">
                    <span className="rounded-full bg-white/20 px-4 py-2 text-sm">
                        감성 분석
                    </span>
                    <span className="rounded-full bg-white/20 px-4 py-2 text-sm">
                        VOC 분석
                    </span>
                    <span className="rounded-full bg-white/20 px-4 py-2 text-sm">
                        AI 리뷰 요약
                    </span>
                </div>
            </section>

            <section className="mb-10">
                <h2 className="mb-5 text-2xl font-bold text-gray-900">
                    카테고리
                </h2>

                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
                    {CATEGORIES.map((category) => {
                        const isActive =
                            category.name === "전체"
                                ? !selectedCategory
                                : selectedCategory === category.name;

                        return (
                            <Link
                                key={category.name}
                                href={
                                    category.name === "전체"
                                        ? "/products"
                                        : `/products?category=${category.name}`
                                }
                                className={`rounded-2xl border bg-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg ${isActive
                                    ? "border-blue-500 ring-2 ring-blue-100"
                                    : "border-gray-200 hover:border-blue-400"
                                    }`}
                            >
                                <div className="text-5xl">
                                    {category.icon}
                                </div>

                                <p className="mt-3 text-lg font-bold text-gray-900">
                                    {category.name}
                                </p>

                                <p className="mt-1 text-sm text-gray-500">
                                    {category.name === "전체"
                                        ? "모든 상품 보기"
                                        : "리뷰 기반 상품 보기"}
                                </p>
                            </Link>
                        );
                    })}
                </div>
            </section>

            <section>
                <div className="mb-5 flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-gray-900">
                        {selectedCategory ?? "전체"} 인기 상품
                    </h2>

                    <p className="text-sm text-gray-500">
                        총 {filteredProducts.length}개 상품
                    </p>
                </div>

                <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                    {filteredProducts.map((product) => (
                        <Link
                            key={product.id}
                            href={`/products/${product.id}`}
                            className="group overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-blue-400 hover:shadow-xl"
                        >
                            <div className="flex h-64 items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200 text-7xl">
                                {CATEGORY_ICON[product.category] ?? "🛍️"}
                            </div>

                            <div className="space-y-3 p-5">
                                <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700">
                                    {product.category}
                                </span>

                                <h2 className="line-clamp-2 text-lg font-bold text-gray-900 transition-colors group-hover:text-blue-600">
                                    {product.name}
                                </h2>

                                <p className="text-sm text-gray-600">
                                    {product.brand}
                                </p>

                                <div className="flex items-center justify-between">
                                    <p className="text-2xl font-extrabold text-gray-900">
                                        {product.price.toLocaleString()}원
                                    </p>

                                    <div className="text-right">
                                        <div className="text-yellow-500">
                                            ★★★★★
                                        </div>
                                        <p className="text-xs text-gray-400">
                                            AI 리뷰 분석
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            </section>
        </main>
    );
}