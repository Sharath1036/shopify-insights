# GenAI Developer Intern Assignment

## Guidelines:

- **Preferred language**: Python for implementing the solution.
- **Preferred framework**: FastAPI/Flask.
- **Database**: If using a database for persistence, MySQL is preferred.
- **Demoable APIs**: APIs should be demoable via Postman or a UI.
- **Focus**: Develop a robust, scalable, and maintainable backend system.
- **Best practices**: Adhere to OOP principles, SOLID design patterns, clean code, and RESTful API design.
- **High-impact areas**: Use of defined models (e.g., Pydantic), code readability, structure, deduplication, and edge-case handling.

## Requirements:

### Mandatory Section:
Complete **ALL** mandatory requirements to qualify.

#### **Shopify Store Insights-Fetcher Application**
**Context**: Shopify is an e-commerce platform enabling D2C businesses to manage online stores. The task is to design a Python application that fetches a brand's Shopify website content (without using the official Shopify API) and organizes the data into a structured form.

**Minimum insights to fetch**:
1. Whole Product Catalog (list of products).
2. Hero Products (products listed on the homepage).
3. Privacy Policy.
4. Return and Refund Policies.
5. Brand FAQs (e.g., Q: Do you have COD? A: Yes).
6. Social Handles (Instagram, Facebook, TikTok, etc.).
7. Contact details (emails, phone numbers).
8. Brand text context (About the brand).
9. Important links (Order tracking, Contact Us, Blogs).

**API Requirements**:
- Expose a route that accepts a `website_url` (e.g., a Shopify store URL).
- Return a JSON response with the Brand Context object on success.
- Handle errors appropriately:
  - `401` if the website is not found.
  - `500` for internal errors.

**References**:
- Example Shopify sites: [memy.co.in](http://memy.co.in), [hairoriginals.com](http://hairoriginals.com).
- List of Shopify sites: [Top 100 Most Successful Shopify Stores](https://webinopoly.com/blogs/news/top-100-most-successful-shopify-stores).

**Hints**:
1. Use `/products.json` to fetch products.
2. Some features (e.g., FAQs) may vary across stores; research accordingly.
3. Leverage LLMs to structure disorganized data.

### Bonus Section:
Attempt **only after** completing the mandatory section.

1. **Competitor Analysis**:
   - Identify competitors of the given brand (e.g., via web search).
   - Fetch the same insights for competitors' webstores.

2. **Persistence**:
   - Store all data in a SQL database.