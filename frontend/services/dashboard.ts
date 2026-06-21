const BASE_URL = "http://127.0.0.1:8000";

export async function getKpi() {
    const response = await fetch(
        `${BASE_URL}/admin/dashboard/kpi`,
        { cache: "no-store" }
    );

    return response.json();
}

export async function getVoc() {
    const response = await fetch(
        `${BASE_URL}/admin/dashboard/voc`,
        { cache: "no-store" }
    );

    return response.json();
}

export async function getProductStats() {
    const response = await fetch(
        `${BASE_URL}/admin/dashboard/products`,
        { cache: "no-store" }
    );

    return response.json();
}

export async function getSentiment() {
    const response = await fetch(
        `${BASE_URL}/admin/dashboard/sentiment`,
        {
            cache: "no-store",
        }
    );

    return response.json();
}

export async function searchReviews(
    keyword: string
) {
    const response = await fetch(
        `${BASE_URL}/admin/reviews/search?keyword=${keyword}`,
        {
            cache: "no-store",
        }
    );

    if (!response.ok) {
        throw new Error("리뷰 검색 실패");
    }

    return response.json();
}
export async function askAdminChat(
    question: string
) {
    const response = await fetch(
        `${BASE_URL}/admin/chat`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                question,
            }),
        }
    );

    if (!response.ok) {
        throw new Error("챗봇 요청 실패");
    }

    return response.json();
}