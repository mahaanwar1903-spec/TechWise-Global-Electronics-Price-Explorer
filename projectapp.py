from flask import Flask, render_template, request, redirect
from flask import session
import sqlite3
import requests

# ------------------------------------------------
# SET YOUR TOKEN HERE
# ------------------------------------------------
EBAY_PROD_TOKEN = "v^1.1#i^1#r^0#I^3#p^3#f^0#t^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"


app = Flask(__name__)


def fetch_all_ebay_electronics():
    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    headers = {
        "Authorization": f"Bearer {EBAY_PROD_TOKEN}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    all_items = []
    limit = 100     # max per request
    offset = 0

    while True:
        params = {
            "q": "electronics",
            "limit": limit,
            "offset": offset
        }

        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            print("eBay API Error:", resp.status_code, resp.text)
            break

        data = resp.json()
        items = data.get("itemSummaries", [])

        if not items:
            break  # no more items

        all_items.extend(items)
        offset += limit

        # Optional: Stop after a certain number to avoid too many requests
        # if offset >= 1000:  
        #     break

    # Insert items into DB
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    inserted = 0
    for item in all_items:
        name = item.get("title", "Unknown Product")
        price = float(item.get("price", {}).get("value", 0))
        link = item.get("itemWebUrl", "")
        image = item.get("image", {}).get("imageUrl", "")
        store = "eBay"
        category = "electronics"

        # Avoid duplicates
        cur.execute("SELECT id FROM products WHERE link = ?", (link,))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO products (name, price, store, link, image, category) VALUES (?, ?, ?, ?, ?, ?)",
                (name, price, store, link, image, category)
            )
            inserted += 1

    conn.commit()
    conn.close()
    print(f"Total items fetched: {len(all_items)}, Inserted into DB: {inserted}")

@app.route("/compare")
def compare_products():
    compare_list = session.get("compare_list", [])

    if not compare_list:
        return "No products selected for comparison."

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = f"SELECT * FROM products WHERE id IN ({','.join(['?']*len(compare_list))})"
    cur.execute(query, compare_list)
    products = cur.fetchall()
    conn.close()

    return render_template("compare.html", products=products)


# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            store TEXT,
            link TEXT,
            image TEXT,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_category_column_if_missing():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(products)")
    cols = [row[1] for row in cur.fetchall()]
    if "category" not in cols:
        cur.execute("ALTER TABLE products ADD COLUMN category TEXT")
        conn.commit()
    conn.close()

init_db()
add_category_column_if_missing()


# -----------------------------
# HELPER: SAFE INSERT NO DUPLICATES
# -----------------------------
def insert_product_if_new(name, price, store, link, image=None, category=None):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT id FROM products WHERE link = ? OR (name = ? AND store = ?)",
                (link, name, store))
    exists = cur.fetchone()

    if not exists:
        cur.execute(
            "INSERT INTO products (name, price, store, link, image, category) VALUES (?, ?, ?, ?, ?, ?)",
            (name, price, store, link, image, category)
        )
        conn.commit()

    conn.close()


