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