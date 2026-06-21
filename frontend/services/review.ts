const BASE_URL = "http://127.0.0.1:8000";

export async function getReviews(productId: string) {
    const response = await fetch(`${BASE_URL}/products/${productId}/reviews`, {
        cache: "no-store",
    });

    if (!response.ok) {
        throw new Error("리뷰 목록 조회 실패");
    }

    return response.json();
}
export async function createReview(
    productId: string,
    rating: number,
    content: string
) {
    const response = await fetch(
        `${BASE_URL}/products/${productId}/reviews`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                rating,
                content,
            }),
        }
    );

    if (!response.ok) {
        throw new Error("리뷰 작성 실패");
    }

    return response.json();
}