| Dimension    | Engineering definition          | Olist example                |
| ------------ | ------------------------------- | ---------------------------- |
| Completeness | Required attributes are present | `customer_id` not null       |
| Validity     | Values satisfy business rules   | payment value ≥ 0            |
| Uniqueness   | Business keys are unique        | `order_id`                   |
| Consistency  | Tables agree with each other    | customer exists              |
| Accuracy     | Values reflect reality          | delivery date after purchase |
| Freshness    | Data arrives on time            | daily load before SLA        |