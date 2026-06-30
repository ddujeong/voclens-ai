import FloatingAdminChat from "@/components/dashboard/FloatingAdminChat";
import {
    getKpi,
    getProductStats,
    getVoc,
    getSentiment,
} from "@/services/dashboard";
import VocKeywordChart from "@/components/dashboard/VocKeywordChart";
import SentimentDonutChart from "@/components/dashboard/SentimentDonutChart";

type ProductStat = {
    product_id: number;
    product_name: string;
    total_reviews: number;
    negative_reviews: number;
    negative_rate: number;
};

export default async function AdminDashboardPage() {
    const [kpi, voc, productStats, sentiment] = await Promise.all([
        getKpi(),
        getVoc(),
        getProductStats(),
        getSentiment(),
    ]);

    const typedProductStats = productStats as ProductStat[];

    const topRiskProducts = [...typedProductStats]
        .sort((a, b) => b.negative_reviews - a.negative_reviews)
        .slice(0, 8);

    const maxNegative = Math.max(
        ...topRiskProducts.map((item) => item.negative_reviews),
        1
    );

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
                        <h2 className="text-xl font-bold text-gray-900">
                            VOC TOP 키워드
                        </h2>
                        <p className="mt-1 text-sm text-gray-500">
                            고객 리뷰에서 많이 언급된 불만 항목
                        </p>

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
                            <SentimentDonutChart data={sentiment} />
                        </div>
                    </div>
                </section>

                <section className="mt-8 rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
                    <h2 className="text-xl font-bold text-gray-900">
                        상품별 부정 리뷰 TOP
                    </h2>

                    <p className="mt-1 text-sm text-gray-500">
                        부정 리뷰가 많이 누적된 상품을 우선적으로 확인하세요.
                    </p>

                    <div className="mt-6 space-y-4">
                        {topRiskProducts.map((item, index) => {
                            const width =
                                (item.negative_reviews / maxNegative) * 100;

                            return (
                                <div
                                    key={item.product_id}
                                    className="rounded-2xl border border-gray-100 bg-gray-50 px-5 py-3"
                                >
                                    <div className="flex items-start justify-between gap-4">
                                        <div className="flex min-w-0 items-start gap-3">
                                            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-red-500 text-sm font-bold text-white">
                                                {index + 1}
                                            </div>

                                            <div className="min-w-0">
                                                <p className="line-clamp-1 font-semibold text-gray-900">
                                                    {item.product_name}
                                                </p>

                                                <p className="mt-1 text-sm text-gray-500">
                                                    리뷰 {item.total_reviews}건 · 부정{" "}
                                                    {item.negative_reviews}건
                                                </p>
                                            </div>
                                        </div>

                                        <span className="shrink-0 rounded-full bg-red-100 px-3 py-1 text-xs font-bold text-red-700">
                                            {item.negative_reviews}건
                                        </span>
                                    </div>

                                    <div className="mt-3 h-2.5 rounded-full bg-gray-200">
                                        <div
                                            className="h-2.5 rounded-full bg-red-500"
                                            style={{
                                                width: `${width}%`,
                                            }}
                                        />
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </section>
            </main>

            <FloatingAdminChat />
        </>
    );
}