# -----------------------------
# FETCH ALL CATEGORIES
# -----------------------------
def get_all_categories():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT category 
        FROM products 
        WHERE category IS NOT NULL 
        ORDER BY category
    """)

    rows = cur.fetchall()
    conn.close()
    return [r["category"] for r in rows]


# -----------------------------
# HOME
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    search_query  = request.args.get("search", "")
    category      = request.args.get("category", "")
    min_price     = request.args.get("min_price", "")
    max_price     = request.args.get("max_price", "")
    sort          = request.args.get("sort", "")   # <--- NEW

    sql = "SELECT * FROM products"
    conditions = []
    params = []

    if search_query:
        conditions.append("name LIKE ?")
        params.append(f"%{search_query}%")

    if category:
        conditions.append("category = ?")
        params.append(category)

    if min_price:
        conditions.append("price >= ?")
        params.append(min_price)

    if max_price:
        conditions.append("price <= ?")
        params.append(max_price)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    # ---------------------
    # SORTING PART
    # ---------------------
    if sort == "price_asc":
        sql += " ORDER BY price ASC"
    elif sort == "price_desc":
        sql += " ORDER BY price DESC"

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # PAGINATION SETTINGS
    page = int(request.args.get("page", 1))
    limit = 12
    offset = (page - 1) * limit

    # add limit + offset in SQL
    sql += f" LIMIT {limit} OFFSET {offset}"

    cur.execute(sql, params)
    products = cur.fetchall()

    # For page count
    cur.execute("SELECT COUNT(*) FROM products")
    total_items = cur.fetchone()[0]
    total_pages = (total_items + limit - 1) // limit


    conn.close()

    categories = get_all_categories()
    rate = get_usd_to_pkr_rate()

    return render_template(
        "home.html",
        products=products,
        categories=categories,
        search_query=search_query,
        selected_category=category,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        total_pages=total_pages,
        current_page=page,
        rate=rate
)

@app.route("/fetch_ebay_all")
def fetch_ebay_all():
    fetch_all_ebay_electronics()
    return redirect("/")

# -----------------------------
# ADD PRODUCT PAGES
# -----------------------------
@app.route("/add")
def add_product_page():
    return render_template("add.html")

@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    price = request.form["price"]
    store = request.form["store"]
    link = request.form["link"]
    image = request.form.get("image", "")
    category = request.form["category"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO products(name, price, store, link, image, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, price, store, link, image, category))

    conn.commit()
    conn.close()

    return redirect("/")



# -----------------------------
# DELETE PRODUCT
# -----------------------------
@app.route("/delete/<int:id>")
def delete_product(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


# -----------------------------
# EDIT / UPDATE PRODUCT
# -----------------------------
@app.route("/edit/<int:id>")
def edit_product_page(id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = cur.fetchone()
    conn.close()
    return render_template("edit.html", product=product)

@app.route("/update/<int:id>", methods=["POST"])
def update_product(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE products
        SET name=?, price=?, store=?, link=?, image=?, category=?
        WHERE id=?
    """, (
        request.form["name"],
        request.form["price"],
        request.form["store"],
        request.form["link"],
        request.form.get("image", ""),
        request.form.get("category", None),
        id
    ))
    conn.commit()
    conn.close()
    return redirect("/")


# -----------------------------
# FETCH FROM EBAY API
# -----------------------------
@app.route("/fetch_ebay_production")
def fetch_ebay_production():

    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"

    headers = {
        "Authorization": f"Bearer {EBAY_PROD_TOKEN}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    params = {
        "q": "electronics",
        "limit": 200,
    }

    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code != 200:
        return f"eBay API Error: {resp.status_code} {resp.text}"

    items = resp.json().get("itemSummaries", [])

    rate = get_usd_to_pkr_rate()  # fetch USD→PKR rate

    for item in items:
        price_usd = float(item.get("price", {}).get("value", 0))
        price_pkr = round(price_usd * rate, 2)

        insert_product_if_new(
            name=item.get("title"),
            price=price_pkr,
            store="eBay",
            link=item.get("itemWebUrl"),
            image=item.get("image", {}).get("imageUrl", ""),
            category="electronics"
        )

    return redirect("/")


def get_usd_to_pkr_rate():
    try:
        # Using ExchangeRate-API (free)
        resp = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=PKR")
        data = resp.json()
        rate = data.get("rates", {}).get("PKR", 1)
        return rate
    except Exception as e:
        print("Currency conversion error:", e)
        return 1  # fallback

# -----------------------------
# RUN FLASK APP
# -----------------------------

app.secret_key = "mahahhahawassup"  # required for session usage

@app.route("/compare/add/<int:id>")
def add_to_compare(id):
    # Get current list from session or empty
    compare_list = session.get("compare_list", [])
    
    if id not in compare_list:
        compare_list.append(id)
        # Limit to max 3 products
        if len(compare_list) > 3:
            compare_list = compare_list[-3:]
    
    session["compare_list"] = compare_list
    # redirect back to the page user was on
    return redirect(request.referrer or "/")
if __name__ == "__main__":
    app.run(debug=True)
