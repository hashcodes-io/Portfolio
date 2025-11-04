"""ipnet_demo.ipam
Core IP allocation logic. Deterministic and testable.
"""
from __future__ import annotations
import ipaddress
import sqlite3
import threading
from typing import Optional, List, Tuple


DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS allocations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cidr TEXT NOT NULL,
    ip TEXT NOT NULL UNIQUE,
    meta TEXT
);
CREATE TABLE IF NOT EXISTS pools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cidr TEXT NOT NULL UNIQUE
);
"""

_lock = threading.Lock()

class IPAM:
    def __init__(self, db_path: str = "ipam.db"):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        with self._conn() as c:
            c.executescript(DB_SCHEMA)

    def add_pool(self, cidr: str) -> None:
        net = ipaddress.ip_network(cidr)
        with self._conn() as conn:
            conn.execute("INSERT OR IGNORE INTO pools(cidr) VALUES (?)", (str(net),))

    def list_pools(self) -> List[str]:
        with self._conn() as conn:
            cur = conn.execute("SELECT cidr FROM pools")
            return [row[0] for row in cur.fetchall()]

    def allocate(self, cidr: Optional[str] = None, meta: Optional[str] = None) -> str:
        """Allocate the next free host from a pool (or specific CIDR if provided)."""
        with _lock:
            with self._conn() as conn:
                pools = [cidr] if cidr else [row[0] for row in conn.execute("SELECT cidr FROM pools")]
                if not pools:
                    raise RuntimeError("no pools configured")

                for p in pools:
                    net = ipaddress.ip_network(p)
                    # iterate hosts (skips network/broadcast for IPv4)
                    for host in net.hosts():
                        ip_str = str(host)
                        cur = conn.execute("SELECT 1 FROM allocations WHERE ip = ?", (ip_str,)).fetchone()
                        if cur:
                            continue
                        conn.execute("INSERT INTO allocations(cidr, ip, meta) VALUES (?, ?, ?)", (str(net), ip_str, meta))
                        return ip_str
                raise RuntimeError("no free IPs in pools")

    def release(self, ip: str) -> bool:
        with _lock:
            with self._conn() as conn:
                cur = conn.execute("DELETE FROM allocations WHERE ip = ?", (ip,))
                return cur.rowcount > 0

    def list_allocations(self) -> List[Tuple[str, str, Optional[str]]]:
        with self._conn() as conn:
            cur = conn.execute("SELECT id, ip, meta FROM allocations")
        return cur.fetchall()

    def reset(self) -> None:
        with self._conn() as conn:
            conn.execute("DELETE FROM allocations")


if __name__ == "__main__":
    ipam = IPAM(":memory:")
    ipam.add_pool("10.0.0.0/29")
    print(ipam.allocate())
