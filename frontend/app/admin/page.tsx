import { getKpi, getProductStats, getVoc } from "@/services/dashboard";

export default async function AdminDashboardPage() {
    const kpi = await getKpi();
    const voc = await getVoc();
    const productStats = await getProductStats();

    return (
        <main className="p-8">
            <h1 className="text-2xl font-bold">VOCLens Dashboard</h1>

            <section className="mt-6 grid gap-4 md:grid-cols-3">
                <div className="rounded border p-4">
                    <p className="text-sm text-gray-500">총 리뷰 수</p>
                    <p className="text-2xl font-bold">{kpi.total_reviews}</p>
                </div>

                <div className="rounded border p-4">
                    <p className="text-sm text-gray-500">긍정 리뷰 비율</p>
                    <p className="text-2xl font-bold">{kpi.positive_rate}%</p>
                </div>

                <div className="rounded border p-4">
                    <p className="text-sm text-gray-500">부정 리뷰 비율</p>
                    <p className="text-2xl font-bold">{kpi.negative_rate}%</p>
                </div>
            </section>

            <section className="mt-8 rounded border p-4">
                <h2 className="text-xl font-bold">VOC TOP 키워드</h2>

                <div className="mt-4 grid gap-2">
                    {voc.top_complaints.map(
                        (item: { keyword: string; count: number }, index: number) => (
                            <div key={item.keyword} className="flex justify-between border-b py-2">
                                <span>
                                    {index + 1}. {item.keyword}
                                </span>
                                <span>{item.count}건</span>
                            </div>
                        )
                    )}
                </div>
            </section>

            <section className="mt-8 rounded border p-4">
                <h2 className="text-xl font-bold">상품별 부정 리뷰 비율</h2>

                <div className="mt-4 grid gap-2">
                    {productStats.map(
                        (item: {
                            product_id: number;
                            product_name: string;
                            total_reviews: number;
                            negative_reviews: number;
                            negative_rate: number;
                        }) => (
                            <div key={item.product_id} className="border-b py-2">
                                <p className="font-semibold">{item.product_name}</p>
                                <p className="text-sm text-gray-600">
                                    리뷰 {item.total_reviews}건 / 부정 {item.negative_reviews}건 /{" "}
                                    {item.negative_rate}%
                                </p>
                            </div>
                        )
                    )}
                </div>
            </section>
        </main>
    );
}