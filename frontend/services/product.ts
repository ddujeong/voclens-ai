const BASE_URL = "http://127.0.0.1:8000";

export async function getProducts() {
    const response = await fetch(`${BASE_URL}/products`, {
        cache: "no-store",
    });

    if (!response.ok) {
        throw new Error("상품 목록 조회 실패");
    }

    return response.json();
}

export async function getProduct(productId: string) {
    const response = await fetch(`${BASE_URL}/products/${productId}`, {
        cache: "no-store",
    });

    if (!response.ok) {
        throw new Error("상품 상세 조회 실패");
    }

    return response.json();
}

export async function getProductSummary(
    productId: string
) {
    const response = await fetch(
        `${BASE_URL}/products/${productId}/summary`,
        {
            cache: "no-store",
        }
    );

    if (!response.ok) {
        throw new Error("AI 리뷰 요약 조회 실패");
    }

    return response.json();
}