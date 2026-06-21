import AdminChat from "@/components/dashboard/AdminChat";

export default function AdminChatPage() {
    return (
        <main className="p-8">
            <h1 className="text-2xl font-bold">
                AI 운영자 비서
            </h1>

            <AdminChat />
        </main>
    );
}