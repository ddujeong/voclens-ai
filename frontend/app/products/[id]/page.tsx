import { getProduct } from "@/services/product";
import { getReviews } from "@/services/review";
import { Product } from "@/types/product";
import { Review } from "@/types/review";
import ReviewForm from "@/components/product/ReviewForm";

interface ProductDetailPageProps {
    params: Promise<{
        id: string;
    }>;
}

export default async function ProductDetailPage({
    params,
}: ProductDetailPageProps) {
    const { id } = await params;

    const product: Product = await getProduct(id);
    const reviews: Review[] = await getReviews(id);

    return (
        <main className="p-8">
            <section className="rounded border p-6">
                <h1 className="text-2xl font-bold">{product.name}</h1>
                <p className="mt-2 text-gray-600">{product.brand}</p>
                <p className="mt-2">{product.category}</p>
                <p className="mt-4 text-xl font-semibold">
                    {product.price.toLocaleString()}원
                </p>
            </section>

            <section className="mt-8">
                <ReviewForm productId={id} />
                <h2 className="text-xl font-bold">리뷰</h2>

                <div className="mt-4 grid gap-4">
                    {reviews.map((review) => (
                        <div key={review.id} className="rounded border p-4">
                            <p>별점: {review.rating}</p>
                            <p className="mt-2">{review.content}</p>
                            <p className="mt-2 text-sm text-gray-500">
                                감성: {review.sentiment ?? "미분석"}
                            </p>
                        </div>
                    ))}
                </div>
            </section>
        </main>
    );
}