import ReviewSearch from "@/components/dashboard/ReviewSearch";

export default function AdminReviewsPage() {
    return (
        <main className="p-8">
            <h1 className="text-2xl font-bold">
                리뷰 검색
            </h1>

            <ReviewSearch />
        </main>
    );
}