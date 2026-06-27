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

type VocAnalysis = {
    summary: string;
    positive: string[];
    negative: string[];
    insight: string;
    improvements: string[];
};

type ChatResponse = {
    answer: string;
    analysis?: VocAnalysis | null;
    risk_products?: RiskProduct[];
    category?: string | null;
    tag?: string | null;
};

type ChatMessage = {
    role: "user" | "assistant";
    content: string;
    analysis?: VocAnalysis | null;
    riskProducts?: RiskProduct[];
};

function AnalysisCard({
    title,
    icon,
    items,
    text,
}: {
    title: string;
    icon: string;
    items?: string[];
    text?: string;
}) {
    if ((!items || items.length === 0) && !text) return null;

    return (
        <div className="rounded-xl border border-gray-200 bg-white p-3 shadow-sm">
            <div className="mb-2 flex items-center gap-2 text-sm font-bold text-gray-900">
                <span>{icon}</span>
                <span>{title}</span>
            </div>

            {text && (
                <p className="text-sm leading-6 text-gray-700">
                    {text}
                </p>
            )}

            {items && items.length > 0 && (
                <ul className="space-y-1 text-sm text-gray-700">
                    {items.map((item, index) => (
                        <li key={index}>• {item}</li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default function AdminChat() {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [loading, setLoading] = useState(false);

    const [selectedTag, setSelectedTag] = useState<string | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
    const loadingTexts = [
        "리뷰를 분석하는 중...",
        "감성을 분류하는 중...",
        "운영 인사이트를 생성하는 중...",
        "VOC를 요약하는 중...",
    ];

    const loadingText =
        loadingTexts[messages.length % loadingTexts.length];

    const handleAsk = async () => {
        const trimmedQuestion = question.trim();
        if (!trimmedQuestion) return;

        try {
            setLoading(true);

            setMessages((prev) => [
                ...prev,
                { role: "user", content: trimmedQuestion },
            ]);

            setQuestion("");

            const result: ChatResponse = await askAdminChat(trimmedQuestion);

            setSelectedCategory(result.category ?? null);
            setSelectedTag(result.tag ?? null);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: result.answer,
                    analysis: result.analysis ?? null,
                    riskProducts: result.risk_products ?? [],
                },
            ]);
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

            setSelectedCategory(product.category);
            setSelectedTag(tagText === "전체" ? null : tagText);

            setMessages((prev) => [
                ...prev,
                { role: "user", content: productQuestion },
            ]);

            const result: ChatResponse = await askAdminChat(
                productQuestion,
                product.product_id,
                product.category
            );

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: result.answer,
                    analysis: result.analysis ?? null,
                    riskProducts: result.risk_products ?? [],
                },
            ]);
        } catch (error) {
            console.error(error);
            alert("상품 VOC 분석 실패");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-full flex-col">
            <div className="flex-1 space-y-4 overflow-y-auto pr-1">
                {messages.length === 0 && (
                    <div className="rounded-2xl bg-gray-50 p-4 text-sm text-gray-600">
                        <p className="font-semibold text-gray-900">예시 질문</p>

                        <div className="mt-3 space-y-2">
                            {[
                                "여성의류에서 사이즈 불만 많은 상품 찾아줘",
                                "패션슈즈에서 착화감 불만 많은 상품 찾아줘",
                                "잡화에서 어떤 불만 있어?",
                            ].map((example) => (
                                <button
                                    key={example}
                                    onClick={() => setQuestion(example)}
                                    className="block w-full rounded-xl border bg-white p-3 text-left hover:border-blue-400"
                                >
                                    {example}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`flex ${message.role === "user"
                            ? "justify-end"
                            : "justify-start"
                            }`}
                    >
                        <div
                            className={`rounded-2xl p-3 text-sm leading-6 ${message.role === "user"
                                ? "ml-auto max-w-[82%] bg-blue-600 text-white"
                                : "mr-auto w-full bg-gray-100 text-gray-900"
                                }`}
                        >
                            {!message.analysis && (
                                <div className="prose prose-sm max-w-none prose-p:my-1 prose-ul:my-1 prose-li:my-0">
                                    <ReactMarkdown>
                                        {message.content}
                                    </ReactMarkdown>
                                </div>
                            )}

                            {message.analysis && (
                                <div className="space-y-2">
                                    <AnalysisCard
                                        title="핵심 요약"
                                        icon="📌"
                                        text={message.analysis.summary}
                                    />

                                    <AnalysisCard
                                        title="긍정 포인트"
                                        icon="🟢"
                                        items={message.analysis.positive}
                                    />

                                    <AnalysisCard
                                        title="부정 포인트"
                                        icon="🔴"
                                        items={message.analysis.negative}
                                    />

                                    <AnalysisCard
                                        title="운영 인사이트"
                                        icon="💡"
                                        text={message.analysis.insight}
                                    />

                                    <AnalysisCard
                                        title="개선 제안"
                                        icon="✅"
                                        items={message.analysis.improvements}
                                    />
                                </div>
                            )}

                            {message.riskProducts &&
                                message.riskProducts.length > 0 && (
                                    <div className="mt-4 space-y-2">
                                        <p className="text-xs font-bold text-gray-500">
                                            위험 상품 후보
                                        </p>

                                        {message.riskProducts.map((product) => (
                                            <button
                                                key={product.product_id}
                                                onClick={() =>
                                                    handleProductAnalyze(product)
                                                }
                                                className="block w-full rounded-xl border border-gray-200 bg-white p-3 text-left text-gray-900 transition hover:border-blue-400 hover:shadow-sm"
                                            >
                                                <div className="font-semibold">
                                                    {product.product_name}
                                                </div>

                                                <div className="mt-1 text-xs text-gray-500">
                                                    {product.category} · 부정 리뷰{" "}
                                                    {product.negative_count}건
                                                </div>
                                            </button>
                                        ))}
                                    </div>
                                )}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex justify-start">
                        <div className="rounded-2xl border border-gray-200 bg-white px-5 py-4 shadow-sm">
                            <div className="flex items-center gap-3">
                                <div className="flex gap-1">
                                    <span className="h-2.5 w-2.5 animate-bounce rounded-full bg-blue-500"></span>

                                    <span
                                        className="h-2.5 w-2.5 animate-bounce rounded-full bg-blue-500"
                                        style={{ animationDelay: "0.15s" }}
                                    />

                                    <span
                                        className="h-2.5 w-2.5 animate-bounce rounded-full bg-blue-500"
                                        style={{ animationDelay: "0.3s" }}
                                    />
                                </div>

                                <div>
                                    <p className="text-sm font-semibold text-gray-900">
                                        🤖 AI 운영 비서
                                    </p>

                                    <p className="text-xs text-gray-500">
                                        {loadingText}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {(selectedTag || selectedCategory) && (
                <div className="mt-4 flex flex-wrap gap-2 text-xs">
                    {selectedCategory && (
                        <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-600">
                            {selectedCategory}
                        </span>
                    )}
                    {selectedTag && (
                        <span className="rounded-full bg-blue-100 px-3 py-1 text-blue-700">
                            {selectedTag}
                        </span>
                    )}
                </div>
            )}

            <div className="mt-4 flex gap-2">
                <input
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            e.preventDefault();
                            handleAsk();
                        }
                    }}
                    placeholder="운영자 질문을 입력하세요..."
                    className="flex-1 rounded-2xl border border-gray-200 px-4 py-3 text-sm text-gray-900 outline-none focus:border-blue-500"
                />

                <button
                    onClick={handleAsk}
                    disabled={loading}
                    className="rounded-2xl bg-blue-600 px-5 py-3 text-sm font-bold text-white transition hover:bg-blue-700 disabled:bg-gray-300"
                >
                    전송
                </button>
            </div>
        </div>
    );
}