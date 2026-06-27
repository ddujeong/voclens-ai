"use client";

import { useState } from "react";
import { createReview } from "@/services/review";

interface Props {
    productId: string;
}

export default function ReviewForm({ productId }: Props) {
    const [rating, setRating] = useState(5);
    const [content, setContent] = useState("");
    const [submitting, setSubmitting] = useState(false);

    const handleSubmit = async (
        e: React.FormEvent<HTMLFormElement>
    ) => {
        e.preventDefault();

        if (!content.trim()) {
            alert("리뷰 내용을 입력해주세요.");
            return;
        }

        try {
            setSubmitting(true);

            await createReview(
                productId,
                rating,
                content
            );

            alert("리뷰가 등록되었습니다.");

            setRating(5);
            setContent("");

            window.location.reload();
        } catch (error) {
            console.error(error);
            alert("리뷰 등록 실패");
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-5">
            <div>
                <p className="text-sm font-semibold text-gray-700">
                    별점
                </p>

                <div className="mt-3 flex gap-2">
                    {[1, 2, 3, 4, 5].map((value) => (
                        <button
                            key={value}
                            type="button"
                            onClick={() => setRating(value)}
                            className={`text-3xl transition ${value <= rating
                                    ? "text-yellow-400"
                                    : "text-gray-300"
                                }`}
                        >
                            ★
                        </button>
                    ))}
                </div>

                <p className="mt-2 text-sm text-gray-500">
                    {rating}점
                </p>
            </div>

            <div>
                <p className="text-sm font-semibold text-gray-700">
                    리뷰 내용
                </p>

                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    className="mt-3 w-full resize-none rounded-2xl border border-gray-200 bg-gray-50 p-4 text-sm text-gray-900 outline-none transition focus:border-blue-500 focus:bg-white"
                    rows={5}
                    placeholder="상품 사용 후기를 작성해주세요."
                />
            </div>

            <button
                type="submit"
                disabled={submitting}
                className="w-full rounded-2xl bg-blue-600 px-5 py-4 text-sm font-bold text-white transition hover:bg-blue-700 disabled:bg-gray-300"
            >
                {submitting ? "등록 중..." : "리뷰 등록"}
            </button>
        </form>
    );
}