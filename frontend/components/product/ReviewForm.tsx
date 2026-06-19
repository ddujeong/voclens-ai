"use client";

import { useState } from "react";
import { createReview } from "@/services/review";

interface Props {
    productId: string;
}

export default function ReviewForm({ productId }: Props) {
    const [rating, setRating] = useState(5);
    const [content, setContent] = useState("");

    const handleSubmit = async (
        e: React.FormEvent<HTMLFormElement>
    ) => {
        e.preventDefault();

        try {
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
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="mt-8 rounded border p-4"
        >
            <h2 className="mb-4 text-lg font-bold">
                리뷰 작성
            </h2>

            <select
                value={rating}
                onChange={(e) =>
                    setRating(Number(e.target.value))
                }
                className="mb-4 border p-2"
            >
                <option value={5}>5점</option>
                <option value={4}>4점</option>
                <option value={3}>3점</option>
                <option value={2}>2점</option>
                <option value={1}>1점</option>
            </select>

            <textarea
                value={content}
                onChange={(e) =>
                    setContent(e.target.value)
                }
                className="mb-4 w-full border p-2"
                rows={4}
                placeholder="리뷰를 작성해주세요"
            />

            <button
                type="submit"
                className="rounded border px-4 py-2"
            >
                등록
            </button>
        </form>
    );
}