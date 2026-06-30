export interface Product {
    id: number;
    name: string;
    brand: string;
    category: string;
    price: number;

    average_rating?: number;
    review_count?: number;
}