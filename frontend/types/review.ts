export interface Review {
    id: number;
    product_id: number;
    rating: number;
    content: string;
    sentiment: string | null;
    created_at: string;
}