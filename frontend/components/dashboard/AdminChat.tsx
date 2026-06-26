"use client";

import { useState } from "react";
import { askAdminChat } from "@/services/dashboard";
import ReactMarkdown from "react-markdown";

type RiskProduct = {
    product_id: number;
    product_name: string;
    category: string;
    negative_count: number;
};

type ChatResponse = {
    answer: string;
    risk_products?: RiskProduct[];
    category?: string | null;
    tag?: string | null;
};

export default function AdminChat() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [riskProducts, setRiskProducts] = useState<RiskProduct[]>([]);
    const [loading, setLoading] = useState(false);
    const [selectedTag, setSelectedTag] = useState<string | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

    const handleAsk = async () => {
        if (!question.trim()) return;

        try {
            setLoading(true);

            const result: ChatResponse = await askAdminChat(question);

            setAnswer(result.answer);
            setRiskProducts(result.risk_products ?? []);
            setSelectedCategory(result.category ?? null);
            setSelectedTag(result.tag ?? null);
        } catch (error) {
            console.error(error);
            alert("챗봇 요청 실패");
        } finally {
            setLoading(false);
        }
    };

    const handleProductAnalyze = async (product: RiskProduct) => {

        const tagText = selectedTag ?? "전체";
        const productQuestion = `${product.product_name} 상품의 ${tagText} 관련 VOC를 분석해줘`;

        try {
            setLoading(true);
            setQuestion(productQuestion);
            setSelectedCategory(product.category);
            setSelectedTag(tagText === "전체" ? null : tagText);
            const result: ChatResponse = await askAdminChat(
                productQuestion,
                product.product_id,
                product.category
            );

            setAnswer(result.answer);
            setRiskProducts(result.risk_products ?? []);
        } catch (error) {
            console.error(error);
            alert("상품 VOC 분석 실패");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="mt-6 space-y-6">
            <section>
                <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="예: 여성의류에서 착용감 불만 많은 상품 찾아줘"
                    className="w-full border p-3"
                    rows={4}
                />

                <button
                    onClick={handleAsk}
                    className="mt-4 border px-4 py-2"
                >
                    {loading ? "분석 중..." : "질문하기"}
                </button>
            </section>
            {selectedTag && (
                <div className="mb-4 rounded border p-3 text-sm text-gray-600">
                    <div>분석 기준: {selectedTag}</div>
                    {selectedCategory && <div>카테고리: {selectedCategory}</div>}
                </div>
            )}
            {answer && (
                <section className="rounded border p-4">
                    <h2 className="text-lg font-bold">답변</h2>

                    <div className="prose mt-4 max-w-none">
                        <ReactMarkdown>{answer}</ReactMarkdown>
                    </div>

                    {riskProducts.length > 0 && (
                        <div className="mt-6 space-y-2">
                            <h3 className="font-bold">위험 상품 후보</h3>

                            {riskProducts.map((product) => (
                                <button
                                    key={product.product_id}
                                    onClick={() => handleProductAnalyze(product)}
                                    className="block w-full rounded border p-3 text-left hover:bg-gray-50"
                                >
                                    <div className="font-semibold">
                                        {product.product_name}
                                    </div>
                                    <div className="text-sm text-gray-500">
                                        {product.category} · 부정 리뷰{" "}
                                        {product.negative_count}건
                                    </div>
                                </button>
                            ))}
                        </div>
                    )}
                </section>
            )}
        </div>
    );
}