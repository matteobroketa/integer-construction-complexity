#!/usr/bin/env python3
"""Exact verification for Unit-Cost Binary--Ternary Construction.

All arithmetic is exact integer arithmetic. No floating-point comparisons are
used in theorem checks. Decimal approximations printed at the end are display
only.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from typing import Iterable
import csv
import math
import sys
sys.setrecursionlimit(20000)

D=(2,3)

@lru_cache(maxsize=None)
def C(n:int)->int:
    if n<=1:
        return 0
    best=n-1
    q,r=divmod(n,2)
    best=min(best,r+1+C(q))
    if n>=3:
        q,r=divmod(n,3)
        best=min(best,r+1+C(q))
    return best

def compressed_array(N:int)->list[int]:
    a=[0]*(N+1)
    if N>=1: a[1]=0
    for n in range(2,N+1):
        v=(n%2)+1+a[n//2]
        if n>=3:
            v=min(v,(n%3)+1+a[n//3])
        a[n]=min(n-1,v)
    return a

def forward_dp(N:int)->list[int]:
    a=[0]*(N+1)
    for n in range(2,N+1):
        v=a[n-1]+1
        if n%2==0: v=min(v,a[n//2]+1)
        if n%3==0: v=min(v,a[n//3]+1)
        a[n]=v
    return a

@lru_cache(maxsize=None)
def fixed_residue_cost(n:int,a:int,b:int)->int:
    """Minimum increments when reverse path must use exactly a /2 and b /3.

    Divisions each cost 1 separately. This function returns only the number of
    required -1 steps (equivalently +1 steps forward). Unavailable signatures
    return INF.
    """
    INF=10**9
    if a==0 and b==0:
        return n-1
    best=INF
    if a>0 and n>=2:
        best=min(best,(n%2)+fixed_residue_cost(n//2,a-1,b))
    if b>0 and n>=3:
        best=min(best,(n%3)+fixed_residue_cost(n//3,a,b-1))
    return best

def canonical_signature_cost(m:int,b:int)->tuple[int,int,int,int]|None:
    # Exact integer k_b = ceil(b log_2 3) without floating point:
    # minimal k with 3^b <= 2^k.
    if b==0:
        return (m,0,0,m)
    p3=3**b
    k=(p3-1).bit_length()  # ceil(log2(p3)); p3 is never power of 2 for b>0
    a=m-k
    if a<0:
        return None
    c=fixed_residue_cost(1<<m,a,b)
    if c>=10**9:
        return None
    return (a,b,c,a+b+c)

BLOCKS=[(81,2),(27,1),(3,1),(6,1),(9,1),(18,1),(36,1),(18,1),(12,1),(81,1),(3,2),(3,1),(6,1),(81,1)]

def factor23(M:int)->list[int]:
    out=[]
    while M%2==0:
        out.append(2); M//=2
    while M%3==0:
        out.append(3); M//=3
    assert M==1
    return out

def primitive_certificate()->tuple[list[str],list[int]]:
    x=1; ops=[]; vals=[x]
    for M,r in BLOCKS:
        for d in factor23(M):
            x*=d; ops.append(f"*{d}"); vals.append(x)
        for _ in range(r):
            x+=1; ops.append("+1"); vals.append(x)
    return ops,vals

def transition_rows(lo:int=45,hi:int=60):
    rows=[]
    for m in range(lo,hi+1):
        n=1<<m
        cm=C(n)
        b2=1+C(n//2)
        b3=(n%3)+1+C(n//3)
        first=[]
        if b2==cm:first.append('/2')
        if b3==cm:first.append('/3')
        rows.append((m,cm,m-cm,b2,b3,','.join(first)))
    return rows

def main():
    here=Path(__file__).resolve().parent
    print("1) Independent finite-range cross-check through 1,000,000")
    N=1_000_000
    ca=compressed_array(N)
    fd=forward_dp(N)
    assert ca==fd
    print("   PASS: compressed recurrence == independent forward DP for every n <= 1,000,000")

    print("2) First power-of-two shortcut")
    for m in range(1,54):
        assert C(1<<m)==m,(m,C(1<<m))
    assert C(1<<54)==53
    print("   PASS: C(2^m)=m for 1<=m<=53; C(2^54)=53")

    print("3) Canonical operation-count signature at 2^54")
    sigs=[]
    for b in range(0,55):
        z=canonical_signature_cost(54,b)
        if z and z[3]==53:
            sigs.append(z[:3])
    assert sigs==[(8,29,16)],sigs
    print("   PASS: unique canonical normalized 53-step signature is (a,b,c)=(8,29,16)")

    print("4) Explicit primitive certificate")
    ops,vals=primitive_certificate()
    assert len(ops)==53
    assert vals[-1]==1<<54
    assert ops.count('*2')==8 and ops.count('*3')==29 and ops.count('+1')==16
    print("   PASS: 53 primitive operations reach 2^54 exactly (8 *2, 29 *3, 16 +1)")
    with open(here/'primitive-certificate.txt','w') as f:
        f.write('Primitive 53-operation certificate for 2^54\n')
        f.write('Start: 1\n')
        for i,(op,v) in enumerate(zip(ops,vals[1:]),1):
            f.write(f'{i:2d}. {op:>2s} -> {v}\n')
        f.write(f'End: {vals[-1]} = 2^54\n')

    print("5) Transition table 45<=m<=60")
    rows=transition_rows()
    with open(here/'transition-table.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['m','C(2^m)','defect','reverse_/2_branch','reverse_/3_branch','optimal_first_branch']); w.writerows(rows)
    print("   PASS: wrote transition-table.csv")

    print("6) Record defects through m=1600")
    records=[]; r=-1
    for m in range(1,1601):
        d=m-C(1<<m)
        if d>r:
            records.append((m,d,C(1<<m))); r=d
    expected=[(1,0,1),(54,1,53),(126,2,124),(1008,3,1005),(1028,4,1024)]
    assert records==expected,records
    print("   PASS:",records)

    print("7) Mersenne reduction identity through m=300")
    running=0
    for m in range(1,301):
        running=max(running,m-1-C((1<<m)-1))
        assert m-C(1<<m)==max(0,running)
    print("   PASS: delta(m)=max_{k<=m}(k-1-C(2^k-1)) through m=300")

    print("8) Selected fixed-tripling profiles")
    checks=[
      (54,8,29,16,53),
      (126,18,68,38,124),
      (966,183,494,288,965),
      (996,213,494,287,994),
      (1008,225,494,286,1005),
      (1028,245,494,285,1024),
    ]
    with open(here/'fixed-count-profiles.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['m','doublings_a','triplings_b','min_increments_c','total_cost','defect'])
        for m,a,b,c,total in checks:
            got=fixed_residue_cost(1<<m,a,b)
            assert got==c,(m,a,b,got,c)
            assert a+b+c==total
            w.writerow([m,a,b,c,total,m-total])
    print("   PASS: selected exact profiles reproduced")

    print("9) Local 2/3 swap table")
    vals=[]
    for q in range(6):
        A=(q%2)+((q//2)%3)
        B=(q%3)+((q//3)%2)
        vals.append(A-B)
    assert vals==[0,0,-1,1,0,0],vals
    print("   PASS: kappa residues = [0,0,-1,+1,0,0] for q mod 6")

    print("10) 3-adic runway at m=54")
    n=(1<<54)-1
    count=0
    while n%3==0:
        n//=3; count+=1
    assert count==4
    for m in range(2,54,2):
        x=(1<<m)-1; c=0
        while x%3==0: x//=3; c+=1
        assert c<4
    print("   PASS: v3(2^54-1)=4 and no smaller positive even m has v3>=4")

    print("\nAll exact verification checks passed.")
    print(f"Memoized scalar states currently cached: {C.cache_info().currsize}")

if __name__=='__main__':
    main()
