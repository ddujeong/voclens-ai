import Link from "next/link";

import { getProducts } from "@/services/product";
import { Product } from "@/types/product";


export default async function ProductsPage() {
    const products: Product[] = await getProducts();

    return (
        <main className="p-8">
            <h1 className="text-2xl font-bold">상품 목록</h1>

            <div className="mt-6 grid gap-4">
                {products.map((product) => (
                    <Link
                        key={product.id}
                        href={`/products/${product.id}`}
                        className="rounded border p-4"
                    >
                        <h2 className="text-lg font-semibold">{product.name}</h2>
                        <p className="text-sm text-gray-600">{product.brand}</p>
                        <p className="mt-2">{product.price.toLocaleString()}원</p>
                    </Link>
                ))}
            </div>
        </main>
    );
}