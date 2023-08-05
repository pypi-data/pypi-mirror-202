import bgpkit
for item in bgpkit.Broker().query(ts_start="2014-04-01 00:00:01", ts_end="2014-04-01 00:04:59", project="riperis", data_type="update", print_url=True):
    elems = bgpkit.Parser(url=item.url,cache_dir="/tmp/data_bgpkit/").parse_all()
    print(f"{item.collector_id} - {len(elems)}")
