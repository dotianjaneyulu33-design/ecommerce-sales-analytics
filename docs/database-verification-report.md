# Database Verification Report (Day 29)

## Row count sanity check (vs Day 25 load)
| Table | Expected | Actual | Match |
|---|---|---|---|
| product | 21,273 | 21,273 | ✅ |
| review | 20,333 | 20,333 | ✅ |
| sales | 21,273 | 21,273 | ✅ |
| platform | 2 | 2 | ✅ |
| category | 9 | 9 | ✅ |

No data drift or corruption since the Day 25 load.

## Platform comparison summary
| Platform | Products | Avg Price | Avg Rating | Total Revenue |
|---|---|---|---|---|
| Amazon | 1,351 | ₹3,304.80 | 4.09 | ₹1,41,48,454.93 |
| Flipkart | 19,922 | ₹1,973.40 | 3.81 | ₹12,80,59,901.00 |

**Caveat:** Flipkart's higher total revenue is largely a sample-size artifact — the dataset contains ~15x more Flipkart products than Amazon products. This is not evidence that Flipkart genuinely outsells Amazon; it reflects the underlying Kaggle sample composition (see Day 9 dataset analysis notes). Amazon products in this sample are, on average, priced higher and rated higher.

## Revenue by platform × category
| Platform | Category | Revenue | Products | Avg Rating |
|---|---|---|---|---|
| Flipkart | Fashion | ₹8,80,46,948 | 11,710 | 3.82 |
| Flipkart | Home & Kitchen | ₹2,02,03,896 | 2,918 | 3.87 |
| Amazon | Electronics | ₹1,07,44,784.09 | 865 | **4.11** (highest of any meaningful category) |
| Flipkart | Electronics | ₹79,89,135 | 1,742 | 3.84 |
| Flipkart | Automotive | ₹37,29,552 | 1,010 | 3.67 |
| Amazon | Home & Kitchen | ₹33,64,811.84 | 450 | 4.04 |
| Flipkart | Other | ₹28,13,896 | 544 | 3.80 |
| Flipkart | Toys & Baby | ₹26,04,216 | 810 | 3.86 |
| Flipkart | Beauty & Personal Care | ₹13,39,283 | 709 | 3.47 |
| Flipkart | Sports & Fitness | ₹6,74,662 | 166 | 4.18 |
| Flipkart | Office & Stationery | ₹6,58,313 | 313 | 3.89 |
| Amazon | Office & Stationery | ₹26,977 | 31 | 4.31 |
| Amazon | Automotive, Other, Beauty, Toys | <₹10,000 each | 1 each | Not statistically meaningful — single-product categories |

**Key takeaway:** Electronics and Home & Kitchen are the only categories with meaningful product counts on both platforms — these are the categories where cross-platform comparison is statistically credible. Amazon's near-total absence from Fashion (its largest Flipkart category) confirms the category mismatch flagged back in Day 9.

## Conclusion
Database is fully populated, verified against source data with zero drift, and the two saved views (`v_platform_category_revenue`, `v_product_summary`) provide reusable, tested query interfaces ready for the Spring Boot analytics APIs (Day 57) and React dashboard (Day 71-75).
