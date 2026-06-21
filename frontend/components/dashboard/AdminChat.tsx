"use client";

import { useState } from "react";
import { askAdminChat } from "@/services/dashboard";
import ReactMarkdown from "react-markdown";

export default function AdminChat() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);

    const handleAsk = async () => {
        if (!question.trim()) return;

        try {
            setLoading(true);
            const result = await askAdminChat(question);
            setAnswer(result.answer);
        } catch (error) {
            console.error(error);
            alert("챗봇 요청 실패");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="mt-6">
            <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="요즘 고객들이 가장 불만인 점은?"
                className="w-full border p-3"
                rows={4}
            />

            <button onClick={handleAsk} className="mt-4 border px-4 py-2">
                {loading ? "분석 중..." : "질문하기"}
            </button>

            {answer && (
                <section className="mt-8 rounded border p-4">
                    <h2 className="text-lg font-bold">답변</h2>

                    <div className="prose mt-4 max-w-none">
                        <ReactMarkdown>{answer}</ReactMarkdown>
                    </div>
                </section>
            )}
        </div>
    );
}