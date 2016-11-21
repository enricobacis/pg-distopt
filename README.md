# pg-distopt
Optimize PostgreSQL EXPLAIN results on multiple servers

## The Query Plan
pg-distopt takes just two input as files. One of them is the xml query plan produced by PostgreSQL.
We executed the PostgreSQL query optimizer on the [TPC-H](http://www.tpc.org/tpch/) suite and saved
the xml query plan for each query in the [plans](https://github.com/enricobacis/pg-distopt/tree/master/plans)
of this repository.

*plans/03.xml*

    <explain xmlns="http://www.postgresql.org/2009/explain">
      <Query>
        <Plan>
          <Node-Type>Sort</Node-Type>
          <Startup-Cost>364167.12</Startup-Cost>
          <Total-Cost>364954.34</Total-Cost>
          <Plan-Rows>314886</Plan-Rows>
          <Plan-Width>24</Plan-Width>
          <Actual-Startup-Time>4623.411</Actual-Startup-Time>
          <Actual-Total-Time>4626.571</Actual-Total-Time>
          <Actual-Rows>11620</Actual-Rows>
          <Actual-Loops>1</Actual-Loops>
          <Output>
            <Item>lineitem.l_orderkey</Item>
            <Item>(sum((lineitem.l_extendedprice * (1::numeric - lineitem.l_discount))))</Item>
            <Item>orders.o_orderdate</Item>
            <Item>orders.o_shippriority</Item>
          </Output>
          <Sort-Key>
            <Item>(sum((lineitem.l_extendedprice * (1::numeric - lineitem.l_discount))))</Item>
            ....
            
## The Config

The second pg-distopt input is the config file. This lists all the options of the second layer
optimization (the first one is the one performed by PostgreSQL). The idea is to list a
number of servers, with different costs (CPU, IO, transfer, ...).

Each server may be a storage server (that also store some table) or a pure computational
server (which just provides computational power). Each server may be able to see attributes
plaintext or in an encrypted form based on the trust level we have on the server
(normally more trust => more expensive).

*configs/bench07.json*

    {
      "nodes": [
        {
          "name" : "CL1",
          "type" : "client",
          "performance" : { "aes" : 500 },
          "costs" : { "cpu" : 0.0006, "in" : 0.0, "out" : 0.0 },
          "links" : {
            "SS1" : { "throughput" : 100 },
            "CS1" : { "throughput" : 100 }
          },
          "plain" : [
            "c_custkey", "c_name", "c_address", "c_nationkey", "c_phone",
            "c_acctbal", "c_mktsegment", "c_comment",
            "l_orderkey", "l_partkey", "l_suppkey", "l_linenumber",
            "l_quantity", "l_extendedprice", "l_discount", "l_tax",
            "l_returnflag", "l_linestatus", "l_shipdate", "l_commitdate",
            "l_receiptdate", "l_shipinstruct", "l_shipmode", "l_comment",
            "n_nationkey", "n_name", "n_regionkey", "n_comment",
            "o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice",
            "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority",
            "o_comment",
            "p_partkey", "p_name", "p_mfgr", "p_brand", "p_type", "p_size",
            "p_container", "p_retailprice", "p_comment",
            "ps_partkey", "ps_suppkey", "ps_availqty", "ps_supplycost",
            "ps_comment",
            "r_regionkey", "r_name", "r_comment",
            "s_suppkey", "s_name", "s_address", "s_nationkey", "s_phone",
            "s_acctbal", "s_comment"
          ],
          "encrypted" : []
        },
        {
          "name" : "SS1",
          "type" : "storage",
          "performance" : { "aes" : 500 },
          "costs" : { "cpu" : 0.0002, "in" : 0.00001, "out" : 0.00001 },
          "links" : {
            "CL1" : { "throughput" : 100 },
            "CS1" : { "throughput" : 10000 }
          },
          "plain" : [
            "c_custkey", "c_name", "c_address", "c_nationkey", "c_phone",
            "c_acctbal", "c_mktsegment", "c_comment",
            "l_orderkey", "l_partkey", "l_suppkey", "l_linenumber",
            "l_quantity", "l_extendedprice", "l_discount", "l_tax",
            "l_returnflag", "l_linestatus", "l_shipdate", "l_commitdate",
            "l_receiptdate", "l_shipinstruct", "l_shipmode", "l_comment",
            "n_nationkey", "n_name", "n_regionkey", "n_comment",
            "o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice",
            "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority",
            "o_comment",
            "p_partkey", "p_name", "p_mfgr", "p_brand", "p_type", "p_size",
            "p_container", "p_retailprice", "p_comment",
            "ps_partkey", "ps_suppkey", "ps_availqty", "ps_supplycost",
            "ps_comment",
            "r_regionkey", "r_name", "r_comment",
            "s_suppkey", "s_name", "s_address", "s_nationkey", "s_phone",
            "s_acctbal", "s_comment"
          ],
          "encrypted" : []
        },
        {
          "name" : "CS1",
          "type" : "computational",
          "performance" : { "aes" : 500 },
          "costs" : { "cpu" : 0.00006, "in" : 0.00001, "out" : 0.00001 },
          "links" : {
            "CL1" : { "throughput" : 100 },
            "SS1" : { "throughput" : 10000 }
          },
          "plain" : [],
          "encrypted" : [
            "c_custkey", "c_name", "c_address", "c_nationkey", "c_phone",
            "c_acctbal", "c_mktsegment", "c_comment",
            "l_orderkey", "l_partkey", "l_suppkey", "l_linenumber",
            "l_quantity", "l_extendedprice", "l_discount", "l_tax",
            "l_returnflag", "l_linestatus", "l_shipdate", "l_commitdate",
            "l_receiptdate", "l_shipinstruct", "l_shipmode", "l_comment",
            "n_nationkey", "n_name", "n_regionkey", "n_comment",
            "o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice",
            "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority",
            "o_comment",
            "p_partkey", "p_name", "p_mfgr", "p_brand", "p_type", "p_size",
            "p_container", "p_retailprice", "p_comment",
            "ps_partkey", "ps_suppkey", "ps_availqty", "ps_supplycost",
            "ps_comment",
            "r_regionkey", "r_name", "r_comment",
            "s_suppkey", "s_name", "s_address", "s_nationkey", "s_phone",
            "s_acctbal", "s_comment"
          ]
        }
      ]
    }
    
Here we have the client (which can of course see all columns plaintext), the
storage server (which can see columns plaintext) and a computational server
which is cheaper than the storage server but can see columns only in an 
encrypted form.

## The algorithm

pg-distopt takes a plan and a configuration and tries to minimize the cost
of executing the plan in the environment described in the configuration.
It must also compute transfer cost (when data is transfered from a server
to an other)and  encryption cost (when data must be encrypted/decrypted)
prior to a transfer to a server with a different trust level.

## Examples

    $ python distopt/main.py  plans/03.xml configs/bench07.json
    1 plans and 1 configs provided
    
    ============================== PLAN plans/03.xml ===============================
    ------------------------------------- TREE -------------------------------------
    1: Sort [Time: 20.368]
        2: Aggregate [Time: 25.598]
            3: Sort [Time: 34.589]
                4: Nested Loop [Time: 3197.51]
                    5: Hash Join [Time: 625.971]
                        6: Seq Scan [Time: 649.887]
                        7: Hash [Time: 12.471]
                            8: Seq Scan [Time: 60.155]
                    9: Index Scan [Time: 0.021]

    -------------------------- BENCH configs/bench07.json --------------------------
    ('Best cost:', 0.0004134287631088)
    ----------------------------------- DISTPLAN -----------------------------------
    Sort [Server: CS1, Cost: 1.22208e-06, Size: 0.755726 MB, Transfer: 1.25451e-05, Encryption: 0]
        Aggregate [Server: CS1, Cost: 1.53588e-06, Size: 0.755726 MB, Transfer: 0, Encryption: 0]
            Sort [Server: CS1, Cost: 2.07534e-06, Size: 0.755726 MB, Transfer: 0, Encryption: 0]
                Nested Loop [Server: CS1, Cost: 0.000191851, Size: 0.755726 MB, Transfer: 0, Encryption: 0]
                    Hash Join [Server: CS1, Cost: 3.75583e-05, Size: 0.175228 MB, Transfer: 0, Encryption: 0]
                        Seq Scan [Server: SS1, Cost: 0.000129977, Size: 1.157 MB, Transfer: 2.31701e-05, Encryption: 4.628e-07]
                        Hash [Server: CS1, Cost: 7.4826e-07, Size: 0.012116 MB, Transfer: 0, Encryption: 0]
                            Seq Scan [Server: SS1, Cost: 1.2031e-05, Size: 0.012116 MB, Transfer: 2.42635e-07, Encryption: 4.8464e-09]
                    Index Scan [Server: SS1, Cost: 4.2e-09, Size: 1.28e-05 MB, Transfer: 2.56333e-10, Encryption: 5.12e-12]
                    
----

You may also use wildcard (as long as they are enclosed in double quotes) to optimize on multiple plans/configurations.

    python distopt/main.py  plans/03.xml "configs/*"
    python distopt/main.py  "plans/*" configs/bench07.json
    python distopt/main.py  "plans/*" "configs/*"
