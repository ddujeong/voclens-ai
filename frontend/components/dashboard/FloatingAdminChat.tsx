"use client";

import { useState } from "react";
import AdminChat from "@/components/dashboard/AdminChat";

export default function FloatingAdminChat() {
    const [open, setOpen] = useState(false);

    return (
        <>
            {open && (
                <div className="fixed bottom-24 right-6 z-50 h-[640px] w-[420px] overflow-hidden rounded-3xl border border-gray-200 bg-white shadow-2xl">
                    <div className="flex items-center justify-between border-b px-5 py-4">
                        <div>
                            <h2 className="font-bold text-gray-900">
                                AI 운영자 비서
                            </h2>
                            <p className="text-xs text-gray-500">
                                VOC 분석 · 위험 상품 탐지
                            </p>
                        </div>

                        <button
                            onClick={() => setOpen(false)}
                            className="rounded-full px-3 py-1 text-sm hover:bg-gray-100"
                        >
                            닫기
                        </button>
                    </div>

                    <div className="h-[580px] overflow-y-auto p-5">
                        <AdminChat />
                    </div>
                </div>
            )}

            <button
                onClick={() => setOpen((prev) => !prev)}
                className="fixed bottom-6 right-6 z-50 rounded-full bg-blue-600 px-6 py-4 font-bold text-white shadow-xl transition hover:bg-blue-700"
            >
                AI 비서
            </button>
        </>
    );
}