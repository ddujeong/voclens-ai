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