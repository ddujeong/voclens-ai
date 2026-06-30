import {
    getProduct,
    getProductSummary,
} from "@/services/product";
import { getReviews } from "@/services/review";
import { Product } from "@/types/product";
import { Review } from "@/types/review";
import ReviewForm from "@/components/product/ReviewForm";

interface ProductDetailPageProps {
    params: Promise<{
        id: string;
    }>;
}

type ProductSummary = {
    summary: string;
    positive: string[];
    negative: string[];
};

const CATEGORY_ICON: Record<string, string> = {
    여성의류: "👗",
    남성의류: "👔",
    패션슈즈: "👟",
    잡화: "👜",
};

const SENTIMENT_LABEL: Record<string, string> = {
    positive: "만족",
    negative: "불만",
    neutral: "보통",
};

const SENTIMENT_ICON: Record<string, string> = {
    positive: "😊",
    negative: "😡",
    neutral: "😐",
};

const getRatingCounts = (reviews: Review[]) => {
    return [5, 4, 3, 2, 1].map((rating) => ({
        rating,
        count: reviews.filter((review) => review.rating === rating).length,
    }));
};

export default async function ProductDetailPage({
    params,
}: ProductDetailPageProps) {
    const { id } = await params;

    const product: Product = await getProduct(id);
    const reviews: Review[] = await getReviews(id);
    const summary: ProductSummary = await getProductSummary(id);

    const ratingCounts = getRatingCounts(reviews);
    const maxRatingCount = Math.max(
        ...ratingCounts.map((item) => item.count),
        1
    );

    const averageRating =
        reviews.length === 0
            ? 0
            : reviews.reduce((sum, review) => sum + review.rating, 0) /
            reviews.length;
    const filledStars = Math.round(averageRating);
    return (
        <main className="mx-auto max-w-7xl px-6 py-10">
            <section className="grid gap-10 rounded-3xl border border-gray-200 bg-white p-8 shadow-sm lg:grid-cols-2">
                <div className="flex min-h-[420px] items-center justify-center rounded-3xl bg-gradient-to-br from-gray-100 to-gray-200 text-9xl">
                    {CATEGORY_ICON[product.category] ?? "🛍️"}
                </div>

                <div className="flex flex-col justify-center">
                    <span className="w-fit rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700">
                        {product.category}
                    </span>

                    <h1 className="mt-4 text-4xl font-extrabold leading-tight text-gray-900">
                        {product.name}
                    </h1>

                    <p className="mt-3 text-gray-600">{product.brand}</p>

                    <div className="mt-5 flex items-center gap-3">
                        <span className="text-yellow-500">
                            {"★".repeat(filledStars)}
                            {"☆".repeat(5 - filledStars)}
                        </span>
                        <span className="text-sm text-gray-500">
                            {averageRating.toFixed(1)} · 리뷰 {reviews.length}건
                        </span>
                    </div>

                    <p className="mt-8 text-4xl font-extrabold text-gray-900">
                        {product.price.toLocaleString()}원
                    </p>

                    <div className="mt-8 grid gap-3 sm:grid-cols-3">
                        <div className="rounded-2xl bg-gray-50 p-4">
                            <p className="text-xs text-gray-500">AI 분석</p>
                            <p className="mt-1 font-bold text-gray-900">
                                VOC 적용
                            </p>
                        </div>

                        <div className="rounded-2xl bg-gray-50 p-4">
                            <p className="text-xs text-gray-500">리뷰 기반</p>
                            <p className="mt-1 font-bold text-gray-900">
                                감성 분류
                            </p>
                        </div>

                        <div className="rounded-2xl bg-gray-50 p-4">
                            <p className="text-xs text-gray-500">운영자</p>
                            <p className="mt-1 font-bold text-gray-900">
                                분석 가능
                            </p>
                        </div>
                    </div>

                    <button className="mt-8 rounded-2xl bg-blue-600 px-6 py-4 font-bold text-white transition hover:bg-blue-700">
                        구매하기
                    </button>
                </div>
            </section>

            <section className="mt-10 grid gap-8 lg:grid-cols-[0.9fr_1.5fr]">
                <div className="space-y-8">
                    <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                        <h2 className="text-2xl font-bold text-gray-900">
                            리뷰 통계
                        </h2>

                        <div className="mt-5 flex items-end gap-3">
                            <span className="text-5xl font-extrabold text-gray-900">
                                {averageRating.toFixed(1)}
                            </span>
                            <span className="pb-2 text-yellow-500">
                                {"★".repeat(filledStars)}
                                {"☆".repeat(5 - filledStars)}
                            </span>
                        </div>

                        <p className="mt-1 text-sm text-gray-500">
                            총 {reviews.length}개 리뷰 기준
                        </p>

                        <div className="mt-6 space-y-3">
                            {ratingCounts.map((item) => (
                                <div
                                    key={item.rating}
                                    className="flex items-center gap-3 text-sm"
                                >
                                    <span className="w-12 text-gray-600">
                                        {item.rating}점
                                    </span>

                                    <div className="h-2.5 flex-1 rounded-full bg-gray-100">
                                        <div
                                            className="h-2.5 rounded-full bg-yellow-400"
                                            style={{
                                                width: `${(item.count /
                                                    maxRatingCount) *
                                                    100
                                                    }%`,
                                            }}
                                        />
                                    </div>

                                    <span className="w-10 text-right text-gray-500">
                                        {item.count}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                        <h2 className="text-2xl font-bold text-gray-900">
                            AI 리뷰 요약
                        </h2>

                        <p className="mt-4 leading-7 text-gray-700">
                            {summary.summary}
                        </p>

                        <div className="mt-6 space-y-5">
                            <div>
                                <h3 className="font-semibold text-gray-900">
                                    👍 장점
                                </h3>

                                <ul className="mt-2 space-y-2 text-sm text-gray-700">
                                    {summary.positive.length === 0 ? (
                                        <li>확인된 장점이 없습니다.</li>
                                    ) : (
                                        summary.positive.map((item) => (
                                            <li key={item}>• {item}</li>
                                        ))
                                    )}
                                </ul>
                            </div>

                            <div>
                                <h3 className="font-semibold text-gray-900">
                                    👎 아쉬운 점
                                </h3>

                                <ul className="mt-2 space-y-2 text-sm text-gray-700">
                                    {summary.negative.length === 0 ? (
                                        <li>확인된 아쉬운 점이 없습니다.</li>
                                    ) : (
                                        summary.negative.map((item) => (
                                            <li key={item}>• {item}</li>
                                        ))
                                    )}
                                </ul>
                            </div>
                        </div>
                    </div>

                    <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                        <h2 className="text-2xl font-bold text-gray-900">
                            리뷰 작성
                        </h2>

                        <p className="mt-2 text-sm text-gray-500">
                            작성된 리뷰는 AI VOC 분석에 활용됩니다.
                        </p>

                        <div className="mt-6">
                            <ReviewForm productId={id} />
                        </div>
                    </div>
                </div>

                <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                    <div className="flex items-center justify-between">
                        <h2 className="text-2xl font-bold text-gray-900">
                            고객 리뷰
                        </h2>

                        <span className="text-sm text-gray-500">
                            총 {reviews.length}건
                        </span>
                    </div>

                    <div className="mt-6 grid gap-4">
                        {reviews.length === 0 ? (
                            <div className="rounded-2xl bg-gray-50 p-8 text-center text-gray-500">
                                아직 작성된 리뷰가 없습니다.
                            </div>
                        ) : (
                            reviews.map((review) => {
                                const sentiment = review.sentiment ?? "neutral";

                                return (
                                    <div
                                        key={review.id}
                                        className="rounded-2xl border border-gray-100 bg-gray-50 p-5"
                                    >
                                        <div className="flex items-center justify-between">
                                            <span className="text-yellow-500">
                                                {"★".repeat(review.rating)}
                                                {"☆".repeat(5 - review.rating)}
                                            </span>

                                            <span className="rounded-full bg-white px-3 py-1 text-xs text-gray-600">
                                                {SENTIMENT_ICON[sentiment] ?? "😐"}{" "}
                                                {SENTIMENT_LABEL[sentiment] ??
                                                    "미분석"}
                                            </span>
                                        </div>

                                        <p className="mt-3 leading-7 text-gray-800">
                                            {review.content}
                                        </p>

                                        <p className="mt-3 text-xs text-gray-400">
                                            {review.created_at?.slice(0, 10)}
                                        </p>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>
            </section>
        </main>
    );
}