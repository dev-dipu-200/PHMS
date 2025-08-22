from db_config import get_connection
from typing import Iterable, Optional, Sequence, Any, Dict, Union, List


def execute_query(
    query: str,
    params: Optional[Sequence[Any]] = None,
    fetch: bool = False,
    many: bool = False
) -> Union[List[Dict], int, None]:
    """
    Execute a query and return:
      - list of dicts if fetch=True
      - lastrowid if INSERT/UPDATE/DELETE
      - None if nothing
    """
    conn = get_connection()
    # Set row factory so we can easily convert to dict
    conn.row_factory = lambda cursor, row: {
        col[0]: row[idx] for idx, col in enumerate(cursor.description)
    }
    cur = conn.cursor()

    if params is None:
        params = ()

    if many:
        cur.executemany(query, params)
    else:
        cur.execute(query, params)

    rows = cur.fetchall() if fetch else None
    last_id = cur.lastrowid

    conn.commit()
    conn.close()

    if fetch:
        return rows
    return last_id


def fetch_one(query: str, params: Optional[Sequence[Any]] = None) -> Optional[Dict]:
    rows = execute_query(query, params=params, fetch=True)
    if rows and len(rows) > 0:
        return rows[0]
    return None


def fetch_all(query: str, params: Optional[Sequence[Any]] = None) -> List[Dict]:
    rows = execute_query(query, params=params, fetch=True)
    return rows if rows else []


def format_currency(v: float) -> str:
    try:
        return f"₹{float(v):,.2f}"
    except Exception:
        return str(v)


# ---------- Business helpers ----------

def get_customer_bills(customer_id: int):
    return fetch_all("""
        SELECT b.id, b.bill_date, b.total_amount, b.payment_status
        FROM bills b
        WHERE b.customer_id = ?
        ORDER BY b.bill_date DESC, b.id DESC
    """, (customer_id,))


def get_last_bill(customer_id: int):
    bill = fetch_one("""
        SELECT b.id, b.bill_date, b.total_amount, b.payment_status
        FROM bills b
        WHERE b.customer_id = ?
        ORDER BY b.bill_date DESC, b.id DESC
        LIMIT 1
    """, (customer_id,))
    if not bill:
        return None

    items = fetch_all("""
        SELECT bi.quantity, bi.price, m.name AS medicine_name, m.id AS medicine_id
        FROM bill_items bi
        JOIN medicines m ON m.id = bi.medicine_id
        WHERE bi.bill_id = ?
    """, (bill["id"],))

    bill["items"] = items
    return bill


def create_bill(customer_id: Optional[int], items: Iterable[dict]) -> int:
    total = sum(float(it["price"]) * int(it["quantity"]) for it in items)
    bill_id = execute_query(
        "INSERT INTO bills (customer_id, total_amount, payment_status) VALUES (?, ?, 'unpaid')",
        (customer_id, total)
    )
    for it in items:
        execute_query("""
            INSERT INTO bill_items (bill_id, medicine_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (bill_id, it["medicine_id"], int(it["quantity"]), float(it["price"])))
        # reduce stock
        execute_query("UPDATE medicines SET stock = stock - ? WHERE id = ?", (int(it["quantity"]), it["medicine_id"]))
    return bill_id


def create_purchase(supplier_id: int, items: Iterable[dict], notes: str = "") -> int:
    total = sum(float(it["price"]) * int(it["quantity"]) for it in items)
    pid = execute_query(
        "INSERT INTO purchases (supplier_id, total_amount, notes) VALUES (?, ?, ?)",
        (supplier_id, total, notes)
    )
    for it in items:
        execute_query("""
            INSERT INTO purchase_items (purchase_id, medicine_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (pid, it["medicine_id"], int(it["quantity"]), float(it["price"])))
        # increase stock
        execute_query("UPDATE medicines SET stock = stock + ? WHERE id = ?", (int(it["quantity"]), it["medicine_id"]))
    return pid


def record_payment(bill_id: int, amount: float, method: str, reference: str = "") -> int:
    pay_id = execute_query("""
        INSERT INTO payments (bill_id, amount, method, reference) VALUES (?, ?, ?, ?)
    """, (bill_id, float(amount), method, reference))

    # Update status if fully paid
    totals = fetch_one("""
        SELECT
          (SELECT COALESCE(SUM(amount),0) FROM payments WHERE bill_id = ?) AS paid,
          (SELECT total_amount FROM bills WHERE id = ?) AS total
    """, (bill_id, bill_id))

    if totals and float(totals["paid"]) >= float(totals["total"]):
        execute_query("UPDATE bills SET payment_status = 'paid' WHERE id = ?", (bill_id,))

    return pay_id


def get_medicine_stock(medicine_id: str) -> Optional[int]:
    med = fetch_one("SELECT stock FROM medicines WHERE id = ?", (medicine_id,))
    if med:
        return med["stock"]
    return None


def update_medicine_stock(medicine_id: str, new_stock: int) -> bool:
    res = execute_query("UPDATE medicines SET stock = ? WHERE id = ?", (new_stock, medicine_id))
    return res is not None


def get_single_medicine(medicine_id: str) -> Optional[Dict]:
    return fetch_one("SELECT * FROM medicines WHERE id = ?", (medicine_id,))


def search_medicines(term: str) -> Iterable[Dict]:
    like_term = f"%{term}%"
    return fetch_all("""
        SELECT * FROM medicines
        WHERE id LIKE ? OR name LIKE ? OR manufacturer LIKE ? OR category LIKE ? OR batch_number LIKE ? OR expiry LIKE ?
        ORDER BY name ASC
        LIMIT 100
    """, (like_term, like_term, like_term, like_term, like_term, like_term))
