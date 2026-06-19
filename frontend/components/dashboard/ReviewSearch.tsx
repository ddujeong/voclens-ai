"use client";

import { useState } from "react";
import { searchReviews } from "@/services/dashboard";

interface Review {
    id: number;
    product_id: number;
    product_name: string;
    rating: number;
    content: string;
    sentiment: string | null;
    created_at: string;
}

export default function ReviewSearch() {
    const [keyword, setKeyword] = useState("");
    const [reviews, setReviews] = useState<Review[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        if (!keyword.trim()) return;

        try {
            setLoading(true);

            const result = await searchReviews(keyword);

            setReviews(result);
        } catch (error) {
            console.error(error);
            alert("검색 실패");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="mt-6">
            <div>
                <input
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    placeholder="배터리"
                    className="border p-2"
                />

                <button
                    onClick={handleSearch}
                    className="ml-2 border px-4 py-2"
                >
                    검색
                </button>
            </div>

            {loading && (
                <p className="mt-4">
                    검색 중...
                </p>
            )}

            <div className="mt-6 grid gap-4">
                {reviews.map((review) => (
                    <div
                        key={review.id}
                        className="rounded border p-4"
                    >
                        <div className="flex justify-between">
                            <span className="font-semibold">
                                {review.product_name}
                            </span>

                            <span>
                                ⭐ {review.rating}
                            </span>
                        </div>

                        <p className="mt-3">
                            {review.content}
                        </p>

                        <p className="mt-2 text-sm text-gray-500">
                            {review.sentiment}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}