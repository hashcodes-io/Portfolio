from ipnet_demo.ipam import IPAM


def test_allocate_and_release(tmp_path):
    db = tmp_path / "test.db"
    ipam = IPAM(str(db))
    ipam.add_pool("192.168.100.0/30")
    ip = ipam.allocate()
    assert ip.startswith("192.168.100.")
    allocations = ipam.list_allocations()
    assert len(allocations) == 1
    assert ipam.release(ip)
    assert len(ipam.list_allocations()) == 0