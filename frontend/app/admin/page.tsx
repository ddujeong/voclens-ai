import FloatingAdminChat from "@/components/dashboard/FloatingAdminChat";
import { getKpi, getProductStats, getVoc, getSentiment } from "@/services/dashboard";
import VocKeywordChart from "@/components/dashboard/VocKeywordChart";
import SentimentDonutChart from "@/components/dashboard/SentimentDonutChart";

const getRiskColor = (rate: number) => {
    if (rate >= 70) return "bg-red-500";
    if (rate >= 40) return "bg-yellow-500";
    return "bg-emerald-500";
};

export default async function AdminDashboardPage() {
    const kpi = await getKpi();
    const voc = await getVoc();
    const productStats = await getProductStats();
    const sentiment = await getSentiment();


    const topRiskProducts = [...productStats]
        .sort((a, b) => {
            if (b.negative_rate !== a.negative_rate) {
                return b.negative_rate - a.negative_rate;
            }

            return b.negative_reviews - a.negative_reviews;
        })
        .slice(0, 8);

    return (
        <>
            <main className="mx-auto max-w-7xl px-6 py-10">
                <section className="mb-8">
                    <p className="text-sm font-semibold text-blue-600">
                        VOCLens Admin
                    </p>

                    <h1 className="mt-2 text-4xl font-extrabold text-gray-900">
                        VOC 분석 대시보드
                    </h1>

                    <p className="mt-3 text-gray-600">
                        리뷰 감성, 주요 불만 키워드, 위험 상품을 한눈에 확인하세요.
                    </p>
                </section>

                <section className="grid gap-5 md:grid-cols-3">
                    <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                        <p className="text-sm text-gray-500">총 리뷰 수</p>
                        <p className="mt-3 text-4xl font-extrabold text-gray-900">
                            {kpi.total_reviews.toLocaleString()}
                        </p>
                        <p className="mt-2 text-sm text-gray-500">
                            분석 대상 전체 리뷰
                        </p>
                    </div>

                    <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                        <p className="text-sm text-gray-500">긍정 리뷰 비율</p>
                        <p className="mt-3 text-4xl font-extrabold text-emerald-600">
                            {kpi.positive_rate}%
                        </p>
                        <p className="mt-2 text-sm text-gray-500">
                            고객 만족 신호
                        </p>
                    </div>

                    <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                        <p className="text-sm text-gray-500">부정 리뷰 비율</p>
                        <p className="mt-3 text-4xl font-extrabold text-red-600">
                            {kpi.negative_rate}%
                        </p>
                        <p className="mt-2 text-sm text-gray-500">
                            개선 우선순위 지표
                        </p>
                    </div>
                </section>

                <section className="mt-8 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
                    <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-xl font-bold text-gray-900">
                                    VOC TOP 키워드
                                </h2>
                                <p className="mt-1 text-sm text-gray-500">
                                    고객 리뷰에서 많이 언급된 불만 항목
                                </p>
                            </div>
                        </div>

                        <div className="mt-6">
                            <VocKeywordChart data={voc.top_complaints} />
                        </div>
                    </div>

                    <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                        <h2 className="text-xl font-bold text-gray-900">
                            감성 분포
                        </h2>
                        <p className="mt-1 text-sm text-gray-500">
                            리뷰 감성 분석 결과
                        </p>

                        <div className="mt-6">
                            <SentimentDonutChart
                                data={sentiment}
                            />
                        </div>
                    </div>
                </section>

                <section className="mt-8 rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                    <div className="flex items-center justify-between">
                        <div>
                            <h2 className="text-xl font-bold text-gray-900">
                                상품별 부정 리뷰 위험도
                            </h2>

                            <p className="mt-1 text-sm text-gray-500">
                                부정 리뷰 비율이 높은 상품을 우선적으로 확인하세요.
                            </p>
                        </div>
                    </div>

                    <div className="mt-6 space-y-4">
                        {topRiskProducts.map(
                            (item: {
                                product_id: number;
                                product_name: string;
                                total_reviews: number;
                                negative_reviews: number;
                                negative_rate: number;
                            }) => (
                                <div
                                    key={item.product_id}
                                    className="rounded-2xl border border-gray-100 bg-gray-50 p-4"
                                >
                                    <div className="flex items-start justify-between gap-4">
                                        <div>
                                            <p className="line-clamp-1 font-semibold text-gray-900">
                                                {item.product_name}
                                            </p>

                                            <p className="mt-1 text-sm text-gray-500">
                                                리뷰 {item.total_reviews}건 · 부정{" "}
                                                {item.negative_reviews}건
                                            </p>
                                        </div>

                                        <span className="rounded-full bg-red-100 px-3 py-1 text-xs font-bold text-red-700">
                                            {item.negative_rate}%
                                        </span>
                                    </div>

                                    <div className="mt-4 h-3 rounded-full bg-gray-200">
                                        <div
                                            className={`h-3 rounded-full ${getRiskColor(item.negative_rate)}`}
                                            style={{
                                                width: `${item.negative_rate}%`,
                                            }}
                                        />
                                    </div>
                                </div>
                            )
                        )}
                    </div>
                </section>
            </main>
            <FloatingAdminChat />
        </>
    );
}